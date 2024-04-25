# trunk-ignore-all(bandit/B101)
import pytest
import pytube

from downdatube.core.select_streams import select_streams


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

@pytest.mark.parametrize(
    "res,adaptive", [("144p", False), ("240p", False), ("360p", False), ("480p", False), ("720p", False), ("1080p", True), ("1440p", True), ("2160p", True)],
)
@pytest.mark.parametrize(
    "video,adaptiveExpected", [(pytube.YouTube("https://www.youtube.com/watch?v=LXb3EKWsInQ"), True), (pytube.YouTube("https://www.youtube.com/watch?v=jNQXAC9IVRw"), False)]
)
def test_adaptive(res, adaptive, video, adaptiveExpected, request):
    yt = video

    streams = select_streams(yt, res)

    if adaptiveExpected:
        if adaptive:
            assert streams[0].is_adaptive
    else:
        assert streams[1] is None
