from unittest import TestCase
from subprocess import PIPE, Popen

from baker import __version__


class TestCLI(TestCase):
    def test_show_help(self):
        output = Popen(['baker', '-h'], stdout=PIPE).communicate()[0]
        output = output.decode("utf-8")
        self.assertTrue('usage:' in output)

    def test_show_version(self):
        output = Popen(['baker', '--version'], stdout=PIPE).communicate()[0]
        output = output.decode("utf-8")
        self.assertEqual(output.strip(), 'baker ' + __version__)
