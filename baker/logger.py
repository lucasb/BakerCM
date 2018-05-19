import sys
import logging

from baker import settings


def init():
    """
    Initialize logger for all application
    """
    global LOGGER
    LOGGER = logging.getLogger()
    level = 'DEBUG' if settings.get('DEBUG') else 'INFO'

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(message)s'))
    LOGGER.addHandler(handler)
    LOGGER.setLevel(level)


def log(*args):
    """
    Logging usual message on cli
    """
    globals()['LOGGER'].info(' '.join(args))


def debug(*args):
    """
    Logging debug information on cli
    """
    globals()['LOGGER'].debug('DEBUG: ' + (' '.join(args)))
