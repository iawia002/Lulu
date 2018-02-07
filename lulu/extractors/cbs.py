#!/usr/bin/env python

import json

from lulu.common import (
    match1,
    get_content,
    playlist_not_supported,
)
from lulu.extractors.theplatform import theplatform_download_by_pid


__all__ = ['cbs_download']
site_info = 'CBS cbs.com'


def cbs_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    """Downloads CBS videos by URL.
    """
    html = get_content(url)
    data = json.loads(match1(html, r'var \$module = (.+);'))
    pid = data['video']['pid']
    title = data['video']['title']
    theplatform_download_by_pid(
        pid, title, output_dir=output_dir, merge=merge, info_only=info_only
    )


download = cbs_download
download_playlist = playlist_not_supported(site_info)
