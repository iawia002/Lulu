#!/usr/bin/env python

import re
import json

from lulu.common import (
    match1,
    print_info,
    get_content,
    download_url_ffmpeg,
    playlist_not_supported,
)


__all__ = ['metacafe_download']
site_info = 'Metacafe metacafe.com'


def metacafe_download(url, info_only=False, **kwargs):
    if re.match(r'http://www.metacafe.com/watch/\w+', url):
        html = get_content(url)
        title = match1(html, r'<meta property="og:title" content="([^"]*)"')

        data = match1(
            html,
            r"<script type='text/json' id='json_video_data'>(.+)</script>"
        )
        data = json.loads(data)
        m3u8_url = data['sources'][0]['src']
        print_info(
            site_info, title, 'm3u8', 0, m3u8_url=m3u8_url, m3u8_type='master'
        )
        if not info_only:
            download_url_ffmpeg(m3u8_url, title, 'mp4', **kwargs)


download = metacafe_download
download_playlist = playlist_not_supported(site_info)
