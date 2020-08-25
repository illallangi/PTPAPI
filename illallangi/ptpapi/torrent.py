from functools import cached_property

from bytesize import Size

from loguru import logger

from yarl import URL


class Torrent(object):
    def __init__(self, dictionary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dictionary = dictionary

        for key in self._dictionary.keys():
            if key not in self._keys:
                raise Exception(f'Unhandled key in {self.__class__}: {key}')
            logger.trace('{}: {}"{}"', key, type(self._dictionary[key]), self._dictionary[key])

    @property
    def _keys(self):
        return [
            'AuthKey',
            'Checked',
            'Codec',
            'Container',
            'CoverImage',
            'GoldenPopcorn',
            'GroupId',
            'Id',
            'ImdbId',
            'ImdbRating',
            'ImdbVoteCount',
            'InfoHash',
            'Leechers',
            'Name',
            'Page',
            'PassKey',
            'Quality',
            'ReleaseGroup',
            'ReleaseName',
            'Resolution',
            'Result',
            'Scene',
            'Seeders',
            'Size',
            'Snatched',
            'Source',
            'TorrentId',
            'UploadTime',
            'Year',
        ]

    def __repr__(self):
        return f'{self.__class__}{self.infohash} - {self.releasename})'

    def __str__(self):
        return f'{self.infohash} - {self.releasename} ({str(self.size).strip("@")} {self.coverimage})'

    @cached_property
    def infohash(self):
        return self._dictionary['InfoHash']

    @cached_property
    def releasename(self):
        return self._dictionary['ReleaseName']

    @cached_property
    def coverimage(self):
        return URL(self._dictionary['CoverImage']).with_scheme('https')

    @cached_property
    def size(self):
        return Size(int(self._dictionary['Size']))
