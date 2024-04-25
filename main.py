import os
import pathlib
from typing import Any, Literal, Optional, Tuple, Union

import pytube
import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from typing_extensions import Annotated

from core.save_video import save_video
from core.select_streams import select_streams

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
        print(f"[cyan]Video selected[/]: {yt.title}")
        total_size = (
            streams[0].filesize + streams[1].filesize if streams[1] is not None else 0
        )
        print(f"[cyan]Size[/]: {total_size / 1024 / 1024:.2f} MB")

    if not yes:
        if not Confirm.ask("Do you want to download the video?", default=True):
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
                    progress.start_task(encode_task)
                    progress.update(encode_task, visible=True, total=None)
                if data == "end":
                    progress.stop_task(encode_task)

        print_download_warning()
        download_path = save_video(
            streams, yt, pathlib.Path(os.getcwd()), progress_callback=update_progress
        )

    print(f'[cyan]Downloaded to[/] "{download_path}"')


@app.command()
def playlist(url: Annotated[str, typer.Argument(help="The URL of the playlist.")]):
    """
    Downloads a playlist's videos. Probably self explanatory.
    """
    # TODO: implement this
    pass


if __name__ == "__main__":
    app()
