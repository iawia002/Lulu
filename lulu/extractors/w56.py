#!/usr/bin/env python

import json

from lulu.common import (
    match1,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.extractors.sohu import sohu_download


__all__ = ['w56_download', 'w56_download_by_id']
site_info = '56网 56.com'


def w56_download_by_id(_id, title=None, info_only=False, **kwargs):
    content = json.loads(get_content(
        'http://vxml.56.com/json/{}/?src=site'.format(_id)
    ))
    info = content['info']
    title = title or info['Subject']
    assert title
    hd = info['hd']
    assert hd in (0, 1, 2)
    hd_types = [['normal', 'qvga'], ['clear', 'vga'], ['super', 'wvga']][hd]
    files = [x for x in info['rfiles'] if x['type'] in hd_types]
    assert len(files) == 1
    size = int(files[0]['filesize'])
    url = files[0]['url'] + '&prod=56'
    ext = 'mp4'

    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, **kwargs)


def w56_download(url, info_only=False, **kwargs):
    content = get_content(url)
    sohu_url = match1(content, r'url:\s*"(.+)"')
    if sohu_url:
        sohu_download(sohu_url, info_only=info_only, **kwargs)
        return
    _id = match1(url, r'http://www.56.com/u\d+/v_(\w+).html') or \
        match1(url, r'http://www.56.com/.*vid-(\w+).html')
    w56_download_by_id(_id, info_only=info_only, **kwargs)


download = w56_download
download_playlist = playlist_not_supported(site_info)
