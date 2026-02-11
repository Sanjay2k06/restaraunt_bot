"""
Reservation service for the Restaurant Bot.
Handles reservation creation, storage, and retrieval.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from .config import settings
from .menu_data import (
    MENU_PACKS, ADDONS, 
    get_event_recommendation, get_table_layout,
    calculate_menu_cost, calculate_addons_cost
)
from .utils import (
    generate_reservation_id, 
    table_layout as generate_table_layout,
    calculate_total_cost
)

# Configure logging
logger = logging.getLogger(__name__)


# In-memory reservation storage (replace with database in production)
reservations_db: Dict[str, Dict[str, Any]] = {}


class ReservationService:
    """
    Service class for managing reservations.
    Handles creation, retrieval, updates, and cancellations.
    """
    
    @staticmethod
    def create_reservation(
        user_id: str,
        name: str,
        people: int,
        date: str,
        time: str,
        event: str,
        menu_pack: str,
        addons: List[str],
        special_requests: Optional[str] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Create a new reservation.
        
        Args:
            user_id: WhatsApp user ID
            name: Customer name
            people: Number of guests
            date: Reservation date
            time: Reservation time
            event: Event type
            menu_pack: Selected menu pack
            addons: List of selected addons
            special_requests: Any special requests
            language: User's language preference
            
        Returns:
            Complete reservation details
        """
        try:
            # Generate unique reservation ID
            reservation_id = generate_reservation_id(name, people, date)
            
            # Get menu pack details
            pack_details = MENU_PACKS.get(menu_pack, {})
            
            # Get addon details
            addon_details = []
            for addon_key in addons:
                addon = ADDONS.get(addon_key, {})
                if addon:
                    addon_details.append({
                        "key": addon_key,
                        "name": addon.get("name_ta" if language == "ta" else "name", addon_key),
                        "price": addon.get("price", 0)
                    })
            
            # Calculate costs
            cost_breakdown = calculate_total_cost(menu_pack, people, addons)
            
            # Get event recommendation
            event_rec = get_event_recommendation(event)
            
            # Generate table layout
            layout_text = generate_table_layout(people, event, language)
            
            # Build recommendation message
            if language == "ta":
                recommendation = event_rec.get("message_ta", event_rec.get("message_en", ""))
            else:
                recommendation = event_rec.get("message_en", "")
            
            # Create reservation record
            reservation = {
                "reservation_id": reservation_id,
                "user_id": user_id,
                "name": name,
                "people": people,
                "date": date,
                "time": time,
                "event": event,
                "menu_pack": menu_pack,
                "menu_details": {
                    "key": menu_pack,
                    "title": pack_details.get("title_ta" if language == "ta" else "title", menu_pack),
                    "price_per_person": pack_details.get("price_per_person", 0),
                    "items": pack_details.get("items_ta" if language == "ta" else "items", [])
                },
                "addons": addons,
                "addon_details": addon_details,
                "layout": layout_text,
                "seating_style": event_rec.get("seating_style", "standard"),
                "recommendation": recommendation,
                "special_notes": event_rec.get("special_notes", ""),
                "base_cost": cost_breakdown["menu_cost"],
                "addon_cost": cost_breakdown["addon_cost"],
                "total_cost": cost_breakdown["total"],
                "cost_breakdown": cost_breakdown,
                "special_requests": special_requests,
                "status": "confirmed",
                "language": language,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Store reservation
            reservations_db[reservation_id] = reservation
            
            logger.info(f"Created reservation {reservation_id} for {name}")
            
            return reservation
            
        except Exception as e:
            logger.error(f"Error creating reservation: {str(e)}")
            raise
    
    @staticmethod
    def get_reservation(reservation_id: str) -> Optional[Dict[str, Any]]:
        """Get reservation by ID."""
        return reservations_db.get(reservation_id)
    
    @staticmethod
    def get_user_reservations(user_id: str) -> List[Dict[str, Any]]:
        """Get all reservations for a user."""
        return [
            res for res in reservations_db.values()
            if res.get("user_id") == user_id
        ]
    
    @staticmethod
    def cancel_reservation(reservation_id: str) -> bool:
        """Cancel a reservation."""
        if reservation_id in reservations_db:
            reservations_db[reservation_id]["status"] = "cancelled"
            reservations_db[reservation_id]["updated_at"] = datetime.now().isoformat()
            logger.info(f"Cancelled reservation {reservation_id}")
            return True
        return False
    
    @staticmethod
    def update_reservation(reservation_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a reservation."""
        if reservation_id in reservations_db:
            reservations_db[reservation_id].update(updates)
            reservations_db[reservation_id]["updated_at"] = datetime.now().isoformat()
            logger.info(f"Updated reservation {reservation_id}")
            return reservations_db[reservation_id]
        return None
    
    @staticmethod
    def get_all_reservations() -> List[Dict[str, Any]]:
        """Get all reservations (admin function)."""
        return list(reservations_db.values())
    
    @staticmethod
    def get_reservations_by_date(date: str) -> List[Dict[str, Any]]:
        """Get all reservations for a specific date."""
        return [
            res for res in reservations_db.values()
            if res.get("date") == date and res.get("status") == "confirmed"
        ]
    
    @staticmethod
    def check_availability(date: str, time: str, people: int) -> Dict[str, Any]:
        """
        Check table availability for given date/time.
        Returns availability status and any conflicts.
        """
        existing = ReservationService.get_reservations_by_date(date)
        
        # Simple availability check (can be enhanced with actual table inventory)
        same_time_reservations = [
            res for res in existing
            if res.get("time") == time
        ]
        
        total_people_at_time = sum(res.get("people", 0) for res in same_time_reservations)
        max_capacity = 150  # Restaurant capacity
        
        available = (total_people_at_time + people) <= max_capacity
        
        return {
            "available": available,
            "date": date,
            "time": time,
            "requested_people": people,
            "current_bookings_at_time": len(same_time_reservations),
            "total_people_at_time": total_people_at_time,
            "remaining_capacity": max(0, max_capacity - total_people_at_time),
            "max_capacity": max_capacity
        }
    
    @staticmethod
    def format_reservation_summary(reservation: Dict[str, Any], language: str = "en") -> str:
        """
        Format reservation for display.
        
        Args:
            reservation: Reservation dictionary
            language: Language code
            
        Returns:
            Formatted string
        """
        if language == "ta":
            addons_str = ", ".join([
                ad.get("name", "") for ad in reservation.get("addon_details", [])
            ]) or "இல்லை"
            
            return (
                f"📋 *பதிவு விவரம்*\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"🔖 பதிவு எண்: *{reservation['reservation_id']}*\n"
                f"👤 பெயர்: {reservation['name']}\n"
                f"👥 விருந்தினர்: {reservation['people']}\n"
                f"📅 தேதி: {reservation['date']}\n"
                f"⏰ நேரம்: {reservation['time']}\n"
                f"🎉 நிகழ்ச்சி: {reservation['event']}\n"
                f"🍽️ மெனு: {reservation['menu_details']['title']}\n"
                f"✨ கூடுதல்: {addons_str}\n"
                f"💰 மொத்தம்: ₹{reservation['total_cost']}"
            )
        else:
            addons_str = ", ".join([
                ad.get("name", "") for ad in reservation.get("addon_details", [])
            ]) or "None"
            
            return (
                f"📋 *Reservation Details*\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"🔖 ID: *{reservation['reservation_id']}*\n"
                f"👤 Name: {reservation['name']}\n"
                f"👥 Guests: {reservation['people']}\n"
                f"📅 Date: {reservation['date']}\n"
                f"⏰ Time: {reservation['time']}\n"
                f"🎉 Event: {reservation['event']}\n"
                f"🍽️ Menu: {reservation['menu_details']['title']}\n"
                f"✨ Add-ons: {addons_str}\n"
                f"💰 Total: ₹{reservation['total_cost']}"
            )


# Convenience function for backward compatibility
def create_reservation(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create reservation from session data (backward compatible).
    
    Args:
        data: Session data dictionary
        
    Returns:
        Reservation details
    """
    return ReservationService.create_reservation(
        user_id=data.get("user_id", "unknown"),
        name=data.get("name", "Guest"),
        people=data.get("people", 1),
        date=data.get("date", ""),
        time=data.get("time", ""),
        event=data.get("event", "General"),
        menu_pack=data.get("menu_pack", "veg"),
        addons=data.get("addons", []),
        special_requests=data.get("special_requests"),
        language=data.get("language", "en")
    )


def calculate_cost(people: int, menu_pack: str, addons: List[str]) -> int:
    """
    Calculate total cost (backward compatible).
    
    Args:
        people: Number of guests
        menu_pack: Menu pack key
        addons: List of addon keys
        
    Returns:
        Total cost
    """
    menu_cost = calculate_menu_cost(menu_pack, people)
    addon_cost = calculate_addons_cost(addons)
    return menu_cost + addon_cost
