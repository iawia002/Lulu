#!/usr/bin/env python

import re
from urllib import parse

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
)


__all__ = ['heavymusic_download']
site_info = 'Heavy Music Archive heavy-music.ru'


def heavymusic_download(url, info_only=False, **kwargs):
    html = get_content(url)
    tracks = re.findall(r'href="(online2\.php[^"]+)"', html)
    for track in tracks:
        band = match1(track, r'band=([^&]*)')
        album = match1(track, r'album=([^&]*)')
        title = match1(track, r'track=([^&]*)')
        file_url = (
            'http://www.heavy-music.ru/online2.php?band={}&album={}&'
            'track={}'.format(
                parse.quote(band), parse.quote(album), parse.quote(title)
            )
        )
        _, _, size = url_info(file_url)

        print_info(site_info, title, 'mp3', size)
        if not info_only:
            download_urls([file_url], title[:-4], 'mp3', size, **kwargs)


download = heavymusic_download
download_playlist = heavymusic_download
