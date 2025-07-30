from __future__ import annotations

import logging
import os
import pickle
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

import mosaik
import numpy as np
from mosaik import AsyncWorld, World, exceptions
from mosaik.async_scenario import AsyncModelMock, Entity
from mosaik.scenario import ModelMock
from mosaik_api_v3.types import SimId

from ..util.dict_util import set_default_bool
from ..util.runtime_config import RuntimeConfig
from .upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class Scenario:
    """Stores everything that is related to the scenario
    build process of MIDAS.

    """

    def __init__(self, name: str, params: Dict[str, Any]):
        self.name: str = name
        self.initial_params = params
        self.world: World | AsyncWorld | None = None
        self.base: Base = Base()
        self.script: Script = Script()
        self.makelists: Makelists = Makelists()
        self.sensors: list = []
        self.actuators: list = []

        self._sim_keys: Dict[str, Any] = {}
        self._mappings: Dict[str, Any] = {}
        self._ict_mappings: List[Dict[str, Any]] = []
        self._powergrid_mappings: Dict[str, Dict[str, Any]] = {}
        self.entities: Dict[SimId | ModelMock | AsyncModelMock, Any] = {}

        self._configure(params)
        self.success: bool = False
        self.world_state: Dict[str, Any] = {}

    def _configure(self, params):
        """Create the base configuration for midas scenarios.

        Parameters
        ----------
        params: dict
            A *dict* containing the cascading contents of yaml config
            files.

        """
        paths = RuntimeConfig().paths
        data = RuntimeConfig().data
        self.base.seed_max = 2**32 - 1
        self.base.output_path = paths["output_path"]
        self.base.data_path = params.setdefault(
            "data_path", paths["data_path"]
        )

        os.makedirs(self.base.output_path, exist_ok=True)

        self.base.step_size = int(params.setdefault("step_size", 15 * 60))
        self.base.start_date = params.setdefault(
            "start_date", "2020-01-01 00:00:00+0100"
        )

        self.base.end = int(params.setdefault("end", 1 * 24 * 60 * 60))
        self.base.cos_phi = params.setdefault("cos_phi", 0.9)
        self.base.no_db = set_default_bool(params, "no_db", False)
        self.base.with_timesim = set_default_bool(
            params, "with_timesim", False
        )
        self.base.with_arl = set_default_bool(params, "with_arl", False)
        self.sensors = params.setdefault("sensors", [])
        self.actuators = params.setdefault("actuators", [])
        self.base.with_ict = set_default_bool(params, "with_ict", False)
        self.base.no_rng = set_default_bool(params, "no_rng", False)
        self.base.silent = set_default_bool(params, "silent", False)
        self.base.forecast_horizon_hours = params.setdefault(
            "forecast_horizon_hours", 0.25
        )
        self.base.flexibility_horizon_hours = params.setdefault(
            "flexibility_horizon_hours", self.base.forecast_horizon_hours
        )
        self.base.flexibility_horizon_start_hours = params.setdefault(
            "flexibility_horizon_start_hours", 0
        )
        self.base.cmd = params.setdefault("cmd", "python")
        try:
            self.base.default_weather_name = data["weather"][0]["name"]
        except KeyError:
            self.base.default_weather_name = "Not installed"
        try:
            self.base.default_simbench_name = data["simbench"][0]["name"]
        except KeyError:
            self.base.default_simbench_name = "Not installed"
        try:
            self.base.default_commercials_name = data["commercials"][0]["name"]
        except KeyError:
            self.base.default_commercials_name = "Not installed"

        self.mosaik_params = params.setdefault("mosaik_params", {})

        if "random_state" in params:
            # A path to a random state object was passed with the params
            with open(params["random_state"], "rb") as state_f:
                random_state = pickle.load(state_f)
            self.base.rng = np.random.RandomState()
            self.base.rng.set_state(random_state)
        elif "seed" in params and params["seed"] is not None:
            # A seed was passed with the params
            if isinstance(params["seed"], int):
                self.base.rng = np.random.RandomState(params["seed"])
            else:
                LOG.warning(
                    "Invalid seed %s of type %s. Provide an integer!",
                    params["seed"],
                    type(params["seed"]),
                )
            state_fname = os.path.join(
                self.base.output_path, f"{self.name}-random_state"
            )
            with open(state_fname, "wb") as state_f:
                pickle.dump(self.base.rng.get_state(), state_f)
            params["random_state"] = state_fname
        else:
            # We create a random state object regardless if no_rng
            # is true. If no_rng is true, random number just won't be
            # used by the simulators.
            self.base.rng = np.random.RandomState()

        if not self.base.no_rng and self.base.start_date == "random":
            self.base.start_date = (
                f"2020-{self.base.rng.randint(1, 12):02d}-"
                f"{self.base.rng.randint(1, 28):02d} "
                f"{self.base.rng.randint(0, 23):02d}:00:00+0100"
            )
            params["start_date"] = self.base.start_date

        self.script.imports.append("import mosaik\n")
        self.script.imports.append("import numpy as np\n")
        self.script.sim_start.append("world = mosaik.World(sim_config)\n")
        self.script.world_start.append(
            f"world.run(until=end, print_progress={not self.base.silent})\n"
        )
        for key, value in self.base.__dict__.items():
            if key in ("rng"):
                continue

            if isinstance(value, str):
                self.script.definitions.append(f'{key} = "{value}"\n')
            else:
                self.script.definitions.append(f"{key} = {value}\n")

        self.script.definitions.append(
            f"rng = np.random.RandomState({params.get('seed', None)})\n"
        )

    def build(self):
        self.world = mosaik.World(
            sim_config=self.makelists.sim_config,
            mosaik_config=self.mosaik_params,
            configure_logging=False,
        )
        for sim_cfg in self.makelists.sim_start:
            sim = self.world.start(**sim_cfg["params"])
            try:
                sid = sim._sid
            except AttributeError:
                sid = sim.sid
            LOG.debug(f"Started simulator {sid} (key: {sim_cfg['sim_key']})")
            self._sim_keys[sim_cfg["sim_key"]]["sim"] = sim
            self.entities[sid] = sim

        for model_entry in self.makelists.model_start:
            model_cfg = self.get_model(
                model_entry["model_key"], model_entry["sim_key"]
            )
            if model_cfg is None:
                msg = (
                    f"Could not find model for {model_entry['model_key']}"
                    f"with sim key {model_entry['sim_key']}"
                )
                raise ValueError(msg)
            sim = self.get_sim(model_entry["sim_key"])
            if model_entry["parent_full_id"] is not None:
                parent = self.entities[model_entry["parent_full_id"]]
                entity = [
                    e for e in parent.children if e.eid == model_cfg["eid"]
                ][0]
            else:
                entity = getattr(sim, model_cfg["name"])(**model_cfg["params"])
            LOG.debug(
                f"Created model {entity.full_id} (key: "
                f"{model_entry['model_key']})."
            )
            self._sim_keys[model_entry["sim_key"]]["models"][
                model_entry["model_key"]
            ] = entity
            self.entities[entity.full_id] = entity

        for connect_cfg in self.makelists.connects:
            from_entity = self.get_model_entity(connect_cfg["from"])
            to_entity = self.get_model_entity(connect_cfg["to"])
            if from_entity is None or not isinstance(from_entity, Entity):
                msg = f"Model {connect_cfg['from']} does not exist."
                raise ValueError(msg)
            if to_entity is None or not isinstance(from_entity, Entity):
                msg = f"Model {connect_cfg['to']} does not exist."
                raise ValueError(msg)

            try:
                self.world.connect(
                    from_entity,
                    to_entity,
                    *connect_cfg["attrs"],
                    **connect_cfg["kwargs"],
                )
            except exceptions.ScenarioError:
                LOG.exception("Something went wrong with your scenario setup")
            LOG.debug(
                "Connected %s to %s (%s).",
                from_entity.full_id,
                to_entity.full_id,
                connect_cfg["attrs"],
            )

    async def build_async(self):
        self.world = mosaik.AsyncWorld(
            sim_config=self.makelists.sim_config,
            mosaik_config=self.mosaik_params,
            skip_greetings=False,
        )

        for sim_cfg in self.makelists.sim_start:
            sim = await self.world.start(**sim_cfg["params"])
            try:
                sid = sim._sid
            except AttributeError:
                sid = sim.sid
            LOG.debug(f"Started simulator {sid} (key: {sim_cfg['sim_key']})")
            self._sim_keys[sim_cfg["sim_key"]]["sim"] = sim
            self.entities[sid] = sim

        for model_entry in self.makelists.model_start:
            model_cfg = self.get_model(
                model_entry["model_key"], model_entry["sim_key"]
            )
            if model_cfg is None:
                msg = (
                    f"Could not find model for {model_entry['model_key']}"
                    f"with sim key {model_entry['sim_key']}"
                )
                raise ValueError(msg)

            sim = self.get_sim(model_entry["sim_key"])
            if model_entry["parent_full_id"] is not None:
                parent = self.entities[model_entry["parent_full_id"]]
                entity = [
                    e for e in parent.children if e.eid == model_cfg["eid"]
                ][0]
            else:
                entity = await getattr(sim, model_cfg["name"])(
                    **model_cfg["params"]
                )
            LOG.debug(
                f"Created model {entity.full_id} (key: "
                f"{model_entry['model_key']})."
            )
            self._sim_keys[model_entry["sim_key"]]["models"][
                model_entry["model_key"]
            ] = entity
            self.entities[entity.full_id] = entity

        for connect_cfg in self.makelists.connects:
            from_entity = self.get_model_entity(connect_cfg["from"])
            to_entity = self.get_model_entity(connect_cfg["to"])

            if from_entity is None or isinstance(from_entity, dict):
                msg = f"Model {connect_cfg['from']} does not exist."
                raise ValueError(msg)
            if to_entity is None or isinstance(from_entity, dict):
                msg = f"Model {connect_cfg['to']} does not exist."
                raise ValueError(msg)

            try:
                self.world.connect(
                    from_entity,
                    to_entity,
                    *connect_cfg["attrs"],
                    **connect_cfg["kwargs"],
                )
            except exceptions.ScenarioError:
                LOG.exception("Something went wrong with your scenario setup")
            LOG.debug(
                "Connected %s to %s (%s).",
                from_entity.full_id,
                to_entity.full_id,
                connect_cfg["attrs"],
            )

    def generate_sim_key(self, module):
        sim_key = f"{module.module_name}_{module.scope_name}_sim".lower()
        self._sim_keys[sim_key] = {}

        return sim_key

    def sim_started(self, sim_key):
        if self._sim_keys[sim_key]:
            return True
        else:
            return False

    def add_sim(self, sim_key, sim_params):
        self._sim_keys[sim_key]["sim"] = sim_params
        self._sim_keys[sim_key]["models"] = {}

        self.makelists.sim_start.append(
            {"sim_key": sim_key, "params": sim_params.copy()}
        )

    def get_sim(self, sim_key):
        try:
            return self._sim_keys[sim_key]["sim"]
        except KeyError:
            LOG.info("Simulator with key %s does not exist, yet!")
            return None

    def model_started(self, model_key, sim_key=None):
        if sim_key is not None:
            if self.sim_started(sim_key):
                if model_key in self._sim_keys[sim_key]["models"]:
                    return True
                else:
                    return False

        for sim_key, sim_cfg in self._sim_keys.items():
            if not sim_cfg:
                continue

            if model_key in sim_cfg["models"]:
                return True

        return False

    def add_model(
        self,
        model_key,
        sim_key,
        model_name,
        params,
        full_id,
        parent_full_id=None,
    ):
        self._sim_keys[sim_key]["models"][model_key] = {
            "name": model_name,
            "params": params,
            "full_id": full_id,
            "sid": full_id.split(".")[0],
            "eid": full_id.split(".")[1],
            "extra_data": {},
        }
        self.makelists.model_start.append(
            {
                "sim_key": sim_key,
                "model_key": model_key,
                "name": model_name,
                "parent_full_id": parent_full_id,
            }
        )

    def add_to_model_extra_data(self, model_key, sim_key, data):
        self._sim_keys[sim_key]["models"][model_key]["extra_data"] = data

    def get_models(self, sim_key):
        return self._sim_keys[sim_key].get("models", {})

    def get_model(self, model_key, sim_key=None) -> dict[str, Any] | None:
        if sim_key is not None:
            if self.sim_started(sim_key):
                if model_key in self._sim_keys[sim_key]["models"]:
                    return self._sim_keys[sim_key]["models"][model_key]
        
        for sim_cfg in self._sim_keys.values():
            if not sim_cfg:
                continue
            if model_key in sim_cfg["models"]:
                return sim_cfg["models"][model_key]

        LOG.info("Model with key %s does not exist, yet!", model_key)
        return None

    def get_model_entity(self, model_key) -> Entity | None:
        for sim_cfg in self._sim_keys.values():
            if not sim_cfg:
                continue
            if model_key in sim_cfg["models"]:
                return sim_cfg["models"][model_key]
        LOG.info("Model with key %s does not exist, yet!", model_key)
        return None

    def generate_model_key(
        self,
        module: Union[UpgradeModule, Tuple[str, str]],
        first_key: Optional[str] = None,
        second_key: Optional[str] = None,
        third_key: Optional[str] = None,
    ):
        if isinstance(module, tuple):
            model_key = f"{module[0]}_{module[1]}"
        elif isinstance(module, UpgradeModule):
            model_key = f"{module.module_name}_{module.scope_name}"
        else:
            LOG.exception(
                "Parameter module must be of Type UpgradeModule or Tuple[str"
                f", str] but is {module} of type {type(module)}"
            )
            raise TypeError

        if first_key is not None:
            model_key += f"_{first_key}"
        if second_key is not None:
            model_key += f"_{second_key}"
        if third_key is not None:
            model_key += f"_{third_key}"
        return model_key

    def find_models(self, sim_key, model_key=None, add_key1=None):
        results = {}
        sim_keys = []
        if sim_key not in self._sim_keys:
            for key in self._sim_keys:
                if sim_key in key:
                    sim_keys.append(key)
        else:
            sim_keys.append(sim_key)
        for sim_key in sim_keys:
            for key, model in self.get_models(sim_key).items():
                if model_key is not None:
                    if model_key not in key:
                        continue
                if add_key1 is not None:
                    if add_key1 not in key:
                        continue
                results[key] = model

        return results

    def find_first_model(
        self, sim_key, model_key=None
    ) -> Tuple[Union[str, None], Union[Any, None]]:
        models = self.find_models(sim_key, model_key)

        for key, model in models.items():
            return key, model

        return None, None

    def create_seed(self):
        return self.base.rng.randint(self.base.seed_max)

    def create_shared_mapping(
        self,
        module: Union[UpgradeModule, Tuple[str, str]],
        first_key: Optional[str] = None,
        second_key: Optional[str] = None,
    ):
        if isinstance(module, tuple):
            key = f"{module[0]}_{module[1]}"
        elif isinstance(module, UpgradeModule):
            key = f"{module.module_name}_{module.scope_name}"
        else:
            LOG.exception(
                "Parameter module must be of Type UpgradeModule or Tuple[str"
                f", str] but is {module} of type {type(module)}"
            )
            raise TypeError

        if first_key is not None:
            key += f"_{first_key}"
        if second_key is not None:
            key += f"_{second_key}"

        key += "_mapping"

        return self._mappings.setdefault(key, {})

    def get_shared_mappings(
        self,
        module_name: Optional[str] = None,
        scope_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        if module_name is not None or scope_name is not None:
            mappings = {}
            for key, mapping in self._mappings.items():
                if module_name is not None and scope_name is not None:
                    if f"{module_name}_{scope_name}" in key:
                        mappings[key] = mapping
                elif module_name is not None:
                    if module_name in key:
                        mappings[key] = mapping
                elif scope_name is not None:
                    if scope_name in key:
                        mappings[key] = mapping
            return mappings
        else:
            return self._mappings

    def get_ict_mappings(self) -> List[Dict[str, Any]]:
        if self._ict_mappings is None:
            self._ict_mappings = []

        return self._ict_mappings

    def get_powergrid_mappings(
        self, scope_name: Optional[str] = None
    ) -> Union[Dict[str, Dict[str, Any]], Dict[str, Any]]:
        if self._powergrid_mappings is None:
            self._powergrid_mappings = {}

        if scope_name is not None:
            self._powergrid_mappings.setdefault(scope_name, {})
            return self._powergrid_mappings[scope_name]

        return self._powergrid_mappings

    def find_grid_entities(self, grid_name, etype, idx=None, endswith=None):
        if idx is not None:
            etype += f"_{idx}"
        entities = self.find_models("powergrid", grid_name, etype)

        if endswith is None:
            return entities
        else:
            results = {}
            for key, entity in entities.items():
                if key.endswith(endswith):
                    results[key] = entity
            return results

    def add_to_world_state(self, key: str, obj: Any):
        self.world_state[key] = obj


@dataclass(init=False)
class Base:
    seed: int
    seed_max: int
    output_path: str
    data_path: str
    step_size: int
    start_date: str
    end: int
    cos_phi: float
    no_db: bool
    with_timesim: bool
    with_arl: bool
    with_ict: bool
    no_rng: bool
    silent: bool
    forecast_horizon_hours: float
    flexibility_horizon_hours: float
    flexibility_horizon_start_hours: float
    rng: np.random.RandomState
    cmd: str

    default_weather_name: str
    default_simbench_name: str
    default_commercials_name: str


@dataclass(init=False)
class Script:
    imports: List[str] = field(default_factory=list)
    definitions: List[str] = field(default_factory=list)
    simconfig: List[str] = field(default_factory=list)
    model_start: List[str] = field(default_factory=list)
    connects: List[str] = field(default_factory=list)
    sim_start: List[str] = field(default_factory=list)
    world_start: List[str] = field(default_factory=list)

    def __init__(self):
        self.imports = []
        self.definitions = []
        self.simconfig = []
        self.sim_start = []
        self.model_start = []
        self.connects = []
        self.world_start = []


@dataclass(init=False)
class Makelists:
    sim_config: mosaik.SimConfig = field(default_factory=dict)
    sim_start: List[Any] = field(default_factory=list)
    model_start: List[Any] = field(default_factory=list)
    connects: List[Any] = field(default_factory=list)

    def __init__(self):
        self.sim_config = {}
        self.sim_start = []
        self.model_start = []
        self.connects = []


# def set_default_bool(key, params, default=False):
#     val = params.get(key, default)
#     if not isinstance(val, bool):
#         val = strtobool(val)
#     params[key] = val
#     return val
