import json

from os import makedirs, path
from itertools import chain


class Storage:
    @staticmethod
    def json(location, content=None):
        dir_path = location.rsplit('/', 1)[0]

        if content is not None:
            _create_folders(dir_path)
            with open(location, 'w+') as lines:
                json.dump(content, lines)
        else:
            data = {}
            if path.isfile(location):
                with open(location) as lines:
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
    def secret_key(location, key=None):
        return file(location, content=key)


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
