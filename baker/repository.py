import re
import hashlib

from os import path
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
from urllib.parse import urlsplit
from datetime import datetime

from baker import settings
from baker import logger
from baker.storage import Storage


class Repository:
    """
    Repository management of recipes
    """
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
        """
        Pull recipe by path and version
        """
        url = self._format_url()
        filename = url.rsplit('/', 1)[1]
        index = _IndexRecipe(self.path, self.version, filename)
        target = settings.get('STORAGE_RECIPE') + index.id + '/'
        self.local_path = download(url, target, force)
        index.indexing(update=force)

    @staticmethod
    def remove(rid):
        """
        Remove locally recipe by id
        """
        location = settings.get('STORAGE_RECIPE_INDEX')
        index = Storage.json(location)

        if len(rid) != 64:
            found = list(filter(lambda idx: idx[:9] == rid, index))
            if found:
                rid = found[0]

        del index[rid]
        Storage.json(location, index)
        logger.log("Removed recipe '%s'" % rid)

    def _check_settings(self):
        """
        Verify if required settings is right to repository works
        """
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


class ListRecipes:
    """
    List recipes in local storage
    """
    @staticmethod
    def list(all_info=False):
        """
        List of recipes saved in index
        """
        recipes = Storage.json(settings.get('STORAGE_RECIPE_INDEX'))
        meta = _IndexRecipe.calc_length(recipes)
        meta['id'] = 64 if all_info else 9
        extra_space = 8
        list_items = ''

        for key in recipes.keys():
            recipe = recipes[key]
            recipe_id = key[:meta['id']]
            created = recipe['datetime'] if all_info else recipe['datetime'][:19]

            list_items += recipe_id + (' ' * (meta['id'] + extra_space - len(recipe_id)))

            for attr_name in ['remote', 'version', 'filename']:
                list_items += (recipe[attr_name] +
                               (' ' * (meta[attr_name] + extra_space - len(recipe[attr_name]))))

            list_items += created + '\n'

        header = ListRecipes._list_header(meta, extra_space)
        logger.log(header + list_items)

    @staticmethod
    def _list_header(meta, extra_space=0):
        """
        Build header of recipes list
        """
        return ('RECIPE ID' + (' ' * (meta['id'] + extra_space - 9)) +
                'REMOTE' + (' ' * (meta['remote'] + extra_space - 6)) +
                'VERSION' + (' ' * (meta['version'] + extra_space - 7)) +
                'FILENAME' + (' ' * (meta['filename'] + extra_space - 8)) +
                'CREATED \n')


def download(url, target=None, force=False):
    """
    Download and storage file from a url
    """
    if not is_url(url):
        raise TypeError("Str '%s' is not a valid url." % url)

    storage_folder = target or settings.get('STORAGE_TEMPLATES')
    auth = str(settings.get('REPOSITORY_AUTH')).replace("'", '')
    file_name = path.basename(urlsplit(url).path)
    file_path = storage_folder + file_name

    if force or not path.isfile(file_path):
        Storage.create_folders(storage_folder)
        try:
            request = Request(url)
            if auth:
                request.add_header('Authorization', auth)
            with urlopen(request) as response:
                Storage.file(file_path, response.read(), 'wb')
            logger.log(url, 'download DONE!')
        except HTTPError as e:
            e.msg += ": URL '%s' cannot be downloaded" % url
            raise e
    else:
        logger.log(url, 'from CACHE!')

    return file_path


def is_url(url):
    """
    Verify if string is following url pattern
    """
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain..
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url)


class _IndexRecipe:
    """
    Index recipes management
    """
    def __init__(self, remote, version, filename):
        self.remote = remote
        self.version = version
        self.filename = filename
        self.id = self._generate_id()
        self.index = Storage.json(settings.get('STORAGE_RECIPE_INDEX'))

    def is_indexed(self):
        """
        Check if recipe is indexed locally
        """
        return self.id in self.index.keys()

    def indexing(self, update=False):
        """
        Indexing recipes locally
        """
        if not self.is_indexed() or update:
            self.index[self.id] = {'remote': self.remote, 'version': self.version,
                                   'filename': self.filename, 'datetime': str(datetime.now())}
            Storage.json(settings.get('STORAGE_RECIPE_INDEX'), self.index)

    @staticmethod
    def calc_length(recipes):
        """
        Calculate size of values in index file
        """
        lengths = {'remote': 6, 'version': 7, 'filename': 8}

        for recipe_id in recipes:
            for attr_name in ['remote', 'version', 'filename']:
                recipe = recipes[recipe_id]
                attr_size = len(recipe[attr_name])
                if attr_size > lengths[attr_name]:
                    lengths[attr_name] = attr_size

        return lengths

    def _generate_id(self):
        """
        Generate a hash as id to a recipe based on path and version
        """
        str_base = self.remote + self.version
        str_hash = hashlib.sha256(str_base.encode(settings.get('ENCODING')))
        return str_hash.hexdigest()
