# 🍽️ Royal Chef's Restaurant - WhatsApp Bot

A production-ready FastAPI backend for WhatsApp-based restaurant table reservations with AI-style conversation flow.

## ✨ Features

- **Multi-language Support**: English and Tamil (தமிழ்)
- **AI-Style Conversation Engine**: Natural, human-like responses with variations
- **Step-based Reservation Flow**: Name → People → Date → Time → Event → Menu → Addons → Confirmation
- **Session Timeout System**: Automatic session cleanup with configurable timeout
- **Dynamic Menu Packs**: Veg, Non-Veg, Premium, and Deluxe options
- **Event Recommendations**: Smart suggestions based on event type
- **Table Layout Generator**: Visual seating arrangements
- **Restart Support**: Users can restart conversation anytime
- **Twilio Integration**: Full WhatsApp webhook support
- **Environment Variables**: Secure configuration management
- **Strong Error Handling**: Graceful error recovery
- **RESTful Admin API**: Manage reservations and sessions

## 📁 Project Structure

```
restaurant_bot/
├── app/
│   ├── __init__.py          # Package exports
│   ├── main.py               # FastAPI application & endpoints
│   ├── bot_logic.py          # Main bot controller
│   ├── conversation_engine.py # Step-based conversation flow
│   ├── session_manager.py    # User session handling
│   ├── reservation_service.py # Reservation CRUD operations
│   ├── language.py           # Multi-language responses
│   ├── menu_data.py          # Menu packs, addons, recommendations
│   ├── models.py             # Pydantic data models
│   ├── utils.py              # Utility functions
│   └── config.py             # Configuration management
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd restaurant_bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac

# Edit .env with your settings
```

Required environment variables:
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
SESSION_TIMEOUT_MINUTES=15
DEBUG_MODE=true
```

### 3. Run the Server

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. Configure Twilio Webhook

1. Go to [Twilio Console](https://console.twilio.com)
2. Navigate to Messaging → Try it out → Send a WhatsApp message
3. Configure your sandbox webhook URL:
   - **When a message comes in**: `https://your-domain.com/bot`
   - **HTTP Method**: POST

## 📱 Conversation Flow

```
User: hi
Bot: 👋 Hello! Welcome to Royal Chef's Restaurant!
     1️⃣ Book a Table
     2️⃣ Plan an Event
     3️⃣ Browse Our Menu

User: 1
Bot: Wonderful! Let's get started! 📝
     May I know your good name?

User: Sanjay
Bot: Nice to meet you, Sanjay! 😊
     How many guests will be joining?

User: 8
Bot: Got it! 8 people – that's going to be fun! 🎉
     When would you like to visit us? 📅
     (DD-MM-YYYY format)

User: 15-03-2026
Bot: Excellent! 15-03-2026 is marked! 📌
     What time would you like your reservation? ⏰

User: 7 PM
Bot: Perfect! See you at 7:00 PM! ⏰
     What's the occasion? 🎊

User: Birthday
Bot: Oh, a Birthday! How exciting! 🎉
     💡 Pro Tip: Theme decoration + cake + music system recommended!
     
     Choose your menu pack:
     🥗 Pure Veg Delight - ₹399/person
     🍗 Non-Veg Classic - ₹499/person
     👑 Premium Royal Feast - ₹749/person
     🌟 Grand Deluxe - ₹999/person

User: nonveg
Bot: Excellent choice! Non-Veg Classic is absolutely delicious! 😋
     
     Want to make it extra special? ✨
     • Theme Decoration – ₹2500
     • Designer Cake – ₹1200
     • Photography – ₹3500
     ...

User: decoration, cake
Bot: Great additions! Added: Theme Decoration, Designer Cake ✨
     
     📋 Booking Summary
     ━━━━━━━━━━━━━━━━
     👤 Name: Sanjay
     👥 Guests: 8
     📅 Date: 15-03-2026
     ⏰ Time: 7:00 PM
     🎉 Event: Birthday
     🍽️ Menu: Non-Veg Classic
     ✨ Add-ons: Theme Decoration, Designer Cake
     💰 Total: ₹7692
     
     Shall I confirm? (yes/no)

User: yes
Bot: 🎉 RESERVATION CONFIRMED!
     📋 Reservation ID: RSV8A3F21
     ...
```

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/bot` | Twilio WhatsApp webhook |
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/stats` | System statistics |
| GET | `/menu` | Get menu packs |
| GET | `/addons` | Get available addons |
| GET | `/reservations` | List all reservations |
| GET | `/reservations/{id}` | Get specific reservation |
| POST | `/reservations/{id}/cancel` | Cancel reservation |
| GET | `/availability` | Check availability |
| POST | `/test` | Test endpoint (debug mode) |

## 🔧 Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `TWILIO_ACCOUNT_SID` | - | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | - | Twilio Auth Token |
| `SESSION_TIMEOUT_MINUTES` | 15 | Session timeout in minutes |
| `DEFAULT_LANGUAGE` | en | Default language (en/ta) |
| `DEBUG_MODE` | false | Enable debug features |
| `RESTAURANT_NAME` | Royal Chef's Restaurant | Restaurant name |
| `OPENING_HOUR` | 11 | Opening hour (24h format) |
| `CLOSING_HOUR` | 23 | Closing hour (24h format) |
| `MIN_PARTY_SIZE` | 1 | Minimum guests |
| `MAX_PARTY_SIZE` | 100 | Maximum guests |
| `ADVANCE_BOOKING_DAYS` | 30 | Max advance booking days |

## 🗣️ Supported Commands

| Command | Description |
|---------|-------------|
| `hi`, `hello` | Start new conversation |
| `restart` | Clear and restart |
| `cancel` | Cancel current booking |
| `help` | Show help message |
| `menu` | View menu packs |
| `tamil` | Switch to Tamil |
| `english` | Switch to English |

## 🔒 Security

- Environment variables for sensitive data
- Twilio request signature validation
- Input sanitization and validation
- Phone number masking in logs
- No credentials in code

## 📦 Dependencies

- **FastAPI** - Modern async web framework
- **Uvicorn** - ASGI server
- **Twilio** - WhatsApp integration
- **Pydantic** - Data validation
- **python-dotenv** - Environment management

## 🏗️ Production Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using ngrok (for testing)

```bash
# Start the server
uvicorn app.main:app --reload

# In another terminal
ngrok http 8000

# Use the ngrok URL as your Twilio webhook
```

## 📄 License

MIT License - feel free to use for your projects!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

Built with ❤️ for Royal Chef's Restaurant
 
