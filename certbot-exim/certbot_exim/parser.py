"""Configuration file parser for Exim."""

class EximParser(object):
    """Parse and mutate an Exim configuration.

    Supports both single-file and split-file configurations.
    """

    def __init__(self, server_root, file_configuration):
        """
        Initialize the Exim parser

        :param str server_root: The path to the server's configuration file(s).
        :param bool file_configuration: True if Exim is using a single-file configuration.
        """
        pass  # TODO

    def get_files(self):
        """
        Return the set of files being managed by the parser

        :return: The file or files being managed by the parser
        :rtype: :class:`collections.Iterable` of :class:`str`
        """
        pass  # TODO

    def get_directive(self, directive):
        """
        Retrieve the current value for a directive

        :param str directive: The directive name.
        :return: The current value for that directive, or `None` if it is not set.
        :rtype: str
        """
        pass  # TODO

    def set_directive(self, directive, value):
        """
        Set a new value for a directive

        :param str directive: The directive name.
        :param str value: The directive value.
        """
        pass  # TODO

    def load(self):
        """
        Load the current contents of the configuration into memory.
        """
        pass  # TODO

    def dump(self):
        """
        Atomically write the configuration from memory to disk.

        Using a temporary file and a move operation to ensure partial changes are not written,
        even in the event of a crash.
        """
        pass  # TODO
