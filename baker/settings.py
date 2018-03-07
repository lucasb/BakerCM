from pathlib import Path

HOME_DIR = str(Path.home())

# Absolute path to store baker key to use secret values
STORAGE_KEY_PATH = HOME_DIR + '/.baker.key'  # TODO: add check for config

# This method transforms option names on every read, get, or set operation.
# The default config keys are case insensitive. E.g. True -> for case sensitive.
CONFIG_CASE_SENSITIVE = False
