import re

from os import path, makedirs
from urllib.request import urlretrieve
from urllib.parse import urlsplit

from baker import settings


url_pattern = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain..
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def is_url(url):
    return url_pattern.match(url)


def download(url):
    storage_folder = settings.get('STORAGE_FILES')
    file_name = path.basename(urlsplit(url).path)
    file_path = storage_folder + file_name

    if not is_url(url):
        raise TypeError("Str '%s' is not a valid url." % url)

    if not path.isdir(storage_folder):
        makedirs(storage_folder, mode=int('0755', 8))

    urlretrieve(url, file_path)
    return file_path
