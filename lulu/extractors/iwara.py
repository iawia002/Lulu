#!/usr/bin/env python

import json

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.config import FAKE_HEADERS


headers = FAKE_HEADERS.copy()
headers.update({
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-CA,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'keep-alive',
    'Save-Data': 'on',
    'Cookie': 'has_js=1;show_adult=1',
})


__all__ = ['iwara_download']
site_info = 'Iwara iwara.tv'


def iwara_download(url, info_only=False, **kwargs):
    video_hash = match1(url, r'http://\w+.iwara.tv/videos/(\w+)')
    video_url = match1(url, r'(http://\w+.iwara.tv)/videos/\w+')
    html = get_content(url, headers=headers)
    title = match1(html, r'<title>(.*)</title>')
    api_url = '{}/api/video/{}'.format(video_url, video_hash)
    content = get_content(api_url, headers=headers)
    data = json.loads(content)
    _type, ext, size = url_info(data[0]['uri'], headers=headers)
    down_urls = data[0]['uri']
    print_info(down_urls, title, _type, size)

    if not info_only:
        download_urls([down_urls], title, ext, size, headers=headers, **kwargs)


download = iwara_download
download_playlist = playlist_not_supported(site_info)
