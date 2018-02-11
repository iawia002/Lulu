#!/usr/bin/env python

import re
import json

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    download_urls,
)


__all__ = ['lizhi_download']
site_info = '荔枝 lizhi.fm'


# radio_id: e.g. 549759 from http://www.lizhi.fm/549759/
#
# Returns a list of tuples (audio_id, title, url) for each episode
# (audio) in the radio playlist. url is the direct link to the audio
# file.
def lizhi_extract_playlist_info(radio_id):
    # /api/radio_audios API parameters:
    #
    # - s: starting episode
    # - l: count (per page)
    # - band: radio_id
    #
    # We use l=65535 for poor man's pagination (that is, no pagination
    # at all -- hope all fits on a single page).
    #
    # TODO: Use /api/radio?band={radio_id} to get number of episodes
    # (au_cnt), then handle pagination properly.
    api_url = (
        'http://www.lizhi.fm/api/radio_audios?s=0&l=65535&band={}'.format(
            radio_id
        )
    )
    api_response = json.loads(get_content(api_url))
    return api_response


def lizhi_download_audio(audio_id, title, url, info_only=False, **kwargs):
    filetype, ext, size = url_info(url)
    print_info(site_info, title, filetype, size)
    if not info_only:
        download_urls([url], title, ext, size, **kwargs)


def lizhi_download_playlist(url, info_only=False, **kwargs):
    # Sample URL: http://www.lizhi.fm/549759/
    radio_id = match1(url, r'/(\d+)')
    if not radio_id:
        raise NotImplementedError('{} not supported'.format(url))
    for data in lizhi_extract_playlist_info(radio_id):
        lizhi_download_audio(
            data['id'], data['name'], data['fixedHighPlayUrl'],
            info_only=info_only, **kwargs
        )


def lizhi_download(url, output_dir='.', info_only=False, **kwargs):
    # Sample URL: http://www.lizhi.fm/549759/2508612053517249030
    m = re.search(r'/(?P<radio_id>\d+)/(?P<audio_id>\d+)', url)
    if not m:
        raise NotImplementedError('{} not supported'.format(url))
    radio_id = m.group('radio_id')
    audio_id = m.group('audio_id')
    # Look for the audio_id among the full list of episodes
    data = list(filter(
        lambda x: x['id'] == audio_id, lizhi_extract_playlist_info(radio_id)
    ))[0]
    lizhi_download_audio(
        audio_id, data['name'], data['fixedHighPlayUrl'], info_only=info_only,
        **kwargs
    )


download = lizhi_download
download_playlist = lizhi_download_playlist
