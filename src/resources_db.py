#!/usr/bin/env python3
"""
Resources database for different languages
"""

from typing import Dict, Optional

class ResourcesDatabase:
    """Database of language learning resources"""

    def __init__(self):
        self.alphabets = self._init_alphabets()
        self.resources = self._init_resources()

    def get_alphabet(self, language_code: str) -> Optional[str]:
        """Get alphabet section for a language"""
        return self.alphabets.get(language_code)

    def get_resources(self, language_code: str, native_lang: str = "en") -> Optional[str]:
        """Get resources for a language"""
        return self.resources.get(language_code, self.resources.get('_template'))

    def _init_alphabets(self) -> Dict[str, str]:
        """Initialize alphabet sections for non-Latin scripts"""
        return {
            'ar': """<a name="alphabet"></a>
## 🔤 Arabic Alphabet (‫)األبجدية العربية‬

28 letters, written right-to-left, with different forms per position.

| Letter | Name | Sound | Notes |
|--------|------|-------|-------|
| ا | alif | ā | Long 'a' |
| ب | bā' | b | Like 'b' in 'bat' |
| ت | tā' | t | Like 't' in 'top' |
| ث | thā' | th | Like 'th' in 'think' |
| ج | jīm | j | Like 'j' in 'jam' |
| ح | ḥā' | ḥ | Breathy 'h' from throat |
| خ | khā' | kh | Like 'ch' in 'Bach' |

[See full alphabet in course materials]

**Resources:**
- Duolingo Arabic Alphabet course
- Write It! Arabic app (iOS/Android)
- YouTube: "Learn Arabic Alphabet" by ArabicPod101

---""",
            'ja': """<a name="alphabet"></a>
## 🔤 Japanese Writing Systems

Japanese uses 3 scripts: Hiragana, Katakana, and Kanji.

### Hiragana (46 characters)
Used for native Japanese words

### Katakana (46 characters)
Used for foreign words

### Kanji (2000+ common)
Chinese characters

**Resources:**
- Duolingo Japanese
- WaniKani for Kanji
- Tofugu's Hiragana/Katakana guides

---""",
            'zh': """<a name="alphabet"></a>
## 🔤 Chinese Characters (汉字)

Mandarin Chinese uses logographic characters.

**Common Radicals:**
- 人 (rén) - person
- 口 (kǒu) - mouth
- 手 (shǒu) - hand

**Tone Marks:**
- First tone: ā (high level)
- Second tone: á (rising)
- Third tone: ǎ (falling-rising)
- Fourth tone: à (falling)

---""",
            'ru': """<a name="alphabet"></a>
## 🔤 Russian Alphabet (Кириллица)

33 letters in Cyrillic script.

| Letter | Sound | Example |
|--------|-------|---------|
| А а | a | like 'a' in 'father' |
| Б б | b | like 'b' in 'book' |
| В в | v | like 'v' in 'very' |
| Г г | g | like 'g' in 'go' |

[Full alphabet chart in materials]

---""",
        }

    def _init_resources(self) -> Dict[str, str]:
        """Initialize resources for different languages"""
        return {
            'ar': self._get_arabic_resources(),
            'ja': self._get_japanese_resources(),
            'zh': self._get_chinese_resources(),
            'es': self._get_spanish_resources(),
            'fr': self._get_french_resources(),
            'de': self._get_german_resources(),
            'ru': self._get_russian_resources(),
            '_template': self._get_template_resources()
        }

    def _get_arabic_resources(self) -> str:
        return """<a name="resources"></a>
## 🌟 Arabic Learning Resources

### 📱 Mobile Apps
- **Duolingo Arabic** - Gamified learning
- **Memrise** - Vocabulary with native speakers
- **Busuu** - Complete course A1-B2
- **Write It! Arabic** - Letter writing practice
- **Drops** - 5-min daily vocabulary

### 🎥 YouTube Channels
- Learn Arabic with Maha
- ArabicPod101
- Easy Arabic (street interviews)
- Learn Arabic with Safaa

### 🌐 Websites
- ArabicOnline.eu - Free comprehensive course
- Madinah Arabic - Free textbooks (PDF)
- Al Jazeera Learning - News by level

### 📚 Textbooks
- Al-Kitaab series (Georgetown)
- Mastering Arabic (Palgrave)
- Arabic for Nerds series

### 💬 Communities
- r/learn_arabic (Reddit)
- Discord: Arabic Learning Server
- iTalki - 1-on-1 tutors

---"""

    def _get_template_resources(self) -> str:
        """Generic template for any language"""
        return """<a name="resources"></a>
## 🌟 Language Learning Resources

### 📱 Recommended Apps
- **Duolingo** - Free gamified learning
- **Memrise** - Vocabulary with mnemonics
- **Busuu** - Structured courses
- **Anki** - Spaced repetition flashcards

### 🎥 YouTube
- Search: "[Language] for beginners"
- Easy Languages channel
- Language-specific channels

### 🌐 Websites
- iTalki - Find tutors
- Tandem - Language exchange
- LingQ - Reading + listening

### 📚 Study Tips
1. Practice daily (15-30 min minimum)
2. Use spaced repetition
3. Immerse yourself (music, movies, podcasts)
4. Speak from day 1 (language exchange)
5. Join online communities

---"""

    def _get_japanese_resources(self) -> str:
        return """<a name="resources"></a>
## 🌟 Japanese Learning Resources

### 📱 Apps
- Duolingo Japanese
- WaniKani (Kanji mastery)
- Bunpro (Grammar SRS)
- HelloTalk (Language exchange)

### 🎥 YouTube
- Japanese Ammo with Misa
- JapanesePod101
- Comprehensible Japanese

### 📚 Resources
- Tae Kim's Grammar Guide
- Genki textbooks
- NHK News Web Easy

---"""

    def _get_spanish_resources(self) -> str:
        return """<a name="resources"></a>
## 🌟 Spanish Learning Resources

### 📱 Apps
- Duolingo Spanish
- Babbel
- SpanishDict dictionary

### 🎥 YouTube
- Butterfly Spanish
- SpanishPod101
- Easy Spanish

### 📺 Netflix
- Money Heist (La Casa de Papel)
- Élite
- Narcos

---"""

    def _get_french_resources(self) -> str:
        return """<a name="resources"></a>
## 🌟 French Learning Resources

### 📱 Apps
- Duolingo French
- Babbel
- TV5Monde

### 🎥 YouTube
- FrenchPod101
- Easy French
- Français avec Pierre

---"""

    def _get_german_resources(self) -> str:
        return """<a name="resources"></a>
## 🌟 German Learning Resources

### 📱 Apps
- Duolingo German
- Babbel
- DW Learn German

### 🎥 YouTube
- Easy German
- GermanPod101
- Learn German with Anja

---"""

    def _get_russian_resources(self) -> str:
        return """<a name="resources"></a>
## 🌟 Russian Learning Resources

### 📱 Apps
- Duolingo Russian
- RussianPod101
- Memrise Russian

### 🎥 YouTube
- Russian with Max
- Easy Russian
- Be Fluent in Russian

---"""

    def _get_chinese_resources(self) -> str:
        return """<a name="resources"></a>
## 🌟 Chinese Learning Resources

### 📱 Apps
- Duolingo Chinese
- HelloChinese
- Pleco (dictionary)

### 🎥 YouTube
- ChinesePod101
- Learn Chinese with ChineseFor.Us
- Mandarin Corner

---"""
