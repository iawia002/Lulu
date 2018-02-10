#!/usr/bin/env python

import re
import json
from time import time
from urllib.parse import quote

from lulu.util import log
from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['pixnet_download']
site_info = '痞客邦 pixnet.net'


def pixnet_download(url, info_only=False, **kwargs):
    if not re.match(r'http://(\w)+.pixnet.net/album/video/(\d)+', url):
        log.wtf('[Failed] Unsupported URL pattern.')
        return
    # http://eric6513.pixnet.net/album/video/206644535
    html = get_content(url)
    title = ''.join(match1(
        html, r'<meta property="og:description\" content="([^"]*)"'
    ).split('-')[1:]).strip()

    time_now = int(time())

    m = re.match(r'http://(\w+).pixnet.net/album/video/(\d+)', url)

    username = m.group(1)
    # eric6513
    _id = m.group(2)
    # 206644535

    data_dict = {
        'username': username, 'autoplay': 1, 'id': _id, 'loop': 0,
        'profile': 9, 'time': time_now,
    }
    # have to be like this
    data_dict_str = quote(str(data_dict).replace("'", '"'), safe='"')
    url2 = 'http://api.pixnet.tv/content?type=json&customData={}'.format(
        data_dict_str
    )
    # &sig=edb07258e6a9ff40e375e11d30607983  can be blank for now
    # if required, can be obtained from url like
    # http://s.ext.pixnet.tv/user/eric6513/html5/autoplay/206644507.js
    # http://api.pixnet.tv/content?type=json&customData={%22username%22:%22eric6513%22,%22id%22:%22206644535%22,%22time%22:1441823350,%22autoplay%22:0,%22loop%22:0,%22profile%22:7}

    video_json = get_content(url2)
    content = json.loads(video_json)
    url_main = content['element']['video_url']
    url_backup = content['element']['backup_video_uri']

    try:
        # In some rare cases the main URL is IPv6 only...
        # Something like #611
        url_info(url_main)
        url = url_main
    except Exception:
        url = url_backup

    _type, ext, size = url_info(url)
    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls([url], title, ext, size, **kwargs)


download = pixnet_download
download_playlist = playlist_not_supported(site_info)
