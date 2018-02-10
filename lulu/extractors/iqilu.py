#!/usr/bin/env python

import re
import json

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['iqilu_download']
site_info = '齐鲁网 iqilu.com'


def iqilu_download(url, info_only=False, **kwargs):
    if re.match(r'http://v.iqilu.com/\w+', url):
        patt = r'url\s*:\s*\[([^\]]+)\]'

        # URL in webpage
        html = get_content(url)
        player_data = '[{}]'.format(match1(html, patt))
        urls = json.loads(player_data)
        url = urls[0]['stream_url']

        # grab title
        title = match1(html, r'<meta name="description" content="(.*?)\"\W')

        _type, ext, size = url_info(url)
        print_info(site_info, title, _type, size)
        if not info_only:
            download_urls([url], title, ext, size, **kwargs)


download = iqilu_download
download_playlist = playlist_not_supported(site_info)
