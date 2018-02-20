#!/usr/bin/env python

import json

from lulu.common import (
    match1,
    player,
    url_size,
    print_info,
    get_content,
    download_urls,
    general_m3u8_extractor,
    playlist_not_supported,
)
from lulu.util.parser import get_parser


__all__ = ['longzhu_download']
site_info = '龙珠直播 longzhu.com'


def longzhu_download(url, info_only=False, **kwargs):
    web_domain = url.split('/')[2]
    if (web_domain == 'star.longzhu.com') or (web_domain == 'y.longzhu.com'):
        domain = url.split('/')[3].split('?')[0]
        m_url = 'http://m.longzhu.com/{}'.format(domain)
        m_html = get_content(m_url)
        room_id_patt = r'var\s*roomId\s*=\s*(\d+);'
        room_id = match1(m_html, room_id_patt)
        json_url = (
            'http://liveapi.plu.cn/liveapp/roomstatus?roomId={}'.format(
                room_id
            )
        )
        content = get_content(json_url)
        data = json.loads(content)
        streamUri = data['streamUri']
        if len(streamUri) <= 4:
            raise ValueError('The live stream is not online!')
        title = data['title']
        streamer = data['userName']
        title = '{}：{}'.format(streamer, title)

        steam_api_url = (
            'http://livestream.plu.cn/live/getlivePlayurl?roomId={}'.format(
                room_id
            )
        )
        content = get_content(steam_api_url)
        data = json.loads(content)
        isonline = data.get('isTransfer')
        if isonline == '0':
            raise ValueError('The live stream is not online!')

        real_url = data['playLines'][0]['urls'][0]['securityUrl']

        print_info(site_info, title, 'flv', float('inf'))

        if not info_only:
            download_urls([real_url], title, 'flv', None, **kwargs)

    elif web_domain == 'replay.longzhu.com':
        videoid = match1(url, r'(\d+)$')
        json_url = (
            'http://liveapi.longzhu.com/livereplay/getreplayfordisplay?'
            'videoId={}'.format(videoid)
        )
        content = get_content(json_url)
        data = json.loads(content)

        username = data['userName']
        title = data['title']
        title = '{}：{}'.format(username, title)
        real_url = data['videoUrl']

        print_info(site_info, title, 'm3u8', 0)
        if player:
            download_urls([real_url], title, 'm3u8', 0, **kwargs)
        else:
            urls = general_m3u8_extractor(real_url)
            if not info_only:
                download_urls(urls, title, 'ts', 0, **kwargs)

    elif web_domain == 'v.longzhu.com':
        page = get_content(url)
        parser = get_parser(page)
        title = parser.title.text
        media_id = match1(url, r'(\d+)$')
        # http://r.plures.net/ov/video/mobile/channel/video-1525da26174.js
        json_url = (
            'http://api.v.plu.cn/CloudMedia/GetInfoForPlayer?'
            'mediaId={}'.format(media_id)
        )
        content = get_content(json_url)
        data = json.loads(content)
        video = list(filter(lambda x: x['Ext'] == 'mp4', data['urls']))[0]
        video_url = video['SecurityUrl']
        ext = video['Ext']
        size = url_size(video_url)

        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls([video_url], title, ext, size, **kwargs)

    else:
        raise ValueError('Wrong url or unsupported link ... {}'.format(url))


download = longzhu_download
download_playlist = playlist_not_supported(site_info)
