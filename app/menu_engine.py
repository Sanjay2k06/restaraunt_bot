"""
Menu Engine for Server Sundharam Bot.
Handles menu packs, addons, and event-based recommendations.

Author: Server Sundharam Dev Team
Version: 2.0
"""

from typing import Dict, List, Optional, Tuple
from .models import MenuPack, Addon, SeatingRecommendation, SeatingType
from .config import settings


class MenuEngine:
    """
    Manages menu packs, addons, and intelligent recommendations.
    Server Sundharam suggests like a real waiter based on context.
    """
    
    # ===========================================
    # MENU PACKS
    # ===========================================
    
    MENU_PACKS: Dict[str, MenuPack] = {
        "veg": MenuPack(
            key="veg",
            name_en="🥗 Vegetarian Pack",
            name_ta="🥗 சைவ பேக்",
            price_per_person=399,
            description_en="Pure veg feast with variety",
            description_ta="சுவையான சைவ விருந்து",
            items_en=[
                "Paneer Butter Masala",
                "Dal Makhani",
                "Veg Biryani",
                "Naan & Tandoori Roti",
                "Raita & Papad",
                "Gulab Jamun",
                "Welcome Drink"
            ],
            items_ta=[
                "பன்னீர் பட்டர் மசாலா",
                "டால் மக்கனி",
                "வெஜ் பிரியாணி",
                "நான் & தந்தூரி ரொட்டி",
                "ரைதா & பாப்பாட்",
                "குலாப் ஜாமூன்",
                "வெல்கம் டிரிங்க்"
            ],
            recommended_for=["casual", "corporate", "kitty"]
        ),
        "nonveg": MenuPack(
            key="nonveg",
            name_en="🍗 Non-Veg Pack",
            name_ta="🍗 அசைவ பேக்",
            price_per_person=499,
            description_en="Delicious chicken & mutton spread",
            description_ta="சுவையான சிக்கன் & மட்டன்",
            items_en=[
                "Chicken Tikka",
                "Mutton Curry",
                "Chicken Biryani",
                "Butter Naan",
                "Raita & Salad",
                "Ice Cream",
                "Welcome Drink"
            ],
            items_ta=[
                "சிக்கன் டிக்கா",
                "மட்டன் கறி",
                "சிக்கன் பிரியாணி",
                "பட்டர் நான்",
                "ரைதா & சாலட்",
                "ஐஸ் கிரீம்",
                "வெல்கம் டிரிங்க்"
            ],
            recommended_for=["party", "casual", "farewell"]
        ),
        "premium": MenuPack(
            key="premium",
            name_en="⭐ Premium Pack",
            name_ta="⭐ பிரீமியம் பேக்",
            price_per_person=749,
            description_en="Premium selection with live counters",
            description_ta="லைவ் கவுண்டர்களுடன் பிரீமியம்",
            items_en=[
                "Live Tandoor Counter",
                "Paneer & Chicken Starters",
                "Hyderabadi Dum Biryani",
                "Butter Chicken / Paneer",
                "Dal Tadka & Raita",
                "Assorted Breads",
                "Dessert Counter",
                "Mocktails"
            ],
            items_ta=[
                "லைவ் தந்தூர் கவுண்டர்",
                "பன்னீர் & சிக்கன் ஸ்டார்டர்ஸ்",
                "ஹைதராபாதி டம் பிரியாணி",
                "பட்டர் சிக்கன் / பன்னீர்",
                "டால் தட்கா & ரைதா",
                "அஸார்ட்டட் பிரெட்ஸ்",
                "டெஸர்ட் கவுண்டர்",
                "மாக்டெய்ல்ஸ்"
            ],
            recommended_for=["birthday", "anniversary", "corporate"]
        ),
        "deluxe": MenuPack(
            key="deluxe",
            name_en="👑 Deluxe Party Pack",
            name_ta="👑 டீலக்ஸ் பார்ட்டி பேக்",
            price_per_person=999,
            description_en="Grand celebration feast - all inclusive",
            description_ta="பெரிய கொண்டாட்ட விருந்து - அனைத்தும் உள்ளடக்கியது",
            items_en=[
                "Welcome Mocktail Counter",
                "Live Chaat & Tandoor",
                "10+ Starter Varieties",
                "Veg & Non-Veg Main Course",
                "Multiple Biryani Options",
                "Live Pasta Counter",
                "Dessert Buffet",
                "Special Paan Counter"
            ],
            items_ta=[
                "வெல்கம் மாக்டெய்ல் கவுண்டர்",
                "லைவ் சாட் & தந்தூர்",
                "10+ ஸ்டார்டர் வகைகள்",
                "வெஜ் & நான்-வெஜ் மெயின் கோர்ஸ்",
                "பல பிரியாணி ஆப்ஷன்ஸ்",
                "லைவ் பாஸ்தா கவுண்டர்",
                "டெஸர்ட் புஃபே",
                "ஸ்பெஷல் பான் கவுண்டர்"
            ],
            recommended_for=["wedding", "anniversary", "birthday"]
        )
    }
    
    # ===========================================
    # ADDONS
    # ===========================================
    
    ADDONS: Dict[str, Addon] = {
        "decoration": Addon(
            key="decoration",
            name_en="🎀 Table Decoration",
            name_ta="🎀 டேபிள் டெகரேஷன்",
            price=1500,
            description_en="Beautiful theme-based decoration",
            description_ta="அழகான தீம் டெகரேஷன்",
            recommended_for=["birthday", "anniversary", "romantic"]
        ),
        "cake": Addon(
            key="cake",
            name_en="🎂 Birthday Cake (1kg)",
            name_ta="🎂 பிறந்தநாள் கேக் (1kg)",
            price=800,
            description_en="Fresh cream cake with custom message",
            description_ta="கஸ்டம் மெசேஜ் கேக்",
            recommended_for=["birthday"]
        ),
        "photography": Addon(
            key="photography",
            name_en="📸 Photography",
            name_ta="📸 போட்டோகிராபி",
            price=2500,
            description_en="Professional photographer (2 hours)",
            description_ta="புரொபஷனல் போட்டோகிராபர் (2 மணி நேரம்)",
            recommended_for=["wedding", "anniversary", "birthday", "corporate"]
        ),
        "music_system": Addon(
            key="music_system",
            name_en="🎵 Music System",
            name_ta="🎵 மியூசிக் சிஸ்டம்",
            price=1000,
            description_en="Bluetooth speaker with mic",
            description_ta="மைக் உடன் ஸ்பீக்கர்",
            recommended_for=["party", "birthday", "farewell"]
        ),
        "dj": Addon(
            key="dj",
            name_en="🎧 DJ Setup",
            name_ta="🎧 DJ செட்அப்",
            price=5000,
            description_en="Professional DJ with lights",
            description_ta="லைட்ஸ் உடன் புரொபஷனல் DJ",
            recommended_for=["wedding", "party", "birthday"]
        ),
        "flowers": Addon(
            key="flowers",
            name_en="💐 Flower Arrangement",
            name_ta="💐 பூ அலங்காரம்",
            price=1200,
            description_en="Fresh flower bouquet & table pieces",
            description_ta="ஃப்ரெஷ் பூ புக்கே & டேபிள் பீஸ்",
            recommended_for=["anniversary", "romantic", "wedding"]
        ),
        "balloons": Addon(
            key="balloons",
            name_en="🎈 Balloon Decoration",
            name_ta="🎈 பலூன் டெகரேஷன்",
            price=800,
            description_en="Colorful balloon arch & bunches",
            description_ta="கலர்ஃபுல் பலூன் ஆர்ச்",
            recommended_for=["birthday", "kids_party"]
        ),
        "projector": Addon(
            key="projector",
            name_en="📽️ Projector & Screen",
            name_ta="📽️ ப்ரொஜெக்டர் & ஸ்கிரீன்",
            price=500,
            description_en="For presentations & slideshows",
            description_ta="பிரசன்டேஷன்ஸ் & ஸ்லைட்ஷோஸ்க்கு",
            recommended_for=["corporate"]
        )
    }
    
    # ===========================================
    # EVENT RECOMMENDATIONS
    # ===========================================
    
    EVENT_RECOMMENDATIONS = {
        "birthday": {
            "menu": "premium",
            "addons": ["decoration", "cake", "balloons", "music_system"],
            "message_en": "🎂 For birthday, I suggest Premium Pack with cake & decoration. Your guest will love it!",
            "message_ta": "🎂 Birthday-க்கு Premium Pack with cake & decoration suggest பண்றேன். உங்க guest-ஸ் love பண்ணுவாங்க!"
        },
        "anniversary": {
            "menu": "premium",
            "addons": ["decoration", "flowers", "photography"],
            "message_en": "💕 Anniversary special! Premium Pack with flowers & romantic decoration creates magic!",
            "message_ta": "💕 Anniversary special! Premium Pack with flowers & romantic decoration magic create பண்ணும்!"
        },
        "corporate": {
            "menu": "premium",
            "addons": ["projector"],
            "message_en": "💼 For corporate events, Premium Pack is perfect. Need projector for presentations?",
            "message_ta": "💼 Corporate events-க்கு Premium Pack perfect. Presentations-க்கு projector வேணுமா?"
        },
        "wedding": {
            "menu": "deluxe",
            "addons": ["decoration", "flowers", "photography", "music_system"],
            "message_en": "💒 Wedding calls for Deluxe Pack! Grand celebration deserves the best!",
            "message_ta": "💒 Wedding-க்கு Deluxe Pack! Grand celebration-க்கு best வேணும்!"
        },
        "party": {
            "menu": "nonveg",
            "addons": ["music_system", "decoration"],
            "message_en": "🎉 Party time! Non-Veg Pack with music will get everyone grooving!",
            "message_ta": "🎉 Party time! Non-Veg Pack with music-ல எல்லாரும் enjoy பண்ணுவாங்க!"
        },
        "casual": {
            "menu": "veg",
            "addons": [],
            "message_en": "Simple and tasty - our Veg Pack is perfect for casual dining!",
            "message_ta": "Simple & tasty - Veg Pack casual dining-க்கு perfect!"
        },
        "date": {
            "menu": "premium",
            "addons": ["decoration", "flowers"],
            "message_en": "💑 Romantic date! Premium Pack with candle-light setup. We'll make it special!",
            "message_ta": "💑 Romantic date! Premium Pack with candle-light setup. Special-ஆ arrange பண்றோம்!"
        },
        "farewell": {
            "menu": "nonveg",
            "addons": ["cake", "music_system"],
            "message_en": "Send-off in style! Non-Veg Pack with cake & music for memories!",
            "message_ta": "Style-ல send-off! Non-Veg Pack with cake & music - நல்ல memories-க்கு!"
        },
        "kitty": {
            "menu": "veg",
            "addons": ["decoration"],
            "message_en": "Ladies special! Our Veg Pack is a crowd favorite at kitty parties!",
            "message_ta": "Ladies special! Veg Pack kitty parties-ல crowd favorite!"
        }
    }
    
    # ===========================================
    # SEATING RECOMMENDATIONS
    # ===========================================
    
    @classmethod
    def get_seating_recommendation(cls, people: int, lang: str = "en") -> SeatingRecommendation:
        """
        Get seating recommendation based on guest count.
        Like a real waiter suggesting the best arrangement.
        """
        if people <= 6:
            return SeatingRecommendation(
                seating_type=SeatingType.TABLE,
                tables_needed=1,
                capacity=6,
                message_en=f"For {people} guests, I'll arrange a nice cozy table. Perfect for intimate dining! 🍽️",
                message_ta=f"{people} பேருக்கு ஒரு நல்ல table arrange பண்றேன். Intimate dining-க்கு perfect! 🍽️",
                layout_visual=cls._generate_table_visual(people, 1)
            )
        elif people <= 12:
            tables = 2
            return SeatingRecommendation(
                seating_type=SeatingType.TABLE,
                tables_needed=tables,
                capacity=12,
                message_en=f"For {people} guests, I'll set up {tables} tables side by side. Nice family-style seating!",
                message_ta=f"{people} பேருக்கு {tables} tables பக்கத்துல arrange பண்றேன். Family-style seating!",
                layout_visual=cls._generate_table_visual(people, tables)
            )
        elif people <= 20:
            tables = 4
            return SeatingRecommendation(
                seating_type=SeatingType.TABLE,
                tables_needed=tables,
                capacity=24,
                message_en=f"For {people} guests, {tables} tables in our main dining area. Comfortable & spacious!",
                message_ta=f"{people} பேருக்கு main dining area-ல {tables} tables. Comfortable & spacious!",
                layout_visual=cls._generate_table_visual(people, tables)
            )
        elif people <= 60:
            return SeatingRecommendation(
                seating_type=SeatingType.MINI_HALL,
                tables_needed=(people // 8) + 1,
                hall_name="Mini Banquet Hall",
                capacity=60,
                message_en=f"For {people} guests, I recommend our Mini Banquet Hall! Private space with buffet setup. 🏛️",
                message_ta=f"{people} பேருக்கு எங்க Mini Banquet Hall recommend பண்றேன்! Private space with buffet setup. 🏛️",
                layout_visual=cls._generate_hall_visual("mini", people)
            )
        else:
            return SeatingRecommendation(
                seating_type=SeatingType.BANQUET_HALL,
                tables_needed=(people // 10) + 1,
                hall_name="Grand Banquet Hall",
                capacity=200,
                message_en=f"Wow, {people} guests! Our Grand Banquet Hall is perfect for you! Full celebration mode! 🎉",
                message_ta=f"Wow, {people} பேர்! எங்க Grand Banquet Hall உங்களுக்கு perfect! Full celebration mode! 🎉",
                layout_visual=cls._generate_hall_visual("grand", people)
            )
    
    @staticmethod
    def _generate_table_visual(people: int, tables: int) -> str:
        """Generate ASCII visual of table layout."""
        if tables == 1:
            return f"""
    ╭─────────────╮
    │  🪑 🪑 🪑  │
    │ ╭─────────╮ │
    │ │  TABLE  │ │
    │ ╰─────────╯ │
    │  🪑 🪑 🪑  │
    ╰─────────────╯
     {people} Guests
"""
        elif tables == 2:
            return f"""
    ╭─────────╮ ╭─────────╮
    │ 🪑T1 🪑│ │ 🪑T2 🪑│
    ╰─────────╯ ╰─────────╯
         {people} Guests
"""
        else:
            return f"""
    ╭────╮ ╭────╮
    │ T1 │ │ T2 │
    ╰────╯ ╰────╯
    ╭────╮ ╭────╮
    │ T3 │ │ T4 │
    ╰────╯ ╰────╯
     {tables} Tables | {people} Guests
"""
    
    @staticmethod
    def _generate_hall_visual(hall_type: str, people: int) -> str:
        """Generate ASCII visual of hall layout."""
        if hall_type == "mini":
            return f"""
    ╔═══════════════════════╗
    ║   MINI BANQUET HALL   ║
    ║  ┌───┐ ┌───┐ ┌───┐   ║
    ║  │ T │ │ T │ │ T │   ║
    ║  └───┘ └───┘ └───┘   ║
    ║  ┌───┐ ┌───┐ ┌───┐   ║
    ║  │ T │ │ T │ │ T │   ║
    ║  └───┘ └───┘ └───┘   ║
    ║    🍽️ BUFFET AREA    ║
    ╚═══════════════════════╝
       Capacity: 60 | Guests: {people}
"""
        else:
            return f"""
    ╔═══════════════════════════════╗
    ║     GRAND BANQUET HALL        ║
    ║  ┌───┐ ┌───┐ ┌───┐ ┌───┐     ║
    ║  │ T │ │ T │ │ T │ │ T │     ║
    ║  └───┘ └───┘ └───┘ └───┘     ║
    ║  ┌───┐ ┌───┐ ┌───┐ ┌───┐     ║
    ║  │ T │ │ T │ │ T │ │ T │     ║
    ║  └───┘ └───┘ └───┘ └───┘     ║
    ║  ┌───┐ ┌───┐ ┌───┐ ┌───┐     ║
    ║  │ T │ │ T │ │ T │ │ T │     ║
    ║  └───┘ └───┘ └───┘ └───┘     ║
    ║       🍽️ BUFFET COUNTER       ║
    ║         🎤 STAGE 🎤           ║
    ╚═══════════════════════════════╝
       Capacity: 200 | Guests: {people}
"""
    
    # ===========================================
    # MENU DISPLAY FORMATTERS
    # ===========================================
    
    @classmethod
    def format_menu_list(cls, lang: str = "en") -> str:
        """Format all menu packs for display."""
        lines = []
        for key, pack in cls.MENU_PACKS.items():
            name = pack.name_en if lang == "en" else pack.name_ta
            desc = pack.description_en if lang == "en" else pack.description_ta
            lines.append(f"{name}")
            lines.append(f"   ₹{pack.price_per_person}/person - {desc}")
            lines.append("")
        
        if lang == "en":
            lines.append("Just say the pack name (veg/nonveg/premium/deluxe) to select!")
        else:
            lines.append("Pack name சொல்லுங்க (veg/nonveg/premium/deluxe) select பண்ண!")
        
        return "\n".join(lines)
    
    @classmethod
    def format_addon_list(cls, lang: str = "en") -> str:
        """Format all addons for display."""
        lines = []
        for key, addon in cls.ADDONS.items():
            name = addon.name_en if lang == "en" else addon.name_ta
            lines.append(f"{name} - ₹{addon.price}")
        
        if lang == "en":
            lines.append("\nSay the addon names you want, or 'none' to skip!")
        else:
            lines.append("\nவேண்டிய addon names சொல்லுங்க, அல்லது 'none' skip பண்ண!")
        
        return "\n".join(lines)
    
    @classmethod
    def get_menu_pack(cls, key: str) -> Optional[MenuPack]:
        """Get menu pack by key."""
        return cls.MENU_PACKS.get(key.lower())
    
    @classmethod
    def get_addon(cls, key: str) -> Optional[Addon]:
        """Get addon by key."""
        return cls.ADDONS.get(key.lower())
    
    @classmethod
    def get_event_recommendation(cls, event_type: str, lang: str = "en") -> dict:
        """Get recommendation for an event type."""
        rec = cls.EVENT_RECOMMENDATIONS.get(event_type.lower(), cls.EVENT_RECOMMENDATIONS["casual"])
        return {
            "menu": rec["menu"],
            "addons": rec["addons"],
            "message": rec[f"message_{lang}"] if f"message_{lang}" in rec else rec["message_en"]
        }
    
    @classmethod
    def calculate_cost(cls, people: int, menu_key: str, addon_keys: List[str]) -> Tuple[int, int, int]:
        """
        Calculate total cost.
        Returns (base_cost, addon_cost, total_cost).
        """
        pack = cls.MENU_PACKS.get(menu_key)
        if not pack:
            return (0, 0, 0)
        
        base_cost = pack.price_per_person * people
        addon_cost = sum(cls.ADDONS[k].price for k in addon_keys if k in cls.ADDONS)
        
        return (base_cost, addon_cost, base_cost + addon_cost)
