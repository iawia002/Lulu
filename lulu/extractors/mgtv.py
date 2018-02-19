# coding=utf-8

import re
import os
import json
from os.path import dirname
from urllib.parse import urlsplit

from lulu.common import (
    match1,
    get_content,
    playlist_not_supported,
)
from lulu.util import log
from lulu.extractor import VideoExtractor


site_info = '芒果TV mgtv.com'


class MGTV(VideoExtractor):
    name = site_info

    # Last updated: 2016-11-13
    stream_types = [
        {'id': 'hd', 'container': 'ts', 'video_profile': '超清'},
        {'id': 'sd', 'container': 'ts', 'video_profile': '高清'},
        {'id': 'ld', 'container': 'ts', 'video_profile': '标清'},
    ]

    id_dic = {i['video_profile']: (i['id']) for i in stream_types}

    api_endpoint = 'http://pcweb.api.mgtv.com/player/video?video_id={video_id}'

    @staticmethod
    def get_vid_from_url(url):
        """Extracts video ID from URL.
        """
        vid = match1(url, 'https?://www.mgtv.com/(?:b|l)/\d+/(\d+).html')
        if not vid:
            vid = match1(url, 'https?://www.mgtv.com/hz/bdpz/\d+/(\d+).html')
        if not vid:
            vid = match1(get_content(url), r'vid: (\d+),')
        return vid

    @staticmethod
    def get_mgtv_real_url(url):
        """str->list of str
        Give you the real URLs."""
        content = json.loads(get_content(url))
        m3u_url = content['info']
        split = urlsplit(m3u_url)

        base_url = '{scheme}://{netloc}{path}/'.format(
            scheme=split[0], netloc=split[1], path=dirname(split[2])
        )

        # get the REAL M3U url, maybe to be changed later?
        content = get_content(content['info'])
        segment_list = []
        segments_size = 0
        for i in content.split():
            # not the best way, better we use the m3u8 package
            if not i.startswith('#'):
                segment_list.append(base_url + i)
            # use ext-info for fast size calculate
            elif i.startswith('#EXT-MGTV-File-SIZE:'):
                segments_size += int(i[i.rfind(':')+1:])

        return m3u_url, segments_size, segment_list

    def download_playlist_by_url(self, url, **kwargs):
        pass

    def prepare(self, **kwargs):
        if self.url:
            self.vid = self.get_vid_from_url(self.url)
        content = get_content(self.api_endpoint.format(video_id=self.vid))
        content = json.loads(content)
        self.title = '{} {}'.format(
            content['data']['info']['title'], content['data']['info']['desc']
        )
        domain = content['data']['stream_domain'][0]

        # stream_avalable = [i['name'] for i in content['data']['stream']]
        stream_available = {}
        for i in content['data']['stream']:
            stream_available[i['name']] = i['url']

        for s in self.stream_types:
            if s['video_profile'] in stream_available.keys():
                quality_id = self.id_dic[s['video_profile']]
                url = stream_available[s['video_profile']]
                url = domain + re.sub(r'(\&arange\=\d+)', '', url)  # Un-Hum
                m3u8_url, m3u8_size, segment_list_this = \
                    self.get_mgtv_real_url(url)

                stream_fileid_list = []
                for i in segment_list_this:
                    stream_fileid_list.append(
                        os.path.basename(i).split('.')[0]
                    )

            # make pieces
            pieces = []
            for i in zip(stream_fileid_list, segment_list_this):
                pieces.append({'fileid': i[0], 'segs': i[1]})

                self.streams[quality_id] = {
                        'container': s['container'],
                        'video_profile': s['video_profile'],
                        'size': m3u8_size,
                        'pieces': pieces,
                        'm3u8_url': m3u8_url
                    }

            if not kwargs['info_only']:
                self.streams[quality_id]['src'] = segment_list_this

    def extract(self, **kwargs):
        if 'stream_id' in kwargs and kwargs['stream_id']:
            # Extract the stream
            stream_id = kwargs['stream_id']

            if stream_id not in self.streams:
                log.e('[Error] Invalid video format.')
                log.e(
                    'Run \'-i\' command with no specific video format to '
                    'view all available formats.'
                )
                exit(2)
        else:
            # Extract stream with the best quality
            stream_id = self.streams_sorted[0]['id']


site = MGTV()
download = site.download_by_url
download_playlist = playlist_not_supported(site_info)
