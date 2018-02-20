#!/usr/bin/env python

import os
import json
import codecs
import base64
from copy import copy

from lulu import config
from lulu.util import fs
from lulu.extractor import SimpleExtractor
from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    post_content,
    get_location,
    get_filename,
    download_urls,
    playlist_not_supported,
)


__all__ = ['netease_download']
site_info = '163.com'


header = copy(config.FAKE_HEADERS)
header.update({
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
})


class Netease(SimpleExtractor):
    def __init__(self):
        super().__init__()
        self.site_info = site_info
        self.enc_sec_key = self.rsa_encrypt(
            config.NETEASE_MUSIC_SECKEY, config.NETEASE_MUSIC_PUBKEY,
            config.NETEASE_MUSIC_COMMENT_MODULE
        )

    def rsa_encrypt(self, text, pub_key, modulus):
        text = text[::-1]
        rs = int(
            codecs.encode(bytes(text, encoding='utf8'), 'hex'), 16
        )**int(pub_key, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def aes_encrypt(self, text, sec_key):
        from cryptography.hazmat.primitives.ciphers import (
            Cipher, algorithms, modes
        )
        from cryptography.hazmat.backends import default_backend
        backend = default_backend()
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        cipher = Cipher(
            algorithms.AES(sec_key.encode('utf-8')),
            modes.CBC(b'0102030405060708'),
            backend=backend
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(text.encode('utf-8')) \
            + encryptor.finalize()
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def create_params(self, song_id):
        text = '{{"ids":[{}], br:"320000", csrf_token:"csrf"}}'.format(song_id)
        nonce = '0CoJUm6Qyw8W8jud'
        nonce2 = 16 * 'F'
        enc_text = self.aes_encrypt(
            self.aes_encrypt(text, nonce).decode('utf-8'), nonce2
        )
        return enc_text

    def get_mp3_link(self, song_id):
        data = {
            'params': self.create_params(song_id),
            'encSecKey': self.enc_sec_key,
        }
        url = config.NETEASE_MP3_URL
        req = post_content(
            url, headers=header,
            post_data=data, decoded=False
        )
        data = json.loads(req.decode('utf-8'))
        return data['data'][0]['url']

    def extract(self, url, **kwargs):
        if '163.fm' in url:
            url = get_location(url)
        if 'music.163.com' in url:
            self.need_download = False
            self.netease_cloud_music_download(url, **kwargs)
        else:
            html = get_content(url)

            title = match1(html, 'movieDescription=\'([^\']+)\'') or \
                match1(html, '<title>(.+)</title>')

            if title[0] == ' ':
                title = title[1:]

            src = match1(html, r'<source src="([^"]+)"') or \
                match1(html, r'<source type="[^"]+" src="([^"]+)"')

            if src:
                url = src
                _, ext, size = url_info(src)
            else:
                url = (
                    match1(html, r'["\'](.+)-list.m3u8["\']') or
                    match1(html, r'["\'](.+).m3u8["\']')
                ) + '.mp4'
                _, _, size = url_info(url)
                ext = 'mp4'

            return {
                'urls': [url],
                'title': title,
                'file_format': ext,
                'size': size,
            }

    def netease_cloud_music_download(
        self, url, output_dir='.', info_only=False, **kwargs
    ):
        rid = match1(url, r'\Wid=(.*)')
        if rid is None:
            rid = match1(url, r'/(\d+)/?')
        if 'album' in url:
            j = json.loads(get_content(
                'http://music.163.com/api/album/{}?id={}&csrf_token='.format(
                    rid, rid
                ),
                headers=header
            ))

            artist_name = j['album']['artists'][0]['name']
            album_name = j['album']['name'].strip()
            new_dir = output_dir + '/' + fs.legitimize(
                '{} - {}'.format(artist_name, album_name)
            )
            if not info_only:
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
                cover_url = j['album']['picUrl']
                download_urls([cover_url], 'cover', 'jpg', 0, new_dir)

            for song in j['album']['songs']:
                self.netease_song_download(
                    song, output_dir=new_dir, info_only=info_only
                )
                # download lyrics
                self.netease_lyric_download(
                    song, output_dir=new_dir, info_only=info_only, **kwargs
                )

        elif 'playlist' in url:
            j = json.loads(get_content(
                'http://music.163.com/api/playlist/detail?'
                'id={}&csrf_token='.format(rid),
                headers=header
            ))
            new_dir = output_dir + '/' + fs.legitimize(j['result']['name'])
            if not info_only:
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
                cover_url = j['result']['coverImgUrl']
                download_urls([cover_url], 'cover', 'jpg', 0, new_dir)

            prefix_width = len(str(len(j['result']['tracks'])))
            for n, song in enumerate(j['result']['tracks']):
                playlist_prefix = '{:0>{}d}_'.format(n, prefix_width)
                self.netease_song_download(
                    song, output_dir=new_dir, info_only=info_only,
                    playlist_prefix=playlist_prefix
                )
                # download lyrics
                self.netease_lyric_download(
                    song, output_dir=new_dir,
                    info_only=info_only, playlist_prefix=playlist_prefix,
                    **kwargs
                )

        elif 'song' in url:
            j = json.loads(get_content(
                'http://music.163.com/api/song/detail/?'
                'id={}&ids=[{}]&csrf_token='.format(rid, rid),
                headers=header
            ))
            song = j['songs'][0]
            self.netease_song_download(
                song, output_dir=output_dir, info_only=info_only
            )
            # download lyrics
            self.netease_lyric_download(
                song, output_dir=output_dir, info_only=info_only, **kwargs
            )

        elif 'program' in url:
            j = json.loads(get_content(
                'http://music.163.com/api/dj/program/detail/?'
                'id={}&ids=[{}]&csrf_token='.format(rid, rid),
                headers=header
            ))
            self.netease_song_download(
                j['program']['mainSong'], output_dir=output_dir,
                info_only=info_only
            )

        elif 'radio' in url:
            j = json.loads(get_content(
                'http://music.163.com/api/dj/program/byradio/?'
                'radioId={}&ids=[{}]&csrf_token='.format(rid, rid),
                headers=header
            ))
            for i in j['programs']:
                self.netease_song_download(
                    i['mainSong'], output_dir=output_dir, info_only=info_only
                )

        elif 'mv' in url:
            j = json.loads(get_content(
                'http://music.163.com/api/mv/detail/?'
                'id={}&ids=[{}]&csrf_token='.format(rid, rid),
                headers=header
            ))
            self.netease_video_download(
                j['data'], output_dir=output_dir, info_only=info_only
            )

    def netease_lyric_download(
        self, song, output_dir, info_only, playlist_prefix='', **kwargs
    ):
        if info_only or not kwargs.get('caption'):
            return

        data = json.loads(get_content(
            'http://music.163.com/api/song/lyric/?'
            'id={}&lv=-1&csrf_token='.format(song['id']),
            headers={'Referer': 'http://music.163.com/'}
        ))
        title = '{}{}. {}'.format(
            playlist_prefix, song['position'], song['name']
        )
        filename = '{}.lrc'.format(get_filename(title))
        print('Saving {} ...'.format(filename), end='', flush=True)
        with open(
            os.path.join(output_dir, filename), 'w', encoding='utf-8'
        ) as x:
            x.write(data['lrc']['lyric'])
            print('Done.')

    def netease_video_download(self, vinfo, output_dir, info_only):
        title = '{} - {}'.format(vinfo['name'], vinfo['artistName'])
        url_best = sorted(
            vinfo['brs'].items(), reverse=True, key=lambda x: int(x[0])
        )[0][1]
        self.netease_download_common(
            title, url_best, output_dir=output_dir, info_only=info_only
        )

    def netease_song_download(
        self, song, output_dir, info_only, playlist_prefix=''
    ):
        title = '{}{}. {}'.format(
            playlist_prefix, song['position'], song['name']
        )
        url_best = self.get_mp3_link(song['id'])
        self.netease_download_common(
            title, url_best, output_dir=output_dir, info_only=info_only
        )

    def netease_download_common(self, title, url_best, output_dir, info_only):
        songtype, ext, size = url_info(url_best)
        print_info(site_info, title, songtype, size)
        if not info_only:
            download_urls([url_best], title, ext, size, output_dir)


download = netease_download = Netease()
download_playlist = playlist_not_supported(site_info)
