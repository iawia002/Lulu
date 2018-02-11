#!/usr/bin/env python

import json

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
)


__all__ = ['icourses_download', 'icourses_download_playlist']
site_info = '爱课程 icourses.cn'


def _download(item, **kwargs):
    url = item['fullLinkUrl']
    title = item['title'].strip()
    _, ext, size = url_info(url)
    print_info(site_info=site_info, title=title, type=ext, size=size)
    if not kwargs.get('info_only'):
        download_urls([url], title, ext, size, **kwargs)


def icourses_download(url, **kwargs):
    page = get_content(url)
    data = json.loads(match1(page, r'var _sourceArrStr = (.+?);'))

    if 'resId' in url:  # 下载播放列表中指定视频
        _id = match1(url, r'resId=([\w-]+)')
        results = list(filter(lambda x: x['id'] == _id, data))
        _download(results[0], **kwargs)
    else:  # 下载第一个
        _download(data[0], **kwargs)


def icourses_download_playlist(url, **kwargs):
    page = get_content(url)
    data = json.loads(match1(page, r'var _sourceArrStr = (.+?);'))
    for item in data:
        _download(item, **kwargs)


download = icourses_download
download_playlist = icourses_download_playlist
