from string import Template
from configparser import ConfigParser

from baker.settings import CONFIG_CASE_SENSITIVE, DEBUG
from baker.secret import Encryption, SecretKey


class ReadConfig:
    def __init__(self, file):
        self.configs = []  # FIXME: Add safe code to get the order of configs are the same of file
        self.config_file = file
        filename = file.lower()

        if filename.endswith('.cfg'):
            self.dict_from_ini()
        # elif filename.endswith('.yml'): # TODO: Add support to configure via yaml file
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
                raise AttributeError("Unsupported attribute '%s'in config file." % var)
            self.__setattr__(var, value)


class BakerTemplate(Template):
    delimiter = '{{'
    pattern = r'''
        \{\{\ *(?:
        (?P<escaped>{)                    | # escape with {{{escape}}} or {{{ escape }}} 
        (?P<named>[_a-z][_a-z0-9]*)\ *}}  | # identifier {{var}} or {{ var }}
        \b\B(?P<braced>)                  | # braced identifier disabled
        (?P<invalid>)                       # ill-formed delimiter expr
        )
    '''
    # FIXME: Replace escape regex to work with braces in the ends too


# TODO: Add support for permission using user, group, mode config attr
class ReplaceTemplate:
    def __init__(self, configs):
        self.configs = configs

    def replace(self):
        # FIXME: Support ignore care replace
        for idx, config in enumerate(self.configs):
            template_file = open(config.template).read()
            template = BakerTemplate(template_file)
            replaced = template.substitute(config.variables)
            target = config.template

            if hasattr(config, 'path'):
                target = config.path
            if target.endswith('.tpl'):  # TODO: Add support to choose template extension
                target = target[:-4]  # TODO: Add support to choose remove template ext or not
            open(target, 'w').write(replaced)

            if DEBUG:  # TODO: Move for a file that care about feedback with cli
                print('\t ', config.name, config.template)
                print('\t\t ', target)
            else:
                print('  ' + '.' * (idx + 1), end='\r')
