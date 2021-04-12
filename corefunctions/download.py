from pytube import YouTube, Stream
import progressbar


def download_stream(yt: YouTube, stream: Stream):

    with progressbar.DataTransferBar(max_value=stream.filesize) as bar:
        def on_progress(stream, chunk: bytes, bytes_remaining: int):
            # bar.update(len(chunk))
            bar.update(stream.filesize - bytes_remaining)
        def on_complete(stream, file_path: str):
            bar.finish()
            print(f'Downloaded at {file_path}')

        yt.register_on_progress_callback(on_progress)
        yt.register_on_complete_callback(on_complete)
        stream.download()