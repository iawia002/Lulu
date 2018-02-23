#!/usr/bin/env python

import os
from copy import copy

from lulu.common import (
    match1,
    dry_run,
    url_size,
    urls_size,
    set_proxy,
    print_info,
    parse_host,
    unset_proxy,
    maybe_print,
    get_filename,
    download_urls,
    download_url_ffmpeg,
    general_m3u8_extractor,
)
from lulu import config
from lulu.util import log
from lulu import json_output


class VideoExtractor:
    '''Suitable for websites that the video files have many formats
    '''
    def __init__(self, *args):
        self.url = None
        self.title = None
        self.vid = None
        self.m3u8_url = None
        self.streams = {}
        self.streams_sorted = []
        self.audiolang = None
        self.password_protected = False
        self.dash_streams = {}
        self.caption_tracks = {}
        self.out = False
        self.ua = None
        self.referer = None
        self.danmuku = None

        if args:
            self.url = args[0]

    def _prepare_download(self, **kwargs):
        proxy = kwargs.get('extractor_proxy')
        if proxy:
            set_proxy(parse_host(kwargs['extractor_proxy']))
        self.prepare(**kwargs)
        if self.out:
            return
        if proxy:
            unset_proxy()

        try:
            self.streams_sorted = [
                dict([('id', stream_type['id'])] + list(
                    self.streams[stream_type['id']].items()
                )) for stream_type in self.__class__.stream_types
                if stream_type['id'] in self.streams
            ]
        except Exception:
            self.streams_sorted = [
                dict([('itag', stream_type['itag'])] + list(
                    self.streams[stream_type['itag']].items()
                )) for stream_type in self.__class__.stream_types
                if stream_type['itag'] in self.streams
            ]
        self.extract(**kwargs)
        self.download(**kwargs)

    def download_by_url(self, url, **kwargs):
        self.url = url
        self.vid = None
        self._prepare_download(**kwargs)

    def download_by_vid(self, vid, **kwargs):
        self.url = None
        self.vid = vid
        self._prepare_download(**kwargs)

    def prepare(self, **kwargs):
        pass
        # raise NotImplementedError()

    def extract(self, **kwargs):
        pass
        # raise NotImplementedError()

    def p_stream(self, stream_id):
        if stream_id in self.streams:
            stream = self.streams[stream_id]
        else:
            stream = self.dash_streams[stream_id]

        if 'itag' in stream:
            print("    - itag:          %s" % log.sprint(
                stream_id, log.NEGATIVE
            ))
        else:
            print("    - format:        %s" % log.sprint(
                stream_id, log.NEGATIVE
            ))

        if 'container' in stream:
            print("      container:     %s" % stream['container'])

        if 'video_profile' in stream:
            maybe_print("      video-profile: %s" % stream['video_profile'])

        if 'quality' in stream:
            print("      quality:       %s" % stream['quality'])

        if 'size' in stream and stream['container'].lower() != 'm3u8':
            if stream['size'] != float('inf') and stream['size'] != 0:
                print("      size:          {} MiB ({} bytes)".format(
                    round(stream['size'] / 1048576, 1), stream['size']
                ))

        if 'm3u8_url' in stream:
            print("      m3u8_url:      {}".format(stream['m3u8_url']))

        if 'itag' in stream:
            print("    # download-with: %s" % log.sprint(
                "lulu --itag=%s [URL]" % stream_id, log.UNDERLINE
            ))
        else:
            print("    # download-with: %s" % log.sprint(
                "lulu --format=%s [URL]" % stream_id, log.UNDERLINE
            ))

        print()

    def p_i(self, stream_id):
        if stream_id in self.streams:
            stream = self.streams[stream_id]
        else:
            stream = self.dash_streams[stream_id]

        maybe_print("    - title:         %s" % self.title)
        print("       size:         {} MiB ({} bytes)".format(
            round(stream['size'] / 1048576, 1), stream['size']
        ))
        print("        url:         %s" % self.url)
        print()

    def p(self, stream_id=None):
        maybe_print("site:                %s" % self.__class__.name)
        maybe_print("title:               %s" % self.title)
        if stream_id:
            # Print the stream
            print("stream:")
            self.p_stream(stream_id)

        elif stream_id is None:
            # Print stream with best quality
            print("stream:              # Best quality")
            stream_id = self.streams_sorted[0]['id'] \
                if 'id' in self.streams_sorted[0] \
                else self.streams_sorted[0]['itag']
            self.p_stream(stream_id)

        elif stream_id == []:
            print("streams:             # Available quality and codecs")
            # Print DASH streams
            if self.dash_streams:
                print("    [ DASH ] %s" % ('_' * 36))
                itags = sorted(
                    self.dash_streams,
                    key=lambda i: -self.dash_streams[i]['size']
                )
                for stream in itags:
                    self.p_stream(stream)
            # Print all other available streams
            print("    [ DEFAULT ] %s" % ('_' * 33))
            for stream in self.streams_sorted:
                self.p_stream(
                    stream['id'] if 'id' in stream else stream['itag']
                )

        if self.audiolang:
            print("audio-languages:")
            for i in self.audiolang:
                print("    - lang:          {}".format(i['lang']))
                print("      download-url:  {}\n".format(i['url']))

    def p_playlist(self, stream_id=None):
        maybe_print("site:                %s" % self.__class__.name)
        print("playlist:            %s" % self.title)
        print("videos:")

    def download(self, **kwargs):
        if 'json_output' in kwargs and kwargs['json_output']:
            json_output.output(self)
        elif 'info_only' in kwargs and kwargs['info_only']:
            if 'stream_id' in kwargs and kwargs['stream_id']:
                # Display the stream
                stream_id = kwargs['stream_id']
                if 'index' not in kwargs:
                    self.p(stream_id)
                else:
                    self.p_i(stream_id)
            else:
                # Display all available streams
                if 'index' not in kwargs:
                    self.p([])
                else:
                    stream_id = self.streams_sorted[0]['id'] \
                        if 'id' in self.streams_sorted[0] \
                        else self.streams_sorted[0]['itag']
                    self.p_i(stream_id)

        else:
            if 'stream_id' in kwargs and kwargs['stream_id']:
                # Download the stream
                stream_id = kwargs['stream_id']
            else:
                # Download stream with the best quality
                stream_id = self.streams_sorted[0]['id'] \
                    if 'id' in self.streams_sorted[0] \
                    else self.streams_sorted[0]['itag']

            if 'index' not in kwargs:
                self.p(stream_id)
            else:
                self.p_i(stream_id)

            if stream_id in self.streams:
                urls = self.streams[stream_id]['src']
                ext = self.streams[stream_id]['container']
                total_size = self.streams[stream_id]['size']
            else:
                urls = self.dash_streams[stream_id]['src']
                ext = self.dash_streams[stream_id]['container']
                total_size = self.dash_streams[stream_id]['size']

            if not urls:
                log.wtf('[Failed] Cannot extract video source.')

            if ext == 'm3u8':
                ffmpeg_kwargs = {}
                if 'iqiyi' in self.name:
                    # ffmpeg_kwargs['override'] = True
                    # ffmpeg_kwargs['params'] = {
                    #     '-c:a': 'copy', '-bsf:a': 'aac_adtstoasc'
                    # }
                    m3u8_urls = general_m3u8_extractor(urls[0])
                    size = sum([
                        int(match1(url, r'contentlength=(\d+)'))
                        for url in m3u8_urls
                    ])
                    download_urls(
                        m3u8_urls, self.title, 'mp4', size, **kwargs
                    )
                else:
                    download_url_ffmpeg(
                        urls[0], self.title, 'mp4',
                        output_dir=kwargs['output_dir'],
                        merge=kwargs['merge'], stream=False,
                        **ffmpeg_kwargs
                    )
            else:
                headers = copy(config.FAKE_HEADERS)
                if self.ua is not None:
                    headers['User-Agent'] = self.ua
                if self.referer is not None:
                    headers['Referer'] = self.referer
                download_urls(
                    urls,
                    self.title,
                    ext,
                    total_size,
                    headers=headers,
                    refer=self.referer,
                    av=stream_id in self.dash_streams,
                    **kwargs
                )
            if 'caption' not in kwargs or not kwargs['caption']:
                print('Skipping captions or danmuku.')
                return
            for lang in self.caption_tracks:
                filename = '%s.%s.srt' % (get_filename(self.title), lang)
                print('Saving %s ... ' % filename, end="", flush=True)
                srt = self.caption_tracks[lang]
                with open(
                    os.path.join(kwargs['output_dir'], filename),
                    'w',
                    encoding='utf-8'
                ) as x:
                    x.write(srt)
                print('Done.')
            if self.danmuku is not None and not dry_run:
                filename = '{}.cmt.xml'.format(get_filename(self.title))
                print('Downloading {} ...\n'.format(filename))
                with open(
                    os.path.join(kwargs['output_dir'], filename),
                    'w',
                    encoding='utf8'
                ) as fp:
                    fp.write(self.danmuku)

        keep_obj = kwargs.get('keep_obj', False)
        if not keep_obj:
            self.__init__()


class SimpleExtractor:
    '''Suitable for small video websites that the video files have only one
    format
    '''
    def __init__(self):
        self.need_download = True
        self.site_info = None

    def __call__(self, url, **kwargs):
        '''
        data = {
            'urls': [],
            'title': '',
            'file_format': '',
            'size': '',
        }
        '''
        data = self.extract(url, **kwargs)

        if not self.need_download:
            return

        file_format = data.get('file_format', 'mp4')
        size = data.get('size')
        urls = data['urls']
        if not size:
            if len(urls) == 1:
                size = url_size(urls[0])
            else:
                size = urls_size(urls)
        print_info(
            site_info=self.site_info, title=data['title'],
            type=file_format, size=size
        )
        if not kwargs['info_only']:
            download_urls(
                urls=urls, title=data['title'], ext=file_format,
                total_size=size, **kwargs
            )

    def extract(self, url, **kwargs):
        raise NotImplementedError()
