"""Session management for conversational video analysis."""

import json
import logging
import os
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from threading import RLock
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class VideoAnalysisCall:
    """Represents a single video analysis within conversation."""

    id: str
    prompt: str
    analysis_response: str
    video_metadata: Dict[str, Any]
    analysis_params: Dict[str, Any]
    created_at: datetime
    referenced_timestamps: List[str] = field(default_factory=list)
    key_insights: List[str] = field(default_factory=list)


@dataclass
class VideoSession:
    """Complete session state for conversational video analysis."""

    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    model: str = "gemini-2.5-pro-preview-05-06"
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    session_name: Optional[str] = None
    description: str = ""
    youtube_url: str = ""
    youtube_metadata: Dict[str, Any] = field(default_factory=dict)
    google_file_id: Optional[str] = None
    video_file_path: Optional[str] = None
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    analysis_calls: List[VideoAnalysisCall] = field(default_factory=list)
    active: bool = True


class SessionManager:
    """Thread-safe manager for video analysis sessions."""

    def __init__(self, max_sessions: int = 50, session_timeout_hours: float = 2.0):
        """Initialize session manager with thread safety."""
        self.max_sessions = max_sessions
        self.session_timeout_hours = session_timeout_hours
        self.sessions: Dict[str, VideoSession] = {}
        self._lock = RLock()
        self.session_data_dir = Path("session_data/sessions")
        self.expired_sessions_dir = Path("session_data/expired_sessions")

        # Ensure directories exist
        self.session_data_dir.mkdir(parents=True, exist_ok=True)
        self.expired_sessions_dir.mkdir(parents=True, exist_ok=True)

        logger.info(
            f"SessionManager initialized with max_sessions={max_sessions}, timeout={session_timeout_hours}h"
        )

    def create_session(
        self,
        description: str,
        video_source: str,
        model: str = "gemini-2.5-pro-preview-05-06",
        session_name: Optional[str] = None,
        source_type: str = "youtube_url",
    ) -> Dict[str, Any]:
        """Create new video analysis session."""
        try:
            with self._lock:
                # Check session limits
                self._cleanup_expired_sessions()
                if len(self.sessions) >= self.max_sessions:
                    return {
                        "success": False,
                        "error": f"Maximum sessions ({self.max_sessions}) reached",
                        "error_type": "session_limit_exceeded",
                    }

                # Create new session
                session = VideoSession(
                    model=model, session_name=session_name, description=description
                )

                # Set video source based on type
                if source_type == "youtube_url":
                    session.youtube_url = video_source
                elif source_type == "local_file":
                    session.video_file_path = video_source
                else:
                    return {
                        "success": False,
                        "error": f"Invalid source_type: {source_type}",
                        "error_type": "invalid_source_type",
                    }

                # Store session
                self.sessions[session.session_id] = session

                # Save session metadata to disk
                self._save_session_metadata(session)

                logger.info(
                    f"Created session {session.session_id} for {source_type}: {video_source}"
                )

                return {
                    "success": True,
                    "session_id": session.session_id,
                    "model": session.model,
                    "source_type": source_type,
                    "video_source": video_source,
                    "created_at": session.created_at.isoformat(),
                    "status": "created",
                }

        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "session_creation_error",
            }

    def get_session(self, session_id: str) -> Optional[VideoSession]:
        """Get session by ID with thread safety."""
        with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.last_activity = datetime.now()
            return session

    def update_session(
        self, session_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update session with new data."""
        try:
            with self._lock:
                session = self.sessions.get(session_id)
                if not session:
                    return {
                        "success": False,
                        "error": f"Session {session_id} not found",
                        "error_type": "session_not_found",
                    }

                # Update session fields
                for key, value in updates.items():
                    if hasattr(session, key):
                        setattr(session, key, value)

                session.last_activity = datetime.now()

                # Save updated metadata
                self._save_session_metadata(session)

                logger.info(f"Updated session {session_id}")

                return {"success": True, "session_id": session_id, "status": "updated"}

        except Exception as e:
            logger.error(f"Failed to update session {session_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "session_update_error",
            }

    def add_analysis_call(
        self,
        session_id: str,
        prompt: str,
        analysis_response: str,
        video_metadata: Dict[str, Any],
        analysis_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Add analysis call to session conversation."""
        try:
            with self._lock:
                session = self.sessions.get(session_id)
                if not session:
                    return {
                        "success": False,
                        "error": f"Session {session_id} not found",
                        "error_type": "session_not_found",
                    }

                # Create analysis call
                call = VideoAnalysisCall(
                    id=str(uuid.uuid4()),
                    prompt=prompt,
                    analysis_response=analysis_response,
                    video_metadata=video_metadata,
                    analysis_params=analysis_params,
                    created_at=datetime.now(),
                )

                # Add to session
                session.analysis_calls.append(call)
                session.last_activity = datetime.now()

                # Update conversation history
                session.conversation_history.append(
                    {
                        "type": "analysis_call",
                        "call_id": call.id,
                        "prompt": prompt,
                        "response": analysis_response,
                        "timestamp": call.created_at.isoformat(),
                    }
                )

                # Save conversation log
                self._save_conversation_log(session)

                logger.info(f"Added analysis call to session {session_id}")

                return {
                    "success": True,
                    "call_id": call.id,
                    "session_id": session_id,
                    "conversation_length": len(session.conversation_history),
                }

        except Exception as e:
            logger.error(f"Failed to add analysis call to session {session_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "analysis_call_error",
            }

    def list_active_sessions(self) -> Dict[str, Any]:
        """List all active sessions."""
        try:
            with self._lock:
                self._cleanup_expired_sessions()

                sessions_list = []
                for session in self.sessions.values():
                    if session.active:
                        sessions_list.append(
                            {
                                "session_id": session.session_id,
                                "session_name": session.session_name,
                                "description": session.description,
                                "model": session.model,
                                "created_at": session.created_at.isoformat(),
                                "last_activity": session.last_activity.isoformat(),
                                "conversation_length": len(
                                    session.conversation_history
                                ),
                                "analysis_calls": len(session.analysis_calls),
                                "video_source": session.youtube_url
                                or session.video_file_path,
                                "source_type": (
                                    "youtube_url"
                                    if session.youtube_url
                                    else "local_file"
                                ),
                            }
                        )

                return {
                    "success": True,
                    "sessions": sessions_list,
                    "total_sessions": len(sessions_list),
                    "max_sessions": self.max_sessions,
                }

        except Exception as e:
            logger.error(f"Failed to list active sessions: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "session_list_error",
            }

    def close_session(self, session_id: str) -> Dict[str, Any]:
        """Close session and cleanup resources."""
        try:
            with self._lock:
                session = self.sessions.get(session_id)
                if not session:
                    return {
                        "success": False,
                        "error": f"Session {session_id} not found",
                        "error_type": "session_not_found",
                    }

                # Mark session as inactive
                session.active = False
                session.last_activity = datetime.now()

                # Save final session state
                self._save_session_metadata(session)
                self._save_conversation_log(session)

                # Archive session to expired directory
                self._archive_session(session)

                # Remove from active sessions
                del self.sessions[session_id]

                logger.info(f"Closed session {session_id}")

                return {
                    "success": True,
                    "session_id": session_id,
                    "status": "closed",
                    "conversation_length": len(session.conversation_history),
                    "analysis_calls": len(session.analysis_calls),
                }

        except Exception as e:
            logger.error(f"Failed to close session {session_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "session_close_error",
            }

    def _cleanup_expired_sessions(self) -> None:
        """Remove expired sessions based on timeout."""
        current_time = datetime.now()
        expired_session_ids = []

        for session_id, session in self.sessions.items():
            time_diff = current_time - session.last_activity
            if time_diff.total_seconds() > (self.session_timeout_hours * 3600):
                expired_session_ids.append(session_id)

        for session_id in expired_session_ids:
            logger.info(f"Cleaning up expired session: {session_id}")
            self.close_session(session_id)

    def _save_session_metadata(self, session: VideoSession) -> None:
        """Save session metadata to disk."""
        try:
            session_dir = self.session_data_dir / session.session_id
            session_dir.mkdir(exist_ok=True)

            metadata_file = session_dir / "session_metadata.json"

            # Convert session to dict, handling datetime serialization
            session_dict = asdict(session)
            session_dict["created_at"] = session.created_at.isoformat()
            session_dict["last_activity"] = session.last_activity.isoformat()

            # Handle analysis calls datetime serialization
            for call in session_dict["analysis_calls"]:
                call["created_at"] = (
                    call["created_at"].isoformat()
                    if isinstance(call["created_at"], datetime)
                    else call["created_at"]
                )

            with open(metadata_file, "w") as f:
                json.dump(session_dict, f, indent=2)

        except Exception as e:
            logger.error(
                f"Failed to save session metadata for {session.session_id}: {e}"
            )

    def _save_conversation_log(self, session: VideoSession) -> None:
        """Save conversation log to disk."""
        try:
            session_dir = self.session_data_dir / session.session_id
            session_dir.mkdir(exist_ok=True)

            log_file = session_dir / "conversation_log.json"

            with open(log_file, "w") as f:
                json.dump(session.conversation_history, f, indent=2)

        except Exception as e:
            logger.error(
                f"Failed to save conversation log for {session.session_id}: {e}"
            )

    def _archive_session(self, session: VideoSession) -> None:
        """Archive closed session to expired directory."""
        try:
            source_dir = self.session_data_dir / session.session_id
            target_dir = self.expired_sessions_dir / session.session_id

            if source_dir.exists():
                # Move session directory to expired
                source_dir.rename(target_dir)
                logger.info(
                    f"Archived session {session.session_id} to expired directory"
                )

        except Exception as e:
            logger.error(f"Failed to archive session {session.session_id}: {e}")
