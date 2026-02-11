"""
Slot Locker Module for Server Sundharam Bot.
BookMyShow-style slot locking to prevent double bookings.

Features:
- Temporary slot locking during booking process
- Auto-release after timeout (3 minutes)
- Thread-safe operations
- Slot availability checking

Author: Server Sundharam Dev Team
Version: 2.0
"""

import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from .models import SlotLock
from .config import settings


class SlotLocker:
    """
    Manages slot locking similar to BookMyShow seat locking.
    
    When a user selects a date+time, the slot is temporarily locked
    for that user. If another user tries to book the same slot,
    they're informed it's held and asked to choose another time.
    
    Locks auto-expire after SLOT_LOCK_DURATION_MINUTES (default 3).
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern for thread-safe slot management."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # Locked slots: {lock_key: SlotLock}
        self._locked_slots: Dict[str, SlotLock] = {}
        
        # Confirmed bookings: {lock_key: user_id}
        self._confirmed_slots: Dict[str, str] = {}
        
        # Lock for thread-safe operations (RLock for re-entrant calls)
        self._data_lock = threading.RLock()
        
        # Start cleanup thread
        self._start_cleanup_thread()
        
        self._initialized = True
    
    def _start_cleanup_thread(self):
        """Start background thread to cleanup expired locks."""
        def cleanup_task():
            import time
            while True:
                self._cleanup_expired_locks()
                time.sleep(30)  # Check every 30 seconds
        
        cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
        cleanup_thread.start()
    
    def _generate_lock_key(self, date: str, time: str) -> str:
        """Generate unique key for a slot."""
        return f"{date}_{time.replace(' ', '').replace(':', '')}"
    
    def _cleanup_expired_locks(self):
        """Remove expired slot locks."""
        with self._data_lock:
            now = datetime.now()
            expired = [
                key for key, lock in self._locked_slots.items()
                if now > lock.expires_at and not lock.is_confirmed
            ]
            for key in expired:
                del self._locked_slots[key]
    
    # ===========================================
    # PUBLIC METHODS
    # ===========================================
    
    def check_availability(self, date: str, time: str, user_id: str) -> Tuple[bool, str]:
        """
        Check if a slot is available.
        
        Returns:
            (is_available, status)
            status can be: 'available', 'locked_by_other', 'locked_by_you', 'confirmed'
        """
        lock_key = self._generate_lock_key(date, time)
        
        with self._data_lock:
            # Check if already confirmed by someone else
            if lock_key in self._confirmed_slots:
                if self._confirmed_slots[lock_key] == user_id:
                    return (False, 'confirmed_by_you')
                return (False, 'confirmed')
            
            # Check if locked
            if lock_key in self._locked_slots:
                lock = self._locked_slots[lock_key]
                
                # Check if lock expired
                if datetime.now() > lock.expires_at:
                    del self._locked_slots[lock_key]
                    return (True, 'available')
                
                # Check if locked by same user
                if lock.user_id == user_id:
                    return (True, 'locked_by_you')
                
                return (False, 'locked_by_other')
            
            return (True, 'available')
    
    def lock_slot(self, date: str, time: str, user_id: str, people: int) -> Tuple[bool, str]:
        """
        Attempt to lock a slot for a user.
        
        Returns:
            (success, message_key)
        """
        lock_key = self._generate_lock_key(date, time)
        
        with self._data_lock:
            # First check availability
            is_available, status = self.check_availability(date, time, user_id)
            
            if status == 'confirmed':
                return (False, 'slot_already_booked')
            
            if status == 'locked_by_other':
                return (False, 'slot_locked_by_other')
            
            if status == 'locked_by_you':
                # Extend the lock
                self._locked_slots[lock_key].expires_at = datetime.now() + timedelta(
                    minutes=settings.SLOT_LOCK_DURATION_MINUTES
                )
                return (True, 'slot_lock_extended')
            
            # Create new lock
            expires_at = datetime.now() + timedelta(minutes=settings.SLOT_LOCK_DURATION_MINUTES)
            
            self._locked_slots[lock_key] = SlotLock(
                lock_key=lock_key,
                user_id=user_id,
                date=date,
                time=time,
                people=people,
                expires_at=expires_at
            )
            
            return (True, 'slot_locked')
    
    def release_lock(self, user_id: str) -> bool:
        """
        Release any slot locked by a user.
        Called when user cancels or session expires.
        """
        with self._data_lock:
            to_remove = [
                key for key, lock in self._locked_slots.items()
                if lock.user_id == user_id and not lock.is_confirmed
            ]
            for key in to_remove:
                del self._locked_slots[key]
            return len(to_remove) > 0
    
    def confirm_slot(self, date: str, time: str, user_id: str) -> bool:
        """
        Confirm a locked slot (convert temporary lock to permanent booking).
        """
        lock_key = self._generate_lock_key(date, time)
        
        with self._data_lock:
            if lock_key in self._locked_slots:
                lock = self._locked_slots[lock_key]
                if lock.user_id == user_id:
                    lock.is_confirmed = True
                    self._confirmed_slots[lock_key] = user_id
                    return True
            return False
    
    def get_user_lock(self, user_id: str) -> Optional[SlotLock]:
        """Get the active lock for a user."""
        with self._data_lock:
            for lock in self._locked_slots.values():
                if lock.user_id == user_id and not lock.is_confirmed:
                    if datetime.now() <= lock.expires_at:
                        return lock
            return None
    
    def get_lock_remaining_time(self, user_id: str) -> Optional[int]:
        """Get remaining seconds on user's current lock."""
        lock = self.get_user_lock(user_id)
        if lock:
            remaining = (lock.expires_at - datetime.now()).total_seconds()
            return int(remaining) if remaining > 0 else 0
        return None
    
    def get_alternative_times(self, date: str, requested_time: str) -> List[str]:
        """
        Get alternative available times on the same date.
        """
        all_times = [
            "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM",
            "4:00 PM", "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM",
            "9:00 PM", "10:00 PM"
        ]
        
        available = []
        for time in all_times:
            lock_key = self._generate_lock_key(date, time)
            if lock_key not in self._locked_slots and lock_key not in self._confirmed_slots:
                available.append(time)
        
        return available[:5]  # Return max 5 alternatives
    
    def get_locked_slots_count(self) -> int:
        """Get count of currently locked slots."""
        self._cleanup_expired_locks()
        with self._data_lock:
            return len(self._locked_slots)
    
    def get_confirmed_slots_count(self) -> int:
        """Get count of confirmed bookings."""
        with self._data_lock:
            return len(self._confirmed_slots)


# Global singleton instance
slot_locker = SlotLocker()
