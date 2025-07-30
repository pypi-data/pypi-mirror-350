import unittest
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

from mosaik.async_scenario import Entity

from midas.scenario.scenario import Scenario
from midas.scenario.upgrade_module import UpgradeModule


class TestScenario(unittest.TestCase):
    def setUp(self):
        self.params = {
            "seed": 123,
            "silent": True,
            "step_size": 900,
            "end": 86400,
            "start_date": "2020-01-01 00:00:00+0100",
        }

    @patch("midas.scenario.scenario.open", new_callable=mock_open)
    @patch("midas.scenario.scenario.pickle.dump")
    @patch("midas.scenario.scenario.np.random.RandomState")
    @patch("midas.scenario.scenario.RuntimeConfig")
    def test_init_and_configure(
        self, mock_runtime, mock_rng, mock_pickle, mock_open_file
    ):
        mock_rng.return_value.get_state.return_value = "mock_state"
        mock_runtime().paths = {"output_path": "/tmp", "data_path": "/data"}
        mock_runtime().data = {
            "weather": [{"name": "weather1"}],
            "simbench": [{"name": "bench1"}],
            "commercials": [{"name": "commercial1"}],
        }

        s = Scenario("test_scenario", self.params)
        self.assertEqual(s.name, "test_scenario")
        self.assertEqual(s.base.step_size, 900)
        mock_pickle.assert_called_once()

    @patch("midas.scenario.scenario.mosaik.World")
    @patch("midas.scenario.scenario.RuntimeConfig")
    def test_build_with_models_and_connects(self, mock_runtime, mock_world):
        s = Scenario("test", self.params)
        sim_mock = MagicMock()
        sim_mock._sid = "sim"
        entity_mock = MagicMock(spec=Entity)
        entity_mock.full_id = "sim.model"
        entity_mock.eid = "model"
        entity_mock.sid = "sim"
        entity_mock.children = [entity_mock]

        s.makelists.sim_start = [
            {"sim_key": "sim1", "params": {"type": "sim"}}
        ]
        s._sim_keys["sim1"] = {
            "sim": sim_mock,
            "models": {
                "m1": {"name": "SomeModel", "params": {}, "eid": "model"}
            },
        }

        s.makelists.model_start = [
            {
                "model_key": "m1",
                "sim_key": "sim1",
                "name": "SomeModel",
                "parent_full_id": None,
            }
        ]
        sim_mock.SomeModel = MagicMock(return_value=entity_mock)
        s.get_sim = MagicMock(return_value=sim_mock)

        s.makelists.connects = [
            {"from": "m1", "to": "m1", "attrs": ["a"], "kwargs": {}}
        ]
        s.get_model_entity = MagicMock(return_value=entity_mock)

        s.build()
        self.assertEqual(s.entities["sim.model"], entity_mock)

    @patch("midas.scenario.scenario.mosaik.AsyncWorld")
    @patch("midas.scenario.scenario.RuntimeConfig")
    def test_build_async_basic(self, mock_runtime, mock_async_world):
        s = Scenario("test", self.params)
        entity_mock = MagicMock()
        entity_mock.full_id = "sim.model"
        entity_mock.eid = "model"
        entity_mock.sid = "sim"
        entity_mock.children = [entity_mock]

        model_cfg = {"name": "Model", "params": {}, "eid": "model"}

        s.makelists.sim_start = [
            {"sim_key": "sim1", "params": {"type": "sim"}}
        ]
        s._sim_keys["sim1"] = {"sim": None, "models": {"m1": model_cfg}}

        s.makelists.model_start = [
            {
                "model_key": "m1",
                "sim_key": "sim1",
                "name": "Model",
                "parent_full_id": None,
            }
        ]
        s.get_model = MagicMock(return_value=model_cfg)

        model_method_mock = AsyncMock(return_value=entity_mock)
        sim_mock = MagicMock()
        setattr(sim_mock, "Model", model_method_mock)
        sim_mock._sid = "sim"
        s.get_sim = MagicMock(return_value=sim_mock)

        mock_world = MagicMock()
        mock_world.start = AsyncMock(return_value=sim_mock)
        mock_async_world.return_value = mock_world
        s.makelists.connects = []

        import asyncio

        async def runner():
            await s.build_async()
            self.assertIn("sim", s.entities)
            self.assertIn("sim.model", s.entities)
            model_method_mock.assert_awaited_once()

        asyncio.run(runner())

    def test_model_key_generation(self):
        s = Scenario("test", self.params)

        # Valid UpgradeModule-like input
        key = s.generate_model_key(ValidModule(), "x", "y", "z")
        self.assertEqual(key, "Mod__x_y_z")

        # Valid tuple input
        key2 = s.generate_model_key(("ModA", "ScopeB"))
        self.assertEqual(key2, "ModA_ScopeB")

        # Invalid input
        with self.assertRaises(TypeError):
            s.generate_model_key(123)  # type: ignore[reportArgumentType]

    def test_create_shared_mapping(self):
        s = Scenario("test", self.params)

        mapping = s.create_shared_mapping(ValidModule())
        self.assertIn("Mod__mapping", s._mappings)
        self.assertEqual(mapping, s.get_shared_mappings()["Mod__mapping"])

        # Test invalid input
        with self.assertRaises(TypeError):
            s.create_shared_mapping(123)  # type: ignore[reportArgumentType]

    def test_sim_and_model_logic(self):
        s = Scenario("test", self.params)
        s._sim_keys = {}

        class Dummy:
            module_name = "A"
            scope_name = "B"

        sim_key = s.generate_sim_key(Dummy())
        self.assertIn(sim_key, s._sim_keys)
        self.assertFalse(s.sim_started(sim_key))

        s.add_sim(sim_key, {"type": "x"})
        self.assertTrue(s.sim_started(sim_key))

        s.add_model("model1", sim_key, "M", {"param": 1}, "sim.model1")
        self.assertTrue(s.model_started("model1"))
        self.assertIsNotNone(s.get_model("model1"))

    def test_world_state_and_find(self):
        s = Scenario("test", self.params)
        s.add_to_world_state("k1", 99)
        self.assertEqual(s.world_state["k1"], 99)

        s._sim_keys["powergrid"] = {
            "models": {
                "pg_load_1": {"name": "Load"},
                "pg_load_2": {"name": "Load"},
            }
        }

        found = s.find_grid_entities("load", "pg", endswith="2")
        self.assertEqual(len(found), 1)
        self.assertIn("pg_load_2", found)


class ValidModule(UpgradeModule):
    def __init__(self):
        super().__init__("Mod", "Scope", "dummy", "dummy")

    def check_module_params(self, module_params):
        return {}

    def check_sim_params(self, module_params):
        pass

    def connect(self):
        pass

    def connect_to_db(self):
        pass

    def start_models(self):
        pass


if __name__ == "__main__":
    unittest.main()
