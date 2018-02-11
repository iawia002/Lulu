#!/usr/bin/env python

from lulu.common import (
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.util.parser import get_parser


__all__ = ['joy_download']
site_info = '激动网 joy.cn'


def joy_download(url, info_only=False, **kwargs):
    page = get_content(url)
    parser = get_parser(page)
    url = parser.source['src']
    title = parser.h1.text.strip()
    _, ext, size = url_info(url)
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, **kwargs)


download = joy_download
download_playlist = playlist_not_supported(site_info)
