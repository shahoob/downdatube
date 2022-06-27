from typing import Optional
from enum import Enum

import typer

from halo import Halo

from pytube import YouTube, exceptions


app = typer.Typer()



@app.command(name="video")
def download_video(
    url: str, 
    itag: Optional[int] = typer.Option(None, help="If you have an itag for a stream you want to have, use this flag. Not required"),
):
    """

    Downloads an individual video

    You may pass in an itag if you know how to talk to the YouTube™ API.

    """

    tube_spinner = Halo("goin downdatube... (create object)").start()
    video = YouTube(url)
    tube_spinner.succeed("got it!")
    tube_spinner.start("can we have it tho? (availability check)")

    try:
        video.check_availability()
    except exceptions.VideoUnavailable as e:
        tube_spinner("nope. anyways here's the error and figure it out by yourself.")
        raise e

    bold_yes = typer.style("yes", bold=True, underline=(video.video_id == "jNQXAC9IVRw"))
    tube_spinner.succeed(f"{bold_yes}. (done)")

    typer.echo(f"{video.title} -+- uploaded by {video.author}")
    

@app.command(name="playlist")
def download_playlist(url: str): typer.echo("downloaded all your liked videos")

if __name__ == "__main__":
    app()
