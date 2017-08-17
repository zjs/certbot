"""Tests for certbot_exim.installer."""

import copy
import os
import pkg_resources
import shutil
import tempfile
import unittest

import mock

import zope.component

from certbot import configuration
from certbot import achallenges
from certbot import crypto_util
from certbot import errors
from certbot.tests import util as certbot_test_util

from certbot.plugins import common

from certbot_exim import installer

class EximTest(unittest.TestCase):
    def setUp(self):
        super(EximTest, self).setUp()

        self.temp_dir, self.config_dir, self.work_dir = common.dir_setup(
            "etc_exim4", "certbot_exim.tests")
        self.logs_dir = tempfile.mkdtemp('logs')

        self.config_path = os.path.join(self.temp_dir, "etc_exim4")
        self.config = get_exim_installer(
            self.config_path, self.config_dir, self.work_dir, self.logs_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        shutil.rmtree(self.config_dir)
        shutil.rmtree(self.work_dir)
        shutil.rmtree(self.logs_dir)

    @mock.patch("certbot_exim.installer.util.exe_exists")
    def test_prepare_no_install(self, mock_exe_exists):
        mock_exe_exists.return_value = False
        self.assertRaises(
            errors.NoInstallationError, self.config.prepare)

    def test_prepare(self):
        pass

    def test_supported_enhancements(self):
        self.assertEqual(['staple-ocsp'],
                         self.config.supported_enhancements())

    def test_get_all_names(self):
        pass

    def test_enhance(self):
        self.assertRaises(
            errors.PluginError, self.config.enhance, 'myhost', 'unknown_enhancement')

    def test_config_test(self):
        pass

    def test_ocsp_stapling(self):
        pass




def get_exim_installer(
        config_path, config_dir, work_dir, logs_dir):
    """Create an Nginx Configurator with the specified options."""

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
            config.prepare()

    # Provide general config utility.
    nsconfig = configuration.NamespaceConfig(config.config)
    zope.component.provideUtility(nsconfig)

    return config


def get_data_filename(filename):
    """Gets the filename of a test data file."""
    return pkg_resources.resource_filename(
        "certbot_exim.tests", os.path.join(
            "testdata", "etc_exim4", filename))


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
