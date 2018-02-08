#!/usr/bin/env python

import unittest

from tests.util import (
    skipOnCI,
    skipOnAppVeyor,
    ignore_network_issue,
)
from lulu import extractors
from lulu.common import any_download_playlist


class TestExtractors(unittest.TestCase):
    def test_imgur(self):
        extractors.imgur.download('http://imgur.com/WVLk5nD', info_only=True)
        extractors.imgur.download(
            'http://imgur.com/gallery/WVLk5nD', info_only=True
        )

    def test_magisto(self):
        extractors.magisto.download(
            'http://www.magisto.com/album/video/f3x9AAQORAkfDnIFDA',
            info_only=True
        )

    def test_youtube(self):
        extractors.youtube.download(
            'http://www.youtube.com/watch?v=pzKerr0JIPA', info_only=True
        )
        extractors.youtube.download(
            'http://youtu.be/pzKerr0JIPA', info_only=True
        )
        extractors.youtube.download(
            'http://www.youtube.com/attribution_link?u=/watch?'
            'v%3DldAKIzq7bvs%26feature%3Dshare',
            info_only=True
        )
        extractors.youtube.download(
            'https://www.youtube.com/watch?v=Gnbch2osEeo', info_only=True
        )

    @skipOnAppVeyor
    @ignore_network_issue
    def test_yixia(self):
        extractors.yixia.download(
            'http://m.miaopai.com/show/channel/'
            'vlvreCo4OZiNdk5Jn1WvdopmAvdIJwi8',
            info_only=True
        )
        extractors.yixia.download(
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
        extractors.bilibili.download(
            'https://www.bilibili.com/video/av16907446/', info_only=True
        )
        extractors.bilibili.download(
            'https://www.bilibili.com/video/av13228063/', info_only=True
        )
        extractors.bilibili.download(
            'https://www.bilibili.com/video/av18764071/', info_only=True
        )
        extractors.bilibili.download(
            'https://www.bilibili.com/bangumi/play/ep113875', info_only=True
        )
        extractors.bilibili.download(
            'https://www.bilibili.com/bangumi/play/ep191521', info_only=True
        )

    @ignore_network_issue
    def test_douyin(self):
        extractors.douyin.download(
            'https://www.douyin.com/share/video/6492273288897629454',
            info_only=True
        )
        extractors.douyin.download(
            'https://www.douyin.com/share/video/6511578018618543368',
            info_only=True
        )

    @ignore_network_issue
    def test_weibo(self):
        extractors.miaopai.download(
            'https://m.weibo.cn/status/FEFq863WF', info_only=True
        )
        extractors.miaopai.download(
            'https://m.weibo.cn/status/4199826726109820', info_only=True
        )

    @skipOnCI
    def test_netease(self):
        # failed on travis, don't know why, maybe ip issue?
        extractors.netease.download(
            'http://music.163.com/#/album?id=35757233', info_only=True
        )
        extractors.netease.download(
            'http://music.163.com/#/song?id=490602750', info_only=True
        )

    @ignore_network_issue
    def test_youku(self):
        extractors.youku.download(
            'http://v.youku.com/v_show/id_XMzMzMDk5MzcyNA==.html',
            info_only=True
        )
        extractors.youku.download(
            'http://v.youku.com/v_show/id_XMzI2NTUyOTIxMg==.html',
            info_only=True
        )

    @ignore_network_issue
    def test_qq(self):
        extractors.qq.download(
            'https://v.qq.com/x/page/n0528cwq4xr.html', info_only=True
        )
        extractors.qq.download(
            'https://v.qq.com/x/cover/ps6mnfqyrfo7es3/q0181hpdvo5.html?',
            info_only=True
        )
        extractors.qq.download(
            'http://v.qq.com/cover/p/ps6mnfqyrfo7es3.html?vid=q0181hpdvo5',
            info_only=True
        )
        extractors.qq.download(
            'https://v.qq.com/x/cover/9hpjiv5fhiyn86u/t0522x58xma.html',
            info_only=True
        )

    # @ignore_network_issue
    # def test_acfun(self):
    #     acfun.download('http://www.acfun.cn/v/ac4209715', info_only=True)
    #     acfun.download('http://www.acfun.cn/v/ac4210425', info_only=True)

    @ignore_network_issue
    def test_kuaishou(self):
        extractors.kuaishou.download(
            'https://www.kuaishou.com/photo/84224949/4007135407',
            info_only=True
        )
        extractors.kuaishou.download(
            'https://www.kuaishou.com/photo/84224949/4267454322',
            info_only=True
        )

    @ignore_network_issue
    def test_huaban(self):
        extractors.huaban.download(
            'http://huaban.com/boards/16687763/',
            info_only=True
        )

    def test_instagram(self):
        # Single picture
        extractors.instagram.download(
            'https://www.instagram.com/p/Bei7whzgfMq',
            info_only=True
        )
        # Album
        extractors.instagram.download(
            'https://www.instagram.com/p/BdZ7sPTgchP/',
            info_only=True
        )
        # Video
        extractors.instagram.download(
            'https://www.instagram.com/p/BYQ0PMWlAQY/',
            info_only=True
        )

    @skipOnCI
    @ignore_network_issue
    def test_ixigua(self):
        extractors.ixigua.download(
            'https://www.ixigua.com/a6487187567887254029',
            info_only=True
        )
        extractors.ixigua.download_playlist(
            'https://www.ixigua.com/c/user/71141690831/',
            info_only=True
        )

    @ignore_network_issue
    def test_yinyuetai(self):
        extractors.yinyuetai.download(
            'http://v.yinyuetai.com/video/3148502', info_only=True
        )
        extractors.yinyuetai.download(
            'http://v.yinyuetai.com/video/3145394', info_only=True
        )
        extractors.yinyuetai.download_playlist(
            'http://v.yinyuetai.com/playlist/397007', info_only=True
        )

    def test_vine(self):
        extractors.vine.download(
            'https://vine.co/v/hVVap7prKjY', info_only=True
        )

    @skipOnCI
    def test_iqiyi(self):
        extractors.iqiyi.download(
            'http://www.iqiyi.com/v_19rrfl3cy4.html', info_only=True
        )
        extractors.iqiyi.download(
            'http://www.iqiyi.com/v_19rrfdpf2k.html', info_only=True
        )

    @ignore_network_issue
    def test_tudou(self):
        extractors.tudou.download(
            'http://new-play.tudou.com/v/824775617.html',
            info_only=True,
        )
        extractors.tudou.download(
            'https://video.tudou.com/v/XMzM2MTA4NTA3Mg==.html',
            info_only=True,
        )
        extractors.tudou.download(
            'http://video.tudou.com/v/XMzM1NTQxMzIyNA==',
            info_only=True,
        )

    @ignore_network_issue
    def test_douban(self):
        extractors.douban.download(
            'https://movie.douban.com/trailer/226557/#content', info_only=True
        )
        extractors.douban.download_playlist(
            'https://movie.douban.com/trailer/226557/#content', info_only=True
        )

    def test_tumblr(self):
        extractors.tumblr.download(
            'http://fuckyeah-fx.tumblr.com/post/170392654141/'
            '180202-%E5%AE%8B%E8%8C%9C',
            info_only=True
        )
        extractors.tumblr.download(
            'https://outdoorspastelnature.tumblr.com/post/170380315768/'
            'feel-at-peace',
            info_only=True
        )

    @skipOnCI
    def test_baidu(self):
        extractors.baidu.download(
            'http://music.baidu.com/song/569080829', info_only=True
        )
        extractors.baidu.download(
            'http://music.baidu.com/album/245838807', info_only=True
        )

    def test_facebook(self):
        extractors.facebook.download(
            'https://www.facebook.com/JackyardsCovers/videos/'
            'vb.267832806658747/1215502888558396/',
            info_only=True
        )

    @ignore_network_issue
    def test_zhanqi(self):
        extractors.zhanqi.download(
            'https://www.zhanqi.tv/videos/Lyingman/2017/01/182308.html',
            info_only=True
        )
        extractors.zhanqi.download(
            'https://www.zhanqi.tv/v2/videos/215593.html',
            info_only=True
        )

    @skipOnCI
    def test_dilidili(self):
        extractors.dilidili.download(
            'http://www.dilidili.wang/watch3/46604/', info_only=True
        )
        extractors.dilidili.download(
            'http://www.dilidili.wang/watch/30758/', info_only=True
        )

    @ignore_network_issue
    def test_douyutv(self):
        extractors.douyutv.download(
            'https://v.douyu.com/show/9DO84vrw2nk7edGr', info_only=True
        )

    def test_flickr(self):
        extractors.flickr.download(
            'https://www.flickr.com/photos/albertdros/33589584740',
            info_only=True
        )
        extractors.flickr.download(
            'https://www.flickr.com/photos/albertdros/33167569260',
            info_only=True
        )

    def test_alive(self):
        extractors.alive.download(
            'http://alive.in.th/watch_video.php?v=8O2DDY6B23HG',
            info_only=True
        )

    def test_archive(self):
        extractors.archive.download(
            'https://archive.org/details/tjdeebok',
            info_only=True
        )
        extractors.archive.download(
            'https://archive.org/details/bt2005-10-26.flac16',
            info_only=True
        )

    def test_cbs(self):
        extractors.cbs.download(
            'http://www.cbs.com/shows/bull/video/'
            'YUS0W1neCNs28u6942vJypYoOPQzgJJ_/bull-keep-your-friends-close/',
            info_only=True
        )

    def test_ted(self):
        extractors.ted.download(
            'https://www.ted.com/talks/'
            'su_kahumbu_how_we_can_help_hungry_kids_one_text_at_a_time',
            info_only=True
        )

    @skipOnCI
    def test_infoq(self):
        extractors.infoq.download(
            'http://www.infoq.com/cn/presentations/from-micro-service-to-'
            'serverless-architecture?utm_source=infoq&utm_medium=videos_'
            'homepage&utm_campaign=videos_row1',
            info_only=True
        )


if __name__ == '__main__':
    unittest.main()
