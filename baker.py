#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

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

    # FIXME: Move it for a specific file for commands
    parser = argparse.ArgumentParser(prog='baker',
                                     description='Baker  <:::> .')

    parser.add_argument('command', type=str, nargs='?', default=None,
                        help='Commands: genkey or configure',)

    parser.add_argument('option', type=str, nargs='?', default=None,
                        help='Options for a command', )

    args = parser.parse_args()

    print(' Baker  <:::> ')

    if args.command == 'genkey':
        print(' Generating secret key .............')
        if not args.option:
            print('Error: Key pass is required to generate a secret key.')
            exit(1)
        SecretKey.generate(args.option)  # 'my secret key ninja_+='
        print(' Secret key created')
    elif args.command == 'configure':
        if not args.option:
            print('Error: Config file is required to configure the system.')
            exit(1)
        config = ReadConfig(args.option)
        parser = ReplaceTemplate(config.configs)
        parser.replace()
        print(' Finished configuration')
    else:
        print('Error: Command not found, try -h.')
        exit(1)

    print('\n All done with success!  \o/')
