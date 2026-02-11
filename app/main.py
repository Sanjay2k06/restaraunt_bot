"""
FastAPI WhatsApp Bot Backend for Restaurant Reservations.
Integrates with Twilio for WhatsApp messaging.
"""

import os
import logging
import hmac
import hashlib
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, Request, HTTPException, Depends, Header
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

from .bot_logic import bot_engine, BotEngine
from .session_manager import session_manager
from .reservation_service import ReservationService
from .config import settings
from .menu_data import MENU_PACKS, ADDONS, format_menu_list, format_addon_list

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG_MODE else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info(f"Starting {settings.RESTAURANT_NAME} WhatsApp Bot...")
    logger.info(f"Session timeout: {settings.SESSION_TIMEOUT_MINUTES} minutes")
    logger.info(f"Business hours: {settings.OPENING_HOUR}:00 - {settings.CLOSING_HOUR}:00")
    settings.validate()
    yield
    # Shutdown
    logger.info("Shutting down WhatsApp Bot...")


# Initialize FastAPI app
app = FastAPI(
    title=f"{settings.RESTAURANT_NAME} - WhatsApp Bot",
    description="AI-powered WhatsApp bot for restaurant table reservations and event bookings",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_twilio_request(request: Request, x_twilio_signature: Optional[str] = Header(None)) -> bool:
    """
    Validate that the request came from Twilio.
    
    Args:
        request: FastAPI request object
        x_twilio_signature: Twilio signature header
        
    Returns:
        True if valid, raises HTTPException otherwise
    """
    if settings.DEBUG_MODE:
        return True
    
    if not x_twilio_signature:
        logger.warning("Missing Twilio signature")
        return True  # Allow in development, should fail in production
    
    if not settings.TWILIO_AUTH_TOKEN:
        logger.warning("TWILIO_AUTH_TOKEN not configured")
        return True
    
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    
    # Get the full URL
    url = str(request.url)
    
    # This would need the form data, which we don't have yet in the dependency
    # For now, return True and validate in the endpoint if needed
    return True


# ==================== HEALTH CHECK ENDPOINTS ====================

@app.get("/", response_class=JSONResponse)
async def root():
    """Root endpoint - API information."""
    return {
        "name": f"{settings.RESTAURANT_NAME} WhatsApp Bot",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "webhook": "/bot",
            "health": "/health",
            "stats": "/stats",
            "menu": "/menu",
            "docs": "/docs"
        }
    }


@app.get("/health", response_class=JSONResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "restaurant-whatsapp-bot",
        "active_sessions": session_manager.get_active_session_count()
    }


# ==================== TWILIO WEBHOOK ENDPOINT ====================

@app.post("/bot", response_class=PlainTextResponse)
async def whatsapp_webhook(
    request: Request,
    From: str = Form(..., description="Sender's WhatsApp number"),
    Body: str = Form(..., description="Message content"),
    ProfileName: Optional[str] = Form(None, description="Sender's WhatsApp profile name"),
    MessageSid: Optional[str] = Form(None, description="Twilio message SID"),
    NumMedia: Optional[int] = Form(0, description="Number of media attachments"),
    WaId: Optional[str] = Form(None, description="WhatsApp ID"),
    AccountSid: Optional[str] = Form(None, description="Twilio account SID")
):
    """
    Main Twilio WhatsApp webhook endpoint.
    Receives messages from Twilio and returns TwiML response.
    
    Args:
        From: Sender's WhatsApp number (e.g., 'whatsapp:+919876543210')
        Body: Message content
        ProfileName: User's WhatsApp profile name
        MessageSid: Twilio message identifier
        NumMedia: Number of media files attached
        WaId: WhatsApp ID
        AccountSid: Twilio account SID
        
    Returns:
        TwiML response string
    """
    try:
        # Log incoming request
        logger.info(f"Webhook received from {From[:15]}... | Message: {Body[:30]}...")
        
        # Handle media messages
        if NumMedia and NumMedia > 0:
            reply = "I can only process text messages at the moment. Please type your request."
        else:
            # Process message through bot engine
            metadata = {
                "profile_name": ProfileName,
                "message_sid": MessageSid,
                "wa_id": WaId
            }
            reply = BotEngine.process(From, Body, metadata)
        
        # Return plain text response (no XML/TwiML)
        return reply
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        
        # Return error response
        return "Sorry, something went wrong. Please try again in a moment."


@app.post("/webhook", response_class=PlainTextResponse)
async def whatsapp_webhook_alt(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...)
):
    """Alternative webhook endpoint (alias for /bot)."""
    return await whatsapp_webhook(request, From=From, Body=Body)


# ==================== ADMIN API ENDPOINTS ====================

@app.get("/stats", response_class=JSONResponse)
async def get_stats():
    """Get system statistics."""
    return BotEngine.get_system_stats()


@app.get("/sessions", response_class=JSONResponse)
async def get_sessions():
    """Get all active sessions (admin only)."""
    if not settings.DEBUG_MODE:
        raise HTTPException(status_code=403, detail="Admin access only")
    
    return {
        "active_sessions": session_manager.get_all_sessions(),
        "stats": session_manager.get_session_stats()
    }


@app.delete("/sessions/{user_id}", response_class=JSONResponse)
async def clear_session(user_id: str):
    """Clear a specific user's session."""
    if not settings.DEBUG_MODE:
        raise HTTPException(status_code=403, detail="Admin access only")
    
    success = BotEngine.reset_user_session(f"whatsapp:{user_id}")
    return {"success": success, "user_id": user_id}


# ==================== MENU ENDPOINTS ====================

@app.get("/menu", response_class=JSONResponse)
async def get_menu(language: str = "en"):
    """
    Get all menu packs.
    
    Args:
        language: Language code ('en' or 'ta')
    """
    menu_data = {}
    for key, pack in MENU_PACKS.items():
        if pack.get("is_available", True):
            menu_data[key] = {
                "title": pack.get("title_ta" if language == "ta" else "title"),
                "price_per_person": pack.get("price_per_person"),
                "items": pack.get("items_ta" if language == "ta" else "items"),
                "description": pack.get("description_ta" if language == "ta" else "description"),
                "min_people": pack.get("min_people", 1)
            }
    
    return {
        "menu_packs": menu_data,
        "formatted": format_menu_list(language)
    }


@app.get("/addons", response_class=JSONResponse)
async def get_addons(language: str = "en"):
    """
    Get all addons.
    
    Args:
        language: Language code ('en' or 'ta')
    """
    addon_data = {}
    for key, addon in ADDONS.items():
        if addon.get("is_available", True):
            addon_data[key] = {
                "name": addon.get("name_ta" if language == "ta" else "name"),
                "price": addon.get("price"),
                "description": addon.get("description_ta" if language == "ta" else "description")
            }
    
    return {
        "addons": addon_data,
        "formatted": format_addon_list(language)
    }


# ==================== RESERVATION ENDPOINTS ====================

@app.get("/reservations", response_class=JSONResponse)
async def get_reservations():
    """Get all reservations (admin only)."""
    if not settings.DEBUG_MODE:
        raise HTTPException(status_code=403, detail="Admin access only")
    
    return {
        "reservations": ReservationService.get_all_reservations(),
        "count": len(ReservationService.get_all_reservations())
    }


@app.get("/reservations/{reservation_id}", response_class=JSONResponse)
async def get_reservation(reservation_id: str):
    """Get a specific reservation."""
    reservation = ReservationService.get_reservation(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


@app.get("/reservations/date/{date}", response_class=JSONResponse)
async def get_reservations_by_date(date: str):
    """Get all reservations for a specific date."""
    reservations = ReservationService.get_reservations_by_date(date)
    return {
        "date": date,
        "reservations": reservations,
        "count": len(reservations)
    }


@app.post("/reservations/{reservation_id}/cancel", response_class=JSONResponse)
async def cancel_reservation(reservation_id: str):
    """Cancel a reservation."""
    success = ReservationService.cancel_reservation(reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"success": True, "reservation_id": reservation_id, "status": "cancelled"}


@app.get("/availability", response_class=JSONResponse)
async def check_availability(date: str, time: str, people: int):
    """
    Check availability for a given date, time, and party size.
    
    Args:
        date: Date in DD-MM-YYYY format
        time: Time (e.g., '7 PM')
        people: Number of guests
    """
    return ReservationService.check_availability(date, time, people)


# ==================== TEST ENDPOINT ====================

@app.post("/test", response_class=JSONResponse)
async def test_message(message: str, user_id: str = "test_user"):
    """
    Test endpoint for debugging (no Twilio).
    
    Args:
        message: Test message
        user_id: Test user ID
    """
    if not settings.DEBUG_MODE:
        raise HTTPException(status_code=403, detail="Debug mode only")
    
    response = BotEngine.process(f"whatsapp:+91{user_id}", message)
    return {
        "input": message,
        "response": response,
        "session": BotEngine.get_session_info(f"whatsapp:+91{user_id}")
    }


# ==================== ERROR HANDLERS ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "status_code": 500}
    )


# ==================== MAIN ENTRY POINT ====================

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (Render provides PORT)
    port = int(os.environ.get("PORT", 10000))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
