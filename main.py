from typing import Optional

import fire
from pytube import YouTube
from halo import Halo

from corefunctions.get_stream import get_stream
from corefunctions.helpers import map_stream
from corefunctions.download import download_stream


def download(url: str, itag: Optional[int] = None, prefetch: Optional[bool] = False):
    with Halo(text='Trying to get a tube... (creating YouTube object...)') as h:
        yt = YouTube(url)
        if prefetch:
            h.text = 'Digging through the tube... (prefetch)'
            yt.prefetch()

    print('Some info about this tube:\n')

    print(yt.title)
    print(yt.description)

    print('\n')

    stream = get_stream(yt=yt, itag=itag)
    print(map_stream(stream))

    download_stream(yt, stream)

if __name__ == '__main__':
    fire.Fire(download, name='downdatube')