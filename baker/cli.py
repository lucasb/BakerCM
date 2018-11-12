import argparse

from baker import __version__


class Parser:
    """
    Parser to build command line interface
    """
    def __init__(self, args, commands):
        self.parser, encrypt = self._build_cli(commands)
        self.options = self.parser.parse_args(args)
        self._parser_checks(encrypt, args)

    def execute(self):
        """
        Execute commands defined in sub parser sending arguments values
        """
        self.options.cmd(self.options)

    def exit_with_error(self, message=None):
        """
        Exit command line interaction with error and a message too
        """
        self.parser.exit(1, message)

    def _parser_checks(self, encrypt, args):
        """
        Special checker to verify with all requirements to execute
        """
        if 'cmd' not in self.options:
            self.parser.print_help()
            self.parser.exit()

        if 'encrypt' in args and not self.options.file and not self.options.plantexts:
            encrypt.error('encrypt expected at least one argument')

    @staticmethod
    def _build_cli(commands):
        """
        Build command line interface options for baker commands with help instructions
        """
        description = 'Baker is a decentralized configuration management based on files. <:::>'
        help_commands = "Run 'baker COMMAND --help' for more info on a command"

        parser = argparse.ArgumentParser(prog='baker', description=description)
        parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
        subparsers = parser.add_subparsers(title='commands', metavar='<COMMAND>',
                                           help=help_commands)

        config = subparsers.add_parser('configs', help='list of configs')
        config.add_argument('-a', '--all', action="store_true", help='list default values too')
        config.set_defaults(cmd=commands.config)

        encrypt = subparsers.add_parser('encrypt', help='encrypt values using secret key')
        encrypt.add_argument('plantexts', nargs='*', help='Values to encrypt')
        encrypt.add_argument('--file', help='encrypt values in file secrets section')
        encrypt.set_defaults(cmd=commands.encrypt)

        genkey = subparsers.add_parser('genkey', help='generate a secret key from a key pass')
        genkey.add_argument('keypass', help='key pass to generate a secret key')
        genkey.set_defaults(cmd=commands.generate_key)

        pull = subparsers.add_parser('pull', help='pull a recipe with configurations')
        pull.add_argument('name', help='name [PATH:VERSION] of recipe')
        pull.add_argument('-f', '--force', action="store_true", help='force download of recipe')
        pull.set_defaults(cmd=commands.pull)

        recipes = subparsers.add_parser('recipes', help='list recipes locally')
        recipes.add_argument('-a', '--all', action="store_true",
                             help='list all details of recipes locally ')
        recipes.set_defaults(cmd=commands.recipes)

        rm = subparsers.add_parser('rm', help='remove recipes locally')
        rm.add_argument('recipe_id', help='recipe id to be removed')
        rm.set_defaults(cmd=commands.rm_recipe)

        run = subparsers.add_parser('run', help='run configurations from a recipe')
        run.add_argument('name', nargs='?', help='name [PATH:VERSION] of recipe')
        run.add_argument('--path', help='path of recipe file')
        run.add_argument('-f', '--force', action="store_true", help='force templates replacement')
        run.set_defaults(cmd=commands.run, multiprocess=True)

        for _parser in [parser, config, encrypt, genkey, pull, recipes, rm, run]:
            _parser.add_argument('--verbose', action="store_true", help='increase output verbosity')

        return parser, encrypt
