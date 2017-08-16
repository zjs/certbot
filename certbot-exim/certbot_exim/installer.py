"""Installer for Exim."""
import logging

import zope.interface

from certbot import interfaces
from certbot.plugins import common

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IInstaller)
@zope.interface.provider(interfaces.IPluginFactory)
class Installer(common.Plugin):
    """Exim installer.

    TODO: implement
    """

    @classmethod
    def add_parser_arguments(cls, add):
        pass

    def __init__(self, *args, **kwargs):
        super(Installer, self).__init__(*args, **kwargs)

    def more_info(self):
        pass

    def prepare(self):
        pass

    def get_all_names(self):
        pass

    def deploy_cert(self, domain, cert_path, key_path, chain_path, fullchain_path):
        pass

    def restart(self):
        pass

    def supported_enhancements(self):
        pass

    def enhance(self, domain, enhancement, options=None):
        pass

    def save(self, title=None, temporary=False):
        pass

    def rollback_checkpoints(self, rollback=1):
        pass

    def recovery_routine(self):
        pass

    def view_config_changes(self):
        pass

    def config_test(self):
        pass
