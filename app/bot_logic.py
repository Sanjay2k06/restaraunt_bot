"""
Bot logic handler for the Restaurant WhatsApp Bot.
Provides the main interface between incoming messages and the conversation engine.
"""

import logging
from typing import Dict, Any, Optional
from .conversation_engine import ConversationEngine, process_message
from .session_manager import session_manager
from .language import LanguageManager
from .utils import sanitize_phone_number, mask_phone_number
from .config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG_MODE else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BotEngine:
    """
    Main bot engine that handles incoming messages.
    Acts as the primary controller for all bot interactions.
    """
    
    @staticmethod
    def process(user_id: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Process incoming message and return response.
        
        Args:
            user_id: WhatsApp user ID (e.g., 'whatsapp:+919876543210')
            message: User's message text
            metadata: Optional metadata (profile name, message sid, etc.)
            
        Returns:
            Bot response string
        """
        try:
            # Sanitize user ID
            clean_user_id = sanitize_phone_number(user_id)
            
            # Log incoming message (mask phone for privacy)
            masked_phone = mask_phone_number(user_id)
            logger.info(f"Incoming from {masked_phone}: {message[:50]}...")
            
            # Process empty messages
            if not message or not message.strip():
                lang = session_manager.get_language(clean_user_id)
                return LanguageManager.get("invalid_input", lang, hint="Please send a message")
            
            # Process message through conversation engine
            response = ConversationEngine.process_message(clean_user_id, message)
            
            # Log response (truncated)
            logger.info(f"Response to {masked_phone}: {response[:50]}...")
            
            return response
            
        except Exception as e:
            logger.error(f"Error in BotEngine.process: {str(e)}", exc_info=True)
            return LanguageManager.get("error", "en")
    
    @staticmethod
    def get_session_info(user_id: str) -> Dict[str, Any]:
        """
        Get current session information for a user.
        
        Args:
            user_id: WhatsApp user ID
            
        Returns:
            Session information dictionary
        """
        clean_user_id = sanitize_phone_number(user_id)
        session = session_manager.get_session(clean_user_id)
        return session.to_dict()
    
    @staticmethod
    def reset_user_session(user_id: str) -> bool:
        """
        Reset a user's session.
        
        Args:
            user_id: WhatsApp user ID
            
        Returns:
            True if session was reset
        """
        clean_user_id = sanitize_phone_number(user_id)
        session_manager.reset_session(clean_user_id)
        logger.info(f"Session reset for {mask_phone_number(user_id)}")
        return True
    
    @staticmethod
    def get_system_stats() -> Dict[str, Any]:
        """
        Get system statistics.
        
        Returns:
            System stats dictionary
        """
        return {
            "session_stats": session_manager.get_session_stats(),
            "config": {
                "restaurant_name": settings.RESTAURANT_NAME,
                "session_timeout_minutes": settings.SESSION_TIMEOUT_MINUTES,
                "business_hours": f"{settings.OPENING_HOUR}:00 - {settings.CLOSING_HOUR}:00",
                "debug_mode": settings.DEBUG_MODE
            }
        }


# Create global bot engine instance
bot_engine_instance = BotEngine()


def bot_engine(user: str, message: str) -> str:
    """
    Main entry point for processing messages (backward compatible).
    
    Args:
        user: User identifier
        message: Message text
        
    Returns:
        Bot response
    """
    return bot_engine_instance.process(user, message)
