import re

from os import path
from urllib.request import urlretrieve
from urllib.parse import urlsplit

from baker import settings


class Repository:
    repository_patterns = {
        'github': '%(repository)s/%(version)s/%(path)s',
        'bitbucket': '%(repository)s/%(path)s?at=%(version)s',
        'custom': '%(custom)s',
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

    def pull(self):
        url = self._format_url()
        print(url)
        # if file exists local and doesnt has force option it will not downloaded
        # download(url)

    def _check_config(self):
        if not self.repository_url or not self.repository_type:
            raise AttributeError('REPOSITORY and REPOSITORY_TYPE must be set to download recipes')
        if not self.repository_patterns.get(self.repository_type):
            raise AttributeError("REPOSITORY_TYPE '%s' is not supported" % self.repository_type)
        if self.repository_type == 'custom' and not self.repository_custom:
            raise AttributeError(
                "REPOSITORY_CUSTOM_PATTERN must be set when REPOSITORY_TYPE is 'custom'")

    def _format_url(self):
        pattern = self.repository_patterns.get(self.repository_type)
        if self.repository_type == 'custom':
            return pattern % {'custom': self.repository_custom}
        else:
            return pattern % {'repository': self.repository_url, 'path': self.path,
                              'version': self.version}


def download(url):
    if not is_url(url):
        raise TypeError("Str '%s' is not a valid url." % url)

    storage_folder = settings.get('STORAGE_TEMPLATES')
    file_name = path.basename(urlsplit(url).path)
    file_path = storage_folder + file_name
    urlretrieve(url, file_path)
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
