import configparser

from baker import settings
from baker.secret import Encryption, SecretKey
from baker.repository import is_url
from baker.storage import Storage


class RecipeParser:
    def __init__(self, file, case_sensitive=False):
        self.parser = None
        self.instructions = []
        self.case_sensitive = case_sensitive or settings.get('RECIPE_CASE_SENSITIVE')
        self.recipe_file = file
        filename = file.lower()

        if filename.endswith('.cfg'):
            self.dict_from_ini()
        # elif filename.endswith('.yml'): # TODO: Add support recipes via yaml file
        #     self.dict_from_yaml()
        else:
            raise FileExistsError('Unsupported file format')

    def dict_from_ini(self):
        self.parser = configparser.ConfigParser()

        if self.case_sensitive:
            self.parser.optionxform = str

        self.parser.read(self.recipe_file, encoding=settings.get('ENCODING'))

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

                    self.instructions.append(Instruction(template, variables, secrets))
        else:
            raise FileExistsError('Unable to read instructions from file')

    def update_secrets(self):
        for instruction in self.instructions:
            if instruction.secrets:
                section = instruction.name + ':secrets'
                for idx, secret in instruction.secrets.items():
                    self.parser[section][idx] = secret

        Storage.parser(self.recipe_file, self.parser, write_mod=True)

    @ staticmethod
    def _get_values(parser, section):
        values = None
        if parser.has_section(section):
            values = dict(parser.items(section))
        return values


class Instruction:
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
                raise AttributeError("Remote template must have attribute 'path'")

        for attr, value in template.items():
            if attr not in ['template', 'path', 'name', 'user', 'group', 'mode']:
                raise AttributeError("Unsupported attribute '%s'in recipe file" % attr)
            self.__setattr__(attr, value)
