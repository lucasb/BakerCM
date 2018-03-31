from pathlib import Path
from configparser import ConfigParser


def _init():
    global CONFIG_CASE_SENSITIVE, DEBUG, ENCODING, STORAGE_KEY_PATH, TEMPLATE_EXT

    # This method transforms option names on every read, get, or set operation.
    # The default config keys are case insensitive. E.g. True -> for case sensitive.
    CONFIG_CASE_SENSITIVE = False

    # DEBUG mode is False as default, it can be change in config file.
    # Using option --verbose in command line DEBUG change to true.
    DEBUG = False

    # Encode of files and secrets
    ENCODING = 'utf-8'

    # Absolute path to store baker key to use secret values
    STORAGE_KEY_PATH = str(Path.home()) + '/.baker.key'

    # Extension for template files. Set 'None' to disable replacement of template name.
    TEMPLATE_EXT = 'tpl'


def load(**kwargs):
    rc_file_path = str(Path.home()) + '/.bakerc'

    _init()

    if Path(rc_file_path).is_file():  # TODO: add check for config for each value below
        configs = ConfigParser()
        configs.read(rc_file_path, encoding=ENCODING)

        for key, value in configs.items():
            upper_key = key.upper()
            if upper_key not in globals():
                raise AttributeError("Setting '%s' in '%s' is not supported."
                                     % upper_key, rc_file_path)
            globals()[upper_key] = value

    for key, value in kwargs.items():
        globals()[key] = value


def get(key):
    return globals()[key]


def values():
    return globals()
