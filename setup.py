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
      long_description_content_type='text/markdown',
      classifiers=[
          'Intended Audience :: Developers',
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: BSD',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
          'Programming Language :: Python :: Implementation :: CPython',
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
          'pycryptodome>=3.6.6,<4.0.0',
      ],
      tests_require=[
          'coverage',
          'pytest',
          'pytest-cov',
          'tox',
      ],
      cmdclass={
          'test': RunTests
      },
      entry_points={
          'console_scripts': ['baker=baker:main'],
      },
      include_package_data=True,
      zip_safe=False)
