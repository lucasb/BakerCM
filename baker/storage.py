import json

from os import makedirs, path
from itertools import chain

from baker import settings


class Storage:
    @staticmethod
    def index(recipes=None):
        index_path = settings.get('STORAGE_RECIPE_INDEX')
        index_dir_path = index_path.rsplit('/', 1)[0]

        if recipes:
            _create_folders(index_dir_path)
            with open(index_path, 'w+') as lines:
                json.dump(recipes, lines)
        else:
            data = {}
            if path.isfile(index_path):
                with open(index_path) as lines:
                    data = json.load(lines)
            return data

    @staticmethod
    def parser(location, parser, write_mod=False, chain_items=None):
        try:
            if write_mod:
                with open(location, 'w+') as lines:
                    parser.write(lines)
            else:
                with open(location) as lines:
                    lines = chain(chain_items, lines)
                    parser.read_file(lines)
        except FileNotFoundError:
            raise FileNotFoundError(
                "File not found at: '%s' "
                "Are you sure that it is available on this path?"
                % location
            )

    @staticmethod
    def secret_key(key=None):
        return file(settings.get('STORAGE_KEY_PATH'), content=key)


def file(location, content=None):
    if content:
        directory = path.split(location)[0]
        _create_folders(directory)
        with open(location, 'w+') as f:
            f.write(content)
    else:
        try:
            with open(location) as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                "File not found at: '%s' "
                "Are you sure that it is available on this path?"
                % location
            )


def _create_folders(directory):
    if not path.exists(directory):
        makedirs(directory, mode=int('0755', 8))
