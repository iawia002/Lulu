#!/usr/bin/env python

import re
import json
import time

from lulu.util import log
from lulu.common import (
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['panda_download']
site_info = '熊猫直播 panda.tv'


def panda_download(url, info_only=False, **kwargs):
    roomid = re.search('/(\d+)', url)
    if roomid is None:
        log.wtf('Cannot found room id for this url')
    roomid = roomid.group(1)
    json_request_url = (
        'http://www.panda.tv/api_room_v2?roomid={}&__plat=pc_web&_={}'.format(
            roomid, int(time.time())
        )
    )
    content = get_content(json_request_url)
    api_json = json.loads(content)

    errno = api_json['errno']
    errmsg = api_json['errmsg']
    if errno:
        raise ValueError('Errno : {}, Errmsg : {}'.format(errno, errmsg))
    data = api_json['data']
    title = data['roominfo']['name']
    room_key = data['videoinfo']['room_key']
    plflag = data['videoinfo']['plflag'].split('_')
    status = data['videoinfo']['status']
    if status is not '2':
        raise ValueError('The live stream is not online! (status:{})'.format(
            status)
        )

    data2 = json.loads(data['videoinfo']['plflag_list'])
    rid = data2['auth']['rid']
    sign = data2['auth']['sign']
    ts = data2['auth']['time']
    real_url = (
        'http://pl{}.live.panda.tv/live_panda/{}.flv?sign={}&ts={}&'
        'rid={}'.format(plflag[1], room_key, sign, ts, rid)
    )
    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_urls([real_url], title, 'flv', None, **kwargs)


download = panda_download
download_playlist = playlist_not_supported(site_info)
