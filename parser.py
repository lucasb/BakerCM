from ConfigParser import ConfigParser
from secret import secret


config = ConfigParser()
config.read('values.cfg')

print secret.decrypt(config.defaults().get('secret_key'))

print config.get('TEST', 'TEST_TIMEOUT')
