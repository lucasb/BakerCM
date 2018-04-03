from baker.configuration import ReadConfig
from baker.secret import SecretKey, Encryption
from baker.template import ReplaceTemplate


def encrypt(args):
    secret_key = str(SecretKey().key)
    enc = Encryption(secret_key)
    return enc.encrypt(args.plantexts)


def generate_key(args):
    return SecretKey.generate(args.keypass)


def run(args):
    config = ReadConfig(args.path)
    template = ReplaceTemplate(config.configs)
    template.replace()
