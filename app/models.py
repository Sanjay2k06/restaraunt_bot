"""
Data models for Server Sundharam Restaurant Bot.
Comprehensive models for NLP, booking, sessions, and slot locking.

Author: Server Sundharam Dev Team
Version: 2.0 - Complete Rewrite
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any, Set
from datetime import datetime, date, time
from enum import Enum
import re


# ===========================================
# ENUMS - State Management
# ===========================================

class ConversationStep(Enum):
    """
    Conversation flow steps.
    The bot guides users through these steps naturally.
    """
    INIT = "init"                     # Fresh start
    GREETING = "greeting"             # After greeting
    AWAITING_NAME = "awaiting_name"   # Waiting for customer name
    AWAITING_PEOPLE = "awaiting_people"
    AWAITING_DATE = "awaiting_date"
    AWAITING_TIME = "awaiting_time"
    AWAITING_EVENT = "awaiting_event"
    AWAITING_MENU = "awaiting_menu"
    AWAITING_ADDONS = "awaiting_addons"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    SLOT_LOCKED = "slot_locked"       # Slot temporarily locked
    COMPLETED = "completed"           # Booking confirmed
    CANCELLED = "cancelled"


class Language(Enum):
    """Supported languages with codes."""
    ENGLISH = "en"
    TAMIL = "ta"


class Intent(Enum):
    """
    User intent classifications.
    NLP engine detects these from user messages.
    """
    GREETING = "greeting"
    BOOKING = "booking"
    MENU_QUERY = "menu_query"
    OFFERS_QUERY = "offers_query"
    LOCATION_QUERY = "location_query"
    TIMING_QUERY = "timing_query"
    PARKING_QUERY = "parking_query"
    FACILITIES_QUERY = "facilities_query"
    FOOD_QUERY = "food_query"
    HELP = "help"
    CANCEL = "cancel"
    RESTART = "restart"
    CONFIRM = "confirm"
    DENY = "deny"
    LANGUAGE_SWITCH = "language_switch"
    CROSS_QUESTION = "cross_question"
    UNKNOWN = "unknown"
    BOOKING_INFO = "booking_info"     # Natural language with booking data


class SeatingType(Enum):
    """Seating arrangement types."""
    TABLE = "table"
    MINI_HALL = "mini_hall"
    BANQUET_HALL = "banquet_hall"
    OUTDOOR = "outdoor"


# ===========================================
# EXTRACTED ENTITIES FROM NLP
# ===========================================

class ExtractedEntities(BaseModel):
    """
    Entities extracted from natural language input.
    Example: "Table for 5 tomorrow evening" extracts:
    - people: 5
    - date: tomorrow
    - time: evening
    """
    people: Optional[int] = None
    date_text: Optional[str] = None      # Raw date text (e.g., "tomorrow", "next sunday")
    parsed_date: Optional[str] = None    # Parsed date (DD-MM-YYYY)
    time_text: Optional[str] = None      # Raw time text (e.g., "evening", "7pm")
    parsed_time: Optional[str] = None    # Parsed time (HH:MM AM/PM)
    event_type: Optional[str] = None
    menu_preference: Optional[str] = None
    addons: List[str] = Field(default_factory=list)
    name: Optional[str] = None
    special_request: Optional[str] = None
    confidence: float = 0.0


# ===========================================
# SESSION & MEMORY
# ===========================================

class UserMemory(BaseModel):
    """
    Persistent memory for returning users.
    Enables personalized greetings and suggestions.
    """
    user_id: str
    name: Optional[str] = None
    last_booking_date: Optional[str] = None
    last_guests: Optional[int] = None
    last_menu_pack: Optional[str] = None
    favorite_items: List[str] = Field(default_factory=list)
    total_bookings: int = 0
    first_visit: datetime = Field(default_factory=datetime.now)
    last_visit: datetime = Field(default_factory=datetime.now)


class UserSession(BaseModel):
    """
    Active user session data.
    Tracks current conversation state and collected booking info.
    """
    user_id: str
    step: ConversationStep = ConversationStep.INIT
    language: Language = Language.ENGLISH
    
    # Booking Data
    name: Optional[str] = None
    people: Optional[int] = None
    date: Optional[str] = None
    time: Optional[str] = None
    event: Optional[str] = None
    menu_pack: Optional[str] = None
    addons: List[str] = Field(default_factory=list)
    special_requests: Optional[str] = None
    
    # Session Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    message_count: int = 0
    
    # Cross-question tracking
    pending_question: Optional[str] = None
    return_to_step: Optional[ConversationStep] = None
    
    # Slot lock reference
    slot_lock_key: Optional[str] = None
    
    # Memory reference
    is_returning_user: bool = False
    user_memory: Optional[UserMemory] = None
    
    class Config:
        use_enum_values = True


# ===========================================
# SLOT LOCKING (BookMyShow Style)
# ===========================================

class SlotLock(BaseModel):
    """
    Temporary slot lock for booking.
    Prevents double-booking during user confirmation.
    """
    lock_key: str           # Format: "DD-MM-YYYY_HH:MM"
    user_id: str
    date: str
    time: str
    people: int
    locked_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime    # Auto-release after 3 minutes
    is_confirmed: bool = False


# ===========================================
# MENU & ADDONS
# ===========================================

class MenuPack(BaseModel):
    """Menu pack configuration with bilingual support."""
    key: str
    name_en: str
    name_ta: str
    price_per_person: int
    description_en: str
    description_ta: str
    items_en: List[str]
    items_ta: List[str]
    recommended_for: List[str] = Field(default_factory=list)
    min_people: int = 1
    is_available: bool = True


class Addon(BaseModel):
    """Addon configuration with bilingual support."""
    key: str
    name_en: str
    name_ta: str
    price: int
    description_en: str
    description_ta: str
    recommended_for: List[str] = Field(default_factory=list)
    is_available: bool = True


# ===========================================
# SEATING & HALL
# ===========================================

class SeatingRecommendation(BaseModel):
    """
    Seating recommendation based on guest count.
    Server Sundharam suggests like a real waiter.
    """
    seating_type: SeatingType
    tables_needed: int
    hall_name: Optional[str] = None
    capacity: int
    message_en: str
    message_ta: str
    layout_visual: str


# ===========================================
# RESERVATION
# ===========================================

class Reservation(BaseModel):
    """Complete confirmed reservation record."""
    reservation_id: str
    user_id: str
    name: str
    people: int
    date: str
    time: str
    event: str
    menu_pack: str
    menu_pack_details: Dict[str, Any]
    addons: List[str]
    addon_details: List[Dict[str, Any]] = Field(default_factory=list)
    seating: SeatingRecommendation
    base_cost: int
    addon_cost: int
    total_cost: int
    status: str = "confirmed"
    created_at: datetime = Field(default_factory=datetime.now)
    special_requests: Optional[str] = None
    confirmation_message_en: str = ""
    confirmation_message_ta: str = ""


# ===========================================
# TWILIO WHATSAPP
# ===========================================

class WhatsAppMessage(BaseModel):
    """Incoming WhatsApp message from Twilio webhook."""
    From: str = Field(..., alias="From")
    Body: str
    MessageSid: Optional[str] = None
    AccountSid: Optional[str] = None
    NumMedia: Optional[int] = 0
    ProfileName: Optional[str] = None
    WaId: Optional[str] = None
    
    class Config:
        populate_by_name = True


class BotResponse(BaseModel):
    """Bot response structure - plain text only, no XML."""
    message: str
    language: str = "en"
    session_updated: bool = True


# ===========================================
# ADMIN & ANALYTICS
# ===========================================

class BookingSearchQuery(BaseModel):
    """Admin search query for bookings."""
    name: Optional[str] = None
    date: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    status: Optional[str] = None
    min_guests: Optional[int] = None
    max_guests: Optional[int] = None


class DashboardStats(BaseModel):
    """Dashboard statistics for admin."""
    total_bookings: int = 0
    today_bookings: int = 0
    pending_confirmations: int = 0
    active_sessions: int = 0
    locked_slots: int = 0
    total_revenue: int = 0
    popular_menu: str = ""
    popular_event: str = ""
    bookings_by_date: Dict[str, int] = Field(default_factory=dict)


# ===========================================
# INTENT DETECTION RESULT
# ===========================================

class IntentResult(BaseModel):
    """Result of NLP intent detection."""
    primary_intent: Intent
    confidence: float
    entities: ExtractedEntities
    secondary_intents: List[Intent] = Field(default_factory=list)
    raw_text: str
    language_detected: Language = Language.ENGLISH
    session_updated: bool = True
    conversation_ended: bool = False
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
