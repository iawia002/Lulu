#!/usr/bin/env python

import re

from lulu.common import (
    get_content,
    playlist_not_supported,
)
from lulu.extractor import SimpleExtractor


__all__ = ['kuaishou_download_by_url']
site_info = 'kuaishou.com'


class Kuaishou(SimpleExtractor):
    def extract(self, url, **kwargs):
        self.site_info = site_info
        page = get_content(url)
        title = re.search(
            r'<meta\s+property="og:title"\s+content="(.+?)"/>', page
        ).group(1)
        try:
            url = re.search(
                r'<meta\s+property="og:video:url"\s+content="(.+?)"/>', page
            ).group(1)
            file_format = url.split('.')[-1]
        except Exception:  # extract image
            url = re.search(
                r'<meta\s+property="og:image"\s+content="(.+?)"/>', page
            ).group(1)
            file_format = url.split('.')[-1]
        return {
            'title': title,
            'urls': [url],
            'file_format': file_format,
        }


download = kuaishou_download_by_url = Kuaishou()
download_playlist = playlist_not_supported(site_info)
