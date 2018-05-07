from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='bakercm',
      version='0.3',
      description='Baker is a decentralized configuration management based on files',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
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
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['baker=baker:main'],
      },
      include_package_data=True,
      zip_safe=False)
