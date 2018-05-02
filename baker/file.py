import json
from os import makedirs, path

from baker import settings


def secret_key(key=None):
    if key:
        key_file_path = settings.get('STORAGE_KEY_PATH')
        key_path = path.split(key_file_path)[0]
        _create_folders(key_path)
        open(key_file_path, 'w').write(key)
    else:
        try:
            return open(settings.get('STORAGE_KEY_PATH')).read()
        except FileNotFoundError:
            raise FileNotFoundError(
                "Secret key not found at: '%s'. "
                "Are you sure it was generated and available on this path?"
                % settings.get('STORAGE_KEY_PATH')
            )


def index(content=None):
    recipe_path = settings.get('STORAGE_RECIPE_INDEX')

    if content:
        _create_folders(recipe_path)
        with open(recipe_path, 'w+') as file:
            json.dump(content, file)
    else:
        data = {}
        if path.isfile(recipe_path):
            with open(recipe_path) as file:
                data = json.load(file)
        return data


def _create_folders(directory):
    if not path.exists(directory):
        makedirs(directory, mode=int('0755', 8))
