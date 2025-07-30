import logging
import os
import shutil
from copy import deepcopy
from typing import Any, Dict, Optional

import click
from ruamel.yaml import YAML

from .. import __version__ as midas_version
from ..util import runtime_config

LOG = logging.getLogger("midas.api")

DIALOG_1 = "#############\n# MIDAS CLI #\n#############"
DIALOG_2 = (
    "# STEP 1 #\n"
    "It seems you're using MIDAS for the first time. We need to perform a "
    "short\nsetup. MIDAS will create a directory in your user config directory"
    ". This\ndirectory will be used to store a runtime configuration file, "
    "data sets, and\nscenario files. Alternatively, the current directory can "
    "be used. However, ie,\neverytime you change the directory and start MIDAS"
    ", this dialog will pop up\nagain.\n"
    "Do you want to create a MIDAS directory in your user config directory: \n"
    f"\n{runtime_config.CONFIG_FILE_PATHS[1]}\n\nto store the configuration "
    "file (y|n)?"
)
DIALOG_3 = (
    "# STEP 2 #\n"
    "MIDAS will download the data sets required by certain modules. By default"
    ", the\nMIDAS directory, created in the first step, will be used. You may "
    "define a\ndifferent path. "
    "Default path is:\n"
)
DIALOG_4 = (
    "\nDo you want to use the default location (y|.|<any path you like>)?"
)

DIALOG_5 = (
    "# STEP 3 #\n"
    "MIDAS will look for scenario files in two different locations. First,\n"
    "internally where the default scenarios are stored. Second, in the MIDAS\n"
    "scenario directory, which will be created in this step. The default path "
    "is:\n"
)
DIALOG_6 = (
    "\nDo you want to use the default location (y|.|<any path you like>)?"
)

DIALOG_7 = (
    "# STEP 4 #\n"
    "Output files created by MIDAS will usually be stored in a new directory "
    "called\n'_outputs' that will be created in the current working directory "
    "on each start.\nAlternatively, you can define an absolute path so all "
    "outputs end in the same\ndirectory on your system.\n"
)
DIALOG_8 = (
    "Type 'y' if you want to keep this setting or type any path that you like "
    "to be\nthe output location (y|<any absolute path you like>):"
)
DIALOG_9 = (
    "# SETUP FINISHED #\n"
    "All above settings can be changed in the midas-runtime-config.yml file.\n"
)

YES = ["y", "j", "yes", "ja", "Y", "J", "Yes", "Ja", "YES", "JA"]
NO = ["n", "no", "nein", "N", "No", "Nein", "NO", "NEIN"]


def configure(
    autocfg: bool = False,
    update: bool = False,
    config_path: str | None = None,
    data_path: str | None = None,
    scenario_path: str | None = None,
    output_path: str | None = None,
) -> bool:
    new_config_path: str = get_implicit_new_config_path(config_path)

    # If one of the parameters is provided, we assume a change
    param_changed = any(
        p is not None
        for p in [config_path, data_path, scenario_path, output_path]
    )
    recreate = False

    if (
        runtime_config.RuntimeConfig().version == "not_defined"
        and os.path.exists(new_config_path)
    ):
        recreate = True
        # new_config_path = get_implicit_new_config_path(new_config_path)

        click.echo("Complete reconfiguration required!")

    if (
        autocfg
        and not update
        and os.path.isfile(new_config_path)
        and not param_changed
        and not recreate
    ):
        # A runtime config exists and since we're in autoconfig mode
        # and have no changes to process, just do nothing
        return False

    default_conf = deepcopy(runtime_config.DEFAULT_BASE_CONFIG)

    # Get paths
    new_data_path: str
    new_scenario_path: str
    new_output_path: str

    # If update then try to re-use most previous settings for paths and
    # logging, modules, and misc
    if recreate:
        LOG.warning("Found old configuration. Recreation required.")
        new_data_path = _get_auto_new_data_path(data_path, restore=True)
        new_scenario_path = runtime_config.RuntimeConfig().paths[
            "scenario_path"
        ]
        new_output_path = runtime_config.RuntimeConfig().paths["output_path"]

        try:
            shutil.move(new_config_path, f"{new_config_path}.bak")
        except FileNotFoundError:
            # Was already moved
            pass
        config_dir = os.path.split(new_config_path)[0]
        try:
            shutil.move(
                os.path.join(config_dir, "midas_data"),
                os.path.join(config_dir, "backup_canbedeleted"),
            )
        except FileNotFoundError:
            # Was already moved
            pass
        try:
            shutil.move(
                os.path.join(config_dir, "midas_scenarios"),
                os.path.join(config_dir, "check_and_delete"),
            )
        except FileNotFoundError:
            # Was already moved
            pass
        LOG.warning(
            "Recreation finished. Check the config path at %s to restore or "
            "delete any redundant files.",
            config_dir,
        )
    elif update:
        LOG.info(
            "Update was chosen. "
            "Updating only critical parts of the configuration ..."
        )
        if os.path.isfile(new_config_path):
            bak_config_file = f"{new_config_path}.bak"
            LOG.debug(f"Backing up old file to {bak_config_file}")
            shutil.copyfile(new_config_path, bak_config_file)

        LOG.debug("Restoring previous path definitions ...")
        new_data_path = _get_auto_new_data_path(data_path, restore=True)
        new_scenario_path = _get_auto_new_scenario_path(
            scenario_path, restore=True
        )
        new_output_path = _get_auto_new_output_path(output_path, restore=True)

        LOG.debug("Restoring previous logging configurations ...")
        _restore_logging(default_conf)

        LOG.debug("Restoring previous custom modules")
        # default_conf["custom_modules"] = deepcopy(
        #     runtime_config.RuntimeConfig().modules["custom_modules"]
        # )

        LOG.debug("Restoring other configurations ...")
        default_conf["misc"] = dict(
            deepcopy(runtime_config.RuntimeConfig().misc)
        )

    elif autocfg:
        # Auto configuration takes provided parameter paths
        # automatically and uses defaults where no path is provided
        LOG.info("Auto configuration was chosen.")
        new_data_path = _get_auto_new_data_path(data_path)
        new_scenario_path = _get_auto_new_scenario_path(scenario_path)
        new_output_path = _get_auto_new_output_path(output_path)
    else:
        LOG.info("Manual configuration was chosen. See terminal prompts.")
        new_config_path = _show_config_dialog(config_path, new_config_path)
        new_data_path = _show_data_dialog(data_path, new_config_path)
        new_scenario_path = _show_scenario_dialog(
            scenario_path, new_config_path
        )
        new_output_path = _show_output_dialog(output_path)

    _create_directories(
        new_config_path, new_data_path, new_scenario_path, new_output_path
    )

    default_conf["paths"]["data_path"] = new_data_path
    default_conf["paths"]["scenario_path"] = new_scenario_path
    default_conf["paths"]["output_path"] = new_output_path
    default_conf["version"] = midas_version
    yml = YAML(typ="safe", pure=True)

    with open(new_config_path, "w") as cfg_out:
        yml.indent(mapping=2, sequence=4, offset=2)
        yml.dump(default_conf, cfg_out)

    runtime_config.RuntimeConfig().reset()
    runtime_config.RuntimeConfig().load(new_config_path)

    default_scenarios_path = os.path.abspath(
        os.path.join(__file__, "..", "..", "scenario", "default_scenarios")
    )
    for f in os.listdir(default_scenarios_path):
        src = os.path.join(default_scenarios_path, f)
        dst = os.path.join(new_scenario_path, f)
        shutil.copyfile(src, dst)

    # click.echo(default_scenarios_path)

    return True


def get_implicit_new_config_path(config_path: str | None) -> str:
    new_config_path: Optional[str] = None

    # Get config path either from parameter or from default
    if config_path is not None:
        new_config_path = os.path.abspath(os.path.expanduser(config_path))

        if os.path.isfile(new_config_path):
            LOG.debug(
                "Config path was provided. Reloading runtime configuration "
                f"from {new_config_path}"
            )
            runtime_config.RuntimeConfig().reset()
            runtime_config.RuntimeConfig().load(new_config_path)
    else:
        new_config_path = runtime_config.RuntimeConfig()._config_file_path
        if new_config_path is None or new_config_path == "(DEFAULT)":
            new_config_path = runtime_config.CONFIG_FILE_PATHS[1]

    LOG.info(f"Using runtime config at {new_config_path}.")
    return new_config_path


def _get_auto_new_data_path(
    data_path: Optional[str], restore: bool = False
) -> str:
    new_data_path: str

    if restore and data_path is None:
        new_data_path = runtime_config.RuntimeConfig().paths["data_path"]
    elif data_path is None:
        # No data path provided so get the default value
        new_data_path = runtime_config.DEFAULT_BASE_CONFIG["paths"][
            "data_path"
        ]
    else:
        # Data path should be absolute to prevent redundant
        # downloads
        new_data_path = os.path.abspath(os.path.expanduser(data_path))

    return new_data_path


def _get_auto_new_scenario_path(
    scenario_path: Optional[str], restore: bool = False
) -> str:
    new_scenario_path: str

    if restore and scenario_path is None:
        new_scenario_path = runtime_config.RuntimeConfig().paths[
            "scenario_path"
        ]
    elif scenario_path is None:
        new_scenario_path = runtime_config.DEFAULT_BASE_CONFIG["paths"][
            "scenario_path"
        ]
    else:
        # Scenario path should be "as-is" because a per-project
        # scenario path might be desired
        new_scenario_path = os.path.expanduser(scenario_path)

    return new_scenario_path


def _get_auto_new_output_path(
    output_path: Optional[str], restore: bool = False
) -> str:
    new_output_path: str

    if restore and output_path is None:
        new_output_path = runtime_config.RuntimeConfig().paths["output_path"]
    elif output_path is None:
        new_output_path = runtime_config.DEFAULT_BASE_CONFIG["paths"][
            "output_path"
        ]
    else:
        # Output path should be "as-is" because a per-project
        # output path might be desired
        new_output_path = output_path

    return new_output_path


def _show_config_dialog(
    config_path: Optional[str], default_conf_path: str
) -> str:
    if config_path is None:
        click.echo(DIALOG_1)
        rsp: str = click.prompt(DIALOG_2, default="y")
        if rsp in YES:
            new_config_path = default_conf_path
        else:
            new_config_path = os.path.join(
                os.getcwd(), runtime_config.CONFIG_FILE_NAME
            )
    else:
        new_config_path = os.path.abspath(os.path.expanduser(config_path))
        if os.path.isdir(new_config_path):
            new_config_path = os.path.join(
                new_config_path, runtime_config.CONFIG_FILE_NAME
            )

    return new_config_path


def _show_data_dialog(data_path: str | None, new_config_path: str) -> str:
    if data_path is not None:
        return os.path.abspath(os.path.expanduser(data_path))

    click.echo(DIALOG_3)
    click.echo(
        os.path.join(
            os.path.split(new_config_path)[0], runtime_config.DATA_DIR_NAME
        )
    )
    rsp: str = click.prompt(DIALOG_4, default="y")

    if rsp in YES:
        data_path = os.path.split(new_config_path)[0]

    elif rsp == ".":
        data_path = os.path.abspath(os.getcwd())
    else:
        try:
            data_path = os.path.abspath(os.path.expanduser(rsp))
        except OSError:
            LOG.exception(
                "Something went wrong with your path. Please "
                "restart the program and enter a valid path."
            )
            raise

    data_path = os.path.join(data_path, runtime_config.DATA_DIR_NAME)
    return data_path


def _show_scenario_dialog(
    scenario_path: str | None, new_config_path: str
) -> str:
    if scenario_path is not None:
        new_scenario_path = os.path.expanduser(scenario_path)
    else:
        click.echo(DIALOG_5)
        click.echo(
            os.path.join(
                os.path.split(new_config_path)[0],
                runtime_config.SCENARIO_DIR_NAME,
            )
        )
        rsp: str = click.prompt(DIALOG_6, default="y")
        if rsp in YES:
            new_scenario_path = os.path.join(
                os.path.split(new_config_path)[0],
                runtime_config.SCENARIO_DIR_NAME,
            )
        elif rsp == ".":
            new_scenario_path = os.path.join(
                os.getcwd(), runtime_config.SCENARIO_DIR_NAME
            )
        else:
            try:
                new_scenario_path = os.path.abspath(os.path.expanduser(rsp))
            except OSError:
                LOG.exception(
                    "Something went wrong with your path. Please "
                    "restart the program and enter a valid path."
                )
                raise

    return new_scenario_path


def _show_output_dialog(output_path: str | None) -> str:
    if output_path is not None:
        return os.path.expanduser(output_path)

    click.echo(DIALOG_7)
    rsp: str = click.prompt(DIALOG_8, default="y")
    if output_path is None:
        new_output_path = runtime_config.DEFAULT_BASE_CONFIG["paths"][
            "output_path"
        ]
    if rsp in YES:
        pass  # Just use default
    else:
        try:
            new_output_path = os.path.expanduser(rsp)
        except OSError:
            LOG.exception(
                "Something went wrong with your path. Default "
                "path will be used."
            )
            raise

    return new_output_path


def _restore_logging(default_conf: Dict[str, Any]):
    for log_name, log_cfg in (
        runtime_config.RuntimeConfig().logging["loggers"].items()
    ):
        default_conf["logging"]["loggers"][log_name] = dict(log_cfg)

    for form_name, form_cfg in (
        runtime_config.RuntimeConfig().logging["formatters"].items()
    ):
        default_conf["logging"]["formatters"][form_name] = {
            "format": str(form_cfg["format"])
        }

    for hand_name, hand_cfg in (
        runtime_config.RuntimeConfig().logging["handlers"].items()
    ):
        default_conf["logging"]["handlers"][hand_name] = dict(hand_cfg)

    default_conf["logging"]["root"]["level"] = (
        runtime_config.RuntimeConfig().logging["root"]["level"]
    )
    default_conf["logging"]["root"]["handlers"] = list(
        runtime_config.RuntimeConfig().logging["root"]["handlers"]
    )


def _create_directories(
    new_config_path: str,
    new_data_path: str,
    new_scenario_path: str,
    new_output_path: str,
):
    new_config_dir = os.path.split(new_config_path)[0]
    if not os.path.isdir(new_config_dir):
        LOG.debug(
            f"Creating directory for runtime config at {new_config_dir}..."
        )
        os.makedirs(new_config_dir, exist_ok=True)

    if not os.path.isdir(new_data_path):
        LOG.debug(f"Creating directory for data  at {new_data_path}...")
        os.makedirs(new_data_path, exist_ok=True)

    new_scenario_dir = os.path.abspath(new_scenario_path)
    if not os.path.isdir(new_scenario_dir):
        LOG.debug(
            f"Creating directory for scenarios at {new_scenario_dir} ..."
        )
        os.makedirs(new_scenario_dir, exist_ok=True)

    new_output_dir = os.path.abspath(new_output_path)
    if not os.path.isdir(new_output_dir):
        LOG.debug(f"Creating directory for outputs at {new_output_dir} ...")
        os.makedirs(new_output_dir, exist_ok=True)

    click.echo("# SUMMARY #")
    click.echo(f"Your config will be saved at {new_config_path}.")
    click.echo(f"Your data will be saved at {new_data_path}.")
    click.echo(f"Your scenarios will be stored at {new_scenario_path}.")
    click.echo(f"Your outputs will be saved to {new_output_path}.")
