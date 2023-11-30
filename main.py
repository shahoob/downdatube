import subprocess
import tempfile
import threading
from typing import Optional, Tuple

import pytube
import typer
from rich import print
from rich.progress import DownloadColumn, Progress, SpinnerColumn
from rich.prompt import Confirm
from typing_extensions import Annotated

from core.select_streams import select_streams

app = typer.Typer()


@app.command()
def video(url: Annotated[str, typer.Argument(help="The URL of the video.")]):
    """
    Downloads a video. Self explanatory.
    """
    # TODO: add error handling
    # TODO: add more options

    yt = pytube.YouTube(url)
    streams: Tuple[pytube.Stream, Optional[pytube.Stream], Optional[pytube.Caption]]

    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        transient=True,
    ) as progress:
        progress.add_task("Getting info...", total=None)
        streams = select_streams(yt, "1080p")
        print(f"[cyan]Video selected[/cyan]: {yt.title}")

    if not Confirm.ask("Do you want to download the video?", default=True):
        raise typer.Exit()

    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        DownloadColumn(),
        transient=True,
    ) as progress:
        download_total_size = (
            streams[0].filesize + streams[1].filesize if streams[1] is not None else 0
        )

        download_task = progress.add_task("Downloading...", total=download_total_size)

        print(
            "[orange][/orange]Note: When downloading sometimes the progress bar might be a bit janky,"
        )
        print(
            "This is normal and as long as the spinner is spinning, everything should be fine."
        )

        def dhandler(stream: pytube.Stream, chunk: bytes, bytes_remaining: int):
            progress.update(download_task, advance=len(chunk))

        yt.register_on_progress_callback(dhandler)

        with tempfile.TemporaryDirectory() as tempdir:
            paths = []

            def download_streams():
                paths.append(
                    streams[0].download(
                        filename_prefix="v" if streams[1] else None, output_path=tempdir
                    )
                )
                if streams[1]:
                    paths.append(
                        streams[1].download(filename_prefix="a", output_path=tempdir)
                    )
                else:
                    paths.append(None)

            dthread = threading.Thread(target=download_streams)
            dthread.start()
            dthread.join()

            print(paths)

            encode_task = progress.add_task("Encoding...", total=None)

            if paths[1]:
                # trunk-ignore(bandit/B603)
                # trunk-ignore(bandit/B607)
                subprocess.run(
                    [
                        "ffmpeg",
                        "-i",
                        paths[0],
                        "-i",
                        paths[1],
                        "-c:v",
                        "copy",
                        "-c:a",
                        "aac",
                        f"{yt.title}.mp4",
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

            progress.stop_task(encode_task)


@app.command()
def playlist(url: Annotated[str, typer.Argument(help="The URL of the playlist.")]):
    """
    Downloads a playlist's videos. Probably self explanatory.
    """
    # TODO: implement this
    pass


if __name__ == "__main__":
    app()
