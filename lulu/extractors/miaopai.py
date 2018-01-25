#!/usr/bin/env python

import json

from lulu import config
from lulu.common import (
    match1,
    url_info,
    url_size,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)

__all__ = ['miaopai_download']
site_info = 'miaopai'


def miaopai_download_by_fid(
    fid, output_dir='.', merge=False, info_only=False, **kwargs
):
    page_url = 'http://video.weibo.com/show?fid=' + fid + '&type=mp4'

    mobile_page = get_content(page_url, headers=config.FAKE_HEADERS_MOBILE)
    url = match1(mobile_page, r'<video id=.*?src=[\'"](.*?)[\'"]\W')
    title = match1(mobile_page, r'<title>((.|\n)+?)</title>')
    if not title:
        title = fid
    title = title.replace('\n', '_')
    ext, size = 'mp4', url_info(url)[2]
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls(
            [url], title, ext, total_size=None, output_dir=output_dir,
            merge=merge
        )


def miaopai_download(
    url, output_dir='.', merge=False, info_only=False, **kwargs
):
    fid = match1(url, r'\?fid=(\d{4}:\w{32})')
    if fid:
        miaopai_download_by_fid(fid, output_dir, merge, info_only)
    elif '/p/230444' in url:
        fid = match1(url, r'/p/230444(\w+)')
        miaopai_download_by_fid('1034:'+fid, output_dir, merge, info_only)
    else:
        status_id = url.split('?')[0].split('/')[-1]
        video_info = json.loads(
            get_content(
                'https://m.weibo.cn/statuses/show?id={}'.format(status_id),
                headers=config.FAKE_HEADERS_MOBILE
            )
        )
        video_url = video_info['data']['page_info']['media_info'][
            'stream_url'
        ]
        title = video_info['data']['page_info']['content2']
        video_format = 'mp4'
        size = url_size(video_url)
        print_info(
            site_info=site_info, title=title, type=video_format, size=size
        )
        if not info_only:
            download_urls(
                urls=[video_url], title=title, ext=video_format,
                total_size=size, **kwargs
            )


download = miaopai_download
download_playlist = playlist_not_supported(site_info)
