from yta_validation.parameter import ParameterValidator
from yta_general_utils.math.progression import Progression


SMALL_AMOUNT_TO_FIX = 0.0000000001
"""
Small amount we need to add to fix some floating
point number issues we've found. Something like
0.3333333333333326 will turn into 9 frames for a 
fps = 30 video, but this is wrong, as it should
be 10 frames and it is happening due to a minimal
floating point difference.
"""

class VideoFrameTHandler:
    """
    Class to wrap and simplify the way we handle
    video and audio frame time moments and frame
    indexes. This class is able to calculate the
    video frame time moment or index that belongs
    to an audio frame time moment or index, or
    viceversa.
    """

    @staticmethod
    def frame_time_to_frame_index(
        t: float,
        fps: float
    ) -> int:
        """
        Transform the provided 't' frame time to 
        its corresponding frame index according
        to the 'fps' provided.

        This method applies the next formula:

        int(t * fps + SMALL_AMOUNT_TO_FIX)
        """
        ParameterValidator.validate_mandatory_positive_number('t', t)
        ParameterValidator.validate_mandatory_positive_number('fps', fps)

        return int((t + SMALL_AMOUNT_TO_FIX) * fps)
    
    @staticmethod
    def frame_index_to_frame_time(
        i: int,
        fps: float
    ) -> float:
        """
        Transform the provided 'i' frame index to
        its corresponding frame time according to
        the 'fps' provided.

        This method applies the next formula:

        i * 1 / fps + SMALL_AMOUNT_TO_FIX
        """
        ParameterValidator.validate_mandatory_positive_int('i', i)
        ParameterValidator.validate_mandatory_positive_number('fps', fps)

        return i * 1 / fps + SMALL_AMOUNT_TO_FIX
    
    @staticmethod
    def get_number_of_frames(
        duration: float,
        fps: float
    ) -> int:
        """
        Get the numbers of frames with the given 'duration'
        and 'fps'.

        int(duration * fps)
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)

        return int(duration * fps)
    
    @staticmethod
    def get_video_frames_indexes_from_duration_and_fps(
        duration: float,
        fps: float
    ) -> list:
        """
        Get all the video frame indexes for a video with
        the given 'fps' and 'duration'. 
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)

        return list(range(fps * duration))
    
    @staticmethod
    def get_video_frames_indexes_from_number_of_frames(
        number_of_frames: int
    ):
        """
        Get all the video frame indexes for a video with
        the given 'number_of_frames'.
        """
        ParameterValidator.validate_mandatory_int('number_of_frames', number_of_frames)

        return list(range(number_of_frames))
    
    @staticmethod
    def get_video_frames_ts_from_duration_and_fps(
        duration: float,
        fps: float
    ):
        """
        Get all the 't' frames time moments for a video
        with the given 'fps' and 'duration'. Each 't'
        includes a small amount increased to ensure it
        fits the frame time range.
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)

        return [
            VideoFrameTHandler.frame_index_to_frame_time(i, fps)
            for i in VideoFrameTHandler.get_video_frames_indexes_from_duration_and_fps(duration, fps)
        ]
    
    @staticmethod
    def get_video_frames_ts_from_number_of_frames(
        number_of_frames: int,
        fps: float
    ):
        """
        Get all the 't' frames time moments for a video
        with the given 'number_of_frames'. Each 't'
        includes a small amount increased to ensure it
        fits the frame time range.
        """
        ParameterValidator.validate_mandatory_positive_int('number_of_frames', number_of_frames)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)

        return [
            VideoFrameTHandler.frame_index_to_frame_time(i, fps)
            for i in VideoFrameTHandler.get_video_frames_indexes_from_number_of_frames(number_of_frames)
        ]
    
    @staticmethod
    def get_frame_t_base(
        t: float,
        fps: float
    ):
        """
        Turn the provided 't' video frame time moment to
        the real base one (the one who is the start of
        the frame time interval, plus a minimum quantity
        to avoid floating point number issues) according
        to the provided 'fps'.
        """
        return VideoFrameTHandler.frame_time_to_frame_index(t, fps) / fps + SMALL_AMOUNT_TO_FIX
    
    @staticmethod
    def get_video_audio_tts_from_video_frame_t(
        video_t: float,
        video_fps: float,
        audio_fps: float
    ):
        """
        Get all the audio time moments associated to
        the given 'video' 't' time moment, as an array.

        One video time moment 't' is associated with a lot
        of video audio time 't' time moments. The amount 
        of video audio frames per video frame is calculated
        with the divions of the audio fps by the video fps.

        The result is an array of 't' video audio time
        moments that correspond to the given video 't' time
        moment.
        
        Maybe you need to turn it into a numpy array before
        using it as audio 't' time moments.
        """
        ParameterValidator.validate_mandatory_positive_number('video_t', video_t, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('video_fps', video_fps, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('audio_fps', audio_fps, do_include_zero = False)

        audio_frames_per_video_frame = int(audio_fps / video_fps)
        audio_frame_duration = 1 / audio_fps
        video_frame_duration = 1 / video_fps

        t = VideoFrameTHandler.get_frame_t_base(video_t, video_fps)

        return Progression(t, t + video_frame_duration - audio_frame_duration, audio_frames_per_video_frame).values
    
    @staticmethod
    def get_video_frame_t_from_video_audio_frame_t(
        audio_t: float,
        video_fps: float
    ):
        """
        Get the video frame time moment t from the given
        video audio frame time moment 'audio_t'. A video
        time moment has a lot of different audio time
        moments attached, so the given 'audio_t' can be
        only in one video 't' time moment.
        """
        ParameterValidator.validate_mandatory_positive_number('audio_t', audio_t, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('video_fps', video_fps, do_include_zero = False)

        return VideoFrameTHandler.get_frame_t_base(audio_t , video_fps)
    
    @staticmethod
    def get_video_frame_index_from_video_audio_frame_index(
        audio_index: int,
        video_fps: float,
        audio_fps: float
    ):
        """
        Get the video frame index from the given video
        audio frame index 'audio_index'.
        """
        ParameterValidator.validate_mandatory_positive_number('audio_index', audio_index, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('video_fps', video_fps, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('audio_fps', audio_fps, do_include_zero = False)

        return round(audio_index * (video_fps / audio_fps))
    
    @staticmethod
    def get_video_frame_t_from_video_audio_frame_index(
        audio_index: int,
        video_fps: float,
        audio_fps: float
    ):
        """
        Get the video frame time moment t from the given
        video audio frame index 'audio_index'.
        """
        ParameterValidator.validate_mandatory_positive_number('audio_index', audio_index, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('video_fps', video_fps, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('audio_fps', audio_fps, do_include_zero = False)

        return VideoFrameTHandler.frame_index_to_frame_time(
            VideoFrameTHandler.get_video_frame_index_from_video_audio_frame_index(
                audio_index,
                video_fps,
                audio_fps
            ),
            video_fps
        )
    
    @staticmethod
    def get_video_frame_index_from_video_audio_frame_t(
        audio_t: float,
        video_fps: float,
        audio_fps: float
    ):
        """
        Get the video frame index from the given video
        audio frame time moment 'audio_t'.
        """
        ParameterValidator.validate_mandatory_positive_number('audio_t', audio_t, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('video_fps', video_fps, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('audio_fps', audio_fps, do_include_zero = False)

        return VideoFrameTHandler.get_video_frame_index_from_video_audio_frame_index(
            VideoFrameTHandler.frame_time_to_frame_index(
                audio_t,
                audio_fps
            ),
            video_fps,
            audio_fps
        )
