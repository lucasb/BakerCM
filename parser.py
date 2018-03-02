import re

from string import Template
from ConfigParser import ConfigParser
from secret import secret


# read configs
config = ConfigParser()
config.optionxform = str
config.read('values.cfg')


# Find and decrypt secret values
def decrypt_secrets(items):
    def call(value):
        secret_val = re.search('secret\((.+?)\)', value)
        if secret_val:
            return secret.decrypt(secret_val.group(1))
        return value
    return dict(map(lambda i: (i[0], call(i[1])), items))


# replace files
for file_location in config.sections():
    values = dict(config.items(file_location))
    values = decrypt_secrets(values.iteritems())
    template = open(file_location).read()
    replacement = Template(template).substitute(values)
    open(file_location[:-4], 'w').write(replacement)
