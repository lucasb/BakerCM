import logging

from baker import settings


def init():
    global LOGGER
    LOGGER = logging.getLogger()

    level = 'INFO'
    fmt_str = '%(message)s'

    if settings.get('DEBUG'):
        level = 'DEBUG'
        fmt_str = '%(levelname)s - ' + fmt_str

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt_str))

    LOGGER.addHandler(handler)
    LOGGER.setLevel(level)


def log(*args):
    globals()['LOGGER'].info(' '.join(args))


def debug(*args):
    globals()['LOGGER'].debug(' '.join(args))
