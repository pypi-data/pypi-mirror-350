import logging
import os
import shutil
from importlib import import_module
from typing import List, Optional

import click

from ..scenario.upgrade_module import UpgradeModule
from ..util.runtime_config import RuntimeConfig

LOG = logging.getLogger("midas.api")


def download(
    keep_tmp: bool = False,
    force: bool = False,
    modules: list[str] | tuple[str] | None = None,
):
    """Download the required datasets.

    There are currently five categories of datasets:
        * Default load profiles from BDEW
        * Commercial dataset from openei.org
        * Simbench data from the simbench grids
        * Smart Nord dataset from the research project Smart Nord
        * Weather dataset from opendata.dwd.de

    The default behavior of this function is to download all missing
    datasets and, afterwards, remove the temporary directory created
    during this process.

    If at least one of the flags is set to *True*, only those datasets
    will be downloaded. If *force* is *True*, the datasets will be
    downloaded regardless of any existing dataset. If *keep_tmp* is
    *True*, the temporary downloaded files will not be removed
    afterwards.

    """
    # # Check parameters
    if modules is None or not modules:
        load_if_necessary = False
    else:
        load_if_necessary = True

    # Create paths
    data_path = RuntimeConfig().paths["data_path"]
    tmp_path = os.path.abspath(os.path.join(data_path, "tmp"))
    LOG.info("Using temporary location '%s'.", tmp_path)
    os.makedirs(tmp_path, exist_ok=True)

    default_modules = RuntimeConfig().modules["default_modules"]
    for module in default_modules:
        mname = module[0]
        mpath = module[1]
        if load_if_necessary and mname not in modules:
            LOG.info("Skipping module '%s'.", mname)
            continue
        LOG.info("Attempting to download data from module '%s'...", module[0])

        if ":" in mpath:
            mod, clazz = mpath.split(":")
        else:
            mod, clazz = mpath.rsplit(".", 1)
        try:
            LOG.debug("Importing module '%s'...", mod)
            mod = import_module(mod)
            mod_inst: UpgradeModule = getattr(mod, clazz)()
        except ImportError:
            LOG.info(
                "Could not import default module '%s'. "
                "Please check your runtime config and/or install the module "
                "if needed.",
                mname,
            )
            continue
        try:
            LOG.debug("Calling download function of '%s'...", mname)
            mod_inst.download(data_path, tmp_path, force)
        except AttributeError as err:
            LOG.debug(
                "Module '%s' does not provide any downloads: '%s'.", mname, err
            )

    custom_modules = RuntimeConfig().modules["custom_modules"]
    for module in custom_modules:
        mname = module[0]
        mpath = module[1]
        if load_if_necessary and mname not in modules:
            LOG.info("Skipping module '%s'.", mname)
            continue

        if ":" in mpath:
            mod, clazz = mpath.split(":")
        else:
            mod, clazz = mpath.rsplit(".", 1)
        try:
            mod = import_module(mod)
            mod_inst: UpgradeModule = getattr(mod, clazz)()
        except ImportError:
            LOG.warning(
                "Could not import module '%s' defined in your runtime "
                "configuration. Please check your config.",
                mname,
            )
            continue
        try:
            mod_inst.download(data_path, tmp_path, force)
        except AttributeError:
            LOG.debug("Module '%s' does not provide any downloads.", mname)

    # Clean up
    if not keep_tmp:
        try:
            shutil.rmtree(tmp_path)
        except Exception as err:
            click.echo(
                f"Failed to remove files '{tmp_path}'': {err}. "
                "You have to remove those files manually."
            )
            LOG.warning(
                "Could not remove temporary files at %s. You have to remove "
                "those files by hand. The error is: %s",
                tmp_path,
                err,
            )

    LOG.info("Download complete!")
