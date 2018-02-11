#!/usr/bin/env python

import re
import json

from lulu.common import (
    match1,
    url_info,
    print_info,
    get_content,
    post_content,
    download_urls,
    playlist_not_supported,
)


__all__ = ['vk_download']
site_info = 'VK vk.com'


def get_video_info(url):
    ep = 'https://vk.com/al_video.php'
    to_post = dict(
        act='show', al=1, module='direct',
        video=re.search(r'video(-\d+_\d+)', url).group(1)
    )
    page = post_content(ep, post_data=to_post)
    video_pt = r'<source src="(.+?)" type="video\/mp4"'
    url = re.search(video_pt, page).group(1)
    title = re.search(r'<div class="mv_title".+?>(.+?)</div>', page).group(1)
    mime, ext, size = url_info(url)
    print_info(site_info, title, mime, size)

    return url, title, ext, size


def get_image_info(url):
    image_page = get_content(url)
    photo_id = url.split('-')[-1]
    photo_data = json.loads(
        match1(image_page, r'({{"id":"-{}.+?}}),'.format(photo_id))
    )
    for quality in ['z_src', 'y_src', 'x_src', 'r_src', 'q_src', 'p_src']:
        if photo_data.get(quality):
            image_link = photo_data[quality]
            break
    title = image_link.split('/')[-1].split('.')[0]
    _type, ext, size = url_info(image_link)
    print_info(site_info, title, _type, size)

    return image_link, title, ext, size


def vk_download(
    url, output_dir='.', stream_type=None, merge=True, info_only=False,
    **kwargs
):
    link = None
    if re.match(r'(.+)vk\.com\/video(.+)', url):
        link, title, ext, size = get_video_info(url)
    elif re.match(r'(.+)vk\.com\/photo(.+)', url):
        link, title, ext, size = get_image_info(url)
    else:
        raise NotImplementedError('Nothing to download here')

    if not info_only and link is not None:
        download_urls([link], title, ext, size, output_dir, merge=merge)


download = vk_download
download_playlist = playlist_not_supported(site_info)
