#!/usr/bin/env python

import unittest

from tests.util import (
    skipOnCI,
    skipOnAppVeyor,
    ignore_network_issue,
)
from lulu.extractors import (
    qq,
    vine,
    # acfun,
    tudou,
    imgur,
    iqiyi,
    yixia,
    youku,
    douyin,
    huaban,
    ixigua,
    magisto,
    miaopai,
    netease,
    youtube,
    bilibili,
    kuaishou,
    instagram,
    yinyuetai,
)
from lulu.common import any_download_playlist


class TestExtractors(unittest.TestCase):
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
            'http://www.youtube.com/attribution_link?u=/watch?'
            'v%3DldAKIzq7bvs%26feature%3Dshare',
            info_only=True
        )
        youtube.download(
            'https://www.youtube.com/watch?v=Gnbch2osEeo', info_only=True
        )

    @skipOnAppVeyor
    @ignore_network_issue
    def test_yixia(self):
        yixia.download(
            'http://m.miaopai.com/show/channel/'
            'vlvreCo4OZiNdk5Jn1WvdopmAvdIJwi8',
            info_only=True
        )
        yixia.download(
            'https://www.miaopai.com/show/'
            '0lZvjbpWeWkKxi2OyrgHIOc8S7cihgbwadeF5g__.htm',
            info_only=True
        )

    def test_bilibili(self):
        any_download_playlist(
            'https://www.bilibili.com/video/av16907446/', info_only=True
        )
        any_download_playlist(
            'https://bangumi.bilibili.com/anime/5584', info_only=True
        )
        bilibili.download(
            'https://www.bilibili.com/video/av16907446/', info_only=True
        )
        bilibili.download(
            'https://www.bilibili.com/video/av13228063/', info_only=True
        )
        bilibili.download(
            'https://www.bilibili.com/video/av18764071/', info_only=True
        )
        bilibili.download(
            'https://www.bilibili.com/bangumi/play/ep113875', info_only=True
        )

    @ignore_network_issue
    def test_douyin(self):
        douyin.download(
            'https://www.douyin.com/share/video/6492273288897629454',
            info_only=True
        )
        douyin.download(
            'https://www.douyin.com/share/video/6511578018618543368',
            info_only=True
        )

    @ignore_network_issue
    def test_weibo(self):
        miaopai.download(
            'https://m.weibo.cn/status/FEFq863WF', info_only=True
        )
        miaopai.download(
            'https://m.weibo.cn/status/4199826726109820', info_only=True
        )

    @skipOnCI
    def test_netease(self):
        # failed on travis, don't know why, maybe ip issue?
        netease.download(
            'http://music.163.com/#/album?id=35757233', info_only=True
        )
        netease.download(
            'http://music.163.com/#/song?id=490602750', info_only=True
        )

    @ignore_network_issue
    def test_youku(self):
        youku.download(
            'http://v.youku.com/v_show/id_XMzMzMDk5MzcyNA==.html',
            info_only=True
        )
        youku.download(
            'http://v.youku.com/v_show/id_XMzI2NTUyOTIxMg==.html',
            info_only=True
        )

    @ignore_network_issue
    def test_qq(self):
        qq.download('https://v.qq.com/x/page/n0528cwq4xr.html', info_only=True)
        qq.download(
            'https://v.qq.com/x/cover/ps6mnfqyrfo7es3/q0181hpdvo5.html?',
            info_only=True
        )
        qq.download(
            'http://v.qq.com/cover/p/ps6mnfqyrfo7es3.html?vid=q0181hpdvo5',
            info_only=True
        )
        qq.download(
            'https://v.qq.com/x/cover/9hpjiv5fhiyn86u/t0522x58xma.html',
            info_only=True
        )

    # @ignore_network_issue
    # def test_acfun(self):
    #     acfun.download('http://www.acfun.cn/v/ac4209715', info_only=True)
    #     acfun.download('http://www.acfun.cn/v/ac4210425', info_only=True)

    @ignore_network_issue
    def test_kuaishou(self):
        kuaishou.download(
            'https://www.kuaishou.com/photo/84224949/4007135407',
            info_only=True
        )
        kuaishou.download(
            'https://www.kuaishou.com/photo/84224949/4267454322',
            info_only=True
        )

    @ignore_network_issue
    def test_huaban(self):
        huaban.download(
            'http://huaban.com/boards/16687763/',
            info_only=True
        )

    def test_instagram(self):
        # Single picture
        instagram.download(
            'https://www.instagram.com/p/Bei7whzgfMq',
            info_only=True
        )
        # Album
        instagram.download(
            'https://www.instagram.com/p/BdZ7sPTgchP/',
            info_only=True
        )
        # Video
        instagram.download(
            'https://www.instagram.com/p/BYQ0PMWlAQY/',
            info_only=True
        )

    @ignore_network_issue
    def test_ixigua(self):
        ixigua.download(
            'https://www.ixigua.com/a6487187567887254029',
            info_only=True
        )
        ixigua.download_playlist(
            'https://www.ixigua.com/c/user/71141690831/',
            info_only=True
        )

    @ignore_network_issue
    def test_yinyuetai(self):
        yinyuetai.download(
            'http://v.yinyuetai.com/video/3148502', info_only=True
        )
        yinyuetai.download(
            'http://v.yinyuetai.com/video/3145394', info_only=True
        )
        yinyuetai.download_playlist(
            'http://v.yinyuetai.com/playlist/397007', info_only=True
        )

    def test_vine(self):
        vine.download('https://vine.co/v/hVVap7prKjY', info_only=True)

    @ignore_network_issue
    def test_iqiyi(self):
        iqiyi.download(
            'http://www.iqiyi.com/v_19rrfl3cy4.html', info_only=True
        )
        iqiyi.download(
            'http://www.iqiyi.com/v_19rrfdpf2k.html', info_only=True
        )

    @ignore_network_issue
    def test_tudou(self):
        tudou.download(
            'http://new-play.tudou.com/v/824775617.html',
            info_only=True,
        )
        tudou.download(
            'https://video.tudou.com/v/XMzM2MTA4NTA3Mg==.html',
            info_only=True,
        )
        tudou.download(
            'http://video.tudou.com/v/XMzM1NTQxMzIyNA==',
            info_only=True,
        )


if __name__ == '__main__':
    unittest.main()
