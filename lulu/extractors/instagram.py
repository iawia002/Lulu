#!/usr/bin/env python

import re
import json

from lulu.common import (
    match1,
    url_info,
    url_size,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.util.parser import get_parser


__all__ = ['instagram_download']
site_info = 'Instagram.com'


def instagram_download(
    url, output_dir='.', merge=True, info_only=False, **kwargs
):
    url = match1(url, r'([^?]*)')
    html = get_content(url)

    vid = match1(url, r'instagram.com/p/([^/]+)')
    parser = get_parser(html)
    description = parser.find('meta', property='og:title')['content']
    title = '{} [{}]'.format(description, vid)
    stream = parser.find('meta', property='og:video')
    if stream:
        stream = stream['content']
        _, ext, size = url_info(stream)

        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls([stream], title, ext, size, output_dir, merge=merge)
    else:
        data = re.search(r'window\._sharedData\s*=\s*(.*);</script>', html)
        info = json.loads(data.group(1))

        if 'edge_sidecar_to_children' in info['entry_data']['PostPage'][0][
            'graphql'
        ]['shortcode_media']:
            edges = info['entry_data']['PostPage'][0]['graphql'][
                'shortcode_media'
            ]['edge_sidecar_to_children']['edges']
            for edge in edges:
                title = edge['node']['shortcode']
                image_url = edge['node']['display_url']
                ext = image_url.split('.')[-1]
                size = url_size(image_url)
                print_info(site_info, title, ext, size)
                if not info_only:
                    download_urls(
                        urls=[image_url], title=title, ext=ext,
                        total_size=size, output_dir=output_dir
                    )
        else:
            title = info['entry_data']['PostPage'][0]['graphql'][
                'shortcode_media'
            ]['shortcode']
            image_url = info['entry_data']['PostPage'][0]['graphql'][
                'shortcode_media'
            ]['display_url']
            ext = image_url.split('.')[-1]
            size = url_size(image_url)
            print_info(site_info, title, ext, size)
            if not info_only:
                download_urls(
                    urls=[image_url], title=title, ext=ext, total_size=size,
                    output_dir=output_dir
                )


download = instagram_download
download_playlist = playlist_not_supported(site_info)
