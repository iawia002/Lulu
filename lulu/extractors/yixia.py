#!/usr/bin/env python

import re
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
site_info = 'Yixia'


def yixia_miaopai_download_by_scid(
    scid, output_dir='.', merge=True, info_only=False
):
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
        download_urls([video_url], title, ext, size, output_dir, merge=merge)


def yixia_xiaokaxiu_download_by_scid(
    scid, output_dir='.', merge=True, info_only=False
):
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
        download_urls([video_url], title, ext, size, output_dir, merge=merge)


def yixia_download(
    url, output_dir='.', merge=True, info_only=False, **kwargs
):
    hostname = urlparse(url).hostname
    if 'miaopai.com' in hostname:  # Miaopai
        yixia_download_by_scid = yixia_miaopai_download_by_scid

        if re.match(r'https?://www.miaopai.com/show/channel/.+', url):  # PC
            scid = match1(
                url, r'https?://www.miaopai.com/show/channel/(.+)\.htm'
            )
        elif re.match(r'https?://www.miaopai.com/show/.+', url):  # PC
            scid = match1(url, r'https?://www.miaopai.com/show/(.+)\.htm')
        elif re.match(r'https?://m.miaopai.com/show/channel/.+', url):
            # Mobile
            scid = match1(
                url, r'https?://m.miaopai.com/show/channel/(.+)\.htm'
            )
            if scid is None:
                scid = match1(url, r'https?://m.miaopai.com/show/channel/(.+)')

    elif 'xiaokaxiu.com' in hostname:  # Xiaokaxiu
        yixia_download_by_scid = yixia_xiaokaxiu_download_by_scid

        if re.match(r'http://v.xiaokaxiu.com/v/.+\.html', url):  # PC
            scid = match1(url, r'http://v.xiaokaxiu.com/v/(.+)\.html')
        elif re.match(r'http://m.xiaokaxiu.com/m/.+\.html', url):  # Mobile
            scid = match1(url, r'http://m.xiaokaxiu.com/m/(.+)\.html')

    else:
        pass

    yixia_download_by_scid(scid, output_dir, merge, info_only)


download = yixia_download
download_playlist = playlist_not_supported(site_info)
