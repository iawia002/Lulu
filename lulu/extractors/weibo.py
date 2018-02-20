#!/usr/bin/env python

import json
from urllib import parse

from lulu import config
from lulu.common import (
    match1,
    url_size,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.extractors.yixia import yixia_miaopai_download_by_scid


__all__ = ['weibo_download']
site_info = '微博 weibo.com'


def weibo_download_by_fid(fid, info_only=False, **kwargs):
    page_url = 'http://video.weibo.com/show?fid={}&type=mp4'.format(fid)

    mobile_page = get_content(page_url, headers=config.FAKE_HEADERS_MOBILE)
    url = match1(mobile_page, r'<video id=.*?src=[\'"](.*?)[\'"]\W')
    title = match1(mobile_page, r'<title>((.|\n)+?)</title>')
    if not title:
        title = fid
    title = title.replace('\n', '_')
    ext, size = 'mp4', url_size(url)
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, **kwargs)


def get_fid(url):
    return match1(url, r'\?fid=(\d{4}:\w{32})')


def weibo_download(url, info_only=False, **kwargs):
    fid = get_fid(url)
    if fid:
        weibo_download_by_fid(fid, info_only, **kwargs)
    elif '/p/230444' in url:
        fid = match1(url, r'/p/230444(\w+)')
        weibo_download_by_fid('1034:{}'.format(fid), info_only, **kwargs)
    else:
        status_id = url.split('?')[0].split('/')[-1]
        video_info = json.loads(
            get_content(
                'https://m.weibo.cn/statuses/show?id={}'.format(status_id),
                headers=config.FAKE_HEADERS_MOBILE
            )
        )
        video_url = video_info['data']['page_info']['media_info'][
            'stream_url_hd'
        ]
        if not video_url:
            video_url = parse.unquote(
                video_info['data']['page_info']['page_url']
            )
            if 'miaopai' in video_url:
                # https://weibo.cn/sinaurl/blocked817bc30b?u=http%3A%2F%2Fmiaopai.com%2Fshow%2FnPWJvdR4z2Bg1Sz3PJpNYffjpDgEiuv4msALgw__.htm  # noqa
                scid = match1(
                    video_url.split('=')[-1],
                    r'.*?miaopai.com/show/(.+)\.htm'
                )
                return yixia_miaopai_download_by_scid(
                    scid, info_only=info_only, **kwargs
                )
            elif 'fid=' in video_url:
                # http://video.weibo.com/show?fid=1034:b91d1ecf44b0e2f18c436d819744b333  # noqa
                fid = get_fid(video_url)
                return weibo_download_by_fid(fid, info_only, **kwargs)
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


download = weibo_download
download_playlist = playlist_not_supported(site_info)
