"""
🎓 المعلم الذكي - AI Teacher v3.5 Pro
ملف الإعدادات الشامل - دعم Streamlit Cloud Secrets
"""

import os
from pathlib import Path

# محاولة استيراد Streamlit (للـ Secrets)
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False


# ═══════════════════════════════════════════════════════════
# 🔐 قراءة المفاتيح من Streamlit Secrets أو من الكود
# ═══════════════════════════════════════════════════════════

def get_secret(key_name, default=None):
    """
    قراءة المفاتيح من Streamlit Secrets أولاً
    لو مش موجودة، ترجع القيمة الافتراضية
    """
    if STREAMLIT_AVAILABLE:
        try:
            if hasattr(st, 'secrets') and key_name in st.secrets:
                value = st.secrets[key_name]
                # لو كانت list ترجعها زي ما هي
                if isinstance(value, list):
                    return value
                # لو كانت string واحدة، حولها لـ list
                if isinstance(value, str):
                    return [value]
                return list(value)
        except Exception:
            pass
    return default if default is not None else []


# ═══════════════════════════════════════════════════════════
# 📁 المسارات الأساسية
# ═══════════════════════════════════════════════════════════
BASE_DIR = Path(__file__).parent
UTILS_DIR = BASE_DIR / "utils"
DATABASE_DIR = BASE_DIR / "database"
ASSETS_DIR = BASE_DIR / "assets"
TEMP_DIR = BASE_DIR / "temp"
AUDIO_CACHE_DIR = TEMP_DIR / "audio_cache"

# إنشاء المجلدات لو مش موجودة
for directory in [DATABASE_DIR, ASSETS_DIR, TEMP_DIR, AUDIO_CACHE_DIR]:
    directory.mkdir(exist_ok=True, parents=True)


# ═══════════════════════════════════════════════════════════
# 🔑 مفاتيح المحركات (من Secrets أولاً، ثم محلياً)
# ═══════════════════════════════════════════════════════════

# 🟢 Google Gemini
GEMINI_API_KEYS = get_secret("GEMINI_KEYS", [])

# 🟣 Groq
GROQ_API_KEYS = get_secret("GROQ_KEYS", [])

# 🔵 Cerebras
CEREBRAS_API_KEYS = get_secret("CEREBRAS_KEYS", [])

# 🟡 OpenRouter
OPENROUTER_API_KEYS = get_secret("OPENROUTER_KEYS", [])

# 🟠 Cohere
COHERE_API_KEYS = get_secret("COHERE_KEYS", [])

# 🔴 Mistral AI
MISTRAL_API_KEYS = get_secret("MISTRAL_KEYS", [])

# ⚪ Together AI
TOGETHER_API_KEYS = get_secret("TOGETHER_KEYS", [])


# ═══════════════════════════════════════════════════════════
# 🤖 إعدادات المحركات
# ═══════════════════════════════════════════════════════════

ENGINES_CONFIG = {
    "gemini": {
        "name": "Google Gemini",
        "icon": "🟢",
        "model": "gemini-2.5-flash",
        "keys": GEMINI_API_KEYS,
        "daily_limit": 1500,
        "quality": 9,
        "speed": 7,
        "arabic_quality": 10,
        "enabled": True,
    },
    "cerebras": {
        "name": "Cerebras (الأسرع)",
        "icon": "⚡",
        "model": "gpt-oss-120b",
        "keys": CEREBRAS_API_KEYS,
        "daily_limit": 1000000,
        "quality": 8,
        "speed": 10,
        "arabic_quality": 7,
        "enabled": True,
    },
    "openrouter": {
        "name": "OpenRouter (Claude/GPT)",
        "icon": "🧠",
        "model": "anthropic/claude-3.5-sonnet",
        "keys": OPENROUTER_API_KEYS,
        "daily_limit": 50,
        "quality": 10,
        "speed": 7,
        "arabic_quality": 10,
        "enabled": True,
        "backup_model": "deepseek/deepseek-chat",
    },
    "groq": {
        "name": "Groq",
        "icon": "🟣",
        "model": "llama-3.3-70b-versatile",
        "keys": GROQ_API_KEYS,
        "daily_limit": 14400,
        "quality": 7,
        "speed": 10,
        "arabic_quality": 6,
        "enabled": True,
    },
    "cohere": {
        "name": "Cohere",
        "icon": "🟠",
        "model": "command-r-plus",
        "keys": COHERE_API_KEYS,
        "daily_limit": 1000,
        "quality": 8,
        "speed": 7,
        "arabic_quality": 8,
        "enabled": True,
    },
    "mistral": {
        "name": "Mistral AI",
        "icon": "🔴",
        "model": "mistral-large-latest",
        "keys": MISTRAL_API_KEYS,
        "daily_limit": 999999,
        "quality": 8,
        "speed": 7,
        "arabic_quality": 7,
        "enabled": True,
    },
    "together": {
        "name": "Together AI",
        "icon": "⚪",
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "keys": TOGETHER_API_KEYS,
        "daily_limit": 5000,
        "quality": 8,
        "speed": 8,
        "arabic_quality": 7,
        "enabled": True,
    },
}


# ═══════════════════════════════════════════════════════════
# 🎯 توزيع المهام (كل مهمة بأحسن محرك)
# ═══════════════════════════════════════════════════════════

TASK_ENGINE_MAP = {
    "quiz_generation": {
        "primary": "gemini",
        "fallback": ["openrouter", "cerebras", "cohere", "groq"],
    },
    "quiz_grading": {
        "primary": "gemini",
        "fallback": ["openrouter", "cohere", "cerebras"],
    },
    "summarization": {
        "primary": "gemini",
        "fallback": ["openrouter", "cohere", "cerebras", "groq"],
    },
    "detailed_summary": {
        "primary": "gemini",
        "fallback": ["openrouter", "cohere"],
    },
    "explanation": {
        "primary": "gemini",
        "fallback": ["openrouter", "cerebras", "groq"],
    },
    "deep_explanation": {
        "primary": "gemini",
        "fallback": ["openrouter", "cohere"],
    },
    "chat": {
        "primary": "cerebras",
        "fallback": ["groq", "gemini", "mistral"],
    },
    "quick_answer": {
        "primary": "cerebras",
        "fallback": ["groq", "mistral"],
    },
    "translation": {
        "primary": "gemini",
        "fallback": ["cohere", "openrouter", "groq"],
    },
    "avatar_speech": {
        "primary": "gemini",
        "fallback": ["openrouter", "cohere"],
    },
    "deep_analysis": {
        "primary": "gemini",
        "fallback": ["openrouter", "cohere", "mistral"],
    },
    "extraction": {
        "primary": "gemini",
        "fallback": ["openrouter", "cerebras", "groq"],
    },
    "default": {
        "primary": "gemini",
        "fallback": ["cerebras", "groq", "openrouter", "cohere", "mistral"],
    },
}


# ═══════════════════════════════════════════════════════════
# ⚙️ الإعدادات العامة
# ═══════════════════════════════════════════════════════════

DEFAULT_MODE = "hybrid_pro"
DEFAULT_ENGINE = "gemini"

GENERATION_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 4000,
    "top_p": 0.9,
}

RETRY_CONFIG = {
    "max_retries": 3,
    "retry_delay": 2,
    "switch_engine_on_fail": True,
}


# ═══════════════════════════════════════════════════════════
# 🎙️ إعدادات الصوت
# ═══════════════════════════════════════════════════════════

VOICE_CONFIG = {
    "default_engine": "edge",
    "default_voice": "ar-EG-ShakirNeural",
    "default_speed": "normal",
    "cache_enabled": True,
}

AVAILABLE_VOICES = {
    "شاكر (مصري ذكر)": "ar-EG-ShakirNeural",
    "سلمى (مصري أنثى)": "ar-EG-SalmaNeural",
    "حامد (سعودي ذكر)": "ar-SA-HamedNeural",
    "زارية (سعودي أنثى)": "ar-SA-ZariyahNeural",
    "Guy (إنجليزي ذكر)": "en-US-GuyNeural",
    "Jenny (إنجليزي أنثى)": "en-US-JennyNeural",
}


# ═══════════════════════════════════════════════════════════
# 🎭 إعدادات الأفاتار
# ═══════════════════════════════════════════════════════════

AVATAR_CONFIG = {
    "default_character": "ahmed",
    "default_background": "classroom",
    "default_type": "css",
}


# ═══════════════════════════════════════════════════════════
# 📁 إعدادات الملفات
# ═══════════════════════════════════════════════════════════

SUPPORTED_FILE_TYPES = {
    "pdf": [".pdf"],
    "word": [".docx", ".doc"],
    "powerpoint": [".pptx", ".ppt"],
    "excel": [".xlsx", ".xls"],
    "text": [".txt", ".md"],
    "csv": [".csv"],
    "image": [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"],
}

MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024

# مسار Tesseract (للنظام المحلي فقط)
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ═══════════════════════════════════════════════════════════
# 🌐 إعدادات الواجهة
# ═══════════════════════════════════════════════════════════

APP_CONFIG = {
    "title": "🎓 المعلم الذكي",
    "version": "v3.5",
    "icon": "🎓",
    "layout": "wide",
    "theme": "light",
    "language": "ar",
}


# ═══════════════════════════════════════════════════════════
# 🔄 التوافق مع الكود القديم
# ═══════════════════════════════════════════════════════════

ALL_EXTENSIONS = []
for ext_list in SUPPORTED_FILE_TYPES.values():
    ALL_EXTENSIONS.extend([ext.replace(".", "") for ext in ext_list])

GEMINI_MODEL = ENGINES_CONFIG["gemini"]["model"]
GROQ_MODEL = ENGINES_CONFIG["groq"]["model"]
AI_TEMPERATURE = GENERATION_CONFIG["temperature"]
MAX_INPUT_LENGTH = 30000
MAX_OUTPUT_LENGTH = 4000

EXPLANATION_LEVELS = {
    "child": {
        "name": "طفل",
        "icon": "👶",
        "prompt": "اشرح كإنك بتكلم طفل عنده 8 سنين، بكلمات بسيطة جداً وأمثلة من الكرتون",
        "description": "شرح بسيط جداً بكلمات سهلة وأمثلة من الكرتون",
    },
    "student": {
        "name": "طالب ثانوي",
        "icon": "🎓",
        "prompt": "اشرح كإنك بتكلم طالب ثانوي، بأمثلة من الحياة اليومية",
        "description": "شرح متوسط مع أمثلة من الحياة اليومية",
    },
    "university": {
        "name": "جامعي",
        "icon": "📚",
        "prompt": "اشرح بمستوى أكاديمي مع التفاصيل والمصطلحات العلمية",
        "description": "شرح أكاديمي مع مصطلحات علمية وتفاصيل",
    },
    "expert": {
        "name": "متخصص",
        "icon": "🔬",
        "prompt": "اشرح بمستوى متخصص مع التحليل العميق والمصطلحات التقنية",
        "description": "شرح عميق ومتقدم للمتخصصين",
    },
}

SUPPORTED_LANGUAGES = {
    "en": "English",
    "ar": "العربية",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "tr": "Turkish",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "hi": "Hindi",
}


# ═══════════════════════════════════════════════════════════
# ✅ دوال التحقق والمساعدة
# ═══════════════════════════════════════════════════════════

def check_config():
    """التحقق من صحة الإعدادات والمفاتيح"""
    issues = []
    active_engines = []

    for engine_id, engine_config in ENGINES_CONFIG.items():
        if not engine_config["enabled"]:
            continue

        valid_keys = [
            k for k in engine_config["keys"]
            if k and not k.startswith("XXXXXXXX") and "XXXXXXXX" not in k
            and not k.startswith("ضع_")
        ]

        if valid_keys:
            active_engines.append({
                "id": engine_id,
                "name": engine_config["name"],
                "icon": engine_config["icon"],
                "keys_count": len(valid_keys),
                "daily_limit": engine_config["daily_limit"],
            })
        else:
            issues.append(f"⚠️ {engine_config['icon']} {engine_config['name']}: مفيش مفاتيح صحيحة")

    if not active_engines:
        issues.append("❌ مفيش أي محرك مفعّل! ضع مفاتيحك في config.py أو Secrets")

    return {
        "status": "ok" if active_engines else "error",
        "active_engines": active_engines,
        "total_engines": len(active_engines),
        "issues": issues,
    }


def get_active_engines():
    """إرجاع قائمة المحركات المفعّلة فقط"""
    active = {}
    for engine_id, config in ENGINES_CONFIG.items():
        if not config["enabled"]:
            continue
        valid_keys = [
            k for k in config["keys"]
            if k and "XXXXXXXX" not in k and not k.startswith("ضع_")
        ]
        if valid_keys:
            active[engine_id] = {
                **config,
                "keys": valid_keys,
            }
    return active


def get_engine_for_task(task_name):
    """إرجاع أحسن محرك لمهمة معينة"""
    task_config = TASK_ENGINE_MAP.get(task_name, TASK_ENGINE_MAP["default"])
    active_engines = get_active_engines()

    primary = task_config["primary"]
    if primary in active_engines:
        return {
            "primary": primary,
            "fallback": [e for e in task_config["fallback"] if e in active_engines],
        }

    for fallback_engine in task_config["fallback"]:
        if fallback_engine in active_engines:
            return {
                "primary": fallback_engine,
                "fallback": [e for e in task_config["fallback"] if e in active_engines and e != fallback_engine],
            }

    if active_engines:
        first_available = list(active_engines.keys())[0]
        return {
            "primary": first_available,
            "fallback": [e for e in active_engines.keys() if e != first_available],
        }

    return None


def get_system_info():
    """معلومات النظام للعرض"""
    active = get_active_engines()
    total_daily_capacity = sum(
        e["daily_limit"] * len(e["keys"])
        for e in active.values()
    )

    return {
        "version": APP_CONFIG["version"],
        "mode": DEFAULT_MODE,
        "active_engines_count": len(active),
        "total_daily_capacity": total_daily_capacity,
        "engines": active,
    }


# ═══════════════════════════════════════════════════════════
# 🎯 Config Class للتوافق مع الكود القديم
# ═══════════════════════════════════════════════════════════

class Config:
    """Class للتوافق مع الكود القديم"""
    GEMINI_API_KEYS = GEMINI_API_KEYS
    GROQ_API_KEYS = GROQ_API_KEYS
    CEREBRAS_API_KEYS = CEREBRAS_API_KEYS
    OPENROUTER_API_KEYS = OPENROUTER_API_KEYS
    COHERE_API_KEYS = COHERE_API_KEYS
    MISTRAL_API_KEYS = MISTRAL_API_KEYS
    TOGETHER_API_KEYS = TOGETHER_API_KEYS

    DEFAULT_ENGINE = DEFAULT_ENGINE
    DEFAULT_MODE = DEFAULT_MODE
    ENGINES_CONFIG = ENGINES_CONFIG
    TASK_ENGINE_MAP = TASK_ENGINE_MAP
    GENERATION_CONFIG = GENERATION_CONFIG
    RETRY_CONFIG = RETRY_CONFIG

    BASE_DIR = BASE_DIR
    DATABASE_DIR = DATABASE_DIR
    TEMP_DIR = TEMP_DIR
    AUDIO_CACHE_DIR = AUDIO_CACHE_DIR

    VOICE_CONFIG = VOICE_CONFIG
    AVAILABLE_VOICES = AVAILABLE_VOICES
    AVATAR_CONFIG = AVATAR_CONFIG
    SUPPORTED_FILE_TYPES = SUPPORTED_FILE_TYPES
    MAX_FILE_SIZE_MB = MAX_FILE_SIZE_MB
    MAX_FILE_SIZE = MAX_FILE_SIZE
    TESSERACT_PATH = TESSERACT_PATH
    APP_CONFIG = APP_CONFIG

    ALL_EXTENSIONS = ALL_EXTENSIONS
    GEMINI_MODEL = GEMINI_MODEL
    GROQ_MODEL = GROQ_MODEL
    AI_TEMPERATURE = AI_TEMPERATURE
    MAX_INPUT_LENGTH = MAX_INPUT_LENGTH
    MAX_OUTPUT_LENGTH = MAX_OUTPUT_LENGTH
    EXPLANATION_LEVELS = EXPLANATION_LEVELS
    SUPPORTED_LANGUAGES = SUPPORTED_LANGUAGES


# ═══════════════════════════════════════════════════════════
# 🚀 تشغيل التحقق عند الاستيراد
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🎓 المعلم الذكي - فحص الإعدادات")
    print("=" * 60)

    info = check_config()
    print(f"\n✅ الحالة: {info['status']}")
    print(f"🤖 المحركات النشطة: {info['total_engines']}")

    if info['active_engines']:
        print("\n📊 المحركات المفعّلة:")
        for engine in info['active_engines']:
            print(f"  {engine['icon']} {engine['name']}")
            print(f"     ├─ المفاتيح: {engine['keys_count']}")
            print(f"     └─ الحد اليومي: {engine['daily_limit']:,}")

    if info['issues']:
        print("\n⚠️  تحذيرات:")
        for issue in info['issues']:
            print(f"  {issue}")

    system_info = get_system_info()
    print(f"\n📈 السعة اليومية الكلية: {system_info['total_daily_capacity']:,} طلب")
    print("=" * 60)