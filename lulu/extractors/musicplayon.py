#!/usr/bin/env python

from lulu.common import (
    match1,
    url_info,
    get_content,
)
from lulu.extractor import VideoExtractor


class MusicPlayOn(VideoExtractor):
    name = 'MusicPlayOn musicplayon.com'

    stream_types = [
        {'id': '720p HD'},
        {'id': '360p SD'},
    ]

    def prepare(self, **kwargs):
        content = get_content(self.url)

        self.title = match1(
            content, r'setup\[\'title\'\] = "([^"]+)";'
        )

        for s in self.stream_types:
            quality = s['id']
            src = match1(
                content,
                r'src: "([^"]+)", "data-res": "{}"'.format(quality)
            )
            if src is not None:
                url = 'https://en.musicplayon.com{}'.format(src)
                self.streams[quality] = {'url': url}

    def extract(self, **kwargs):
        for i in self.streams:
            s = self.streams[i]
            _, s['container'], s['size'] = url_info(s['url'], faker=True)
            s['src'] = [s['url']]


site = MusicPlayOn()
download = site.download_by_url
# TBD: implement download_playlist
