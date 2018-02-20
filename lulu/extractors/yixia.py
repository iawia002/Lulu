#!/usr/bin/env python

import json
from urllib.parse import urlparse

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['yixia_download']
site_info = '秒拍 miaopai.com'


def yixia_miaopai_download_by_scid(scid, info_only=False, **kwargs):
    api_endpoint = (
        'http://api.miaopai.com/m/v2_channel.json?fillType=259&scid='
        '{scid}&vend=miaopai'.format(scid=scid)
    )
    html = get_content(api_endpoint)
    api_content = json.loads(html)
    video_url = match1(api_content['result']['stream']['base'], r'(.+)\?vend')
    title = api_content['result']['ext']['t']
    _type, ext, size = url_info(video_url)
    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls([video_url], title, ext, size, **kwargs)


def yixia_xiaokaxiu_download_by_scid(scid, info_only=False, **kwargs):
    site_info = '小咖秀 xiaokaxiu.com'
    api_endpoint = (
        'http://api.xiaokaxiu.com/video/web/get_play_video?'
        'scid={scid}'.format(scid=scid)
    )
    html = get_content(api_endpoint)
    api_content = json.loads(html)
    video_url = api_content['data']['linkurl']
    title = api_content['data']['title']
    _type, ext, size = url_info(video_url)
    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls([video_url], title, ext, size, **kwargs)


def yixia_download(url, info_only=False, **kwargs):
    hostname = urlparse(url).hostname
    if 'miaopai.com' in hostname:  # Miaopai
        yixia_download_by_scid = yixia_miaopai_download_by_scid

        scid = match1(url, r'miaopai\.com/show/channel/(.+)\.htm') or \
            match1(url, r'miaopai\.com/show/(.+)\.htm') or \
            match1(url, r'm\.miaopai\.com/show/channel/(.+)\.htm') or \
            match1(url, r'm\.miaopai\.com/show/channel/([^\?]+)')

    elif 'xiaokaxiu.com' in hostname:  # Xiaokaxiu
        yixia_download_by_scid = yixia_xiaokaxiu_download_by_scid

        scid = match1(url, r'v.xiaokaxiu.com/v/(.+)\.html') or \
            match1(url, r'm.xiaokaxiu.com/m/(.+)\.html')

    else:
        pass

    yixia_download_by_scid(scid, info_only, **kwargs)


download = yixia_download
download_playlist = playlist_not_supported(site_info)
