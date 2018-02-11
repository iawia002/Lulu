#!/usr/bin/env python

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['alive_download']
site_info = 'Alive alive.in.th'


def alive_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_content(url)

    title = match1(html, r'<meta property="og:title" content="([^"]+)"')

    url = match1(html, r'file: "(http://alive[^"]+)"')
    _type, ext, size = url_info(url)

    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge=merge)


download = alive_download
download_playlist = playlist_not_supported(site_info)
