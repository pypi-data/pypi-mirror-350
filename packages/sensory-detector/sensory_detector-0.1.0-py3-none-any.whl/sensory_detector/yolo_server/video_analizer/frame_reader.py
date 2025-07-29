# project_root/yolo_server/frame_reader.py
import av
import numpy as np
import logging
import os
from typing import Generator, Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class FrameReadError(Exception):
    """Custom exception for errors during frame reading."""
    pass

class FrameReader:
    """
    Reads video frames from a file using pyAV and yields them.
    Acts as a context manager for resource handling.
    """
    def __init__(self, video_path: str):
        self.video_path = video_path
        self._container: Optional[av.container.InputContainer] = None
        self._stream: Optional[av.Stream] = None
        self._frame_iterator: Optional[Generator] = None # To hold the pyAV frame generator
        self._frame_count = 0

        if not os.path.exists(video_path):
             logger.error(f"Video file not found for reading: {video_path}")
             raise FileNotFoundError(f"Video file not found: {video_path}")

        logger.debug(f"FrameReader initialized for {video_path}")

    def __enter__(self) -> 'FrameReader':
        """Opens the video container and prepares for reading."""
        logger.debug(f"Opening video container: {self.video_path}")
        try:
            # av.open is blocking
            self._container = av.open(self.video_path)
            # Find the first video stream - blocking
            try:
                self._stream = self._container.streams.video[0]
                logger.debug(f"Video stream found. Codec: {self._stream.codec_context.codec.name}, FPS: {self._stream.average_rate}, Frames: {self._stream.frames if self._stream.frames > 0 else 'unknown'}")
            except IndexError:
                logger.error(f"No video stream found in {self.video_path}")
                self._container.close() # Close if stream not found
                self._container = None
                raise FrameReadError(f"No video stream found in file: {self.video_path}")

            # Create the frame iterator
            # container.decode is blocking and yields frames
            self._frame_iterator = self._container.decode(self._stream)
            logger.debug("Frame iterator created.")

            return self

        except av.AVError as e:
            logger.error(f"Error opening video file {self.video_path} with pyAV: {e}", exc_info=True)
            self.close() # Ensure cleanup
            raise FrameReadError(f"Could not open video file {self.video_path}. Is it a valid video?") from e
        except Exception as e:
            logger.error(f"An unexpected error occurred during opening video {self.video_path}: {e}", exc_info=True)
            self.close() # Ensure cleanup
            raise FrameReadError(f"An unexpected error occurred opening video.") from e

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures the video container is closed."""
        logger.debug(f"Closing video container for {self.video_path}.")
        self.close()
        # Return False to propagate any exceptions that occurred in the 'with' block
        return False

    def read_frames(self) -> Generator[Tuple[int, np.ndarray, float], None, None]:
        """
        Generator that yields decoded video frames as numpy arrays
        along with frame index and timestamp.

        Yields:
            Tuple[int, np.ndarray, float]: (frame_index, frame_data_as_numpy_array, timestamp_in_seconds)

        Raises:
            StopIteration: When no more frames are available.
            FrameReadError: If an error occurs during decoding a frame.
        """
        if self._frame_iterator is None or self._stream is None:
             logger.error("read_frames called before video container was opened.")
             raise FrameReadError("Video container not opened. Use FrameReader within a 'with' statement.")

        while True:
            try:
                frame = next(self._frame_iterator)
                try: img = frame.to_ndarray(format="bgr24")
                except Exception as e: continue 
                yield frame.index, img, frame.time
                
            except StopIteration:
                logger.debug(f"End of video stream reached for {self.video_path}.")
                break 

            except av.AVError as e:
                logger.error(f"Error decoding frame {self._frame_count} from {self.video_path} with pyAV: {e}", exc_info=True)

                continue 

            except Exception as e:
                logger.error(f"An unexpected error occurred processing frame {self._frame_count} from {self.video_path}: {e}", exc_info=True)

                continue

    def close(self):
        """Closes the pyAV container and releases resources."""
        if self._container:
            try:
                self._container.close()
                logger.debug(f"Video container for {self.video_path} closed.")
            except Exception as e:
                logger.warning(f"Error closing video container for {self.video_path}: {e}", exc_info=True)
            self._container = None
            self._stream = None
            self._frame_iterator = None # Dereference iterator too

    def __del__(self):
        """Ensures cleanup on object deletion."""
        self.close()