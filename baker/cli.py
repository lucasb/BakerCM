import argparse

from baker import commands


def parser():
    description = 'Baker is a configuration management base on static files. <:::>'
    main_parser = argparse.ArgumentParser(prog='baker', description=description)
    subparsers = main_parser.add_subparsers(help='sub-command help')

    encrypt = subparsers.add_parser('encrypt', help='encrypt values using secret key')
    encrypt.add_argument('plantexts', nargs='+', help='Values to encrypt')
    encrypt.set_defaults(cmd=commands.encrypt)

    genkey = subparsers.add_parser('genkey', help='generate a secret key from a key pass')
    genkey.add_argument('keypass', help='key pass to generate a secret key')
    genkey.set_defaults(cmd=commands.generate_key)

    run = subparsers.add_parser('run', help='run configurations from a recipe')
    run.add_argument('path', help='path of configuration file')
    run.set_defaults(cmd=commands.run)

    for sub_parser in [main_parser, encrypt, genkey, run]:
        sub_parser.add_argument('--verbose', action="store_true", help='increase output verbosity')

    return main_parser
