#!/usr/bin/env python

from lulu.common import (
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.util.parser import get_parser


__all__ = ['giphy_download']
site_info = 'GIPHY giphy.com'


def giphy_download(url, info_only=False, **kwargs):
    html = get_content(url)
    parser = get_parser(html)

    title = parser.find('meta', property='og:title')['content']
    gif = parser.find('meta', property='og:image')['content']
    video = parser.find('meta', property='og:video')['content']

    for url in [gif, video]:
        _type, ext, size = url_info(url)
        print_info(site_info, title, _type, size)
        if not info_only:
            download_urls([url], title, ext, size, **kwargs)


download = giphy_download
download_playlist = playlist_not_supported(site_info)
