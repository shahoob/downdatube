import typer

app = typer.Typer()

@app.command(name="video")
def download_video(url: str): typer.echo("downloaded \"Me at the zoo\"")

@app.command(name="playlist")
def download_playlist(url: str): typer.echo("downloaded all your liked videos")

if __name__ == "__main__":
    app()
