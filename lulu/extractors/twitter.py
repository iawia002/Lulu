#!/usr/bin/env python

import re
import json
from urllib import parse
from html import unescape

from lulu.common import (
    match1,
    get_head,
    urls_size,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.extractors.vine import vine_download


__all__ = ['twitter_download']
site_info = 'Twitter twitter.com'


def extract_m3u(source):
    r1 = get_content(source)
    s1 = re.findall(r'(/ext_tw_video/.*)', r1)
    s1 += re.findall(r'(/amplify_video/.*)', r1)
    r2 = get_content('https://video.twimg.com{}'.format(s1[-1]))
    s2 = re.findall(r'(/ext_tw_video/.*)', r2)
    s2 += re.findall(r'(/amplify_video/.*)', r2)
    return ['https://video.twimg.com{}'.format(i) for i in s2]


def twitter_download(url, info_only=False, **kwargs):
    html = get_content(url)
    screen_name = match1(html, r'data-screen-name="([^"]*)"') or \
        match1(html, r'<meta name="twitter:title" content="([^"]*)"')
    item_id = match1(html, r'data-item-id="([^"]*)"') or \
        match1(html, r'<meta name="twitter:site:id" content="([^"]*)"')
    page_title = '{} [{}]'.format(screen_name, item_id)

    try:  # extract images
        urls = re.findall(
            r'property="og:image"\s*content="([^"]+:large)"', html
        )
        assert urls
        images = []
        for url in urls:
            url = ':'.join(url.split(':')[:-1]) + ':orig'
            filename = parse.unquote(url.split('/')[-1])
            title = '.'.join(filename.split('.')[:-1])
            ext = url.split(':')[-2].split('.')[-1]
            size = int(get_head(url)['Content-Length'])
            images.append({
                'title': title,
                'url': url,
                'ext': ext,
                'size': size
            })
        size = sum([image['size'] for image in images])
        print_info(site_info, page_title, images[0]['ext'], size)

        if not info_only:
            for image in images:
                title = image['title']
                ext = image['ext']
                size = image['size']
                url = image['url']
                print_info(site_info, title, ext, size)
                download_urls([url], title, ext, size, **kwargs)

    except Exception:  # extract video
        # always use i/cards or videos url
        if not re.match(r'https?://twitter.com/i/', url):
            url = match1(
                html, r'<meta\s*property="og:video:url"\s*content="([^"]+)"'
            )
            if not url:
                url = 'https://twitter.com/i/videos/{}'.format(item_id)
            html = get_content(url)

        data_config = match1(html, r'data-config="([^"]*)"') or \
            match1(html, r'data-player-config="([^"]*)"')
        i = json.loads(unescape(data_config))
        if 'video_url' in i:
            source = i['video_url']
            item_id = i['tweet_id']
            page_title = "{} [{}]".format(screen_name, item_id)
        elif 'playlist' in i:
            source = i['playlist'][0]['source']
            if not item_id:
                page_title = i['playlist'][0]['contentId']
        elif 'vmap_url' in i:
            vmap_url = i['vmap_url']
            vmap = get_content(vmap_url)
            source = match1(vmap, r'<MediaFile>\s*<!\[CDATA\[(.*)\]\]>')
            item_id = i['tweet_id']
            page_title = '{} [{}]'.format(screen_name, item_id)
        elif 'scribe_playlist_url' in i:
            scribe_playlist_url = i['scribe_playlist_url']
            return vine_download(
                scribe_playlist_url, info_only=info_only, **kwargs
            )

        try:
            urls = extract_m3u(source)
        except Exception:
            urls = [source]
        size = urls_size(urls)
        mime, ext = 'video/mp4', 'mp4'

        print_info(site_info, page_title, mime, size)
        if not info_only:
            download_urls(urls, page_title, ext, size, **kwargs)


download = twitter_download
download_playlist = playlist_not_supported(site_info)
