#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    try:
        from baker.secret import SecretKey
        from baker.parser import ReadConfig, ReplaceTemplate
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Baker is missing to avoid masking other exceptions.
        try:
            import baker
        except ImportError:
            raise ImportError(
                "Couldn't import Baker. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    print(' Baker <:::>')
    print('\t Starting')
    print('\t Processing .............')
    # SecretKey.generate('my secret key ninja_+=')
    config = ReadConfig('./example/dev2.cfg')
    parser = ReplaceTemplate(config.configs)
    parser.replace()
    # replace()

    print('\n\t Baker Finished: All done with success!  \o/')
