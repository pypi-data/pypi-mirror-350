"""This module contains the configurator for midas scenarios."""

import logging
import os
import pprint
import time
from copy import deepcopy
from importlib import import_module
from typing import Any, Dict, List, Optional

from mosaik import World
from ruamel.yaml import YAML

from ..util.config_util import get_config_files, load_configs, normalize
from ..util.dict_util import convert, update
from ..util.runtime_config import RuntimeConfig
from .scenario import Scenario

LOG = logging.getLogger(__name__)


class Configurator:
    """This is the main configurator for midas scenarios.

    The configurator takes at least a scenario name to create a fully-
    configured mosaik scenario. Usually, the configurator is not used
    directly. Instead, it will be called from the midas.api.

    The configurator provides two public methods: :meth:`configure` and
    :meth:`run`. The whole scenario is set up in *configure* while the
    only purpose of *run* is to start the mosaik simulation.

    Attributes
    ----------
    scenario_name : str
        Stores the name of the scenario (to be) created.
    params : Dict[str, Any]
        A *dict* containing the configuration of the scenario. The dict
        is extended during the configuration.
    custom_cfg : List[str]
        Stores paths to custom configuration files if provided.
    scenario : dict
        A *dict* containing references to everything that is created
        during the configuration of the senario.

    """

    def __init__(self):
        self.scenario_name: str = ""
        self.params: Dict[str, Any] = {}
        self.custom_cfgs: List[str] = []
        self.scenario: Scenario = Scenario("", {})

    def configure(
        self,
        scenario_name: str,
        params: Dict[str, Any],
        custom_cfgs: Optional[List[str]] = None,
        no_script: bool = False,
        no_yaml: bool = False,
    ) -> Scenario:
        """Configure the midas scenario.

        The scenario will be created based on the provided information.
        If the configuration fails, the returned scenario has its'
        attribute :attr:`success` set to *False*.

        Parameters
        ----------
        scenario_name: str
            The name of the scenario to run. This is a toplevel key in
            a scenario file.
        params: Dict[str, Any]
            A dict containing parameters that should overwrite values
            from the scenario file.
        custom_cfgs: Optional[List[str]], optional
            A list containing paths to additional scenario files.
        no_script: bool, optional
            If set to True, no autoscript file will be generated.
        no_yaml: bool, optional
            If set to True, the full configuration will not be saved as
            new yaml file.

        Returns
        -------
        Scenario
            The configured :class:`.Scenario` with its' attribute
            :attr:`success` indicating if the configuration was
            successful or not.

        """
        LOG.info(
            "Starting configuration of the scenario '%s'...", scenario_name
        )
        start = time.time()
        self.scenario_name = scenario_name
        self.params = params
        self.custom_cfgs = custom_cfgs if custom_cfgs is not None else []
        default_path = os.path.abspath(
            os.path.join(__file__, "..", "default_scenarios")
        )
        files = get_config_files(self.custom_cfgs, default_path)

        if not files:
            msg = "No configuration files found. Aborting!"
            raise ValueError(msg)

        configs = load_configs(files)
        if not configs:
            msg = (
                "Something went wrong during loading the config files. "
                "Please consult the logs to find the reason. Aborting!"
            )
            raise ValueError(msg)

        params = self._organize_params(configs)

        LOG.debug("Creating base configuration...")
        self.scenario = Scenario(self.scenario_name, params)
        self._apply_modules(params)

        if not no_yaml:
            self._save_config(self.scenario_name, params)
        if not no_script:
            self._save_script(self.scenario.script)

        duration = time.time() - start
        LOG.info("Configuration finished after %.3f seconds.", duration)
        self.scenario.success = True
        return self.scenario

    def build(self):
        """Populate the mosaik world object."""

        self.scenario.success = False
        self.scenario.build()
        # self.scenario.build_async()
        self.scenario.success = True

    async def build_async(self):
        """Populate the mosaik world object."""

        self.scenario.success = False
        # self.scenario.build()
        await self.scenario.build_async()
        self.scenario.success = True

    def run(self):
        """Run the scenario configured before."""

        if not hasattr(self, "scenario"):
            LOG.error(
                "Scenario is not configured. "
                "Maybe you forgot to call configure?"
            )
            return

        if not self.scenario.success:
            LOG.error(
                "Scenario was not successful. Cannot sart the simulation."
            )
            return

        if self.scenario.world is None:
            msg = "World is None, that should not happen"
            raise ValueError(msg)

        LOG.info("Starting the scenario ...")
        start = time.time()
        self.scenario.world.run(
            until=self.scenario.base.end,
            print_progress=not self.params["silent"],
        )
        duration = time.time() - start
        LOG.info("Scenario finished after %.3f seconds.", duration)

    async def run_async(self):
        """Run the scenario configured before."""

        if not hasattr(self, "scenario"):
            LOG.error(
                "Scenario is not configured. "
                "Maybe you forgot to call configure?"
            )
            return

        if not self.scenario.success:
            LOG.error(
                "Scenario was not successful. Cannot sart the simulation."
            )
            return

        if self.scenario.world is None or isinstance(
            self.scenario.world, World
        ):
            msg = (
                "World is None or not async. Make sure you call 'build_async' "
                "of the configurator."
            )
            raise ValueError(msg)

        LOG.info("Starting the scenario ...")
        start = time.time()
        await self.scenario.world.run(
            until=self.scenario.base.end,
            print_progress=not self.params["silent"],
        )
        await self.scenario.world.shutdown()
        duration = time.time() - start
        LOG.info("Scenario finished after %.3f seconds.", duration)

    def _organize_params(self, configs):
        """Sort params in correct order."""
        try:
            cfg_chain = [configs[self.scenario_name]]
        except KeyError:
            LOG.exception(
                "%s not found in config files. Cannot process any further.",
                self.scenario_name,
            )
            msg = (
                f"{self.scenario_name} was not found in any of the scenario "
                "files. Make sure you provide the correct scenario file with"
                " 'midasctl run -c path/to/scenario.yml'."
            )
            raise ValueError(msg)

        parent = cfg_chain[0].get("parent", None)
        while parent is not None and parent != "None":
            cfg_chain.append(configs[parent])
            parent = cfg_chain[-1].get("parent", None)

        LOG.debug("Ordering the configs ...")
        modules = list()
        final_params = dict()
        for cfg in reversed(cfg_chain):
            modules += cfg.get("modules", [])
            update(final_params, cfg)
        final_params["modules"] = modules

        update(final_params, self.params)
        LOG.debug("Normalizing the config ...")
        normalize(final_params)

        return final_params

    def _save_config(self, name, params):
        """Save a copy of the current config."""
        yaml = YAML(typ="safe", pure=True)
        path = os.path.join(
            RuntimeConfig().paths["output_path"], f"{name}_cfg.yml"
        )
        params = convert(deepcopy(params))
        LOG.debug("Current config is %s.", pprint.pformat(params))
        LOG.info("Saving current config to %s.", path)
        with open(path, "w") as cfg_out:
            yaml.indent(mapping=4, sequence=6, offset=3)
            yaml.dump({"myconfig": params}, cfg_out)

    def _save_script(self, script):
        fname = os.path.join(
            RuntimeConfig().paths["output_path"],
            f"{self.scenario_name}_auto_script.py",
        )
        fctn = ""
        order = [
            "imports",
            "definitions",
            "simconfig",
            "sim_start",
            "model_start",
            "connects",
            "world_start",
        ]
        for part in order:
            for line in getattr(script, part):
                fctn += line
            fctn += "\n"
        with open(fname, "w") as sfile:
            sfile.write(fctn)

    def _apply_modules(self, params):
        """Apply all required modules in the correct order."""

        LOG.debug("Now adding further modules (if any)...")
        for module, cmod in RuntimeConfig().modules["default_modules"]:
            # Preserve ordering of modules
            if module in params["modules"]:
                LOG.debug("Adding module %s.", module)
                if ":" in cmod:
                    mod, clazz = cmod.split(":")
                else:
                    mod, clazz = cmod.rsplit(".", 1)
                mod = import_module(mod)
                getattr(mod, clazz)().upgrade(self.scenario, params)

        self._apply_custom_modules(params)

        # self.scenario.params = params
        self.scenario.script.definitions.append(
            f"sensors = {self.scenario.sensors}\n"
        )
        self.scenario.script.definitions.append(
            f"actuators = {self.scenario.actuators}\n"
        )
        return self.scenario

    def _apply_custom_modules(self, params):
        if "custom_modules" not in params:
            return
        if params["custom_modules"] is None:
            return

        LOG.debug(
            "Trying to load %d custom module(s) ...",
            len(params["custom_modules"]),
        )
        for module, cmod in params["custom_modules"]:
            # All custom module are loaded
            if ":" in cmod:
                mod, clazz = cmod.split(":")
            else:
                mod, clazz = cmod.rplit(".", 1)
            LOG.debug("Adding module %s.", module)
            mod = import_module(mod)
            getattr(mod, clazz)().upgrade(self.scenario, params)
