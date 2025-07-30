"""
TODO: Maybe move to 'yta_multimedia_constants' and
its Enums module.
"""
from yta_constants.enum import YTAEnum as Enum


class VideoFrameExtractionMode(Enum):
    """
    Enum to simplify the way we indicate the frame extraction
    operation we want to execute.
    """

    FRAME_TIME_MOMENT = 'frame_time_moment'
    """
    Use the frame time moments, which are the time moments 
    that belong to the time in which the frame is being
    displayed according to its duration and fps.
    """
    FRAME_INDEX = 'frame_index'
    """
    Use the frame indexes, which are the indexes of the
    frames, one after the other.
    """