BakerCM
=======
|gitter| |travisci| |codecov| |codeclimate| |license|

BakerCM is a decentralized configuration management based on files. BakerCM is an out of the box tool to auto-configure an environment using recipe files.

Why Should I Use This?
-------
BakerCM is a configuration management that doesn't need a centralized server to configure environments. BakerCM is the lightweight tool built on Python (version 3) that configures files from templates.

Secondly, BakerCM can encrypt and decrypt values using secret sections in recipes files. BakerCM cares about the security of values to decrypt it in the right environment, so your configuration files can live openly with your source code and your secrets values will still safe.

Finally, recipe files can be stored and download from the most used versioning control servers like Github, Bitbucket or another server of files where configuration files can be versioned and BakerCM will care to set up your environment using the right version.

Features
-------
* Configure dynamic values in template files per environment
* Encrypt and decrypt values to keep it safe
* Move or copy files in a file system
* Change permission, owner, and group of files
* Manage versions of recipe files from most used versioning control servers
* Customization of BakerCM settings

Installation
-------
BakerCM must be installed on environment that you want to self configured and it easy once you have python installed.

.. code-block:: console

    $ pip install bakercm

Using Baker
-------
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

.. |gitter| image:: https://img.shields.io/gitter/room/TechnologyAdvice/Stardust.svg?style=flat
   :target: https://gitter.im/bakerchat/Lobby
.. |travisci| image:: https://travis-ci.org/lucasb/BakerCM.svg?branch=master
    :target: https://travis-ci.org/lucasb/BakerCM   
.. |codecov| image:: https://codecov.io/gh/lucasb/BakerCM/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/lucasb/BakerCM
.. |codeclimate| image:: https://codeclimate.com/github/lucasb/BakerCM/badges/gpa.svg
    :target: https://codeclimate.com/github/lucasb/BakerCM
.. |license| image:: https://img.shields.io/badge/license-BSD3-green.svg
