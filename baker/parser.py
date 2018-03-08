import re

from string import Template
from configparser import ConfigParser

from baker.settings import CONFIG_CASE_SENSITIVE
from baker.secret import Encryption, SecretKey


class ReadConfig:
    def __init__(self, file):
        self.configs = []
        self.config_file = file
        filename = file.lower()

        if filename.endswith('.cfg'):
            self.dict_from_ini()
        # elif filename.endswith('.yml'):
        #     self.dict_from_yaml()
        else:
            raise FileExistsError('Unsupported file format.')

    def dict_from_ini(self):
        parser = ConfigParser()

        if CONFIG_CASE_SENSITIVE:
            parser.optionxform = str

        parser.read(self.config_file, encoding='utf-8')

        if parser.sections():
            templates = set(map(lambda x: x.rsplit(':', 1)[0], parser.sections()))
            for name in templates:
                variables = self._get_values(parser, name + ':variables')
                secrets = self._get_values(parser, name + ':secrets')
                template = self._get_values(parser, name + ':template')

                if template:
                    template['name'] = name
                else:
                    raise AttributeError('Attribute template is required.')

                self.configs.append(Config(template, variables, secrets))
        else:
            raise FileExistsError('Unable to read configs from file.')

    @staticmethod
    def _get_values(parser, section):
        values = None
        if parser.has_section(section):
            values = dict(parser.items(section))
        return values


class Config:
    def __init__(self, template, variables=None, secrets=None):
        self._template(template)
        self.variables = variables
        self._secrets(secrets)

    def _secrets(self, secrets):
        if secrets:
            if not self.variables:
                self.variables = {}
            secret_key = SecretKey()
            encryption = Encryption(secret_key.key)
            for var, secret in secrets.items():
                decrypted_value = encryption.decrypt(secret)
                self.variables[var] = decrypted_value

    def _template(self, template):
        for var, value in template.items():
            if var not in ['template', 'path', 'name', 'user', 'group', 'mode']:
                raise AttributeError("Unsupported attribute '" + var + "'in config file.")
            self.__setattr__(var, value)


class BakerTemplate(Template):
    delimiter = '{{ '
    pattern = r'''
        \{\{ (?:
           (?P<escaped>\\)                | # Expression [-- will become [-
           (?P<named>[_a-z][_a-z0-9]*) \}\} | # -, [, ], and \n can't be used in names
           \b\B(?P<braced>)              | # Braced names disabled
           (?P<invalid>)                 | #
        )
    '''


class ReplaceTemplate:
    def __init__(self, configs):
        print(configs[0].variables)
        self.configs = configs

    def replace(self):
        for config in self.configs:
            template = open(config.template).read()
            print(template)
            replaced = BakerTemplate(template).substitute(config.variables)
            print(replaced)


def replace():
    # read configs
    config = ConfigParser()
    config.optionxform = str
    config.read('values.cfg')

    # instance encryption
    encryption = Encryption(SecretKey().key)

    # find and decrypt secret values
    def decrypt_secrets(items):
        def call(value):
            secret_val = re.search('_secret\((.+?)\)', value)
            if secret_val:
                return encryption.decrypt(secret_val.group(1))
            return value
        return dict(map(lambda i: (i[0], call(i[1])), items))

    # replace files
    for file_location in config.sections():
        values = dict(config.items(file_location))
        values = decrypt_secrets(values.items())
        template = open(file_location).read()
        replacement = Template(template).substitute(values)
        open(file_location[:-4], 'w').write(replacement)
