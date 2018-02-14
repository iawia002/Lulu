# coding=utf-8

import re
from urllib import parse
from xml.dom.minidom import parseString

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    get_filename,
    download_urls,
    playlist_not_supported,
)
from lulu.util import log


__all__ = ['xiami_download']
site_info = '虾米音乐 xiami.com'


def location_dec(str):
    head = int(str[0])
    str = str[1:]
    rows = head
    cols = int(len(str)/rows) + 1

    out = ''
    full_row = len(str) % head
    for c in range(cols):
        for r in range(rows):
            if c == (cols - 1) and r >= full_row:
                continue
            if r < full_row:
                char = str[r*cols+c]
            else:
                char = str[cols*full_row+(r-full_row)*(cols-1)+c]
            out += char
    return parse.unquote(out).replace('^', '0')


def xiami_download_lyric(lrc_url, file_name, output_dir):
    lrc = get_content(lrc_url)
    filename = get_filename(file_name)
    if len(lrc) > 0:
        with open(
            '{}/{}.lrc'.format(output_dir, filename), 'w', encoding='utf-8'
        ) as x:
            x.write(lrc)


def xiami_download_pic(pic_url, file_name, output_dir):
    pic_url = pic_url.replace('_1', '')
    pos = pic_url.rfind('.')
    ext = pic_url[pos:]
    pic = get_content(pic_url, decoded=False)
    if len(pic) > 0:
        with open(
            '{}/{}{}'.format(output_dir, file_name.replace('/', '-'), ext),
            'wb'
        ) as x:
            x.write(pic)


def xiami_download_song(sid, output_dir='.', info_only=False):
    xml = get_content(
        'http://www.xiami.com/song/playlist/id/{}/object_name/default/'
        'object_id/0'.format(sid)
    )
    doc = parseString(xml)
    i = doc.getElementsByTagName('track')[0]
    artist = i.getElementsByTagName('artist')[0].firstChild.nodeValue
    album_name = i.getElementsByTagName('album_name')[0].firstChild.nodeValue
    song_title = i.getElementsByTagName('name')[0].firstChild.nodeValue
    url = location_dec(
        i.getElementsByTagName('location')[0].firstChild.nodeValue
    )
    try:
        lrc_url = i.getElementsByTagName('lyric')[0].firstChild.nodeValue
    except Exception:
        pass
    type_, ext, size = url_info(url)
    if not ext:
        ext = 'mp3'

    print_info(site_info, song_title, ext, size)
    if not info_only:
        file_name = '{} - {} - {}'.format(song_title, artist, album_name)
        download_urls([url], file_name, ext, size, output_dir)
        try:
            xiami_download_lyric(lrc_url, file_name, output_dir)
        except Exception:
            pass


def xiami_download_showcollect(cid, output_dir='.', info_only=False):
    html = get_content(
        'http://www.xiami.com/song/showcollect/id/{}'.format(cid)
    )
    collect_name = match1(html, r'<title>(.*)</title>')

    xml = get_content(
        'http://www.xiami.com/song/playlist/id/{}/type/3'.format(cid)
    )
    doc = parseString(xml)
    output_dir = '{}/[{}]'.format(output_dir, collect_name)
    tracks = doc.getElementsByTagName('track')
    track_nr = 1
    for i in tracks:
        artist = album_name = song_title = url = ''
        try:
            song_id = i.getElementsByTagName('song_id')[0].firstChild.nodeValue
            artist = i.getElementsByTagName('artist')[0].firstChild.nodeValue
            album_name = i.getElementsByTagName(
                'album_name'
            )[0].firstChild.nodeValue
            song_title = i.getElementsByTagName(
                'title'
            )[0].firstChild.nodeValue
            url = location_dec(
                i.getElementsByTagName('location')[0].firstChild.nodeValue
            )
        except Exception:
            log.e(
                'Song {} failed. [Info Missing] artist: {}, album: {}, title:'
                ' {}, url: {}'.format(
                    song_id, artist, album_name, song_title, url
                )
            )
            continue
        try:
            lrc_url = i.getElementsByTagName('lyric')[0].firstChild.nodeValue
        except Exception:
            pass
        type_, ext, size = url_info(url)
        if not ext:
            ext = 'mp3'

        print_info(site_info, song_title, ext, size)
        if not info_only:
            file_name = '{:0>2d}.{} - {} - {}'.format(
                track_nr, song_title, artist, album_name
            )
            download_urls([url], file_name, ext, size, output_dir)
            try:
                xiami_download_lyric(lrc_url, file_name, output_dir)
            except Exception:
                pass

        track_nr += 1


def xiami_download_album(aid, output_dir='.', info_only=False):
    xml = get_content(
        'http://www.xiami.com/song/playlist/id/{}/type/1'.format(aid)
    )
    album_name = match1(xml, r'<album_name><!\[CDATA\[(.*)\]\]>')
    artist = match1(xml, r'<artist><!\[CDATA\[(.*)\]\]>')
    doc = parseString(xml)
    output_dir = '{}/{} - {}'.format(output_dir, artist, album_name)
    track_list = doc.getElementsByTagName('trackList')[0]
    tracks = track_list.getElementsByTagName('track')
    track_nr = 1
    pic_exist = False
    for i in tracks:
        # in this xml track tag is used for both "track in a trackList" and
        # track no dirty here
        if i.firstChild.nodeValue is not None:
            continue
        song_title = i.getElementsByTagName('songName')[0].firstChild.nodeValue
        url = location_dec(
            i.getElementsByTagName('location')[0].firstChild.nodeValue
        )
        try:
            lrc_url = i.getElementsByTagName('lyric')[0].firstChild.nodeValue
        except Exception:
            pass
        if not pic_exist:
            pic_url = i.getElementsByTagName('pic')[0].firstChild.nodeValue
        type_, ext, size = url_info(url)
        if not ext:
            ext = 'mp3'

        print_info(site_info, song_title, ext, size)
        if not info_only:
            file_name = '{:0>2d}.{}'.format(track_nr, song_title)
            download_urls([url], file_name, ext, size, output_dir)
            try:
                xiami_download_lyric(lrc_url, file_name, output_dir)
            except Exception:
                pass
            if not pic_exist:
                xiami_download_pic(pic_url, 'cover', output_dir)
                pic_exist = True

        track_nr += 1


def xiami_download_mv(url, output_dir='.', merge=True, info_only=False):
    # FIXME: broken merge
    page = get_content(url)
    title = re.findall('<title>([^<]+)', page)[0]
    vid, uid = re.findall(r'vid:"(\d+)",uid:"(\d+)"', page)[0]
    api_url = (
        'http://cloud.video.taobao.com/videoapi/info.php?vid={}&uid={}'.format(
            vid, uid
        )
    )
    result = get_content(api_url)
    doc = parseString(result)
    video_url = doc.getElementsByTagName('video_url')[-1].firstChild.nodeValue
    length = int(doc.getElementsByTagName('length')[-1].firstChild.nodeValue)

    v_urls = []
    k_start = 0
    total_size = 0
    while True:
        k_end = k_start + 20000000
        if k_end >= length:
            k_end = length - 1
        v_url = video_url + '/start_{}/end_{}/1.flv'.format(k_start, k_end)
        try:
            _, ext, size = url_info(v_url)
        except Exception:
            break
        v_urls.append(v_url)
        total_size += size
        k_start = k_end + 1

    print_info(site_info, title, ext, total_size)
    if not info_only:
        download_urls(v_urls, title, ext, total_size, output_dir, merge=merge)


def xiami_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    # albums
    if re.match(r'http://www.xiami.com/album/\d+', url):
        _id = match1(url, r'http://www.xiami.com/album/(\d+)')
        xiami_download_album(_id, output_dir, info_only)
    elif re.match(r'http://www.xiami.com/album/\w+', url):
        page = get_content(url)
        album_id = re.search(
            r'rel="canonical"\s+href="http://www.xiami.com/album/([^"]+)"',
            page
        ).group(1)
        xiami_download_album(album_id, output_dir, info_only)

    # collections
    if re.match(r'http://www.xiami.com/collect/\d+', url):
        _id = match1(url, r'http://www.xiami.com/collect/(\d+)')
        xiami_download_showcollect(_id, output_dir, info_only)

    # single track
    if re.match(r'http://www.xiami.com/song/\d+\b', url):
        _id = match1(url, r'http://www.xiami.com/song/(\d+)')
        xiami_download_song(_id, output_dir, info_only)
    elif re.match(r'http://www.xiami.com/song/\w+', url):
        html = get_content(url)
        _id = match1(
            html, r'rel="canonical" href="http://www.xiami.com/song/([^"]+)"'
        )
        xiami_download_song(_id, output_dir, info_only)

    if re.match('http://www.xiami.com/song/detail/id/\d+', url):
        _id = match1(url, r'http://www.xiami.com/song/detail/id/(\d+)')
        xiami_download_song(_id, output_dir, info_only)

    if re.match('http://www.xiami.com/mv', url):
        xiami_download_mv(url, output_dir, merge=merge, info_only=info_only)


download = xiami_download
download_playlist = playlist_not_supported(site_info)
