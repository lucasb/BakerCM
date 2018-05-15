from setuptools import setup

from baker import __version__


setup(name='bakercm',
      version=__version__,
      description='Baker is a decentralized configuration management based on files',
      long_description='Baker is a decentralized configuration management based on files',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Software Distribution',
      ],
      keywords='baker configuration management',
      url='https://github.com/lucasb/BakerCM',
      author='Lucas Boscaini',
      author_email='lucasboscaini@gmail.com',
      license='BSD3',
      packages=['baker'],
      install_requires=[
          'pycryptodome==3.4.11',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3', 'coverage', 'flake8'],
      entry_points={
          'console_scripts': ['baker=baker:main'],
      },
      include_package_data=True,
      zip_safe=False)
