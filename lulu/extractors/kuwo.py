#!/usr/bin/env python

import re

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
)


__all__ = ['kuwo_download']
site_info = '酷我音乐 kuwo.cn'


def kuwo_download_by_rid(rid, info_only=False, **kwargs):
    html = get_content(
        'http://player.kuwo.cn/webmusic/st/getNewMuiseByRid?rid='
        'MUSIC_{}'.format(rid)
    )
    title = match1(html, r'<name>(.*)</name>')
    if not title:
        title = rid
    # format =aac|mp3 ->to get aac format=mp3 ->to get mp3
    url = get_content(
        'http://antiserver.kuwo.cn/anti.s?format=mp3&rid=MUSIC_{}&'
        'type=convert_url&response=url'.format(rid)
    )
    songtype, ext, size = url_info(url)
    print_info(site_info, title, songtype, size)
    if not info_only:
        download_urls([url], title, ext, size, **kwargs)


def kuwo_playlist_download(url, info_only=False, **kwargs):
    html = get_content(url)
    matched = set(re.compile('yinyue/(\d+)').findall(html))
    for rid in matched:
        kuwo_download_by_rid(rid, info_only, **kwargs)


def kuwo_download(url, info_only=False, **kwargs):
    if 'www.kuwo.cn/yinyue' in url:
        rid = match1(url, 'yinyue/(\d+)')
        kuwo_download_by_rid(rid, info_only, **kwargs)
    else:
        kuwo_playlist_download(url, info_only, **kwargs)


download = kuwo_download
download_playlist = kuwo_playlist_download
