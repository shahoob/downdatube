from typer.testing import CliRunner

from main.main import app

runner = CliRunner()

def test_download_video():
    result = runner.invoke(app, ["video", "https://youtu.be/jNQXAC9IVRw"])
    assert result.exit_code == 0
    assert "downloaded \"Me at the zoo\"" in result.stdout

    resulterr = runner.invoke(app, ["video"])
    assert resulterr.exit_code != 0

def test_download_playlist():
    result = runner.invoke(app, ["playlist", "https://youtu.be/jNQXAC9IVRw"])
    assert result.exit_code == 0
    assert "downloaded all your liked videos" in result.stdout
