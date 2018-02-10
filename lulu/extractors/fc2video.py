#!/usr/bin/env python

from hashlib import md5
from urllib.parse import urlparse

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.config import FAKE_HEADERS


__all__ = ['fc2video_download']
site_info = 'FC2 Video video.fc2.com'


def makeMimi(upid):
    """From http://cdn37.atwikiimg.com/sitescript/pub/dksitescript/FC2.site.js
    Also com.hps.util.fc2.FC2EncrptUtil.makeMimiLocal
    L110
    """
    strSeed = 'gGddgPfeaf_gzyr'
    prehash = '{}_{}'.format(upid, strSeed)
    return md5(prehash.encode('utf-8')).hexdigest()


def fc2video_download_by_upid(
    upid, output_dir='.', merge=True, info_only=False, **kwargs
):
    fake_headers = FAKE_HEADERS.copy()
    fake_headers.update({
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-CA,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2',
        'X-Requested-With': 'ShockwaveFlash/19.0.0.245',
        'Connection': 'keep-alive',
    })
    api_base = (
        'https://video.fc2.com/ginfo.php?upid={upid}&mimi='
        '{mimi}'.format(upid=upid, mimi=makeMimi(upid))
    )
    html = get_content(api_base, headers=fake_headers)
    video_url = match1(html, r'filepath=(.+)&sec')
    video_url = video_url.replace('&mid', '?mid')

    title = match1(html, r'&title=([^&]+)')

    _type, ext, size = url_info(video_url, headers=fake_headers)
    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls(
            [video_url], title, ext, size, output_dir, merge=merge,
            headers=fake_headers, **kwargs
        )


def fc2video_download(
    url, output_dir='.', merge=True, info_only=False, **kwargs
):
    """wrapper"""
    # 'http://video.fc2.com/en/content/20151021bTVKnbEw'
    # 'http://xiaojiadianvideo.asia/content/20151021bTVKnbEw'
    # 'http://video.fc2.com/ja/content/20151021bTVKnbEw'
    # 'http://video.fc2.com/tw/content/20151021bTVKnbEw'
    hostname = urlparse(url).hostname
    if not ('fc2.com' in hostname or 'xiaojiadianvideo.asia' in hostname):
        return False
    upid = match1(url, r'.+/content/(\w+)')

    fc2video_download_by_upid(upid, output_dir, merge, info_only)


download = fc2video_download
download_playlist = playlist_not_supported(site_info)
