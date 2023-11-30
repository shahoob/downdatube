# trunk-ignore-all(bandit/B101)
import pytest
import pytube

from core.select_streams import select_streams


@pytest.fixture()
def video_1():
    return pytube.YouTube("https://www.youtube.com/watch?v=LXb3EKWsInQ")


@pytest.fixture()
def video_2():
    return pytube.YouTube("https://www.youtube.com/watch?v=jNQXAC9IVRw")


@pytest.mark.parametrize(
    "res", ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
)
def test_up_to_4k(res, video_1):
    yt = video_1

    streams = select_streams(yt, res)
    assert streams[0].resolution == res


def test_max_res(video_2):
    yt = video_2

    streams = select_streams(yt, "2160p")
    assert streams[0].resolution == "360p"

    streams = select_streams(yt, "144p")
    assert streams[0].resolution == "144p"
