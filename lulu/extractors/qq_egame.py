import re
import json
from html import unescape

from lulu.util import log
from lulu.common import get_content
from lulu.extractor import VideoExtractor


__all__ = ['qq_egame_download']


class QQEgame(VideoExtractor):
    stream_types = [
        {'id': '1080p', 'video_profile': 0, 'container': 'flv'},
        {'id': '720p', 'video_profile': 3000, 'container': 'flv'},
        {'id': '540p', 'video_profile': 1500, 'container': 'flv'}
    ]
    name = '企鹅电竞 egame.qq.com'

    def prepare(self, **kwargs):
        page = get_content(self.url)
        server_data = re.search(r'window\.__NUXT__=({.+?});', page)
        if server_data is None:
            log.wtf('cannot find server_data')
        json_data = json.loads(server_data.group(1))['state']
        live_info = json_data['live-info']['liveInfo']
        self.title = '{}_{}'.format(
            json_data['anchor-info']['anchorInfo']['nickName'],
            live_info['videoInfo']['title']
        )
        for exsited_stream in live_info['videoInfo']['streamInfos']:
            for s in self.__class__.stream_types:
                if s['video_profile'] == exsited_stream['bitrate']:
                    current_stream_id = s['id']
                    stream_info = dict(
                        src=[unescape(exsited_stream['playUrl'])]
                    )
                    stream_info['video_profile'] = exsited_stream['desc']
                    stream_info['container'] = s['container']
                    stream_info['size'] = float('inf')
                    self.streams[current_stream_id] = stream_info


def qq_egame_download(url, **kwargs):
    QQEgame().download_by_url(url, **kwargs)
    # url dispatching has been done in qq.py
