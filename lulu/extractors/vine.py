#!/usr/bin/env python

import json

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['vine_download']
site_info = 'Vine.co'


def vine_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_content(url)
    video_id = match1(url, r'vine.co/v/([^/]+)')
    title = match1(html, r'<title>([^<]*)</title>')
    stream = match1(
        html,
        r'<meta property="twitter:player:stream" content="([^"]*)">'
    )
    if not stream:  # https://vine.co/v/.../card
        stream = match1(html, r'"videoUrl":"([^"]+)"')
        if stream:
            stream = stream.replace('\\/', '/')
        else:
            posts_url = 'https://archive.vine.co/posts/{}.json'.format(
                video_id
            )
            json_data = json.loads(get_content(posts_url))
            stream = json_data['videoDashUrl']
            title = json_data['description']
            if title == '':
                title = '{}_{}'.format(
                    json_data['username'].replace(' ', '_'), video_id
                )

    mime, ext, size = url_info(stream)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([stream], title, ext, size, output_dir, merge=merge)


download = vine_download
download_playlist = playlist_not_supported(site_info)
