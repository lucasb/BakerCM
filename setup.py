from sys import platform
from setuptools import Command, find_packages, setup
from subprocess import call

from baker import __version__


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def run():
        """Run all tests!"""
        err = call(['py.test', '--cov=baker', '--cov-report=term-missing'],
                   shell=(platform == 'win32'))
        raise SystemExit(err)


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='bakercm',
      version=__version__,
      description='Baker is a decentralized configuration management based on files',
      long_description=readme(),
      classifiers=[
          'Intended Audience :: Developers',
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3.6',
          'Topic :: System :: Software Distribution',
          'Topic :: Utilities',
      ],
      keywords='baker configuration management',
      url='https://github.com/lucasb/BakerCM',
      author='Lucas Boscaini',
      author_email='lucasboscaini@gmail.com',
      license='BSD3',
      packages=find_packages(exclude=['docs', 'example', 'tests', '.github', '.git']),
      test_suite='py.test',
      install_requires=[
          'pycryptodome==3.4.11',
      ],
      tests_require=[
          'coverage',
          'pytest',
          'pytest-cov',
      ],
      cmdclass={
          'test': RunTests
      },
      entry_points={
          'console_scripts': ['baker=baker:main'],
      },
      include_package_data=True,
      zip_safe=False)
