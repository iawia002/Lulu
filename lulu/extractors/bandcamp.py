#!/usr/bin/env python

import json

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
)


__all__ = ['bandcamp_download']
site_info = 'Bandcamp bandcamp.com'


def bandcamp_download(
    url, output_dir='.', merge=True, info_only=False, **kwargs
):
    html = get_content(url)
    trackinfo = json.loads(
        match1(html, r'trackinfo:\s+(\[.+\]),')
    )
    for track in trackinfo:
        track_num = track['track_num']
        title = '{}. {}'.format(track_num, track['title'])
        file_url = track['file']['mp3-128']
        mime, ext, size = url_info(file_url)

        print_info(site_info, title, mime, size)
        if not info_only:
            download_urls(
                [file_url], title, ext, size, output_dir, merge=merge,
                **kwargs
            )


download = bandcamp_download
download_playlist = bandcamp_download
