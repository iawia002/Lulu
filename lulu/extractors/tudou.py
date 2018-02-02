#!/usr/bin/env python

import json

from lulu.common import (
    match1,
    get_content,
    playlist_not_supported,
)
from lulu.extractors.youku import youku_download_by_vid


__all__ = ['tudou_download']
site_info = '土豆 tudou.com'


def tudou_download(url, **kwargs):
    if 'video.tudou.com' in url:
        vid = match1(url, r'.*?video.tudou.com/v/([\w=]+)')
    else:
        page = get_content(url)
        video_info = json.loads(
            match1(page, r'window.__INITIAL_STATE__=\s*(.+?);</script>')
        )
        vid = video_info['videoDesc']['detail']['videoid']
    youku_download_by_vid(vid, **kwargs)


download = tudou_download
download_playlist = playlist_not_supported(site_info)
