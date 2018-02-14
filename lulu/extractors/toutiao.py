#!/usr/bin/env python

import json
import base64
import random
import binascii

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['toutiao_download', ]
site_info = 'Toutiao.com'


def sign_video_url(vid):
    # some code from http://codecloud.net/110854.html
    r = str(random.random())[2:]

    def right_shift(val, n):
        return val >> n if val >= 0 else (val + 0x100000000) >> n

    url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/%s' % vid
    n = '{}?r={}'.format(
        url.replace('http://i.snssdk.com', ''), r
    )
    c = binascii.crc32(n.encode('ascii'))
    s = right_shift(c, 0)
    return '{}?r={}&s={}'.format(url, r, s)


class ToutiaoVideoInfo(object):

    def __init__(self):
        self.bitrate = None
        self.definition = None
        self.size = None
        self.height = None
        self.width = None
        self.type = None
        self.url = None

    def __str__(self):
        return json.dumps(self.__dict__)


def get_file_by_vid(video_id):
    vRet = []
    url = sign_video_url(video_id)
    ret = get_content(url)
    ret = json.loads(ret)
    vlist = ret.get('data').get('video_list')
    if len(vlist) > 0:
        vInfo = vlist.get(sorted(vlist.keys(), reverse=True)[0])
        vUrl = vInfo.get('main_url')
        vUrl = base64.decodestring(vUrl.encode('ascii')).decode('ascii')
        videoInfo = ToutiaoVideoInfo()
        videoInfo.bitrate = vInfo.get('bitrate')
        videoInfo.definition = vInfo.get('definition')
        videoInfo.size = vInfo.get('size')
        videoInfo.height = vInfo.get('vheight')
        videoInfo.width = vInfo.get('vwidth')
        videoInfo.type = vInfo.get('vtype')
        videoInfo.url = vUrl
        vRet.append(videoInfo)
    return vRet


def toutiao_download(url, info_only=False, **kwargs):
    html = get_content(url)
    video_id = match1(html, r"videoid\s*:\s*'([^']+)',\n")
    title = match1(html, r"title: '([^']+)'.replace")
    video_file_list = get_file_by_vid(video_id)  # 调api获取视频源文件
    _type, ext, size = url_info(video_file_list[0].url, faker=True)
    print_info(site_info=site_info, title=title, type=_type, size=size)
    if not info_only:
        download_urls([video_file_list[0].url], title, ext, size, **kwargs)


download = toutiao_download
download_playlist = playlist_not_supported(site_info)
