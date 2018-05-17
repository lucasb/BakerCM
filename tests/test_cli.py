from unittest import TestCase
from subprocess import PIPE, Popen

from baker import __version__


class TestCLI(TestCase):
    def test_show_version(self):
        output = Popen(['baker', '--version'], stdout=PIPE).communicate()[0]
        output = output.decode('utf-8')
        self.assertEqual(output.strip(), 'baker ' + __version__)

    def test_show_help(self):
        output = Popen(['baker', '-h'], stdout=PIPE).communicate()[0]
        output = output.decode('utf-8')
        self.assertTrue('usage:' in output)

    def test_show_help_no_option(self):
        output = Popen(['baker'], stdout=PIPE).communicate()[0]
        output = output.decode('utf-8')
        self.assertTrue('usage:' in output)

    def test_show_help_configs(self):
        output = Popen(['baker', 'configs', '-h'], stdout=PIPE).communicate()
        output1 = output[0].decode('utf-8')
        self.assertTrue('usage: baker configs' in output1)

    def test_show_help_encrypt(self):
        output = Popen(['baker', 'encrypt', '-h'], stdout=PIPE).communicate()
        output1 = output[0].decode('utf-8')
        self.assertTrue('usage: baker encrypt' in output1)

    def test_show_help_encrypt_no_option(self):
        output = Popen(['baker', 'encrypt'], stderr=PIPE).communicate()
        output1 = output[1].decode('utf-8')
        self.assertTrue('encrypt expected at least one argument' in output1)

    def test_show_help_genkey(self):
        output = Popen(['baker', 'genkey', '-h'], stdout=PIPE).communicate()
        output1 = output[0].decode('utf-8')
        self.assertTrue('usage: baker genkey' in output1)

    def test_show_help_pull(self):
        output = Popen(['baker', 'pull', '-h'], stdout=PIPE).communicate()
        output1 = output[0].decode('utf-8')
        self.assertTrue('usage: baker pull' in output1)

    def test_show_help_recipes(self):
        output = Popen(['baker', 'recipes', '-h'], stdout=PIPE).communicate()
        output1 = output[0].decode('utf-8')
        self.assertTrue('usage: baker recipes' in output1)

    def test_show_help_rm(self):
        output = Popen(['baker', 'rm', '-h'], stdout=PIPE).communicate()
        output1 = output[0].decode('utf-8')
        self.assertTrue('usage: baker rm' in output1)

    def test_show_help_run(self):
        output = Popen(['baker', 'run', '-h'], stdout=PIPE).communicate()
        output1 = output[0].decode('utf-8')
        self.assertTrue('usage: baker run' in output1)

    def test_error_invalid_command(self):
        output = Popen(['baker', 'invalid'], stderr=PIPE).communicate()
        output1 = output[1].decode('utf-8')
        self.assertTrue("baker: error: argument <COMMAND>: invalid choice: 'invalid'" in output1)
