#!/usr/bin/env python

from lulu.common import (
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.util.parser import get_parser


__all__ = ['archive_download']
site_info = 'Internet Archive archive.org'


def archive_download(url, merge=True, info_only=False, **kwargs):
    html = get_content(url)
    parser = get_parser(html)
    title = parser.find('meta', property='og:title')['content']
    source = parser.find('meta', property='og:video')['content']
    mime, ext, size = url_info(source)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([source], title, ext, size, merge=merge, **kwargs)


download = archive_download
download_playlist = playlist_not_supported(site_info)
