from unittest import TestCase
from subprocess import PIPE, Popen

from baker import __version__


class TestCLI(TestCase):
    def test_show_help(self):
        output = Popen(['baker', '-h'], stdout=PIPE).communicate()[0]
        output = output.decode("utf-8")
        self.assertTrue('usage:' in output)

    def test_show_help_no_option(self):
        output = Popen(['baker'], stdout=PIPE).communicate()[0]
        output = output.decode("utf-8")
        self.assertTrue('usage:' in output)

    def test_show_version(self):
        output = Popen(['baker', '--version'], stdout=PIPE).communicate()[0]
        output = output.decode("utf-8")
        self.assertEqual(output.strip(), 'baker ' + __version__)

    def test_show_recipes(self):
        output = Popen(['python', 'baker', 'configs', '-h'], stdout=PIPE).communicate()
        output1 = output[0].decode("utf-8")
        print(output1)
        #self.assertTrue('RECIPE ID' in output)

