"""Tests for certbot_exim.parser."""
import unittest

from certbot_exim import parser, constants


class EximParserTest(unittest.TestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        self.parser = parser.EximParser(constants.CLI_DEFAULTS['server_root'],
                                        False)

    def test_get_files(self):
        self.parser.get_files()

    def test_get_directive(self):
        self.parser.get_directive(None)

    def test_set_directive(self):
        self.parser.set_directive(None, None)

    def test_load(self):
        self.parser.load()

    def test_dump(self):
        self.parser.dump()
