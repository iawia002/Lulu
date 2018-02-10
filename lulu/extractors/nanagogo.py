#!/usr/bin/env python

import re
import json

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.extractors.universal import universal_download


__all__ = ['nanagogo_download']
site_info = '755 7gogo.jp'


def nanagogo_download(url, info_only=False, **kwargs):
    if re.match(r'https?://stat.7gogo.jp', url):
        universal_download(url, info_only=info_only, **kwargs)
        return

    talk_id = match1(url, r'7gogo.jp/([^/]+)/')
    post_id = match1(url, r'7gogo.jp/[^/]+/(\d+)')
    title = '{}_{}'.format(talk_id, post_id)
    api_url = 'https://api.7gogo.jp/web/v2/talks/{}/posts/{}'.format(
        talk_id, post_id
    )
    info = json.loads(get_content(api_url))

    items = []
    if info['data']['posts']['post'] is None:
        return
    if info['data']['posts']['post']['body'] is None:
        return
    for i in info['data']['posts']['post']['body']:
        if 'image' in i:
            image_url = i['image']
            if image_url[:2] == '//':
                continue  # skip stamp images
            _, ext, size = url_info(image_url)
            items.append({
                'title': title, 'url': image_url, 'ext': ext, 'size': size
            })
        elif 'movieUrlHq' in i:
            movie_url = i['movieUrlHq']
            _, ext, size = url_info(movie_url)
            items.append({
                'title': title, 'url': movie_url, 'ext': ext, 'size': size
            })

    size = sum([i['size'] for i in items])
    if size == 0:
        return  # do not fail the whole process
    print_info(site_info, title, ext, size)
    if not info_only:
        for i in items:
            print_info(site_info, i['title'], i['ext'], i['size'])
            download_urls(
                [i['url']], i['title'], i['ext'], i['size'], **kwargs
            )


download = nanagogo_download
download_playlist = playlist_not_supported(site_info)
