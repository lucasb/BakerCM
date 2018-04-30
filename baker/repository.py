import re
import json
import hashlib

from os import path
from urllib.request import urlretrieve
from urllib.parse import urlsplit

from baker import settings
from baker import logger


class Repository:
    ext = 'cfg'  # TODO: Add support to configure via yaml file
    repository_patterns = {
        'github': '%(repository)s/%(version)s/%(path)s.%(ext)s',
        'bitbucket': '%(repository)s/%(path)s.%(ext)s?at=%(version)s',
    }

    def __init__(self, name):
        sep = ':'
        if sep not in name:
            raise AttributeError(
                "Attr 'name' has malformed value. It must have ':' splitting path and version")

        self.repository_url = settings.get('REPOSITORY')
        self.repository_type = settings.get('REPOSITORY_TYPE')
        self.repository_custom = settings.get('REPOSITORY_CUSTOM_PATTERN')
        self.path, self.version = name.split(sep)
        self._check_config()

    def pull(self, force=False):
        index = _IndexRecipe(self.path, self.version)
        url = self._format_url()
        # FIXME: Add force option
        local_file = download(url, target=settings.get('STORAGE_CONFIG'), force=force)
        index.indexing(local_file)

    def _check_config(self):
        if not self.repository_url or not self.repository_type:
            raise AttributeError('REPOSITORY and REPOSITORY_TYPE must be set to download recipes')

        if self.repository_type == 'custom':
            if not self.repository_custom:
                raise AttributeError(
                    "REPOSITORY_CUSTOM_PATTERN must be set when REPOSITORY_TYPE is 'custom'")
        elif self.repository_type not in self.repository_patterns.keys():
                raise AttributeError("REPOSITORY_TYPE '%s' is not supported" % self.repository_type)

    def _format_url(self):
        pattern = self.repository_custom if self.repository_type == 'custom' \
            else self.repository_patterns.get(self.repository_type)

        return pattern % {'repository': self.repository_url, 'ext': self.ext,
                          'path': self.path, 'version': self.version}


class _IndexRecipe:
    def __init__(self, remote, version):
        self.remote = remote
        self.version = version
        self.id = self._generate_id()
        self.index = self._load_index()

    def is_indexed(self):
        return self.id in self.index.keys()

    def indexing(self, filename):
        if not self.is_indexed():
            self.index[self.id] = {'remote': self.remote, 'version': self.version,
                                   'filename': filename}
            with open(settings.get('STORAGE_CONFIG_INDEX'), 'w+') as file:
                json.dump(self.index, file)

    def _generate_id(self):
        str_base = self.remote + self.version
        str_hash = hashlib.sha256(str_base.encode(settings.get('ENCODING')))
        return str_hash.hexdigest()

    @staticmethod
    def _load_index():
        data = {}
        if path.isfile(settings.get('STORAGE_CONFIG_INDEX')):
            with open(settings.get('STORAGE_CONFIG_INDEX')) as file:
                data = json.load(file)
        return data


def download(url, target=None, force=False):
    if not is_url(url):
        raise TypeError("Str '%s' is not a valid url." % url)

    storage_folder = target or settings.get('STORAGE_TEMPLATES')
    file_name = path.basename(urlsplit(url).path)
    file_path = storage_folder + file_name
    # FIXME: create folder with id in config, maybe for templates too.
    if force or not path.isfile(file_path):
        urlretrieve(url, file_path)
        logger.log(url, 'download DONE!')
    else:
        logger.log(url, 'from CACHE!')

    return file_path


def is_url(url):
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain..
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url)
