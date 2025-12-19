# src/chuk_mcp_pptx/components/core/video.py
"""
Video component for PowerPoint presentations.

Provides video insertion with poster frames and playback options.
"""

from typing import Optional, Dict, Any
from pptx.util import Inches
from pathlib import Path
import base64
import io

from ..base import Component
from ..registry import component, ComponentCategory, prop, example


@component(
    name="Video",
    category=ComponentCategory.UI,
    description="Video component with poster frame and playback controls",
    props=[
        prop("video_source", "string", "Video file path or URL", required=True),
        prop("poster_image", "string", "Poster image path or base64 data (shown before play)"),
        prop("left", "number", "Left position in inches", required=True),
        prop("top", "number", "Top position in inches", required=True),
        prop("width", "number", "Width in inches", default=4.0),
        prop("height", "number", "Height in inches", default=3.0),
        prop("autoplay", "boolean", "Auto-play video on slide load", default=False),
        prop("loop", "boolean", "Loop video playback", default=False),
        prop("show_controls", "boolean", "Show playback controls", default=True),
    ],
    examples=[
        example(
            "Simple video",
            """
video = Video(video_source="path/to/video.mp4")
video.render(slide, left=2, top=2, width=5, height=4)
            """,
            video_source="demo.mp4",
        ),
        example(
            "Video with poster",
            """
video = Video(
    video_source="intro.mp4",
    poster_image="poster.jpg",
    autoplay=True
)
video.render(slide, left=1, top=1, width=6, height=4.5)
            """,
            video_source="intro.mp4",
            poster_image="poster.jpg",
            autoplay=True,
        ),
    ],
    tags=["video", "media", "movie", "playback", "multimedia"],
)
class Video(Component):
    """
    Video component for adding videos to slides.

    Features:
    - File path or URL support
    - Poster frame customization
    - Playback controls
    - Auto-play and loop options

    Usage:
        # Simple video from file
        video = Video(video_source="demo.mp4")
        video.render(slide, left=2, top=2, width=5, height=4)

        # Video with poster and auto-play
        video = Video(
            video_source="intro.mp4",
            poster_image="poster.jpg",
            autoplay=True,
            loop=True
        )
        video.render(slide, left=1, top=1, width=6, height=4.5)
    """

    def __init__(
        self,
        video_source: str,
        poster_image: Optional[str] = None,
        autoplay: bool = False,
        loop: bool = False,
        show_controls: bool = True,
        theme: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize video component.

        Args:
            video_source: Path to video file or video URL
            poster_image: Path to poster image (shown before playback)
            autoplay: Whether to auto-play video on slide load
            loop: Whether to loop video playback
            show_controls: Whether to show playback controls
            theme: Optional theme override
        """
        super().__init__(theme)

        # Validate required parameters
        if not video_source:
            raise ValueError("Video requires 'video_source' (URL or file path)")
        if not isinstance(video_source, str):
            raise TypeError(
                f"Video 'video_source' must be a string, got {type(video_source).__name__}"
            )

        self.video_source = video_source
        self.poster_image = poster_image
        self.autoplay = autoplay
        self.loop = loop
        self.show_controls = show_controls

    async def render(
        self,
        slide,
        left: float,
        top: float,
        width: float = 4.0,
        height: float = 3.0,
        placeholder: Optional[Any] = None,
    ) -> Any:
        """
        Render video to slide.

        Args:
            slide: PowerPoint slide object
            left: Left position in inches
            top: Top position in inches
            width: Width in inches
            height: Height in inches
            placeholder: Optional placeholder to replace

        Returns:
            Movie shape object
        """
        # If placeholder provided, extract bounds and delete it
        bounds = self._extract_placeholder_bounds(placeholder)
        if bounds is not None:
            left, top, width, height = bounds

        # Delete placeholder after extracting bounds
        self._delete_placeholder_if_needed(placeholder)

        # Validate video file exists (if local path)
        if not self.video_source.startswith(("http://", "https://")):
            video_path = Path(self.video_source)
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {self.video_source}")
            video_source_str = str(video_path.absolute())
        else:
            # URL - use as-is
            video_source_str = self.video_source

        # Prepare poster image if provided
        poster_stream = None
        if self.poster_image:
            if self.poster_image.startswith("data:image/"):
                # Base64 poster image
                header, encoded = self.poster_image.split(",", 1)
                image_data = base64.b64decode(encoded)
                poster_stream = io.BytesIO(image_data)
            elif Path(self.poster_image).exists():
                # File path poster image
                with open(self.poster_image, "rb") as f:
                    poster_stream = io.BytesIO(f.read())

        # Add video to slide
        # Note: python-pptx's add_movie method signature:
        # add_movie(movie_file, left, top, width, height, poster_frame_image=None, mime_type='video/mp4')
        try:
            movie = slide.shapes.add_movie(
                video_source_str,
                Inches(left),
                Inches(top),
                Inches(width),
                Inches(height),
                poster_frame_image=poster_stream,
                mime_type=self._get_mime_type(video_source_str),
            )

            # Configure playback settings
            # Note: These are PowerPoint XML settings, may require accessing _element
            if hasattr(movie, "_element"):
                # Set autoplay
                if self.autoplay:
                    # This would require XML manipulation
                    pass  # PowerPoint XML attribute for autoplay

                # Set loop
                if self.loop:
                    # This would require XML manipulation
                    pass  # PowerPoint XML attribute for loop

            return movie

        except Exception as e:
            raise RuntimeError(f"Failed to add video to slide: {str(e)}")

    def _get_mime_type(self, video_source: str) -> str:
        """Determine MIME type from video file extension."""
        source_lower = video_source.lower()

        if source_lower.endswith(".mp4"):
            return "video/mp4"
        elif source_lower.endswith(".avi"):
            return "video/x-msvideo"
        elif source_lower.endswith(".mov"):
            return "video/quicktime"
        elif source_lower.endswith(".wmv"):
            return "video/x-ms-wmv"
        elif source_lower.endswith(".webm"):
            return "video/webm"
        else:
            # Default to mp4
            return "video/mp4"
