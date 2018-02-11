#!/usr/bin/env python

import re
import json
import time
import hashlib

from lulu.common import (
    match1,
    get_content,
)
from lulu.util import log
from lulu.util.parser import get_parser
from lulu.extractor import VideoExtractor


'''
Changelog:
-> http://www.iqiyi.com/common/flashplayer/20150916/MainPlayer_5_2_28_c3_3_7_4.swf
   use @fffonion 's method in #617.
   Add trace AVM(asasm) code in Iqiyi's encode function where the salt is put into the encode array and reassemble by RABCDasm(or WinRABCDasm),then use Fiddler to response modified file to replace the src file with its AutoResponder function ,set browser Fiddler proxy and play with !debug version! Flash Player ,finially get result in flashlog.txt(its location can be easily found in search engine).
   Code Like (without letters after #comment:),it just do the job : trace("{IQIYI_SALT}:"+salt_array.join(""))
   ```(Postion After getTimer)
     findpropstrict      QName(PackageNamespace(""), "trace")
     pushstring          "{IQIYI_SALT}:" #comment for you to locate the salt
     getscopeobject      1
     getslot             17 #comment: 17 is the salt slots number defined in code
     pushstring          ""
     callproperty        QName(Namespace("http://adobe.com/AS3/2006/builtin"), "join"), 1
     add
     callpropvoid        QName(PackageNamespace(""), "trace"), 1
   ```

-> http://www.iqiyi.com/common/flashplayer/20150820/MainPlayer_5_2_27_2_c3_3_7_3.swf
    some small changes in Zombie.bite function

'''  # noqa

'''
com.qiyi.player.core.model.def.DefinitonEnum
bid meaning for quality
0 none
1 standard
2 high
3 super
4 suprt-high
5 fullhd
10 4k
96 topspeed
'''


class Iqiyi(VideoExtractor):
    name = '爱奇艺 iqiyi.com'

    stream_types = [
        {'id': '4k', 'container': 'm3u8', 'video_profile': '4k'},
        {'id': 'BD', 'container': 'm3u8', 'video_profile': '1080p'},
        {'id': 'TD', 'container': 'm3u8', 'video_profile': '720p'},
        {'id': 'TD_H265', 'container': 'm3u8', 'video_profile': '720p H265'},
        {'id': 'HD', 'container': 'm3u8', 'video_profile': '540p'},
        {'id': 'HD_H265', 'container': 'm3u8', 'video_profile': '540p H265'},
        {'id': 'SD', 'container': 'm3u8', 'video_profile': '360p'},
        {'id': 'LD', 'container': 'm3u8', 'video_profile': '210p'},
    ]
    ids = ['4k', 'BD', 'TD', 'HD', 'SD', 'LD']
    vd_2_id = {
        10: '4k', 19: '4k', 5: 'BD', 18: 'BD', 21: 'HD_H265', 2: 'HD',
        4: 'TD', 17: 'TD_H265', 96: 'LD', 1: 'SD',
    }
    # http://www.iqiyi.com/v_19rr7p0jss.html
    # 14: 'TD' 中的 m3u8 地址中的文件有问题
    id_2_profile = {
        '4k': '4k', 'BD': '1080p', 'TD': '720p', 'HD': '540p', 'SD': '360p',
        'LD': '210p', 'HD_H265': '540p H265', 'TD_H265': '720p H265',
    }

    def get_raw_data(self, tvid, vid):
        t = int(time.time() * 1000)
        src = '76f90cbd92f94a2e925d83e8ccd22cb7'
        key = 'd5fb4bd9d50c4be6948c97edd7254b0e'
        sc = hashlib.new(
            'md5', bytes(str(t) + key + vid, 'utf-8')
        ).hexdigest()
        vmsreq = (
            'http://cache.m.iqiyi.com/jp/tmts/{}/{}/?t={}&sc={}&src={}'.format(
                tvid, vid, t, sc, src
            )
        )
        return json.loads(get_content(vmsreq)[len('var tvInfoJs='):])

    def download_playlist_by_url(self, url, **kwargs):
        self.url = url

        video_page = get_content(url)
        videos = set(re.findall(
            r'<a href="(http://www\.iqiyi\.com/v_[^"]+)"', video_page
        ))

        for video in videos:
            self.__class__().download_by_url(video, **kwargs)

    def prepare(self, **kwargs):
        assert self.url or self.vid

        if self.url and not self.vid:
            html = get_content(self.url)
            tvid = match1(self.url, r'#curid=(.+)_') or match1(
                self.url, r'tvid=([^&]+)'
            ) or match1(html, r'data-player-tvid="([^"]+)"') or match1(
                html, r'tv(?:i|I)d=(.+?)\&'
            ) or match1(html, r'param\[\'tvid\'\]\s*=\s*"(.+?)"')
            videoid = match1(self.url, r'#curid=.+_(.*)$') or match1(
                self.url, r'vid=([^&]+)'
            ) or match1(html, r'data-player-videoid="([^"]+)"') or match1(
                html, r'vid=(.+?)\&'
            ) or match1(html, r'param\[\'vid\'\]\s*=\s*"(.+?)"')
            self.vid = (tvid, videoid)
            info_u = 'http://mixer.video.iqiyi.com/jp/mixin/videos/{}'.format(
                tvid
            )
            mixin = get_content(info_u)
            mixin_json = json.loads(mixin[len('var tvInfoJs='):])
            real_u = mixin_json['url']
            real_html = get_content(real_u)
            parser = get_parser(real_html)
            self.title = parser.find('meta', property='og:title')['content']
        tvid, videoid = self.vid
        info = self.get_raw_data(tvid, videoid)
        assert info['code'] == 'A00000', "Can't play this video"
        for stream in info['data']['vidl']:
            if 'm3utx' not in stream:
                continue
            try:
                stream_id = self.vd_2_id[stream['vd']]
                stream_profile = self.id_2_profile[stream_id]
                self.streams[stream_id] = {
                    'video_profile': stream_profile,
                    'container': 'm3u8',
                    'src': [stream['m3utx']],
                    'size': 0,
                    'm3u8_url': stream['m3utx'],
                }
            except Exception as e:
                pass
                # log.i('vd: {} is not handled'.format(stream['vd']))
                # log.i('info is {}'.format(stream))


site = Iqiyi()
download = site.download_by_url
iqiyi_download_by_vid = site.download_by_vid
download_playlist = site.download_playlist_by_url
