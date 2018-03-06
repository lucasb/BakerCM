import re

from string import Template
from configparser import ConfigParser, ExtendedInterpolation

from baker.secret import Encryption, SecretKey
from baker.settings import HOME_DIR


def replace():
    # read configs
    config = ConfigParser()
    config.optionxform = str
    config._interpolation = ExtendedInterpolation()
    # config.add_section('DEFAULT')
    # config.default_section['HOME_DIR'] = HOME_DIR
    config.set('DEFAULT', 'HOME_DIR', HOME_DIR)
    config.read('values.cfg')
    print(config.values())
    # instance encryption
    encryption = Encryption(SecretKey().key)

    # find and decrypt secret values
    def decrypt_secrets(items):
        def call(value):
            secret_val = re.search('_secret\((.+?)\)', value)
            if secret_val:
                return encryption.decrypt(secret_val.group(1))
            return value
        return dict(map(lambda i: (i[0], call(i[1])), items))

    # replace files
    for file_location in config.sections():
        values = dict(config.items(file_location))
        values = decrypt_secrets(values.items())
        template = open(file_location).read()
        replacement = Template(template).substitute(values)
        open(file_location[:-4], 'w').write(replacement)
