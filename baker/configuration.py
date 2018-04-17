import configparser

from baker import settings
from baker.secret import Encryption, SecretKey
from baker.repository import is_url


class ConfigParser:
    def __init__(self, file, case_sensitive=False):
        self.parser = None
        self.configs = []
        self.case_sensitive = case_sensitive or settings.get('CONFIG_CASE_SENSITIVE')
        self.config_file = file
        filename = file.lower()

        if filename.endswith('.cfg'):
            self.dict_from_ini()
        # elif filename.endswith('.yml'): # TODO: Add support to configure via yaml file
        #     self.dict_from_yaml()
        else:
            raise FileExistsError('Unsupported file format')

    def dict_from_ini(self):
        self.parser = configparser.ConfigParser()

        if self.case_sensitive:
            self.parser.optionxform = str

        self.parser.read(self.config_file, encoding=settings.get('ENCODING'))

        if self.parser.sections():
            curr_template = None

            for section in self.parser.sections():
                name = section.rsplit(':', 1)[0]

                if name != curr_template:
                    curr_template = name

                    variables = self._get_values(self.parser, name + ':variables')
                    secrets = self._get_values(self.parser, name + ':secrets')
                    template = self._get_values(self.parser, name + ':template')

                    if template:
                        template['name'] = name
                    else:
                        raise AttributeError('Attribute template is required')

                    self.configs.append(Config(template, variables, secrets))
        else:
            raise FileExistsError('Unable to read configs from file')

    def update_secrets(self):
        for config in self.configs:
            if config.secrets:
                section = config.name + ':secrets'
                for idx, secret in config.secrets.items():
                    self.parser[section][idx] = secret

        try:
            with open(self.config_file, 'w') as configfile:
                self.parser.write(configfile)
        except FileNotFoundError:
            raise FileNotFoundError(
                "Configuration file not found at: '%s'. "
                "Are you sure that it is available on this path?"
                % self.config_file
            )

    @ staticmethod
    def _get_values(parser, section):
        values = None
        if parser.has_section(section):
            values = dict(parser.items(section))
        return values


class Config:
    def __init__(self, template, variables=None, secrets=None):
        self._template(template)
        self.variables = variables
        self.secrets = secrets

    def secrets_to_plan(self):
        if self.secrets:
            if not self.variables:
                self.variables = {}
            secret_key = SecretKey()
            encryption = Encryption(secret_key.key)

            for idx, secret in self.secrets.items():
                decrypted_value = encryption.decrypt(secret)
                self.variables[idx] = decrypted_value

    def plan_to_secrets(self):
        if self.secrets:
            secret_key = SecretKey()
            encryption = Encryption(secret_key.key)
            items = self.secrets.items()
            self.secrets = dict(map(lambda s: (s[0], encryption.encrypt(s[1])), items))

    def _template(self, template):
        self.__setattr__('is_remote', False)
        if is_url(template['template']):
            self.__setattr__('is_remote', True)

            if not template['path']:
                raise AttributeError("Remove template must have attribute 'path'")

        for attr, value in template.items():
            if attr not in ['template', 'path', 'name', 'user', 'group', 'mode']:
                raise AttributeError("Unsupported attribute '%s'in config file" % attr)
            self.__setattr__(attr, value)
