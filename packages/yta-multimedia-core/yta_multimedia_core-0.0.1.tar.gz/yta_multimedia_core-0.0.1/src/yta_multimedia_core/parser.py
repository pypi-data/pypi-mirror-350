from yta_multimedia_core.video.mp_video import MPVideo
from yta_file.handler import FileHandler
from yta_validation import PythonValidator
from yta_validation.parameter import ParameterValidator
from moviepy import VideoFileClip
from moviepy.Clip import Clip
from typing import Union


class VideoParser:
    """
    Class to simplify the way we parse video parameters.
    """

    @staticmethod
    def to_moviepy(
        video: Union[str, Clip],
        do_include_mask: bool = False,
        do_calculate_real_duration: bool = False
    ):
        """
        This method is a helper to turn the provided 'video' to a moviepy
        video type. If it is any of the moviepy video types specified in
        method declaration, it will be returned like that. If not, it will
        be load as a VideoFileClip if possible, or will raise an Exception
        if not.

        The 'do_include_mask' parameter includes the mask in the video if
        True value provided. The 'do_check_duration' parameter checks and
        updates the real video duration to fix a bug in moviepy lib.
        """
        # TODO: Maybe check if subclass of VideoClip
        ParameterValidator.validate_mandatory_instance_of('video', video, [str, Clip])
        ParameterValidator.validate_mandatory_bool('do_include_mask', do_include_mask)
        ParameterValidator.validate_mandatory_bool('do_calculate_real_duration', do_calculate_real_duration)
        
        if PythonValidator.is_string(video):
            # TODO: Maybe validate the content and not only the
            # extension (?)
            if not FileHandler.is_video_file(video):
                raise Exception('The "video" parameter provided is not a valid video filename.')
            
            video = VideoFileClip(video, has_mask = do_include_mask)

        # TODO: This below just adds a mask attribute but
        # without fps and empty, so it doesn't make sense
        # if do_include_mask and not video.mask:
        #     video = video.add_mask()

        # Due to problems with decimal values I'm forcing
        # to obtain the real duration again, making the
        # system slower but avoiding fatal errors
        # TODO: I hope one day I don't need this below
        return (
            video
            if not do_calculate_real_duration else
            MPVideo(video).video
        )

        # TODO: Remove this old code below if no problems
        # with the import at the begining of the file
        if do_calculate_real_duration:
            from yta_multimedia.video import MPVideo

            video = MPVideo(video).video

        return video