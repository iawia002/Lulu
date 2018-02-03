#!/usr/bin/env python

import re
import os
from pathlib import Path

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
)
from lulu.util.parser import get_parser


__all__ = ['douban_download']
site_info = '豆瓣 douban.com'


def douban_download(
    url, output_dir='.', merge=True, info_only=False, **kwargs
):
    html = get_content(url)
    parser = get_parser(html)

    if re.match(r'https?://movie', url):
        title = ' '.join(
            [string.strip() for string in parser.h1.strings]
        )
        tid = match1(url, 'trailer/(\d+)')
        real_url = 'https://movie.douban.com/trailer/video_url?tid={}'.format(
            tid
        )
        _type, ext, size = url_info(real_url)

        print_info(site_info, title, _type, size)
        if not info_only:
            download_urls(
                [real_url], title, ext, size, output_dir, merge=merge
            )


def douban_download_playlist(url, output_dir='.', **kwargs):
    html = get_content(url)
    parser = get_parser(html)
    video_dir = Path(output_dir) / parser.h1.a.text
    if not kwargs['info_only']:
        if not video_dir.exists():
            os.mkdir(video_dir)
    urls = parser.find_all('a', class_='pr-video')
    for url in urls:
        douban_download(url['href'], output_dir=video_dir, **kwargs)


download = douban_download
download_playlist = douban_download_playlist
