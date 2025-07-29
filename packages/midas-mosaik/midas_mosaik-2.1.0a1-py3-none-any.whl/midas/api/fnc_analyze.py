from __future__ import annotations

import logging
import os
from importlib import import_module
from typing import List, Optional

import click
import pandas as pd

from ..scenario.upgrade_module import UpgradeModule
from ..util.runtime_config import RuntimeConfig

LOG = logging.getLogger("midas.api")


def analyze(
    scenario_db_path: str,
    output_folder: str = "",
    start: int = 0,
    end: int = -1,
    step_size: int = 900,
    full: bool = False,
    modules: Optional[List[str]] = None,
):
    """The analyze function of MIDAS CLI.

    The actual analysis is part of the modules. Usually, there will be
    a markdown file containing important statistics and maybe one or
    more plots, visualizing the time series.

    Parameters
    ==========
    scenario_db_path: str
        The path to the HDF5 database file, created by the MidasStore
        module that contains the results to be analyzed. This should be
        the relative or absolute path to that file. If the database file
        is located in the outputs folder configured in the runtime
        config, it is sufficient to provide the filename.
    output_folder: str, optional
        The directory where the results will be stored. If empty, the
        default output path from the runtime config is used.
    start: int, optional
        The first row of the database that should be included in the
        analysis. Default is 0, which means that the first entry in the
        database will be the first entry in the analysis.
    end: int, optional
        The last row of the database that should be included in the
        analysis. Default is -1, which means that the last entry in the
        database will be the last entry in the analysis.
    step_size: int, optional
        The step size that was used in the simulation. Is required for
        the calculation of energy. The default is 900.
    full: bool, optional
        Request a full report. The full report includes plots for all
        components and takes considerably more time. Default is False,
        which only creates a minimal set of plots.
    modules: List[str], optional
        Request the analysis only from certain modules. Default is None,
        which requests analysis from all modules listed in the runtime
        config.
    """

    db_file = os.path.abspath(scenario_db_path)
    if not os.path.isfile(db_file):
        # The provided file does not exist, so check if it exists
        # inside of the default outputs directory
        output_db_path = os.path.abspath(
            os.path.join(
                RuntimeConfig().paths["output_path"], scenario_db_path
            )
        )
        if not os.path.isfile(output_db_path):
            # The provided file does not exist within the outputs folder.
            # Additional checks can be provided here but most probably
            # the wrong filename was provided.
            msg =(
                f"Searched for the database at '{db_file}' and "
                f"'{output_db_path}' without success. Aborting!"
            )
            raise ValueError(msg)
        else:
            db_file = output_db_path

    suffix = db_file.rsplit(".", 1)[-1]
    name = os.path.split(db_file)[-1][: -(len(suffix) + 1)]
    LOG.info(
        f"Located database '{name}' with file extension '{suffix}' at "
        f"'{db_file}'."
    )

    if output_folder == "":
        output_folder = RuntimeConfig().paths["output_path"]
    output_folder = os.path.abspath(output_folder)

    if not output_folder.endswith(name):
        output_folder = os.path.join(output_folder, name)

    if start > 0:
        output_folder += f"_from-{start}"
        if end < 0:
            output_folder += "_to-end"
        else:
            output_folder += f"_to-{end}"
    elif end > 0:
        output_folder += f"_from-start_to-{end}"

    LOG.info("Results will be saved at '%s'", output_folder)
    os.makedirs(output_folder, exist_ok=True)
    LOG.debug("Reading database...")
    data = pd.read_csv(db_file)

    LOG.info("Calling modules to analyze the database...")
    check_modules = (
        RuntimeConfig().modules["default_modules"]
        + RuntimeConfig().modules["custom_modules"]
    )
    if modules is None or not modules:
        analyze_if_necessary = False
    else:
        analyze_if_necessary = True

    for module in check_modules:
        mname = module[0]
        mpath = module[1]
        if analyze_if_necessary and mname not in modules:
            LOG.info("Skipping module '%s'.", mname)
            continue
        LOG.info("Processing module '%s' from '%s'...", mname, mpath)

        if ":" in mpath:
            mod, clazz = mpath.split(":")
        else:
            mod, clazz = mpath.rsplit(":", 1)
        try:
            LOG.debug("Importing module '%s'...", mod)
            mod = import_module(mod)
            mod_inst: UpgradeModule = getattr(mod, clazz)()
        except ImportError:
            LOG.warning(
                "Could not import module '%s' configured in the runtime"
                " config. Please check your configuration!.",
                mname,
            )
            continue
        try:
            LOG.debug("Calling analyze function of '%s'...", mname)
            mod_inst.analyze(
                name, data, output_folder, start, end, step_size, full
            )
        except AttributeError:
            LOG.debug(
                "Module '%s' does not provide an analyze function.", mname
            )

    # LOG.info("Closing database.")
    # data.close()

    click.echo("Analysis complete!")
