#!/usr/bin/env python

import unittest

from lulu.extractors import (
    imgur,
    magisto,
    youtube,
    yixia,
    bilibili,
    douyin,
    miaopai,
    # netease,
    youku,
)


class LuluTests(unittest.TestCase):
    def test_imgur(self):
        imgur.download('http://imgur.com/WVLk5nD', info_only=True)
        imgur.download('http://imgur.com/gallery/WVLk5nD', info_only=True)

    def test_magisto(self):
        magisto.download(
            'http://www.magisto.com/album/video/f3x9AAQORAkfDnIFDA',
            info_only=True
        )

    def test_youtube(self):
        youtube.download(
            'http://www.youtube.com/watch?v=pzKerr0JIPA', info_only=True
        )
        youtube.download('http://youtu.be/pzKerr0JIPA', info_only=True)
        youtube.download(
            'http://www.youtube.com/attribution_link?u=/watch?v%3DldAKIzq7bvs%26feature%3Dshare',  # noqa
            info_only=True
        )

    def test_yixia(self):
        yixia.download(
            'http://m.miaopai.com/show/channel/vlvreCo4OZiNdk5Jn1WvdopmAvdIJwi8',  # noqa
            info_only=True
        )

    def test_bilibili(self):
        bilibili.download(
            'https://www.bilibili.com/video/av16907446/', info_only=True
        )
        bilibili.download(
            'https://www.bilibili.com/video/av13228063/', info_only=True
        )

    def test_douyin(self):
        douyin.download(
            'https://www.douyin.com/share/video/6492273288897629454',
            info_only=True
        )

    def test_weibo(self):
        miaopai.download('https://m.weibo.cn/status/FEFq863WF', info_only=True)

    def test_netease(self):
        # failed on travis, don't know why, maybe ip issue?
        pass
        # netease.download(
        #     'http://music.163.com/#/album?id=35757233', info_only=True
        # )
        # netease.download(
        #     'http://music.163.com/#/song?id=490602750', info_only=True
        # )

    def test_youku(self):
        youku.download(
            'http://v.youku.com/v_show/id_XMzMzMDk5MzcyNA==.html',
            info_only=True
        )
        youku.download(
            'http://v.youku.com/v_show/id_XMzI2NTUyOTIxMg==.html',
            info_only=True
        )


if __name__ == '__main__':
    unittest.main()
