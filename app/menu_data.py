"""
Menu data configuration for the Restaurant Bot.
Contains menu packs, addons, and event recommendations.
"""

from typing import Dict, List, Any, Optional


# Menu Pack Definitions
MENU_PACKS: Dict[str, Dict[str, Any]] = {
    "veg": {
        "key": "veg",
        "title": "Pure Veg Delight",
        "title_ta": "சைவ விருந்து",
        "price_per_person": 399,
        "description": "A delightful vegetarian feast with aromatic dishes",
        "description_ta": "நறுமணமான சைவ விருந்து",
        "items": [
            "Paneer Tikka",
            "Veg Biryani",
            "Gobi 65 / Mushroom Fry",
            "Roti with Paneer Butter Masala",
            "Dal Makhani",
            "Raita & Papad",
            "Gulab Jamun (2 pcs)",
            "Welcome Drink"
        ],
        "items_ta": [
            "பன்னீர் டிக்கா",
            "காய்கறி பிரியாணி",
            "காளிபிளவர் 65",
            "ரொட்டி + பன்னீர் பட்டர் மசாலா",
            "தால் மக்கனி",
            "ரைத்தா & பப்பட்",
            "குலாப் ஜாமூன்",
            "வரவேற்பு பானம்"
        ],
        "min_people": 2,
        "is_available": True,
        "dietary_info": "100% Vegetarian, Contains Dairy"
    },
    
    "nonveg": {
        "key": "nonveg",
        "title": "Non-Veg Classic",
        "title_ta": "அசைவ கிளாசிக்",
        "price_per_person": 499,
        "description": "Classic non-vegetarian favorites for meat lovers",
        "description_ta": "அசைவ பிரியர்களுக்கான கிளாசிக் விருந்து",
        "items": [
            "Chicken 65 / Fish Fry",
            "Chicken Biryani",
            "Grilled Tandoori Chicken",
            "Roti with Chicken Curry",
            "Egg Curry / Pepper Chicken",
            "Raita & Papad",
            "Ice Cream (2 scoops)",
            "Welcome Drink"
        ],
        "items_ta": [
            "சிக்கன் 65 / மீன் வறுவல்",
            "சிக்கன் பிரியாணி",
            "தந்தூரி சிக்கன்",
            "ரொட்டி + சிக்கன் கறி",
            "முட்டை கறி / மிளகு சிக்கன்",
            "ரைத்தா & பப்பட்",
            "ஐஸ்கிரீம்",
            "வரவேற்பு பானம்"
        ],
        "min_people": 2,
        "is_available": True,
        "dietary_info": "Contains Chicken, Fish, Eggs"
    },
    
    "premium": {
        "key": "premium",
        "title": "Premium Royal Feast",
        "title_ta": "பிரீமியம் ராயல் விருந்து",
        "price_per_person": 749,
        "description": "Premium selection with exotic dishes and superior ingredients",
        "description_ta": "சிறந்த பொருட்களுடன் கூடிய பிரீமியம் விருந்து",
        "items": [
            "Mutton Seekh Kebab",
            "Prawns 65 / Crab Masala",
            "Mutton Biryani (Hyderabadi Style)",
            "Tandoori Platter (Chicken, Fish, Paneer)",
            "Butter Naan with Mutton Rogan Josh",
            "Fish Moilee / Prawn Curry",
            "Assorted Raita & Chutneys",
            "Dessert Platter (3 varieties)",
            "Mocktails (2 glasses)"
        ],
        "items_ta": [
            "மட்டன் சீக் கபாப்",
            "இறால் 65 / நண்டு மசாலா",
            "மட்டன் பிரியாணி",
            "தந்தூரி பிளேட்டர்",
            "நான் + மட்டன் ரோகன் ஜோஷ்",
            "மீன் மொய்லி / இறால் கறி",
            "வகைவகையான ரைத்தா",
            "இனிப்பு பிளேட்டர்",
            "மாக்டெய்ல்ஸ்"
        ],
        "min_people": 4,
        "is_available": True,
        "dietary_info": "Contains Mutton, Prawns, Fish, Chicken"
    },
    
    "deluxe": {
        "key": "deluxe",
        "title": "Grand Deluxe Experience",
        "title_ta": "கிராண்ட் டீலக்ஸ் அனுபவம்",
        "price_per_person": 999,
        "description": "The ultimate dining experience with live counters and chef specials",
        "description_ta": "லைவ் கவுண்டர்களுடன் கூடிய சிறந்த உணவு அனுபவம்",
        "items": [
            "Live Grill Counter (Unlimited)",
            "Lobster / Crab / Prawns Platter",
            "Chef's Special Biryani (Lucknowi)",
            "International Platter (Thai, Chinese, Continental)",
            "Live Pasta / Noodle Counter",
            "Premium Tandoor Selection",
            "Unlimited Soft Beverages",
            "Live Dessert Counter",
            "Espresso / Cappuccino",
            "Complimentary Cake (for events)"
        ],
        "items_ta": [
            "லைவ் கிரில் கவுண்டர்",
            "கடல் உணவு பிளேட்டர்",
            "செஃப் ஸ்பெஷல் பிரியாணி",
            "சர்வதேச பிளேட்டர்",
            "லைவ் பாஸ்தா கவுண்டர்",
            "பிரீமியம் தந்தூர்",
            "அன்லிமிடெட் பானங்கள்",
            "லைவ் இனிப்பு கவுண்டர்",
            "காபி",
            "இலவச கேக்"
        ],
        "min_people": 10,
        "is_available": True,
        "dietary_info": "Includes Veg & Non-Veg Options, Seafood"
    }
}


# Addon Definitions
ADDONS: Dict[str, Dict[str, Any]] = {
    "decoration": {
        "key": "decoration",
        "name": "Theme Decoration",
        "name_ta": "தீம் அலங்காரம்",
        "price": 2500,
        "description": "Beautiful theme-based decoration with balloons, banners, and centerpieces",
        "description_ta": "அழகான தீம் அலங்காரம்",
        "includes": ["Balloons", "Banners", "Table Centerpieces", "Photo Backdrop"],
        "is_available": True
    },
    
    "cake": {
        "key": "cake",
        "name": "Designer Cake",
        "name_ta": "டிசைனர் கேக்",
        "price": 1200,
        "description": "1 kg designer cake (Chocolate/Vanilla/Butterscotch)",
        "description_ta": "1 கிலோ டிசைனர் கேக்",
        "includes": ["1 kg Cake", "Cake Knife", "Candles", "Serving Plates"],
        "is_available": True
    },
    
    "photography": {
        "key": "photography",
        "name": "Professional Photography",
        "name_ta": "தொழில்முறை புகைப்படம்",
        "price": 3500,
        "description": "2-hour professional photography session with edited photos",
        "description_ta": "2 மணி நேர புகைப்பட அமர்வு",
        "includes": ["Professional Photographer", "2 Hours Coverage", "50+ Edited Photos", "Digital Delivery"],
        "is_available": True
    },
    
    "music_system": {
        "key": "music_system",
        "name": "Sound System",
        "name_ta": "ஒலி அமைப்பு",
        "price": 1500,
        "description": "Premium sound system with microphone",
        "description_ta": "மைக்குடன் கூடிய ஒலி அமைப்பு",
        "includes": ["Speakers", "Microphone", "Bluetooth Connectivity", "Background Music"],
        "is_available": True
    },
    
    "dj": {
        "key": "dj",
        "name": "DJ & Party Lights",
        "name_ta": "டிஜே & பார்ட்டி லைட்ஸ்",
        "price": 5000,
        "description": "Professional DJ with party lighting setup",
        "description_ta": "தொழில்முறை டிஜே மற்றும் பார்ட்டி விளக்குகள்",
        "includes": ["Professional DJ", "Dance Floor Lights", "Fog Machine", "3-Hour Session"],
        "is_available": True
    },
    
    "live_music": {
        "key": "live_music",
        "name": "Live Music Band",
        "name_ta": "லைவ் மியூசிக் பேண்ட்",
        "price": 8000,
        "description": "Live music band performance (2 hours)",
        "description_ta": "லைவ் இசைக்குழு நிகழ்ச்சி",
        "includes": ["4-piece Band", "2 Hours Performance", "Song Requests", "Background Music"],
        "is_available": True
    },
    
    "flowers": {
        "key": "flowers",
        "name": "Flower Arrangement",
        "name_ta": "மலர் அலங்காரம்",
        "price": 2000,
        "description": "Fresh flower arrangements and garlands",
        "description_ta": "புதிய மலர் அலங்காரம்",
        "includes": ["Table Flowers", "Stage Decoration", "Welcome Garlands", "Rose Petals"],
        "is_available": True
    },
    
    "balloons": {
        "key": "balloons",
        "name": "Balloon Decoration",
        "name_ta": "பலூன் அலங்காரம்",
        "price": 1800,
        "description": "Premium balloon arch and decoration",
        "description_ta": "பிரீமியம் பலூன் ஆர்ச்",
        "includes": ["Balloon Arch", "Helium Balloons", "Number/Letter Balloons", "Ceiling Balloons"],
        "is_available": True
    }
}


# Event-based Recommendations
EVENT_RECOMMENDATIONS: Dict[str, Dict[str, Any]] = {
    "birthday": {
        "event_type": "Birthday",
        "recommended_pack": "nonveg",
        "recommended_addons": ["decoration", "cake", "balloons"],
        "message_en": "🎂 For birthdays, we recommend the Non-Veg Classic pack with decoration, cake & balloons. Creates a festive atmosphere!",
        "message_ta": "🎂 பிறந்தநாளுக்கு அசைவ கிளாசிக் பேக் + அலங்காரம், கேக் & பலூன் பரிந்துரைக்கிறோம்!",
        "seating_style": "circular",
        "special_notes": "Complimentary birthday song by staff"
    },
    
    "engagement": {
        "event_type": "Engagement",
        "recommended_pack": "premium",
        "recommended_addons": ["decoration", "photography", "flowers"],
        "message_en": "💍 For engagements, the Premium Royal Feast with professional photography and flower decorations is perfect!",
        "message_ta": "💍 நிச்சயதார்த்தத்திற்கு பிரீமியம் ராயல் பேக் + புகைப்படம் & மலர் அலங்காரம் சிறந்தது!",
        "seating_style": "u_shape",
        "special_notes": "Ring ceremony setup included"
    },
    
    "anniversary": {
        "event_type": "Anniversary",
        "recommended_pack": "premium",
        "recommended_addons": ["decoration", "cake", "live_music"],
        "message_en": "💑 Celebrate your special day with Premium feast, romantic decoration, and live music!",
        "message_ta": "💑 உங்கள் திருமண நாளை பிரீமியம் விருந்து, ரொமாண்டிக் அலங்காரம் & லைவ் மியூசிக்குடன் கொண்டாடுங்கள்!",
        "seating_style": "intimate",
        "special_notes": "Candlelight dinner setup available"
    },
    
    "corporate": {
        "event_type": "Corporate Event",
        "recommended_pack": "nonveg",
        "recommended_addons": ["music_system"],
        "message_en": "👔 For corporate events, Non-Veg Classic with sound system for presentations works great!",
        "message_ta": "👔 கார்ப்பரேட் நிகழ்வுகளுக்கு அசைவ கிளாசிக் + ஒலி அமைப்பு சிறந்தது!",
        "seating_style": "conference",
        "special_notes": "Projector setup available on request"
    },
    
    "family dinner": {
        "event_type": "Family Dinner",
        "recommended_pack": "veg",
        "recommended_addons": [],
        "message_en": "🍽️ For family dinners, our Pure Veg Delight is a crowd-pleaser! Add decoration for extra charm.",
        "message_ta": "🍽️ குடும்ப விருந்துக்கு சைவ விருந்து எல்லோருக்கும் பிடிக்கும்!",
        "seating_style": "family",
        "special_notes": "Kids menu available"
    },
    
    "friends gathering": {
        "event_type": "Friends Gathering",
        "recommended_pack": "nonveg",
        "recommended_addons": ["dj", "balloons"],
        "message_en": "🎉 Party time! Non-Veg Classic with DJ and balloon decoration for maximum fun!",
        "message_ta": "🎉 பார்ட்டி நேரம்! அசைவ கிளாசிக் + டிஜே & பலூன் அலங்காரம்!",
        "seating_style": "casual",
        "special_notes": "Dance floor setup included"
    },
    
    "wedding reception": {
        "event_type": "Wedding Reception",
        "recommended_pack": "deluxe",
        "recommended_addons": ["decoration", "photography", "dj", "flowers"],
        "message_en": "💒 For wedding receptions, our Grand Deluxe Experience with full decoration and photography is ideal!",
        "message_ta": "💒 திருமண வரவேற்புக்கு கிராண்ட் டீலக்ஸ் + முழு அலங்காரம் & புகைப்படம் சிறந்தது!",
        "seating_style": "banquet",
        "special_notes": "Stage and backdrop setup included"
    },
    
    "baby shower": {
        "event_type": "Baby Shower",
        "recommended_pack": "veg",
        "recommended_addons": ["decoration", "cake", "photography", "balloons"],
        "message_en": "👶 Baby showers are special! Veg pack with cute decorations, cake, and photography!",
        "message_ta": "👶 பேபி ஷவர் சிறப்பானது! சைவ பேக் + அலங்காரம், கேக் & புகைப்படம்!",
        "seating_style": "circular",
        "special_notes": "Theme-based decoration available"
    },
    
    "farewell": {
        "event_type": "Farewell Party",
        "recommended_pack": "nonveg",
        "recommended_addons": ["decoration", "music_system"],
        "message_en": "👋 Make farewells memorable with Non-Veg Classic, decoration, and a speech setup!",
        "message_ta": "👋 பிரியா விடை நிகழ்வை மறக்கமுடியாததாக்குங்கள்!",
        "seating_style": "u_shape",
        "special_notes": "Memory wall setup available"
    },
    
    "default": {
        "event_type": "General Event",
        "recommended_pack": "nonveg",
        "recommended_addons": ["decoration"],
        "message_en": "🌟 For your event, we recommend the Non-Veg Classic pack. Add decoration for extra charm!",
        "message_ta": "🌟 உங்கள் நிகழ்வுக்கு அசைவ கிளாசிக் பேக் பரிந்துரை!",
        "seating_style": "standard",
        "special_notes": "Customization available"
    }
}


# Table Layout Configurations
TABLE_LAYOUTS: Dict[str, Dict[str, Any]] = {
    "circular": {
        "style": "Circular Seating",
        "style_ta": "வட்ட அமைப்பு",
        "description": "Round tables arranged in a circle, perfect for celebrations",
        "description_ta": "கொண்டாட்டங்களுக்கு ஏற்ற வட்ட மேசை அமைப்பு",
        "max_per_table": 8,
        "ideal_for": ["birthday", "baby shower"]
    },
    
    "u_shape": {
        "style": "U-Shape Arrangement",
        "style_ta": "U-வடிவ அமைப்பு",
        "description": "U-shaped table setup for speeches and presentations",
        "description_ta": "உரைகள் மற்றும் விளக்கக்காட்சிகளுக்கு U-வடிவ அமைப்பு",
        "max_per_table": 30,
        "ideal_for": ["engagement", "farewell"]
    },
    
    "conference": {
        "style": "Conference Style",
        "style_ta": "மாநாட்டு அமைப்பு",
        "description": "Long rectangular tables for business meetings",
        "description_ta": "வணிக சந்திப்புகளுக்கு நீண்ட செவ்வக மேசைகள்",
        "max_per_table": 20,
        "ideal_for": ["corporate"]
    },
    
    "banquet": {
        "style": "Banquet Style",
        "style_ta": "விருந்து அமைப்பு",
        "description": "Multiple round tables for large gatherings",
        "description_ta": "பெரிய கூட்டங்களுக்கு பல வட்ட மேசைகள்",
        "max_per_table": 10,
        "ideal_for": ["wedding reception"]
    },
    
    "casual": {
        "style": "Casual Lounge",
        "style_ta": "சாதாரண அமைப்பு",
        "description": "Mix of high tables and lounge seating",
        "description_ta": "உயர் மேசைகள் மற்றும் நாற்காலி கலவை",
        "max_per_table": 6,
        "ideal_for": ["friends gathering"]
    },
    
    "family": {
        "style": "Family Style",
        "style_ta": "குடும்ப அமைப்பு",
        "description": "Long communal tables for family-style dining",
        "description_ta": "குடும்ப உணவுக்கு நீண்ட பொது மேசைகள்",
        "max_per_table": 12,
        "ideal_for": ["family dinner"]
    },
    
    "intimate": {
        "style": "Intimate Setting",
        "style_ta": "நெருக்கமான அமைப்பு",
        "description": "Cozy setup with smaller tables",
        "description_ta": "சிறிய மேசைகளுடன் நெருக்கமான அமைப்பு",
        "max_per_table": 4,
        "ideal_for": ["anniversary"]
    },
    
    "standard": {
        "style": "Standard Seating",
        "style_ta": "நிலையான அமைப்பு",
        "description": "Versatile arrangement suitable for most events",
        "description_ta": "பெரும்பாலான நிகழ்வுகளுக்கு ஏற்ற அமைப்பு",
        "max_per_table": 6,
        "ideal_for": ["default"]
    }
}


def get_menu_pack(pack_key: str) -> Optional[Dict[str, Any]]:
    """Get menu pack by key."""
    return MENU_PACKS.get(pack_key.lower())


def get_addon(addon_key: str) -> Optional[Dict[str, Any]]:
    """Get addon by key."""
    return ADDONS.get(addon_key.lower())


def get_event_recommendation(event_type: str) -> Dict[str, Any]:
    """Get recommendation for event type."""
    event_lower = event_type.lower()
    
    # Find matching event
    for key, rec in EVENT_RECOMMENDATIONS.items():
        if key in event_lower or event_lower in key:
            return rec
    
    return EVENT_RECOMMENDATIONS["default"]


def get_table_layout(style: str) -> Dict[str, Any]:
    """Get table layout configuration."""
    return TABLE_LAYOUTS.get(style, TABLE_LAYOUTS["standard"])


def get_available_menu_keys() -> List[str]:
    """Get list of available menu pack keys."""
    return [k for k, v in MENU_PACKS.items() if v.get("is_available", True)]


def get_available_addon_keys() -> List[str]:
    """Get list of available addon keys."""
    return [k for k, v in ADDONS.items() if v.get("is_available", True)]


def calculate_menu_cost(pack_key: str, people: int) -> int:
    """Calculate menu cost for given pack and people count."""
    pack = get_menu_pack(pack_key)
    if not pack:
        return 0
    return pack["price_per_person"] * people


def calculate_addons_cost(addon_keys: List[str]) -> int:
    """Calculate total addons cost."""
    total = 0
    for key in addon_keys:
        addon = get_addon(key)
        if addon:
            total += addon["price"]
    return total


def format_menu_list(language: str = "en") -> str:
    """Format menu list for display."""
    lines = []
    for i, (key, pack) in enumerate(MENU_PACKS.items(), 1):
        if not pack.get("is_available", True):
            continue
        
        if language == "ta":
            title = pack["title_ta"]
            description = pack.get("description_ta", "")
        else:
            title = pack["title"]
            description = pack.get("description", "")
        
        emoji = "🥗" if "veg" in key.lower() and "non" not in key.lower() else "🍗"
        if key == "premium":
            emoji = "👑"
        elif key == "deluxe":
            emoji = "🌟"
        
        lines.append(f"{emoji} *{title}*")
        lines.append(f"   ₹{pack['price_per_person']}/person")
        if pack.get("min_people", 1) > 1:
            min_text = "Min guests" if language == "en" else "குறைந்தபட்சம்"
            lines.append(f"   _{min_text}: {pack['min_people']}_")
        lines.append("")
    
    return "\n".join(lines)


def format_addon_list(language: str = "en") -> str:
    """Format addon list for display."""
    lines = []
    for key, addon in ADDONS.items():
        if not addon.get("is_available", True):
            continue
        
        if language == "ta":
            name = addon["name_ta"]
        else:
            name = addon["name"]
        
        lines.append(f"• {name} – ₹{addon['price']}")
    
    return "\n".join(lines)
