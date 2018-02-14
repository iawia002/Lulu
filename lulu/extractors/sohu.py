#!/usr/bin/env python

import re
import json
import time
from random import random
from urllib.parse import urlparse

from lulu.common import (
    match1,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)

__all__ = ['sohu_download']
site_info = '搜狐视频 tv.sohu.com'


'''
Changelog:
    1. http://tv.sohu.com/upload/swf/20150604/Main.swf
        new api
'''


def real_url(host, vid, tvid, new, clipURL, ck):
    url = (
        'http://{}/?prot=9&prod=flash&pt=1&file={}&new={}&key={}&vid={}'
        '&uid={}&t={}&rb=1'.format(
            host, clipURL, new, ck, str(vid), str(int(time.time()*1000)),
            str(random())
        )
    )
    return json.loads(get_content(url))['url']


def sohu_download(url, info_only=False, **kwargs):
    if re.match(r'http://share.vrs.sohu.com', url):
        vid = match1(url, 'id=(\d+)')
    else:
        html = get_content(url)
        vid = match1(html, r'\Wvid\s*[\:=]\s*[\'"]?(\d+)[\'"]?')
    assert vid

    if re.match(r'http[s]://tv.sohu.com/', url):
        info = json.loads(get_content(
            'http://hot.vrs.sohu.com/vrs_flash.action?vid={}'.format(vid)
        ))
        for qtyp in ['oriVid', 'superVid', 'highVid', 'norVid', 'relativeId']:
            if 'data' in info:
                hqvid = info['data'][qtyp]
            else:
                hqvid = info[qtyp]
            if hqvid != 0 and hqvid != vid:
                info = json.loads(get_content(
                    'http://hot.vrs.sohu.com/vrs_flash.action?vid={}'.format(
                        hqvid
                    )
                ))
                if 'allot' not in info:
                    continue
                break
        host = info['allot']
        tvid = info['tvid']
        urls = []
        data = info['data']
        title = data['tvName']
        size = sum(data['clipsBytes'])
        assert len(data['clipsURL']) == len(data['clipsBytes']) \
            == len(data['su'])
        for new, clip, ck in zip(data['su'], data['clipsURL'], data['ck']):
            clipURL = urlparse(clip).path
            urls.append(real_url(host, hqvid, tvid, new, clipURL, ck))

    else:
        info = json.loads(get_content(
            'http://my.tv.sohu.com/play/videonew.do?vid={}&referer='
            'http://my.tv.sohu.com'.format(vid)
        ))
        host = info['allot']
        tvid = info['tvid']
        urls = []
        data = info['data']
        title = data['tvName']
        size = sum(map(int, data['clipsBytes']))
        assert len(data['clipsURL']) == len(data['clipsBytes']) \
            == len(data['su'])
        for new, clip, ck, in zip(data['su'], data['clipsURL'], data['ck']):
            clipURL = urlparse(clip).path
            urls.append(real_url(host, vid, tvid, new, clipURL, ck))

    print_info(site_info, title, 'mp4', size)
    if not info_only:
        download_urls(urls, title, 'mp4', size, refer=url, **kwargs)


download = sohu_download
download_playlist = playlist_not_supported(site_info)
