"""
Session Manager for Server Sundharam Bot.
Handles user sessions with memory, timeout, and cross-question support.

Features:
- User memory for returning users
- Cross-question state preservation
- Session timeout and cleanup
- Thread-safe operations

Author: Server Sundharam Dev Team
Version: 2.0
"""

import time
import threading
import logging
import json
from pathlib import Path
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta
from .config import settings
from .models import ConversationStep, UserMemory

# Configure logging
logger = logging.getLogger(__name__)


class SessionData:
    """
    Represents a user session with all booking-related data.
    Enhanced with cross-question support and memory.
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.step: str = ConversationStep.INIT.value
        self.language: str = settings.DEFAULT_LANGUAGE
        
        # Booking Data
        self.name: Optional[str] = None
        self.people: Optional[int] = None
        self.date: Optional[str] = None
        self.time: Optional[str] = None
        self.event: Optional[str] = None
        self.menu_pack: Optional[str] = None
        self.addons: List[str] = []
        self.special_requests: Optional[str] = None
        
        # Session Metadata
        self.created_at: float = time.time()
        self.last_update: float = time.time()
        self.message_count: int = 0
        self.last_message: Optional[str] = None
        self.error_count: int = 0
        
        # Cross-question Support
        self.pending_question: Optional[str] = None
        self.return_to_step: Optional[str] = None
        self.cross_question_count: int = 0
        
        # Slot Lock Reference
        self.slot_lock_key: Optional[str] = None
        
        # User Memory Reference
        self.is_returning_user: bool = False
        self.user_memory: Optional[Dict] = None
        
        # Additional metadata
        self.metadata: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary."""
        return {
            "user_id": self.user_id,
            "step": self.step,
            "language": self.language,
            "name": self.name,
            "people": self.people,
            "date": self.date,
            "time": self.time,
            "event": self.event,
            "menu_pack": self.menu_pack,
            "addons": self.addons,
            "special_requests": self.special_requests,
            "created_at": self.created_at,
            "last_update": self.last_update,
            "message_count": self.message_count,
            "is_returning_user": self.is_returning_user,
            "cross_question_count": self.cross_question_count
        }
    
    def update(self, **kwargs) -> None:
        """Update session fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.last_update = time.time()
        self.message_count += 1
    
    def is_expired(self, timeout_seconds: int) -> bool:
        """Check if session has expired."""
        return (time.time() - self.last_update) > timeout_seconds
    
    def get_duration_minutes(self) -> float:
        """Get session duration in minutes."""
        return (time.time() - self.created_at) / 60
    
    def reset(self) -> None:
        """Reset to initial step while preserving language and memory."""
        lang = self.language
        memory = self.user_memory
        is_returning = self.is_returning_user
        user_id = self.user_id
        
        self.__init__(user_id)
        self.language = lang
        self.user_memory = memory
        self.is_returning_user = is_returning
    
    def save_cross_question_state(self) -> None:
        """Save current state before handling cross-question."""
        self.return_to_step = self.step
        self.cross_question_count += 1
    
    def restore_cross_question_state(self) -> None:
        """Restore state after answering cross-question."""
        if self.return_to_step:
            self.step = self.return_to_step
            self.return_to_step = None


class UserMemoryStore:
    """
    Persistent storage for user memory.
    Remembers returning users and their preferences.
    """
    
    def __init__(self, storage_path: str = None):
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            self.storage_path = Path(__file__).parent.parent / "data" / "user_memory.json"
        
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._memory: Dict[str, Dict] = {}
        self._load()
    
    def _load(self):
        """Load user memory from file."""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r') as f:
                    self._memory = json.load(f)
        except Exception as e:
            logger.error(f"Error loading user memory: {e}")
            self._memory = {}
    
    def _save(self):
        """Save user memory to file."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self._memory, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving user memory: {e}")
    
    def get(self, user_id: str) -> Optional[Dict]:
        """Get memory for a user."""
        return self._memory.get(user_id)
    
    def save_memory(self, user_id: str, name: str, guests: int = None, 
                    menu_pack: str = None) -> None:
        """Save or update user memory."""
        if user_id not in self._memory:
            self._memory[user_id] = {
                "first_visit": datetime.now().isoformat(),
                "total_bookings": 0
            }
        
        memory = self._memory[user_id]
        memory["name"] = name
        memory["last_visit"] = datetime.now().isoformat()
        memory["total_bookings"] = memory.get("total_bookings", 0) + 1
        
        if guests:
            memory["last_guests"] = guests
        if menu_pack:
            memory["last_menu_pack"] = menu_pack
        
        self._save()
    
    def is_returning(self, user_id: str) -> bool:
        """Check if user has visited before."""
        return user_id in self._memory


class SessionManager:
    """
    Manages all user sessions with automatic cleanup and timeout handling.
    Thread-safe implementation for concurrent access.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._sessions: Dict[str, SessionData] = {}
        self._session_lock = threading.Lock()
        self._timeout_seconds = settings.SESSION_TIMEOUT_MINUTES * 60
        self._cleanup_interval = 300  # 5 minutes
        self._last_cleanup = time.time()
        self._initialized = True
        
        # User memory store
        self._memory_store = UserMemoryStore()
        
        # Start background cleanup thread
        self._start_cleanup_thread()
        
        logger.info(f"SessionManager initialized with {self._timeout_seconds}s timeout")
    
    def _start_cleanup_thread(self) -> None:
        """Start background thread for session cleanup."""
        def cleanup_worker():
            while True:
                time.sleep(self._cleanup_interval)
                self._cleanup_expired_sessions()
        
        thread = threading.Thread(target=cleanup_worker, daemon=True)
        thread.start()
        logger.info("Session cleanup thread started")
    
    def _cleanup_expired_sessions(self) -> None:
        """Remove expired sessions."""
        # Import here to avoid circular import
        from .slot_locker import slot_locker
        
        with self._session_lock:
            current_time = time.time()
            expired_users = [
                user_id for user_id, session in self._sessions.items()
                if session.is_expired(self._timeout_seconds)
            ]
            
            for user_id in expired_users:
                # Release any slot locks for expired sessions
                slot_locker.release_lock(user_id)
                del self._sessions[user_id]
                logger.info(f"Cleaned up expired session for {user_id}")
            
            self._last_cleanup = current_time
    
    def get_session(self, user_id: str) -> SessionData:
        """Get or create session for user."""
        with self._session_lock:
            if user_id in self._sessions:
                session = self._sessions[user_id]
                
                # Check if expired
                if session.is_expired(self._timeout_seconds):
                    logger.info(f"Session expired for {user_id}, creating new session")
                    old_lang = session.language
                    session = SessionData(user_id)
                    session.language = old_lang
                    session.metadata["previous_session_expired"] = True
                    
                    # Check for returning user
                    memory = self._memory_store.get(user_id)
                    if memory:
                        session.is_returning_user = True
                        session.user_memory = memory
                    
                    self._sessions[user_id] = session
                    return session
                
                session.last_update = time.time()
                return session
            
            # Create new session
            session = SessionData(user_id)
            
            # Check for returning user
            memory = self._memory_store.get(user_id)
            if memory:
                session.is_returning_user = True
                session.user_memory = memory
            
            self._sessions[user_id] = session
            logger.info(f"Created new session for {user_id}")
            return session
    
    def save_user_memory(self, user_id: str, name: str, guests: int = None,
                         menu_pack: str = None) -> None:
        """Save user memory for future visits."""
        self._memory_store.save_memory(user_id, name, guests, menu_pack)
    
    def update_session(self, user_id: str, **kwargs) -> SessionData:
        """Update session with new data."""
        session = self.get_session(user_id)
        session.update(**kwargs)
        return session
    
    def clear_session(self, user_id: str) -> bool:
        """Clear/delete a user's session."""
        # Import here to avoid circular import
        from .slot_locker import slot_locker
        
        with self._session_lock:
            if user_id in self._sessions:
                # Release any slot locks
                slot_locker.release_lock(user_id)
                del self._sessions[user_id]
                logger.info(f"Cleared session for {user_id}")
                return True
            return False
    
    def reset_session(self, user_id: str) -> SessionData:
        """Reset session to initial state, preserving language and memory."""
        with self._session_lock:
            if user_id in self._sessions:
                self._sessions[user_id].reset()
                return self._sessions[user_id]
            return self.get_session(user_id)
    
    def set_language(self, user_id: str, language: str) -> None:
        """Set language preference for user."""
        session = self.get_session(user_id)
        session.language = language
    
    def get_language(self, user_id: str) -> str:
        """Get language preference for user."""
        session = self.get_session(user_id)
        return session.language
    
    def set_step(self, user_id: str, step: ConversationStep) -> None:
        """Set conversation step for user."""
        session = self.get_session(user_id)
        session.step = step.value if isinstance(step, ConversationStep) else step
    
    def get_step(self, user_id: str) -> str:
        """Get current conversation step for user."""
        session = self.get_session(user_id)
        return session.step
    
    def save_cross_question_state(self, user_id: str) -> None:
        """Save state before handling cross-question."""
        session = self.get_session(user_id)
        session.save_cross_question_state()
    
    def restore_cross_question_state(self, user_id: str) -> None:
        """Restore state after answering cross-question."""
        session = self.get_session(user_id)
        session.restore_cross_question_state()
    
    def get_active_session_count(self) -> int:
        """Get count of active (non-expired) sessions."""
        with self._session_lock:
            return sum(
                1 for session in self._sessions.values()
                if not session.is_expired(self._timeout_seconds)
            )
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Get all active sessions as dictionaries."""
        with self._session_lock:
            return [
                session.to_dict() for session in self._sessions.values()
                if not session.is_expired(self._timeout_seconds)
            ]
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics."""
        with self._session_lock:
            total = len(self._sessions)
            active = sum(
                1 for s in self._sessions.values()
                if not s.is_expired(self._timeout_seconds)
            )
            
            return {
                "total_sessions": total,
                "active_sessions": active,
                "expired_sessions": total - active,
                "timeout_minutes": settings.SESSION_TIMEOUT_MINUTES,
                "last_cleanup": datetime.fromtimestamp(self._last_cleanup).isoformat()
            }


# Global session manager instance
session_manager = SessionManager()


# Convenience functions
def get_session(user: str) -> Dict[str, Any]:
    """Get session as dictionary."""
    session = session_manager.get_session(user)
    return session.to_dict()


def clear_session(user: str) -> bool:
    """Clear user session."""
    return session_manager.clear_session(user)


def get_session_object(user: str) -> SessionData:
    """Get session object directly."""
    return session_manager.get_session(user)
