from yta_multimedia_core.video.frame.numpy import NumpyFrameHelper

import numpy as np


class VideoFrameValidator:
    """
    Class to simplify the video frame validation process.
    """
    
    @staticmethod
    def frame_is_moviepy_frame(
        frame: np.ndarray
    ):
        """
        Check if the provided 'frame' (that is a numpy array) is
        recognize as a normal or mask frame of the moviepy library.
        """
        return (
            VideoFrameValidator.frame_is_video_frame(frame) or
            VideoFrameValidator.frame_is_mask_frame(frame)
        )

    @staticmethod
    def frame_is_video_frame(
        frame: np.ndarray
    ):
        """
        Checks if the provided 'frame' numpy array is recognized as
        a frame of a normal moviepy video with values between 0 and
        255.

        This numpy array should represent a frame of a clip.
        
        A non-modified clip is '.ndim = 3' and '.dtype = np.uint8'.
        """
        return NumpyFrameHelper.is_rgb_not_normalized(frame)
        
    @staticmethod
    def frame_is_mask_frame(
        frame: np.ndarray
    ):
        """
        Checks if the provided 'frame' numpy array is recognized as
        an original moviepy mask clip with values between 0 and 1.
        This numpy array should represent a frame of a mask clip.
        
        A non-modified mask clip is '.ndim = 2' and '.dtype = np.float64'.
        """
        return NumpyFrameHelper.is_alpha_normalized(frame)