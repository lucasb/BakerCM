from unittest import TestCase
from subprocess import PIPE, Popen


class TestConfig(TestCase):
    def test_list_config_all(self):
        output = Popen(['baker', 'configs', '-a'], stdout=PIPE).communicate()
        output = output[0].decode('utf-8')
        self.assertTrue('DEBUG=False' in output)
