# Unmaintained

Sorry for this.

For a similar project that is still actively developed, try Annie: <https://github.com/iawia002/annie>

# Lulu

[![PyPI](https://img.shields.io/pypi/v/lulu.svg)](https://pypi.python.org/pypi/lulu/)
[![Build Status](https://travis-ci.org/iawia002/Lulu.svg?branch=master)](https://travis-ci.org/iawia002/Lulu)
[![Build status](https://ci.appveyor.com/api/projects/status/ph9ypng9g01mdr6d/branch/master?svg=true)](https://ci.appveyor.com/project/iawia002/lulu/branch/master)
[![codecov](https://codecov.io/gh/iawia002/Lulu/branch/master/graph/badge.svg)](https://codecov.io/gh/iawia002/Lulu)

Lulu is a friendly [you-get](https://github.com/soimort/you-get) fork (⏬ Dumb downloader that scrapes the web).


## Why fork?
Faster updates


## Installation
### Prerequisites

The following dependencies are required and must be installed separately.

* **[Python 3.4+](https://www.python.org/downloads/)**
* **[FFmpeg](https://www.ffmpeg.org/)** (strongly recommended) or [Libav](https://libav.org/)
* (Optional) [RTMPDump](https://rtmpdump.mplayerhq.hu/)

### Install via pip

    $ pip3 install lulu

upgrade:

    $ pip3 install -U lulu


## Get Started

Here's how you use `Lulu` to download a video from [Bilibili](https://www.bilibili.com/video/av18295259/):

```console
$ lulu https://www.bilibili.com/video/av18295259/
site:                Bilibili
title:               【中文八级】俄罗斯人的名字超乎你的想象
stream:
    - format:        flv720
      container:     flv
      size:          175.4 MiB (183914793 bytes)
    # download-with: lulu --format=flv720 [URL]

Downloading 【中文八级】俄罗斯人的名字超乎你的想象.flv ...
 100% (175.4/175.4MB) ├████████████████████████████████████████┤[1/1]    3 MB/s

Downloading 【中文八级】俄罗斯人的名字超乎你的想象.cmt.xml ...
```

### Download a video

When you get a video of interest, you might want to use the `--info`/`-i` option to see all available quality and formats:

```
$ lulu -i 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
site:                YouTube
title:               Me at the zoo
streams:             # Available quality and codecs
    [ DEFAULT ] _________________________________
    - itag:          43
      container:     webm
      quality:       medium
      size:          0.5 MiB (564215 bytes)
    # download-with: lulu --itag=43 [URL]

    - itag:          18
      container:     mp4
      quality:       medium
    # download-with: lulu --itag=18 [URL]

    - itag:          5
      container:     flv
      quality:       small
    # download-with: lulu --itag=5 [URL]

    - itag:          36
      container:     3gp
      quality:       small
    # download-with: lulu --itag=36 [URL]

    - itag:          17
      container:     3gp
      quality:       small
    # download-with: lulu --itag=17 [URL]
```

The format marked with `DEFAULT` is the one you will get by default. If that looks cool to you, download it:

```
$ lulu 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
site:                YouTube
title:               Me at the zoo
stream:
    - itag:          43
      container:     webm
      quality:       medium
      size:          0.5 MiB (564215 bytes)
    # download-with: lulu --itag=43 [URL]

Downloading zoo.webm ...
100.0% (  0.5/0.5  MB) ├████████████████████████████████████████┤[1/1]    7 MB/s

Saving Me at the zoo.en.srt ...Done.
```

(If a YouTube video has any closed captions, they will be downloaded together with the video file, in SubRip subtitle format.)

Or, if you prefer another format (mp4), just use whatever the option `lulu` shows to you:

```
$ lulu --itag=18 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

**Note:**

* At this point, format selection has not been generally implemented for most of our supported sites; in that case, the default format to download is the one with the highest quality.
* `ffmpeg` is a required dependency, for downloading and joining videos streamed in multiple parts (e.g. on some sites like Youku), and for YouTube videos of 1080p or high resolution.
* If you don't want `lulu` to join video parts after downloading them, use the `--no-merge`/`-n` option.

### Download anything else

If you already have the URL of the exact resource you want, you can download it directly with:

```
$ lulu https://stallman.org/rms.jpg
Site:       stallman.org
Title:      rms
Type:       JPEG Image (image/jpeg)
Size:       0.06 MiB (66482 Bytes)

Downloading rms.jpg ...
100.0% (  0.1/0.1  MB) ├████████████████████████████████████████┤[1/1]  127 kB/s
```

Otherwise, `lulu` will scrape the web page and try to figure out if there's anything interesting to you:

```
$ lulu http://kopasas.tumblr.com/post/69361932517
Site:       Tumblr.com
Title:      kopasas
Type:       Unknown type (None)
Size:       0.51 MiB (536583 Bytes)

Site:       Tumblr.com
Title:      tumblr_mxhg13jx4n1sftq6do1_1280
Type:       Portable Network Graphics (image/png)
Size:       0.51 MiB (536583 Bytes)

Downloading tumblr_mxhg13jx4n1sftq6do1_1280.png ...
100.0% (  0.5/0.5  MB) ├████████████████████████████████████████┤[1/1]   22 MB/s
```

**Note:**

* This feature is an experimental one and far from perfect. It works best on scraping large-sized images from popular websites like Tumblr and Blogger, but there is really no universal pattern that can apply to any site on the Internet.

### Pause and resume a download

You may use <kbd>Ctrl</kbd>+<kbd>C</kbd> to interrupt a download.

A temporary `.download` file is kept in the output directory. Next time you run `lulu` with the same arguments, the download progress will resume from the last session. In case the file is completely downloaded (the temporary `.download` extension is gone), `lulu` will just skip the download.

To enforce re-downloading, use the `--force`/`-f` option. (**Warning:** doing so will overwrite any existing file or temporary file with the same name!)

### Multi-Thread Download

Use `-T/--thread number` option to enable multithreading to download(only works for multiple-parts video), `number` means how many threads you want to use.

### Proxy settings

You may specify an HTTP proxy for `lulu` to use, via the `--http-proxy`/`-x` option:

```
$ lulu -x 127.0.0.1:8087 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

However, the system proxy setting (i.e. the environment variable `http_proxy`) is applied by default. To disable any proxy, use the `--no-proxy` option.

**Tips:**

* If you need to use proxies a lot (in case your network is blocking certain sites), you might want to use `lulu` with [proxychains](https://github.com/rofl0r/proxychains-ng) and set `alias lulu="proxychains -q lulu"` (in Bash).
* For some websites (e.g. Youku), if you need access to some videos that are only available in mainland China, there is an option of using a specific proxy to extract video information from the site: `--extractor-proxy`/`-y`.

### Load cookies

Not all videos are publicly available to anyone. If you need to log in your account to access something (e.g., a private video), it would be unavoidable to feed the browser cookies to `lulu` via the `--cookies`/`-c` option.

**Note:**

* As of now, we are supporting two formats of browser cookies: Mozilla `cookies.sqlite` and Netscape `cookies.txt`.

### Watch a video

Use the `--player`/`-p` option to feed the video into your media player of choice, e.g. `mplayer` or `vlc`, instead of downloading it:

```
$ lulu -p vlc 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

Or, if you prefer to watch the video in a browser, just without ads or comment section:

```
$ lulu -p chromium 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

**Tips:**

* It is possible to use the `-p` option to start another download manager, e.g., `lulu -p uget-gtk 'https://www.youtube.com/watch?v=jNQXAC9IVRw'`, though they may not play together very well.

### Set the path and name of downloaded file

Use the `--output-dir`/`-o` option to set the path, and `--output-filename`/`-O` to set the name of the downloaded file:

```
$ lulu -o ~/Videos -O zoo.webm 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

**Tips:**

* These options are helpful if you encounter problems with the default video titles, which may contain special characters that do not play well with your current shell / operating system / filesystem.
* These options are also helpful if you write a script to batch download files and put them into designated folders with designated names.

### Reuse extracted data

Use `--url`/`-u` to get a list of downloadable resource URLs extracted from the page. Use `--json` to get an abstract of extracted data in the JSON format.

**Warning:**

* For the time being, this feature has **NOT** been stabilized and the JSON schema may have breaking changes in the future.

### Search on Google Videos and download

You can pass literally anything to `lulu`. If it isn't a valid URL, `lulu` will do a Google search and download the most relevant video for you. (It might not be exactly the thing you wish to see, but still very likely.)

```
$ lulu "Richard Stallman eats"
```


## Supported Sites

| Site | URL | Videos? | Images? | Audios? |
| :--: | :-- | :-----: | :-----: | :-----: |
| **YouTube** | <https://www.youtube.com/>    |✓| | |
| **Twitter** | <https://twitter.com/>        |✓|✓| |
| VK          | <http://vk.com/>              |✓|✓| |
| Vine        | <https://vine.co/>            |✓| | |
| Vimeo       | <https://vimeo.com/>          |✓| | |
| Vidto       | <http://vidto.me/>            |✓| | |
| Videomega   | <http://videomega.tv/>        |✓| | |
| Veoh        | <http://www.veoh.com/>        |✓| | |
| **Tumblr**  | <https://www.tumblr.com/>     |✓|✓|✓|
| TED         | <http://www.ted.com/>         |✓| | |
| SoundCloud  | <https://soundcloud.com/>     | | |✓|
| SHOWROOM    | <https://www.showroom-live.com/> |✓| | |
| Pinterest   | <https://www.pinterest.com/>  | |✓| |
| MusicPlayOn | <http://en.musicplayon.com/>  |✓| | |
| MTV81       | <http://www.mtv81.com/>       |✓| | |
| Metacafe    | <http://www.metacafe.com/>    |✓| | |
| Magisto     | <http://www.magisto.com/>     |✓| | |
| Khan Academy | <https://www.khanacademy.org/> |✓| | |
| Internet Archive | <https://archive.org/>   |✓| | |
| **Instagram** | <https://instagram.com/>    |✓|✓| |
| InfoQ       | <http://www.infoq.com/presentations/> |✓| | |
| Imgur       | <http://imgur.com/>           | |✓| |
| Heavy Music Archive | <http://www.heavy-music.ru/> | | |✓|
| **Google+** | <https://plus.google.com/>    |✓|✓| |
| Freesound   | <http://www.freesound.org/>   | | |✓|
| Flickr      | <https://www.flickr.com/>     |✓|✓| |
| FC2 Video   | <http://video.fc2.com/>       |✓| | |
| Facebook    | <https://www.facebook.com/>   |✓| | |
| eHow        | <http://www.ehow.com/>        |✓| | |
| Dailymotion | <http://www.dailymotion.com/> |✓| | |
| Coub        | <http://coub.com/>            |✓| | |
| CBS         | <http://www.cbs.com/>         |✓| | |
| Bandcamp    | <http://bandcamp.com/>        | | |✓|
| AliveThai   | <http://alive.in.th/>         |✓| | |
| **755<br/>ナナゴーゴー** | <http://7gogo.jp/> |✓|✓| |
| **niconico<br/>ニコニコ動画** | <http://www.nicovideo.jp/> |✓| | |
| **163<br/>网易视频<br/>网易云音乐** | <http://v.163.com/><br/><http://music.163.com/> |✓| |✓|
| 56网     | <http://www.56.com/>           |✓| | |
| **AcFun** | <http://www.acfun.cn/>        |✓| | |
| **Baidu<br/>百度贴吧** | <http://tieba.baidu.com/> |✓|✓| |
| 爆米花网 | <http://www.baomihua.com/>     |✓| | |
| **bilibili<br/>哔哩哔哩** | <http://www.bilibili.com/> |✓| | |
| Dilidili | <http://www.dilidili.com/>     |✓| | |
| 豆瓣     | <http://www.douban.com/>       |✓| | |
| 斗鱼     | <http://www.douyutv.com/>      |✓| | |
| Panda<br/>熊猫 | <http://www.panda.tv/>      |✓| | |
| 凤凰视频 | <http://v.ifeng.com/>          |✓| | |
| 风行网   | <http://www.fun.tv/>           |✓| | |
| iQIYI<br/>爱奇艺 | <http://www.iqiyi.com/> |✓| | |
| 激动网   | <http://www.joy.cn/>           |✓| | |
| 酷6网    | <http://www.ku6.com/>          |✓| | |
| 酷狗音乐 | <http://www.kugou.com/>        | | |✓|
| 酷我音乐 | <http://www.kuwo.cn/>          | | |✓|
| 乐视网   | <http://www.le.com/>           |✓| | |
| 荔枝FM   | <http://www.lizhi.fm/>         | | |✓|
| 秒拍     | <http://www.miaopai.com/>      |✓| | |
| 小咖秀     | <http://xiaokaxiu.com>      |✓| | |
| 痞客邦   | <https://www.pixnet.net/>      |✓| | |
| PPTV聚力 | <http://www.pptv.com/>         |✓| | |
| 齐鲁网   | <http://v.iqilu.com/>          |✓| | |
| QQ<br/>腾讯视频 | <http://v.qq.com/>      |✓| | |
| 企鹅直播 | <http://live.qq.com/>          |✓| | |
| Sina<br/>新浪视频<br/>微博秒拍视频 | <http://video.sina.com.cn/><br/><http://video.weibo.com/> |✓| | |
| Sohu<br/>搜狐视频 | <http://tv.sohu.com/> |✓| | |
| **Tudou<br/>土豆** | <http://www.tudou.com/> |✓| | |
| 虾米     | <http://www.xiami.com/>        |✓| |✓|
| 阳光卫视 | <http://www.isuntv.com/>       |✓| | |
| **音悦Tai** | <http://www.yinyuetai.com/> |✓| | |
| **Youku<br/>优酷** | <http://www.youku.com/> |✓| | |
| 战旗TV   | <http://www.zhanqi.tv/lives>   |✓| | |
| 央视网   | <http://www.cntv.cn/>          |✓| | |
| 花瓣     | <http://huaban.com/>           | |✓| |
| Naver<br/>네이버 | <http://tvcast.naver.com/>     |✓| | |
| 芒果TV   | <http://www.mgtv.com/>         |✓| | |
| 火猫TV   | <http://www.huomao.com/>       |✓| | |
| 全民直播 | <http://www.quanmin.tv/>       |✓| | |
| 阳光宽频网 | <http://www.365yg.com/>      |✓| | |
| 西瓜视频 | <https://www.ixigua.com/>      |✓| | |
| 快手 | <https://www.kuaishou.com/>      |✓|✓| |
| 抖音 | <https://www.douyin.com/>      |✓| | |
| 龙珠直播 | <http://longzhu.com>      |✓| | |
| 半次元 | <https://bcy.net>      | |✓| |
| pixivision | <https://www.pixivision.net>      | |✓| |

For all other sites not on the list, the universal extractor will take care of finding and downloading interesting resources from the page.


## Development

### Preparation

Install [pipenv](https://github.com/pypa/pipenv):

    $ pip3 install pipenv

and [fabric](https://github.com/fabric/fabric) (**Note: fabric doesn't support python3 now, install using pip2**):

    $ pip install fabric

Initialize virtualenv

    $ pipenv --python 3

Install all dependencies:

    $ pipenv install --dev

Use the shell:

    $ pipenv shell

Run the tests:

    $ fab test

### Contributing

Lulu is an open source project and welcome contributions 😉

#### Note

[@iawia002](https://github.com/iawia002) has [pep8](https://www.python.org/dev/peps/pep-0008) obsessive-compulsive disorder, all code must follow [pep8](http://pep8.org) guidelines.

You can use [flake8](https://github.com/PyCQA/flake8) to check the code before submitting.


## Authors

You can find the [list of all contributors](https://github.com/iawia002/Lulu/graphs/contributors) here.

## License

MIT
