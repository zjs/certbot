"""Installer for Exim."""
import logging

import zope.interface

from certbot import errors
from certbot import interfaces
from certbot import util
from certbot.plugins import common

from certbot_exim import constants

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IInstaller)
@zope.interface.provider(interfaces.IPluginFactory)
class Installer(common.Plugin):
    """Exim installer.

    TODO: implement
    """

    @classmethod
    def add_parser_arguments(cls, add):
        add("server-root", default=constants.CLI_DEFAULTS["server_root"],
            help="Exim server root directory.")

    def __init__(self, *args, **kwargs):
        super(Installer, self).__init__(*args, **kwargs)

        self._enhance_func = {"staple-ocsp": self._enable_ocsp_stapling}

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return 'This plugin configures Exim to use a certificate.'

    def prepare(self):
        """Check if exim daemon is installed.

        :raises .errors.NoInstallationError: If Exim command cannot be found
        """
        restart_cmd = constants.CLI_DEFAULTS['restart_cmd']
        if not util.exe_exists(restart_cmd):
            raise errors.NoInstallationError(
                'Cannot find command {0}'.format(restart_cmd))

    def get_all_names(self):
        """Returns all names known to Exim.

        :rtype: `collections.Iterable` of `str`
        """
        pass  # TODO: return the value of `primary_hostname` from the Exim config

    def deploy_cert(self, domain, cert_path, key_path, chain_path,
                    fullchain_path):
        """Deploy certificate.

        :param str domain: domain to deploy certificate file
        :param str cert_path: absolute path to the certificate file
        :param str key_path: absolute path to the private key file
        :param str chain_path: absolute path to the certificate chain file
        :param str fullchain_path: absolute path to the certificate fullchain
            file (cert plus chain)

        :raises .PluginError: when cert cannot be deployed
        """
        pass

    def restart(self):
        """Restart exim daemon"""
        try:
            util.run_script(constants.CLI_DEFAULTS['restart_cmd'])
        except errors.SubprocessError as err:
            raise errors.MisconfigurationError(str(err))

    def config_test(self):
        """Check the Exim configuration for errors.

        :raises .errors.MisconfigurationError: If config_test fails
        """
        pass

    ##################################
    # Enhancement methods (IInstaller)
    ##################################

    def supported_enhancements(self):  # pylint: disable=no-self-use
        """Returns a `collections.Iterable` of supported enhancements.

        :returns: supported enhancements which should be a subset of
            :const:`~certbot.constants.ENHANCEMENTS`
        :rtype: :class:`collections.Iterable` of :class:`str`
        """
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

        :param str domain: domain to enable OCSP response for
        :param chain_path: chain file path
        :type chain_path: `str` or `None`
        """
        pass  # TODO: Write `tls_ocsp_file = $chain_path` to the configuration file for $domain

    ###################################################
    # Wrapper functions for Reverter class (IInstaller)
    ###################################################

    # TODO: Implement these methods using a `reverter.Reverter` instance

    def save(self, title=None, temporary=False):
        """Saves all changes to the configuration files.

        Both title and temporary are needed because a save may be
        intended to be permanent, but the save is not ready to be a full
        checkpoint.

        It is assumed that at most one checkpoint is finalized by this
        method. Additionally, if an exception is raised, it is assumed a
        new checkpoint was not finalized.

        :param str title: The title of the save. If a title is given, the
            configuration will be saved as a new checkpoint and put in a
            timestamped directory. `title` has no effect if temporary is true.

        :param bool temporary: Indicates whether the changes made will
            be quickly reversed in the future (challenges)

        :raises .errors.PluginError: If there was an error in
            an attempt to save the configuration, or an error creating a
            checkpoint
        """
        pass

    def rollback_checkpoints(self, rollback=1):
        """Revert `rollback` number of configuration checkpoints.

        :param int rollback: Number of checkpoints to revert

        :raises .errors.PluginError: If there is a problem with the input or
            the function is unable to correctly revert the configuration
        """
        pass

    def recovery_routine(self):
        """Revert configuration to most recent finalized checkpoint.

        Remove all changes (temporary and permanent) that have not been
        finalized. This is useful to protect against crashes and other
        execution interruptions.

        :raises .errors.PluginError: If unable to recover the configuration
        """
        pass

    def view_config_changes(self):
        """Show all of the configuration changes that have taken place.

        :raises .errors.PluginError: If there is a problem while processing
            the checkpoints directories.
        """
        pass
