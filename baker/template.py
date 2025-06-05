import os
import re
import shutil

from string import Template

from baker import settings
from baker import logger
from baker.storage import Storage


class ReplaceTemplate:
    """
    Replace items in template file based on recipe mapping
    """
    def __init__(self, instructions):
        self.instructions = instructions

    def replace(self):
        """
        Replace variables in template file based on recipe instructions
        """
        for instruction in self.instructions:
            target = instruction.template
            template_path = instruction.template
            replaced = Storage.file(template_path)

            if instruction.variables:
                template = BakerTemplate(replaced)
                replaced = template.replace(instruction.variables)

            if hasattr(instruction, 'path'):
                target = instruction.path

            if settings.get('TEMPLATE_EXT') and target.endswith(settings.get('TEMPLATE_EXT')):
                ext_size = len(settings.get('TEMPLATE_EXT')) + 1
                target = target[:-ext_size]

            Storage.file(target, content=replaced)
            self._add_file_permission(instruction, target)
            logger.log(instruction.name, instruction.template, target)

    @staticmethod
    def _add_file_permission(instruction, path):
        """
        Add permission and owner for templates files after replace
        """
        if hasattr(instruction, 'user') or hasattr(instruction, 'group'):
            user = instruction.user if hasattr(instruction, 'user') else None
            group = instruction.group if hasattr(instruction, 'group') else None
            shutil.chown(path, user, group)
        if hasattr(instruction, 'mode'):
            os.chmod(path, int(instruction.mode, 8))


class BakerTemplate(Template):
    """
    Template with baker pattern of variables
    """
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
        """
        Replace variable based on mapping key
        """
        try:
            if settings.get('RECIPE_CASE_SENSITIVE'):
                return super(BakerTemplate, self).substitute(mapping)
            else:
                return self.ignore_case_substitute(mapping)
        except KeyError as e:
            raise KeyError('Missing variable %s' % e)

    def ignore_case_substitute(self, mapping):
        """
        Substitution of values in replace ignoring case sensitive of variables
        """
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

        # Compile the pattern with re.VERBOSE flag to ensure compatibility across Python versions
        compiled_pattern = re.compile(self.pattern, re.VERBOSE)
        return compiled_pattern.sub(convert, self.template)
