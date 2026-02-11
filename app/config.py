"""
Configuration settings for Server Sundharam Restaurant Bot.
Loads environment variables and provides centralized configuration.

Author: Server Sundharam Dev Team
Version: 2.0 - Complete Rewrite with Human-like Personality
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """
    Application settings loaded from environment variables.
    Provides default values for development and production configs.
    """
    
    # ===========================================
    # TWILIO CONFIGURATION
    # ===========================================
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_NUMBER: str = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
    
    # ===========================================
    # RESTAURANT DETAILS
    # ===========================================
    RESTAURANT_NAME: str = os.getenv("RESTAURANT_NAME", "Royal Chef's Restaurant")
    RESTAURANT_LOCATION: str = os.getenv("RESTAURANT_LOCATION", "123 Food Street, T Nagar, Chennai - 600017")
    RESTAURANT_PHONE: str = os.getenv("RESTAURANT_PHONE", "+91-9876543210")
    RESTAURANT_EMAIL: str = os.getenv("RESTAURANT_EMAIL", "reservations@royalchefs.com")
    RESTAURANT_TIMINGS: str = os.getenv("RESTAURANT_TIMINGS", "11 AM - 11 PM (All days)")
    PARKING_INFO: str = os.getenv("PARKING_INFO", "Free valet parking available, sir! 50+ car capacity.")
    
    # ===========================================
    # BOT IDENTITY - SERVER SUNDHARAM
    # ===========================================
    BOT_NAME: str = "Server Sundharam"
    BOT_ROLE: str = "Online Waiter"
    BOT_EMOJI: str = "😊"
    
    # ===========================================
    # SESSION & SLOT LOCKING
    # ===========================================
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "15"))
    SLOT_LOCK_DURATION_MINUTES: int = int(os.getenv("SLOT_LOCK_DURATION_MINUTES", "3"))
    
    # ===========================================
    # BUSINESS HOURS
    # ===========================================
    OPENING_HOUR: int = int(os.getenv("OPENING_HOUR", "11"))
    CLOSING_HOUR: int = int(os.getenv("CLOSING_HOUR", "23"))
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "en")
    
    # ===========================================
    # RESERVATION SETTINGS
    # ===========================================
    MIN_PARTY_SIZE: int = int(os.getenv("MIN_PARTY_SIZE", "1"))
    MAX_PARTY_SIZE: int = int(os.getenv("MAX_PARTY_SIZE", "200"))
    ADVANCE_BOOKING_DAYS: int = int(os.getenv("ADVANCE_BOOKING_DAYS", "60"))
    
    # ===========================================
    # DEBUG & DEVELOPMENT
    # ===========================================
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    # ===========================================
    # FACILITIES INFORMATION
    # ===========================================
    FACILITIES = {
        "parking": "Free valet parking available with 50+ car capacity",
        "ac": "Fully air-conditioned halls and dining area",
        "kids_area": "Yes! Kids play area with toys and games",
        "wifi": "Free high-speed WiFi available",
        "projector": "Projector available for corporate events (₹500 extra)",
        "music": "Live music available on weekends",
        "outdoor": "Beautiful outdoor garden seating available",
        "private_room": "Private dining rooms available for special occasions"
    }
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration."""
        required_fields = []
        
        if not cls.TWILIO_ACCOUNT_SID:
            required_fields.append("TWILIO_ACCOUNT_SID")
        if not cls.TWILIO_AUTH_TOKEN:
            required_fields.append("TWILIO_AUTH_TOKEN")
        
        if required_fields and not cls.DEBUG_MODE:
            print(f"Warning: Missing required configuration: {', '.join(required_fields)}")
            return False
        return True


# Global settings instance
settings = Settings()
