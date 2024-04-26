# trunk-ignore-all(bandit/B101)
import pytest

from typer.testing import CliRunner
from .main import app

runner = CliRunner()

@pytest.fixture()
def video_1():
    return "https://www.youtube.com/watch?v=LXb3EKWsInQ"


@pytest.fixture()
def video_2():
    return "https://www.youtube.com/watch?v=jNQXAC9IVRw"

def test_video(video_1):
    result = runner.invoke(app, ['video', video_1, '-y'])
    assert result.exit_code == 0
    assert "Downloaded to" in result.stdout
