import pathlib
import shutil
import tempfile
from typing import Any, Callable, Optional, Tuple

from datetime import timedelta

import pytube
from ffmpeg import FFmpeg, Progress


def save_video(
    streams: Tuple[pytube.Stream, Optional[pytube.Stream]],
    yt: pytube.YouTube,
    path: pathlib.Path,
    filename: Optional[str] = None,
    progress_callback: Optional[Callable[[str, Any], None]] = (lambda x, y: None),
):
    """
    Saves a video in a easily usable manner at the specified path.
    """
    final_path: pathlib.Path

    with tempfile.TemporaryDirectory() as tempdir:
        v_path: str = ""
        a_path: Optional[str] = ""

        global download_remaining_size
        download_remaining_size = (
            streams[0].filesize + streams[1].filesize if streams[1] is not None else 0
        )

        if not filename:
            filename = streams[0].default_filename

        def dhandler(stream: pytube.Stream, chunk: bytes, bytes_remaining: int):
            global download_remaining_size
            download_remaining_size -= len(chunk)
            progress_callback("download", (len(chunk), download_remaining_size))

        yt.register_on_progress_callback(dhandler)

        v_path = streams[0].download(output_path=tempdir, filename_prefix="v_")
        if streams[1]:
            a_path = streams[1].download(output_path=tempdir, filename_prefix="a_")

        final_path = path / filename

        if streams[1]:

            encode = (
                FFmpeg()
                .option("y")
                .input(v_path)
                .input(a_path)
                .output(final_path, {"c:v": "copy", "c:a": "aac"})
            )

            @encode.listens_to("start")
            def onStart(args):
                progress_callback("encode", "start")
                print(args)

            @encode.listens_to("progress")
            def onProgress(progress: Progress):
                progress_callback("encode", progress.time/timedelta(seconds=yt.length))

            @encode.listens_to("completed")
            def onEnd():
                progress_callback("encode", "end")

            encode.execute()
        else:
            shutil.move(v_path, final_path)
    return final_path



