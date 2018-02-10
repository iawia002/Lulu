#!/usr/bin/env python


from lulu.common import (
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.util.parser import get_parser


__all__ = ['freesound_download']
site_info = 'Freesound freesound.org'


def freesound_download(
    url, output_dir='.', merge=True, info_only=False, **kwargs
):
    page = get_content(url)
    parser = get_parser(page)
    title = parser.find('meta', property='og:title')['content']
    preview_url = parser.find('meta', property='og:audio')['content']

    _type, ext, size = url_info(preview_url)

    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls(
            [preview_url], title, ext, size, output_dir, merge=merge, **kwargs
        )


download = freesound_download
download_playlist = playlist_not_supported(site_info)
