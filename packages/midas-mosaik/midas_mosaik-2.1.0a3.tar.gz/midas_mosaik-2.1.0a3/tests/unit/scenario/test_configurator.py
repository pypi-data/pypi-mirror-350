import unittest
from unittest.mock import AsyncMock, MagicMock, call, mock_open, patch

from midas.scenario import configurator


class TestConfigurat(unittest.TestCase):
    def setUp(self):
        self.cfgr = configurator.Configurator()
        self.scenario_name = "four_bus"
        self.params = {"silent": True}
        self.custom_cfgs = ["custom.yaml"]
        self.mock_configs = {
            "four_bus": {
                "parent": None,
                "modules": ["store", "powergrid", "sndata"],
                "silent": True,
            }
        }

    @patch("midas.scenario.configurator.open", new_callable=mock_open)
    @patch("midas.scenario.configurator.RuntimeConfig")
    @patch("midas.scenario.configurator.convert", side_effect=lambda x: x)
    @patch("midas.scenario.configurator.normalize")
    @patch(
        "midas.scenario.configurator.update",
        side_effect=lambda d, u: d.update(u) or d,
    )
    @patch("midas.scenario.configurator.load_configs")
    @patch("midas.scenario.configurator.get_config_files")
    @patch("midas.scenario.configurator.Scenario")
    def test_configure_success(
        self,
        mock_scenario,
        mock_get_files,
        mock_load_configs,
        mock_update,
        mock_normalize,
        mock_convert,
        mock_runtime,
        mock_open_file,
    ):
        mock_get_files.return_value = ["file.yaml"]
        mock_load_configs.return_value = self.mock_configs
        scenario_instance = MagicMock()
        mock_scenario.return_value = scenario_instance
        mock_runtime().paths = {"output_path": "/tmp"}

        result = self.cfgr.configure(
            self.scenario_name,
            self.params,
            self.custom_cfgs,
            no_script=True,
            no_yaml=True,
        )

        self.assertTrue(result.success)
        self.assertEqual(result, scenario_instance)
        mock_get_files.assert_called_once()
        mock_load_configs.assert_called_once()
        mock_normalize.assert_called_once()
        mock_scenario.assert_called_once_with(
            self.scenario_name, self.mock_configs["four_bus"]
        )
        mock_update.assert_any_call(self.mock_configs["four_bus"], self.params)

    @patch("midas.scenario.configurator.Scenario")
    def test_build_sets_success(self, mock_scenario):
        scenario_instance = MagicMock()
        self.cfgr.scenario = scenario_instance
        self.cfgr.build()
        scenario_instance.build.assert_called_once()
        self.assertTrue(self.cfgr.scenario.success)

    @patch("midas.scenario.configurator.Scenario")
    def test_run_success(self, mock_scenario):
        scenario_instance = MagicMock()
        scenario_instance.success = True
        scenario_instance.world = MagicMock()
        scenario_instance.base.end = 3600
        self.cfgr.scenario = scenario_instance
        self.cfgr.params = {"silent": False}

        self.cfgr.run()

        scenario_instance.world.run.assert_called_once()

    @patch("midas.scenario.configurator.Scenario")
    def test_run_world_none_raises(self, mock_scenario):
        self.cfgr.scenario = MagicMock()
        self.cfgr.scenario.success = True
        self.cfgr.scenario.world = None

        with self.assertRaises(ValueError):
            self.cfgr.run()

    @patch("midas.scenario.configurator.Scenario")
    def test_run_async_success(self, mock_scenario):
        scenario_instance = MagicMock()
        scenario_instance.success = True
        scenario_instance.base.end = 3600
        world_mock = AsyncMock()
        scenario_instance.world = world_mock
        self.cfgr.scenario = scenario_instance
        self.cfgr.params = {"silent": True}

        async def run_test():
            await self.cfgr.run_async()
            world_mock.run.assert_awaited_once()
            world_mock.shutdown.assert_awaited_once()

        import asyncio

        asyncio.run(run_test())

    @patch("midas.scenario.configurator.Scenario")
    def test_run_async_invalid_world_raises(self, mock_scenario):
        from mosaik import World

        scenario_instance = MagicMock()
        scenario_instance.success = True
        scenario_instance.world = World({})
        self.cfgr.scenario = scenario_instance
        self.cfgr.params = {"silent": True}

        async def run_test():
            with self.assertRaises(ValueError):
                await self.cfgr.run_async()
                await scenario_instance.world.shutdown()

        import asyncio

        asyncio.run(run_test())

    # def test_configure_success(self):
    #     """Test a successful call of configure"""

    #     configurator.get_config_files = mock.MagicMock(
    #         return_value=["TestFile"]
    #     )
    #     configurator.load_configs = mock.MagicMock(return_value=[{}])
    #     self.cfgr._organize_params = mock.MagicMock(return_value={})
    #     self.cfgr._apply_modules = mock.MagicMock()
    #     scenario = self.cfgr.configure(
    #         "Test", {}, no_script=True, no_yaml=True
    #     )

    #     self.assertTrue(scenario.success)

    #     # scenario.world.shutdown()
    #     configurator.get_config_files.assert_called_once()
    #     configurator.load_configs.assert_called_once()
    #     self.cfgr._organize_params.assert_called_once()
    #     self.cfgr._apply_modules.assert_called_once()

    def test_configure_no_config_files(self):
        """Test configure when no configuration files are found."""
        configurator.get_config_files = MagicMock(return_value=[])
        with self.assertRaises(ValueError) as cm:
            self.cfgr.configure("Test", {})

        self.assertIn("No configuration files found.", str(cm.exception))

    def test_configure_failed_to_load_config_files(self):
        """Test configure when loading of config files failed."""

        configurator.get_config_files = MagicMock(return_value=["TestFile"])
        configurator.load_configs = MagicMock(return_value=[])
        with self.assertRaises(ValueError) as cm:
            self.cfgr.configure("Test", {})

        self.assertIn("Something went wrong during loading", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
