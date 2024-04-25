# trunk-ignore-all(bandit/B101)
import pytest
import pytube

from downdatube.core.save_video import save_video
from downdatube.core.select_streams import select_streams


@pytest.fixture()
def video_1():
    return pytube.YouTube("https://www.youtube.com/watch?v=LXb3EKWsInQ")


@pytest.fixture()
def video_2():
    return pytube.YouTube("https://www.youtube.com/watch?v=jNQXAC9IVRw")


@pytest.mark.parametrize("res", ["144p", "360p", "720p", "1080p", "1440p", "2160p"])
def test_adaptive(res, video_1, tmp_path):
    yt = video_1

    streams = select_streams(yt, res)

    final_path = save_video(streams=streams, yt=yt, path=tmp_path)

    assert final_path is not None
    assert final_path.exists()
