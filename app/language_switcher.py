"""
Language Switcher for Server Sundharam Bot.
Handles bilingual support (English + Tamil).

Author: Server Sundharam Dev Team
Version: 2.0
"""

import re
from typing import Optional, Tuple
from .models import Language


class LanguageSwitcher:
    """
    Manages language detection and switching between English and Tamil.
    Provides bilingual response selection.
    """
    
    # Language switch trigger words
    TAMIL_TRIGGERS = ['tamil', 'தமிழ்', 'tamizh', 'thamizh']
    ENGLISH_TRIGGERS = ['english', 'eng', 'inglish', 'english please']
    
    # Tamil indicators in text
    TAMIL_UNICODE_PATTERN = re.compile(r'[\u0B80-\u0BFF]')
    TAMIL_TRANSLITERATION = [
        'vanakkam', 'nandri', 'sari', 'illa', 'iruku', 'panna',
        'venum', 'enna', 'eppo', 'enga', 'yen', 'appa', 'amma',
        'romba', 'nalla', 'konjam', 'paaru', 'sollu', 'kodu',
        'vaa', 'poda', 'podi', 'macha', 'machaa', 'da', 'di'
    ]
    
    @classmethod
    def detect_switch_request(cls, text: str) -> Optional[str]:
        """
        Detect if user wants to switch language.
        Returns 'ta' for Tamil, 'en' for English, None if no switch requested.
        """
        text_lower = text.lower().strip()
        
        # Check for Tamil switch
        for trigger in cls.TAMIL_TRIGGERS:
            if trigger in text_lower:
                # Ensure it's a language switch request, not just mentioning the word
                words = text_lower.split()
                if len(words) <= 3 or trigger in ['தமிழ்']:
                    return 'ta'
        
        # Check for English switch
        for trigger in cls.ENGLISH_TRIGGERS:
            if trigger in text_lower:
                words = text_lower.split()
                if len(words) <= 3:
                    return 'en'
        
        return None
    
    @classmethod
    def detect_language_from_text(cls, text: str) -> Language:
        """
        Detect the language of input text based on characters and words.
        """
        # Check for Tamil Unicode characters
        if cls.TAMIL_UNICODE_PATTERN.search(text):
            return Language.TAMIL
        
        # Check for Tamil transliteration words
        text_lower = text.lower()
        tamil_word_count = sum(1 for word in cls.TAMIL_TRANSLITERATION if word in text_lower)
        
        if tamil_word_count >= 1:
            return Language.TAMIL
        
        return Language.ENGLISH
    
    @classmethod
    def get_switch_confirmation(cls, new_lang: str) -> str:
        """
        Get confirmation message when switching language.
        """
        if new_lang == 'ta':
            return "சரி சார்! இனிமேல் தமிழில் பேசலாம் 😊 என்ன service வேணும்?"
        else:
            return "Sure sir! Let's continue in English 😊 How can I help you?"
    
    @classmethod
    def get_text_by_lang(cls, texts: dict, lang: str) -> str:
        """
        Get text from a bilingual dictionary based on language.
        Falls back to English if Tamil not available.
        """
        return texts.get(lang, texts.get('en', ''))
    
    @classmethod
    def format_bilingual(cls, en_text: str, ta_text: str, lang: str) -> str:
        """
        Return appropriate text based on current language.
        """
        return ta_text if lang == 'ta' else en_text
