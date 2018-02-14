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


__all__ = [
    'ximalaya_download_playlist', 'ximalaya_download',
    'ximalaya_download_by_id'
]
site_info = '喜马拉雅FM ximalaya.com'


stream_types = [
    {'itag': '1', 'container': 'm4a', 'bitrate': 'default'},
    {'itag': '2', 'container': 'm4a', 'bitrate': '32'},
    {'itag': '3', 'container': 'm4a', 'bitrate': '64'},
]


def ximalaya_download_by_id(
    _id, title=None, info_only=False, stream_id=None, **kwargs
):
    BASE_URL = 'http://www.ximalaya.com/tracks/'
    json_url = '{}{}.json'.format(BASE_URL, _id)
    json_data = json.loads(get_content(json_url))
    if 'res' in json_data:
        if json_data['res'] is False:
            raise ValueError('Server reported id {} is invalid'.format(_id))
    if 'is_paid' in json_data and json_data['is_paid']:
        if 'is_free' in json_data and not json_data['is_free']:
            raise ValueError('{} is paid item'.format(_id))
    if (not title) and 'title' in json_data:
        title = json_data['title']
    # no size data in the json. should it be calculated?
    size = 0
    url = json_data['play_path_64']
    if stream_id:
        if stream_id == '1':
            url = json_data['play_path_32']
        elif stream_id == '0':
            url = json_data['play_path']
    ext = 'm4a'
    urls = [url]
    print('Site:        %s' % site_info)
    print('title:       %s' % title)
    if info_only:
        if stream_id:
            print_stream_info(stream_id)
        else:
            for item in range(0, len(stream_types)):
                print_stream_info(item)
    if not info_only:
        print('Type:        MPEG-4 audio m4a')
        print('Size:        N/A')
        download_urls(urls, title, ext, size, **kwargs)


def ximalaya_download(url, info_only=False, stream_id=None, **kwargs):
    if re.match(r'http://www\.ximalaya\.com/(\d+)/sound/(\d+)', url):
        _id = match1(url, r'http://www\.ximalaya\.com/\d+/sound/(\d+)')
    else:
        raise NotImplementedError(url)
    ximalaya_download_by_id(
        _id, info_only=info_only, stream_id=stream_id, **kwargs
    )


def ximalaya_download_page(
    playlist_url, info_only=False, stream_id=None, **kwargs
):
    if re.match(r'http://www\.ximalaya\.com/(\d+)/album/(\d+)', playlist_url):
        page_content = get_content(playlist_url)
        pattern = re.compile(r'<li sound_id="(\d+)"')
        ids = pattern.findall(page_content)
        for _id in ids:
            try:
                ximalaya_download_by_id(
                    _id, info_only=info_only, stream_id=stream_id, **kwargs
                )
            except(ValueError):
                print(
                    'Something wrong with {}, perhaps paid item?'.format(_id)
                )
    else:
        raise NotImplementedError(playlist_url)


def ximalaya_download_playlist(url, info_only=False, stream_id=None, **kwargs):
    match_result = re.match(
        r'http://www\.ximalaya\.com/(\d+)/album/(\d+)', url
    )
    if not match_result:
        raise NotImplementedError(url)
    pages = []
    page_content = get_content(url)
    if page_content.find('<div class="pagingBar_wrapper"') == -1:
        pages.append(url)
    else:
        base_url = 'http://www.ximalaya.com/{}/album/{}'.format(
            match_result.group(1), match_result.group(2)
        )
        html_str = '<a href=(\'|")\/{}\/album\/{}\?page='.format(
            match_result.group(1), match_result.group(2)
        )
        count = len(re.findall(html_str, page_content))
        for page_num in range(count):
            pages.append('{}?page={}'.format(base_url, str(page_num+1)))
            print(pages[-1])
    for page in pages:
        ximalaya_download_page(
            page, info_only=info_only, stream_id=stream_id, **kwargs
        )


def print_stream_info(stream_id):
    print('    - itag:        %s' % stream_id)
    print('      container:   %s' % 'm4a')
    print('      bitrate:     %s' % stream_types[int(stream_id)]['bitrate'])
    print('      size:        %s' % 'N/A')
    print('    # download-with: lulu --itag=%s [URL]' % stream_id)


download = ximalaya_download
download_playlist = ximalaya_download_playlist
