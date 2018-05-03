import argparse


class Parser:
    def __init__(self, args, commands):
        self.parser, encrypt = self._build_cli(commands)
        self.options = self.parser.parse_args(args)
        self._parser_checks(encrypt, args)

    def execute(self):
        self.options.cmd(self.options)

    def exit_with_error(self, message=None):
        self.parser.exit(1, message)

    def _parser_checks(self, encrypt, args):
        if 'cmd' not in self.options:
            self.parser.print_help()
            self.parser.exit()

        if 'encrypt' in args and not self.options.file and not self.options.plantexts:
            encrypt.error('encrypt expected at least one argument')

    @staticmethod
    def _build_cli(commands):
        description = 'Baker is a decentralized configuration management based on files. <:::>'
        help_commands = "Run 'baker COMMAND --help' for more info on a command"

        parser = argparse.ArgumentParser(prog='baker', description=description)
        parser.add_argument('-v', '--version', action='version', version='%(prog)s v0.2.0')
        subparsers = parser.add_subparsers(title='commands', metavar='<COMMAND>',
                                           help=help_commands)

        config = subparsers.add_parser('config', help='list of configs')
        config.add_argument('-a', '--all', action="store_true", help='list default values too')
        config.set_defaults(cmd=commands.config)

        encrypt = subparsers.add_parser('encrypt', help='encrypt values using secret key')
        encrypt.add_argument('plantexts', nargs='*', help='Values to encrypt')
        encrypt.add_argument('--file', help='encrypt values in file secrets section')
        encrypt.set_defaults(cmd=commands.encrypt)

        genkey = subparsers.add_parser('genkey', help='generate a secret key from a key pass')
        genkey.add_argument('keypass', help='key pass to generate a secret key')
        genkey.set_defaults(cmd=commands.generate_key)

        list_recipes = subparsers.add_parser('list', help='list recipes locally')
        list_recipes.add_argument('-a', '--all', action="store_true",
                                  help='list all details of recipes locally ')
        list_recipes.set_defaults(cmd=commands.list)

        rm_recipe = subparsers.add_parser('rm', help='remove recipes locally')
        rm_recipe.add_argument('recipe_id', help='recipe id to be removed')
        rm_recipe.set_defaults(cmd=commands.rm_recipe)

        pull = subparsers.add_parser('pull', help='pull a recipe with configurations')
        pull.add_argument('name', help='name [PATH:VERSION] of recipe')
        pull.add_argument('-f', '--force', action="store_true", help='force download of recipe')
        pull.set_defaults(cmd=commands.pull)

        run = subparsers.add_parser('run', help='run configurations from a recipe')
        run.add_argument('name', nargs='?', help='name [PATH:VERSION] of recipe')
        run.add_argument('--path', help='path of recipe file')
        run.add_argument('-f', '--force', action="store_true", help='force templates replacement')
        run.set_defaults(cmd=commands.run)

        for _parser in [parser, config, encrypt, genkey, list_recipes, pull, rm_recipe, run]:
            _parser.add_argument('--verbose', action="store_true", help='increase output verbosity')

        return parser, encrypt
