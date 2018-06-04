from io import StringIO
from unittest import TestCase, mock

from baker.commands import execute_command_line


class TestConfig(TestCase):
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_config_all(self, mock_stdout):
        execute_command_line(['baker', 'configs', '--all'])
        output = mock_stdout.getvalue()
        self.assertTrue('DEBUG=False' in output)

    @mock.patch('baker.settings.path')
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_config(self, mock_stdout, mock_path):
        mock_path.return_value.expanduser = '/home/ll'
        # mock_path.return_value.isfile = False
        # read errors: http://alexmarandon.com/articles/python_mock_gotchas/
        execute_command_line(['baker', 'configs'])
        output = mock_stdout.getvalue()
        self.assertTrue('DEBUG=False' in output)
