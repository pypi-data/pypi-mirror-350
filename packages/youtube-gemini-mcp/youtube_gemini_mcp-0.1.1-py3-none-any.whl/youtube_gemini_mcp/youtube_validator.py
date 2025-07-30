"""YouTube URL validation and metadata extraction."""

import logging
from typing import Any, Dict
from urllib.parse import parse_qs, urlparse

import yt_dlp

logger = logging.getLogger(__name__)


class YouTubeValidator:
    """YouTube URL validation and metadata extraction."""

    def __init__(self) -> None:
        """Initialize validator."""
        logger.info("YouTubeValidator initialized")

    def validate_and_normalize_url(self, url: str) -> Dict[str, Any]:
        """Validate and normalize YouTube URL."""
        try:
            # Extract video ID from various YouTube URL formats
            if "youtube.com/watch" in url:
                parsed = urlparse(url)
                video_id = parse_qs(parsed.query).get("v", [None])[0]
            elif "youtu.be/" in url:
                video_id = url.split("youtu.be/")[1].split("?")[0]
            elif len(url) == 11:  # Direct video ID
                video_id = url
                url = f"https://www.youtube.com/watch?v={video_id}"
            else:
                raise ValueError("Invalid YouTube URL format")

            if not video_id:
                raise ValueError("Could not extract video ID")

            normalized_url = f"https://www.youtube.com/watch?v={video_id}"

            return {
                "valid": True,
                "video_id": video_id,
                "normalized_url": normalized_url,
                "original_url": url,
            }

        except Exception as e:
            return {"valid": False, "error": str(e), "original_url": url}

    def extract_metadata(self, youtube_url: str) -> Dict[str, Any]:
        """Extract video metadata using yt-dlp (without downloading)."""
        try:
            validation = self.validate_and_normalize_url(youtube_url)
            if not validation["valid"]:
                raise ValueError(f"Invalid URL: {validation['error']}")

            # Extract metadata without downloading
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "extractflat": False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(validation["normalized_url"], download=False)

                # Check video duration (max 2 hours for Gemini)
                duration = info.get("duration", 0)
                if duration > 7200:  # 2 hours
                    logger.warning(
                        f"Video duration {duration}s exceeds recommended 2-hour limit"
                    )

                return {
                    "success": True,
                    "video_metadata": {
                        "video_id": validation["video_id"],
                        "title": info.get("title", ""),
                        "channel": info.get("uploader", ""),
                        "duration": duration,
                        "duration_formatted": self._format_duration(duration),
                        "upload_date": info.get("upload_date", ""),
                        "view_count": info.get("view_count", 0),
                        "description": info.get("description", "")[:500],  # Truncate
                        "normalized_url": validation["normalized_url"],
                    },
                }

        except Exception as e:
            logger.error(f"Metadata extraction failed for {youtube_url}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "metadata_extraction_error",
            }

    def _format_duration(self, seconds: int) -> str:
        """Format duration in seconds to HH:MM:SS or MM:SS."""
        if seconds < 3600:  # Less than 1 hour
            minutes, seconds = divmod(seconds, 60)
            return f"{minutes:02d}:{seconds:02d}"
        else:  # 1 hour or more
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def check_gemini_compatibility(self, youtube_url: str) -> Dict[str, Any]:
        """Check if YouTube video is compatible with Gemini API requirements."""
        try:
            metadata_result = self.extract_metadata(youtube_url)
            if not metadata_result["success"]:
                return metadata_result

            metadata = metadata_result["video_metadata"]
            duration = metadata["duration"]

            # Gemini API limits
            compatibility_checks = {
                "duration_ok": duration <= 7200,  # 2 hours max
                "public_video": True,  # Assume public if metadata extracted successfully
                "supported_format": True,  # YouTube videos are supported
            }

            compatible = all(compatibility_checks.values())

            warnings = []
            if duration > 7200:
                warnings.append(
                    f"Video duration ({metadata['duration_formatted']}) exceeds 2-hour Gemini limit"
                )

            return {
                "success": True,
                "compatible": compatible,
                "checks": compatibility_checks,
                "warnings": warnings,
                "metadata": metadata,
            }

        except Exception as e:
            logger.error(f"Compatibility check failed for {youtube_url}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "compatibility_check_error",
            }
