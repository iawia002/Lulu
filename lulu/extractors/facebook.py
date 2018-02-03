#!/usr/bin/env python

import re

from lulu.common import (
    match1,
    url_info,
    urls_size,
    unicodize,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['facebook_download']
site_info = 'facebook.com'


def facebook_download(
    url, output_dir='.', merge=True, info_only=False, **kwargs
):
    html = get_content(url)

    title = match1(html, r'<title id="pageTitle">(.+)</title>')

    if title is None:
        title = url

    sd_urls = list(set([
        unicodize(str.replace(i, '\\/', '/'))
        for i in re.findall(r'sd_src_no_ratelimit:"([^"]*)"', html)
    ]))
    hd_urls = list(set([
        unicodize(str.replace(i, '\\/', '/'))
        for i in re.findall(r'hd_src_no_ratelimit:"([^"]*)"', html)
    ]))
    urls = hd_urls if hd_urls else sd_urls

    _type, ext, size = url_info(urls[0], True)
    size = urls_size(urls)

    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls(urls, title, ext, size, output_dir, merge=False)


download = facebook_download
download_playlist = playlist_not_supported(site_info)
