from humanfriendly import format_size
from pytube import Stream


def map_stream(stream: Stream):
    return f'{stream.title} | itag: {stream.itag} | {stream.resolution} | {stream.mime_type} | {format_size(stream.filesize)} | is_progressive: {stream.is_progressive}'
