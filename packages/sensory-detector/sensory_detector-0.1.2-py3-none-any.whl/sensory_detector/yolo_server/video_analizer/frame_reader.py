# project_root/yolo_server/frame_reader.py
import av
import numpy as np
import logging
import os
from typing import Generator, Tuple, Optional
from pathlib import Path
try:                                # PyAV >= 11
    from av.error import FFmpegError as _AVError
except (ImportError, AttributeError):
    # «старый» PyAV
    _AVError = getattr(av, "AVError", OSError)
AVError = _AVError    

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
        
    def __enter__(self) -> "FrameReader":
        try:
            self._container = av.open(self.video_path)        # blocking
            self._stream = self._container.streams.video[0]   # may raise IndexError
            self._frame_iter = self._container.decode(self._stream)
            logger.debug(
                "Opened %s: codec=%s, fps=%s",
                self.video_path,
                self._stream.codec_context.codec.name,
                self._stream.average_rate,
            )
            return self
        except IndexError as e:
            self.close()
            raise FrameReadError(f"No video stream in file {self.video_path}") from e
        except AVError as e:
            self.close()
            raise FrameReadError(f"PyAV cannot open {self.video_path}: {e}") from e
        except Exception:
            self.close()
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures the video container is closed."""
        logger.debug(f"Closing video container for {self.video_path}.")
        self.close()
        # Return False to propagate any exceptions that occurred in the 'with' block
        return False
    
    def read_frames(self) -> Generator[Tuple[int, np.ndarray, float], None, None]:
        """Yields (idx, frame_bgr, ts_seconds)."""
        if self._frame_iter is None:
            raise FrameReadError("FrameReader must be used inside a `with` block")

        for idx, frame in enumerate(self._frame_iter):
            try:
                img = frame.to_ndarray(format="bgr24")
                ts = float(frame.time or 0.0)
                yield idx, img, ts
            except AVError as e:
                logger.warning("AVError on frame %s: %s (skipped)", idx, e)
                continue
            except Exception as e:
                logger.warning("Unexpected error on frame %s: %s (skipped)", idx, e)
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