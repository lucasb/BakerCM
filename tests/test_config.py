from unittest import TestCase, mock
from subprocess import PIPE, Popen


class TestConfig(TestCase):
    def test_list_config_all(self):
        output = Popen(['baker', 'configs', '-a'], stdout=PIPE).communicate()
        output = output[0].decode('utf-8')
        self.assertTrue('DEBUG=False' in output)

    @mock.patch('baker.settings.Path.is_file')
    @mock.patch('baker.settings.Storage.file')
    def test_list_config(self, mock_path, mock_storage):
        mock_path.return_value = True
        mock_storage.return_value = 'DEBUG=True'

        output = Popen(['baker', 'configs'], stdout=PIPE).communicate()
        output = output[0].decode('utf-8')
        self.assertTrue('DEBUG=True' in output)
