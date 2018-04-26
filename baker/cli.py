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
        parser = argparse.ArgumentParser(prog='baker', description=description)
        parser.add_argument('-v', '--version', action='version', version='%(prog)s v0.2.0')
        subparsers = parser.add_subparsers(title='commands', metavar='<COMMAND>',
                                           help="Run 'baker.py COMMAND --help' for more info on a command")

        encrypt = subparsers.add_parser('encrypt', help='encrypt values using secret key')
        encrypt.add_argument('plantexts', nargs='*', help='Values to encrypt')
        encrypt.add_argument('--file', help='encrypt values in file secrets section')
        encrypt.set_defaults(cmd=commands.encrypt)

        genkey = subparsers.add_parser('genkey', help='generate a secret key from a key pass')
        genkey.add_argument('keypass', help='key pass to generate a secret key')
        genkey.set_defaults(cmd=commands.generate_key)

        pull = subparsers.add_parser('pull', help='pull a recipe with configurations')
        pull.add_argument('name', help='name [PATH:VERSION] of recipe')
        pull.set_defaults(cmd=commands.pull)

        run = subparsers.add_parser('run', help='run configurations from a recipe')
        run.add_argument('path', help='path of configuration file')
        run.set_defaults(cmd=commands.run)

        for _parser in [parser, encrypt, genkey, pull, run]:
            _parser.add_argument('--verbose', action="store_true", help='increase output verbosity')

        return parser, encrypt
