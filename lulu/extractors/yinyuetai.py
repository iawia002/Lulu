#!/usr/bin/env python

import re
import json
from urllib import parse

from lulu.util import fs
from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls
)


__all__ = ['yinyuetai_download', 'yinyuetai_download_by_id']
site_info = 'YinYueTai.com'


def yinyuetai_download_by_id(
    vid, title=None, output_dir='.', merge=True, info_only=False
):
    video_info = json.loads(get_content(
        'http://www.yinyuetai.com/insite/get-video-info?json=true&'
        'videoId={}'.format(vid)
    ))
    url_models = video_info['videoInfo']['coreVideoInfo']['videoUrlModels']
    url_models = sorted(url_models, key=lambda i: i['qualityLevel'])
    url = url_models[-1]['videoUrl']
    _type = ext = match1(url, r'\.(flv|mp4)')
    _, _, size = url_info(url)

    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge=merge)


def yinyuetai_download(
    url, output_dir='.', merge=True, info_only=False, **kwargs
):
    _id = match1(url, r'http://\w+.yinyuetai.com/video/(\d+)') or match1(
        url, r'http://\w+.yinyuetai.com/video/h5/(\d+)'
    )
    if not _id:
        yinyuetai_download_playlist(
            url, output_dir=output_dir, merge=merge, info_only=info_only
        )
        return

    html = get_content(url)
    title = match1(
        html, r'<meta property="og:title"\s+content="([^"]+)"/>'
    ) or match1(html, r'<title>(.*)')
    assert title
    title = parse.unquote(title)
    title = fs.legitimize(title)
    yinyuetai_download_by_id(
        _id, title, output_dir, merge=merge, info_only=info_only
    )


def yinyuetai_download_playlist(
    url, output_dir='.', merge=True, info_only=False, **kwargs
):
    html = get_content(url)

    data_ids = re.findall(r'data-id="(\d+)"\s*data-index="\d+"', html)
    for data_id in data_ids:
        yinyuetai_download(
            'http://v.yinyuetai.com/video/{}'.format(data_id),
            output_dir=output_dir, merge=merge, info_only=info_only
        )


download = yinyuetai_download
download_playlist = yinyuetai_download_playlist
