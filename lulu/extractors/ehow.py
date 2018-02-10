#!/usr/bin/env python

import re

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.util.parser import get_parser

__all__ = ['ehow_download']
site_info = 'eHow ehow.com'


def ehow_download(url, info_only=False, **kwargs):

    assert re.search(
        r'https?://www.ehow.com/video_', url
    ), 'URL you entered is not supported'

    html = get_content(url)
    parser = get_parser(html)
    title = parser.find('meta', property='og:title')['content']
    video = parser.find('meta', property='og:video')['content']
    url = match1(video, r'source=(.+?)&')
    _type, ext, size = url_info(url)
    print_info(site_info, title, _type, size)

    if not info_only:
        download_urls([url], title, ext, size, **kwargs)


download = ehow_download
download_playlist = playlist_not_supported(site_info)
