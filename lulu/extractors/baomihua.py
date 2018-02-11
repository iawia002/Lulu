#!/usr/bin/env python

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['baomihua_download', 'baomihua_download_by_id']
site_info = '爆米花 baomihua.com'


def baomihua_download_by_id(
    _id, title=None, output_dir='.', merge=True, info_only=False, **kwargs
):
    html = get_content(
        'http://play.baomihua.com/getvideourl.aspx?flvid={}&devicetype='
        'phone_app'.format(_id)
    )
    host = match1(html, r'host=([^&]*)')
    assert host
    _type = match1(html, r'videofiletype=([^&]*)')
    assert _type
    vid = match1(html, r'&stream_name=([^&]*)')
    assert vid
    dir_str = match1(html, r'&dir=([^&]*)').strip()
    url = 'http://{}/{}/{}.{}'.format(host, dir_str, vid, _type)
    _, ext, size = url_info(url)
    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls(
            [url], title, ext, size, output_dir, merge=merge, **kwargs
        )


def baomihua_download(
    url, output_dir='.', merge=True, info_only=False, **kwargs
):
    html = get_content(url)
    title = match1(html, r'<title>(.*)</title>')
    assert title
    _id = match1(html, r'flvid\s*=\s*(\d+)')
    assert _id
    baomihua_download_by_id(
        _id, title, output_dir=output_dir, merge=merge, info_only=info_only,
        **kwargs
    )


download = baomihua_download
download_playlist = playlist_not_supported(site_info)
