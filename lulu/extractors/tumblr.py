#!/usr/bin/env python

import re
from urllib import parse
from html import unescape

from lulu.extractors.vine import vine_download
from lulu.extractors.vimeo import vimeo_download
from lulu.extractors.universal import universal_download
from lulu.extractors.dailymotion import dailymotion_download

from lulu.common import (
    match1,
    url_info,
    url_size,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['tumblr_download']
site_info = 'Tumblr.com'


def tumblr_download(
    url, output_dir='.', merge=True, info_only=False, **kwargs
):
    if re.match(r'https?://\d+\.media\.tumblr\.com/', url):
        universal_download(url, output_dir, merge=merge, info_only=info_only)
        return

    html = parse.unquote(get_content(url)).replace('\/', '/')
    feed = match1(
        html, r'<meta property="og:type" content="tumblr-feed:(\w+)" />'
    )

    if feed in ['photo', 'photoset', 'entry'] or feed is None:
        # try to extract photos
        page_title = match1(
            html, r'<meta name="description" content="([^"\n]+)'
        ) or match1(
            html, r'<meta property="og:description" content="([^"\n]+)'
        ) or match1(html, r'<title>([^<\n]*)')
        urls = re.findall(
            r'(https?://[^;"&]+/tumblr_[^;"]+_\d+\.jpg)', html
        ) + re.findall(
            r'(https?://[^;"&]+/tumblr_[^;"]+_\d+\.png)', html
        ) + re.findall(r'(https?://[^;"&]+/tumblr_[^";]+_\d+\.gif)', html)

        tuggles = {}
        for url in urls:
            filename = parse.unquote(url.split('/')[-1])
            title = '.'.join(filename.split('.')[:-1])
            tumblr_id = match1(title, r'^tumblr_(.+)_\d+$')
            quality = int(match1(title, r'^tumblr_.+_(\d+)$'))
            ext = filename.split('.')[-1]
            try:
                size = url_size(url)
                if tumblr_id not in tuggles or tuggles[tumblr_id]['quality'] \
                        < quality:
                    tuggles[tumblr_id] = {
                        'title': title,
                        'url': url,
                        'quality': quality,
                        'ext': ext,
                        'size': size,
                    }
            except Exception:
                pass

        if tuggles:
            size = sum([tuggles[t]['size'] for t in tuggles])
            print_info(site_info, page_title, None, size)

            if not info_only:
                for t in tuggles:
                    title = tuggles[t]['title']
                    ext = tuggles[t]['ext']
                    size = tuggles[t]['size']
                    url = tuggles[t]['url']
                    print_info(site_info, title, ext, size)
                    download_urls(
                        [url], title, ext, size, output_dir=output_dir
                    )
            return

    # feed == 'audio' or feed == 'video' or feed is None
    # try to extract video / audio
    real_url = match1(html, r'source src=\\x22([^\\]+)\\')
    if not real_url:
        real_url = match1(html, r'audio_file=([^&]+)&')
        if real_url:
            real_url = (
                '{}?plead=please-dont-download-this-or-our-lawyers-wont-let-us'
                '-host-audio'.format(real_url)
            )
    if not real_url:
        real_url = match1(html, r'<source src="([^"]*)"')
    if not real_url:
        iframe_url = match1(
            html,
            r'<[^>]+tumblr_video_container[^>]+><iframe[^>]+'
            r'src=[\'"]([^\'"]*)[\'"]'
        )
        if iframe_url:
            iframe_html = get_content(iframe_url)
            real_url = match1(
                iframe_html,
                r'<video[^>]*>[\n ]*<source[^>]+src=[\'"]([^\'"]*)[\'"]'
            )
        else:
            iframe_url = match1(html, r'<iframe[^>]+src=[\'"]([^\'"]*)[\'"]')
            if iframe_url[:2] == '//':
                iframe_url = 'http:' + iframe_url
            if re.search(r'player\.vimeo\.com', iframe_url):
                vimeo_download(
                    iframe_url, output_dir, merge=merge, info_only=info_only,
                    referer='http://tumblr.com/', **kwargs
                )
                return
            elif re.search(r'dailymotion\.com', iframe_url):
                dailymotion_download(
                    iframe_url, output_dir, merge=merge, info_only=info_only,
                    **kwargs
                )
                return
            elif re.search(r'vine\.co', iframe_url):
                vine_download(
                    iframe_url, output_dir, merge=merge, info_only=info_only,
                    **kwargs
                )
                return
            else:
                iframe_html = get_content(iframe_url)
                real_url = match1(iframe_html, r'<source src="([^"]*)"')

    title = unescape(
        match1(
            html, r'<meta property="og:title" content="([^"]*)" />'
        ) or match1(
            html, r'<meta property="og:description" content="([^"]*)" />'
        ) or match1(html, r'<title>([^<\n]*)') or url.split('/')[4]
    ).replace('\n', '')

    _type, ext, size = url_info(real_url)

    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge=merge)


download = tumblr_download
download_playlist = playlist_not_supported(site_info)
