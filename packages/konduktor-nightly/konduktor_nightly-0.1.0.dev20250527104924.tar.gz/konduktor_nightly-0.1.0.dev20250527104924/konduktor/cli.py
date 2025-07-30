# Proprietary Changes made for Trainy under the Trainy Software License
# Original source: skypilot: https://github.com/skypilot-org/skypilot
# which is Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The 'konduktor' command line tool.

Example usage:

  # See available commands.
  >> konduktor

  # Run a task, described in a yaml file.
  >> konduktor launch task.yaml

  # Show the list of scheduled jobs
  >> konduktor status

  # Tear down a specific job.
  >> konduktor down cluster_name

  # Tear down all scheduled jobs
  >> konduktor down -a

NOTE: the order of command definitions in this file corresponds to how they are
listed in "konduktor --help".  Take care to put logically connected commands close to
each other.
"""

import os
import shlex
from typing import Any, Dict, List, Optional, Tuple

import click
import colorama
import dotenv
import prettytable
import yaml
from rich.progress import track

import konduktor
from konduktor import check as konduktor_check
from konduktor import logging
from konduktor.backends import jobset_utils
from konduktor.utils import (
    common_utils,
    kubernetes_utils,
    log_utils,
    loki_utils,
    ux_utils,
)

_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

logger = logging.get_logger(__name__)


def _parse_env_var(env_var: str) -> Tuple[str, str]:
    """Parse env vars into a (KEY, VAL) pair."""
    if '=' not in env_var:
        value = os.environ.get(env_var)
        if value is None:
            raise click.UsageError(f'{env_var} is not set in local environment.')
        return (env_var, value)
    ret = tuple(env_var.split('=', 1))
    if len(ret) != 2:
        raise click.UsageError(
            f'Invalid env var: {env_var}. Must be in the form of KEY=VAL ' 'or KEY.'
        )
    return ret[0], ret[1]


def _merge_env_vars(
    env_dict: Optional[Dict[str, str]], env_list: List[Tuple[str, str]]
) -> List[Tuple[str, str]]:
    """Merges all values from env_list into env_dict."""
    if not env_dict:
        return env_list
    for key, value in env_list:
        env_dict[key] = value
    return list(env_dict.items())


def _make_task_with_overrides(
    entrypoint: Tuple[str, ...],
    *,
    entrypoint_name: str = 'konduktor.Task',
    name: Optional[str] = None,
    workdir: Optional[str] = None,
    cloud: Optional[str] = None,
    gpus: Optional[str] = None,
    cpus: Optional[str] = None,
    memory: Optional[str] = None,
    instance_type: Optional[str] = None,
    num_nodes: Optional[int] = None,
    image_id: Optional[str] = None,
    disk_size: Optional[int] = None,
    env: Optional[List[Tuple[str, str]]] = None,
    field_to_ignore: Optional[List[str]] = None,
) -> konduktor.Task:
    """Creates a task from an entrypoint with overrides.

    Returns:
        konduktor.Task
    """
    entrypoint = ' '.join(entrypoint)
    is_yaml, _ = _check_yaml(entrypoint)
    entrypoint: Optional[str]
    if is_yaml:
        # Treat entrypoint as a yaml.
        click.secho(f'{entrypoint_name} from YAML spec: ', fg='yellow', nl=False)
        click.secho(entrypoint, bold=True)
    else:
        if entrypoint is not None and len(entrypoint) == 0:
            raise ValueError(
                'no entrypoint specified, run with \n' '`konduktor launch task.yaml'
            )
        raise ValueError(f'{entrypoint} is not a valid YAML spec,')

    override_params = _parse_override_params(
        gpus=gpus,
        cpus=cpus,
        memory=memory,
        image_id=image_id,
        disk_size=disk_size,
    )

    if field_to_ignore is not None:
        _pop_and_ignore_fields_in_override_params(override_params, field_to_ignore)

    assert entrypoint is not None
    task_configs = common_utils.read_yaml_all(entrypoint)
    assert len(task_configs) == 1, 'Only single tasks are supported'
    task = konduktor.Task.from_yaml_config(task_configs[0], env)
    # Override.
    if workdir is not None:
        task.workdir = workdir

    task.set_resources_override(override_params)

    if num_nodes is not None:
        task.num_nodes = num_nodes
    if name is not None:
        task.name = name
    return task


_TASK_OPTIONS = [
    click.option(
        '--workdir',
        required=False,
        type=click.Path(exists=True, file_okay=False),
        help=(
            'If specified, sync this dir to the remote working directory, '
            'where the task will be invoked. '
            'Overrides the "workdir" config in the YAML if both are supplied.'
        ),
    ),
    click.option(
        '--cloud',
        required=False,
        type=str,
        help=(
            'The cloud to use. If specified, overrides the "resources.cloud" '
            'config. Passing "none" resets the config. [defunct] currently '
            'only supports a single cloud'
        ),
    ),
    click.option(
        '--num-nodes',
        required=False,
        type=int,
        help=(
            'Number of nodes to execute the task on. '
            'Overrides the "num_nodes" config in the YAML if both are '
            'supplied.'
        ),
    ),
    click.option(
        '--cpus',
        default=None,
        type=str,
        required=False,
        help=(
            'Number of vCPUs each instance must have (e.g., '
            '``--cpus=4`` (exactly 4) or ``--cpus=4+`` (at least 4)). '
            'This is used to automatically select the instance type.'
        ),
    ),
    click.option(
        '--memory',
        default=None,
        type=str,
        required=False,
        help=(
            'Amount of memory each instance must have in GB (e.g., '
            '``--memory=16`` (exactly 16GB), ``--memory=16+`` (at least 16GB))'
        ),
    ),
    click.option(
        '--disk-size',
        default=None,
        type=int,
        required=False,
        help=('OS disk size in GBs.'),
    ),
    click.option(
        '--image-id',
        required=False,
        default=None,
        help=(
            'Custom image id for launching the instances. '
            'Passing "none" resets the config.'
        ),
    ),
    click.option(
        '--env-file',
        required=False,
        type=dotenv.dotenv_values,
        help="""\
        Path to a dotenv file with environment variables to set on the remote
        node.

        If any values from ``--env-file`` conflict with values set by
        ``--env``, the ``--env`` value will be preferred.""",
    ),
    click.option(
        '--env',
        required=False,
        type=_parse_env_var,
        multiple=True,
        help="""\
        Environment variable to set on the remote node.
        It can be specified multiple times.
        Examples:

        \b
        1. ``--env MY_ENV=1``: set ``$MY_ENV`` on the cluster to be 1.

        2. ``--env MY_ENV2=$HOME``: set ``$MY_ENV2`` on the cluster to be the
        same value of ``$HOME`` in the local environment where the CLI command
        is run.

        3. ``--env MY_ENV3``: set ``$MY_ENV3`` on the cluster to be the
        same value of ``$MY_ENV3`` in the local environment.""",
    ),
]
_TASK_OPTIONS_WITH_NAME = [
    click.option(
        '--name',
        '-n',
        required=False,
        type=str,
        help=(
            'Task name. Overrides the "name" '
            'config in the YAML if both are supplied.'
        ),
    ),
] + _TASK_OPTIONS
_EXTRA_RESOURCES_OPTIONS = [
    click.option(
        '--gpus',
        required=False,
        type=str,
        help=(
            'Type and number of GPUs to use. Example values: '
            '"V100:8", "V100" (short for a count of 1)'
            'If a new cluster is being launched by this command, this is the '
            'resources to provision. If an existing cluster is being reused, this'
            " is seen as the task demand, which must fit the cluster's total "
            'resources and is used for scheduling the task. '
            'Overrides the "accelerators" '
            'config in the YAML if both are supplied. '
            'Passing "none" resets the config.'
        ),
    ),
]


def _get_click_major_version():
    return int(click.__version__.split('.', maxsplit=1)[0])


_RELOAD_ZSH_CMD = 'source ~/.zshrc'
_RELOAD_BASH_CMD = 'source ~/.bashrc'


def _add_click_options(options: List[click.Option]):
    """A decorator for adding a list of click option decorators."""

    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


def _parse_override_params(
    gpus: Optional[str] = None,
    cpus: Optional[str] = None,
    memory: Optional[str] = None,
    image_id: Optional[str] = None,
    disk_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Parses the override parameters into a dictionary."""
    override_params: Dict[str, Any] = {}
    if gpus is not None:
        if gpus.lower() == 'none':
            override_params['accelerators'] = None
        else:
            override_params['accelerators'] = gpus
    if cpus is not None:
        if cpus.lower() == 'none':
            override_params['cpus'] = None
        else:
            override_params['cpus'] = cpus
    if memory is not None:
        if memory.lower() == 'none':
            override_params['memory'] = None
        else:
            override_params['memory'] = memory
    if image_id is not None:
        if image_id.lower() == 'none':
            override_params['image_id'] = None
        else:
            override_params['image_id'] = image_id
    if disk_size is not None:
        override_params['disk_size'] = disk_size
    return override_params


def _launch_with_confirm(
    task: konduktor.Task,
    *,
    dryrun: bool,
    detach_run: bool,
    no_confirm: bool,
):
    """Launch a cluster with a Task."""

    confirm_shown = False
    if not no_confirm:
        # Prompt if (1) --cluster is None, or (2) cluster doesn't exist, or (3)
        # it exists but is STOPPED.
        prompt = (
            f'Launching a new job {colorama.Style.BRIGHT}'
            f'{colorama.Fore.GREEN}{task.name}{colorama.Style.RESET_ALL}. '
            'Proceed?'
        )
        if prompt is not None:
            confirm_shown = True
            click.confirm(prompt, default=True, abort=True, show_default=True)

    if not confirm_shown:
        click.secho(f'Running task {task.name}...', fg='yellow')
    return konduktor.launch(
        task,
        dryrun=dryrun,
        detach_run=detach_run,
    )


def _check_yaml(entrypoint: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Checks if entrypoint is a readable YAML file.

    Args:
        entrypoint: Path to a YAML file.
    """
    is_yaml = True
    config: Optional[List[Dict[str, Any]]] = None
    result = None
    shell_splits = shlex.split(entrypoint)
    yaml_file_provided = len(shell_splits) == 1 and (
        shell_splits[0].endswith('yaml') or shell_splits[0].endswith('.yml')
    )
    invalid_reason = ''
    try:
        with open(entrypoint, 'r', encoding='utf-8') as f:
            try:
                config = list(yaml.safe_load_all(f))
                if config:
                    result = config[0]
                else:
                    result = {}
                if isinstance(result, str):
                    # 'konduktor exec cluster ./my_script.sh'
                    is_yaml = False
            except yaml.YAMLError as e:
                if yaml_file_provided:
                    logger.debug(e)
                    detailed_error = f'\nYAML Error: {e}\n'
                    invalid_reason = (
                        'contains an invalid configuration. '
                        'Please check syntax.\n'
                        f'{detailed_error}'
                    )
                is_yaml = False

    except OSError:
        if yaml_file_provided:
            entry_point_path = os.path.expanduser(entrypoint)
            if not os.path.exists(entry_point_path):
                invalid_reason = (
                    'does not exist. Please check if the path' ' is correct.'
                )
            elif not os.path.isfile(entry_point_path):
                invalid_reason = (
                    'is not a file. Please check if the path' ' is correct.'
                )
            else:
                invalid_reason = (
                    'yaml.safe_load() failed. Please check if the' ' path is correct.'
                )
        is_yaml = False
    if not is_yaml:
        if yaml_file_provided:
            click.confirm(
                f'{entrypoint!r} looks like a yaml path but {invalid_reason}\n'
                'It will be treated as a command to be run remotely. Continue?',
                abort=True,
            )
    return is_yaml, result


def _pop_and_ignore_fields_in_override_params(
    params: Dict[str, Any], field_to_ignore: List[str]
) -> None:
    """Pops and ignores fields in override params.

    Args:
        params: Override params.
        field_to_ignore: Fields to ignore.

    Returns:
        Override params with fields ignored.
    """
    if field_to_ignore is not None:
        for field in field_to_ignore:
            field_value = params.pop(field, None)
            if field_value is not None:
                click.secho(
                    f'Override param {field}={field_value} is ignored.', fg='yellow'
                )


class _NaturalOrderGroup(click.Group):
    """Lists commands in the order defined in this script.

    Reference: https://github.com/pallets/click/issues/513
    """

    def list_commands(self, ctx):
        return self.commands.keys()

    def invoke(self, ctx):
        return super().invoke(ctx)


class _DocumentedCodeCommand(click.Command):
    """Corrects help strings for documented commands such that --help displays
    properly and code blocks are rendered in the official web documentation.
    """

    def get_help(self, ctx):
        help_str = ctx.command.help
        ctx.command.help = help_str.replace('.. code-block:: bash\n', '\b')
        return super().get_help(ctx)


@click.group(cls=_NaturalOrderGroup, context_settings=_CONTEXT_SETTINGS)
@click.version_option(konduktor.__version__, '--version', '-v', prog_name='konduktor')
@click.version_option(
    konduktor.__commit__,
    '--commit',
    '-c',
    prog_name='konduktor',
    message='%(prog)s, commit %(version)s',
    help='Show the commit hash and exit',
)
def cli():
    pass


@cli.command()
@click.option(
    '--all-users',
    '-u',
    default=False,
    is_flag=True,
    required=False,
    help='Show all clusters, including those not owned by the ' 'current user.',
)
# pylint: disable=redefined-builtin
def status(all_users: bool):
    # NOTE(dev): Keep the docstring consistent between the Python API and CLI.
    """Shows list of all the jobs

    Args:
        all_users (bool): whether to show all jobs
        regardless of the user in this namespace
    """
    context = kubernetes_utils.get_current_kube_config_context_name()
    namespace = kubernetes_utils.get_kube_config_context_namespace(context)
    user = common_utils.user_and_hostname_hash() if not all_users else 'All'
    click.secho(f'User: {user}', fg='green', bold=True)
    click.secho('Jobs', fg='cyan', bold=True)
    jobset_utils.show_status_table(namespace, all_users=all_users)


@cli.command()
@click.option(
    '--status',
    is_flag=True,
    default=False,
    help=(
        'If specified, do not show logs but exit with a status code for the '
        "job's status: 0 for succeeded, or 1 for all other statuses."
    ),
)
@click.option(
    '--follow/--no-follow',
    is_flag=True,
    default=True,
    help=(
        'Follow the logs of a job. '
        'If --no-follow is specified, print the log so far and exit. '
        '[default: --follow]'
    ),
)
@click.option(
    '--tail',
    default=1000,
    type=int,
    help=(
        'The number of lines to display from the end of the log file. '
        'Default is 1000.'
    ),
)
@click.argument('job_id', type=str, nargs=1)
# TODO(zhwu): support logs by job name
def logs(
    status: bool,
    job_id: str,
    follow: bool,
    tail: int,
):
    # NOTE(dev): Keep the docstring consistent between the Python API and CLI.
    """Tail the log of a job."""
    if status:
        raise click.UsageError('`--status` is being deprecated)')

    # Check if the job exists
    if not job_id:
        raise click.UsageError('Please provide a job ID.')

    context = kubernetes_utils.get_current_kube_config_context_name()
    namespace = kubernetes_utils.get_kube_config_context_namespace(context)

    # Verify the job exists before attempting to tail logs
    # TODO(asaiacai): unify the 404 logic under jobset_utils
    try:
        jobset_utils.get_jobset(namespace, job_id)
    except jobset_utils.JobNotFoundError:
        raise click.UsageError(
            f"Job '{job_id}' not found in namespace "
            f"'{namespace}'. Check your jobs with "
            f'{colorama.Style.BRIGHT}`konduktor status`'
            f'{colorama.Style.RESET_ALL}.'
        )

    click.secho(
        'Logs are tailed from 1 hour ago, ' 'to see more logs, check Grafana.',
        fg='yellow',
    )
    loki_utils.tail_loki_logs_ws(job_id, follow=follow, num_logs=tail)


@cli.command(cls=_DocumentedCodeCommand)
@click.argument(
    'entrypoint',
    required=False,
    type=str,
    nargs=-1,
)
@click.option(
    '--dryrun',
    default=False,
    is_flag=True,
    help='If True, do not actually run the job.',
)
@click.option(
    '--detach-run',
    '-d',
    default=False,
    is_flag=True,
    help=(
        'If True, as soon as a job is submitted, return from this call '
        'and do not stream execution logs.'
    ),
)
@_add_click_options(_TASK_OPTIONS_WITH_NAME + _EXTRA_RESOURCES_OPTIONS)
@click.option(
    '--yes',
    '-y',
    is_flag=True,
    default=False,
    required=False,
    # Disabling quote check here, as there seems to be a bug in pylint,
    # which incorrectly recognizes the help string as a docstring.
    # pylint: disable=bad-docstring-quotes
    help='Skip confirmation prompt.',
)
def launch(
    entrypoint: Tuple[str, ...],
    dryrun: bool,
    detach_run: bool,
    name: Optional[str],
    workdir: Optional[str],
    cloud: Optional[str],
    gpus: Optional[str],
    cpus: Optional[str],
    memory: Optional[str],
    num_nodes: Optional[int],
    image_id: Optional[str],
    env_file: Optional[Dict[str, str]],
    env: List[Tuple[str, str]],
    disk_size: Optional[int],
    yes: bool,
):
    """Launch a task.

    If ENTRYPOINT points to a valid YAML file, it is read in as the task
    specification. Otherwise, it is interpreted as a bash command.
    """
    # NOTE(dev): Keep the docstring consistent between the Python API and CLI.
    env = _merge_env_vars(env_file, env)

    task = _make_task_with_overrides(
        entrypoint=entrypoint,
        name=name,
        workdir=workdir,
        cloud=cloud,
        gpus=gpus,
        cpus=cpus,
        memory=memory,
        num_nodes=num_nodes,
        image_id=image_id,
        env=env,
        disk_size=disk_size,
    )

    click.secho(
        f'Considered resources ({task.num_nodes} nodes):', fg='green', bold=True
    )
    table_kwargs = {
        'hrules': prettytable.FRAME,
        'vrules': prettytable.NONE,
        'border': True,
    }
    headers = ['CPUs', 'Mem (GB)', 'GPUs']
    table = log_utils.create_table(headers, **table_kwargs)
    assert task.resources is not None
    table.add_row(
        [task.resources.cpus, task.resources.memory, task.resources.accelerators]
    )
    print(table)

    job_name = _launch_with_confirm(
        task,
        dryrun=dryrun,
        detach_run=detach_run,
        no_confirm=yes,
    )
    click.secho(
        ux_utils.command_hint_messages(ux_utils.CommandHintType.JOB, job_name),
        fg='green',
        bold=True,
    )


@cli.command(cls=_DocumentedCodeCommand)
@click.argument(
    'jobs',
    nargs=-1,
    required=False,
)
@click.option('--all', '-a', default=None, is_flag=True, help='Tear down all jobs.')
@click.option(
    '--yes',
    '-y',
    is_flag=True,
    default=False,
    required=False,
    help='Skip confirmation prompt.',
)
def down(
    jobs: List[str],
    all: Optional[bool],  # pylint: disable=redefined-builtin
    yes: bool,
):
    # NOTE(dev): Keep the docstring consistent between the Python API and CLI.
    """Tear down job(s).

    JOB is the name of the job to tear down.  If both
    JOB and ``--all`` are supplied, the latter takes precedence.

    Tearing down a job will delete all associated containers (all billing
    stops), and any data on the containers disks will be lost.  Accelerators
    (e.g., GPUs) that are part of the job will be deleted too.


    Examples:

    .. code-block:: bash

      # Tear down a specific job.
      konduktor down cluster_name
      \b
      # Tear down multiple clusters.
      konduktor down jobs
      \b
      # Tear down all existing clusters.
      konduktor down -a

    """

    context = kubernetes_utils.get_current_kube_config_context_name()
    namespace = kubernetes_utils.get_kube_config_context_namespace(context)
    if all:
        jobs_specs = jobset_utils.list_jobset(namespace)
        assert jobs_specs is not None, f'No ' f'jobs found in namespace {namespace}'
        assert len(jobs_specs) > 0, f'No ' f'jobs found in namespace {namespace}'
        jobs = [job['metadata']['name'] for job in jobs_specs['items']]
    if not yes:
        # Prompt if (1) --cluster is None, or (2) cluster doesn't exist, or (3)
        # it exists but is STOPPED.
        prompt = (
            f'Tearing down job(s) {colorama.Style.BRIGHT} '
            f'{colorama.Fore.GREEN}{jobs}{colorama.Style.RESET_ALL}. '
            'Proceed?'
        )
        if prompt is not None:
            click.confirm(prompt, default=True, abort=True, show_default=True)

    for job in track(jobs, description='Tearing down job(s)...'):
        jobset_utils.delete_jobset(namespace, job)


@cli.command(cls=_DocumentedCodeCommand)
@click.argument('clouds', required=True, type=str, nargs=-1)
def check(clouds: Tuple[str]):
    """Check which clouds are available to use for storage

    This checks storage credentials for a cloud supported by konduktor. If a
    cloud is detected to be inaccessible, the reason and correction steps will
    be shown.

    If CLOUDS are specified, checks credentials for only those clouds.

    The enabled clouds are cached and form the "search space" to be considered
    for each task.

    Examples:

    .. code-block:: bash

      # Check only specific clouds - gs, s3.
      konduktor check gs
      konduktor check s3
    """
    clouds_arg = clouds if len(clouds) > 0 else None
    konduktor_check.check(clouds=clouds_arg)


def main():
    return cli()


if __name__ == '__main__':
    main()
