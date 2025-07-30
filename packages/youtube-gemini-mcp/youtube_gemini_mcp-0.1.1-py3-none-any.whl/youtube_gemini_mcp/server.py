"""Main FastMCP server for YouTube Gemini video analysis."""

import logging
import os
import sys
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from mcp.server import FastMCP

from .files_uploader import FilesUploader
from .gemini_client import GeminiClient
from .session_manager import SessionManager
from .youtube_validator import YouTubeValidator

# Load environment variables
load_dotenv()

# Configure logging (CRITICAL: Use exact same format as openai-image-mcp)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
    force=True,
)

logger = logging.getLogger(__name__)
logger.info("YouTube Gemini MCP Server initializing...")

# Create FastMCP server (CRITICAL: Use exact same pattern)
mcp = FastMCP("youtube-gemini-mcp")

# Global instances (CRITICAL: Use exact same singleton pattern)
session_manager: Optional[SessionManager] = None
gemini_client: Optional[GeminiClient] = None
youtube_validator: Optional[YouTubeValidator] = None
files_uploader: Optional[FilesUploader] = None


def get_session_manager() -> SessionManager:
    """Get or create session manager instance."""
    global session_manager
    if session_manager is None:
        max_sessions = int(os.getenv("MCP_MAX_SESSIONS", "50"))
        session_timeout = int(os.getenv("MCP_SESSION_TIMEOUT", "7200")) // 3600
        session_manager = SessionManager(
            max_sessions=max_sessions, session_timeout_hours=session_timeout
        )
        logger.info("SessionManager initialized")
    return session_manager


def get_gemini_client() -> GeminiClient:
    """Get or create Gemini client instance."""
    global gemini_client
    if gemini_client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("CRITICAL: GOOGLE_API_KEY environment variable is required")
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        gemini_client = GeminiClient(api_key=api_key)
        logger.info("GeminiClient initialized")
    return gemini_client


def get_youtube_validator() -> YouTubeValidator:
    """Get or create YouTube validator instance."""
    global youtube_validator
    if youtube_validator is None:
        youtube_validator = YouTubeValidator()
        logger.info("YouTubeValidator initialized")
    return youtube_validator


def get_files_uploader() -> FilesUploader:
    """Get or create Files uploader instance."""
    global files_uploader
    if files_uploader is None:
        client = get_gemini_client()
        files_uploader = FilesUploader(client.client)
        logger.info("FilesUploader initialized")
    return files_uploader


# CRITICAL: Every MCP tool must use this exact error handling pattern
@mcp.tool()
def create_video_session(
    description: str,
    video_source: str,
    model: str = "gemini-2.5-pro-preview-05-06",
    session_name: Optional[str] = None,
    source_type: str = "youtube_url",
) -> Dict[str, Any]:
    """Create new conversational video analysis session.

    Args:
        description: Session context/purpose
        video_source: YouTube URL or local video file path
        model: Gemini model to use
        session_name: Optional friendly name
        source_type: "youtube_url" (default) or "local_file"
    """
    try:
        manager = get_session_manager()

        # Validate video source based on type
        if source_type == "youtube_url":
            validator = get_youtube_validator()
            validation = validator.validate_and_normalize_url(video_source)
            if not validation["valid"]:
                return {
                    "success": False,
                    "error": f"Invalid YouTube URL: {validation['error']}",
                    "error_type": "invalid_youtube_url",
                }
            video_source = validation["normalized_url"]

        # Create session
        result = manager.create_session(
            description=description,
            video_source=video_source,
            model=model,
            session_name=session_name,
            source_type=source_type,
        )

        if result["success"] and source_type == "youtube_url":
            # Extract metadata for YouTube videos
            validator = get_youtube_validator()
            metadata_result = validator.extract_metadata(video_source)
            if metadata_result["success"]:
                # Update session with metadata
                session_id = result["session_id"]
                manager.update_session(
                    session_id, {"youtube_metadata": metadata_result["video_metadata"]}
                )
                result["video_info"] = metadata_result["video_metadata"]
                result["processing_method"] = "youtube_url_direct"

        return result

    except Exception as e:
        logger.error(f"Failed to create video session: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "session_creation_error",
        }


@mcp.tool()
def analyze_video_in_session(
    session_id: str, prompt: str, timestamp_range: Optional[str] = None
) -> Dict[str, Any]:
    """Analyze video within session context.

    Args:
        session_id: UUID of existing session
        prompt: Analysis question/instruction
        timestamp_range: Optional "MM:SS-MM:SS" for segment analysis
    """
    try:
        manager = get_session_manager()
        session = manager.get_session(session_id)

        if not session:
            return {
                "success": False,
                "error": f"Session {session_id} not found",
                "error_type": "session_not_found",
            }

        # Analyze video using Gemini
        client = get_gemini_client()
        analysis_result = client.analyze_video_with_conversation(
            session=session, user_prompt=prompt, timestamp_range=timestamp_range
        )

        if analysis_result["success"]:
            # Add analysis to session
            manager.add_analysis_call(
                session_id=session_id,
                prompt=prompt,
                analysis_response=analysis_result["analysis_response"],
                video_metadata=session.youtube_metadata or {},
                analysis_params={
                    "timestamp_range": timestamp_range,
                    "model": session.model,
                },
            )

            return {
                "success": True,
                "analysis": analysis_result["analysis_response"],
                "session_context": f"Session {session_id} conversation",
                "conversation_length": analysis_result.get("conversation_length", 0),
                "method": analysis_result.get("method", "unknown"),
            }

        return analysis_result

    except Exception as e:
        logger.error(f"Failed to analyze video in session: {e}")
        return {"success": False, "error": str(e), "error_type": "video_analysis_error"}


@mcp.tool()
def analyze_youtube_video(
    youtube_url: str,
    prompt: str,
    model: str = "gemini-2.5-pro-preview-05-06",
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Single-shot or session-integrated YouTube video analysis using direct URL method.

    Args:
        youtube_url: YouTube video URL or ID
        prompt: Analysis instruction
        model: Gemini model to use
        session_id: Optional session for context
    """
    try:
        # Validate YouTube URL
        validator = get_youtube_validator()
        validation = validator.validate_and_normalize_url(youtube_url)
        if not validation["valid"]:
            return {
                "success": False,
                "error": f"Invalid YouTube URL: {validation['error']}",
                "error_type": "invalid_youtube_url",
            }

        normalized_url = validation["normalized_url"]

        # Analyze video directly
        client = get_gemini_client()
        result = client.analyze_youtube_video_direct(
            youtube_url=normalized_url, user_prompt=prompt
        )

        if result["success"] and session_id:
            # Add to session if provided
            manager = get_session_manager()
            manager.add_analysis_call(
                session_id=session_id,
                prompt=prompt,
                analysis_response=result["analysis_response"],
                video_metadata={"youtube_url": normalized_url},
                analysis_params={"model": model},
            )

        return result

    except Exception as e:
        logger.error(f"Failed to analyze YouTube video: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "youtube_analysis_error",
        }


@mcp.tool()
def analyze_local_video(
    video_path: str,
    prompt: str,
    model: str = "gemini-2.5-pro-preview-05-06",
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Single-shot or session-integrated local video analysis using Files API.

    Args:
        video_path: Local video file path
        prompt: Analysis instruction
        model: Gemini model to use
        session_id: Optional session for context
    """
    try:
        # Upload video to Files API
        uploader = get_files_uploader()
        upload_result = uploader.upload_video_file(video_path)

        if not upload_result["success"]:
            return upload_result

        file_id = upload_result["file_id"]

        # Analyze uploaded video
        client = get_gemini_client()
        result = client.analyze_uploaded_video(file_id=file_id, user_prompt=prompt)

        if result["success"] and session_id:
            # Add to session if provided
            manager = get_session_manager()
            session = manager.get_session(session_id)
            if session:
                # Update session with file info
                manager.update_session(session_id, {"google_file_id": file_id})

                manager.add_analysis_call(
                    session_id=session_id,
                    prompt=prompt,
                    analysis_response=result["analysis_response"],
                    video_metadata={"file_id": file_id, "video_path": video_path},
                    analysis_params={"model": model},
                )

        # Include upload info in result
        result["upload_info"] = upload_result

        return result

    except Exception as e:
        logger.error(f"Failed to analyze local video: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "local_video_analysis_error",
        }


@mcp.tool()
def get_session_status(session_id: str) -> Dict[str, Any]:
    """Get current session status and history."""
    try:
        manager = get_session_manager()
        session = manager.get_session(session_id)

        if not session:
            return {
                "success": False,
                "error": f"Session {session_id} not found",
                "error_type": "session_not_found",
            }

        return {
            "success": True,
            "session_info": {
                "session_id": session.session_id,
                "session_name": session.session_name,
                "description": session.description,
                "model": session.model,
                "created_at": session.created_at.isoformat(),
                "last_activity": session.last_activity.isoformat(),
                "active": session.active,
                "video_source": session.youtube_url or session.video_file_path,
                "source_type": "youtube_url" if session.youtube_url else "local_file",
                "conversation_length": len(session.conversation_history),
                "analysis_calls": len(session.analysis_calls),
            },
            "video_metadata": session.youtube_metadata,
            "recent_history": (
                session.conversation_history[-3:]
                if session.conversation_history
                else []
            ),
        }

    except Exception as e:
        logger.error(f"Failed to get session status: {e}")
        return {"success": False, "error": str(e), "error_type": "session_status_error"}


@mcp.tool()
def list_active_sessions() -> Dict[str, Any]:
    """List all active video analysis sessions."""
    try:
        manager = get_session_manager()
        return manager.list_active_sessions()

    except Exception as e:
        logger.error(f"Failed to list active sessions: {e}")
        return {"success": False, "error": str(e), "error_type": "session_list_error"}


@mcp.tool()
def close_session(session_id: str) -> Dict[str, Any]:
    """Close session and cleanup resources."""
    try:
        manager = get_session_manager()
        return manager.close_session(session_id)

    except Exception as e:
        logger.error(f"Failed to close session: {e}")
        return {"success": False, "error": str(e), "error_type": "session_close_error"}


@mcp.tool()
def validate_youtube_url(url: str) -> Dict[str, Any]:
    """Validate and normalize YouTube URLs/IDs."""
    try:
        validator = get_youtube_validator()
        validation = validator.validate_and_normalize_url(url)

        if validation["valid"]:
            # Also check Gemini compatibility
            compatibility = validator.check_gemini_compatibility(
                validation["normalized_url"]
            )
            validation.update(compatibility)

        return validation

    except Exception as e:
        logger.error(f"Failed to validate YouTube URL: {e}")
        return {"success": False, "error": str(e), "error_type": "url_validation_error"}


@mcp.tool()
def get_usage_guide() -> Dict[str, Any]:
    """Comprehensive tool documentation and examples."""
    try:
        guide = {
            "success": True,
            "server_info": {
                "name": "YouTube Gemini MCP Server",
                "version": "0.1.0",
                "description": "Session-based conversational YouTube video analysis using Gemini 2.5 Pro",
            },
            "key_features": [
                "Direct YouTube URL processing (no download required)",
                "Local video file upload via Google Files API",
                "Session-based conversational analysis",
                "Thread-safe session management",
                "Comprehensive error handling",
            ],
            "workflow_examples": {
                "youtube_session": {
                    "step1": "create_video_session(description='Analyze lecture', video_source='https://youtube.com/watch?v=abc', source_type='youtube_url')",
                    "step2": "analyze_video_in_session(session_id='uuid', prompt='What are the key concepts?')",
                    "step3": "analyze_video_in_session(session_id='uuid', prompt='Explain the part about neural networks')",
                },
                "local_video": {
                    "step1": "analyze_local_video(video_path='/path/to/video.mp4', prompt='Summarize this video')",
                    "note": "Files auto-delete after 48 hours",
                },
            },
            "important_notes": [
                "YouTube videos: Unlimited session duration",
                "Local videos: 48-hour session limit due to Files API",
                "Maximum video length: 2 hours",
                "Maximum file size: 2GB",
            ],
        }

        return guide

    except Exception as e:
        logger.error(f"Failed to get usage guide: {e}")
        return {"success": False, "error": str(e), "error_type": "usage_guide_error"}


@mcp.tool()
def get_server_stats() -> Dict[str, Any]:
    """Server statistics and health monitoring."""
    try:
        manager = get_session_manager()
        sessions_result = manager.list_active_sessions()

        return {
            "success": True,
            "server_status": "healthy",
            "active_sessions": sessions_result.get("total_sessions", 0),
            "max_sessions": sessions_result.get("max_sessions", 50),
            "components": {
                "session_manager": (
                    "initialized" if session_manager else "not_initialized"
                ),
                "gemini_client": "initialized" if gemini_client else "not_initialized",
                "youtube_validator": (
                    "initialized" if youtube_validator else "not_initialized"
                ),
                "files_uploader": (
                    "initialized" if files_uploader else "not_initialized"
                ),
            },
            "environment": {
                "google_api_key": (
                    "configured" if os.getenv("GOOGLE_API_KEY") else "missing"
                ),
                "max_sessions": os.getenv("MCP_MAX_SESSIONS", "50"),
                "session_timeout": os.getenv("MCP_SESSION_TIMEOUT", "7200"),
            },
        }

    except Exception as e:
        logger.error(f"Failed to get server stats: {e}")
        return {"success": False, "error": str(e), "error_type": "server_stats_error"}


def main() -> None:
    """Main entry point for the MCP server."""
    try:
        # Validate environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error(
                "CRITICAL_MAIN: GOOGLE_API_KEY environment variable is required. Server cannot start."
            )
            return

        logger.info("Starting YouTube Gemini MCP Server")

        # Initialize global instances
        get_session_manager()
        get_gemini_client()
        get_youtube_validator()
        get_files_uploader()

        logger.info("All components initialized successfully")

        # Run the MCP server
        mcp.run()

    except Exception as e:
        logger.error(f"CRITICAL_MAIN: Server startup failed: {e}")


if __name__ == "__main__":
    main()
