"""
Server Sundharam's Personality Module.
Contains all human-like responses, phrases, and character traits.

This module makes the bot feel like a real friendly waiter,
not a robotic AI assistant.

Author: Server Sundharam Dev Team
Version: 2.0
"""

import random
from typing import Dict, List, Optional
from .config import settings


class ServerSundharam:
    """
    Server Sundharam - The friendly online waiter.
    
    Personality traits:
    - Warm and welcoming
    - Uses casual, friendly language
    - Mixes English and Tamil naturally
    - Adds humor when appropriate
    - Never sounds robotic or technical
    """
    
    # ===========================================
    # GREETING RESPONSES
    # ===========================================
    
    GREETINGS = {
        "en": [
            f"Hello sir! I'm {settings.BOT_NAME}, your online waiter at {settings.RESTAURANT_NAME} 😊 How can I help you today?",
            f"Hey there! {settings.BOT_NAME} here, ready to serve you! What would you like to do?",
            f"Welcome welcome! {settings.BOT_NAME} at your service 🙏 Table booking? Or just checking our menu?",
            f"Hi sir/madam! {settings.BOT_NAME} here from {settings.RESTAURANT_NAME}. What can I do for you today?",
        ],
        "ta": [
            f"வணக்கம் சார்! நான் {settings.BOT_NAME}, உங்கள் online waiter 😊 எப்படி help பண்ணலாம்?",
            f"Hello சார்! {settings.BOT_NAME} இங்க! என்ன service வேணும்?",
            f"வணக்கம் வணக்கம்! {settings.BOT_NAME} உங்கள் சேவையில் 🙏 Table book பண்ணணுமா?",
            f"Hi சார்! {settings.RESTAURANT_NAME}-ல இருந்து {settings.BOT_NAME}. என்ன help?",
        ]
    }
    
    # ===========================================
    # RETURNING USER GREETINGS
    # ===========================================
    
    RETURNING_USER_GREETINGS = {
        "en": [
            "Welcome back {name} sir! Last time you booked for {guests} guests. Same setup today?",
            "Hey {name}! Good to see you again! Planning another event?",
            "Oh {name} sir! Welcome back to {restaurant}! What's the occasion this time?",
        ],
        "ta": [
            "Welcome back {name} சார்! Last time {guests} பேருக்கு book பண்ணீங்க. Same-aa?",
            "Hey {name}! திரும்பவும் வந்தீங்க! என்ன plan?",
            "அட {name} சார்! மீண்டும் வரவேற்கிறோம்! இந்த தடவை என்ன occasion?",
        ]
    }
    
    # ===========================================
    # ASKING FOR NAME
    # ===========================================
    
    ASK_NAME = {
        "en": [
            "Super! Before we proceed, may I know your good name please?",
            "Lovely! What name should I note the booking under?",
            "Nice! Can I get your name for the reservation?",
        ],
        "ta": [
            "Super! உங்க நல்ல பேரு என்னன்னு சொல்லுங்க?",
            "சரி! யாரு பேர்ல booking போடணும்?",
            "நல்லது! உங்க name சொல்லுங்க reservation-க்கு",
        ]
    }
    
    # ===========================================
    # NAME CONFIRMATION
    # ===========================================
    
    NAME_CONFIRMED = {
        "en": [
            "Nice to meet you, {name}! 😊",
            "Welcome {name}! Happy to serve you!",
            "Noted, {name} sir/madam! Let's proceed.",
            "Great name, {name}! Now let's plan your visit.",
        ],
        "ta": [
            "சந்தோஷம் {name}! 😊",
            "Welcome {name}! உங்களுக்கு service பண்ண happy!",
            "Noted {name} சார்! போகலாம் வாங்க.",
            "Super {name}! இப்போ plan பண்ணலாம்.",
        ]
    }
    
    # ===========================================
    # ASKING FOR PEOPLE COUNT
    # ===========================================
    
    ASK_PEOPLE = {
        "en": [
            "How many guests will be joining, {name}?",
            "And how many people should I arrange for?",
            "Cool! How many will be coming?",
            "Nice! Total எத்தனை பேர் sir?",
        ],
        "ta": [
            "எத்தனை பேர் வருவீங்க {name}?",
            "Total guests எத்தனை?",
            "எத்தனை பேருக்கு arrange பண்ணணும்?",
        ]
    }
    
    # ===========================================
    # PEOPLE COUNT CONFIRMATION
    # ===========================================
    
    PEOPLE_CONFIRMED = {
        "en": [
            "Got it! {count} guests. ",
            "Noted! Arranging for {count} people. ",
            "Perfect! {count} பேர். ",
            "{count} guests - noted sir! ",
        ],
        "ta": [
            "OK சார்! {count} பேர். ",
            "Noted! {count} guests-க்கு arrange பண்றேன். ",
            "சரி சார்! {count} பேர். ",
        ]
    }
    
    # ===========================================
    # ASKING FOR DATE
    # ===========================================
    
    ASK_DATE = {
        "en": [
            "When would you like to come? You can say 'tomorrow', 'next Saturday', or a specific date.",
            "What date works for you?",
            "Which day are you planning to visit?",
        ],
        "ta": [
            "எப்போ வரணும்? 'நாளை', 'அடுத்த சனிக்கிழமை', அல்லது date சொல்லலாம்.",
            "எந்த date-க்கு plan?",
            "எந்த நாள் வரணும் சார்?",
        ]
    }
    
    # ===========================================
    # DATE CONFIRMATION
    # ===========================================
    
    DATE_CONFIRMED = {
        "en": [
            "Alright, {date} it is! ",
            "Perfect! Marking {date}. ",
            "{date} - noted! ",
        ],
        "ta": [
            "OK, {date} fix! ",
            "Super! {date} note பண்றேன். ",
            "{date} - OK சார்! ",
        ]
    }
    
    # ===========================================
    # ASKING FOR TIME
    # ===========================================
    
    ASK_TIME = {
        "en": [
            "What time should I reserve? You can say 'evening', '7pm', or any time between 11 AM - 11 PM.",
            "What time works for you?",
            "And the timing?",
        ],
        "ta": [
            "என்ன time-க்கு? 'மாலை', '7pm' அல்லது 11 AM - 11 PM-க்குள் சொல்லலாம்.",
            "எந்த நேரம்?",
            "Time என்ன சார்?",
        ]
    }
    
    # ===========================================
    # TIME CONFIRMATION
    # ===========================================
    
    TIME_CONFIRMED = {
        "en": [
            "{time} - perfect timing! ",
            "Got it! {time}. ",
            "Noted - {time}. ",
        ],
        "ta": [
            "{time} - super timing! ",
            "OK! {time}. ",
            "Noted - {time}. ",
        ]
    }
    
    # ===========================================
    # ASKING FOR EVENT TYPE
    # ===========================================
    
    ASK_EVENT = {
        "en": [
            "What's the occasion? Birthday? Anniversary? Corporate meeting? Or just a casual get-together?",
            "Is this for any special event?",
            "Any particular occasion we should prepare for?",
        ],
        "ta": [
            "என்ன occasion சார்? Birthday? Anniversary? Meeting? அல்லது casual gathering?",
            "ஏதாவது special event-ஆ?",
            "என்ன function-க்கு?",
        ]
    }
    
    # ===========================================
    # EVENT CONFIRMATION WITH RECOMMENDATION
    # ===========================================
    
    EVENT_CONFIRMED = {
        "en": {
            "birthday": "Aha! Birthday party! 🎂 Let me suggest some special arrangements...",
            "anniversary": "How lovely! Anniversary celebration! 💕 I have some romantic setup ideas...",
            "corporate": "Corporate event - got it! 💼 Let me show professional options...",
            "wedding": "Wedding function! 💒 This calls for our grand arrangements...",
            "casual": "Casual dining - nice! Simple and elegant it is!",
            "default": "Nice! Let me show you our best options..."
        },
        "ta": {
            "birthday": "Birthday party! 🎂 Special arrangements suggest பண்றேன்...",
            "anniversary": "Anniversary! 💕 Romantic setup ideas இருக்கு...",
            "corporate": "Corporate event! 💼 Professional options காட்றேன்...",
            "wedding": "Wedding function! 💒 Grand arrangements ready...",
            "casual": "Casual dining - nice! Simple-ஆ arrange பண்றேன்!",
            "default": "நல்லது! Best options காட்றேன்..."
        }
    }
    
    # ===========================================
    # MENU PRESENTATION
    # ===========================================
    
    MENU_INTRO = {
        "en": [
            "Here are our menu packs. Pick one that suits your taste:",
            "Sir, we have these special menu options:",
            "Take a look at our delicious menu packs:",
        ],
        "ta": [
            "இதோ எங்க menu packs. உங்க taste-க்கு pick பண்ணுங்க:",
            "சார், இந்த special menu options இருக்கு:",
            "எங்க tasty menu packs பாருங்க:",
        ]
    }
    
    # ===========================================
    # ADDON PRESENTATION
    # ===========================================
    
    ADDON_INTRO = {
        "en": [
            "Want to add any extras? We have:",
            "Some add-ons to make it special:",
            "Optional extras available:",
        ],
        "ta": [
            "Extras add பண்ணணுமா? இருக்கு:",
            "Special-ஆ இதெல்லாம் add பண்ணலாம்:",
            "Optional adds இருக்கு:",
        ]
    }
    
    # ===========================================
    # SLOT LOCKING MESSAGES
    # ===========================================
    
    SLOT_CHECKING = {
        "en": [
            "One moment sir, let me check availability...",
            "Checking our table availability... ✨",
            "Just a sec, verifying the slot...",
        ],
        "ta": [
            "ஒரு நிமிஷம் சார், availability check பண்றேன்...",
            "Table availability பாக்கறேன்... ✨",
            "Just a sec, slot verify பண்றேன்...",
        ]
    }
    
    SLOT_AVAILABLE = {
        "en": [
            "Great news! This slot is available! 🎉 I've held it for you for 3 minutes while you confirm.",
            "Good news sir! Slot available! Reserved temporarily for you.",
            "Perfect! I've locked this slot for you. Please confirm within 3 minutes.",
        ],
        "ta": [
            "Super news! இந்த slot available! 🎉 3 minutes உங்களுக்கு hold பண்றேன்.",
            "Good news சார்! Slot இருக்கு! Temporarily reserve பண்ணிட்டேன்.",
            "Perfect! Slot lock பண்ணிட்டேன். 3 minutes-ல confirm பண்ணுங்க.",
        ]
    }
    
    SLOT_LOCKED_BY_OTHER = {
        "en": [
            "Oops sir, this time slot is temporarily held by another guest. Can I suggest a different time?",
            "Sorry sir, someone else is booking this slot right now. Should I check nearby times?",
            "This slot is currently being held. Want me to show other available times?",
        ],
        "ta": [
            "Oops சார், இந்த slot வேற யாரோ hold பண்ணிருக்காங்க. வேற time suggest பண்ணட்டுமா?",
            "Sorry சார், யாரோ இந்த slot book பண்றாங்க. Nearby times check பண்ணட்டுமா?",
            "இந்த slot hold-ல இருக்கு. வேற times காட்டட்டுமா?",
        ]
    }
    
    SLOT_ALREADY_BOOKED = {
        "en": [
            "Sir, this slot is already confirmed by another guest. Let me suggest alternatives.",
            "Apologies, this time is fully booked. How about these options?",
        ],
        "ta": [
            "சார், இந்த slot already booked ஆயிடுச்சு. வேற options சொல்றேன்.",
            "Sorry சார், இந்த time full. இந்த options எப்படி?",
        ]
    }
    
    # ===========================================
    # CONFIRMATION MESSAGES
    # ===========================================
    
    BOOKING_SUMMARY_INTRO = {
        "en": [
            "Alright {name}, here's your booking summary:",
            "Perfect! Let me confirm the details, {name}:",
            "Here's what I have noted down:",
        ],
        "ta": [
            "சரி {name}, இதோ உங்க booking summary:",
            "Perfect! Details confirm பண்றேன் {name}:",
            "இதோ note பண்ணிருக்கேன்:",
        ]
    }
    
    ASK_CONFIRMATION = {
        "en": [
            "Everything look good? Reply 'Yes' to confirm or 'No' to make changes.",
            "Shall I confirm this booking? Say Yes or No.",
            "Ready to book? Just say Yes to confirm!",
        ],
        "ta": [
            "எல்லாம் சரியா இருக்கா? 'Yes' confirm or 'No' change பண்ண.",
            "Booking confirm பண்ணட்டுமா? Yes அல்லது No சொல்லுங்க.",
            "Ready-ஆ? Yes சொன்னா confirm பண்ணிடறேன்!",
        ]
    }
    
    BOOKING_CONFIRMED = {
        "en": [
            "🎉 BOOKING CONFIRMED! 🎉\n\nThank you {name}! Your table is reserved. See you on {date} at {time}!\n\nReservation ID: {id}\n\nFor any changes, just message me!",
            "✅ Done and done! {name}, your booking is confirmed!\n\nID: {id}\nDate: {date}\nTime: {time}\n\nWe're excited to serve you!",
        ],
        "ta": [
            "🎉 BOOKING CONFIRMED! 🎉\n\nநன்றி {name}! Table reserve ஆயிடுச்சு. {date} அன்று {time}-க்கு சந்திப்போம்!\n\nReservation ID: {id}\n\nChanges இருந்தா message பண்ணுங்க!",
            "✅ Done! {name}, booking confirm ஆயிடுச்சு!\n\nID: {id}\nDate: {date}\nTime: {time}\n\nஉங்களை serve பண்ண excited!",
        ]
    }
    
    # ===========================================
    # CANCELLATION
    # ===========================================
    
    CANCELLED = {
        "en": [
            "No problem {name}! I've cancelled the booking process. Feel free to start again anytime!",
            "Alright, cancelled. Come back whenever you're ready!",
        ],
        "ta": [
            "No problem {name}! Booking cancel பண்ணிட்டேன். Anytime திரும்ப வாங்க!",
            "சரி, cancel பண்ணிட்டேன். Ready-ஆ இருக்கும்போது வாங்க!",
        ]
    }
    
    # ===========================================
    # CROSS-QUESTION ANSWERS
    # ===========================================
    
    CROSS_QUESTION_ANSWERS = {
        "parking": {
            "en": f"Yes sir! {settings.PARKING_INFO}",
            "ta": f"ஆமா சார்! Free valet parking இருக்கு. 50+ cars fit ஆகும்."
        },
        "timing": {
            "en": f"We're open {settings.RESTAURANT_TIMINGS}. Best to come during evening for the full experience!",
            "ta": f"நாங்க {settings.RESTAURANT_TIMINGS} open. Evening-ல வந்தா best experience!"
        },
        "location": {
            "en": f"We're at {settings.RESTAURANT_LOCATION}. Easy to find, Google Maps-ல search பண்ணுங்க!",
            "ta": f"எங்க address: {settings.RESTAURANT_LOCATION}. Google Maps-ல search பண்ணுங்க சார்!"
        },
        "ac": {
            "en": "100% fully air-conditioned! All our halls and dining areas are cool and comfortable.",
            "ta": "Full AC சார்! எல்லா halls-உம் dining areas-உம் AC."
        },
        "kids_area": {
            "en": "Yes! We have a kids play area with toys and games. Parents can relax!",
            "ta": "ஆமா! Kids play area இருக்கு, toys and games-உடன். Parents relax பண்ணலாம்!"
        },
        "wifi": {
            "en": "Free high-speed WiFi available throughout the restaurant!",
            "ta": "Free WiFi இருக்கு சார், full restaurant-லயும்!"
        },
        "biryani": {
            "en": "Of course! Our Hyderabadi Dum Biryani is legendary! Available in veg, chicken, and mutton.",
            "ta": "நிச்சயமா! எங்க Hyderabadi Dum Biryani famous! Veg, chicken, mutton எல்லாம் இருக்கு."
        },
        "offers": {
            "en": "Yes sir! 10% off for groups above 20, and free cake for birthday bookings!",
            "ta": "ஆமா சார்! 20 பேருக்கு மேல 10% off, Birthday-க்கு free cake!"
        },
        "projector": {
            "en": "Yes, projector available for corporate events. ₹500 extra. Should I add it?",
            "ta": "ஆமா, projector இருக்கு corporate events-க்கு. ₹500 extra. Add பண்ணட்டுமா?"
        },
        "outdoor": {
            "en": "Beautiful outdoor garden seating available! Perfect for evening events.",
            "ta": "Outdoor garden seating இருக்கு சார்! Evening events-க்கு perfect."
        }
    }
    
    # ===========================================
    # FALLBACK / UNKNOWN
    # ===========================================
    
    FALLBACK = {
        "en": [
            "Hmm, I didn't quite get that. Could you say it differently? Or say 'help' for options.",
            "Sorry sir, I'm a bit confused. Can you rephrase? You can also type 'menu' or 'book'.",
            "I'm not sure I understood. Want to book a table? Just say 'book' or 'reservation'!",
        ],
        "ta": [
            "Hmm, புரியல சார். வேற மாதிரி சொல்ல முடியுமா? 'help' type பண்ணலாம்.",
            "Sorry சார், confuse ஆயிடுச்சு. 'menu' அல்லது 'book' சொல்லலாம்.",
            "புரியல சார். Table book பண்ணணுமா? 'book' சொல்லுங்க!",
        ]
    }
    
    # ===========================================
    # HELP MESSAGE
    # ===========================================
    
    HELP_MESSAGE = {
        "en": f"""
I'm {settings.BOT_NAME}, your friendly online waiter! Here's what I can help with:

📋 *Book a table* - Just say "book" or "reserve"
🍽️ *See menu* - Say "menu" or "food"
❓ *Ask questions* - Parking? Timings? Just ask!
🔄 *Start over* - Say "restart"
❌ *Cancel* - Say "cancel"
🌐 *Tamil* - Say "tamil" to switch

Feel free to ask anything!
""",
        "ta": f"""
நான் {settings.BOT_NAME}, உங்க online waiter! என்னால் help பண்ண முடியும்:

📋 *Table book* - "book" சொல்லுங்க
🍽️ *Menu* - "menu" சொல்லுங்க
❓ *Questions* - Parking? Timings? கேளுங்க!
🔄 *Start over* - "restart" சொல்லுங்க
❌ *Cancel* - "cancel" சொல்லுங்க
🌐 *English* - "english" சொல்லுங்க

Feel free to ask!
"""
    }
    
    # ===========================================
    # THINKING / PROCESSING PHRASES
    # ===========================================
    
    THINKING_PHRASES = {
        "en": [
            "One moment...",
            "Let me check...",
            "Hold on sir...",
            "Checking...",
        ],
        "ta": [
            "ஒரு நிமிஷம்...",
            "Check பண்றேன்...",
            "Hold on சார்...",
            "பாக்கறேன்...",
        ]
    }
    
    # ===========================================
    # SEATING RECOMMENDATIONS
    # ===========================================
    
    SEATING_MESSAGES = {
        "table": {
            "en": "For {count} guests, I'll arrange a nice cozy table setup.",
            "ta": "{count} பேருக்கு nice table arrange பண்றேன்."
        },
        "multi_table": {
            "en": "For {count} guests, I'll set up {tables} tables together. Comfortable family-style seating!",
            "ta": "{count} பேருக்கு {tables} tables arrange பண்றேன். Family-style seating!"
        },
        "mini_hall": {
            "en": "For {count} guests, I recommend our Mini Hall - perfect for private gatherings! 🏛️",
            "ta": "{count} பேருக்கு எங்க Mini Hall recommend பண்றேன் - private gatherings-க்கு perfect! 🏛️"
        },
        "banquet_hall": {
            "en": "Wow, {count} guests! Let me book our Grand Banquet Hall for you! 🎉",
            "ta": "Wow, {count} பேர்! Grand Banquet Hall book பண்றேன்! 🎉"
        }
    }
    
    # ===========================================
    # SOFT CORRECTIONS
    # ===========================================
    
    SOFT_CORRECTIONS = {
        "past_date": {
            "en": "Oops sir, {date} is already passed! Did you mean a future date?",
            "ta": "Oops சார், {date} already போயிடுச்சே! Future date-ஆ?"
        },
        "invalid_date": {
            "en": "Hmm, I couldn't understand that date. Could you try something like 'tomorrow' or '25-02-2026'?",
            "ta": "Hmm, date புரியல. 'நாளை' அல்லது '25-02-2026' மாதிரி சொல்ல முடியுமா?"
        },
        "invalid_time": {
            "en": "Sir, we're open {timings}. Could you pick a time within that?",
            "ta": "சார், நாங்க {timings} தான் open. அந்த time-ல choose பண்ணுங்க?"
        },
        "too_many_guests": {
            "en": "Wow that's a big crowd! For {count}+ guests, please call us at {phone} for special arrangements.",
            "ta": "Wow பெரிய crowd! {count}+ guests-க்கு {phone}-ல call பண்ணுங்க special arrangements-க்கு."
        }
    }
    
    # ===========================================
    # ACKNOWLEDGMENTS
    # ===========================================
    
    ACKNOWLEDGMENTS = {
        "en": ["Super!", "Noted!", "Got it!", "Perfect!", "Lovely!", "Great!"],
        "ta": ["Super!", "Noted!", "OK சார்!", "Perfect!", "நல்லது!", "Great!"]
    }
    
    # ===========================================
    # HELPER METHODS
    # ===========================================
    
    @classmethod
    def get_greeting(cls, lang: str = "en") -> str:
        """Get a random greeting message."""
        return random.choice(cls.GREETINGS.get(lang, cls.GREETINGS["en"]))
    
    @classmethod
    def get_returning_greeting(cls, name: str, guests: int, lang: str = "en") -> str:
        """Get personalized greeting for returning user."""
        template = random.choice(cls.RETURNING_USER_GREETINGS.get(lang, cls.RETURNING_USER_GREETINGS["en"]))
        return template.format(name=name, guests=guests, restaurant=settings.RESTAURANT_NAME)
    
    @classmethod
    def get_acknowledgment(cls, lang: str = "en") -> str:
        """Get a random acknowledgment phrase."""
        return random.choice(cls.ACKNOWLEDGMENTS.get(lang, cls.ACKNOWLEDGMENTS["en"]))
    
    @classmethod
    def get_thinking(cls, lang: str = "en") -> str:
        """Get a random thinking phrase."""
        return random.choice(cls.THINKING_PHRASES.get(lang, cls.THINKING_PHRASES["en"]))
    
    @classmethod
    def get_fallback(cls, lang: str = "en") -> str:
        """Get a random fallback message."""
        return random.choice(cls.FALLBACK.get(lang, cls.FALLBACK["en"]))
    
    @classmethod
    def get_cross_answer(cls, topic: str, lang: str = "en") -> Optional[str]:
        """Get answer for cross-question topic."""
        if topic in cls.CROSS_QUESTION_ANSWERS:
            return cls.CROSS_QUESTION_ANSWERS[topic].get(lang, cls.CROSS_QUESTION_ANSWERS[topic]["en"])
        return None
    
    @classmethod
    def format_response(cls, key: str, lang: str = "en", **kwargs) -> str:
        """Get and format a response template."""
        templates = getattr(cls, key, None)
        if not templates:
            return ""
        
        lang_templates = templates.get(lang, templates.get("en", []))
        
        if isinstance(lang_templates, list):
            template = random.choice(lang_templates)
        elif isinstance(lang_templates, dict):
            # For nested dicts like EVENT_CONFIRMED
            event_type = kwargs.get("event_type", "default")
            template = lang_templates.get(event_type, lang_templates.get("default", ""))
        else:
            template = lang_templates
        
        try:
            return template.format(**kwargs)
        except KeyError:
            return template
