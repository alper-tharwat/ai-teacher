"""
🔊 محرك صوت الأستاذ - مع كاش لتوفير الوقت
"""

import edge_tts
import asyncio
import tempfile
import os
import base64
import hashlib
import streamlit as st
from modules.auth.outputs_manager import save_output, get_cached_output


TEACHER_VOICES = {
    "العربية (مصري - شاكر)": "ar-EG-ShakirNeural",
    "العربية (مصري - سلمى)": "ar-EG-SalmaNeural",
    "العربية (سعودي - حامد)": "ar-SA-HamedNeural",
    "العربية (سعودي - زرياب)": "ar-SA-ZariyahNeural",
    "English (US - Guy)": "en-US-GuyNeural",
    "English (US - Jenny)": "en-US-JennyNeural",
    "English (UK - Ryan)": "en-GB-RyanNeural",
    "Français": "fr-FR-HenriNeural",
    "Deutsch": "de-DE-ConradNeural",
    "Español": "es-ES-AlvaroNeural",
    "Türkçe": "tr-TR-AhmetNeural",
}


def _generate_text_hash(text: str) -> str:
    """حساب hash للنص لتمييزه في الكاش"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()[:16]


async def _generate_async(text: str, voice: str, rate: str = "+0%"):
    """توليد الصوت"""
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_path = temp_file.name
    temp_file.close()
    
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(temp_path)
    
    return temp_path


def generate_teacher_voice(text: str, voice_name: str = "العربية (مصري - شاكر)", speed: str = "عادي") -> dict:
    """
    توليد صوت الأستاذ - مع كاش
    
    Returns:
        {
            "audio_base64": str,
            "success": bool,
            "duration": float,
            "from_cache": bool
        }
    """
    
    # ============ فحص الكاش الأول ============
    current_file_id = st.session_state.get('current_file_id')
    
    if current_file_id and text:
        text_hash = _generate_text_hash(text)
        cache_settings = {
            'text_hash': text_hash,
            'voice': voice_name,
            'speed': speed
        }
        
        cached_audio = get_cached_output(
            file_id=current_file_id,
            output_type='teacher_voice_audio',
            settings=cache_settings
        )
        
        if cached_audio and isinstance(cached_audio, dict):
            audio_base64 = cached_audio.get('audio_base64')
            if audio_base64:
                return {
                    "audio_base64": audio_base64,
                    "duration": cached_audio.get('duration', 0),
                    "success": True,
                    "from_cache": True
                }
    
    # ============ توليد جديد ============
    voice = TEACHER_VOICES.get(voice_name, "ar-EG-ShakirNeural")
    
    speed_map = {
        "بطيء جداً": "-30%",
        "بطيء": "-15%",
        "عادي": "+0%",
        "سريع": "+15%",
        "سريع جداً": "+30%"
    }
    rate = speed_map.get(speed, "+0%")
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_path = loop.run_until_complete(
            _generate_async(text, voice, rate)
        )
        loop.close()
        
        # قراءة الصوت
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        
        # حساب المدة التقريبية
        word_count = len(text.split())
        duration = (word_count / 150) * 60
        
        # تنظيف الملف المؤقت
        try:
            os.remove(audio_path)
        except:
            pass
        
        # ============ حفظ في الكاش ============
        if current_file_id and text:
            text_hash = _generate_text_hash(text)
            cache_settings = {
                'text_hash': text_hash,
                'voice': voice_name,
                'speed': speed
            }
            
            save_output(
                file_id=current_file_id,
                output_type='teacher_voice_audio',
                content={
                    'audio_base64': audio_base64,
                    'duration': duration,
                    'text_preview': text[:100]
                },
                settings=cache_settings
            )
        
        return {
            "audio_base64": audio_base64,
            "duration": duration,
            "success": True,
            "from_cache": False
        }
    
    except Exception as e:
        return {
            "audio_base64": None,
            "duration": 0,
            "success": False,
            "from_cache": False,
            "error": str(e)
        }


def get_available_voices() -> dict:
    return TEACHER_VOICES


# للتوافق مع الكود القديم
def generate_teacher_voice_synced(text, voice_name="العربية (مصري - شاكر)", speed="عادي"):
    result = generate_teacher_voice(text, voice_name, speed)
    return {
        "audio_base64": result.get("audio_base64"),
        "word_timings": [],
        "total_duration": result.get("duration", 0) * 1000,
        "text": text,
        "success": result.get("success", False),
        "from_cache": result.get("from_cache", False),
        "error": result.get("error", "")
    }


def cleanup_audio(audio_path):
    try:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
    except:
        pass