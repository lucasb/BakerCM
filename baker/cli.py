import argparse
import logging

from baker import settings
from baker import commands


def execute_command_line(argv):
    del argv[0]
    parser = _init_parser()
    options = parser.parse_args(argv)

    try:
        if 'cmd' in options:
            _set_log_config(options)
            options.cmd(options)
            logging.info('All done with success!  \o/')
        else:
            parser.print_help()
    except Exception as e:
        logging.error('\n\n ', e)


def log(*args):
    if settings.get('DEBUG'):
        print('\t ', args)
    else:
        print('  .')


def _init_parser():
    description = 'Baker is a configuration management base on static files. <:::>'
    parser = argparse.ArgumentParser(prog='baker', description=description)
    subparsers = parser.add_subparsers(help='sub-command help')

    encrypt = subparsers.add_parser('encrypt', help='encrypt values using secret key')
    encrypt.add_argument('plantexts', nargs='+', help='Values to encrypt')
    encrypt.set_defaults(cmd=commands.encrypt)

    genkey = subparsers.add_parser('genkey', help='generate a secret key from a key pass')
    genkey.add_argument('keypass', nargs='+', help='key pass to generate a secret key')
    genkey.set_defaults(cmd=commands.generate_key)

    run = subparsers.add_parser('run', help='run configurations from a recipe')
    run.add_argument('path', help='path of configuration file')
    run.set_defaults(cmd=commands.run)

    for sub_parser in [parser, encrypt, genkey, run]:
        sub_parser.add_argument('--verbose', action="store_true", help='increase output verbosity')

    return parser


def _set_log_config(options):
    if options.verbose:
        settings.load(DEBUG=True)
    else:
        settings.load()
    logging.basicConfig(level='DEBUG' if settings.get('DEBUG') else 'INFO')
