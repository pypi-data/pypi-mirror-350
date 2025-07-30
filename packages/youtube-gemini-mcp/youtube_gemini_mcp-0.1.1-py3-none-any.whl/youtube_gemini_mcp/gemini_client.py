"""Google Gemini API client for video analysis."""

import logging
import time
from typing import Any, Dict, List, Optional

from google import genai
from google.genai import types

from .session_manager import VideoSession

logger = logging.getLogger(__name__)


class GeminiClient:
    """Google Gemini API client for video analysis."""

    def __init__(self, api_key: str):
        """Initialize Gemini client."""
        self.client = genai.Client(api_key=api_key)
        logger.info("GeminiClient initialized")

    def analyze_youtube_video_direct(
        self, youtube_url: str, user_prompt: str, timestamp_range: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze YouTube video directly using URL (PREFERRED METHOD)."""
        try:
            # Build prompt parts for direct YouTube URL analysis
            prompt_parts = []

            # Add YouTube video directly via URL
            prompt_parts.append(
                types.Part(file_data=types.FileData(file_uri=youtube_url))
            )

            # Add timestamp context if provided
            if timestamp_range:
                prompt_parts.append(
                    types.Part(text=f"Focus on timestamp range: {timestamp_range}")
                )

            # Add user prompt
            prompt_parts.append(types.Part(text=user_prompt))

            # Generate response using Gemini 2.5 Pro
            response = self.client.models.generate_content(
                model="models/gemini-2.5-pro-preview-05-06",
                contents=types.Content(parts=prompt_parts),
            )

            return {
                "success": True,
                "analysis_response": response.text,
                "method": "youtube_url_direct",
                "video_url": youtube_url,
            }

        except Exception as e:
            logger.error(f"Direct YouTube analysis failed for {youtube_url}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "youtube_direct_error",
            }

    def upload_local_video_file(self, video_path: str, display_name: str) -> Any:
        """Upload local video to Google Files API (for non-YouTube videos)."""
        try:
            # Upload video file using Files API
            video_file = self.client.files.upload(path=video_path)
            logger.info(f"Uploaded video {video_path} as {video_file.name}")

            # Wait for processing if needed
            while (
                hasattr(video_file, "state") and video_file.state.name == "PROCESSING"
            ):
                time.sleep(10)
                video_file = self.client.files.get(video_file.name)

            if hasattr(video_file, "state") and video_file.state.name == "FAILED":
                raise ValueError(f"Video processing failed: {video_file.state}")

            return video_file.name

        except Exception as e:
            logger.error(f"Failed to upload video {video_path}: {e}")
            raise

    def analyze_uploaded_video(
        self, file_id: str, user_prompt: str, timestamp_range: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze uploaded video using Files API (for local videos)."""
        try:
            # Build prompt parts for uploaded video analysis
            prompt_parts = []

            # Add uploaded video file reference
            video_file = self.client.files.get(file_id)
            prompt_parts.append(video_file)

            # Add timestamp context if provided
            if timestamp_range:
                prompt_parts.append(
                    types.Part(text=f"Focus on timestamp range: {timestamp_range}")
                )

            # Add user prompt
            prompt_parts.append(types.Part(text=user_prompt))

            # Generate response
            response = self.client.models.generate_content(
                model="models/gemini-2.5-pro-preview-05-06",
                contents=types.Content(parts=prompt_parts),
            )

            return {
                "success": True,
                "analysis_response": response.text,
                "method": "files_api",
                "file_id": file_id,
            }

        except Exception as e:
            logger.error(f"Uploaded video analysis failed for {file_id}: {e}")
            return {"success": False, "error": str(e), "error_type": "files_api_error"}

    def analyze_video_with_conversation(
        self,
        session: VideoSession,
        user_prompt: str,
        timestamp_range: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Analyze video using conversation context."""
        try:
            # Build conversation context
            conversation_context = self.build_conversation_context(session)

            # Build prompt parts
            prompt_parts = []

            # Add video reference (YouTube URL or Files API)
            if session.youtube_url:
                # Use direct YouTube URL method (PREFERRED)
                prompt_parts.append(
                    types.Part(file_data=types.FileData(file_uri=session.youtube_url))
                )
            elif session.google_file_id:
                # Use Files API for uploaded local videos
                video_file = self.client.files.get(session.google_file_id)
                prompt_parts.append(video_file)
            else:
                raise ValueError("No video source available in session")

            # Add conversation context
            if conversation_context:
                prompt_parts.append(
                    types.Part(
                        text=f"Previous conversation context:\n{conversation_context}"
                    )
                )

            # Add timestamp context if provided
            if timestamp_range:
                prompt_parts.append(
                    types.Part(text=f"Focus on timestamp range: {timestamp_range}")
                )

            # Add user prompt
            prompt_parts.append(types.Part(text=f"User request: {user_prompt}"))

            # Generate response
            response = self.client.models.generate_content(
                model="models/gemini-2.5-pro-preview-05-06",
                contents=types.Content(parts=prompt_parts),
            )

            return {
                "success": True,
                "analysis_response": response.text,
                "conversation_length": len(session.conversation_history),
                "method": "youtube_url_direct" if session.youtube_url else "files_api",
            }

        except Exception as e:
            logger.error(f"Conversational video analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "conversation_analysis_error",
            }

    def build_conversation_context(self, session: VideoSession) -> str:
        """Build conversation context from session history."""
        try:
            if not session.conversation_history:
                return ""

            context_parts = []

            # Add session description
            if session.description:
                context_parts.append(f"Session Context: {session.description}")

            # Add video metadata if available
            if session.youtube_metadata:
                metadata = session.youtube_metadata
                context_parts.append(
                    f"Video: {metadata.get('title', 'Unknown')} "
                    f"by {metadata.get('channel', 'Unknown')} "
                    f"({metadata.get('duration_formatted', 'Unknown duration')})"
                )

            # Add recent conversation history (last 5 exchanges)
            recent_history = session.conversation_history[-5:]
            for i, exchange in enumerate(recent_history):
                if exchange.get("type") == "analysis_call":
                    context_parts.append(
                        f"Previous Q{i+1}: {exchange.get('prompt', '')}"
                    )
                    # Truncate long responses
                    response = exchange.get("response", "")
                    if len(response) > 200:
                        response = response[:200] + "..."
                    context_parts.append(f"Previous A{i+1}: {response}")

            return "\n".join(context_parts)

        except Exception as e:
            logger.error(f"Failed to build conversation context: {e}")
            return ""

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about available Gemini models."""
        try:
            models = self.client.models.list()
            model_list = []

            for model in models:
                model_list.append(
                    {
                        "name": model.name,
                        "display_name": getattr(model, "display_name", "Unknown"),
                        "description": getattr(model, "description", "No description"),
                        "supported_generation_methods": getattr(
                            model, "supported_generation_methods", []
                        ),
                    }
                )

            return {
                "success": True,
                "models": model_list,
                "default_model": "models/gemini-2.5-pro-preview-05-06",
            }

        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            return {"success": False, "error": str(e), "error_type": "model_info_error"}
