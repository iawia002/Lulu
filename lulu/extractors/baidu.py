#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import time
from urllib import (
    parse,
    request,
)

from lulu.common import (
    match1,
    ungzip,
    cookies,
    url_info,
    print_info,
    get_content,
    post_content,
    download_urls,
    playlist_not_supported,
)
from lulu.config import FAKE_HEADERS
from lulu.util.parser import get_parser
from lulu.extractors.embed import embed_download


__all__ = ['baidu_download']
site_info = '百度 baidu.com'


def baidu_get_song_data(sid):
    data = json.loads(get_content(
        'http://music.baidu.com/data/music/fmlink?songIds={}'.format(sid)
    ))['data']

    if data['xcode'] != '':
        # inside china mainland
        return data['songList'][0]
    else:
        # outside china mainland
        return None


def baidu_download_song(sid, output_dir='.', merge=True, info_only=False):
    data = baidu_get_song_data(sid)
    if data is not None:
        url = data['songLink']
        title = data['songName']
        artist = data['artistName']
        # album = data['albumName']
        lrc = data['lrcLink']
        file_name = '{} - {}'.format(title, artist)
    else:
        html = get_content('http://music.baidu.com/song/{}'.format(sid))
        url = match1(html, r'data_url="([^"]+)"')
        title = match1(html, r'data_name="([^"]+)"')
        file_name = title

    _type, ext, size = url_info(url, faker=True)
    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls(
            [url], file_name, ext, size, output_dir, merge=merge, faker=True
        )

    try:
        _type, ext, size = url_info(lrc, faker=True)
        print_info(site_info, title, _type, size)
        if not info_only:
            download_urls([lrc], file_name, ext, size, output_dir, faker=True)
    except Exception:
        pass


def baidu_download_album(aid, output_dir='.', merge=True, info_only=False):
    html = get_content('http://music.baidu.com/album/{}'.format(aid))
    parser = get_parser(html)
    album_name = parser.find('h2', class_='album-name').text
    artist = parser.find('span', class_='author_list')['title']
    output_dir = '{}/{} - {}'.format(output_dir, artist, album_name)
    ids = json.loads(
        match1(
            html, r'<span class="album-add" data-adddata=\'(.+?)\'>'
        ).replace('&quot', '').replace(';', '"')
    )['ids']
    track_nr = 1
    for _id in ids:
        song_data = baidu_get_song_data(_id)
        song_url = song_data['songLink']
        song_title = song_data['songName']
        song_lrc = song_data['lrcLink']
        file_name = '{:0>2d}.{}'.format(track_nr, song_title)

        _type, ext, size = url_info(song_url, faker=True)
        print_info(site_info, song_title, _type, size)
        if not info_only:
            download_urls(
                [song_url], file_name, ext, size, output_dir, merge=merge,
                faker=True
            )
        if song_lrc:
            _type, ext, size = url_info(song_lrc, faker=True)
            print_info(site_info, song_title, _type, size)
            if not info_only:
                download_urls(
                    [song_lrc], file_name, ext, size, output_dir, faker=True
                )

        track_nr += 1


def baidu_download(
    url, output_dir='.', stream_type=None, merge=True, info_only=False,
    **kwargs
):
    if re.match(r'https?://pan.baidu.com', url):
        real_url, title, ext, size = baidu_pan_download(url)
        print_info('百度网盘', title, ext, size)
        if not info_only:
            print('Hold on...')
            time.sleep(5)
            download_urls(
                [real_url], title, ext, size, output_dir, url, merge=merge,
                faker=True
            )
    elif re.match(r'http://music.baidu.com/album/\d+', url):
        _id = match1(url, r'http://music.baidu.com/album/(\d+)')
        baidu_download_album(_id, output_dir, merge, info_only)

    elif re.match('http://music.baidu.com/song/\d+', url):
        _id = match1(url, r'http://music.baidu.com/song/(\d+)')
        baidu_download_song(_id, output_dir, merge, info_only)

    elif re.match('http://tieba.baidu.com/', url):
        try:
            # embedded videos
            embed_download(url, output_dir, merge=merge, info_only=info_only)
        except Exception:
            # images
            html = get_content(url)
            title = match1(html, r'title:"([^"]+)"')

            items = re.findall(
                r'//imgsrc.baidu.com/forum/w[^"]+/([^/"]+)', html
            )
            urls = [
                'http://imgsrc.baidu.com/forum/pic/item/{}'.format(i)
                for i in set(items)
            ]

            # handle albums
            kw = match1(html, r'kw=([^&]+)') or match1(html, r"kw:'([^']+)'")
            tid = match1(html, r'tid=(\d+)') or match1(html, r"tid:'([^']+)'")
            album_url = (
                'http://tieba.baidu.com/photo/g/bw/picture/list?'
                'kw={}&tid={}&pe={}'.format(kw, tid, 1000)
            )
            album_info = json.loads(get_content(album_url))
            for i in album_info['data']['pic_list']:
                urls.append(
                    'http://imgsrc.baidu.com/forum/pic/item/{}{}'.format(
                        i['pic_id'], '.jpg'
                    )
                )

            ext = 'jpg'
            size = float('Inf')
            print_info(site_info, title, ext, size)

            if not info_only:
                download_urls(
                    urls, title, ext, size, output_dir=output_dir, merge=False
                )


def baidu_pan_download(url):
    errno_patt = r'errno":([^"]+),'
    refer_url = ''
    fake_headers = FAKE_HEADERS.copy()
    fake_headers.update({
        'Host': 'pan.baidu.com',
        'Origin': 'http://pan.baidu.com',
        'Referer': refer_url,
    })
    if cookies:
        print('Use user specified cookies')
    else:
        print('Generating cookies...')
        fake_headers['Cookie'] = baidu_pan_gen_cookies(url)
    refer_url = 'http://pan.baidu.com'
    html = get_content(url, fake_headers, decoded=True)
    isprotected = False
    sign, timestamp, bdstoken, appid, primary_id, fs_id, uk = baidu_pan_parse(
        html
    )
    if sign is None:
        if re.findall(r'verify-property', html):
            isprotected = True
            sign, timestamp, bdstoken, appid, primary_id, fs_id, uk, \
                fake_headers, psk = baidu_pan_protected_share(url)
        if not isprotected:
            raise AssertionError('Share not found or canceled: {}'.format(url))
    if bdstoken is None:
        bdstoken = ''
    if not isprotected:
        sign, timestamp, bdstoken, appid, primary_id, fs_id, \
            uk = baidu_pan_parse(html)
    request_url = (
        'http://pan.baidu.com/api/sharedownload?sign={}&timestamp={}&'
        'bdstoken={}&channel=chunlei&clienttype=0&web=1&app_id={}'.format(
            sign, timestamp, bdstoken, appid
        )
    )
    refer_url = url
    post_data = {
        'encrypt': 0,
        'product': 'share',
        'uk': uk,
        'primaryid': primary_id,
        'fid_list': '[{}]'.format(fs_id)
    }
    if isprotected:
        post_data['sekey'] = psk
    response_content = post_content(request_url, fake_headers, post_data, True)
    errno = match1(response_content, errno_patt)
    if errno != '0':
        raise AssertionError(
            'Server refused to provide download link! (Errno:{})'.format(errno)
        )
    real_url = match1(response_content, r'dlink":"([^"]+)"').replace(
        '\\/', '/'
    )
    title = match1(
        response_content, r'server_filename":"([^"]+)"'
    )
    assert real_url
    _type, ext, size = url_info(real_url, faker=True)
    title_wrapped = json.loads(
        '{{"wrapper":"{}"}}'.format(title)
    )  # \u4ecb\u7ecd -> 介绍
    title = title_wrapped['wrapper']
    return real_url, title, ext, size


def baidu_pan_parse(html):
    sign_patt = r'sign":"([^"]+)"'
    timestamp_patt = r'timestamp":([^"]+),'
    appid_patt = r'app_id":"([^"]+)"'
    bdstoken_patt = r'bdstoken":"([^"]+)"'
    fs_id_patt = r'fs_id":([^"]+),'
    uk_patt = r'uk":([^"]+),'
    # errno_patt = r'errno":([^"]+),'
    primary_id_patt = r'shareid":([^"]+),'
    sign = match1(html, sign_patt)
    timestamp = match1(html, timestamp_patt)
    appid = match1(html, appid_patt)
    bdstoken = match1(html, bdstoken_patt)
    fs_id = match1(html, fs_id_patt)
    uk = match1(html, uk_patt)
    primary_id = match1(html, primary_id_patt)
    return sign, timestamp, bdstoken, appid, primary_id, fs_id, uk


def baidu_pan_gen_cookies(url, post_data=None):
    from http import cookiejar
    cookiejar = cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cookiejar))
    opener.open('http://pan.baidu.com')
    if post_data is not None:
        opener.open(url, bytes(parse.urlencode(post_data), 'utf-8'))
    return cookjar2hdr(cookiejar)


def baidu_pan_protected_share(url):
    print('This share is protected by password!')
    inpwd = input('Please provide unlock password: ')
    inpwd = inpwd.replace(' ', '').replace('\t', '')
    print('Please wait...')
    post_pwd = {
        'pwd': inpwd,
        'vcode': None,
        'vstr': None
    }
    from http import cookiejar
    import time
    cookiejar = cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cookiejar))
    resp = opener.open('http://pan.baidu.com')
    resp = opener.open(url)
    init_url = resp.geturl()
    verify_url = (
        'http://pan.baidu.com/share/verify?{}&t={}&channel=chunlei&'
        'clienttype=0&web=1'.format(
            init_url.split('?', 1)[1], int(time.time())
        )
    )
    refer_url = init_url
    fake_headers = FAKE_HEADERS.copy()
    fake_headers.update({
        'Host': 'pan.baidu.com',
        'Origin': 'http://pan.baidu.com',
        'Referer': refer_url,
    })
    opener.addheaders = dict2triplet(fake_headers)
    pwd_resp = opener.open(
        verify_url, bytes(parse.urlencode(post_pwd), 'utf-8')
    )
    pwd_resp_str = ungzip(pwd_resp.read()).decode('utf-8')
    pwd_res = json.loads(pwd_resp_str)
    if pwd_res['errno'] != 0:
        raise AssertionError(
            'Server returned an error: {} (Incorrect password?)'.format(
                pwd_res['errno']
            )
        )
    pg_resp = opener.open(
        'http://pan.baidu.com/share/link?{}'.format(init_url.split('?', 1)[1])
    )
    content = ungzip(pg_resp.read()).decode('utf-8')
    sign, timestamp, bdstoken, appid, primary_id, fs_id, uk = baidu_pan_parse(
        content
    )
    psk = query_cookiejar(cookiejar, 'BDCLND')
    psk = parse.unquote(psk)
    fake_headers['Cookie'] = cookjar2hdr(cookiejar)
    return (
        sign, timestamp, bdstoken, appid, primary_id, fs_id, uk,
        fake_headers, psk
    )


def cookjar2hdr(cookiejar):
    cookie_str = ''
    for i in cookiejar:
        cookie_str = cookie_str + i.name + '=' + i.value + ';'
    return cookie_str[:-1]


def query_cookiejar(cookiejar, name):
    for i in cookiejar:
        if i.name == name:
            return i.value


def dict2triplet(dictin):
    out_triplet = []
    for i in dictin:
        out_triplet.append((i, dictin[i]))
    return out_triplet


download = baidu_download
download_playlist = playlist_not_supported(site_info)
