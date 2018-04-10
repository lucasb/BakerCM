import logging

from baker import settings


def init():
    global LOGGER
    LOGGER = logging.getLogger()
    level = 'INFO'

    if settings.get('DEBUG'):
        level = 'DEBUG'

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    LOGGER.addHandler(handler)
    LOGGER.setLevel(level)


def log(*args):
    globals()['LOGGER'].info(' '.join(args))


def debug(*args):
    globals()['LOGGER'].debug('DEBUG: ' + (' '.join(args)))
