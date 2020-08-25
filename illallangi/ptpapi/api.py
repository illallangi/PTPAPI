from click import get_app_dir

from diskcache import Cache

from loguru import logger

from requests import get as http_get

from yarl import URL

from .torrent import Torrent

ENDPOINTDEF = 'https://passthepopcorn.me/'
EXPIRE = 7 * 24 * 60 * 60


class API(object):
    def __init__(self, api_user, api_key, endpoint=ENDPOINTDEF, cache=True, config_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_user = api_user
        self.api_key = api_key
        self.endpoint = URL(endpoint) if not isinstance(endpoint, URL) else endpoint
        self.cache = cache
        self.config_path = get_app_dir(__package__) if not config_path else config_path

    def get_torrent(self, hash):
        hash = hash.upper()
        with Cache(self.config_path) as cache:
            if not self.cache or hash not in cache:
                sleep_time = 5
                while True:
                    r = http_get(self.endpoint / 'torrents.php',
                                 params={
                                     'json': 'noredirect',
                                     'infohash': hash,
                                 },
                                 headers={
                                     'ApiUser': self.api_user,
                                     'ApiKey': self.api_key,
                                     'user-agent': 'illallangi-btnapi/0.0.1',
                                 })
                    logger.debug('Received {0} bytes from API'.format(len(r.content)))
                    logger.trace(r.json())
                    if 'Torrents' not in r.json() or len([x for x in r.json()['Torrents'] if x['InfoHash'] == hash]) != 1:
                        logger.error('No response received for hash {hash}')
                        return None
                    cache.set(
                        hash,
                        {
                            **{
                                key: r.json()[key]
                                for key in r.json()
                                if key not in ['Torrents']
                            },
                            **[x for x in r.json()['Torrents'] if x['InfoHash'] == hash][0]
                        },
                        expire=EXPIRE)
                    break

            return Torrent(cache[hash])
