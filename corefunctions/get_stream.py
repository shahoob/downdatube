from typing import Optional

from halo import Halo
from pytube import YouTube, Stream
from pick import pick

from corefunctions.helpers import map_stream


def get_stream(yt: YouTube, itag: Optional[int] = None) -> Stream:
    if itag is None:
        streams: list[Stream] = []

        print(f'{yt.watch_url} has {len(yt.streams)} streams')

        with Halo(text='Finding all streams... (none)', animation='marquee') as h:
            counter = 0
            for s in yt.streams:
                counter+=1
                h.text = f'Finding all streams... (stream: {map_stream(s)}, #{counter} of #{len(yt.streams)})'
                streams.append(s)

        result: Stream = pick(streams, options_map_func=map_stream)[0]
    else: result: Stream = yt.streams.get_by_itag(itag=itag)

    return result
