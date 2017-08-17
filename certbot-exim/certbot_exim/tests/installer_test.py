"""Tests for certbot_exim.installer."""
import os
import shutil
import tempfile
import unittest

import mock
import six

import zope.component

from certbot import configuration
from certbot import errors

from certbot.plugins import common

from certbot_exim import installer


class EximTest(unittest.TestCase):
    def setUp(self):
        super(EximTest, self).setUp()

        self.temp_dir, self.config_dir, self.work_dir = common.dir_setup(
            "etc_exim4", "certbot_exim.tests")
        self.logs_dir = tempfile.mkdtemp('logs')

        self.config_path = os.path.join(self.temp_dir, "etc_exim4")
        self.installer = get_exim_installer(
            self.config_path, self.config_dir, self.work_dir, self.logs_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        shutil.rmtree(self.config_dir)
        shutil.rmtree(self.work_dir)
        shutil.rmtree(self.logs_dir)

    def test_parser_arguments(self):
        m = mock.MagicMock()

        # pylint: disable=no-member
        self.installer.add_parser_arguments(m)

        m.assert_any_call('server-root', default=mock.ANY, help=mock.ANY)
        m.assert_any_call('file-configuration', action="store_true", help=mock.ANY)

    def test_more_info(self):
        # pylint: disable=no-member
        self.assertTrue(isinstance(self.installer.more_info(), six.string_types))

    @mock.patch("certbot_exim.installer.util.exe_exists")
    def test_prepare_no_install(self, mock_exe_exists):
        mock_exe_exists.return_value = False
        self.assertRaises(errors.NoInstallationError, self.installer.prepare)

    @mock.patch("certbot_exim.installer.util.exe_exists")
    def test_prepare_is_installed(self, mock_exe_exists):
        mock_exe_exists.return_value = True
        self.installer.prepare()

        self.assertIsNotNone(self.installer.parser)

    def test_supported_enhancements(self):
        self.assertEqual(['staple-ocsp'],
                         self.installer.supported_enhancements())

    def test_get_all_names(self):
        self.installer.parser = mock.MagicMock()
        self.installer.parser.get_directive.return_value = "test.mail.example.com"

        names = self.installer.get_all_names()

        self.installer.parser.get_directive.assert_called_once_with("primary_hostname")
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0], "test.mail.example.com")

    def test_enhance_unknown(self):
        self.assertRaises(errors.PluginError, self.installer.enhance, 'myhost', 'unknown')

    def test_enhance_staple_ocsp(self):
        self.installer.parser = mock.MagicMock()

        self.installer.enhance('myhost', 'staple-ocsp')
        self.installer.parser.set_directive.assert_called_once_with("tls_ocsp_file", mock.ANY)

    @mock.patch("certbot_nginx.configurator.util.run_script")
    def test_config_test(self, mock_runscript):
        mock_runscript.returnvalue = 1

        self.installer.parser = mock.MagicMock()
        self.installer.config_test()

    @mock.patch("certbot.reverter.Reverter.recovery_routine")
    def test_recovery_routine_throws_error_from_reverter(self, mock_recovery_routine):
        self.installer.parser = mock.MagicMock()

        mock_recovery_routine.side_effect = errors.ReverterError("foo")
        self.assertRaises(errors.PluginError, self.installer.recovery_routine)

    @mock.patch("certbot.reverter.Reverter.view_config_changes")
    def test_view_config_changes_throws_error_from_reverter(self, mock_view_config_changes):
        mock_view_config_changes.side_effect = errors.ReverterError("foo")
        self.assertRaises(errors.PluginError, self.installer.view_config_changes)

    @mock.patch("certbot.reverter.Reverter.rollback_checkpoints")
    def test_rollback_checkpoints_throws_error_from_reverter(self, mock_rollback_checkpoints):
        mock_rollback_checkpoints.side_effect = errors.ReverterError("foo")
        self.assertRaises(errors.PluginError, self.installer.rollback_checkpoints)


def get_exim_installer(
        config_path, config_dir, work_dir, logs_dir):
    """Create an Exim Configurator with the specified options."""

    backups = os.path.join(work_dir, "backups")

    with mock.patch("certbot_exim.installer.EximInstaller."
                    "config_test"):
        with mock.patch("certbot_exim.installer.util."
                        "exe_exists") as mock_exe_exists:
            mock_exe_exists.return_value = True
            config = installer.EximInstaller(
                config=mock.MagicMock(
                    nginx_server_root=config_path,
                    le_vhost_ext="-le-ssl.conf",
                    config_dir=config_dir,
                    work_dir=work_dir,
                    logs_dir=logs_dir,
                    backup_dir=backups,
                    temp_checkpoint_dir=os.path.join(work_dir, "temp_checkpoints"),
                    in_progress_dir=os.path.join(backups, "IN_PROGRESS"),
                    server="https://acme-server.org:443/new",
                    tls_sni_01_port=5001,
                ),
                name="exim")

    # Provide general config utility.
    nsconfig = configuration.NamespaceConfig(config.config)
    zope.component.provideUtility(nsconfig)

    return config


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
