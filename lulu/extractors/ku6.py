#!/usr/bin/env python

import string
from urllib import parse

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['ku6_download']
site_info = '酷6网 ku6.com'


def ku6_download(url, info_only=False, **kwargs):
    page = get_content(url)
    video = match1(page, r'type: "video/mp4", src: "(.+)"').replace(' ', '%20')
    video = parse.quote(
        video, safe=string.printable
    )
    title = match1(page, r'document.title = "(.+)"')
    _type, ext, size = url_info(video)
    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls([video], title, ext, size, **kwargs)


download = ku6_download
download_playlist = playlist_not_supported(site_info)
