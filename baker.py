#!/usr/bin/env python

if __name__ == '__main__':
    try:
        from baker.secret import SecretKey
        from baker.parser import replace
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

    print('Starting Baker')

    SecretKey.generate('my secret key ninja_+=')
    replace()

    print('\n SUCCESS: All done with success!  \o/')
