# coding=utf-8

import re
import json

from lulu.common import (
    get_content,
    playlist_not_supported,
)
from lulu.extractor import SimpleExtractor


__all__ = ['douyin_download_by_url']
site_info = 'douyin'


class DouYin(SimpleExtractor):
    def extract(self, url):
        self.site_info = site_info
        page_content = get_content(url)
        match_rule = re.compile(r'var data = \[(.*?)\];')
        video_info = json.loads(match_rule.findall(page_content)[0])
        self.urls = [video_info['video']['play_addr']['url_list'][0]]
        self.title = video_info['cha_list'][0]['cha_name']


download = douyin_download_by_url = DouYin()
download_playlist = playlist_not_supported(site_info)
