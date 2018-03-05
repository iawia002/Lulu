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
        extractors.magisto.download(
            'https://www.magisto.com/album/video/PHkvVlFBA118eX4GDnQncnN7fQ',
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
        extractors.yixia.download(
            'http://m.miaopai.com/show/channel/RjJnaplo7c~T~1BhGrzVWUVKg3dK4'
            'A8wCy~ucg__?from=groupmessage&isappinstalled=0',
            info_only=True
        )
        extractors.yixia.download(
            'http://v.xiaokaxiu.com/v/9xLT7TdMLhGvn0kpRsKydQ__.html',
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
        extractors.bilibili.download_playlist(
            'https://bangumi.bilibili.com/anime/5584', info_only=True
        )
        # All kinds of bangumi urls
        extractors.bilibili.download(
            'http://bangumi.bilibili.com/anime/21542/play#173286',
            info_only=True
        )
        extractors.bilibili.download(
            'https://www.bilibili.com/bangumi/play/ss21542', info_only=True
        )
        extractors.bilibili.download(
            'https://www.bilibili.com/bangumi/play/ss21542#173287',
            info_only=True
        )
        extractors.bilibili.download(
            'https://www.bilibili.com/bangumi/play/ep173288', info_only=True
        )
        # movie
        extractors.bilibili.download(
            'https://www.bilibili.com/bangumi/play/ss12044', info_only=True
        )
        # tv
        extractors.bilibili.download(
            'https://www.bilibili.com/bangumi/play/ep196751/', info_only=True
        )
        extractors.bilibili.download_playlist(
            'https://www.bilibili.com/bangumi/play/ep196751/', info_only=True
        )

    @ignore_network_issue
    def test_douyin(self):
        extractors.douyin.download(
            'https://www.douyin.com/share/video/6492273288897629454',
            info_only=True
        )

    @ignore_network_issue
    def test_weibo(self):
        extractors.weibo.download(
            'https://m.weibo.cn/status/FEFq863WF', info_only=True
        )
        extractors.weibo.download(
            'https://m.weibo.cn/status/4199826726109820', info_only=True
        )
        extractors.weibo.download(
            'https://m.weibo.cn/5762457113/G3cSD7Fby', info_only=True
        )
        extractors.weibo.download(
            'https://m.weibo.cn/status/G3lIbETfF', info_only=True
        )
        extractors.weibo.download(
            'https://weibo.com/tv/v/G3lIbETfF?fid='
            '1034:b91d1ecf44b0e2f18c436d819744b333',
            info_only=True
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
        # qie_video
        extractors.qq.download(
            'http://live.qq.com/video/v/376279',
            info_only=True
        )

    @ignore_network_issue
    def test_acfun(self):
        extractors.acfun.download(
            'http://www.acfun.cn/v/ac4210425', info_only=True
        )

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
            'http://alive.in.th/watch_video.php?v=BKBADG831SOM',
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

    @skipOnCI
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

    def test_vk(self):
        extractors.vk.download(
            'https://vk.com/photo-158176266_456239057',
            info_only=True
        )
        extractors.vk.download(
            'https://vk.com/photo-200_456239105',
            info_only=True
        )
        extractors.vk.download(
            'https://vk.com/video?z=video-74192244_456244018'
            '%2F8ccaec8554ab3864e8%2Fpl_cat_featured',
            info_only=True
        )
        extractors.vk.download(
            'https://vk.com/video-74192244_456244018',
            info_only=True
        )

    @ignore_network_issue
    def test_baomihua(self):
        extractors.baomihua.download(
            'http://video.baomihua.com/v/37305339',
            info_only=True
        )

    def test_bandcamp(self):
        extractors.bandcamp.download(
            'https://radicaldreamland.bandcamp.com/album/'
            'celeste-original-soundtrack',
            info_only=True
        )

    def test_bigthink(self):
        extractors.bigthink.download(
            'http://bigthink.com/playlists/new-voices-in-american-foreign-'
            'policy-charles-koch-foundation',
            info_only=True
        )

    @ignore_network_issue
    def test_cntv(self):
        extractors.cntv.download(
            'http://news.cctv.com/2018/02/09/'
            'ARTIMfB4dxy7AH9ZN8IHCOA2180209.shtml',
            info_only=True
        )
        extractors.cntv.download(
            'http://news.cctv.com/2018/02/09/'
            'ARTIiO6RNQCh1gTSAUOEEvN4180209.shtml',
            info_only=True
        )

    def test_coub(self):
        extractors.coub.download(
            'http://coub.com/view/131ozl',
            info_only=True
        )

    def test_dailymotion(self):
        extractors.dailymotion.download(
            'http://www.dailymotion.com/video/x69g1zc',
            info_only=True
        )

    def test_ehow(self):
        extractors.ehow.download(
            'https://www.ehow.com/video_12340520_fresh-berry-ice-cubes.html',
            info_only=True
        )

    def test_fc2video(self):
        extractors.fc2video.download(
            'http://video.fc2.com/en/content/20151021bTVKnbEw',
            info_only=True
        )

    def test_freesound(self):
        extractors.freesound.download(
            'https://freesound.org/people/crispydinner/sounds/120405/',
            info_only=True
        )

    # @ignore_network_issue
    # def test_funshion(self):
    #     extractors.funshion.download(
    #         'https://www.fun.tv/vplay/v-19729665/',
    #         info_only=True
    #     )
    #     extractors.funshion.download(
    #         'https://www.fun.tv/vplay/g-313897/',
    #         info_only=True
    #     )

    def test_giphy(self):
        extractors.giphy.download(
            'https://giphy.com/gifs/NYFW-nyfw-2016-new-york-fashion-week-'
            'l0MYFI3rPn45greIo',
            info_only=True
        )
        extractors.giphy.download(
            'https://giphy.com/nyfw/past-fashion-weeks/shows/'
            'vivienne-tam-feb-2017',
            info_only=True
        )

    def test_heavymusic(self):
        extractors.heavymusic.download(
            'http://www.heavy-music.ru/?browse&band=0xist&album='
            '(2010)%20-%20Unveiling%20the%20Shadow%20World',
            info_only=True
        )

    @ignore_network_issue
    def test_icourses(self):
        extractors.icourses.download(
            'http://www.icourses.cn/web/sword/portal/videoDetail?courseId='
            '9fe9d456-1327-1000-9193-4876d02411f6#/?resId=d1165ef9-1334-'
            '1000-9014-1d109e90c3cf',
            info_only=True
        )
        extractors.icourses.download(
            'http://www.icourses.cn/web/sword/portal/videoDetail?courseId='
            '168a8f9c-1345-1000-b224-22f745f72788#/?resId=168b110d-1345-1000-'
            'b249-22f745f72788',
            info_only=True
        )
        extractors.icourses.download_playlist(
            'http://www.icourses.cn/web/sword/portal/videoDetail?courseId='
            '9fe9d456-1327-1000-9193-4876d02411f6#/?resId=d1165ef9-1334-'
            '1000-9014-1d109e90c3cf',
            info_only=True
        )

    @ignore_network_issue
    def test_ifeng(self):
        extractors.ifeng.download(
            'http://v.ifeng.com/video_11689002.shtml',
            info_only=True
        )

    def test_iwara(self):
        extractors.iwara.download(
            'http://www.iwara.tv/videos/k09z6iqkrwszz0qyk',
            info_only=True
        )

    @ignore_network_issue
    def test_iqilu(self):
        extractors.iqilu.download(
            'http://v.iqilu.com/sdws/zasd/2018/0209/4508775.html',
            info_only=True
        )

    @ignore_network_issue
    def test_joy(self):
        extractors.joy.download(
            'http://www.joy.cn/videoEntertainment?resourceId=60242908',
            info_only=True
        )

    def test_khan(self):
        extractors.khan.download(
            'https://www.khanacademy.org/computing/computer-programming/'
            'programming/intro-to-programming/v/programming-intro',
            info_only=True
        )

    @ignore_network_issue
    def test_ku6(self):
        extractors.ku6.download(
            'https://www.ku6.com/video/detail?id=9l7XvS7f7vAH7CVcfP7LSioPNSk.',
            info_only=True
        )

    @ignore_network_issue
    def test_kugou(self):
        extractors.kugou.download(
            'http://www.kugou.com/song/#hash=0DBC1E271612559994F48E779A71671E&'
            'album_id=8345464',
            info_only=True
        )
        extractors.kugou.download_playlist(
            'http://www.kugou.com/yy/special/single/244402.html',
            info_only=True
        )
        extractors.kugou.download(
            'http://5sing.kugou.com/fc/16355679.html',
            info_only=True
        )

    @ignore_network_issue
    def test_kuwo(self):
        extractors.kuwo.download(
            'http://www.kuwo.cn/yinyue/6657692',
            info_only=True
        )
        extractors.kuwo.download_playlist(
            'http://yinyue.kuwo.cn/yy/cinfo_3349.htm',
            info_only=True
        )

    @ignore_network_issue
    def test_le(self):
        extractors.le.download(
            'http://www.le.com/ptv/vplay/31375060.html',
            info_only=True
        )
        extractors.le.download(
            'http://www.le.com/ptv/vplay/31342937.html',
            info_only=True
        )

    @ignore_network_issue
    def test_lizhi(self):
        extractors.lizhi.download(
            'http://www.lizhi.fm/549759/2508612053517249030',
            info_only=True
        )

    @ignore_network_issue
    def test_metacafe(self):
        extractors.metacafe.download(
            'http://www.metacafe.com/watch/11629007/overwatch-hero-match-lucio'
            '-trailer-blizzard-entertainment-directors-aaron-keller-chris-metz'
            'en-jeff-kaplan/',
            info_only=True
        )

    @ignore_network_issue
    def test_mgtv(self):
        extractors.mgtv.download(
            'https://www.mgtv.com/b/321502/4280446.html',
            info_only=True
        )
        extractors.mgtv.download(
            'https://www.mgtv.com/l/100016375.html',
            info_only=True
        )

    def test_mtv81(self):
        extractors.mtv81.download(
            'http://www.mtv81.com/videos/the-buzz/suiyoubi-no-campanella-'
            'pumps-pink-red-bull-through-her-veins/',
            info_only=True
        )

    def test_musicplayon(self):
        extractors.musicplayon.download(
            'https://zh.musicplayon.com/Maroon-5-Wait-Video-320200.html',
            info_only=True
        )

    def test_nanagogo(self):
        extractors.nanagogo.download(
            'https://7gogo.jp/akimoto-manatsu/5258',
            info_only=True
        )
        extractors.nanagogo.download(
            'https://7gogo.jp/goto-moe/72696',
            info_only=True
        )

    @ignore_network_issue
    def test_naver(self):
        extractors.naver.download(
            'http://tv.naver.com/v/2694018',
            info_only=True
        )

    def test_pinterest(self):
        extractors.pinterest.download(
            'https://www.pinterest.com/pin/762656518121280263/',
            info_only=True
        )
        extractors.pinterest.download(
            'https://www.pinterest.com/pin/726346246125451851/',
            info_only=True
        )

    @skipOnCI
    def test_pixnet(self):
        extractors.pixnet.download(
            'http://eric6513.pixnet.net/album/video/206644535',
            info_only=True
        )

    @ignore_network_issue
    def test_pptv(self):
        extractors.pptv.download(
            'http://v.pptv.com/show/B20ysRXcF1W4Np4.html',
            info_only=True
        )

    @ignore_network_issue
    def test_qingting(self):
        extractors.qingting.download(
            'http://www.qingting.fm/channels/232855/programs/8160697',
            info_only=True
        )

    @ignore_network_issue
    def test_sina(self):
        extractors.sina.download(
            'http://video.sina.com.cn/view/252618328.html',
            info_only=True
        )

    @ignore_network_issue
    def test_sohu(self):
        extractors.sohu.download(
            'http://my.tv.sohu.com/pl/9392627/98047585.shtml',
            info_only=True
        )

    def test_soundcloud(self):
        extractors.soundcloud.download(
            'https://soundcloud.com/scumgang6ix9ine/keke-ft-fetty-wap-a-boogie'
            '-wit-da-hoodie',
            info_only=True
        )

    def test_twitter(self):
        # Image
        extractors.twitter.download(
            'https://twitter.com/Remembear/status/961045374084448256',
            info_only=True
        )
        # Video
        extractors.twitter.download(
            'https://twitter.com/thisisjohnny/status/952993048207806464',
            info_only=True
        )

    @ignore_network_issue
    def test_ucas(self):
        extractors.ucas.download(
            'http://v.ucas.ac.cn/course/getplaytitle.do?menuCode=2&code=14562'
            '&classcode=1&classid=R5djhgQ26hx1OqPuXf&sectionNumber=23&section'
            'Display=1',
            info_only=True
        )

    def test_veoh(self):
        extractors.veoh.download(
            'http://www.veoh.com/watch/v654486353dnASqzc',
            info_only=True
        )

    def test_vimeo(self):
        extractors.vimeo.download(
            'https://vimeo.com/58388167',
            info_only=True
        )

    @ignore_network_issue
    def test_w56(self):
        extractors.w56.download(
            'http://www.56.com/u98/v_MTQ4OTk3NzI3.html',
            info_only=True
        )

    @skipOnCI
    def test_ximalaya(self):
        extractors.ximalaya.download(
            'http://www.ximalaya.com/24137038/sound/71717551/',
            info_only=True
        )
        extractors.ximalaya.download_playlist(
            'http://www.ximalaya.com/41564736/album/11792141/',
            info_only=True
        )

    @ignore_network_issue
    def test_pixivision(self):
        extractors.pixivision.download(
            'https://www.pixivision.net/zh/a/3244',
            info_only=True
        )

    @ignore_network_issue
    def test_longzhu(self):
        extractors.longzhu.download(
            'http://v.longzhu.com/xiayike233/v/762954',
            info_only=True
        )
        extractors.longzhu.download(
            'http://replay.longzhu.com/v/5669968',
            info_only=True
        )

    @ignore_network_issue
    def test_bcy(self):
        extractors.bcy.download(
            'https://bcy.net/coser/detail/67736/2009414',
            info_only=True
        )
        extractors.bcy.download(
            'https://bcy.net/illust/detail/15294/2077317',
            info_only=True
        )


if __name__ == '__main__':
    unittest.main()
