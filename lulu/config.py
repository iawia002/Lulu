# coding=utf-8

SITES = {
    '163': 'netease',
    '56': 'w56',
    'acfun': 'acfun',
    'archive': 'archive',
    'baidu': 'baidu',
    'bandcamp': 'bandcamp',
    'baomihua': 'baomihua',
    'bcy': 'bcy',
    'bigthink': 'bigthink',
    'bilibili': 'bilibili',
    'cctv': 'cntv',
    'cntv': 'cntv',
    'cbs': 'cbs',
    'coub': 'coub',
    'dailymotion': 'dailymotion',
    'dilidili': 'dilidili',
    'douban': 'douban',
    'douyin': 'douyin',
    'douyu': 'douyutv',
    'ehow': 'ehow',
    'facebook': 'facebook',
    'fantasy': 'fantasy',
    'fc2': 'fc2video',
    'flickr': 'flickr',
    'freesound': 'freesound',
    'fun': 'funshion',
    'google': 'google',
    'giphy': 'giphy',
    'heavy-music': 'heavymusic',
    'huaban': 'huaban',
    'huomao': 'huomaotv',
    'iask': 'sina',
    'icourses': 'icourses',
    'ifeng': 'ifeng',
    'imgur': 'imgur',
    'in': 'alive',
    'infoq': 'infoq',
    'instagram': 'instagram',
    'iqilu': 'iqilu',
    'iqiyi': 'iqiyi',
    'ixigua': 'ixigua',
    'isuntv': 'suntv',
    'joy': 'joy',
    'kankanews': 'bilibili',
    'khanacademy': 'khan',
    'ku6': 'ku6',
    'kuaishou': 'kuaishou',
    'kugou': 'kugou',
    'kuwo': 'kuwo',
    'le': 'le',
    'letv': 'le',
    'lizhi': 'lizhi',
    'longzhu': 'longzhu',
    'magisto': 'magisto',
    'metacafe': 'metacafe',
    'mgtv': 'mgtv',
    'mtv81': 'mtv81',
    'musicplayon': 'musicplayon',
    'naver': 'naver',
    '7gogo': 'nanagogo',
    'nicovideo': 'nicovideo',
    'panda': 'panda',
    'pinterest': 'pinterest',
    'pixivision': 'pixivision',
    'pixnet': 'pixnet',
    'pptv': 'pptv',
    'qingting': 'qingting',
    'qq': 'qq',
    'quanmin': 'quanmin',
    'showroom-live': 'showroom',
    'sina': 'sina',
    'smgbb': 'bilibili',
    'sohu': 'sohu',
    'soundcloud': 'soundcloud',
    'ted': 'ted',
    'theplatform': 'theplatform',
    'tucao': 'tucao',
    'tudou': 'tudou',
    'tumblr': 'tumblr',
    'twimg': 'twitter',
    'twitter': 'twitter',
    'ucas': 'ucas',
    'videomega': 'videomega',
    'vidto': 'vidto',
    'vimeo': 'vimeo',
    'wanmen': 'wanmen',
    'weibo': 'weibo',
    'veoh': 'veoh',
    'vine': 'vine',
    'vk': 'vk',
    'xiami': 'xiami',
    'xiaokaxiu': 'yixia',
    'xiaojiadianvideo': 'fc2video',
    'ximalaya': 'ximalaya',
    'yinyuetai': 'yinyuetai',
    'miaopai': 'yixia',
    'yizhibo': 'yizhibo',
    'youku': 'youku',
    'iwara': 'iwara',
    'youtu': 'youtube',
    'youtube': 'youtube',
    'zhanqi': 'zhanqi',
    '365yg': 'toutiao',
}

FAKE_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',  # noqa
}

FAKE_HEADERS_MOBILE = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',  # noqa
}

# netease
NETEASE_MP3_URL = (
    'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
)
NETEASE_MUSIC_PUBKEY = '010001'
NETEASE_MUSIC_SECKEY = 16 * 'F'
NETEASE_MUSIC_COMMENT_MODULE = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'  # noqa

# YouTube
# YouTube media encoding options, in descending quality order.
# http://en.wikipedia.org/wiki/YouTube#Quality_and_codecs.
# Retrieved July 17, 2014.
YOUTUBE_CODECS = [
    {
        'itag': '38', 'container': 'MP4', 'video_resolution': '3072p',
        'video_encoding': 'H.264', 'video_profile': 'High',
        'video_bitrate': '3.5-5', 'audio_encoding': 'AAC',
        'audio_bitrate': '192',
    },
    # {'itag': '85', 'container': 'MP4', 'video_resolution': '1080p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '3-4', 'audio_encoding': 'AAC', 'audio_bitrate': '192'},  # noqa
    {
        'itag': '46', 'container': 'WebM', 'video_resolution': '1080p',
        'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '',
        'audio_encoding': 'Vorbis', 'audio_bitrate': '192',
    },
    {
        'itag': '37', 'container': 'MP4', 'video_resolution': '1080p',
        'video_encoding': 'H.264', 'video_profile': 'High',
        'video_bitrate': '3-4.3', 'audio_encoding': 'AAC',
        'audio_bitrate': '192',
    },
    # {'itag': '102', 'container': 'WebM', 'video_resolution': '720p', 'video_encoding': 'VP8', 'video_profile': '3D', 'video_bitrate': '', 'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},  # noqa
    {
        'itag': '45', 'container': 'WebM', 'video_resolution': '720p',
        'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '2',
        'audio_encoding': 'Vorbis', 'audio_bitrate': '192',
    },
    # {'itag': '84', 'container': 'MP4', 'video_resolution': '720p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '2-3', 'audio_encoding': 'AAC', 'audio_bitrate': '192'},  # noqa
    {
        'itag': '22', 'container': 'MP4', 'video_resolution': '720p',
        'video_encoding': 'H.264', 'video_profile': 'High',
        'video_bitrate': '2-3', 'audio_encoding': 'AAC',
        'audio_bitrate': '192',
    },
    {
        'itag': '120', 'container': 'FLV', 'video_resolution': '720p',
        'video_encoding': 'H.264', 'video_profile': 'Main@L3.1',
        'video_bitrate': '2', 'audio_encoding': 'AAC',
        'audio_bitrate': '128',
    },  # Live streaming only
    {
        'itag': '44', 'container': 'WebM', 'video_resolution': '480p',
        'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '1',
        'audio_encoding': 'Vorbis', 'audio_bitrate': '128',
    },
    {
        'itag': '35', 'container': 'FLV', 'video_resolution': '480p',
        'video_encoding': 'H.264', 'video_profile': 'Main',
        'video_bitrate': '0.8-1', 'audio_encoding': 'AAC',
        'audio_bitrate': '128',
    },
    # {'itag': '101', 'container': 'WebM', 'video_resolution': '360p', 'video_encoding': 'VP8', 'video_profile': '3D', 'video_bitrate': '', 'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},  # noqa
    # {'itag': '100', 'container': 'WebM', 'video_resolution': '360p', 'video_encoding': 'VP8', 'video_profile': '3D', 'video_bitrate': '', 'audio_encoding': 'Vorbis', 'audio_bitrate': '128'},  # noqa
    {
        'itag': '43', 'container': 'WebM', 'video_resolution': '360p',
        'video_encoding': 'VP8', 'video_profile': '',
        'video_bitrate': '0.5', 'audio_encoding': 'Vorbis',
        'audio_bitrate': '128',
    },
    {
        'itag': '34', 'container': 'FLV', 'video_resolution': '360p',
        'video_encoding': 'H.264', 'video_profile': 'Main',
        'video_bitrate': '0.5', 'audio_encoding': 'AAC',
        'audio_bitrate': '128',
    },
    # {'itag': '82', 'container': 'MP4', 'video_resolution': '360p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '0.5', 'audio_encoding': 'AAC', 'audio_bitrate': '96'},  # noqa
    {
        'itag': '18', 'container': 'MP4', 'video_resolution': '270p/360p',
        'video_encoding': 'H.264', 'video_profile': 'Baseline',
        'video_bitrate': '0.5', 'audio_encoding': 'AAC',
        'audio_bitrate': '96',
    },
    {
        'itag': '6', 'container': 'FLV', 'video_resolution': '270p',
        'video_encoding': 'Sorenson H.263', 'video_profile': '',
        'video_bitrate': '0.8', 'audio_encoding': 'MP3',
        'audio_bitrate': '64',
    },
    # {'itag': '83', 'container': 'MP4', 'video_resolution': '240p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '0.5', 'audio_encoding': 'AAC', 'audio_bitrate': '96'},  # noqa
    {
        'itag': '13', 'container': '3GP', 'video_resolution': '',
        'video_encoding': 'MPEG-4 Visual', 'video_profile': '',
        'video_bitrate': '0.5', 'audio_encoding': 'AAC',
        'audio_bitrate': '',
    },
    {
        'itag': '5', 'container': 'FLV', 'video_resolution': '240p',
        'video_encoding': 'Sorenson H.263', 'video_profile': '',
        'video_bitrate': '0.25', 'audio_encoding': 'MP3',
        'audio_bitrate': '64',
    },
    {
        'itag': '36', 'container': '3GP', 'video_resolution': '240p',
        'video_encoding': 'MPEG-4 Visual', 'video_profile': 'Simple',
        'video_bitrate': '0.175', 'audio_encoding': 'AAC',
        'audio_bitrate': '36',
    },
    {
        'itag': '17', 'container': '3GP', 'video_resolution': '144p',
        'video_encoding': 'MPEG-4 Visual', 'video_profile': 'Simple',
        'video_bitrate': '0.05', 'audio_encoding': 'AAC',
        'audio_bitrate': '24',
    },
]
