"""This module contains the midas command line interface 2.0."""

import sys
from typing import Optional, Tuple

import click

from ..util import runtime_config
from ..util.logging import init_logger, set_and_init_logger
from . import fnc_analyze, fnc_configure, fnc_download, fnc_list, fnc_run


@click.group(invoke_without_command=True)
@click.option(
    "--config",
    "-c",
    type=click.Path(),
    help=(
        "Supply custom runtime configuration file. If used together with "
        "autocfg and no config is present at the given path, a new default "
        "config will be created. (Default search path: %s)"
        % runtime_config.CONFIG_FILE_PATHS
    ),
)
@click.option(
    "--verbose",
    "-v",
    count=True,
    help=(
        "Increase program verbosity, can be given numerous times: "
        "-v prints also INFO messages, and -vv emits DEBUG output."
    ),
)
@click.option(
    "--logfile",
    "-l",
    type=click.Path(
        file_okay=True,
        dir_okay=True,
        allow_dash=True,
        writable=True,
        resolve_path=True,
    ),
    help=(
        "Specify a differnt logfile where logs are stored for this "
        "execution."
    ),
    default=None,
)
def main(config=None, verbose=0, logfile=None):
    if config:
        try:
            with open(config, "r") as fp:
                runtime_config.RuntimeConfig().load(fp)
        except OSError as err:
            click.echo(
                "ERROR: Could not load config from %s: %s." % (config, err)
            )
            exit(1)
    else:
        try:
            runtime_config.RuntimeConfig()
        except FileNotFoundError as err:
            click.echo(
                "Please create a runtime config. %s.\n"
                "Will continue with built-in defaults. " % err,
                file=sys.stderr,
            )
    if logfile is not None:
        set_and_init_logger(verbose, "cli-logfile", logfile)
    else:
        init_logger(verbose)


@main.command()
@click.option(
    "--autocfg",
    "-a",
    is_flag=True,
    help=(
        "Skip ini dialog and apply defaults or use inipath and datapath"
        " if provided with this command."
    ),
)
@click.option(
    "--config-path",
    "-c",
    "config_path",
    type=click.Path(),
    help=(
        "Supply a path for the runtime configuration file to skip the "
        "corresponding prompt."
    ),
)
@click.option(
    "--data-path",
    "-d",
    "data_path",
    type=click.Path(),
    help=(
        "Specify the path to the datasets to skip the corresponding prompt."
    ),
)
@click.option(
    "--scenario-path",
    "-s",
    "scenario_path",
    type=click.Path(),
    help=(
        "Specify the path to the scenario directory to skip the corresponding"
        " prompt."
    ),
)
@click.option(
    "--output-path",
    "-o",
    "output_path",
    type=click.Path(),
    help=(
        "Specify the path to the output directory to skip the corresponding"
        " prompt."
    ),
)
@click.option(
    "--update",
    "-u",
    is_flag=True,
    help="Loading the newst DEFAULT_RUN_TIME_CONFIG",
)
def configure(**kwargs):
    fnc_configure.configure(
        autocfg=kwargs.get("autocfg", False),
        update=kwargs.get("update", False),
        config_path=kwargs.get("config_path", None),
        data_path=kwargs.get("data_path", None),
        scenario_path=kwargs.get("scenario_path", None),
        output_path=kwargs.get("output_path", None),
    )


@main.command()
@click.option(
    "-k",
    "--keep-tmp",
    "keep_tmp",
    is_flag=True,
    help="Keep the temporarily downloaded files.",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Download the datasets and ignore existing ones.",
)
@click.option(
    "-m",
    "--module",
    multiple=True,
    help=(
        "Specify a module to download. Other modules will be skipped. "
        "Can be given numerous times."
    ),
)
def download(keep_tmp: bool, force: bool, module: Optional[Tuple[str]]):
    click.echo("Start downloading...")
    fnc_download.download(keep_tmp, force, module)
    click.echo("Download complete.")


@main.command()
@click.argument("scenario_name")
@click.option(
    "--config",
    "-c",
    multiple=True,
    type=click.Path(
        exists=True,
        readable=True,
        dir_okay=True,
        file_okay=True,
        allow_dash=True,
    ),
    help=(
        "Provide a custom (scenario-)config file. Providing a scenario"
        " name is still required "
    ),
)
@click.option(
    "--db-file",
    "-df",
    "db_file",
    help=(
        "Specify a database file. Temporarily overwrites the scenario "
        "file settings. The -nd flag is ignored."
    ),
)
@click.option(
    "--end",
    "-e",
    default=None,
    type=int,
    help="Specify the number of simulation steps mosaik should perform.",
)
@click.option(
    "--no-db",
    "-nd",
    "no_db",
    is_flag=True,
    help=(
        "Disable the database. Default behavior is to use the settings"
        " of the scenario file."
    ),
)
@click.option(
    "--no-rng",
    "-nr",
    "no_rng",
    is_flag=True,
    help="Globally disable random number generator in the simulation.",
)
@click.option(
    "--port", "-p", default=5555, type=int, help="Specify the port for mosaik."
)
@click.option(
    "--seed", "-s", type=int, help="Set a positive integer as random seed."
)
@click.option(
    "--silent",
    "-q",
    is_flag=True,
    help="Pass the silent flag to mosaik to suppress mosaik output",
)
@click.option(
    "--skip-configure",
    "skip_configure",
    is_flag=True,
    help="Skip the auto-configuration.",
)
@click.option(
    "--skip-download", "skip_download", is_flag=True, help="Skip download"
)
def run(scenario_name, config=None, **kwargs):
    if not scenario_name:
        click.echo(
            "WARNING: No scenario name provided. Rerun the command with\n\n\t"
            "midasctl run demo\n\nto run the demo scenario or replace 'demo' "
            "with any other scenario you\n"
            "like (see 'Scenarios' in the docs)."
        )
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()
    # click.echo(kwargs)ss

    # Process additional cli options
    params = dict()

    db_file = kwargs.get("db_file", None)
    if db_file is not None:
        if not db_file.endswith(".hdf5"):
            db_file = f"{db_file}.hdf5"
        params["no_db"] = False
        params["store_params"] = {"filename": db_file}
    else:
        params["no_db"] = kwargs.get("no_db", False)

    # Mosaik options and port number
    port = kwargs.get("port", 5555)
    try:
        port = int(port)
    except ValueError:
        click.echo(f"Port {port} is not an integer. Using default port 5555.")
        port = 5555
    params["mosaik_params"] = {"addr": ("127.0.0.1", port)}
    params["silent"] = kwargs.get("silent", False)
    end = kwargs.get("end", None)
    if end is not None:
        params["end"] = end

    # Seeds and rng
    seed = kwargs.get("seed", None)
    if seed is not None:
        try:
            seed = abs(int(seed))
        except ValueError:
            click.echo(
                f"Seed {seed} is not an integer. Seed will be random, then!"
            )
            seed = "random"
        params["seed"] = seed
    params["deny_rng"] = kwargs.get("no_rng", False)

    fnc_run.run(
        scenario_name,
        params,
        config,
        skip_configure=kwargs.get("skip_configure", False),
        skip_download=kwargs.get("skip_download", False),
    )


@main.command()
@click.argument(
    "scenario_db_path",
    type=click.Path(
        exists=False,
        readable=True,
        file_okay=True,
        dir_okay=False,
        allow_dash=True,
    ),
)
@click.option(
    "--output-folder",
    "-o",
    "output_folder",
    default="",
    help=(
        "Specify the folder where to store the analysis results. "
        "If not provided, the default output folder is used."
    ),
)
@click.option(
    "--from-step",
    "-s",
    "start",
    type=click.INT,
    default=0,
    help="Specify the first step to be included in the analysis.",
)
@click.option(
    "--to-step",
    "-e",
    "end",
    type=click.INT,
    default=-1,
    help="Specify the last step to be included in the analysis.",
)
@click.option(
    "--step-size",
    "-ss",
    "step_size",
    type=click.INT,
    default=900,
    help="Specify the step size used in the given database.",
)
@click.option(
    "--full", "-f", is_flag=True, help="Enable full report: More plot outputs."
)
def analyze(scenario_db_path, output_folder, start, end, step_size, full):
    if start >= end and end != -1:
        click.echo(
            "Value for start must be lower than the value for end. "
            "Will use the default values."
        )
        start = 0
        end = -1
    fnc_analyze.analyze(
        scenario_db_path, output_folder, start, end, step_size, full
    )


@main.command()
@click.option(
    "--config",
    "-c",
    multiple=True,
    type=click.Path(
        exists=True,
        readable=True,
        dir_okay=True,
        file_okay=True,
        allow_dash=True,
    ),
    help=(
        "Provide a custom (scenario-)config file. Providing a scenario"
        " name is still required "
    ),
)
def list_scenarios(config):
    fnc_list.list_scenarios(config)


@main.command()
@click.argument("scenario_name")
@click.option(
    "--config",
    "-c",
    multiple=True,
    type=click.Path(
        exists=True,
        readable=True,
        dir_okay=True,
        file_okay=True,
        allow_dash=True,
    ),
)
@click.option(
    "--sensors",
    "-s",
    is_flag=True,
    help="Print sensor information in the terminal.",
)
@click.option(
    "--actuators",
    "-a",
    is_flag=True,
    help="Print actuator information in the terminal.",
)
@click.option(
    "--keyword",
    "-k",
    multiple=True,
    help=(
        "If provided, only sensors/actuators containing a keyword will be"
        " printed. Can be given numerous times."
    ),
)
@click.option(
    "--negative-keyword",
    "-n",
    "negative_keyword",
    multiple=True,
    help=(
        "If provided, only sensors/actuators not containing a keyword will be"
        " printed. Can be given numerous times."
    ),
)
@click.option("--prefix", "-p", help="Prefix to add to each sensor/actuator")
def show(
    scenario_name,
    config,
    sensors=False,
    actuators=False,
    keyword=None,
    negative_keyword=None,
    prefix=None,
):
    if keyword is None:
        keyword = []
    if negative_keyword is None:
        negative_keyword = []
    if prefix is None:
        prefix = ""
    fnc_list.show(
        scenario_name,
        config,
        sensors,
        actuators,
        keyword,
        negative_keyword,
        prefix,
    )


if __name__ == "__main__":
    main(obj={})
