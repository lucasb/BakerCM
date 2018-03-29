import argparse

from baker.secret import SecretKey, Encryption
from baker.configuration import ReadConfig
from baker.template import ReplaceTemplate
from baker.settings import DEBUG, STORAGE_KEY_PATH


parser = argparse.ArgumentParser(prog='baker.py', description='Baker  <:::> .')

parser.add_argument('command', type=str, help='Commands: genkey, encrypt or configure', )
parser.add_argument('option', type=str, help='Options for a command', )
parser.add_argument('--verbose', action="store_true", help='increase output verbosity', )

args = parser.parse_args()

print(' Baker  <:::> \n')

if args.verbose:
    DEBUG = True

if args.command == 'genkey':
    print(' Generating secret key .............')
    if not args.option:
        print('Error: Key pass is required to generate a secret key.')
        exit(1)
    secret_key = SecretKey.generate(args.option)  # 'my secret key ninja_+='
    if DEBUG:
        print(" Secret key '%s' created at %s" % (secret_key, STORAGE_KEY_PATH))
    else:
        print(' Secret key created')
elif args.command == 'encrypt':
    print(' Encrypting secret key .............')
    if not args.option:
        print('Error: Value to encrypt required to configure the system.')
        exit(1)
    secret_key = str(SecretKey().key)
    enc = Encryption(secret_key)
    print(enc.encrypt(args.option))
elif args.command == 'configure':
    print(' Configure templates ')
    if not args.option:
        print('Error: Config file is required to configure the system.')
        exit(1)
    config = ReadConfig(args.option)
    template = ReplaceTemplate(config.configs)
    template.replace()
else:
    print("Error: Command '%s' not found." % args.command)
    exit(1)

print('\n\n All done with success!  \o/')


def execute_command_line(argv):
    del argv[0]
    parser.parse_args(argv)
