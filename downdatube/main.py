import os
import pathlib
from typing import Any, Literal, Optional, Tuple

import pytube
import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from typing_extensions import Annotated

from .core.save_video import save_video
from .core.select_streams import select_streams

from questionary import confirm

app = typer.Typer()


def print_download_warning():
    print(
        "[yellow]Note[/]: When downloading sometimes the progress bar might be a bit janky,"
    )
    print(
        "This is normal and as long as the spinner is spinning, everything should be fine."
    )
    print("I'll try to fix this sometime in the future.")


@app.command()
def video(
    url: Annotated[str, typer.Argument(help="The URL of the video.")],
    yes: Annotated[
        bool, typer.Option("-y", help="Answer all prompts with their default options.")
    ] = False,
):
    """
    Downloads a video. Self explanatory.
    """
    # TODO: add error handling
    # TODO: add more options
    # TODO: add support for captions

    yt = pytube.YouTube(url)
    streams: Tuple[pytube.Stream, Optional[pytube.Stream], Optional[pytube.Caption]]

    download_path: pathlib.Path

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Getting info...", total=None)
        streams = select_streams(yt, "1080p")
        print(f"[cyan]Video selected[/]: [link {yt.watch_url}]{yt.title}[/]")
        total_size = (
            streams[0].filesize + streams[1].filesize if streams[1] is not None else 0
        )
        print(f"[cyan]Size[/]: {total_size / 1024 / 1024:.2f} MB")

    if not yes:
        if not confirm("Do you want to download the video?").ask():
            raise typer.Exit()

    with Progress(
        SpinnerColumn(), *Progress.get_default_columns(), transient=True
    ) as progress:
        download_task = progress.add_task("Downloading...")
        encode_task = progress.add_task("Encoding...", visible=False, start=False)

        total_size = (
            streams[0].filesize + streams[1].filesize if streams[1] is not None else 0
        )

        def update_progress(event_type: Literal["download", "encode"], data: Any):
            if event_type == "download":
                progress.update(
                    download_task, completed=(total_size - data[1]), total=total_size
                )
            if event_type == "encode":
                if data == "start":
                    progress.stop_task(download_task)
                    progress.update(download_task, visible=False)
                    progress.start_task(encode_task)
                    progress.update(encode_task, visible=True, total=1)
                elif data == "end":
                    progress.stop_task(encode_task)
                else:
                    progress.update(encode_task, total=1, completed=data)

        print_download_warning()
        download_path = save_video(
            streams, yt, pathlib.Path(os.getcwd()), progress_callback=update_progress
        )

    print(f'[green]Downloaded to[/] "{download_path}"!')

@app.command()
def playlist(
    url: Annotated[str, typer.Argument(help="The URL of the playlist.")],
):
    """
    Downloads a playlist's videos. Probably self explanatory.
    """
    # TODO: implement this
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(25),
        transient=True,
    ) as progress:
        playlist_info_fetch_task = progress.add_task('Getting playlist info...', total=None)
        playlist = pytube.Playlist(url)

        plural = 's' if playlist.length > 0 else ''

        print(f'[cyan]Got [/][grey88]{playlist.title}"[/], which has {playlist.length} video{plural}')
        progress.stop_task(playlist_info_fetch_task)
        progress.update(playlist_info_fetch_task, visible=False)
        video_info_fetch_task = progress.add_task("Getting video info...", total=playlist.length)

        for video in progress.track(sequence=playlist.videos, task_id=video_info_fetch_task):
            video.check_availability()
            # print(f"[cyan]Video available[/]: [link {video.watch_url}]{video.title}[/]")
            def no_audio_only(s: pytube.Stream):
                    return s.resolution is not None    # convert the resolutions from strings to integers so we can compare them easily
            max_res = int(sorted(
                video.streams.filter(
                    custom_filter_functions=[no_audio_only]
                ), key=lambda s: int(s.resolution[:-1]), reverse=True
            )[0].resolution[:-1])

            # print(f"Highest resolution is {max_res}p")


if __name__ == "__main__": # pragma: no cover
    app()
