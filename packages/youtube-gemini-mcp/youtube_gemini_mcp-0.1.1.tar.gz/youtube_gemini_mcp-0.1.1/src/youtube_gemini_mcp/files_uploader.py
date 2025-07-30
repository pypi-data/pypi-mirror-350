"""Google Files API integration for local video uploads."""

import logging
import os
import time
from typing import Any, Dict, Optional

from google import genai

logger = logging.getLogger(__name__)


class FilesUploader:
    """Google Files API integration for local video uploads."""

    def __init__(self, genai_client: genai.Client):
        """Initialize with Gemini client."""
        self.client = genai_client
        logger.info("FilesUploader initialized")

    def upload_video_file(
        self, video_path: str, display_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload local video file to Google Files API."""
        try:
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")

            # Validate file size (2GB per file, 20GB per project)
            file_size = os.path.getsize(video_path)
            max_size = 2 * 1024 * 1024 * 1024  # 2GB limit per file

            if file_size > max_size:
                raise ValueError(f"File too large: {file_size} bytes (max: {max_size})")

            # IMPORTANT: Files are auto-deleted after 48 hours
            logger.info(
                f"Uploading {video_path} ({file_size} bytes) - will auto-delete in 48 hours"
            )

            # Upload file using CORRECTED API syntax
            uploaded_file = self.client.files.upload(path=video_path)

            logger.info(f"Uploaded video as {uploaded_file.name}")

            # Return file information
            return {
                "success": True,
                "file_id": uploaded_file.name,
                "file_uri": (
                    uploaded_file.uri if hasattr(uploaded_file, "uri") else None
                ),
                "display_name": (
                    uploaded_file.display_name
                    if hasattr(uploaded_file, "display_name")
                    else os.path.basename(video_path)
                ),
                "size_bytes": file_size,
                "upload_time": time.time(),
                "expires_in_hours": 48,
                "note": "File will be automatically deleted after 48 hours",
            }

        except Exception as e:
            logger.error(f"Failed to upload video {video_path}: {e}")
            return {"success": False, "error": str(e), "error_type": "upload_error"}

    def delete_file(self, file_id: str) -> Dict[str, Any]:
        """Delete uploaded file from Google Files API."""
        try:
            # Use CORRECTED API syntax
            self.client.files.delete(file_id)
            logger.info(f"Deleted file: {file_id}")

            return {"success": True, "file_id": file_id, "status": "deleted"}

        except Exception as e:
            logger.error(f"Failed to delete file {file_id}: {e}")
            return {"success": False, "error": str(e), "error_type": "deletion_error"}

    def get_file_info(self, file_id: str) -> Dict[str, Any]:
        """Get information about uploaded file."""
        try:
            # Use CORRECTED API syntax
            file_metadata = self.client.files.get(file_id)

            return {
                "success": True,
                "file_info": {
                    "file_id": file_metadata.name,
                    "display_name": getattr(file_metadata, "display_name", "Unknown"),
                    "mime_type": getattr(file_metadata, "mime_type", "Unknown"),
                    "size_bytes": getattr(file_metadata, "size_bytes", 0),
                    "create_time": getattr(file_metadata, "create_time", None),
                    "update_time": getattr(file_metadata, "update_time", None),
                    "expires_in_hours": 48,
                    "note": "File auto-deletes after 48 hours",
                },
            }

        except Exception as e:
            logger.error(f"Failed to get file info for {file_id}: {e}")
            return {"success": False, "error": str(e), "error_type": "file_info_error"}

    def list_files(self) -> Dict[str, Any]:
        """List all uploaded files."""
        try:
            files = self.client.files.list()

            file_list = []
            for file in files:
                file_list.append(
                    {
                        "file_id": file.name,
                        "display_name": getattr(file, "display_name", "Unknown"),
                        "mime_type": getattr(file, "mime_type", "Unknown"),
                        "size_bytes": getattr(file, "size_bytes", 0),
                        "create_time": getattr(file, "create_time", None),
                    }
                )

            return {
                "success": True,
                "files": file_list,
                "total_files": len(file_list),
                "storage_note": "All files auto-delete after 48 hours",
                "project_limit": "20GB total storage per project",
            }

        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return {"success": False, "error": str(e), "error_type": "list_files_error"}
