#!/usr/bin/env python

import re
import json

from lulu.common import (
    match1,
    url_info,
    urls_size,
    get_content,
)
from lulu.extractor import VideoExtractor


class Imgur(VideoExtractor):
    name = 'Imgur'

    stream_types = [
        {'id': 'original'},
        {'id': 'thumbnail'},
    ]

    def prepare(self, **kwargs):
        if re.search(r'imgur\.com/a/', self.url):
            # album
            content = get_content(self.url)
            album = match1(content, r'album\s*:\s*({.*}),') or \
                match1(content, r'image\s*:\s*({.*}),')
            album = json.loads(album)
            # count = album['album_images']['count']
            images = album['album_images']['images']
            ext = images[0]['ext']
            self.streams = {
                'original': {
                    'src': [
                        'http://i.imgur.com/{}{}'.format(
                            i['hash'], ext
                        ) for i in images
                    ],
                    'size': sum([i['size'] for i in images]),
                    'container': ext[1:]
                },
                'thumbnail': {
                    'src': [
                        'http://i.imgur.com/{}s{}'.format(
                            i['hash'], '.jpg'
                        ) for i in images
                    ],
                    'container': 'jpg'
                }
            }
            self.title = album['title']

        elif re.search(r'i\.imgur\.com/', self.url):
            # direct image
            _, container, size = url_info(self.url)
            self.streams = {
                'original': {
                    'src': [self.url],
                    'size': size,
                    'container': container
                }
            }
            self.title = match1(self.url, r'i\.imgur\.com/([^./]*)')

        else:
            # gallery image
            content = get_content(self.url)
            image = json.loads(match1(content, r'image\s*:\s*({.*}),'))
            ext = image['ext']
            self.streams = {
                'original': {
                    'src': [
                        'http://i.imgur.com/{}{}'.format(image['hash'], ext)
                    ],
                    'size': image['size'],
                    'container': ext[1:]
                },
                'thumbnail': {
                    'src': [
                        'http://i.imgur.com/{}s{}'.format(
                            image['hash'], '.jpg'
                        )
                    ],
                    'container': 'jpg'
                }
            }
            self.title = image['title'] or image['hash']

    def extract(self, **kwargs):
        if 'stream_id' in kwargs and kwargs['stream_id']:
            i = kwargs['stream_id']
            if 'size' not in self.streams[i]:
                self.streams[i]['size'] = urls_size(self.streams[i]['src'])


site = Imgur()
download = site.download_by_url
download_playlist = site.download_by_url
