#!/usr/bin/env python

from lulu.common import (
    match1,
    print_info,
    get_content,
    download_url_ffmpeg,
    playlist_not_supported,
)
from lulu.util.parser import get_parser


__all__ = ['huomaotv_download']
site_info = '火猫直播 huomao.com'


def huomaotv_download(
    url, output_dir='.', merge=True, info_only=False, **kwargs
):
    room_id_pattern = r'huomao.com/(\d+)'
    room_id = match1(url, room_id_pattern)
    html = get_content(
        'http://m.huomao.com/mobile/mob_live/{}'.format(room_id)
    )
    parser = get_parser(html)
    m3u8_url = parser.source['src']
    title = parser.title.text

    print_info(site_info, title, 'm3u8', float('inf'))

    if not info_only:
        download_url_ffmpeg(
            m3u8_url, title, 'mp4', None, output_dir=output_dir, merge=merge
        )


download = huomaotv_download
download_playlist = playlist_not_supported(site_info)
