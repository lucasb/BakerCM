import os
import shutil

from string import Template

from baker import settings
from baker import logger
from baker.repository import download


class ReplaceTemplate:
    def __init__(self, instructions):
        self.instructions = instructions

    def replace(self):
        for instruction in self.instruction:
            # FIXME: Add force option
            template_path = download(instruction.template) if instruction.is_remote else instruction.template
            template_file = self._file(template_path)
            template = BakerTemplate(template_file)
            replaced = template.replace(instruction.variables) if instruction.variables else template_file
            target = instruction.template

            if hasattr(instruction, 'path'):
                target = instruction.path

            if settings.get('TEMPLATE_EXT') and target.endswith(settings.get('TEMPLATE_EXT')):
                ext_size = len(settings.get('TEMPLATE_EXT')) + 1
                target = target[:-ext_size]

            self._file(target, mode='w', content=replaced)
            self._add_file_permission(instruction, target)
            logger.log(instruction.name, instruction.template, target)

    @staticmethod
    def _file(path, mode='r', content=None):
        try:
            with open(path, mode) as file:
                if mode == 'r':
                    return file.read()
                elif content:
                    return file.write(content)
        except FileNotFoundError:
            raise FileNotFoundError(
                "Template not found at: '%s'. Are you sure that it is available on this path?"
                % path
            )

    @staticmethod
    def _add_file_permission(instruction, path):
        if hasattr(instruction, 'user') or hasattr(instruction, 'group'):
            user = instruction.user if hasattr(instruction, 'user') else None
            group = instruction.group if hasattr(instruction, 'group') else None
            shutil.chown(path, user, group)
        if hasattr(instruction, 'mode'):
            os.chmod(path, int(instruction.mode, 8))


class BakerTemplate(Template):
    delimiter = '{{'
    pattern = r'''
        \{\{\ *(?:
        (?P<escaped>\\)                     | # escape with {{\escape}} or {{\ escape }}} 
        (?P<named>[_a-z][_a-z0-9]*)\ *}}    | # identifier {{var}} or {{ var }}
        \b\B(?P<braced>)                    | # braced identifier disabled
        (?P<invalid>)                         # ill-formed delimiter expr
        )
    '''

    def replace(self, mapping):
        try:
            if settings.get('RECIPE_CASE_SENSITIVE'):
                return super(BakerTemplate, self).substitute(mapping)
            else:
                return self.ignore_case_substitute(mapping)
        except KeyError as e:
            raise KeyError('Missing variable %s' % e)

    def ignore_case_substitute(self, mapping):
        if not mapping:
            raise TypeError(
                "Descriptor 'ignore_case_substitute' of 'BakerTemplate' object needs an argument."
            )

        def convert(mo):
            named = mo.group('named')
            if named is not None:
                return str(mapping[named.lower()])
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern', self.pattern)
        return self.pattern.sub(convert, self.template)
