"""
Multi-language support module with human-like response variations.
Supports English and Tamil with contextual, natural responses.
"""

import random
from typing import Dict, List, Optional, Any
from .config import settings


class LanguageManager:
    """
    Manages multi-language responses with human-like variations.
    Provides contextual, natural-sounding replies.
    """
    
    # Response templates with multiple variations for natural conversation
    RESPONSES: Dict[str, Dict[str, List[str]]] = {
        "en": {
            # Greetings
            "greet": [
                "👋 Hello! Welcome to *{restaurant}*!\n\nI'm your personal dining assistant. How can I make your day special?\n\n1️⃣ Book a Table\n2️⃣ Plan an Event\n3️⃣ Browse Our Menu\n\n_Type 'tamil' to switch to தமிழ் 🇮🇳_",
                "👋 Hi there! I'm the virtual concierge at *{restaurant}*.\n\nReady to create a memorable dining experience for you!\n\n1️⃣ Reserve a Table\n2️⃣ Event Booking\n3️⃣ View Menu Packs\n\n_Want Tamil? Just type 'tamil' 🇮🇳_",
                "👋 Welcome to *{restaurant}*! So glad you're here!\n\nI'm here to help you with:\n\n1️⃣ Table Reservations\n2️⃣ Special Event Bookings\n3️⃣ Menu Information\n\n_Type 'tamil' for தமிழ் 🇮🇳_"
            ],
            
            # Name collection
            "ask_name": [
                "Wonderful! Let's get started! 📝\n\nMay I know your good name?",
                "Perfect choice! 🌟\n\nFirst things first – what name should I use for the reservation?",
                "Excellent! Let's make this happen! ✨\n\nWhat's your name, please?",
                "Great! I'm excited to help you! 😊\n\nCould you share your name with me?"
            ],
            
            "name_confirm": [
                "Nice to meet you, *{name}*! 😊",
                "Lovely name, *{name}*! Let's continue.",
                "Thanks, *{name}*! Great to have you here!",
                "Welcome aboard, *{name}*! 🙌"
            ],
            
            # Party size
            "ask_people": [
                "How many guests will be joining the celebration? 👥",
                "How many people should I book for?",
                "Tell me the party size – how many guests in total?",
                "How many seats do you need? 🪑"
            ],
            
            "people_confirm": [
                "Got it! *{count} people* – that's going to be fun! 🎉",
                "Perfect! Noted *{count} guests*.",
                "Awesome! *{count} people* it is!",
                "*{count} guests* – wonderful! Let me find the best arrangement."
            ],
            
            "people_invalid": [
                "Hmm, I need a valid number of guests. Could you enter a number between {min} and {max}?",
                "Oops! Please enter a number between {min} and {max} for the guest count.",
                "I didn't quite catch that. How many people? (Enter a number from {min} to {max})"
            ],
            
            # Date collection
            "ask_date": [
                "When would you like to visit us? 📅\n\n_Please enter the date in DD-MM-YYYY format_",
                "What date works best for you?\n\n_Format: DD-MM-YYYY (e.g., 25-12-2025)_",
                "Pick your perfect day! 🗓️\n\n_Enter date as DD-MM-YYYY_",
                "Which date should I reserve for you?\n\n_Example: 15-02-2026_"
            ],
            
            "date_confirm": [
                "Excellent! *{date}* is marked! 📌",
                "Perfect! I've noted *{date}*.",
                "*{date}* – consider it done! ✅",
                "Great choice! *{date}* is locked in."
            ],
            
            "date_invalid": [
                "That date doesn't look right. Please use DD-MM-YYYY format (e.g., 25-12-2025).",
                "I couldn't parse that date. Try again with DD-MM-YYYY format.",
                "Hmm, invalid date format. Please enter like this: 25-02-2026"
            ],
            
            "date_past": [
                "Oops! That date has already passed. Please choose a future date.",
                "Time travel isn't available yet! 😄 Please pick a date in the future.",
                "That's in the past! Let's pick an upcoming date."
            ],
            
            # Time collection
            "ask_time": [
                "What time would you like your reservation? ⏰\n\n_We're open {opening}:00 to {closing}:00_",
                "Choose your preferred time slot:\n\n_Business hours: {opening} AM - {closing} PM_",
                "When should we expect you? ⏰\n\n_Just type the time, like '7 PM' or '19:00'_",
                "What time works for you?\n\n_Example: 7:30 PM or 19:30_"
            ],
            
            "time_confirm": [
                "Perfect! See you at *{time}*! ⏰",
                "*{time}* – noted! Getting exciting!",
                "Awesome! Reserved for *{time}*.",
                "*{time}* it is! Can't wait to serve you!"
            ],
            
            "time_invalid": [
                "Sorry, we're open from {opening}:00 to {closing}:00. Please choose a time within these hours.",
                "That time is outside our business hours ({opening}:00 - {closing}:00). Please pick another.",
                "We operate between {opening}:00 and {closing}:00. What time works within those hours?"
            ],
            
            # Event type
            "ask_event": [
                "What's the occasion? 🎊\n\n• Birthday 🎂\n• Anniversary 💑\n• Engagement 💍\n• Corporate Event 👔\n• Family Dinner 👨‍👩‍👧‍👦\n• Friends Gathering 🎉\n• Other\n\n_Just type the event name_",
                "Tell me about the celebration! What type of event is this?\n\n🎂 Birthday\n💍 Engagement\n👔 Corporate\n🍽️ Family Dinner\n🎉 Party\n\n_Or describe your event_",
                "What special occasion brings you to us? 🌟\n\nCommon events:\n• Birthday Party\n• Engagement Ceremony\n• Business Meeting\n• Anniversary Celebration\n• Casual Get-together"
            ],
            
            "event_confirm": [
                "Oh, a *{event}*! How exciting! 🎉",
                "Wonderful! *{event}* – we'll make it special! ✨",
                "*{event}* – one of our favorites to host! 🌟",
                "Perfect! We love hosting *{event}* celebrations!"
            ],
            
            "event_recommendation": [
                "💡 *Pro Tip for {event}:*\n{recommendation}",
                "✨ *Our suggestion for {event}:*\n{recommendation}",
                "🌟 *Expert recommendation:*\n{recommendation}"
            ],
            
            # Menu selection
            "ask_menu": [
                "Now for the delicious part! 🍽️\n\nChoose your menu pack:\n\n{menu_list}\n\n_Reply with the pack name (veg/nonveg/premium/deluxe)_",
                "Let's talk food! 😋\n\nOur menu packs:\n\n{menu_list}\n\n_Type your choice: veg, nonveg, premium, or deluxe_",
                "Time to select your feast! 🍛\n\n{menu_list}\n\n_Which one catches your eye?_"
            ],
            
            "menu_confirm": [
                "Excellent choice! *{pack}* is absolutely delicious! 😋",
                "*{pack}* – you've got great taste! 👨‍🍳",
                "Perfect! The *{pack}* never disappoints! 🌟",
                "*{pack}* selected! Your guests are in for a treat!"
            ],
            
            "menu_invalid": [
                "I don't recognize that menu pack. Please choose from: veg, nonveg, premium, or deluxe.",
                "Hmm, that's not on our menu list. Try: veg / nonveg / premium / deluxe",
                "Let me help – please type one of these: veg, nonveg, premium, deluxe"
            ],
            
            # Addons
            "ask_addons": [
                "Want to make it extra special? ✨\n\nAvailable add-ons:\n{addon_list}\n\n_Type what you'd like (comma-separated) or 'none' to skip_",
                "Optional extras to enhance your experience:\n\n{addon_list}\n\n_Choose any combination or type 'none'_",
                "Make your event unforgettable! 🌟\n\n{addon_list}\n\n_Example: decoration, cake, photography\nor type 'none' if you're all set_"
            ],
            
            "addons_confirm": [
                "Great additions! Added: *{addons}* ✨",
                "Perfect choices! *{addons}* will make it memorable!",
                "Noted! *{addons}* – excellent picks! 🎉",
                "*{addons}* – your event is going to be amazing!"
            ],
            
            "addons_none": [
                "No problem! The standard package is wonderful too! 👍",
                "That's perfectly fine! Let's proceed without extras.",
                "All good! Moving forward without add-ons.",
                "Sure! Sometimes less is more! 😊"
            ],
            
            "addons_invalid": [
                "I didn't recognize some of those add-ons. Available options:\n{addon_list}\n\n_Or type 'none' to skip_"
            ],
            
            # Confirmation
            "show_summary": [
                "📋 *Booking Summary*\n━━━━━━━━━━━━━━━━\n👤 Name: {name}\n👥 Guests: {people}\n📅 Date: {date}\n⏰ Time: {time}\n🎉 Event: {event}\n🍽️ Menu: {menu}\n✨ Add-ons: {addons}\n💰 Total: ₹{total}\n━━━━━━━━━━━━━━━━\n\nShall I confirm this reservation?\n\n_Reply *yes* to confirm or *no* to cancel_"
            ],
            
            "ask_confirm": [
                "Does everything look good? Should I lock this in? 🔐\n\n_Reply: yes / no_",
                "Ready to confirm? 🎯\n\n_Type 'yes' to book or 'no' to cancel_",
                "All set to finalize your reservation?\n\n_yes = confirm | no = cancel_"
            ],
            
            # Success
            "confirmed": [
                "🎉 *RESERVATION CONFIRMED!*\n━━━━━━━━━━━━━━━━━━━━━\n\n📋 Reservation ID: *{reservation_id}*\n\n{details}\n\n🪑 *Table Arrangement:*\n{layout}\n\n💡 *Our Recommendation:*\n{recommendation}\n\n━━━━━━━━━━━━━━━━━━━━━\n\nWe can't wait to serve you at *{restaurant}*!\n\n📞 For any changes: {phone}\n📧 Email: {email}\n\n_Type 'hi' anytime to make another reservation!_ ❤️",
            ],
            
            # Cancel
            "cancelled": [
                "No worries! Your booking has been cancelled. 😊\n\nFeel free to come back anytime – we're always here to help!\n\n_Type 'hi' to start a new reservation._",
                "Booking cancelled! No problem at all.\n\nWhenever you're ready, just say 'hi' and we'll start fresh! 👋",
                "Cancelled! I hope to see you soon.\n\nReady to try again? Just type 'hi'! 🙌"
            ],
            
            # Errors and fallbacks
            "invalid_input": [
                "I didn't quite catch that. Could you try again?",
                "Hmm, I'm not sure I understood. Can you rephrase?",
                "Sorry, I didn't get that. Let me help – {hint}",
                "Oops! That doesn't seem right. {hint}"
            ],
            
            "error": [
                "Something went wrong on my end. Let me try again...",
                "Oops! A small hiccup. Please try again.",
                "Sorry about that! Could you repeat your last message?"
            ],
            
            # Session/Reset
            "session_expired": [
                "⏰ Your session has timed out due to inactivity.\n\nNo worries! Just type 'hi' to start fresh. 🔄",
                "It's been a while! Your session expired.\n\nType 'hi' to begin a new reservation! 👋"
            ],
            
            "restart": [
                "🔄 Starting fresh! Previous conversation cleared.\n\nType 'hi' when you're ready to begin!",
                "Session reset! Let's start over.\n\nSay 'hi' to kick off a new reservation! 🚀"
            ],
            
            # Language switch
            "switch_tamil": [
                "🇮🇳 மொழி தமிழுக்கு மாற்றப்பட்டது!\n\nType 'english' to switch back."
            ],
            
            "switch_english": [
                "🇬🇧 Language switched to English!\n\nType 'tamil' to switch to தமிழ்."
            ],
            
            # Help
            "help": [
                "🆘 *Need Help?*\n\nHere's what I can do:\n• 'hi' or 'hello' - Start new booking\n• 'restart' - Clear & start over\n• 'cancel' - Cancel current booking\n• 'menu' - View our menu packs\n• 'tamil' - Switch to Tamil\n• 'help' - Show this message\n\nJust follow my questions to make a reservation! 📝"
            ],
            
            # Menu display
            "menu_display": [
                "🍽️ *Our Menu Packs*\n━━━━━━━━━━━━━━━━\n{menu_details}\n\n_Type 'hi' to start a reservation!_"
            ],
            
            # Purpose selection
            "select_purpose_invalid": [
                "Please choose an option:\n\n1️⃣ Book a Table\n2️⃣ Plan an Event\n3️⃣ Browse Menu\n\n_Just type 1, 2, or 3_"
            ]
        },
        
        "ta": {
            # Greetings
            "greet": [
                "👋 வணக்கம்! *{restaurant}* உங்களை வரவேற்கிறது!\n\nநான் உங்கள் உணவக உதவியாளர். எப்படி உதவ வேண்டும்?\n\n1️⃣ மேசை முன்பதிவு\n2️⃣ நிகழ்ச்சி திட்டம்\n3️⃣ மெனு பார்க்க\n\n_'english' என்று type செய்து ஆங்கிலத்திற்கு மாற்றலாம் 🇬🇧_",
                "👋 நல்வரவு! *{restaurant}* க்கு வந்ததற்கு நன்றி!\n\nநான் உங்களுக்கு உதவ தயார்:\n\n1️⃣ டேபிள் பதிவு\n2️⃣ விழா பதிவு\n3️⃣ மெனு பட்டியல்\n\n_English: 'english' என்று type செய்யவும் 🇬🇧_"
            ],
            
            # Name
            "ask_name": [
                "அருமை! 📝 முதலில் உங்கள் பெயரை சொல்லுங்கள்?",
                "நல்லது! ✨ உங்கள் பெயர் என்ன?",
                "சரி! 😊 பதிவுக்கு உங்கள் பெயர் தேவை?"
            ],
            
            "name_confirm": [
                "நன்றி, *{name}*! 😊 தொடரலாம்.",
                "அழகான பெயர், *{name}*!",
                "வரவேற்கிறேன், *{name}*! 🙌"
            ],
            
            # People
            "ask_people": [
                "எத்தனை பேர் வருவார்கள்? 👥",
                "மொத்தம் எத்தனை விருந்தினர்கள்?",
                "எத்தனை இடங்கள் தேவை? 🪑"
            ],
            
            "people_confirm": [
                "சரி! *{count} பேர்* – குறித்துக்கொண்டேன்! 🎉",
                "நல்லது! *{count} விருந்தினர்கள்*.",
                "*{count} பேர்* – அருமை!"
            ],
            
            "people_invalid": [
                "தயவுசெய்து {min} முதல் {max} வரை எண்ணை உள்ளிடவும்.",
                "சரியான எண் தேவை. {min}-{max} இடையே உள்ளிடவும்."
            ],
            
            # Date
            "ask_date": [
                "எந்த தேதியில் வர விரும்புகிறீர்கள்? 📅\n\n_DD-MM-YYYY வடிவத்தில் எழுதுங்கள்_",
                "தேதியை தேர்வு செய்யுங்கள் 🗓️\n\n_உதா: 25-12-2025_"
            ],
            
            "date_confirm": [
                "சரி! *{date}* பதிவு செய்துள்ளேன்! 📌",
                "*{date}* – குறித்துக்கொண்டேன்! ✅"
            ],
            
            "date_invalid": [
                "தவறான தேதி வடிவம். DD-MM-YYYY என்று எழுதுங்கள் (உதா: 25-12-2025).",
                "புரியவில்லை. இப்படி எழுதுங்கள்: 25-02-2026"
            ],
            
            "date_past": [
                "அந்த தேதி கடந்துவிட்டது! எதிர்கால தேதியை தேர்வு செய்யுங்கள்.",
                "இது பழைய தேதி! வரும் தேதியை தேர்வு செய்யுங்கள்."
            ],
            
            # Time
            "ask_time": [
                "எந்த நேரத்தில் வர விரும்புகிறீர்கள்? ⏰\n\n_நாங்கள் {opening}:00 - {closing}:00 வரை திறந்திருக்கிறோம்_",
                "நேரத்தை தேர்வு செய்யுங்கள்:\n\n_உதா: 7 PM அல்லது 19:00_"
            ],
            
            "time_confirm": [
                "நல்லது! *{time}* க்கு சந்திப்போம்! ⏰",
                "*{time}* – பதிவு செய்துள்ளேன்!"
            ],
            
            "time_invalid": [
                "மன்னிக்கவும், நாங்கள் {opening}:00 - {closing}:00 வரை மட்டுமே திறந்திருக்கிறோம்.",
                "இந்த நேரம் வேலை நேரத்திற்கு வெளியே. {opening}:00 - {closing}:00 தேர்வு செய்யுங்கள்."
            ],
            
            # Event
            "ask_event": [
                "என்ன நிகழ்ச்சி? 🎊\n\n• பிறந்தநாள் 🎂\n• திருமண நாள் 💑\n• திருமண நிச்சயம் 💍\n• அலுவலக விழா 👔\n• குடும்ப விருந்து 👨‍👩‍👧‍👦\n• நண்பர்கள் கூட்டம் 🎉\n\n_நிகழ்ச்சி பெயரை எழுதுங்கள்_",
                "எந்த சிறப்பு நிகழ்ச்சி? 🌟\n\n🎂 பிறந்தநாள்\n💍 நிச்சயம்\n👔 கார்ப்பரேட்\n🍽️ குடும்ப விருந்து"
            ],
            
            "event_confirm": [
                "*{event}* – அருமை! 🎉 சிறப்பாக செய்வோம்!",
                "நல்லது! *{event}* – ஒரு மறக்கமுடியாத நிகழ்வாக செய்வோம்! ✨"
            ],
            
            "event_recommendation": [
                "💡 *{event} க்கு எங்கள் பரிந்துரை:*\n{recommendation}"
            ],
            
            # Menu
            "ask_menu": [
                "உணவு தேர்வு செய்யலாம்! 🍽️\n\n{menu_list}\n\n_veg/nonveg/premium/deluxe என்று type செய்யுங்கள்_",
                "மெனு பேக் தேர்வு செய்யுங்கள்: 😋\n\n{menu_list}\n\n_உங்கள் தேர்வு?_"
            ],
            
            "menu_confirm": [
                "சிறந்த தேர்வு! *{pack}* மிகவும் சுவையானது! 😋",
                "*{pack}* – அருமையான தேர்வு! 👨‍🍳"
            ],
            
            "menu_invalid": [
                "இந்த மெனு இல்லை. இவற்றில் தேர்வு செய்யுங்கள்: veg, nonveg, premium, deluxe"
            ],
            
            # Addons
            "ask_addons": [
                "கூடுதல் சேவைகள் வேண்டுமா? ✨\n\n{addon_list}\n\n_கமாவால் பிரித்து எழுதுங்கள் அல்லது 'none' என்று type செய்யுங்கள்_"
            ],
            
            "addons_confirm": [
                "நல்லது! *{addons}* சேர்க்கப்பட்டது! ✨",
                "*{addons}* – சிறந்த தேர்வுகள்! 🎉"
            ],
            
            "addons_none": [
                "பரவாயில்லை! அடிப்படை பேக்கேஜ் கூட அருமை! 👍",
                "சரி! கூடுதல் சேவைகள் இல்லாமல் தொடரலாம்."
            ],
            
            # Confirmation
            "show_summary": [
                "📋 *பதிவு விவரம்*\n━━━━━━━━━━━━━━━━\n👤 பெயர்: {name}\n👥 விருந்தினர்: {people}\n📅 தேதி: {date}\n⏰ நேரம்: {time}\n🎉 நிகழ்ச்சி: {event}\n🍽️ மெனு: {menu}\n✨ கூடுதல்: {addons}\n💰 மொத்தம்: ₹{total}\n━━━━━━━━━━━━━━━━\n\nபதிவு செய்யலாமா?\n\n_'yes' = உறுதி | 'no' = ரத்து_"
            ],
            
            # Success
            "confirmed": [
                "🎉 *பதிவு வெற்றி!*\n━━━━━━━━━━━━━━━━━━━━━\n\n📋 பதிவு எண்: *{reservation_id}*\n\n{details}\n\n🪑 *மேசை அமைப்பு:*\n{layout}\n\n💡 *பரிந்துரை:*\n{recommendation}\n\n━━━━━━━━━━━━━━━━━━━━━\n\n*{restaurant}* இல் சந்திப்போம்!\n\n📞 தொடர்புக்கு: {phone}\n📧 மின்னஞ்சல்: {email}\n\n_மீண்டும் பதிவு செய்ய 'hi' என்று type செய்யுங்கள்!_ ❤️"
            ],
            
            # Cancel
            "cancelled": [
                "பரவாயில்லை! பதிவு ரத்து செய்யப்பட்டது. 😊\n\nபுதிய பதிவுக்கு 'hi' என்று type செய்யுங்கள்!",
                "ரத்து செய்யப்பட்டது! விரைவில் சந்திப்போம்.\n\nமீண்டும் தொடங்க 'hi' type செய்யுங்கள்! 👋"
            ],
            
            # Errors
            "invalid_input": [
                "புரியவில்லை. மீண்டும் முயற்சிக்கவும்.",
                "தவறான உள்ளீடு. {hint}"
            ],
            
            "error": [
                "ஏதோ தவறு நடந்தது. மீண்டும் முயற்சிக்கவும்.",
                "மன்னிக்கவும்! திரும்ப முயற்சிக்கவும்."
            ],
            
            # Session
            "session_expired": [
                "⏰ செயலற்ற நிலையால் அமர்வு முடிந்தது.\n\nபுதிதாக தொடங்க 'hi' type செய்யுங்கள்! 🔄"
            ],
            
            "restart": [
                "🔄 புதிய அமர்வு தொடங்கப்பட்டது!\n\n'hi' type செய்து ஆரம்பிக்கவும்!"
            ],
            
            # Language
            "switch_english": [
                "🇬🇧 மொழி ஆங்கிலத்திற்கு மாற்றப்பட்டது!\n\nதமிழுக்கு 'tamil' type செய்யுங்கள்."
            ],
            
            "switch_tamil": [
                "🇮🇳 மொழி தமிழில் உள்ளது!\n\n'english' type செய்து ஆங்கிலத்திற்கு மாற்றலாம்."
            ],
            
            # Help
            "help": [
                "🆘 *உதவி*\n\n• 'hi' - புதிய பதிவு\n• 'restart' - மீண்டும் தொடங்கு\n• 'cancel' - பதிவை ரத்து செய்\n• 'menu' - மெனு பார்க்க\n• 'english' - ஆங்கிலத்திற்கு மாற்று\n• 'help' - இந்த செய்தி"
            ],
            
            # Menu display
            "menu_display": [
                "🍽️ *எங்கள் மெனு பேக்கேஜ்கள்*\n━━━━━━━━━━━━━━━━\n{menu_details}\n\n_பதிவுக்கு 'hi' type செய்யுங்கள்!_"
            ],
            
            "select_purpose_invalid": [
                "தயவுசெய்து தேர்வு செய்யுங்கள்:\n\n1️⃣ மேசை பதிவு\n2️⃣ நிகழ்ச்சி திட்டம்\n3️⃣ மெனு பார்க்க\n\n_1, 2, அல்லது 3 type செய்யுங்கள்_"
            ]
        }
    }
    
    @classmethod
    def get(cls, key: str, language: str = "en", **kwargs) -> str:
        """
        Get a random response variation for the given key and language.
        
        Args:
            key: Response key (e.g., 'greet', 'ask_name')
            language: Language code ('en' or 'ta')
            **kwargs: Format parameters for the response
            
        Returns:
            Formatted response string
        """
        lang_responses = cls.RESPONSES.get(language, cls.RESPONSES["en"])
        responses = lang_responses.get(key, cls.RESPONSES["en"].get(key, ["Error: Response not found"]))
        
        # Select random variation
        response = random.choice(responses)
        
        # Add default restaurant info
        kwargs.setdefault("restaurant", settings.RESTAURANT_NAME)
        kwargs.setdefault("phone", settings.RESTAURANT_PHONE)
        kwargs.setdefault("email", settings.RESTAURANT_EMAIL)
        kwargs.setdefault("opening", settings.OPENING_HOUR)
        kwargs.setdefault("closing", settings.CLOSING_HOUR)
        kwargs.setdefault("min", settings.MIN_PARTY_SIZE)
        kwargs.setdefault("max", settings.MAX_PARTY_SIZE)
        
        # Format with provided kwargs
        try:
            return response.format(**kwargs)
        except KeyError as e:
            # Return unformatted if missing keys
            return response
    
    @classmethod
    def get_all_variations(cls, key: str, language: str = "en") -> List[str]:
        """Get all variations for a response key."""
        lang_responses = cls.RESPONSES.get(language, cls.RESPONSES["en"])
        return lang_responses.get(key, cls.RESPONSES["en"].get(key, []))
    
    @classmethod
    def detect_language_switch(cls, message: str) -> Optional[str]:
        """
        Detect if user wants to switch language.
        
        Returns:
            'en' for English, 'ta' for Tamil, None if no switch requested
        """
        msg_lower = message.lower().strip()
        
        # Use exact word matching to avoid false positives (e.g., "restart" containing "ta")
        tamil_triggers_exact = ['tamil', 'தமிழ்', 'tamizh']
        tamil_triggers_abbrev = ['ta']  # Only match if it's the entire message
        english_triggers_exact = ['english', 'ஆங்கிலம்']
        english_triggers_abbrev = ['eng', 'en']  # Only match if it's the entire message
        
        # Check exact matches for full words
        words = msg_lower.split()
        
        if any(trigger in words for trigger in tamil_triggers_exact):
            return "ta"
        if any(trigger in words for trigger in english_triggers_exact):
            return "en"
        
        # Check abbreviations only if they are the entire message
        if msg_lower in tamil_triggers_abbrev:
            return "ta"
        if msg_lower in english_triggers_abbrev:
            return "en"
        
        return None
    
    @classmethod
    def is_greeting(cls, message: str) -> bool:
        """Check if message is a greeting."""
        greetings = [
            'hi', 'hello', 'hey', 'hola', 'start', 'begin',
            'வணக்கம்', 'ஹாய்', 'ஹலோ', 'நமஸ்காரம்'
        ]
        msg_lower = message.lower().strip()
        return any(msg_lower.startswith(g) or msg_lower == g for g in greetings)
    
    
    @classmethod
    def is_restart(cls, message: str) -> bool:
        """Check if user wants to restart."""
        restart_triggers = ['restart', 'reset', 'start over', 'new', 'fresh', 'மீண்டும்']
        msg_lower = message.lower().strip()
        return any(trigger in msg_lower for trigger in restart_triggers)
    
    @classmethod
    def is_cancel(cls, message: str) -> bool:
        """Check if user wants to cancel."""
        cancel_triggers = ['cancel', 'stop', 'quit', 'exit', 'no more', 'ரத்து']
        msg_lower = message.lower().strip()
        return any(trigger in msg_lower for trigger in cancel_triggers)
    
    @classmethod
    def is_help(cls, message: str) -> bool:
        """Check if user needs help."""
        help_triggers = ['help', 'support', '?', 'how', 'உதவி']
        msg_lower = message.lower().strip()
        return any(trigger in msg_lower for trigger in help_triggers)
    
    @classmethod
    def is_menu_request(cls, message: str) -> bool:
        """Check if user wants to see menu."""
        menu_triggers = ['menu', 'food', 'packages', 'packs', 'மெனு', 'உணவு']
        msg_lower = message.lower().strip()
        return any(trigger in msg_lower for trigger in menu_triggers)
    
    @classmethod
    def is_affirmative(cls, message: str) -> bool:
        """Check if response is affirmative."""
        yes_triggers = ['yes', 'yeah', 'yep', 'sure', 'ok', 'okay', 'confirm', 'ஆம்', 'சரி']
        msg_lower = message.lower().strip()
        return any(trigger in msg_lower for trigger in yes_triggers)
    
    @classmethod
    def is_negative(cls, message: str) -> bool:
        """Check if response is negative."""
        no_triggers = ['no', 'nope', 'nah', 'cancel', 'stop', 'இல்லை', 'வேண்டாம்']
        msg_lower = message.lower().strip()
        return any(trigger in msg_lower for trigger in no_triggers)


# Legacy support - keeping old LANG dict for backwards compatibility
LANG = {
    "en": {
        "greet": LanguageManager.RESPONSES["en"]["greet"][0],
        "ask_name": LanguageManager.RESPONSES["en"]["ask_name"][0],
        "ask_people": LanguageManager.RESPONSES["en"]["ask_people"][0],
        "ask_date": LanguageManager.RESPONSES["en"]["ask_date"][0],
        "ask_time": LanguageManager.RESPONSES["en"]["ask_time"][0],
        "ask_event": LanguageManager.RESPONSES["en"]["ask_event"][0],
        "ask_menu": "Choose your menu pack:\nReply: veg / nonveg / premium / deluxe",
        "ask_addons": "Choose addons or type 'none'",
        "confirm": "Shall I confirm your booking? Reply: yes / no",
        "cancel": "No problem! Booking cancelled. 😊",
        "confirmed": "🎉 Reservation Confirmed! Details below:\n",
        "switch_tamil": "Language switched to Tamil 🇮🇳",
        "switch_english": "Language switched to English 🇬🇧",
        "invalid": "Sorry, I didn't understand that.",
    },
    "ta": {
        "greet": LanguageManager.RESPONSES["ta"]["greet"][0],
        "ask_name": LanguageManager.RESPONSES["ta"]["ask_name"][0],
        "ask_people": LanguageManager.RESPONSES["ta"]["ask_people"][0],
        "ask_date": LanguageManager.RESPONSES["ta"]["ask_date"][0],
        "ask_time": LanguageManager.RESPONSES["ta"]["ask_time"][0],
        "ask_event": LanguageManager.RESPONSES["ta"]["ask_event"][0],
        "ask_menu": "மெனு பேக் தேர்வு செய்யவும்: veg / nonveg / premium / deluxe",
        "ask_addons": "கூடுதல் சேவைகள் தேர்வு செய்யவும் அல்லது 'none'",
        "confirm": "பதிவு செய்யலாமா? yes / no",
        "cancel": "பரவாயில்லை! பதிவு ரத்து செய்யப்பட்டது 😊",
        "confirmed": "🎉 உங்கள் பதிவு வெற்றிகரமாக செய்யப்பட்டது! விவரங்கள்:\n",
        "switch_tamil": "மொழி தமிழுக்கு மாற்றப்பட்டது 🇮🇳",
        "switch_english": "மொழி ஆங்கிலத்திற்கு மாற்றப்பட்டது 🇬🇧",
        "invalid": "மன்னிக்கவும், புரியவில்லை.",
    }
}
