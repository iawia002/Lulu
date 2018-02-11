#!/usr/bin/env python

import re
import json
from base64 import b64decode

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
)


__all__ = ['kugou_download']
site_info = '酷狗音乐 kugou.com'


def kugou_download_by_hash(hash_val, info_only=False, **kwargs):
    # http://www.kugou.com/yy/album/single/536957.html
    html = get_content(
        'http://www.kugou.com/yy/index.php?r=play/getdata&hash={}'.format(
            hash_val
        )
    )
    data = json.loads(html)
    url = data['data']['play_url']
    title = data['data']['audio_name']
    songtype, ext, size = url_info(url)
    print_info(site_info, title, songtype, size)
    if not info_only:
        download_urls([url], title, ext, size, **kwargs)


def kugou_download_playlist(url, info_only=False, **kwargs):
    html = get_content(url)
    pattern = re.compile('title="(.*?)".* data="(\w*)\|.*?"')
    pairs = pattern.findall(html)
    for title, hash_val in pairs:
        kugou_download_by_hash(hash_val, info_only, **kwargs)


def kugou_download(url, info_only=False, **kwargs):
    html = get_content(url)
    if url.lower().find('5sing') != -1:
        # for 5sing.kugou.com
        ticket = match1(html, r'"ticket":\s*"(.*)"')
        j = json.loads(str(b64decode(ticket), encoding='utf-8'))
        url = j['file']
        title = j['songName']
        songtype, ext, size = url_info(url)
        print_info(site_info, title, songtype, size)
        if not info_only:
            download_urls([url], title, ext, size, **kwargs)
    else:
        # for the www.kugou.com
        hash_val = match1(url, r'hash=(\w+)')
        kugou_download_by_hash(hash_val, info_only, **kwargs)


download = kugou_download
download_playlist = kugou_download_playlist
