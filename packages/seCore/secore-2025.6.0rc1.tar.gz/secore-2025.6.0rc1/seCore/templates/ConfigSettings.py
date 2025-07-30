import textwrap

# Constants containing default environment settings
DEFAULT_ENV_SETTINGS = textwrap.dedent('''\
    # Configuration Settings
    # ------------------------------------------------------------------------------------------------------------------
    # NOTE: No need to use quotes around values but you can use single, double or no quotes.
    #       The values are the items to the right of the equals sign, and comments are stripped from the line.
    # ------------------------------------------------------------------------------------------------------------------
    [Encryption]
    fn_key                  = '${fn_key}'

    [Logging]
    log_level               = 'DEBUG'                       # Set logging level. Options: DEBUG, INFO, WARNING
    # log_format: Default is Enterprise
      # Basic:              '{extra[app]} | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>'
      # Simple:             '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {extra[app]} | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>'
      # Enterprise:         '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {extra[app]} | <blue>{extra[request_id]}</blue> | <green>{extra[key]}</green> | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>'
    #log_format              = '{extra[app]} | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>'
    log_appname             = 'seCore'                      # Used to write to standard out what app is logging
    
    [Settings]
    setting_1               = 'value_1'
    setting_2               = 'value_2'
''')

DEFAULT_ENV_SECRET_SETTINGS = textwrap.dedent('''\
    # Configuration Secret Settings
    # ------------------------------------------------------------------------------------------------------------------
    # Passwords/API parameters or any other setting that doesn't need to be checked into source control
    #
    # NOTE: No need to use quotes around values but you can use single, double or no quotes.
    #       The values are the items to the right of the equals sign, and comments are stripped from the line.
    # ------------------------------------------------------------------------------------------------------------------
    [Env]
    environment             = "Local"                       # Valid: 'Local', 'Dev', 'Test', 'Prod'
        
    [MS Sql]
    mssql_username          = '{username}'                  # Can be encrypted or plain text
    mssql_password          = '{password}'                  # Can be encrypted or plain text
    mssql_hostname          = '{hostname}'                  # Hostname must resolve to IP to work in OpenShift
    mssql_port              = '{port}'
    mssql_database          = '{default_database}'
    mssql_trust             = '{trust}'                     # Valid: 'yes', 'no' - Needs to be a SQL account to work in OpenShift
''')
