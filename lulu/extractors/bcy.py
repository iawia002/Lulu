#!/usr/bin/env python

from pathlib import Path

from lulu.common import (
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.util.parser import get_parser


__all__ = ['bcy_download']
site_info = '半次元 bcy.net'


def bcy_download(url, output_dir='.', info_only=False, **kwargs):
    html = get_content(url)
    parser = get_parser(html)
    title = parser.h1.text.strip()
    output_dir = Path(output_dir) / title
    imgs = parser.find_all('img', class_='detail_std detail_clickable')
    print_info(site_info, title, 'jpg', 0)
    if not info_only:
        for img in imgs:
            # https://img9.bcyimg.com/drawer/15294/post/1799t/1f5a87801a0711e898b12b640777720f.jpg/w650  # noqa
            img = img['src'][:-5]
            filename, ext = img.split('/')[-1].split('.')
            download_urls(
                [img], filename, ext, 0, output_dir, **kwargs
            )


download = bcy_download
download_playlist = playlist_not_supported(site_info)
