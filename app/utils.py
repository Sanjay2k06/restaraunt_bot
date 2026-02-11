"""
Utility functions for the Restaurant Bot.
Provides formatting, validation, and helper functions.
"""

import re
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from .config import settings
from .menu_data import (
    MENU_PACKS, ADDONS, TABLE_LAYOUTS,
    format_menu_list, format_addon_list,
    get_event_recommendation, get_table_layout
)


def format_menu(language: str = "en") -> str:
    """
    Format menu packs for display.
    
    Args:
        language: 'en' for English, 'ta' for Tamil
        
    Returns:
        Formatted menu string
    """
    menu_list = format_menu_list(language)
    
    if language == "ta":
        header = "🍽️ *எங்கள் மெனு பேக்கேஜ்கள்*"
        footer = "_veg / nonveg / premium / deluxe என்று type செய்யுங்கள்_"
    else:
        header = "🍽️ *Our Menu Packs*"
        footer = "_Reply with: veg / nonveg / premium / deluxe_"
    
    return f"{header}\n━━━━━━━━━━━━━━━━\n{menu_list}\n{footer}"


def format_addons(language: str = "en") -> str:
    """
    Format addons for display.
    
    Args:
        language: 'en' for English, 'ta' for Tamil
        
    Returns:
        Formatted addons string
    """
    addon_list = format_addon_list(language)
    
    if language == "ta":
        header = "✨ *கூடுதல் சேவைகள்*"
        footer = "_கமாவால் பிரித்து எழுதுங்கள் அல்லது 'none'_"
    else:
        header = "✨ *Optional Add-ons*"
        footer = "_Type what you want (comma-separated) or 'none'_"
    
    return f"{header}\n━━━━━━━━━━━━━━━━\n{addon_list}\n\n{footer}"


def format_menu_details(pack_key: str, language: str = "en") -> str:
    """
    Format detailed menu pack information.
    
    Args:
        pack_key: Menu pack key
        language: Language code
        
    Returns:
        Formatted menu details
    """
    pack = MENU_PACKS.get(pack_key)
    if not pack:
        return "Menu pack not found"
    
    if language == "ta":
        title = pack.get("title_ta", pack["title"])
        items = pack.get("items_ta", pack["items"])
        items_header = "உள்ளடக்கம்:"
    else:
        title = pack["title"]
        items = pack["items"]
        items_header = "Includes:"
    
    items_str = "\n".join([f"  • {item}" for item in items])
    
    return f"*{title}*\n{items_header}\n{items_str}"


def table_layout(people: int, event_type: str = "default", language: str = "en") -> str:
    """
    Generate table layout recommendation.
    
    Args:
        people: Number of guests
        event_type: Type of event
        language: Language code
        
    Returns:
        Layout recommendation string
    """
    # Get event recommendation for seating style
    rec = get_event_recommendation(event_type)
    seating_style = rec.get("seating_style", "standard")
    layout_config = get_table_layout(seating_style)
    
    max_per_table = layout_config.get("max_per_table", 6)
    tables_needed = (people + max_per_table - 1) // max_per_table
    
    if language == "ta":
        style = layout_config.get("style_ta", layout_config["style"])
        desc = layout_config.get("description_ta", layout_config["description"])
    else:
        style = layout_config["style"]
        desc = layout_config["description"]
    
    # Build visual layout representation
    visual = generate_layout_visual(tables_needed, seating_style)
    
    if language == "ta":
        return (
            f"📐 *{style}*\n"
            f"{desc}\n\n"
            f"🪑 மேசைகள்: {tables_needed} ({max_per_table} இடங்கள் ஒவ்வொன்றிலும்)\n"
            f"👥 மொத்த கொள்ளளவு: {tables_needed * max_per_table} பேர்\n\n"
            f"{visual}"
        )
    else:
        return (
            f"📐 *{style}*\n"
            f"{desc}\n\n"
            f"🪑 Tables: {tables_needed} ({max_per_table} seats each)\n"
            f"👥 Total capacity: {tables_needed * max_per_table} guests\n\n"
            f"{visual}"
        )


def generate_layout_visual(tables: int, style: str) -> str:
    """
    Generate a simple text-based visual layout.
    
    Args:
        tables: Number of tables
        style: Seating style
        
    Returns:
        ASCII art representation of layout
    """
    if style == "circular" or style == "banquet":
        # Circular tables visual
        if tables <= 3:
            return "  ⭕  ⭕  ⭕  " if tables == 3 else "  ⭕  ⭕  " if tables == 2 else "    ⭕    "
        elif tables <= 6:
            row1 = "  " + "⭕  " * min(3, tables)
            row2 = "  " + "⭕  " * (tables - 3) if tables > 3 else ""
            return f"{row1}\n{row2}"
        else:
            rows = []
            remaining = tables
            per_row = 4
            while remaining > 0:
                count = min(per_row, remaining)
                rows.append("  " + "⭕  " * count)
                remaining -= count
            return "\n".join(rows)
    
    elif style == "u_shape":
        return (
            "  ┌─────────────────┐\n"
            "  │  🪑  🪑  🪑  🪑  │\n"
            "  │                 │\n"
            "  │  🪑          🪑  │\n"
            "  │                 │\n"
            "  └──🪑──🪑──🪑──🪑──┘"
        )
    
    elif style == "conference":
        return (
            "  ┌─────────────────────┐\n"
            "  │ 🪑🪑🪑🪑🪑🪑🪑🪑🪑🪑 │\n"
            "  │                     │\n"
            "  │ 🪑🪑🪑🪑🪑🪑🪑🪑🪑🪑 │\n"
            "  └─────────────────────┘"
        )
    
    elif style == "intimate":
        return "    ⭕🕯️⭕    \n   _romantic_"
    
    else:
        # Standard layout
        if tables <= 4:
            return "  " + "⬜  " * tables
        else:
            row1 = "  " + "⬜  " * 4
            row2 = "  " + "⬜  " * (tables - 4)
            return f"{row1}\n{row2}"


def validate_date(date_str: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate date string.
    
    Args:
        date_str: Date string in DD-MM-YYYY format
        
    Returns:
        Tuple of (is_valid, normalized_date, error_message)
    """
    # Try multiple date formats
    formats = ["%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y", "%Y-%m-%d"]
    
    parsed_date = None
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_str.strip(), fmt)
            break
        except ValueError:
            continue
    
    if not parsed_date:
        return False, None, "Invalid date format. Please use DD-MM-YYYY"
    
    # Check if date is in the future
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if parsed_date < today:
        return False, None, "Date must be in the future"
    
    # Check if date is not too far in the future
    max_date = today + timedelta(days=settings.ADVANCE_BOOKING_DAYS)
    if parsed_date > max_date:
        return False, None, f"Bookings can only be made up to {settings.ADVANCE_BOOKING_DAYS} days in advance"
    
    normalized = parsed_date.strftime("%d-%m-%Y")
    return True, normalized, None


def validate_time(time_str: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate time string.
    
    Args:
        time_str: Time string (e.g., "7 PM", "19:00", "7:30 pm")
        
    Returns:
        Tuple of (is_valid, normalized_time, error_message)
    """
    time_str = time_str.strip().upper()
    
    # Patterns to match various time formats
    patterns = [
        (r'^(\d{1,2}):(\d{2})\s*(AM|PM)$', 'h:mm AM/PM'),
        (r'^(\d{1,2})\s*(AM|PM)$', 'h AM/PM'),
        (r'^(\d{1,2}):(\d{2})$', '24-hour'),
        (r'^(\d{1,2})$', 'hour only')
    ]
    
    hour = None
    minute = 0
    
    for pattern, _ in patterns:
        match = re.match(pattern, time_str)
        if match:
            groups = match.groups()
            
            if len(groups) == 3:  # h:mm AM/PM
                hour = int(groups[0])
                minute = int(groups[1])
                if groups[2] == 'PM' and hour != 12:
                    hour += 12
                elif groups[2] == 'AM' and hour == 12:
                    hour = 0
                    
            elif len(groups) == 2:
                if groups[1] in ('AM', 'PM'):  # h AM/PM
                    hour = int(groups[0])
                    if groups[1] == 'PM' and hour != 12:
                        hour += 12
                    elif groups[1] == 'AM' and hour == 12:
                        hour = 0
                else:  # 24-hour format
                    hour = int(groups[0])
                    minute = int(groups[1])
                    
            else:  # hour only (assume PM if reasonable)
                hour = int(groups[0])
                if hour < 12 and hour >= 1:
                    hour += 12  # Assume PM for restaurant hours
            
            break
    
    if hour is None:
        return False, None, "Invalid time format. Use formats like '7 PM', '7:30 PM', or '19:00'"
    
    # Validate business hours
    if hour < settings.OPENING_HOUR or hour >= settings.CLOSING_HOUR:
        return False, None, f"We're open from {settings.OPENING_HOUR}:00 to {settings.CLOSING_HOUR}:00"
    
    # Normalize to readable format
    period = "AM" if hour < 12 else "PM"
    display_hour = hour if hour <= 12 else hour - 12
    if display_hour == 0:
        display_hour = 12
    
    normalized = f"{display_hour}:{minute:02d} {period}"
    return True, normalized, None


def validate_people(people_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Validate number of people.
    
    Args:
        people_str: Number as string
        
    Returns:
        Tuple of (is_valid, count, error_message)
    """
    try:
        # Extract number from string
        numbers = re.findall(r'\d+', people_str)
        if not numbers:
            return False, None, f"Please enter a number between {settings.MIN_PARTY_SIZE} and {settings.MAX_PARTY_SIZE}"
        
        count = int(numbers[0])
        
        if count < settings.MIN_PARTY_SIZE:
            return False, None, f"Minimum party size is {settings.MIN_PARTY_SIZE}"
        
        if count > settings.MAX_PARTY_SIZE:
            return False, None, f"Maximum party size is {settings.MAX_PARTY_SIZE}. For larger events, please call us."
        
        return True, count, None
        
    except ValueError:
        return False, None, "Please enter a valid number"


def validate_name(name: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate and normalize name.
    
    Args:
        name: Name string
        
    Returns:
        Tuple of (is_valid, normalized_name, error_message)
    """
    name = name.strip()
    
    if len(name) < 2:
        return False, None, "Name is too short"
    
    if len(name) > 100:
        return False, None, "Name is too long"
    
    # Check for valid characters (letters, spaces, common punctuation)
    # Allow Tamil Unicode characters
    if not re.match(r'^[a-zA-Z\s\.\'\-\u0B80-\u0BFF]+$', name):
        # Still accept but warn
        pass
    
    # Normalize: title case
    normalized = name.title()
    return True, normalized, None


def validate_menu_pack(pack_str: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate menu pack selection.
    
    Args:
        pack_str: Menu pack input
        
    Returns:
        Tuple of (is_valid, pack_key, error_message)
    """
    pack_lower = pack_str.lower().strip()
    
    # Direct match
    if pack_lower in MENU_PACKS:
        if MENU_PACKS[pack_lower].get("is_available", True):
            return True, pack_lower, None
        else:
            return False, None, "This menu pack is currently unavailable"
    
    # Fuzzy match
    aliases = {
        "veg": ["vegetarian", "vegan", "1", "one", "pure veg", "சைவ"],
        "nonveg": ["non-veg", "non veg", "chicken", "meat", "2", "two", "அசைவ"],
        "premium": ["prem", "royal", "3", "three", "பிரீமியம்"],
        "deluxe": ["grand", "luxury", "4", "four", "டீலக்ஸ்"]
    }
    
    for pack_key, alias_list in aliases.items():
        if pack_lower in alias_list:
            if MENU_PACKS[pack_key].get("is_available", True):
                return True, pack_key, None
    
    return False, None, "Please select: veg, nonveg, premium, or deluxe"


def validate_addons(addons_str: str) -> Tuple[bool, List[str], Optional[str]]:
    """
    Validate addon selections.
    
    Args:
        addons_str: Comma-separated addon input
        
    Returns:
        Tuple of (is_valid, addon_list, error_message)
    """
    addons_str = addons_str.lower().strip()
    
    # Check for "none"
    if addons_str in ["none", "no", "skip", "nothing", "nil", "இல்லை", "வேண்டாம்"]:
        return True, [], None
    
    # Parse comma-separated values
    raw_addons = [a.strip() for a in re.split(r'[,\s]+', addons_str) if a.strip()]
    
    valid_addons = []
    invalid_addons = []
    
    # Aliases for addons
    aliases = {
        "decoration": ["decor", "decorations", "அலங்காரம்"],
        "cake": ["birthday cake", "கேக்"],
        "photography": ["photo", "photos", "photographer", "புகைப்படம்"],
        "music_system": ["music", "sound", "speakers", "speaker", "ஒலி"],
        "dj": ["disc jockey", "டிஜே"],
        "live_music": ["live band", "band", "லைவ் மியூசிக்"],
        "flowers": ["flower", "floral", "மலர்"],
        "balloons": ["balloon", "பலூன்"]
    }
    
    for addon in raw_addons:
        # Direct match
        if addon in ADDONS:
            if ADDONS[addon].get("is_available", True):
                valid_addons.append(addon)
            continue
        
        # Alias match
        matched = False
        for addon_key, alias_list in aliases.items():
            if addon in alias_list:
                if ADDONS[addon_key].get("is_available", True):
                    valid_addons.append(addon_key)
                matched = True
                break
        
        if not matched:
            invalid_addons.append(addon)
    
    if invalid_addons and not valid_addons:
        return False, [], f"Unknown addons: {', '.join(invalid_addons)}"
    
    # Remove duplicates while preserving order
    valid_addons = list(dict.fromkeys(valid_addons))
    
    return True, valid_addons, None


def generate_reservation_id(name: str, people: int, date: str) -> str:
    """
    Generate unique reservation ID.
    
    Args:
        name: Customer name
        people: Party size
        date: Reservation date
        
    Returns:
        Unique reservation ID
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data = f"{name}{people}{date}{timestamp}"
    hash_str = hashlib.md5(data.encode()).hexdigest()[:6].upper()
    return f"RSV{hash_str}"


def calculate_total_cost(menu_pack: str, people: int, addons: List[str]) -> Dict[str, int]:
    """
    Calculate total cost breakdown.
    
    Args:
        menu_pack: Selected menu pack key
        people: Number of guests
        addons: List of addon keys
        
    Returns:
        Cost breakdown dictionary
    """
    pack = MENU_PACKS.get(menu_pack, {})
    base_price = pack.get("price_per_person", 0)
    menu_cost = base_price * people
    
    addon_cost = 0
    addon_breakdown = []
    for addon_key in addons:
        addon = ADDONS.get(addon_key, {})
        price = addon.get("price", 0)
        addon_cost += price
        addon_breakdown.append({
            "name": addon.get("name", addon_key),
            "price": price
        })
    
    total = menu_cost + addon_cost
    
    return {
        "menu_cost": menu_cost,
        "price_per_person": base_price,
        "addon_cost": addon_cost,
        "addon_breakdown": addon_breakdown,
        "total": total
    }


def format_confirmation_details(
    name: str,
    people: int,
    date: str,
    time: str,
    event: str,
    menu_pack: str,
    addons: List[str],
    language: str = "en"
) -> str:
    """
    Format booking details for confirmation.
    
    Args:
        All booking details
        language: Language code
        
    Returns:
        Formatted details string
    """
    pack = MENU_PACKS.get(menu_pack, {})
    
    if language == "ta":
        pack_title = pack.get("title_ta", pack.get("title", menu_pack))
        addons_str = ", ".join([
            ADDONS.get(a, {}).get("name_ta", a) for a in addons
        ]) if addons else "இல்லை"
        
        return (
            f"👤 பெயர்: {name}\n"
            f"👥 விருந்தினர்: {people}\n"
            f"📅 தேதி: {date}\n"
            f"⏰ நேரம்: {time}\n"
            f"🎉 நிகழ்ச்சி: {event}\n"
            f"🍽️ மெனு: {pack_title}\n"
            f"✨ கூடுதல்: {addons_str}"
        )
    else:
        pack_title = pack.get("title", menu_pack)
        addons_str = ", ".join([
            ADDONS.get(a, {}).get("name", a) for a in addons
        ]) if addons else "None"
        
        return (
            f"👤 Name: {name}\n"
            f"👥 Guests: {people}\n"
            f"📅 Date: {date}\n"
            f"⏰ Time: {time}\n"
            f"🎉 Event: {event}\n"
            f"🍽️ Menu: {pack_title}\n"
            f"✨ Add-ons: {addons_str}"
        )


def sanitize_phone_number(phone: str) -> str:
    """
    Sanitize and normalize phone number from Twilio format.
    
    Args:
        phone: Phone number (e.g., 'whatsapp:+919876543210')
        
    Returns:
        Normalized phone number
    """
    # Remove WhatsApp prefix
    phone = phone.replace("whatsapp:", "")
    # Remove any non-numeric chars except +
    phone = re.sub(r'[^\d+]', '', phone)
    return phone


def mask_phone_number(phone: str) -> str:
    """
    Mask phone number for privacy.
    
    Args:
        phone: Full phone number
        
    Returns:
        Masked phone number (e.g., '+91****3210')
    """
    phone = sanitize_phone_number(phone)
    if len(phone) > 6:
        return phone[:3] + "****" + phone[-4:]
    return "****"
