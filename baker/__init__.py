import sys

__version__ = '0.4.5'


def main():
    try:
        from baker.commands import execute_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Baker is missing to avoid masking other exceptions.
        try:
            import baker   # noqa: F401
        except ImportError:
            raise ImportError(
                "Couldn't import Baker. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_command_line(sys.argv)
