#!/usr/bin/env python

import json

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['magisto_download']
site_info = 'Magisto magisto.com'


def magisto_download(url, info_only=False, **kwargs):
    video_hash = match1(url, r'video\/([a-zA-Z0-9]+)')
    api_url = 'https://www.magisto.com/api/video/{}'.format(video_hash)
    content = get_content(api_url)
    data = json.loads(content)
    title1 = data['title']
    title2 = data['creator']
    title = '{} - {}'.format(title1, title2)
    url = data['video_direct_url']
    _type, ext, size = url_info(url)

    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls([url], title, ext, size, **kwargs)


download = magisto_download
download_playlist = playlist_not_supported(site_info)
