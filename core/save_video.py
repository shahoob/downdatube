import pathlib
import shutil
import subprocess
import tempfile
from typing import Any, Callable, Optional, Tuple

import pytube


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
            progress_callback("encode", "start")

            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    v_path,
                    "-i",
                    a_path,
                    "-c:v",
                    "copy",
                    "-c:a",
                    "aac",
                    final_path,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            progress_callback("encode", "end")
        else:
            shutil.move(v_path, final_path)
    return final_path
