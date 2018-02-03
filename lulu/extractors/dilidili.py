#!/usr/bin/env python

from lulu.common import (
    match1,
    get_content,
    any_download,
    playlist_not_supported,
)


__all__ = ['dilidili_download']
site_info = 'dilidili.com'


def dilidili_download(url, **kwargs):
    html = get_content(url)
    # player loaded via internal iframe
    # http://www.maoyun.tv/mdparse/index.php?id=http://v.youku.com/v_show/id_XMTYxNzk0NjUzMg==.html  # noqa
    iframe_url = match1(html, r'<iframe src=\"(.+?)\"')
    url = match1(
        iframe_url, r'https?://www.maoyun.tv/mdparse/index.php\?id=(.+)'
    )
    any_download(url, **kwargs)


download = dilidili_download
download_playlist = playlist_not_supported(site_info)
