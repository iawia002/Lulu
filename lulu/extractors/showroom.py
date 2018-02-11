#!/usr/bin/env python

import re
import json
from time import time, sleep

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_url_ffmpeg,
    playlist_not_supported,
)
from lulu.util import log
from lulu.config import FAKE_HEADERS_MOBILE


__all__ = ['showroom_download']
site_info = 'SHOWROOM showroom-live.com'


def showroom_get_roomid_by_room_url_key(room_url_key):
    """str->str
    """
    webpage_url = 'https://www.showroom-live.com/{}'.format(room_url_key)
    html = get_content(webpage_url, headers=FAKE_HEADERS_MOBILE)
    roomid = match1(html, r'room\?room_id\=(\d+)')
    assert roomid
    return roomid


def showroom_download_by_room_id(room_id, info_only=False, **kwargs):
    '''Source: Android mobile
    '''
    while True:
        timestamp = str(int(time() * 1000))
        api_endpoint = (
            'https://www.showroom-live.com/api/live/streaming_url?room_id='
            '{room_id}&_={timestamp}'.format(
                room_id=room_id, timestamp=timestamp
            )
        )
        html = get_content(api_endpoint)
        html = json.loads(html)
        if len(html) >= 1:
            break
        log.w('The live show is currently offline.')
        sleep(1)

    # This is mainly for testing the M3U FFmpeg parser so I would ignore
    # any non-m3u ones
    stream_url = [
        i['url'] for i in html['streaming_url_list']
        if i['is_default'] and i['type'] == 'hls'
    ][0]
    assert stream_url
    # title
    title = ''
    profile_api = (
        'https://www.showroom-live.com/api/room/profile?room_id='
        '{room_id}'.format(room_id=room_id)
    )
    html = json.loads(get_content(profile_api))
    try:
        title = html['main_name']
    except KeyError:
        title = 'Showroom_{room_id}'.format(room_id=room_id)

    type_, ext, size = url_info(stream_url)
    print_info(site_info, title, type_, size)
    if not info_only:
        download_url_ffmpeg(
            url=stream_url, title=title, ext='mp4', **kwargs
        )


def showroom_download(url, info_only=False, **kwargs):
    if re.match(r'(\w+)://www.showroom-live.com/([-\w]+)', url):
        room_url_key = match1(url, r'\w+://www.showroom-live.com/([-\w]+)')
        room_id = showroom_get_roomid_by_room_url_key(room_url_key)
        showroom_download_by_room_id(room_id, info_only, **kwargs)


download = showroom_download
download_playlist = playlist_not_supported(site_info)
