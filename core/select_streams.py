from typing import Optional, Tuple

import pytube


def select_streams(
    yt: pytube.YouTube, res: str
) -> Tuple[pytube.Stream, Optional[pytube.Stream], Optional[pytube.Caption]]:
    """
    Selects the streams closest to the user's preferences.

    Returns a tuple with the best video stream, audio stream (if it's adaptive), and a caption track (if available)
    """

    def no_audio_only(s: pytube.Stream):
        return s.resolution is not None

    # convert the resolutions from strings to intergers so we can compare them easily
    max_res = int(sorted(
        yt.streams.filter(
            custom_filter_functions=[no_audio_only]
        ), key=lambda s: int(s.resolution[:-1]), reverse=True
    )[0].resolution[:-1])
    _res = int(res[:-1])

    # if the max resolution AND the user's requested resolution is greater than 720p, use adaptive streams
    use_adaptive = (max_res > 720) and (_res > 720)
    streams = yt.streams.filter(adaptive=use_adaptive)

    if _res > max_res:
        # use the highest resolution available if the user requested a higher resolution than the video's highest.
        best_stream_1: pytube.Stream = streams.filter(resolution=f"{max_res}p").first()
    else:
        # otherwise use the requested resolution
        best_stream_1: pytube.Stream = streams.filter(resolution=f"{_res}p").first()

    best_stream_2: Optional[pytube.Stream] = None

    if use_adaptive:
        best_stream_2 = (
            # streams.filter(only_audio=True).order_by("abr").last()
            streams.get_audio_only()
        )

    return (best_stream_1, best_stream_2, None)
