from pathlib import Path

HOME_DIR = str(Path.home())

# TODO: add check for config for each value below
# Absolute path to store baker key to use secret values
STORAGE_KEY_PATH = HOME_DIR + '/.baker.key'

# This method transforms option names on every read, get, or set operation.
# The default config keys are case insensitive. E.g. True -> for case sensitive.
CONFIG_CASE_SENSITIVE = False

# DEBUG mode is False as default, it can be change in config file.
# Using option --verbose in command line DEBUG change to true.
DEBUG = False

# Encode of files and secrets
ENCODING = 'utf-8'

# Extension for template files. Set 'None' to disable replacement of template name.
TEMPLATE_EXT = 'tpl'
