#!/usr/bin/env python

import re
import time
from urllib import (
    parse,
    request,
)

from lulu.common import (
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.util import log
from lulu.config import FAKE_HEADERS


__all__ = ['vidto_download']
site_info = 'Vidto vidto.me'


def vidto_download(url, info_only=False, **kwargs):
    html = get_content(url)
    params = {}
    r = re.findall(
        r'type="(?:hidden|submit)?"(?:.*?)name="(.+?)"\s* value="?(.+?)">',
        html
    )
    for name, value in r:
        params[name] = value
    data = parse.urlencode(params).encode('utf-8')
    req = request.Request(url, headers=FAKE_HEADERS)
    print('Please wait for 6 seconds...')
    time.sleep(6)
    print('Starting')
    new_html = request.urlopen(req, data).read().decode('utf-8', 'replace')
    new_stff = re.search(r'lnk_download" href="(.*?)">', new_html)
    if new_stff:
        url = new_stff.group(1)
        title = params['fname']
        _type = ''
        ext = ''
        a, b, size = url_info(url)
        print_info(site_info, title, _type, size)
        if not info_only:
            download_urls([url], title, ext, size, **kwargs)
    else:
        log.wtf("Cann't find link, please review")


download = vidto_download
download_playlist = playlist_not_supported(site_info)
