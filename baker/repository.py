import re
import hashlib

from os import makedirs, path
from urllib.request import urlretrieve
from urllib.parse import urlsplit
from datetime import datetime

from baker import settings
from baker import logger
from baker.storage import Storage


class Repository:
    ext = 'cfg'  # TODO: Add support recipe via yaml file
    repository_patterns = {
        'github': '%(repository)s/%(version)s/%(path)s.%(ext)s',
        'bitbucket': '%(repository)s/%(path)s.%(ext)s?at=%(version)s',
    }

    def __init__(self, name):
        sep = ':'
        if sep not in name:
            raise AttributeError(
                "Attr 'name' has malformed value. It must have ':' splitting path and version")

        self.local_path = None
        self.repository_url = settings.get('REPOSITORY')
        self.repository_type = settings.get('REPOSITORY_TYPE')
        self.repository_custom = settings.get('REPOSITORY_CUSTOM_PATTERN')
        self.path, self.version = name.split(sep)
        self._check_settings()

    def pull(self, force):
        url = self._format_url()
        filename = url.rsplit('/', 1)[1]
        index = _IndexRecipe(self.path, self.version)
        target = settings.get('STORAGE_RECIPE') + index.id + '/'
        self.local_path = download(url, target, force)
        index.indexing(filename, update=force)

    def _check_settings(self):
        if not self.repository_url or not self.repository_type:
            raise AttributeError('REPOSITORY and REPOSITORY_TYPE '
                                 'must be set to download instructions')

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
        self.index = Storage.index()

    def is_indexed(self):
        return self.id in self.index.keys()

    def indexing(self, filename, update=False):
        if not self.is_indexed() or update:
            self.index[self.id] = {'remote': self.remote, 'version': self.version,
                                   'filename': filename, 'datetime': str(datetime.now())}
            Storage.index(self.index)

    def _generate_id(self):
        str_base = self.remote + self.version
        str_hash = hashlib.sha256(str_base.encode(settings.get('ENCODING')))
        return str_hash.hexdigest()


def download(url, target=None, force=False):
    if not is_url(url):
        raise TypeError("Str '%s' is not a valid url." % url)

    storage_folder = target or settings.get('STORAGE_TEMPLATES')
    file_name = path.basename(urlsplit(url).path)
    file_path = storage_folder + file_name

    if force or not path.isfile(file_path):
        _create_folders(storage_folder)
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


def _create_folders(directory):
    if not path.exists(directory):
        makedirs(directory, mode=int('0755', 8))
