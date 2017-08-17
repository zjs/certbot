"""Tests for certbot_exim.installer."""

import copy
import os
import pkg_resources
import shutil
import tempfile
import unittest

import mock

from certbot import configuration

from certbot.tests import util as test_util

from certbot.plugins import common

from certbot_exim import installer

class EximTest(unittest.TestCase):
    def setUp(self):
        super(EximTest, self).setUp()

        self.temp_dir, self.config_dir, self.work_dir = common.dir_setup(
            "etc_exim4", "certbot_exim.tests")
        self.logs_dir = tempfile.mkdtemp('logs')

        self.config_path = os.path.join(self.temp_dir, "etc_nginx")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        shutil.rmtree(self.config_dir)
        shutil.rmtree(self.work_dir)
        shutil.rmtree(self.logs_dir)


def get_data_filename(filename):
    """Gets the filename of a test data file."""
    return pkg_resources.resource_filename(
        "certbot_exim.tests", os.path.join(
            "testdata", "etc_exim4", filename))


