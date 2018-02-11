#!/usr/bin/env python

from urllib import (
    parse,
    request,
)

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
    playlist_not_supported,
)
from lulu.config import FAKE_HEADERS


__all__ = ['nicovideo_download']
site_info = 'niconico nicovideo.jp'
fake_headers = FAKE_HEADERS.copy()


def nicovideo_login(user, password):
    data = 'current_form=login&mail={}&password={}&login_submit=Log+In'.format(
        user, password
    )
    response = request.urlopen(request.Request(
        'https://secure.nicovideo.jp/secure/login?site=niconico',
        headers=fake_headers, data=data.encode('utf-8')
    ))
    return response.headers


def nicovideo_download(url, info_only=False, **kwargs):
    import ssl
    ssl_context = request.HTTPSHandler(
        context=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    )
    cookie_handler = request.HTTPCookieProcessor()
    opener = request.build_opener(ssl_context, cookie_handler)
    request.install_opener(opener)

    import netrc
    import getpass
    try:
        info = netrc.netrc().authenticators('nicovideo')
    except Exception:
        info = None
    if info is None:
        user = input('User:     ')
        password = getpass.getpass('Password: ')
    else:
        user, password = info[0], info[2]
    print('Logging in...')
    nicovideo_login(user, password)

    html = get_content(url)  # necessary!
    title = match1(html, r'<title>(.+?)</title>')

    vid = url.split('/')[-1].split('?')[0]
    api_html = get_content('http://flapi.nicovideo.jp/api/getflv?v={}'.format(
        vid
    ))
    real_url = parse.unquote(match1(api_html, r'url=([^&]+)&'))

    _type, ext, size = url_info(real_url)
    print_info(site_info, title, _type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, **kwargs)


download = nicovideo_download
download_playlist = playlist_not_supported(site_info)
