from typing import Optional

import typer

import match_video.utils as utils
from match_video.anchor import Anchor

app = typer.Typer()


@app.command()
def set_half_starts(
    input_video_path: str,
    first_half_start_time: str,
    second_half_start_time: str,
    extra_time_first_half_start_time: Optional[str] = None,
    extra_time_second_half_start_time: Optional[str] = None,
    output_video_path: Optional[str] = None,
) -> None:
    """Set the start times for each half of a match video.

    Args:
        input_video_path: The path to a video.
        first_half_start_time: The start of the first half as hh:mm:ss or mm:ss in video time.
        second_half_start_time: The start of the second half as hh:mm:ss or mm:ss in video time.
        extra_time_first_half_start_time: The start of the first half of extra time as hh:mm:ss or mm:ss in video time.
        extra_time_second_half_start_time: The start of the second half of extra time as hh:mm:ss or mm:ss in video time.
        output_video_path: The path to write the video with anchors to. Overwrite the
            input video if this is not specified.
    """
    if output_video_path is None:
        output_video_path = input_video_path

    def get_anchor(period: int, video_time_str: str) -> Anchor:
        split_video_time = video_time_str.split(":")

        if len(split_video_time) == 3:
            video_hours, video_minutes, video_seconds = split_video_time
        elif len(split_video_time) == 2:
            video_minutes, video_seconds = split_video_time
            video_hours = 0  # type: ignore
        else:
            raise ValueError(
                f"Invalid time format: {video_time_str}, expected mm:ss or hh:mm:ss"
            )

        video_time = (
            int(video_hours) * 3600 + int(video_minutes) * 60 + int(video_seconds)
        )

        return Anchor(period, 0.0, video_time)

    anchors = [
        get_anchor(1, first_half_start_time),
        get_anchor(2, second_half_start_time),
    ]

    if extra_time_first_half_start_time is not None:
        assert (
            extra_time_second_half_start_time is not None
        ), "Start times for both halves of extra time must be provided"

        anchors.append(get_anchor(3, extra_time_first_half_start_time))
        anchors.append(get_anchor(4, extra_time_second_half_start_time))

    utils.write_anchors(input_video_path, output_video_path, anchors)


@app.command()
def read_anchors(video_path: str) -> None:
    """Read the anchors set for a video.

    Args:
        video_path: The path to a video.
    """
    anchors = utils.read_anchors(video_path)

    if len(anchors) == 0:
        typer.echo("No anchors set for video")

    for anchor in anchors:
        minute = int(anchor.clock / 60)
        second = int(anchor.clock % 60)

        video_minute = int(anchor.video_time / 60)
        video_second = int(anchor.video_time % 60)

        typer.echo(
            f"Period {anchor.period} {minute}:{second:02} | {video_minute}:{video_second:02} in video"
        )


if __name__ == "__main__":
    app()
