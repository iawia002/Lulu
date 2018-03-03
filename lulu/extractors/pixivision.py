# coding=utf-8

from pathlib import Path

from lulu.common import (
    url_size,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.config import FAKE_HEADERS
from lulu.util.parser import get_parser


__all__ = ['pixivision_download']
site_info = 'pixivision pixivision.net'


def pixivision_download(url, output_dir='.', info_only=False, **kwargs):
    html = get_content(url)
    parser = get_parser(html)
    title = parser.h1.text.strip()
    output_dir = Path(output_dir) / title
    imgs = parser.find_all('img', class_='am__work__illust')
    print_info(site_info, title, 'jpg', 0)
    if not info_only:
        headers = FAKE_HEADERS.copy()
        headers.update({'Referer': url})
        for img in imgs:
            img = img['src']
            size = url_size(img, headers=headers)
            filename, ext = img.split('/')[-1].split('.')
            download_urls(
                [img], filename, ext, size, output_dir, refer=url, **kwargs
            )


download = pixivision_download
download_playlist = playlist_not_supported(site_info)
