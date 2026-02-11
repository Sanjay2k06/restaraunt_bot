"""
Restaurant WhatsApp Bot Application Package.
A production-ready FastAPI backend for WhatsApp-based restaurant reservations.
"""

__version__ = "2.0.0"
__author__ = "Restaurant Bot Team"
__description__ = "AI-powered WhatsApp bot for restaurant table reservations"

# Module exports
from .config import settings
from .models import (
    ConversationStep,
    Language,
    UserSession,
    Reservation,
    BotResponse
)
from .bot_logic import bot_engine, BotEngine
from .conversation_engine import ConversationEngine, process_message
from .session_manager import session_manager, get_session, clear_session
from .reservation_service import ReservationService, create_reservation
from .language import LanguageManager, LANG
from .menu_data import MENU_PACKS, ADDONS, EVENT_RECOMMENDATIONS

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__description__",
    
    # Configuration
    "settings",
    
    # Models
    "ConversationStep",
    "Language",
    "UserSession",
    "Reservation",
    "BotResponse",
    
    # Core components
    "BotEngine",
    "bot_engine",
    "ConversationEngine",
    "process_message",
    
    # Session management
    "session_manager",
    "get_session",
    "clear_session",
    
    # Reservation
    "ReservationService",
    "create_reservation",
    
    # Language
    "LanguageManager",
    "LANG",
    
    # Data
    "MENU_PACKS",
    "ADDONS",
    "EVENT_RECOMMENDATIONS"
]
 
