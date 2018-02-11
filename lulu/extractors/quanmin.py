#!/usr/bin/env python

import json

from lulu.common import (
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['quanmin_download']
site_info = '全民直播 quanmin.tv'


def quanmin_download(url, info_only=False, **kwargs):
    roomid = url.split('/')[3].split('?')[0]

    json_request_url = (
        'https://m.quanmin.tv/json/rooms/{}/noinfo6.json'.format(roomid)
    )
    content = get_content(json_request_url)
    data = json.loads(content)

    title = data['title']

    if not data['play_status']:
        raise ValueError('The live stream is not online!')
    real_url = 'https://flv.quanmin.tv/live/{}.flv'.format(roomid)

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_urls([real_url], title, 'flv', None, **kwargs)


download = quanmin_download
download_playlist = playlist_not_supported(site_info)
