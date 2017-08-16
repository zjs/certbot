'''exim plugin constants'''


CLI_DEFAULTS = dict(
    server_root="/etc/exim4",
    restart_cmd=['/etc/init.d/exim4', 'restart'],
    reconfig_cmd=['update-exim4.conf']
)
