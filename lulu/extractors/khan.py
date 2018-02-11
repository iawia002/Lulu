#!/usr/bin/env python


from lulu.common import (
    get_content,
    playlist_not_supported,
)
from lulu.util.parser import get_parser
from lulu.extractors.youtube import YouTube


__all__ = ['khan_download']
site_info = 'Khan Academy khanacademy.org'


def khan_download(url, **kwargs):
    html = get_content(url)
    parser = get_parser(html)
    youtube_url = parser.find('meta', property='og:video')['content']
    YouTube().download_by_url(youtube_url, **kwargs)


download = khan_download
download_playlist = playlist_not_supported(site_info)
