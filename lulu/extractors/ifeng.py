#!/usr/bin/env python

from html import unescape

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['ifeng_download', 'ifeng_download_by_id']
site_info = '凤凰网 ifeng.com'


def ifeng_download_by_id(_id, title=None, info_only=False, **kwargs):
    assert match1(
        _id, r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    ), _id
    url = 'http://vxml.ifengimg.com/video_info_new/{}/{}/{}.xml'.format(
        _id[-2], _id[-2:], _id
    )
    xml = get_content(url)
    title = match1(xml, r'Name="([^"]+)"')
    title = unescape(title)
    url = match1(xml, r'VideoPlayUrl="([^"]+)"')
    url = url.replace(
        'http://wideo.ifeng.com/', 'http://ips.ifeng.com/wideo.ifeng.com/'
    )
    _, ext, size = url_info(url)

    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, **kwargs)


def ifeng_download(url, info_only=False, **kwargs):
    # old pattern /uuid.shtml
    # now it could be #uuid
    _id = match1(
        url,
        r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    )
    if _id:
        return ifeng_download_by_id(_id, None, info_only=info_only, **kwargs)

    html = get_content(url)
    uuid_pattern = (
        r'"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"'
    )
    _id = match1(
        html,
        r'var vid="([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-'
        '[0-9a-f]{12})"'
    )
    if _id is None:
        video_pattern = r'"vid"\s*:\s*' + uuid_pattern
        _id = match1(html, video_pattern)
    assert _id, "Can't find video info"
    return ifeng_download_by_id(_id, None, info_only=info_only, **kwargs)


download = ifeng_download
download_playlist = playlist_not_supported(site_info)
