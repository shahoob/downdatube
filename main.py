from typing import Optional, Tuple
import typer
from typing_extensions import Annotated

import time

import pytube

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

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

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task("Getting info...", total=None)

        streams: Tuple[pytube.Stream, Optional[pytube.Stream], Optional[pytube.Caption]] = select_streams(yt, "1080p")

        print(f"Video: {yt.title}")

        progress.remove_task(task)
        


@app.command()
def playlist(url: Annotated[str, typer.Argument(help="The URL of the playlist.")]):
    """
    Downloads a playlist's videos. Probably self explanatory.
    """
    # TODO: implement this
    pass


if __name__ == "__main__":
    app()
