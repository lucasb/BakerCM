from baker import settings


def log(*args):
    if settings.get('DEBUG'):
        print('\t ', args)
    else:
        print('  .')
