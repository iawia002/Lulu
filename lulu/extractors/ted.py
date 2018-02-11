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

__all__ = ['ted_download']
site_info = 'TED ted.com'


def ted_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_content(url)
    patt = r'"__INITIAL_DATA__"\s*:\s*\{(.+)\}'
    metadata = json.loads('{' + match1(html, patt) + '}')
    title = metadata['talks'][0]['title']
    nativeDownloads = metadata['talks'][0]['downloads']['nativeDownloads']
    for quality in ['high', 'medium', 'low']:
        if quality in nativeDownloads:
            url = nativeDownloads[quality]
            _type, ext, size = url_info(url)
            print_info(site_info, title, _type, size)
            if not info_only:
                download_urls([url], title, ext, size, output_dir, merge=merge)
            break


download = ted_download
download_playlist = playlist_not_supported(site_info)
