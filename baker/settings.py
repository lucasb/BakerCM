from configparser import ConfigParser
from itertools import chain
from pathlib import Path


_HOME_PATH = str(Path.home())

_REPOSITORY_PATTERNS = {
    'github': '%(repository)s/%(version)s/%(path)s',
    'bitbucket': '%(repository)s/%(path)s?at=%(version)s',
    'custom': '%(custom)s',
}

_default_values = {
    # This method transforms option names on every read, get, or set operation.
    # The default config keys are case insensitive. E.g. True -> for case sensitive.
    'CONFIG_CASE_SENSITIVE': False,

    # DEBUG mode is False as default, it can be change in config file.
    # Using option --verbose in command line DEBUG change to true.
    'DEBUG': False,

    # Encode of files and secrets
    'ENCODING': 'utf-8',

    # Repository url including protocol http/https and domain until the root folder.
    'REPOSITORY': None,

    # Type of repository to use some pattern that is know like: github or bitbucket.
    # Pattern can be customized setting it as custom and filling REPOSITORY_CUSTOM_PATTERN config.
    'REPOSITORY_TYPE': None,

    # Customization of repository access the recipes with configurations.
    # To build pattern use variables to build url to access config in a remote repository.
    # E.g.: '%(repository)s/%(path)s/%(version)s'
    'REPOSITORY_CUSTOM_PATTERN': None,

    # Absolute path to store files when downloaded via baker
    'STORAGE_FILES': _HOME_PATH + '/.baker/',

    # Absolute path to store baker key to use secret values
    'STORAGE_KEY_PATH': _HOME_PATH + '/.baker.key',

    # Extension for template files. Set 'None' to disable replacement of template name.
    'TEMPLATE_EXT': 'tpl',
}


def load(**kwargs):
    global BAKER_SETTINGS
    BAKER_SETTINGS = _default_values
    rc_file_path = _HOME_PATH + '/.bakerc'

    def convert_if_bool(string):
        lower_str = string.lower()
        if lower_str in ('true', 'false'):
            return lower_str == 'true'
        return string

    if Path(rc_file_path).is_file():
        parser = ConfigParser()

        with open(rc_file_path) as lines:
            lines = chain(("[DEFAULT]",), lines)
            parser.read_file(lines)

        for key, value in parser.defaults().items():
            upper_key = key.upper()

            if upper_key not in values():
                raise AttributeError(
                    "Setting '{0}' at '{1}' is not supported.".format(upper_key, rc_file_path)
                )

            values()[upper_key] = convert_if_bool(value)

    for key, value in kwargs.items():
        values()[key] = value


def get(key):
    return values()[key]


def values():
    return globals()['BAKER_SETTINGS']
