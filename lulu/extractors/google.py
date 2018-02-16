#!/usr/bin/env python

import re
from html import unescape
from urllib import (
    parse,
    request,
)

from lulu.common import (
    match1,
    url_info,
    unicodize,
    print_info,
    get_content,
    get_location,
    download_urls,
    playlist_not_supported,
)
from lulu.config import YOUTUBE_CODECS


__all__ = ['google_download']
site_info = 'Google google.com'


fmt_level = dict(zip(
    [str(codec['itag']) for codec in YOUTUBE_CODECS],
    range(len(YOUTUBE_CODECS))
))


def google_download(url, info_only=False, **kwargs):
    # Percent-encoding Unicode URL
    url = parse.quote(url, safe=':/+%?=')

    service = url.split('/')[2].split('.')[0]

    if service == 'plus':  # Google Plus

        # attempt to extract images first
        # TBD: posts with > 4 images
        # TBD: album links
        html = get_content(parse.unquote(url))
        real_urls = []
        for src in re.findall(r'src="([^"]+)"[^>]*itemprop="image"', html):
            t = src.split('/')
            t[0], t[-2] = t[0] or 'https:', 's0-d'
            u = '/'.join(t)
            real_urls.append(u)
        if not real_urls:
            real_urls = [
                match1(html, r'<meta property="og:image" content="([^"]+)')
            ]
            real_urls = [re.sub(r'w\d+-h\d+-p', 's0', u) for u in real_urls]
        post_date = match1(html, r'"?(20\d\d[-/]?[01]\d[-/]?[0123]\d)"?')
        post_id = match1(html, r'/posts/([^"]+)')
        title = '{}_{}'.format(post_date, post_id)

        try:
            url = 'https://plus.google.com/{}'.format(
                match1(html, r'(photos/\d+/albums/\d+/\d+)\?authkey')
            )
            html = get_content(url)
            temp = re.findall(r'\[(\d+),\d+,\d+,"([^"]+)"\]', html)
            temp = sorted(temp, key=lambda x: fmt_level[x[0]])
            urls = [unicodize(i[1]) for i in temp if i[0] == temp[0][0]]
            assert urls
            real_urls = urls  # Look ma, there's really a video!

            post_url = match1(
                html, r'"(https://plus.google.com/[^/]+/posts/[^"]*)"'
            )
            post_author = match1(post_url, r'/\+([^/]+)/posts')
            if post_author:
                post_url = 'https://plus.google.com/+{}/posts/{}'.format(
                    parse.quote(post_author), match1(post_url, r'posts/(.+)')
                )
            post_html = get_content(post_url)
            title = match1(post_html, r'<title[^>]*>([^<\n]+)')
        except Exception:
            pass

        for i, real_url in enumerate(real_urls):
            title_i = '{}[{}]'.format(title, i) if len(real_urls) > 1 \
                else title
            _, ext, size = url_info(real_url)
            if ext is None:
                ext = 'mp4'

            print_info(site_info, title_i, ext, size)
            if not info_only:
                download_urls([real_url], title_i, ext, size, **kwargs)

    elif service in ['docs', 'drive']:  # Google Docs
        html = get_content(url)

        title = match1(html, r'"title":"([^"]*)"') or match1(
            html, r'<meta itemprop="name" content="([^"]*)"'
        )
        if len(title.split('.')) > 1:
            title = ".".join(title.split('.')[:-1])

        docid = match1(url, '/file/d/([^/]+)')

        request.install_opener(
            request.build_opener(request.HTTPCookieProcessor())
        )

        real_url = (
            'https://docs.google.com/uc?export=download&confirm=no_antivirus&'
            'id={}'.format(docid)
        )
        redirected_url = get_location(real_url)
        if real_url != redirected_url:
            # tiny file - get real url here
            _, ext, size = url_info(redirected_url)
            real_url = redirected_url
        else:
            # huge file - the real_url is a confirm page and real url is in it
            confirm_page = get_content(real_url)
            hrefs = re.findall(r'href="(.+?)"', confirm_page)
            for u in hrefs:
                if u.startswith('/uc?export=download'):
                    rel = unescape(u)
            confirm_url = 'https://docs.google.com' + rel
            real_url = get_location(confirm_url)
            _, ext, size = url_info(real_url)
            if size is None:
                size = 0

        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls([real_url], title, ext, size, **kwargs)


download = google_download
download_playlist = playlist_not_supported(site_info)
