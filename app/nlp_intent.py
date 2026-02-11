"""
NLP Intent Detection Engine for Server Sundharam Bot.
Extracts intents and entities from natural language input.

Features:
- Intent classification (greeting, booking, menu, etc.)
- Entity extraction (people, date, time, event)
- Synonym handling and spelling tolerance
- Multi-language support (English + Tamil)

Author: Server Sundharam Dev Team
Version: 2.0
"""

import re
from datetime import datetime, timedelta
from typing import Optional, List, Tuple, Dict
from .models import Intent, ExtractedEntities, IntentResult, Language


class NLPEngine:
    """
    Natural Language Processing engine for understanding user messages.
    Extracts intent and entities from free-form text.
    """
    
    # ===========================================
    # INTENT PATTERNS
    # ===========================================
    
    # Greeting patterns (English + Tamil + casual)
    GREETING_PATTERNS = [
        r'\b(hi|hello|hey|hii+|hai|helo|hola|yo)\b',
        r'\b(good\s*(morning|afternoon|evening|night))\b',
        r'\b(vanakkam|vannakam|வணக்கம்)\b',
        r'\b(bro|macha|machaa|dei|da|di|anna|bhai)\b',
        r'\b(namaste|namaskar)\b',
    ]
    
    # Booking intent patterns
    BOOKING_PATTERNS = [
        r'\b(book|booking|reserve|reservation|table)\b',
        r'\b(need|want|looking\s+for)\s+(a\s+)?(table|seat|place)\b',
        r'\b(arrange|plan|setup)\b.*\b(table|party|event)\b',
        r'\bbook\s*pann[ua]?\b',  # Tamil "book pannu"
        r'\b(table|seat)\s+(for|வேணும்|venum)\b',
    ]
    
    # Menu query patterns
    MENU_PATTERNS = [
        r'\b(menu|food|dish|item|eat|cuisine)\b',
        r'\b(what|show|see)\s+(do\s+you\s+)?(have|serve|offer)\b',
        r'\b(price|cost|rate|charge)\b',
        r'\b(veg|nonveg|non-veg|vegetarian)\b',
        r'\b(biryani|biriyani|chicken|mutton|fish|paneer)\b',
        r'\b(sapadu|சாப்பாடு|saapad|உணவு)\b',
    ]
    
    # Offers query patterns
    OFFER_PATTERNS = [
        r'\b(offer|discount|deal|promo|coupon)\b',
        r'\b(offer\s+iruk|discount\s+iruk)\b',
        r'\b(special|combo)\s+(offer|price)\b',
    ]
    
    # Location query patterns
    LOCATION_PATTERNS = [
        r'\b(where|location|address|place|area|direction)\b',
        r'\b(enga|எங்க|enge)\b',
        r'\b(how\s+to\s+(reach|come|get))\b',
    ]
    
    # Timing query patterns
    TIMING_PATTERNS = [
        r'\b(timing|time|hour|open|close|when)\b',
        r'\b(eppo|எப்போ|eppudi)\b',
        r'\b(working\s+hours?|business\s+hours?)\b',
    ]
    
    # Parking query patterns
    PARKING_PATTERNS = [
        r'\b(parking|park|car|vehicle|bike)\b',
        r'\b(free\s+parking|valet)\b',
    ]
    
    # Facilities query patterns (AC, WiFi, kids area, etc.)
    FACILITY_PATTERNS = [
        r'\b(ac|air\s*condition|cool)\b',
        r'\b(wifi|wi-fi|internet)\b',
        r'\b(kids?|child|children|play\s*area)\b',
        r'\b(outdoor|garden|terrace)\b',
        r'\b(projector|screen|presentation)\b',
        r'\b(private|separate)\s+(room|hall|area)\b',
    ]
    
    # Help patterns
    HELP_PATTERNS = [
        r'\b(help|assist|support|guide)\b',
        r'\b(what\s+can\s+you\s+do)\b',
        r'\b(options?|features?)\b',
    ]
    
    # Cancel patterns
    CANCEL_PATTERNS = [
        r'\b(cancel|stop|quit|exit|abort)\b',
        r'\b(don\'?t\s+want|no\s+need|forget\s+it)\b',
        r'\b(venda|வேண்டாம்)\b',
    ]
    
    # Restart patterns
    RESTART_PATTERNS = [
        r'\b(restart|reset|start\s*over|begin\s*again|fresh\s*start)\b',
        r'\b(from\s+beginning|pudhusu)\b',
    ]
    
    # Confirm patterns
    CONFIRM_PATTERNS = [
        r'\b(yes|yeah|yep|yup|sure|ok|okay|fine|correct|right)\b',
        r'\b(confirm|proceed|go\s*ahead|done)\b',
        r'\b(sari|சரி|ama|ஆமா|aama)\b',
    ]
    
    # Deny patterns
    DENY_PATTERNS = [
        r'\b(no|nope|nah|never|wrong|incorrect)\b',
        r'\b(illa|இல்ல|illai|வேண்டாம்)\b',
        r'\b(change|modify|edit|different)\b',
    ]
    
    # Language switch patterns
    LANGUAGE_SWITCH_PATTERNS = {
        "ta": [r'\b(tamil|தமிழ்|tamizh)\b'],
        "en": [r'\b(english|eng|inglish)\b'],
    }
    
    # ===========================================
    # ENTITY EXTRACTION PATTERNS
    # ===========================================
    
    # Number words to digits
    NUMBER_WORDS = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'fifteen': 15, 'twenty': 20,
        'twenty-five': 25, 'thirty': 30, 'forty': 40, 'fifty': 50,
        'hundred': 100
    }
    
    # Relative date words
    DATE_WORDS = {
        'today': 0, 'tomorrow': 1, 'day after tomorrow': 2,
        'day after': 2, 'naale': 1, 'naalai': 1, 'நாளை': 1,
        'indru': 0, 'inniku': 0, 'இன்று': 0
    }
    
    # Day names
    DAY_NAMES = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    # Time words
    TIME_WORDS = {
        'morning': '10:00 AM', 'noon': '12:00 PM', 'afternoon': '2:00 PM',
        'evening': '7:00 PM', 'night': '8:00 PM', 'dinner': '8:00 PM',
        'lunch': '1:00 PM', 'breakfast': '9:00 AM',
        'kaalai': '10:00 AM', 'மாலை': '7:00 PM', 'malai': '7:00 PM',
        'iravu': '8:00 PM', 'இரவு': '8:00 PM'
    }
    
    # Event types
    EVENT_KEYWORDS = {
        'birthday': ['birthday', 'bday', 'b\'day', 'pirandha', 'பிறந்தநாள்'],
        'anniversary': ['anniversary', 'anni', 'wedding anniversary'],
        'corporate': ['corporate', 'office', 'meeting', 'business', 'conference', 'team'],
        'wedding': ['wedding', 'marriage', 'reception', 'engagement', 'kalyanam', 'திருமணம்'],
        'party': ['party', 'celebration', 'get-together', 'get together', 'gathering'],
        'date': ['date', 'romantic', 'couple', 'candle light'],
        'casual': ['casual', 'family', 'friends', 'outing', 'dinner', 'lunch'],
        'farewell': ['farewell', 'send-off', 'goodbye'],
        'kitty': ['kitty', 'kitty party', 'ladies'],
    }
    
    # Menu preferences
    MENU_KEYWORDS = {
        'veg': ['veg', 'vegetarian', 'pure veg', 'saiva', 'சைவம்'],
        'nonveg': ['nonveg', 'non-veg', 'non veg', 'chicken', 'mutton', 'fish', 'asaiva'],
        'premium': ['premium', 'special', 'best', 'top'],
        'deluxe': ['deluxe', 'grand', 'full', 'complete', 'party pack'],
    }
    
    # Addon keywords
    ADDON_KEYWORDS = {
        'decoration': ['decoration', 'decor', 'decorate', 'decorations'],
        'cake': ['cake', 'birthday cake', 'pastry'],
        'photography': ['photography', 'photo', 'photographer', 'camera'],
        'music': ['music', 'dj', 'songs', 'music system'],
        'flowers': ['flowers', 'flower', 'bouquet', 'garland'],
        'balloons': ['balloons', 'balloon', 'balloon decoration'],
    }
    
    # ===========================================
    # MAIN DETECTION METHOD
    # ===========================================
    
    @classmethod
    def detect_intent(cls, text: str, current_lang: str = "en") -> IntentResult:
        """
        Detect user intent and extract entities from text.
        Returns IntentResult with primary intent, confidence, and extracted entities.
        """
        text_lower = text.lower().strip()
        
        # Initialize result
        entities = ExtractedEntities()
        primary_intent = Intent.UNKNOWN
        secondary_intents = []
        confidence = 0.0
        detected_lang = Language.ENGLISH
        
        # Check for language switch first
        lang_switch = cls._detect_language_switch(text_lower)
        if lang_switch:
            return IntentResult(
                primary_intent=Intent.LANGUAGE_SWITCH,
                confidence=1.0,
                entities=ExtractedEntities(),
                raw_text=text,
                language_detected=Language.TAMIL if lang_switch == "ta" else Language.ENGLISH
            )
        
        # Detect language of input
        detected_lang = cls._detect_language(text_lower)
        
        # Check intents in priority order
        intent_checks = [
            (Intent.CANCEL, cls.CANCEL_PATTERNS),
            (Intent.RESTART, cls.RESTART_PATTERNS),
            (Intent.CONFIRM, cls.CONFIRM_PATTERNS),
            (Intent.DENY, cls.DENY_PATTERNS),
            (Intent.GREETING, cls.GREETING_PATTERNS),
            (Intent.HELP, cls.HELP_PATTERNS),
            (Intent.MENU_QUERY, cls.MENU_PATTERNS),
            (Intent.OFFERS_QUERY, cls.OFFER_PATTERNS),
            (Intent.PARKING_QUERY, cls.PARKING_PATTERNS),
            (Intent.TIMING_QUERY, cls.TIMING_PATTERNS),
            (Intent.LOCATION_QUERY, cls.LOCATION_PATTERNS),
            (Intent.FACILITIES_QUERY, cls.FACILITY_PATTERNS),
            (Intent.BOOKING, cls.BOOKING_PATTERNS),
        ]
        
        for intent, patterns in intent_checks:
            if cls._matches_patterns(text_lower, patterns):
                if primary_intent == Intent.UNKNOWN:
                    primary_intent = intent
                    confidence = 0.8
                else:
                    secondary_intents.append(intent)
        
        # Extract entities regardless of intent
        entities = cls._extract_entities(text_lower, text)
        
        # If entities found but no clear intent, it might be booking info
        if primary_intent == Intent.UNKNOWN and entities.has_booking_data():
            primary_intent = Intent.BOOKING_INFO
            confidence = 0.7
        
        # Default to unknown with low confidence
        if primary_intent == Intent.UNKNOWN:
            confidence = 0.3
        
        return IntentResult(
            primary_intent=primary_intent,
            confidence=confidence,
            entities=entities,
            secondary_intents=secondary_intents,
            raw_text=text,
            language_detected=detected_lang
        )
    
    # ===========================================
    # ENTITY EXTRACTION
    # ===========================================
    
    @classmethod
    def _extract_entities(cls, text_lower: str, original_text: str) -> ExtractedEntities:
        """Extract all possible entities from text."""
        entities = ExtractedEntities()
        
        # Extract people count
        people = cls._extract_people(text_lower)
        if people:
            entities.people = people
        
        # Extract date
        date_text, parsed_date = cls._extract_date(text_lower)
        if date_text:
            entities.date_text = date_text
            entities.parsed_date = parsed_date
        
        # Extract time
        time_text, parsed_time = cls._extract_time(text_lower)
        if time_text:
            entities.time_text = time_text
            entities.parsed_time = parsed_time
        
        # Extract event type
        event = cls._extract_event(text_lower)
        if event:
            entities.event_type = event
        
        # Extract menu preference
        menu = cls._extract_menu(text_lower)
        if menu:
            entities.menu_preference = menu
        
        # Extract addons
        addons = cls._extract_addons(text_lower)
        if addons:
            entities.addons = addons
        
        # Calculate confidence based on entities found
        found_count = sum([
            entities.people is not None,
            entities.parsed_date is not None,
            entities.parsed_time is not None,
            entities.event_type is not None,
        ])
        entities.confidence = min(found_count * 0.25, 1.0)
        
        return entities
    
    @classmethod
    def _extract_people(cls, text: str) -> Optional[int]:
        """Extract number of people from text."""
        # Pattern: "for X people" or "X guests" or just number
        patterns = [
            r'(?:for|table\s+for)\s+(\d+)',
            r'(\d+)\s*(?:people|guests|persons|pax|பேர்|per)',
            r'(?:party\s+of|group\s+of)\s+(\d+)',
            r'(\d+)\s*(?:of\s+us|members)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                num = int(match.group(1))
                if 1 <= num <= 200:
                    return num
        
        # Check for number words
        for word, num in cls.NUMBER_WORDS.items():
            if re.search(rf'\b{word}\b', text):
                return num
        
        # Standalone number at beginning or end
        match = re.search(r'^(\d+)\b|\b(\d+)$', text)
        if match:
            num = int(match.group(1) or match.group(2))
            if 1 <= num <= 200:
                return num
        
        return None
    
    @classmethod
    def _extract_date(cls, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract date from text. Returns (raw_text, parsed_date)."""
        today = datetime.now()
        
        # Check for relative date words
        for word, days_offset in cls.DATE_WORDS.items():
            if word in text:
                target_date = today + timedelta(days=days_offset)
                return (word, target_date.strftime("%d-%m-%Y"))
        
        # Check for day names (this Sunday, next Monday, etc.)
        for i, day in enumerate(cls.DAY_NAMES):
            # "this Sunday" or "Sunday"
            if re.search(rf'\b(this\s+)?{day}\b', text):
                current_day = today.weekday()
                target_day = i
                days_ahead = target_day - current_day
                if days_ahead <= 0:
                    days_ahead += 7
                target_date = today + timedelta(days=days_ahead)
                return (day, target_date.strftime("%d-%m-%Y"))
            
            # "next Sunday"
            if re.search(rf'\bnext\s+{day}\b', text):
                current_day = today.weekday()
                target_day = i
                days_ahead = target_day - current_day + 7
                target_date = today + timedelta(days=days_ahead)
                return (f"next {day}", target_date.strftime("%d-%m-%Y"))
        
        # Check for explicit date formats
        date_patterns = [
            (r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', '%d-%m-%Y'),  # DD-MM-YYYY
            (r'(\d{1,2})[/-](\d{1,2})[/-](\d{2})', '%d-%m-%y'),  # DD-MM-YY
            (r'(\d{1,2})\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s*(\d{4})?', None),
        ]
        
        # DD-MM-YYYY or DD/MM/YYYY
        match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', text)
        if match:
            day, month, year = match.groups()
            if len(year) == 2:
                year = '20' + year
            try:
                date_obj = datetime(int(year), int(month), int(day))
                return (match.group(0), date_obj.strftime("%d-%m-%Y"))
            except ValueError:
                pass
        
        return (None, None)
    
    @classmethod
    def _extract_time(cls, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract time from text. Returns (raw_text, parsed_time).
        
        IMPORTANT: Check explicit time (like '5pm') FIRST, before time words (like 'evening').
        This ensures 'evening 5pm' returns 5pm, not 7pm.
        """
        # FIRST: Check for explicit time patterns (5pm, 7:30pm, etc.)
        # This ensures user's explicit time is preserved
        match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)', text, re.IGNORECASE)
        if match:
            hour = int(match.group(1))
            minute = match.group(2) or '00'
            period = match.group(3).lower().replace('.', '')
            
            if hour > 12:
                # 24-hour format
                hour = hour - 12
                period = 'pm'
            elif hour == 12:
                period = period  # Keep user's am/pm
            
            return (match.group(0), f"{hour}:{minute} {period.upper()}")
        
        # SECOND: Check for time-only numbers without am/pm (assume PM for dinner hours)
        match = re.search(r'\b(\d{1,2})(?::(\d{2}))?\b(?!\s*(am|pm))', text)
        if match and not re.search(r'\d{1,2}[/-]\d', text):  # Avoid matching dates
            hour = int(match.group(1))
            minute = match.group(2) or '00'
            if 1 <= hour <= 12:
                # Assume PM for hours 1-10 (dinner time), AM for 11-12
                period = 'PM' if 1 <= hour <= 10 else 'AM'
                return (match.group(0), f"{hour}:{minute} {period}")
        
        # LAST: Check time words (morning, evening, etc.) only if no explicit time
        for word, time_value in cls.TIME_WORDS.items():
            if word in text:
                return (word, time_value)
        
        return (None, None)
    
    @classmethod
    def _extract_event(cls, text: str) -> Optional[str]:
        """Extract event type from text."""
        for event_type, keywords in cls.EVENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return event_type
        return None
    
    @classmethod
    def _extract_menu(cls, text: str) -> Optional[str]:
        """Extract menu preference from text."""
        for menu_type, keywords in cls.MENU_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return menu_type
        return None
    
    @classmethod
    def _extract_addons(cls, text: str) -> List[str]:
        """Extract addon preferences from text."""
        addons = []
        for addon_type, keywords in cls.ADDON_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    addons.append(addon_type)
                    break
        return addons
    
    # ===========================================
    # HELPER METHODS
    # ===========================================
    
    @classmethod
    def _matches_patterns(cls, text: str, patterns: List[str]) -> bool:
        """Check if text matches any of the given patterns."""
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    @classmethod
    def _detect_language_switch(cls, text: str) -> Optional[str]:
        """Detect if user wants to switch language."""
        for lang, patterns in cls.LANGUAGE_SWITCH_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    # Make sure it's a language switch request, not part of longer text
                    if len(text.split()) <= 3:
                        return lang
        return None
    
    @classmethod
    def _detect_language(cls, text: str) -> Language:
        """Detect the language of input text."""
        # Tamil Unicode range check
        tamil_chars = len(re.findall(r'[\u0B80-\u0BFF]', text))
        if tamil_chars > 0:
            return Language.TAMIL
        
        # Tamil transliteration words
        tamil_words = ['iruku', 'panna', 'venum', 'illa', 'sari', 'romba', 
                       'nalla', 'enna', 'eppo', 'enga', 'yen', 'appa']
        for word in tamil_words:
            if word in text:
                return Language.TAMIL
        
        return Language.ENGLISH
    
    @classmethod
    def detect_cross_question(cls, text: str) -> Optional[str]:
        """
        Detect if user is asking a cross-question during booking.
        Returns the topic if found, None otherwise.
        """
        text_lower = text.lower()
        
        # Check various cross-question topics
        cross_topics = {
            'parking': cls.PARKING_PATTERNS,
            'timing': cls.TIMING_PATTERNS,
            'location': cls.LOCATION_PATTERNS,
            'offers': cls.OFFER_PATTERNS,
        }
        
        # Specific food items
        food_items = ['biryani', 'biriyani', 'chicken', 'mutton', 'paneer', 'fish']
        for item in food_items:
            if item in text_lower:
                return 'biryani' if 'biryani' in item or 'biriyani' in item else item
        
        # Facilities
        if any(re.search(p, text_lower) for p in cls.FACILITY_PATTERNS):
            if 'ac' in text_lower or 'air' in text_lower:
                return 'ac'
            if 'kid' in text_lower or 'child' in text_lower or 'play' in text_lower:
                return 'kids_area'
            if 'wifi' in text_lower:
                return 'wifi'
            if 'outdoor' in text_lower or 'garden' in text_lower:
                return 'outdoor'
            if 'projector' in text_lower:
                return 'projector'
        
        for topic, patterns in cross_topics.items():
            if cls._matches_patterns(text_lower, patterns):
                return topic
        
        return None


# Add method to ExtractedEntities to check if has booking data
def has_booking_data(self) -> bool:
    """Check if any booking-related entity was extracted."""
    return any([
        self.people is not None,
        self.parsed_date is not None,
        self.parsed_time is not None,
        self.event_type is not None,
    ])

# Monkey-patch the method onto the class
ExtractedEntities.has_booking_data = has_booking_data
