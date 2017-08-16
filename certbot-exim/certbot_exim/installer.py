"""Installer for Exim."""
import logging

import zope.interface

from certbot import errors
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

        self._enhance_func = {"staple-ocsp": self._enable_ocsp_stapling}

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

    def supported_enhancements(self):  # pylint: disable=no-self-use
        """Returns currently supported enhancements."""
        return ['staple-ocsp']

    def enhance(self, domain, enhancement, options=None):
        """Perform a configuration enhancement.

        :param str domain: domain for which to provide enhancement
        :param str enhancement: An enhancement as defined in
            :const:`~certbot.constants.ENHANCEMENTS`
        :param options: Flexible options parameter for enhancement.
            Check documentation of
            :const:`~certbot.constants.ENHANCEMENTS`
            for expected options for each enhancement.

        :raises .PluginError: If Enhancement is not supported, or if
            an error occurs during the enhancement.
        """
        try:
            return self._enhance_func[enhancement](domain, options)
        except (KeyError, ValueError):
            raise errors.PluginError("Unsupported enhancement: {0}".format(enhancement))
        except errors.PluginError:
            logger.warning("Failed %s for %s", enhancement, domain)
            raise

    def _enable_ocsp_stapling(self, domain, chain_path):
        """Enables OCSP Stapling
        """
        pass  # TODO: Write `tls_ocsp_file = $chain_path` to the configuration file for $domain

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
