import unittest
from unittest import mock

from midas.scenario import configurator


class TestConfigurat(unittest.TestCase):
    def setUp(self):
        self.cfgr = configurator.Configurator()

    def test_configure_success(self):
        """Test a successful call of configure"""

        configurator.get_config_files = mock.MagicMock(
            return_value=["TestFile"]
        )
        configurator.load_configs = mock.MagicMock(return_value=[{}])
        self.cfgr._organize_params = mock.MagicMock(return_value={})
        self.cfgr._apply_modules = mock.MagicMock()
        scenario = self.cfgr.configure(
            "Test", {}, no_script=True, no_yaml=True
        )

        self.assertTrue(scenario.success)

        # scenario.world.shutdown()
        configurator.get_config_files.assert_called_once()
        configurator.load_configs.assert_called_once()
        self.cfgr._organize_params.assert_called_once()
        self.cfgr._apply_modules.assert_called_once()

    def test_configure_no_config_files(self):
        """Test configure when no configuration files are found."""
        configurator.get_config_files = mock.MagicMock(return_value=[])
        with self.assertLogs(
            "midas.scenario.configurator", level="ERROR"
        ) as cm:
            scenario = self.cfgr.configure("Test", {})

        self.assertFalse(scenario.success)
        # scenario.world.shutdown()
        self.assertIn("No configuration files found.", cm.output[0])

    def test_configure_failed_to_load_config_files(self):
        """Test configure when loading of config files failed."""

        configurator.get_config_files = mock.MagicMock(
            return_value=["TestFile"]
        )
        configurator.load_configs = mock.MagicMock(return_value=[])
        with self.assertLogs(
            "midas.scenario.configurator", level="ERROR"
        ) as cm:
            scenario = self.cfgr.configure("Test", {})

        self.assertFalse(scenario.success)
        # scenario.world.shutdown()
        self.assertIn("Something went wrong during loading", cm.output[0])


if __name__ == "__main__":
    unittest.main()
