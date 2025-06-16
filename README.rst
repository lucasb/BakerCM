BakerCM
=======
|pypi| |license|

BakerCM is a decentralized configuration management based on files. BakerCM is an out of the box tool to auto-configure an environment using recipe files.

Why Should I Use This?
----------------------
BakerCM is a configuration management that doesn't need a centralized server to configure environments. BakerCM is the lightweight tool built on Python (version 3.6 through 3.13) that configures files from templates.

Secondly, BakerCM can encrypt and decrypt values using secret sections in recipes files. BakerCM cares about the security of values to decrypt it in the right environment, so your configuration files can live openly with your source code and your secrets values will still safe.

Finally, recipe files can be stored and download from the most used versioning control servers like Github, Bitbucket or another server of files where configuration files can be versioned and BakerCM will care to set up your environment using the right version.

Features
--------
* Configure dynamic values in template files per environment
* Encrypt and decrypt values to keep it safe
* Move or copy files in a file system
* Change permission, owner, and group of files
* Manage versions of recipe files from most used versioning control servers
* Customization of BakerCM settings

Installation
------------
BakerCM must be installed on the environment that you want to self-configure. It is easy once you have Python (3.6–3.12) installed.

.. code-block:: console

    $ pip install bakercm

Using Baker
-----------
1. Create a recipe like simple.cfg

.. code-block:: ini

    [appdb:template]
    template = app.conf.tpl
    [appdb:variables]
    HOST = dev.host.db
    PORT = 9000

2. Create a template app.conf.tpl

.. code-block:: ini

    database:
     engine: 'postgres'
     host: '{{ HOST }}'
     port: '{{ PORT }}'

3. Run BakerCM 

.. code-block:: console

    $ baker run --path simple.cfg

4. Done! File configured.

Secrets
-------
Secret section keeps the encrypted values in recipes. It's work like other variables but instead of plaintext values are encrypted and will be decrypted only when a recipe will run to set a template in an environment.

Secret section in a recipe
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: ini

    ...

    [appdb:secrets]
    PASSWORD = cfce1f5e82798a7fca808d8acae50baa\c092ca0bbc873e99d0a2318efa381355\6e9b48

    ...

In a template, secrets are like other variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: ini

    database:
     ...
     password: '{{ PASSWORD }}'

To encrypt and decrypt values is necessary to generate a secret key running ``genkey`` command passing a keypass.  

.. code-block:: console

    $ baker genkey myKeyPass

To encrypt value to save in recipes you can use ``encrypt`` command.

.. code-block:: console

    $ baker encrypt valueToEncrypt
    or to encrypt all values in secret section from a recipe 
    $ baker encrypt --file recipe-to-encrypt.cfg

File System Operations
----------------------
To change file options on file system you can add options on recipes, in template section. Look options supported in template section:

.. code-block:: ini

    [appdb:template]
    template = /path/to/template.conf.tpl       # Template location, it can be a URL too
    path = /path/to/save/replaced/config.conf   # Target location to save replaced file, 
                                                # you also can rename the file
    user = owner                                # Set what user will be the file owner 
    group = group-of-onwer                      # Set group that this file will belong
    mode = 0755                                 # Set permission of file using the number format

All options above works fine for Unix OS like. For Windows, the options ``user``, ``group``, ``mode`` are not supported yet.

Remote Recipes
--------------
Remote recipes are files stored in a versioning server and BakerCM gets them to configure an environment. It's very useful when you want to store your environment configurations and versioning it, and BakerCM will care to manage any environment you want with the right configuration.

Repository settings
^^^^^^^^^^^^^^^^^^^
Repository should be set in settings to Baker know where recipes are stored. For that, change ``~/.bakerc`` file with repository settings.

.. code-block:: ini

    REPOSITORY='https://raw.githubusercontent.com/lucasb/BakerCM/'         # Repository url
    REPOSITORY_TYPE='github'    # Repository pattern like: 'github', 'bitbucket' or 'custom'

    # if authorization is necessary to read files from repository you can
    # add authorization in this setting.
    REPOSITORY_AUTH='Basic YmFrZXI6YmFrZXJjbQ=='

    # if REPOSITORY_TYPE='custom', REPOSITORY_CUSTOM_PATTERN should be set 
    #                using special keys: repository, path, ext and version
    REPOSITORY_CUSTOM_PATTERN='%(repository)s/%(path)s.%(ext)s/%(version)s'

Remote recipes commands
^^^^^^^^^^^^^^^^^^^^^^^
To get a recipe from a repository use command ``pull`` with name argument, ``name`` format is <path>:<version>, where the path is the location in the repository to recipe file and version of the recipe.

.. code-block:: console

    $ baker pull example/dev2:0.4.2
    to force download of recipe use option -f
    $ baker pull -f example/dev:0.4.2

To list all recipes and versions saved in an environment use command ``recipes``.

.. code-block:: console

    $ baker recipes

    RECIPE_ID        REMOTE         VERSION        FILENAME        CREATED 
    af33908tg        example/dev2   0.4.2          dev2.cfg        2018-06-03 06:18

To remove some recipe stored locally use command ``rm`` with ``RECIPE_ID``.

.. code-block:: console

    $ baker rm af33908tg

Also, you can use command ``run`` to pull a recipe and run it using ``name`` argument.

.. code-block:: console

    $ baker run example/dev2:0.4.2

Options
-------
To know more about BakerCM options just run ``--help -h``, for a help with a specific command the same option works.

.. code-block:: console

    $ baker -h

    usage: baker [-h] [-v] [--verbose] <COMMAND> ...

    Baker is a decentralized configuration management based on files. <:::>

    optional arguments:
      -h, --help     show this help message and exit
      -v, --version  show program's version number and exit
      --verbose      increase output verbosity

    commands:
      <COMMAND>      Run 'baker COMMAND --help' for more info on a command
        configs      list of configs
        encrypt      encrypt values using secret key
        genkey       generate a secret key from a key pass
        pull         pull a recipe with configurations
        recipes      list recipes locally
        rm           remove recipes locally
        run          run configurations from a recipe

Settings
--------
You can customize BakerCM options via settings. For that you need to create a ``.bakerc`` on your HOME directory:

.. code-block:: console

    $ vim ~/.bakerc

.. code-block:: ini

    DEBUG=False                            # Verbose mode, the default is false
    ENCODING=utf-8                         # Encode of files and secrets
    RECIPE_CASE_SENSITIVE=False            # The default config keys are case insensitive
    REPOSITORY=None                        # Repository url including protocol http/https
    REPOSITORY_TYPE=None                   # Repository pattern like: 'github', 'bitbucket' or 'custom'
    REPOSITORY_AUTH=None                   # Authorization to read files from repository. Value is set as a header.
                                           # e.g.: 'Basic YmFrZXI6YmFrZXJjbQ=='
    REPOSITORY_CUSTOM_PATTERN=None         # Custom repository url for others pattern. 
                                           # e.g.: '%(repository)s/%(path)s.%(ext)s/%(version)s'
    STORAGE_RECIPE=~/.baker/recipes/       # Remote recipes are storage
    STORAGE_RECIPE_INDEX=~/.baker/index    # Baker index items
    STORAGE_RECIPE_META=~/.baker/meta      # Baker matadata
    STORAGE_KEY_PATH=~/.baker/baker.key    # Store secret key to encrypt and decrypt secret values
    STORAGE_TEMPLATES=~/.baker/templates/  # Remote templates are storage
    TEMPLATE_EXT=tpl                       # Extension for template files. Set 'None' for no extension

To list all settings (customized and defaults) for BakerCM.

.. code-block:: console

    $ baker configs --all

Development
----------
Testing
^^^^^^^
BakerCM uses tox to run tests against multiple Python versions. To run the tests:

.. code-block:: console

    $ pip install tox
    $ tox

This will run the tests against Python 3.7 to 3.13 with coverage reporting.

To run tests against a specific Python version:

.. code-block:: console

    $ tox -e py37  # For Python 3.7
    $ tox -e py311  # For Python 3.11
    $ tox -e py312  # For Python 3.12
    $ tox -e py313  # For Python 3.13
Others
--------
Escape variables
^^^^^^^^^^^^^^^^
How to escape variables in a template:

.. code-block:: ini

    escape-conn: '{{\ connection }}'

Multiple templates for a recipe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Multiple template management is possible in one recipe. For that use different name for each template file that you want to configure. Using the format ``<name>:<section>``.

.. code-block:: ini

    [name1:template]
    ...
    [name1:variable]

    ...
    [name2:template]
    ...
    [name2:secrets]


.. |pypi| image:: https://badge.fury.io/py/bakercm.svg
    :target: https://pypi.org/project/bakercm/
.. |license| image:: https://img.shields.io/badge/license-BSD3-green.svg
