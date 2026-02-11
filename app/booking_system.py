"""
Booking System for Server Sundharam Bot.
Handles reservation creation, storage, and management.

Author: Server Sundharam Dev Team
Version: 2.0
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import threading
import json
from pathlib import Path
from .models import Reservation, SeatingRecommendation
from .menu_engine import MenuEngine
from .slot_locker import slot_locker
from .config import settings


class BookingSystem:
    """
    Manages reservation creation, storage, and retrieval.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # In-memory reservations store
        self._reservations: Dict[str, Reservation] = {}
        self._data_lock = threading.Lock()
        
        # Storage path for persistence
        self._storage_path = Path(__file__).parent.parent / "data" / "reservations.json"
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing reservations
        self._load_reservations()
        
        self._initialized = True
    
    def _load_reservations(self):
        """Load reservations from file."""
        try:
            if self._storage_path.exists():
                with open(self._storage_path, 'r') as f:
                    data = json.load(f)
                    # Convert back to Reservation objects (simplified for now)
                    self._reservations = data
        except Exception as e:
            print(f"Error loading reservations: {e}")
            self._reservations = {}
    
    def _save_reservations(self):
        """Save reservations to file."""
        try:
            with open(self._storage_path, 'w') as f:
                json.dump(self._reservations, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving reservations: {e}")
    
    def create_reservation(
        self,
        user_id: str,
        name: str,
        people: int,
        date: str,
        time: str,
        event: str,
        menu_pack: str,
        addons: List[str],
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Create a new reservation.
        
        Returns a dict with reservation details and confirmation messages.
        """
        # Generate unique reservation ID
        reservation_id = f"RC{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        
        # Get menu pack details
        pack = MenuEngine.get_menu_pack(menu_pack)
        if not pack:
            pack = MenuEngine.get_menu_pack("veg")
        
        # Calculate costs
        base_cost, addon_cost, total_cost = MenuEngine.calculate_cost(people, menu_pack, addons)
        
        # Get seating recommendation
        seating = MenuEngine.get_seating_recommendation(people, lang)
        
        # Build addon details
        addon_details = []
        for addon_key in addons:
            addon = MenuEngine.get_addon(addon_key)
            if addon:
                addon_details.append({
                    "key": addon.key,
                    "name": addon.name_en if lang == "en" else addon.name_ta,
                    "price": addon.price
                })
        
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
            "menu_pack_details": {
                "name": pack.name_en if lang == "en" else pack.name_ta,
                "price_per_person": pack.price_per_person,
                "items": pack.items_en if lang == "en" else pack.items_ta
            },
            "addons": addons,
            "addon_details": addon_details,
            "seating": {
                "type": seating.seating_type.value,
                "tables": seating.tables_needed,
                "hall": seating.hall_name,
                "layout": seating.layout_visual
            },
            "base_cost": base_cost,
            "addon_cost": addon_cost,
            "total_cost": total_cost,
            "status": "confirmed",
            "created_at": datetime.now().isoformat(),
            "restaurant": settings.RESTAURANT_NAME
        }
        
        # Confirm the slot lock
        slot_locker.confirm_slot(date, time, user_id)
        
        # Store reservation
        with self._data_lock:
            self._reservations[reservation_id] = reservation
            self._save_reservations()
        
        # Generate confirmation messages
        confirmation_en = self._generate_confirmation_message(reservation, "en")
        confirmation_ta = self._generate_confirmation_message(reservation, "ta")
        
        return {
            "reservation": reservation,
            "confirmation_en": confirmation_en,
            "confirmation_ta": confirmation_ta
        }
    
    def _generate_confirmation_message(self, reservation: dict, lang: str) -> str:
        """Generate human-like confirmation message."""
        if lang == "ta":
            msg = f"""
🎉 *BOOKING CONFIRMED!* 🎉

நன்றி {reservation['name']}! உங்க table ready!

━━━━━━━━━━━━━━━━━━━━━
📋 *Booking Details*
━━━━━━━━━━━━━━━━━━━━━
🎫 Reservation ID: *{reservation['reservation_id']}*
📅 Date: *{reservation['date']}*
⏰ Time: *{reservation['time']}*
👥 Guests: *{reservation['people']} பேர்*
🎊 Event: *{reservation['event'].title()}*
🍽️ Menu: *{reservation['menu_pack_details']['name']}*

━━━━━━━━━━━━━━━━━━━━━
💰 *Bill Summary*
━━━━━━━━━━━━━━━━━━━━━
Menu Cost: ₹{reservation['base_cost']}
Addons: ₹{reservation['addon_cost']}
*Total: ₹{reservation['total_cost']}*

━━━━━━━━━━━━━━━━━━━━━
📍 {settings.RESTAURANT_NAME}
📞 {settings.RESTAURANT_PHONE}
━━━━━━━━━━━━━━━━━━━━━

உங்களை serve பண்ண excited-ஆ இருக்கோம்! 
See you soon! 🙏
"""
        else:
            msg = f"""
🎉 *BOOKING CONFIRMED!* 🎉

Thank you {reservation['name']}! Your table is ready!

━━━━━━━━━━━━━━━━━━━━━
📋 *Booking Details*
━━━━━━━━━━━━━━━━━━━━━
🎫 Reservation ID: *{reservation['reservation_id']}*
📅 Date: *{reservation['date']}*
⏰ Time: *{reservation['time']}*
👥 Guests: *{reservation['people']} people*
🎊 Event: *{reservation['event'].title()}*
🍽️ Menu: *{reservation['menu_pack_details']['name']}*

━━━━━━━━━━━━━━━━━━━━━
💰 *Bill Summary*
━━━━━━━━━━━━━━━━━━━━━
Menu Cost: ₹{reservation['base_cost']}
Addons: ₹{reservation['addon_cost']}
*Total: ₹{reservation['total_cost']}*

━━━━━━━━━━━━━━━━━━━━━
📍 {settings.RESTAURANT_NAME}
📞 {settings.RESTAURANT_PHONE}
━━━━━━━━━━━━━━━━━━━━━

We're excited to serve you!
See you soon! 🙏
"""
        return msg.strip()
    
    def get_reservation(self, reservation_id: str) -> Optional[Dict]:
        """Get a reservation by ID."""
        with self._data_lock:
            return self._reservations.get(reservation_id)
    
    def get_user_reservations(self, user_id: str) -> List[Dict]:
        """Get all reservations for a user."""
        with self._data_lock:
            return [
                r for r in self._reservations.values()
                if r.get("user_id") == user_id
            ]
    
    def search_reservations(
        self,
        name: str = None,
        date: str = None,
        date_from: str = None,
        date_to: str = None,
        status: str = None
    ) -> List[Dict]:
        """Search reservations with filters."""
        with self._data_lock:
            results = list(self._reservations.values())
            
            if name:
                results = [r for r in results if name.lower() in r.get("name", "").lower()]
            
            if date:
                results = [r for r in results if r.get("date") == date]
            
            if status:
                results = [r for r in results if r.get("status") == status]
            
            # Sort by date descending
            results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
            return results
    
    def get_all_reservations(self) -> List[Dict]:
        """Get all reservations."""
        with self._data_lock:
            return list(self._reservations.values())
    
    def get_today_reservations(self) -> List[Dict]:
        """Get today's reservations."""
        today = datetime.now().strftime("%d-%m-%Y")
        return self.search_reservations(date=today)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get booking statistics."""
        with self._data_lock:
            all_bookings = list(self._reservations.values())
            today = datetime.now().strftime("%d-%m-%Y")
            
            today_bookings = [b for b in all_bookings if b.get("date") == today]
            total_revenue = sum(b.get("total_cost", 0) for b in all_bookings)
            
            # Popular menu
            menu_counts = {}
            for b in all_bookings:
                menu = b.get("menu_pack", "unknown")
                menu_counts[menu] = menu_counts.get(menu, 0) + 1
            popular_menu = max(menu_counts, key=menu_counts.get) if menu_counts else "N/A"
            
            # Popular event
            event_counts = {}
            for b in all_bookings:
                event = b.get("event", "unknown")
                event_counts[event] = event_counts.get(event, 0) + 1
            popular_event = max(event_counts, key=event_counts.get) if event_counts else "N/A"
            
            return {
                "total_bookings": len(all_bookings),
                "today_bookings": len(today_bookings),
                "total_revenue": total_revenue,
                "popular_menu": popular_menu,
                "popular_event": popular_event,
                "active_slots_locked": slot_locker.get_locked_slots_count()
            }
    
    def cancel_reservation(self, reservation_id: str, user_id: str) -> bool:
        """Cancel a reservation."""
        with self._data_lock:
            if reservation_id in self._reservations:
                r = self._reservations[reservation_id]
                if r.get("user_id") == user_id:
                    r["status"] = "cancelled"
                    self._save_reservations()
                    return True
            return False


# Global booking system instance
booking_system = BookingSystem()
