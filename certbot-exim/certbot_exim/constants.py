'''exim plugin constants'''

CLI_DEFAULTS = dict(
    server_root='/etc/exim4',
    restart_cmd='/etc/init.d/exim4 restart',
    reconfig_cmd=['update-exim4.conf'],
    file_configuration='single-file',
    config_file_location='/usr/exim/configure',
    config_listmacrosdefs='/etc/exim4/conf.d/main/01_exim4-config_listmacrosdefs',
    config_options='/etc/exim4/conf.d/main/02_exim4-config_options',
    tls_config_options='/etc/exim4/conf.d/main/03_exim4-config_tlsoptions',
    config_log_selector='/etc/exim4/conf.d/main/90_exim4-config_log_selector'
)
