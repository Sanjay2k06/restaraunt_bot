"""
Server Sundharam Conversation Engine.
The brain of the bot - handles all conversation flows naturally.

Features:
- Natural language understanding
- Smart entity extraction from free-form text  
- Cross-question support during booking
- BookMyShow-style slot locking
- Human-like responses without technical language

Author: Server Sundharam Dev Team
Version: 2.0
"""

import logging
import random
from typing import Tuple, Optional, Dict, Any
from .models import ConversationStep, Intent, BotResponse
from .personality import ServerSundharam
from .nlp_intent import NLPEngine
from .language_switcher import LanguageSwitcher
from .session_manager import session_manager, SessionData
from .menu_engine import MenuEngine
from .slot_locker import slot_locker
from .booking_system import booking_system
from .config import settings

# Configure logging
logger = logging.getLogger(__name__)


class ConversationEngine:
    """
    Server Sundharam's conversation brain.
    Processes messages naturally like a human waiter.
    """
    
    @classmethod
    def process_message(cls, user_id: str, message: str) -> str:
        """
        Main entry point for processing user messages.
        Returns plain text response (no XML).
        """
        try:
            # Get or create session
            session = session_manager.get_session(user_id)
            lang = session.language
            msg = message.strip()
            
            # Log incoming message
            logger.info(f"[{user_id}] Step: {session.step}, Message: {msg[:50]}")
            
            # Detect intent and extract entities
            intent_result = NLPEngine.detect_intent(msg, lang)
            
            # Handle language switch first
            if intent_result.primary_intent == Intent.LANGUAGE_SWITCH:
                return cls._handle_language_switch(session, intent_result.language_detected.value)
            
            # Check for cross-questions during booking
            cross_topic = NLPEngine.detect_cross_question(msg)
            if cross_topic and session.step not in [ConversationStep.INIT.value, ConversationStep.GREETING.value]:
                return cls._handle_cross_question(session, cross_topic, lang)
            
            # Handle global commands
            if intent_result.primary_intent == Intent.RESTART:
                return cls._handle_restart(session, user_id, lang)
            
            if intent_result.primary_intent == Intent.CANCEL:
                return cls._handle_cancel(session, user_id, lang)
            
            if intent_result.primary_intent == Intent.HELP:
                return ServerSundharam.HELP_MESSAGE.get(lang, ServerSundharam.HELP_MESSAGE["en"])
            
            # Apply extracted entities to session if available
            if intent_result.entities.confidence > 0.5:
                cls._apply_entities_to_session(session, intent_result.entities)
            
            # Process based on current step
            return cls._process_step(session, msg, intent_result, lang, user_id)
            
        except Exception as e:
            logger.error(f"Error processing message for {user_id}: {str(e)}", exc_info=True)
            return cls._get_error_response(session.language if session else "en")
    
    @classmethod
    def _handle_language_switch(cls, session: SessionData, new_lang: str) -> str:
        """Handle language switch request."""
        session.language = new_lang
        return LanguageSwitcher.get_switch_confirmation(new_lang)
    
    @classmethod
    def _handle_cross_question(cls, session: SessionData, topic: str, lang: str) -> str:
        """Handle cross-question during booking flow."""
        answer = ServerSundharam.get_cross_answer(topic, lang)
        if answer:
            # Add continuation prompt
            if lang == "ta":
                continuation = "\n\nசரி, booking continue பண்ணலாமா?"
            else:
                continuation = "\n\nOkay, shall we continue with the booking?"
            return answer + continuation
        return ServerSundharam.get_fallback(lang)
    
    @classmethod
    def _handle_restart(cls, session: SessionData, user_id: str, lang: str) -> str:
        """Handle restart command."""
        slot_locker.release_lock(user_id)
        session_manager.reset_session(user_id)
        if lang == "ta":
            return "சரி சார்! Fresh start! 😊 என்ன help பண்ணலாம்?"
        return "Sure sir! Fresh start! 😊 How can I help you?"
    
    @classmethod
    def _handle_cancel(cls, session: SessionData, user_id: str, lang: str) -> str:
        """Handle cancel command."""
        name = session.name or "sir"
        slot_locker.release_lock(user_id)
        session_manager.clear_session(user_id)
        return random.choice(ServerSundharam.CANCELLED.get(lang, ServerSundharam.CANCELLED["en"])).format(name=name)
    
    @classmethod
    def _get_next_missing_step(cls, session: SessionData, lang: str) -> Tuple[ConversationStep, str]:
        """Determine next step and question based on what's already filled.
        
        This enables smart routing - if user already provided people, date, time, etc.
        in their initial message, skip those steps and go to the next missing field.
        """
        # Check in order: name → people → date → time → event → menu → addons → confirm
        if not session.name:
            return (ConversationStep.AWAITING_NAME, 
                    random.choice(ServerSundharam.ASK_NAME.get(lang, ServerSundharam.ASK_NAME["en"])))
        
        if not session.people:
            return (ConversationStep.AWAITING_PEOPLE,
                    random.choice(ServerSundharam.ASK_PEOPLE.get(lang, ServerSundharam.ASK_PEOPLE["en"])).format(name=session.name))
        
        if not session.date:
            return (ConversationStep.AWAITING_DATE,
                    random.choice(ServerSundharam.ASK_DATE.get(lang, ServerSundharam.ASK_DATE["en"])))
        
        if not session.time:
            return (ConversationStep.AWAITING_TIME,
                    random.choice(ServerSundharam.ASK_TIME.get(lang, ServerSundharam.ASK_TIME["en"])))
        
        if not session.event:
            return (ConversationStep.AWAITING_EVENT,
                    random.choice(ServerSundharam.ASK_EVENT.get(lang, ServerSundharam.ASK_EVENT["en"])))
        
        if not session.menu_pack:
            menu_intro = random.choice(ServerSundharam.MENU_INTRO.get(lang, ServerSundharam.MENU_INTRO["en"]))
            menu_list = MenuEngine.format_menu_list(lang)
            return (ConversationStep.AWAITING_MENU, f"{menu_intro}\n{menu_list}")
        
        if session.addons is None:  # Explicitly check None since empty list means no addons
            addon_intro = random.choice(ServerSundharam.ADDON_INTRO.get(lang, ServerSundharam.ADDON_INTRO["en"]))
            addon_list = MenuEngine.format_addon_list(lang)
            return (ConversationStep.AWAITING_ADDONS, f"{addon_intro}\n{addon_list}")
        
        # All filled - go to confirmation
        summary = cls._build_summary(session, lang)
        return (ConversationStep.AWAITING_CONFIRMATION, summary)

    @classmethod
    def _apply_entities_to_session(cls, session: SessionData, entities) -> None:
        """Apply extracted entities to session."""
        if entities.people and not session.people:
            session.people = entities.people
        if entities.parsed_date and not session.date:
            session.date = entities.parsed_date
        if entities.parsed_time and not session.time:
            session.time = entities.parsed_time
        if entities.event_type and not session.event:
            session.event = entities.event_type
        if entities.menu_preference and not session.menu_pack:
            session.menu_pack = entities.menu_preference
        if entities.name and not session.name:
            session.name = entities.name
    
    @classmethod
    def _process_step(cls, session: SessionData, msg: str, intent_result, lang: str, user_id: str) -> str:
        """Process message based on current conversation step."""
        step = session.step
        
        # STEP: INIT or GREETING
        if step in [ConversationStep.INIT.value, ConversationStep.GREETING.value, "init", "greeting"]:
            return cls._handle_init(session, msg, intent_result, lang)
        
        # STEP: AWAITING NAME
        elif step in [ConversationStep.AWAITING_NAME.value, "awaiting_name"]:
            return cls._handle_name_step(session, msg, lang)
        
        # STEP: AWAITING PEOPLE
        elif step in [ConversationStep.AWAITING_PEOPLE.value, "awaiting_people"]:
            return cls._handle_people_step(session, msg, intent_result, lang)
        
        # STEP: AWAITING DATE
        elif step in [ConversationStep.AWAITING_DATE.value, "awaiting_date"]:
            return cls._handle_date_step(session, msg, intent_result, lang)
        
        # STEP: AWAITING TIME
        elif step in [ConversationStep.AWAITING_TIME.value, "awaiting_time"]:
            return cls._handle_time_step(session, msg, intent_result, lang, user_id)
        
        # STEP: AWAITING EVENT
        elif step in [ConversationStep.AWAITING_EVENT.value, "awaiting_event"]:
            return cls._handle_event_step(session, msg, intent_result, lang)
        
        # STEP: AWAITING MENU
        elif step in [ConversationStep.AWAITING_MENU.value, "awaiting_menu"]:
            return cls._handle_menu_step(session, msg, intent_result, lang)
        
        # STEP: AWAITING ADDONS
        elif step in [ConversationStep.AWAITING_ADDONS.value, "awaiting_addons"]:
            return cls._handle_addons_step(session, msg, intent_result, lang)
        
        # STEP: AWAITING CONFIRMATION
        elif step in [ConversationStep.AWAITING_CONFIRMATION.value, "awaiting_confirmation"]:
            return cls._handle_confirmation_step(session, msg, intent_result, lang, user_id)
        
        # DEFAULT: Return to greeting
        else:
            session.step = ConversationStep.GREETING.value
            return cls._handle_init(session, msg, intent_result, lang)
    
    # ===========================================
    # STEP HANDLERS
    # ===========================================
    
    @classmethod
    def _handle_init(cls, session: SessionData, msg: str, intent_result, lang: str) -> str:
        """Handle initial greeting and intent detection."""
        msg_lower = msg.lower().strip()
        
        # Check if returning user
        if session.is_returning_user and session.user_memory:
            memory = session.user_memory
            name = memory.get("name", "sir")
            guests = memory.get("last_guests", 0)
            greeting = ServerSundharam.get_returning_greeting(name, guests, lang)
            session.name = name
            session.step = ConversationStep.AWAITING_PEOPLE.value
            return greeting
        
        # Check if user is selecting a menu pack (from greeting or after seeing menu)
        # This handles "veg", "veg pack", "veg menu", "deluxe party pack", etc.
        pack_selection = cls._detect_pack_selection(msg_lower)
        if pack_selection:
            # User selected a pack - start booking with this pack pre-selected
            session.menu_pack = pack_selection
            session.step = ConversationStep.AWAITING_NAME.value
            pack = MenuEngine.get_menu_pack(pack_selection)
            pack_name = pack.name_en if lang == "en" else pack.name_ta
            if lang == "ta":
                return f"👍 {pack_name} - நல்ல choice சார்!\n\nBooking-க்கு உங்க name சொல்லுங்க?"
            return f"👍 {pack_name} - Great choice!\n\nWhat name should I note for the booking?"
        
        # Check for booking intent with data
        if intent_result.primary_intent == Intent.BOOKING or intent_result.primary_intent == Intent.BOOKING_INFO:
            entities = intent_result.entities
            
            # If user gave all/some info in one message
            if entities.people or entities.parsed_date or entities.parsed_time:
                cls._apply_entities_to_session(session, entities)
                
                # Acknowledge what we understood
                ack = ServerSundharam.get_acknowledgment(lang)
                understood = cls._build_understood_response(session, lang)
                
                # Ask for next missing info
                next_question = cls._get_next_question(session, lang)
                
                return f"{ack} {understood}\n\n{next_question}"
            else:
                # Start booking flow
                session.step = ConversationStep.AWAITING_NAME.value
                return random.choice(ServerSundharam.ASK_NAME.get(lang, ServerSundharam.ASK_NAME["en"]))
        
        # Menu query - just show menu, don't start booking
        if intent_result.primary_intent == Intent.MENU_QUERY:
            menu_list = MenuEngine.format_menu_list(lang)
            if lang == "ta":
                intro = "சார், இதோ எங்க menu packs:\n\n_ஒன்னு select பண்ணுங்க - veg/nonveg/premium/deluxe_"
            else:
                intro = "Sir, here are our menu packs:\n\n_Select one to start booking - veg/nonveg/premium/deluxe_"
            return f"{intro}\n\n{menu_list}"
        
        # Default greeting
        greeting = ServerSundharam.get_greeting(lang)
        session.step = ConversationStep.GREETING.value
        return greeting
    
    @classmethod
    def _detect_pack_selection(cls, msg: str) -> Optional[str]:
        """Detect if user is selecting a menu pack."""
        # Pack synonyms
        pack_patterns = {
            'veg': ['veg', 'vegetarian', 'veg pack', 'veg menu', 'vegetarian pack', 'saiva'],
            'nonveg': ['nonveg', 'non-veg', 'non veg', 'nonveg pack', 'non veg pack', 'chicken', 'mutton pack'],
            'premium': ['premium', 'premium pack', 'special', 'special pack'],
            'deluxe': ['deluxe', 'deluxe pack', 'deluxe party', 'deluxe party pack', 'grand', 'party pack'],
        }
        
        for pack_key, patterns in pack_patterns.items():
            for pattern in patterns:
                if pattern in msg:
                    return pack_key
        return None
    
    @classmethod
    def _handle_name_step(cls, session: SessionData, msg: str, lang: str) -> str:
        """Handle name collection."""
        # Basic validation - accept any reasonable name
        name = msg.strip().title()
        if len(name) < 2 or len(name) > 50:
            if lang == "ta":
                return "சார், உங்க பேரு சொல்லுங்க please?"
            return "Sir, could you tell me your name please?"
        
        # Check if it might be a number or command
        if name.isdigit():
            if lang == "ta":
                return "சார், அது number மாதிரி இருக்கு. உங்க name சொல்லுங்க?"
            return "Sir, that looks like a number. What's your name?"
        
        session.name = name
        
        # Confirm name
        confirm = random.choice(ServerSundharam.NAME_CONFIRMED.get(lang, ServerSundharam.NAME_CONFIRMED["en"])).format(name=name)
        
        # Smart routing - check what's already filled and skip to next missing field
        next_step, next_question = cls._get_next_missing_step(session, lang)
        session.step = next_step.value
        
        return f"{confirm}\n\n{next_question}"
    
    @classmethod
    def _handle_people_step(cls, session: SessionData, msg: str, intent_result, lang: str) -> str:
        """Handle guest count collection."""
        # Try to extract number
        count = intent_result.entities.people
        if not count:
            # Try direct number parsing
            import re
            match = re.search(r'\d+', msg)
            if match:
                count = int(match.group())
        
        if not count or count < 1:
            if lang == "ta":
                return "சார், எத்தனை பேர் வருவீங்கன்னு சொல்லுங்க? (1-200)"
            return "Sir, how many guests? (1-200)"
        
        if count > 200:
            if lang == "ta":
                return f"Wow {count} பேர்! இந்த crowd-க்கு direct-ஆ {settings.RESTAURANT_PHONE}-ல call பண்ணுங்க special arrangements-க்கு."
            return f"Wow {count} guests! For this crowd, please call {settings.RESTAURANT_PHONE} for special arrangements."
        
        session.people = count
        
        # Confirm + seating hint
        confirm = random.choice(ServerSundharam.PEOPLE_CONFIRMED.get(lang, ServerSundharam.PEOPLE_CONFIRMED["en"])).format(count=count)
        seating = MenuEngine.get_seating_recommendation(count, lang)
        seating_hint = seating.message_en if lang == "en" else seating.message_ta
        
        # Smart routing - skip to next missing field
        next_step, next_question = cls._get_next_missing_step(session, lang)
        session.step = next_step.value
        
        return f"{confirm}{seating_hint}\n\n{next_question}"
    
    @classmethod
    def _handle_date_step(cls, session: SessionData, msg: str, intent_result, lang: str) -> str:
        """Handle date collection."""
        parsed_date = intent_result.entities.parsed_date
        
        if not parsed_date:
            # Try to parse ourselves
            from datetime import datetime, timedelta
            msg_lower = msg.lower()
            today = datetime.now()
            
            if 'tomorrow' in msg_lower or 'naale' in msg_lower:
                parsed_date = (today + timedelta(days=1)).strftime("%d-%m-%Y")
            elif 'today' in msg_lower or 'inniku' in msg_lower:
                parsed_date = today.strftime("%d-%m-%Y")
            else:
                # Try DD-MM-YYYY pattern
                import re
                match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', msg)
                if match:
                    d, m, y = match.groups()
                    if len(y) == 2:
                        y = '20' + y
                    try:
                        date_obj = datetime(int(y), int(m), int(d))
                        if date_obj.date() >= today.date():
                            parsed_date = date_obj.strftime("%d-%m-%Y")
                        else:
                            if lang == "ta":
                                return f"Oops சார், {d}-{m}-{y} already போயிடுச்சே! Future date சொல்லுங்க?"
                            return f"Oops sir, {d}-{m}-{y} has already passed! Please pick a future date?"
                    except:
                        pass
        
        if not parsed_date:
            if lang == "ta":
                return "சார், date புரியல. 'நாளை' அல்லது '25-02-2026' மாதிரி சொல்ல முடியுமா?"
            return "Sir, I couldn't understand the date. Could you say 'tomorrow' or '25-02-2026'?"
        
        session.date = parsed_date
        
        confirm = random.choice(ServerSundharam.DATE_CONFIRMED.get(lang, ServerSundharam.DATE_CONFIRMED["en"])).format(date=parsed_date)
        
        # Smart routing - skip to next missing field
        next_step, next_question = cls._get_next_missing_step(session, lang)
        session.step = next_step.value
        
        return f"{confirm}{next_question}"
    
    @classmethod
    def _handle_time_step(cls, session: SessionData, msg: str, intent_result, lang: str, user_id: str) -> str:
        """Handle time collection with slot locking."""
        parsed_time = intent_result.entities.parsed_time
        
        if not parsed_time:
            # Try to parse time
            import re
            msg_lower = msg.lower()
            
            time_words = {'morning': '10:00 AM', 'noon': '12:00 PM', 'afternoon': '2:00 PM',
                         'evening': '7:00 PM', 'night': '8:00 PM', 'dinner': '8:00 PM',
                         'lunch': '1:00 PM', 'malai': '7:00 PM'}
            
            for word, time_val in time_words.items():
                if word in msg_lower:
                    parsed_time = time_val
                    break
            
            if not parsed_time:
                match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?', msg_lower)
                if match:
                    hour = int(match.group(1))
                    minute = match.group(2) or '00'
                    period = (match.group(3) or '').lower().replace('.', '')
                    if not period:
                        period = 'pm' if 1 <= hour <= 10 else 'am'
                    if hour > 12:
                        period = 'pm'
                        hour = hour - 12 if hour > 12 else hour
                    parsed_time = f"{hour}:{minute} {period.upper()}"
        
        if not parsed_time:
            if lang == "ta":
                return f"சார், நாங்க {settings.RESTAURANT_TIMINGS} open. என்ன time-க்கு வரணும்?"
            return f"Sir, we're open {settings.RESTAURANT_TIMINGS}. What time works for you?"
        
        # Check slot availability
        checking_msg = random.choice(ServerSundharam.SLOT_CHECKING.get(lang, ServerSundharam.SLOT_CHECKING["en"]))
        
        success, status = slot_locker.lock_slot(session.date, parsed_time, user_id, session.people)
        
        if not success:
            if status == 'slot_locked_by_other':
                alternatives = slot_locker.get_alternative_times(session.date, parsed_time)
                msg = random.choice(ServerSundharam.SLOT_LOCKED_BY_OTHER.get(lang, ServerSundharam.SLOT_LOCKED_BY_OTHER["en"]))
                if alternatives:
                    alt_str = ", ".join(alternatives[:3])
                    if lang == "ta":
                        msg += f"\n\nAvailable times: {alt_str}"
                    else:
                        msg += f"\n\nAvailable times: {alt_str}"
                return msg
            
            if status == 'slot_already_booked':
                return random.choice(ServerSundharam.SLOT_ALREADY_BOOKED.get(lang, ServerSundharam.SLOT_ALREADY_BOOKED["en"]))
        
        session.time = parsed_time
        
        available_msg = random.choice(ServerSundharam.SLOT_AVAILABLE.get(lang, ServerSundharam.SLOT_AVAILABLE["en"]))
        confirm = random.choice(ServerSundharam.TIME_CONFIRMED.get(lang, ServerSundharam.TIME_CONFIRMED["en"])).format(time=parsed_time)
        
        # Smart routing - skip to next missing field
        next_step, next_question = cls._get_next_missing_step(session, lang)
        session.step = next_step.value
        
        return f"{confirm}{available_msg}\n\n{next_question}"
    
    @classmethod
    def _handle_event_step(cls, session: SessionData, msg: str, intent_result, lang: str) -> str:
        """Handle event type collection."""
        event = intent_result.entities.event_type or msg.strip().lower()
        
        # Normalize common event types
        event_mapping = {
            'birthday': 'birthday', 'bday': 'birthday', 'b\'day': 'birthday',
            'anniversary': 'anniversary', 'anni': 'anniversary',
            'corporate': 'corporate', 'office': 'corporate', 'meeting': 'corporate',
            'wedding': 'wedding', 'marriage': 'wedding', 'reception': 'wedding',
            'party': 'party', 'celebration': 'party', 'get together': 'casual',
            'casual': 'casual', 'family': 'casual', 'dinner': 'casual', 'lunch': 'casual',
            'casual get together': 'casual', 'get-together': 'casual',
            'date': 'date', 'romantic': 'date',
        }
        
        event_type = event_mapping.get(event, event)
        if len(event_type) < 2:
            event_type = 'casual'
        
        session.event = event_type
        
        # Get event-specific response
        event_response = ServerSundharam.EVENT_CONFIRMED[lang].get(event_type, ServerSundharam.EVENT_CONFIRMED[lang]["default"])
        
        # Check if menu pack was already selected (from greeting step)
        if session.menu_pack:
            # Skip menu selection, go to addons
            session.step = ConversationStep.AWAITING_ADDONS.value
            pack = MenuEngine.get_menu_pack(session.menu_pack)
            pack_name = pack.name_en if lang == "en" else pack.name_ta
            addon_intro = random.choice(ServerSundharam.ADDON_INTRO.get(lang, ServerSundharam.ADDON_INTRO["en"]))
            addon_list = MenuEngine.format_addon_list(lang)
            
            if lang == "ta":
                return f"{event_response}\n\nMenu: *{pack_name}* ✓\n\n{addon_intro}\n{addon_list}"
            return f"{event_response}\n\nMenu: *{pack_name}* ✓\n\n{addon_intro}\n{addon_list}"
        
        # No pack selected yet - show menu
        session.step = ConversationStep.AWAITING_MENU.value
        
        # Get recommendation
        rec = MenuEngine.get_event_recommendation(event_type, lang)
        
        # Show menu
        menu_intro = random.choice(ServerSundharam.MENU_INTRO.get(lang, ServerSundharam.MENU_INTRO["en"]))
        menu_list = MenuEngine.format_menu_list(lang)
        
        return f"{event_response}\n\n{rec['message']}\n\n{menu_intro}\n{menu_list}"
    
    @classmethod
    def _handle_menu_step(cls, session: SessionData, msg: str, intent_result, lang: str) -> str:
        """Handle menu pack selection."""
        menu_choice = intent_result.entities.menu_preference
        
        if not menu_choice:
            msg_lower = msg.lower()
            menu_keywords = {
                'veg': ['veg', 'vegetarian', 'saiva'],
                'nonveg': ['nonveg', 'non-veg', 'non veg', 'chicken', 'mutton'],
                'premium': ['premium', 'special'],
                'deluxe': ['deluxe', 'grand', 'party'],
            }
            for menu_type, keywords in menu_keywords.items():
                if any(kw in msg_lower for kw in keywords):
                    menu_choice = menu_type
                    break
        
        if not menu_choice or menu_choice not in MenuEngine.MENU_PACKS:
            if lang == "ta":
                return "சார், எந்த pack: veg, nonveg, premium, அல்லது deluxe?"
            return "Sir, which pack would you like: veg, nonveg, premium, or deluxe?"
        
        session.menu_pack = menu_choice
        session.step = ConversationStep.AWAITING_ADDONS.value
        
        pack = MenuEngine.get_menu_pack(menu_choice)
        pack_name = pack.name_en if lang == "en" else pack.name_ta
        
        ack = ServerSundharam.get_acknowledgment(lang)
        addon_intro = random.choice(ServerSundharam.ADDON_INTRO.get(lang, ServerSundharam.ADDON_INTRO["en"]))
        addon_list = MenuEngine.format_addon_list(lang)
        
        return f"{ack} {pack_name} selected!\n\n{addon_intro}\n{addon_list}"
    
    @classmethod
    def _handle_addons_step(cls, session: SessionData, msg: str, intent_result, lang: str) -> str:
        """Handle addon selection."""
        msg_lower = msg.lower()
        
        # Check for "none" or "no"
        if any(word in msg_lower for word in ['none', 'no', 'skip', 'illa', 'வேண்டாம்']):
            session.addons = []
        else:
            # Extract addon mentions
            addon_keywords = {
                'decoration': ['decoration', 'decor'],
                'cake': ['cake'],
                'photography': ['photo', 'photography', 'photographer'],
                'music_system': ['music', 'speaker'],
                'dj': ['dj'],
                'flowers': ['flower', 'flowers', 'bouquet'],
                'balloons': ['balloon', 'balloons'],
                'projector': ['projector', 'screen'],
            }
            
            selected = []
            for addon_key, keywords in addon_keywords.items():
                if any(kw in msg_lower for kw in keywords):
                    selected.append(addon_key)
            
            session.addons = selected if selected else intent_result.entities.addons
        
        session.step = ConversationStep.AWAITING_CONFIRMATION.value
        
        # Build confirmation summary
        summary = cls._build_booking_summary(session, lang)
        ask_confirm = random.choice(ServerSundharam.ASK_CONFIRMATION.get(lang, ServerSundharam.ASK_CONFIRMATION["en"]))
        
        return f"{summary}\n\n{ask_confirm}"
    
    @classmethod
    def _handle_confirmation_step(cls, session: SessionData, msg: str, intent_result, lang: str, user_id: str) -> str:
        """Handle final confirmation."""
        msg_lower = msg.lower()
        
        # Check for yes/confirm
        yes_words = ['yes', 'yeah', 'yep', 'ok', 'okay', 'sure', 'confirm', 'sari', 'ஆமா', 'சரி']
        no_words = ['no', 'nope', 'cancel', 'change', 'illa', 'வேண்டாம்']
        
        if any(word in msg_lower for word in yes_words) or intent_result.primary_intent == Intent.CONFIRM:
            # Create the booking
            result = booking_system.create_reservation(
                user_id=user_id,
                name=session.name,
                people=session.people,
                date=session.date,
                time=session.time,
                event=session.event,
                menu_pack=session.menu_pack,
                addons=session.addons or [],
                lang=lang
            )
            
            # Save user memory for future
            session_manager.save_user_memory(user_id, session.name, session.people, session.menu_pack)
            
            # Clear session
            session_manager.clear_session(user_id)
            
            # Return confirmation message
            if lang == "ta":
                return result["confirmation_ta"]
            return result["confirmation_en"]
        
        elif any(word in msg_lower for word in no_words) or intent_result.primary_intent == Intent.DENY:
            return cls._handle_cancel(session, user_id, lang)
        
        else:
            if lang == "ta":
                return "சார், 'Yes' confirm பண்ண அல்லது 'No' cancel பண்ண சொல்லுங்க?"
            return "Sir, please say 'Yes' to confirm or 'No' to cancel?"
    
    # ===========================================
    # HELPER METHODS
    # ===========================================
    
    @classmethod
    def _build_understood_response(cls, session: SessionData, lang: str) -> str:
        """Build response showing what we understood from user input."""
        parts = []
        
        if session.people:
            if lang == "ta":
                parts.append(f"{session.people} பேர்")
            else:
                parts.append(f"{session.people} guests")
        
        if session.date:
            parts.append(session.date)
        
        if session.time:
            parts.append(session.time)
        
        if session.event:
            parts.append(session.event)
        
        if parts:
            if lang == "ta":
                return f"நான் புரிஞ்சது: {', '.join(parts)}"
            return f"I understood: {', '.join(parts)}"
        return ""
    
    @classmethod
    def _get_next_question(cls, session: SessionData, lang: str) -> str:
        """Get the next question based on missing information."""
        if not session.name:
            session.step = ConversationStep.AWAITING_NAME.value
            return random.choice(ServerSundharam.ASK_NAME.get(lang, ServerSundharam.ASK_NAME["en"]))
        
        if not session.people:
            session.step = ConversationStep.AWAITING_PEOPLE.value
            return random.choice(ServerSundharam.ASK_PEOPLE.get(lang, ServerSundharam.ASK_PEOPLE["en"])).format(name=session.name)
        
        if not session.date:
            session.step = ConversationStep.AWAITING_DATE.value
            return random.choice(ServerSundharam.ASK_DATE.get(lang, ServerSundharam.ASK_DATE["en"]))
        
        if not session.time:
            session.step = ConversationStep.AWAITING_TIME.value
            return random.choice(ServerSundharam.ASK_TIME.get(lang, ServerSundharam.ASK_TIME["en"]))
        
        if not session.event:
            session.step = ConversationStep.AWAITING_EVENT.value
            return random.choice(ServerSundharam.ASK_EVENT.get(lang, ServerSundharam.ASK_EVENT["en"]))
        
        if not session.menu_pack:
            session.step = ConversationStep.AWAITING_MENU.value
            menu_list = MenuEngine.format_menu_list(lang)
            intro = random.choice(ServerSundharam.MENU_INTRO.get(lang, ServerSundharam.MENU_INTRO["en"]))
            return f"{intro}\n{menu_list}"
        
        # All info collected
        session.step = ConversationStep.AWAITING_ADDONS.value
        addon_intro = random.choice(ServerSundharam.ADDON_INTRO.get(lang, ServerSundharam.ADDON_INTRO["en"]))
        addon_list = MenuEngine.format_addon_list(lang)
        return f"{addon_intro}\n{addon_list}"
    
    @classmethod
    def _build_booking_summary(cls, session: SessionData, lang: str) -> str:
        """Build booking summary for confirmation."""
        pack = MenuEngine.get_menu_pack(session.menu_pack) if session.menu_pack else None
        pack_name = ""
        if pack:
            pack_name = pack.name_en if lang == "en" else pack.name_ta
        
        base_cost, addon_cost, total = MenuEngine.calculate_cost(
            session.people or 0, 
            session.menu_pack or "veg", 
            session.addons or []
        )
        
        addon_names = []
        for addon_key in (session.addons or []):
            addon = MenuEngine.get_addon(addon_key)
            if addon:
                addon_names.append(addon.name_en if lang == "en" else addon.name_ta)
        addons_str = ", ".join(addon_names) if addon_names else ("None" if lang == "en" else "இல்லை")
        
        # Get seating
        seating = MenuEngine.get_seating_recommendation(session.people or 1, lang)
        
        intro = random.choice(ServerSundharam.BOOKING_SUMMARY_INTRO.get(lang, ServerSundharam.BOOKING_SUMMARY_INTRO["en"])).format(name=session.name)
        
        if lang == "ta":
            summary = f"""
{intro}

━━━━━━━━━━━━━━━━━━━━━
📋 *Booking Summary*
━━━━━━━━━━━━━━━━━━━━━
👤 Name: *{session.name}*
👥 Guests: *{session.people} பேர்*
📅 Date: *{session.date}*
⏰ Time: *{session.time}*
🎊 Event: *{session.event}*
🍽️ Menu: *{pack_name}*
✨ Addons: *{addons_str}*

━━━━━━━━━━━━━━━━━━━━━
💰 *Cost Estimate*
━━━━━━━━━━━━━━━━━━━━━
Menu: ₹{base_cost}
Addons: ₹{addon_cost}
*Total: ₹{total}*

{seating.layout_visual}
"""
        else:
            summary = f"""
{intro}

━━━━━━━━━━━━━━━━━━━━━
📋 *Booking Summary*
━━━━━━━━━━━━━━━━━━━━━
👤 Name: *{session.name}*
👥 Guests: *{session.people} people*
📅 Date: *{session.date}*
⏰ Time: *{session.time}*
🎊 Event: *{session.event}*
🍽️ Menu: *{pack_name}*
✨ Addons: *{addons_str}*

━━━━━━━━━━━━━━━━━━━━━
💰 *Cost Estimate*
━━━━━━━━━━━━━━━━━━━━━
Menu: ₹{base_cost}
Addons: ₹{addon_cost}
*Total: ₹{total}*

{seating.layout_visual}
"""
        return summary.strip()
    
    @classmethod
    def _get_error_response(cls, lang: str) -> str:
        """Get error response."""
        if lang == "ta":
            return "Sorry சார், ஏதோ problem ஆயிடுச்சு. மீண்டும் try பண்ணுங்க?"
        return "Sorry sir, something went wrong. Please try again?"


# Convenience function
def process_message(user: str, message: str) -> str:
    """Process message (backward compatible interface)."""
    return ConversationEngine.process_message(user, message)

