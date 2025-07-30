from yta_multimedia_core.video.frame.validator import VideoFrameValidator
# TODO: Is this 'yta_image' strictly needed (?)
from yta_image.parser import ImageParser
from yta_constants.enum import YTAEnum as Enum

import numpy as np


class FrameMaskingMethod(Enum):
    """
    Method to turn a frame into a mask frame.
    """

    MEAN = 'mean'
    """
    Calculate the mean value of the RGB pixel color
    values and uses it as a normalized value between
    0.0 and 1.0 to set as transparency.
    """
    PURE_BLACK_AND_WHITE = 'pure_black_and_white'
    """
    Apply a threshold and turn pixels into pure black
    and white pixels, setting them to pure 1.0 or 0.0
    values to be completely transparent or opaque.
    """

    # TODO: Add more methods
    # TODO: Create a method that applies a 'remove_background'
    # and then the remaining shape as a mask that can be zoomed
    # so we obtain a nice effect

    def to_mask_frame(
        self,
        frame: np.ndarray
    ):
        """
        Process the provided video normal 'frame' according to this
        type of masking processing method and turns it into a frame
        that can be used as a mask frame.
        """
        frame = ImageParser.to_numpy(frame)

        if not VideoFrameValidator.frame_is_video_frame(frame):
            raise Exception('The provided "frame" is not actually a moviepy normal video frame.')

        # TODO: I think this should be lambda or it will be doing
        # the calculations even when we don't want to
        return {
            FrameMaskingMethod.MEAN: lambda: np.mean(frame, axis = -1) / 255.0,
            FrameMaskingMethod.PURE_BLACK_AND_WHITE: lambda: pure_black_and_white_image_to_moviepy_mask_numpy_array(frame_to_pure_black_and_white_image(frame))
        }[self]()
    

"""
Some utils below.
"""

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]

def is_pure_black_and_white_image(
    image
):
    """
    Check if the provided 'image' only contains pure 
    black ([0, 0, 0]) and white ([255, 255, 255]) colors.
    """
    image = ImageParser.to_numpy(image)

    return (
        False 
        # Check if some color is not pure black or white
        if np.any(~np.all((image == WHITE) | (image == BLACK), axis = -1)) else
        True
    )

# TODO: Should I combine these 2 methods below in only 1 (?)
def pure_black_and_white_image_to_moviepy_mask_numpy_array(
    image
):
    """
    Turn the received 'image' (that must be a pure black
    and white image) to a numpy array that can be used as
    a moviepy mask (by using ImageClip).

    This is useful for static processed images that we 
    want to use as masks, such as frames to decorate our
    videos.
    """
    image = ImageParser.to_numpy(image)

    if not is_pure_black_and_white_image(image):
        raise Exception(f'The provided "image" parameter "{str(image)}" is not a black and white image.')

    # Image to a numpy parseable as moviepy mask
    mask = np.zeros(image.shape[:2], dtype = int)   # 3col to 1col
    mask[np.all(image == WHITE, axis = -1)] = 1     # white to 1 value

    return mask

def frame_to_pure_black_and_white_image(
    frame: np.ndarray
):
    """
    Process the provided moviepy clip mask frame (that
    must have values between 0.0 and 1.0) or normal clip
    frame (that must have values between 0 and 255) and
    convert it into a pure black and white image (an
    image that contains those 2 colors only).

    This method returns a not normalized numpy array of only
    2 colors (pure white [255, 255, 255] and pure black
    [0, 0, 0]), perfect to turn into a mask for moviepy clips.

    This is useful when handling an alpha transition video 
    that can include (or not) an alpha layer but it is also
    clearly black and white so you transform it into a mask
    to be applied on a video clip.
    """
    frame = ImageParser.to_numpy(frame)

    if not VideoFrameValidator.frame_is_moviepy_frame(frame):
        raise Exception('The provided "frame" parameter is not a moviepy mask clip frame nor a normal clip frame.')
    
    if VideoFrameValidator.frame_is_video_frame(frame):
        # TODO: Process it with some threshold to turn it
        # into pure black and white image (only those 2
        # colors) to be able to transform them into a mask.
        threshold = 220
        white_pixels = np.all(frame >= threshold, axis = -1)

        # Image to completely and pure black
        new_frame = np.array(frame)
        
        # White pixels to pure white
        new_frame[white_pixels] = WHITE
        new_frame[~white_pixels] = BLACK
    elif VideoFrameValidator.frame_is_mask_frame(frame):
        transparent_pixels = frame == 1

        new_frame = np.array(frame)
        
        # Transparent pixels to pure white
        new_frame[transparent_pixels] = WHITE
        new_frame[~transparent_pixels] = BLACK

    return new_frame