#!/usr/bin/env python

import re
import ssl
from urllib import request

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['videomega_download']
site_info = 'Videomega.tv'


def videomega_download(url, info_only=False, **kwargs):
    # Hot-plug cookie handler
    ssl_context = request.HTTPSHandler(
        context=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    )
    cookie_handler = request.HTTPCookieProcessor()
    opener = request.build_opener(ssl_context, cookie_handler)
    opener.addheaders = [('Referer', url), ('Cookie', 'noadvtday=0')]
    request.install_opener(opener)

    if re.search(r'view\.php', url):
        php_url = url
    else:
        content = get_content(url)
        m = re.search(
            r'ref="([^"]*)";\s*width="([^"]*)";\s*height="([^"]*)"', content
        )
        ref = m.group(1)
        width, height = m.group(2), m.group(3)
        php_url = (
            'http://videomega.tv/view.php?ref={}&width={}&height={}'.format(
                ref, width, height
            )
        )
    content = get_content(php_url)

    title = match1(content, r'<title>(.*)</title>')
    js = match1(content, r'(eval.*)')
    t = match1(js, r'\$\("\w+"\)\.\w+\("\w+","([^"]+)"\)')
    t = re.sub(r'(\w)', r'{\1}', t)
    t = t.translate({87 + i: str(i) for i in range(10, 36)})
    s = match1(js, r"'([^']+)'\.split").split('|')
    src = t.format(*s)

    _type, ext, size = url_info(src, faker=True)

    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls([src], title, ext, size, **kwargs)


download = videomega_download
download_playlist = playlist_not_supported(site_info)
