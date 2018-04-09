import traceback

from baker import cli
from baker import logger
from baker import settings
from baker.configuration import ReadConfig
from baker.secret import SecretKey, Encryption
from baker.template import ReplaceTemplate


def encrypt(args):
    secret_key = str(SecretKey().key)
    enc = Encryption(secret_key)

    for text in args.plantexts:
        logger.log(text, enc.encrypt(text))


def generate_key(args):
    SecretKey.generate(args.keypass)


def run(args):
    config = ReadConfig(args.path)
    template = ReplaceTemplate(config.configs)
    template.replace()


def execute_command_line(argv):
    del argv[0]
    parser = cli.parser()
    options = parser.parse_args(argv)

    try:
        if 'cmd' in options:
            settings.load(DEBUG=options.verbose)
            logger.init()

            logger.log('Baker start <:::> \n')

            options.cmd(options)
            logger.log('\n All done with success!  \o/')
        else:
            parser.print_help()
    except Exception as e:
        logger.debug(str(traceback.format_exc()))
        logger.log(str(e))
        logger.log('ERROR: An error was caught. Add --verbose option for more information.')
