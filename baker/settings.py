from configparser import ConfigParser
from itertools import chain
from pathlib import Path


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

    def convert_if_bool(string):
        lower_str = string.lower()
        if lower_str in ('true', 'false'):
            return True if lower_str == 'true' else False
        return string

    _init()

    if Path(rc_file_path).is_file():
        parser = ConfigParser()
        with open(rc_file_path) as lines:
            lines = chain(("[DEFAULT]",), lines)
            parser.read_file(lines)

        for key, value in parser.defaults().items():
            upper_key = key.upper()

            if upper_key not in globals():
                raise AttributeError("Setting '{0}' in '{1}' is not supported.".format(
                                     upper_key, rc_file_path))
            globals()[upper_key] = convert_if_bool(value)

    for key, value in kwargs.items():
        globals()[key] = value


def get(key):
    return globals()[key]


def values():
    return globals()
