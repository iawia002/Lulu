#!/usr/bin/env python

import time
import json
import socket
import hashlib
import urllib.parse
import urllib.request
from xml.dom.minidom import parseString

from lulu.common import (
    match1,
    get_content,
    url_locations,
)
from lulu.util import log
from lulu.config import FAKE_HEADERS
from lulu.util.parser import get_parser
from lulu.extractor import VideoExtractor
from lulu.extractors.qq import qq_download_by_vid
from lulu.extractors.sina import sina_download_by_vid
from lulu.extractors.youku import youku_download_by_vid


__all__ = ['bilibili_download']


class Bilibili(VideoExtractor):
    name = '哔哩哔哩 bilibili.com'
    live_api = 'https://live.bilibili.com/api/playurl?cid={}&otype=json'
    api_url = 'https://interface.bilibili.com/v2/playurl?'
    bangumi_api_url = 'https://bangumi.bilibili.com/player/web_api/playurl?'
    live_room_init_api_url = (
        'https://api.live.bilibili.com/room/v1/Room/room_init?id={}'
    )
    live_room_info_api_url = (
        'https://api.live.bilibili.com/room/v1/Room/get_info?room_id={}'
    )

    SEC1 = '1c15888dc316e05a15fdd0a02ed6584f'
    SEC2 = '9b288147e5474dd2aa67085f716c560d'
    stream_types = [
        {'id': 'flv_p60'},
        {'id': 'flv720_p60'},
        {'id': 'flv'},
        {'id': 'flv720'},
        {'id': 'flv480'},
        {'id': 'flv360'},
        {'id': 'hdmp4'},
        {'id': 'mp4'},
        {'id': 'live'},
        {'id': 'vc'},
    ]

    @staticmethod
    def bilibili_stream_type(urls):
        url = urls[0]
        if '-116.flv' in url:
            return 'flv_p60', 'flv'
        if '-74.flv' in url:
            return 'flv720_p60', 'flv'
        if '-80.flv' in url:
            return 'flv', 'flv'
        if '-64.flv' in url:
            return 'flv720', 'flv'
        if '-32.flv' in url:
            return 'flv480', 'flv'
        if '-15.flv' in url:
            return 'flv360', 'flv'
        if '.flv' in url:
            return 'flv', 'flv'
        if 'hd.mp4' in url or '-48.mp4' in url:
            return 'hdmp4', 'mp4'
        if '.mp4' in url:
            return 'mp4', 'mp4'
        raise Exception('Unknown stream type')

    def api_req(self, cid, quality, bangumi, bangumi_movie=False, **kwargs):
        ts = str(int(time.time()))
        if not bangumi:
            params_str = 'cid={}&player=1&qn={}&quality={}&ts={}'.format(
                cid, quality, quality, ts
            )
            chksum = hashlib.md5(
                bytes(params_str+self.SEC1, 'utf8')
            ).hexdigest()
            api_url = self.api_url + params_str + '&sign=' + chksum
        else:
            mod = 'movie' if bangumi_movie else 'bangumi'
            params_str = (
                'cid={}&module={}&player=1&qn={}&quality={}&ts={}'.format(
                    cid, mod, quality, quality, ts
                )
            )
            chksum = hashlib.md5(
                bytes(params_str+self.SEC2, 'utf8')
            ).hexdigest()
            api_url = self.bangumi_api_url + params_str + '&sign=' + chksum

        xml_str = get_content(api_url, headers={
            'Referer': self.url,
            'User-Agent': FAKE_HEADERS['User-Agent'],
        })
        return xml_str

    def parse_bili_xml(self, xml_str):
        urls_list = []
        total_size = 0
        doc = parseString(xml_str.encode('utf8'))
        durls = doc.getElementsByTagName('durl')
        for durl in durls:
            size = durl.getElementsByTagName('size')[0]
            total_size += int(size.firstChild.nodeValue)
            url = durl.getElementsByTagName('url')[0]
            urls_list.append(url.firstChild.nodeValue)
        if not urls_list:
            return
        stream_type, container = self.bilibili_stream_type(urls_list)
        if stream_type not in self.streams:
            self.streams[stream_type] = {}
            self.streams[stream_type]['src'] = urls_list
            self.streams[stream_type]['size'] = total_size
            self.streams[stream_type]['container'] = container

    def download_by_vid(self, cid, bangumi, **kwargs):
        stream_id = kwargs.get('stream_id')
        # guard here. if stream_id invalid, fallback as not stream_id

        info_only = kwargs.get('info_only')
        for qlt in [116, 74, 80, 64, 32, 15]:
            api_xml = self.api_req(cid, qlt, bangumi, **kwargs)
            self.parse_bili_xml(api_xml)
        if not info_only or stream_id:
            self.danmuku = get_danmuku_xml(cid)

    def prepare(self, **kwargs):
        if socket.getdefaulttimeout() == 600:  # no timeout specified
            socket.setdefaulttimeout(2)  # fail fast, very speedy!

        # handle 'watchlater' URLs
        if '/watchlater/' in self.url:
            aid = match1(self.url, r'av(\d+)')
            self.url = 'https://www.bilibili.com/video/av{}/'.format(aid)
        self.ua = FAKE_HEADERS['User-Agent']
        if 'bangumi' not in self.url:
            # bangumi redirect will miss fragment argument here
            # http://bangumi.bilibili.com/anime/21542/play#173286 ->
            # https://www.bilibili.com/bangumi/play/ss21542
            # It should be https://www.bilibili.com/bangumi/play/ss21542#173286
            self.url = url_locations([self.url])[0]

        frag = urllib.parse.urlparse(self.url).fragment
        # http://www.bilibili.com/video/av3141144/index_2.html#page=3
        if frag:
            page = match1(frag, r'page=(\d+)')
            if page:
                aid = match1(self.url, r'av(\d+)')
                self.url = (
                    'https://www.bilibili.com/video/av{}/index_{}.html'.format(
                        aid, page
                    )
                )

        # handle bangumi url like this
        # http://bangumi.bilibili.com/anime/21542/play#173286
        # https://www.bilibili.com/bangumi/play/ss21542#173286
        # https://www.bilibili.com/bangumi/play/ep173286
        bangumi_ep_id = match1(self.url, r'/anime/\d+/play#(\d+)') or \
            match1(self.url, r'/bangumi/play/ss\d+#(\d+)')
        if bangumi_ep_id:
            self.url = 'https://www.bilibili.com/bangumi/play/ep{}'.format(
                bangumi_ep_id
            )

        self.referer = self.url
        self.page = get_content(self.url)
        self.parser = get_parser(self.page)
        if self.parser.h1:
            self.title = self.parser.h1.text.strip()
        else:
            # Some movie page got no h1 tag
            self.title = self.parser.find(
                'meta', property='og:title'
            )['content']
        if 'subtitle' in kwargs:
            subtitle = kwargs['subtitle']
            self.title = '{} {}'.format(self.title, subtitle)

        if 'live.bilibili.com' in self.url:
            self.live_entry(**kwargs)
        elif 'vc.bilibili.com' in self.url:
            self.vc_entry(**kwargs)
        else:
            # bangumi, movie use this entry too
            self.entry(**kwargs)

    def entry(self, **kwargs):
        # tencent player
        tc_flashvars = match1(
            self.page, r'"bili-cid=\d+&bili-aid=\d+&vid=([^"]+)"'
        )
        if tc_flashvars:
            self.out = True
            qq_download_by_vid(
                tc_flashvars, self.title, output_dir=kwargs['output_dir'],
                merge=kwargs['merge'], info_only=kwargs['info_only']
            )
            return

        has_plist = r'<option' in self.page
        if has_plist and match1(self.url, 'index_(\d+).html') is None:
            log.w(
                'This page contains a playlist. (use --playlist to download '
                'all videos.)'
            )

        cid = match1(self.page, r'cid=(\d+)') \
            or match1(self.page, r'"cid":(\d+)')
        if cid:
            self.download_by_vid(
                cid, 'bangumi' in self.url, **kwargs
            )
        else:
            # flashvars?
            flashvars = match1(self.page, r'flashvars="([^"]+)"')
            if flashvars is None:
                raise Exception('Unsupported page {}'.format(self.url))
            param = flashvars.split('&')[0]
            t, cid = param.split('=')
            t = t.strip()
            cid = cid.strip()
            if t == 'vid':
                sina_download_by_vid(
                    cid, self.title, output_dir=kwargs['output_dir'],
                    merge=kwargs['merge'], info_only=kwargs['info_only']
                )
            elif t == 'ykid':
                youku_download_by_vid(
                    cid, self.title, output_dir=kwargs['output_dir'],
                    merge=kwargs['merge'], info_only=kwargs['info_only']
                )
            else:
                raise NotImplementedError(
                    'Unknown flashvars {}'.format(flashvars)
                )
            return

    def live_entry(self, **kwargs):
        # Extract room ID from the short display ID (seen in the room
        # URL). The room ID is usually the same as the short ID, but not
        # always; case in point: https://live.bilibili.com/48, with 48
        # as the short ID and 63727 as the actual ID.
        room_short_id = match1(
            self.url, r'live.bilibili.com/([^?]+)'
        )
        room_init_api_response = json.loads(get_content(
            self.live_room_init_api_url.format(room_short_id)
        ))
        self.room_id = room_init_api_response['data']['room_id']

        room_info_api_response = json.loads(get_content(
            self.live_room_info_api_url.format(self.room_id)
        ))
        self.title = room_info_api_response['data']['title']

        api_url = self.live_api.format(self.room_id)
        json_data = json.loads(get_content(api_url))
        urls = [json_data['durl'][0]['url']]

        self.streams['live'] = {}
        self.streams['live']['src'] = urls
        self.streams['live']['container'] = 'flv'
        self.streams['live']['size'] = 0

    def vc_entry(self, **kwargs):
        vc_id = match1(self.url, r'video/(\d+)') \
            or match1(self.url, r'vcdetail\?vc=(\d+)')
        if not vc_id:
            log.wtf('Unknown url pattern')
        endpoint = (
            'https://api.vc.bilibili.com/clip/v1/video/detail?video_id={}'
            '&need_playurl=1'.format(vc_id)
        )
        vc_meta = json.loads(get_content(endpoint, headers=FAKE_HEADERS))
        if vc_meta['code'] != 0:
            log.wtf('{}\n{}'.format(vc_meta['msg'], vc_meta['message']))
        item = vc_meta['data']['item']
        self.title = item['description']

        self.streams['vc'] = {}
        self.streams['vc']['src'] = [item['video_playurl']]
        self.streams['vc']['container'] = 'mp4'
        self.streams['vc']['size'] = int(item['video_size'])


def collect_bangumi_urls(json_data):
    eps = json_data['episodes'][::-1]
    return [ep['webplay_url'] for ep in eps]


def get_bangumi_info(bangumi_id):
    BASE_URL = 'https://bangumi.bilibili.com/jsonp/seasoninfo/'
    long_epoch = int(time.time() * 1000)
    req_url = '{}{}.ver?callback=seasonListCallback&jsonp=jsonp&_={}'.format(
        BASE_URL, bangumi_id, str(long_epoch)
    )
    season_data = get_content(req_url)
    season_data = season_data[len('seasonListCallback('):]
    season_data = season_data[: -1 * len(');')]
    json_data = json.loads(season_data)
    return json_data['result']


def get_danmuku_xml(cid):
    return get_content('https://comment.bilibili.com/{}.xml'.format(cid))


site = Bilibili()


def bilibili_download_playlist_by_url(url, **kwargs):
    url = url_locations([url])[0]
    if 'live.bilibili' in url:
        site.download_by_url(url)
    elif 'bangumi.bilibili' in url:
        bangumi_id = match1(url, r'(\d+)')
        bangumi_data = get_bangumi_info(bangumi_id)
        ep_urls = collect_bangumi_urls(bangumi_data)
        for ep_url in ep_urls:
            Bilibili().download_by_url(ep_url, **kwargs)
    else:
        aid = match1(url, r'av(\d+)')
        if aid:
            # normal playlist
            # https://www.bilibili.com/video/av16907446/
            page_list = json.loads(get_content(
                'https://www.bilibili.com/widget/getPageList?aid={}'.format(
                    aid
                )
            ))
            page_cnt = len(page_list)
            for no in range(1, page_cnt+1):
                page_url = (
                    'https://www.bilibili.com/video/av{}/index_{}.html'.format(
                        aid, no
                    )
                )
                subtitle = page_list[no-1]['pagename']
                # 循环里面不能用同一个实例，self.streams 不会改变的
                # 它里面始终存的是第一个地址的最高清晰度的 url
                # parse_bili_xml L107
                Bilibili().download_by_url(
                    page_url, subtitle=subtitle, **kwargs
                )
        else:
            # tv playlist
            # https://www.bilibili.com/bangumi/play/ep196751/
            page = get_content(url)
            ep_data = json.loads(match1(
                page, r'window.__INITIAL_STATE__=(.+?);'
            ))
            for ep in ep_data['epList']:
                ep_url = 'https://www.bilibili.com/bangumi/play/ep{}'.format(
                    ep['ep_id']
                )
                Bilibili().download_by_url(ep_url, **kwargs)


download = bilibili_download = site.download_by_url
download_playlist = bilibili_download_playlist_by_url
