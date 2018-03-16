import os, shutil
from string import Template

from baker.settings import TEMPLATE_EXT, DEBUG


class ReplaceTemplate:
    def __init__(self, configs):
        self.configs = configs

    def replace(self):
        # FIXME: Support ignore case replace
        for idx, config in enumerate(self.configs):
            template_file = open(config.template).read()
            template = BakerTemplate(template_file)
            replaced = template.substitute(config.variables)
            target = config.template

            if hasattr(config, 'path'):
                target = config.path

            if TEMPLATE_EXT and target.endswith(TEMPLATE_EXT):
                ext_size = len(TEMPLATE_EXT) + 1
                target = target[:-ext_size]

            open(target, 'w').write(replaced)

            self._add_file_permission(config, target)

            if DEBUG:  # TODO: Move for a file that care about feedback with cli
                print('\t ', config.name, config.template)
                print('\t\t ', target)
            else:
                print('  ' + '.' * (idx + 1), end='\r')

    @staticmethod
    def _add_file_permission(config, path):
        if hasattr(config, 'user') or hasattr(config, 'group'):
            user = config.user if hasattr(config, 'user') else None
            group = config.group if hasattr(config, 'group') else None
            shutil.chown(path, user, group)
        if hasattr(config, 'mode'):
            os.chmod(path, int(config.mode, 8))


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
