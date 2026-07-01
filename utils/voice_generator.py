"""
🎙️ مولد الصوت العربي المتقدم (الإصدار 2.0)
مع محسّن النص الذكي وتحسينات النطق
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tempfile
import hashlib
from gtts import gTTS
from config import Config
from utils.text_enhancer import TextEnhancer


class VoiceGenerator:
    """
    مولد الصوت الذكي (محسّن)
    
    المحركات المدعومة:
    1. gTTS (مجاني - Google Text-to-Speech)
    2. Edge-TTS (مجاني - أصوات أحلى)
    
    التحسينات الجديدة:
    ✨ محسّن النص الذكي
    ✨ تصحيح نطق الكلمات الشائعة
    ✨ تحويل الأرقام لحروف
    ✨ إضافة وقفات طبيعية
    ✨ سرعات مختلفة (بطيء/طبيعي/سريع)
    ✨ أساليب نطق متعددة
    """
    
    # الأصوات المتاحة في Edge-TTS
    VOICES = {
        "ar": {
            "male_1": {
                "id": "ar-EG-ShakirNeural",
                "name": "🧑 شاكر (مصري)",
                "gender": "male",
                "rate": "+0%",
                "pitch": "+0Hz"
            },
            "female_1": {
                "id": "ar-EG-SalmaNeural",
                "name": "👩 سلمى (مصرية)",
                "gender": "female",
                "rate": "+0%",
                "pitch": "+0Hz"
            },
            "male_2": {
                "id": "ar-SA-HamedNeural",
                "name": "🧑 حامد (سعودي)",
                "gender": "male",
                "rate": "+0%",
                "pitch": "+0Hz"
            },
            "female_2": {
                "id": "ar-SA-ZariyahNeural",
                "name": "👩 زارية (سعودية)",
                "gender": "female",
                "rate": "+0%",
                "pitch": "+0Hz"
            },
        },
        "en": {
            "male_1": {
                "id": "en-US-GuyNeural",
                "name": "👨 Guy (US)",
                "gender": "male",
                "rate": "+0%",
                "pitch": "+0Hz"
            },
            "female_1": {
                "id": "en-US-JennyNeural",
                "name": "👩 Jenny (US)",
                "gender": "female",
                "rate": "+0%",
                "pitch": "+0Hz"
            },
        }
    }
    
    # أنماط النطق
    SPEECH_STYLES = {
        "natural": {
            "name": "🗣️ طبيعي",
            "rate": "+0%",
            "description": "نطق طبيعي وسلس"
        },
        "slow": {
            "name": "🐢 بطيء (للشرح)",
            "rate": "-15%",
            "description": "بطيء وواضح للفهم"
        },
        "very_slow": {
            "name": "🐌 بطيء جداً (للمبتدئين)",
            "rate": "-25%",
            "description": "بطيء جداً لتعلم اللغة"
        },
        "fast": {
            "name": "🐰 سريع",
            "rate": "+15%",
            "description": "سريع للمراجعة"
        },
        "storytelling": {
            "name": "📖 حكاية",
            "rate": "-5%",
            "description": "نمط الحكي والقصص"
        },
        "energetic": {
            "name": "⚡ حماسي",
            "rate": "+10%",
            "description": "حماسي ونشيط"
        }
    }
    
    def __init__(self, method="edge", cache_dir=None, ai_engine=None):
        """
        Args:
            method: 'gtts' أو 'edge'
            cache_dir: مسار حفظ الملفات
            ai_engine: محرك AI لتحسين النص (اختياري)
        """
        self.method = method
        self.cache_dir = cache_dir or os.path.join(Config.TEMP_DIR, "audio_cache")
        
        # إنشاء مجلد الـ cache
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        
        # التحقق من Edge-TTS
        self.edge_available = self._check_edge_tts()
        
        # محسّن النص
        self.text_enhancer = TextEnhancer(ai_engine=ai_engine)
        self.ai_engine = ai_engine
    
    def _check_edge_tts(self):
        """التحقق من توفر edge-tts"""
        try:
            import edge_tts
            return True
        except ImportError:
            return False
    
    # ============================================
    # 🎤 توليد الصوت الرئيسي (محسّن)
    # ============================================
    
    def generate(self, text, language="ar", voice=None, 
                 style="natural", enhance_text=True, use_ai_enhance=False, 
                 use_cache=True):
        """
        توليد ملف صوتي من نص (محسّن)
        
        Args:
            text: النص المراد تحويله
            language: 'ar' أو 'en'
            voice: اسم الصوت
            style: نمط النطق (natural/slow/fast/storytelling/energetic)
            enhance_text: تحسين النص قبل النطق (موصى به)
            use_ai_enhance: تحسين متقدم بالـ AI (أبطأ بس أحسن)
            use_cache: استخدم الـ cache
        
        Returns:
            dict: نتيجة العملية
        """
        if not text or not text.strip():
            return {
                'success': False,
                'audio_path': None,
                'error': '⚠️ النص فاضي'
            }
        
        # 🎯 تحسين النص (التحسين الجديد!)
        original_text = text
        if enhance_text:
            if use_ai_enhance and self.ai_engine:
                text = self.text_enhancer.smart_enhance(text)
            else:
                text = self.text_enhancer.prepare_for_speech(text, style=style)
        
        # 📦 إنشاء اسم الملف
        cache_key = self._get_cache_key(text, language, voice, style)
        audio_path = os.path.join(self.cache_dir, f"{cache_key}.mp3")
        
        # 🔍 التحقق من الـ cache
        if use_cache and os.path.exists(audio_path):
            return {
                'success': True,
                'audio_path': audio_path,
                'cached': True,
                'method': 'cache',
                'enhanced_text': text,
                'original_text': original_text
            }
        
        # 🎙️ اختيار المحرك
        if self.method == "edge" and self.edge_available:
            result = self._generate_edge(text, language, voice, style, audio_path)
        else:
            result = self._generate_gtts(text, language, style, audio_path)
        
        # إضافة معلومات إضافية
        result['enhanced_text'] = text
        result['original_text'] = original_text
        
        return result
    
    # ============================================
    # 🔵 Edge-TTS مع التحسينات
    # ============================================
    
    def _generate_edge(self, text, language, voice, style, output_path):
        """توليد الصوت باستخدام Edge-TTS مع التحسينات"""
        try:
            import edge_tts
            import asyncio
            
            # اختيار الصوت
            voice_id = self._get_voice_id(language, voice)
            
            # اختيار السرعة من النمط
            rate = self.SPEECH_STYLES.get(style, self.SPEECH_STYLES['natural'])['rate']
            
            # دالة async مع SSML للتحكم الأفضل
            async def generate_audio():
                communicate = edge_tts.Communicate(
                    text=text,
                    voice=voice_id,
                    rate=rate,
                    pitch="+0Hz",
                    volume="+0%"
                )
                await communicate.save(output_path)
            
            # تشغيل
            asyncio.run(generate_audio())
            
            return {
                'success': True,
                'audio_path': output_path,
                'cached': False,
                'method': 'edge',
                'voice': voice_id,
                'style': style
            }
            
        except Exception as e:
            print(f"Edge-TTS error: {e}")
            # Fallback لـ gTTS
            return self._generate_gtts(text, language, style, output_path)
    
    # ============================================
    # 🟢 gTTS مع التحسينات
    # ============================================
    
    def _generate_gtts(self, text, language, style, output_path):
        """توليد الصوت باستخدام Google TTS"""
        try:
            # السرعة
            is_slow = style in ['slow', 'very_slow']
            
            # تقسيم النص
            chunks = self._split_text(text, max_length=500)
            
            if len(chunks) == 1:
                tts = gTTS(text=text, lang=language, slow=is_slow)
                tts.save(output_path)
            else:
                from pydub import AudioSegment
                combined = AudioSegment.empty()
                
                for i, chunk in enumerate(chunks):
                    temp_file = os.path.join(self.cache_dir, f"_temp_{i}.mp3")
                    tts = gTTS(text=chunk, lang=language, slow=is_slow)
                    tts.save(temp_file)
                    
                    audio = AudioSegment.from_mp3(temp_file)
                    combined += audio
                    
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                
                combined.export(output_path, format="mp3")
            
            return {
                'success': True,
                'audio_path': output_path,
                'cached': False,
                'method': 'gtts',
                'chunks': len(chunks),
                'style': style
            }
            
        except Exception as e:
            return {
                'success': False,
                'audio_path': None,
                'error': f"خطأ في gTTS: {str(e)}"
            }
    
    # ============================================
    # 🎯 دوال جاهزة محسّنة
    # ============================================
    
    def speak_lesson(self, text, voice="male_1"):
        """نطق درس - بطيء وواضح"""
        return self.generate(
            text, 
            language="ar",
            voice=voice,
            style="slow",
            enhance_text=True
        )
    
    def speak_story(self, text, voice="female_1"):
        """نطق قصة - أسلوب حكي"""
        return self.generate(
            text,
            language="ar",
            voice=voice,
            style="storytelling",
            enhance_text=True
        )
    
    def speak_normal(self, text, voice="male_1"):
        """نطق عادي"""
        return self.generate(
            text,
            language="ar",
            voice=voice,
            style="natural",
            enhance_text=True
        )
    
    def speak_smart(self, text, voice="male_1"):
        """نطق ذكي بتحسين AI (الأحسن)"""
        return self.generate(
            text,
            language="ar",
            voice=voice,
            style="natural",
            enhance_text=True,
            use_ai_enhance=True
        )
    
    # ============================================
    # 🔧 أدوات مساعدة
    # ============================================
    
    def _split_text(self, text, max_length=500):
        """تقسيم النص لأجزاء منطقية"""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        current = ""
        
        # تقسيم بالجمل
        sentences = []
        for delimiter in ['. ', '! ', '? ', '؟ ', '! ', '\n']:
            if delimiter in text:
                temp = text.split(delimiter)
                sentences = [s + delimiter.strip() for s in temp if s]
                break
        
        if not sentences:
            sentences = [text]
        
        for sentence in sentences:
            if len(current) + len(sentence) <= max_length:
                current += sentence + " "
            else:
                if current:
                    chunks.append(current.strip())
                current = sentence + " "
        
        if current:
            chunks.append(current.strip())
        
        return chunks if chunks else [text]
    
    def _get_cache_key(self, text, language, voice, style):
        """توليد مفتاح فريد للنص"""
        content = f"{text}_{language}_{voice}_{style}_{self.method}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:16]
    
    def _get_voice_id(self, language, voice_key):
        """الحصول على ID الصوت"""
        lang_voices = self.VOICES.get(language, self.VOICES["ar"])
        
        if voice_key and voice_key in lang_voices:
            return lang_voices[voice_key]["id"]
        
        default_key = list(lang_voices.keys())[0]
        return lang_voices[default_key]["id"]
    
    def get_available_voices(self, language="ar"):
        """قائمة الأصوات المتاحة"""
        return self.VOICES.get(language, {})
    
    def get_available_styles(self):
        """قائمة أنماط النطق المتاحة"""
        return self.SPEECH_STYLES
    
    # ============================================
    # 🧹 إدارة الـ Cache
    # ============================================
    
    def clear_cache(self):
        """مسح الـ cache"""
        try:
            count = 0
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.mp3'):
                    os.remove(os.path.join(self.cache_dir, filename))
                    count += 1
            return {
                'success': True,
                'deleted': count,
                'message': f'✅ تم حذف {count} ملف'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_cache_size(self):
        """حساب حجم الـ cache"""
        try:
            total = 0
            count = 0
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.mp3'):
                    filepath = os.path.join(self.cache_dir, filename)
                    total += os.path.getsize(filepath)
                    count += 1
            
            size_mb = total / (1024 * 1024)
            
            return {
                'files': count,
                'size_bytes': total,
                'size_mb': round(size_mb, 2),
                'size_readable': f"{size_mb:.2f} MB"
            }
        except Exception as e:
            return {'error': str(e)}
    
    def test_voice(self):
        """اختبار سريع"""
        test_text = "أهلاً بيكم! أنا المعلم الذكي، علشان نبدأ الشرح، خلينا نتعرف على المحتوى."
        result = self.generate(test_text, language="ar", style="natural")
        
        if result['success']:
            return True, f"✅ المحرك شغال! الملف: {result['audio_path']}"
        else:
            return False, f"❌ {result.get('error', 'خطأ')}"