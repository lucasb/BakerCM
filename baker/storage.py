import json

from os import makedirs, path
from itertools import chain


class Storage:
    """
    Storage control of data in files
    """
    @staticmethod
    def json(location, content=None):
        """
        Read and write json format from file
        """
        dir_path = location.rsplit('/', 1)[0]

        if content is not None:
            Storage.create_folders(dir_path)
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
        """
        Read and write file using parser of ini data
        """
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
    def file(location, content=None, mode=None):
        """
        Read and write raw values from file
        """
        if content:
            directory = path.split(location)[0]
            Storage.create_folders(directory)
            mode = mode or 'w+'
            with open(location, mode) as f:
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

    @staticmethod
    def create_folders(directory):
        """
        Create structure of folders if it not exists
        """
        if not path.exists(directory):
            makedirs(directory, mode=int('0755', 8))
