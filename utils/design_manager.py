"""
🎨 مدير التصميم - قراءة وحفظ الإعدادات
"""
import json
import os
from pathlib import Path


DESIGN_FILE = Path(__file__).parent.parent / "design_settings.json"


# الإعدادات الافتراضية (لو الملف مش موجود)
DEFAULT_SETTINGS = {
    "colors": {
        "primary": "#667eea",
        "secondary": "#764ba2",
        "success": "#11998e",
        "danger": "#dc3545",
        "warning": "#ff9800",
        "info": "#2196f3",
        "background": "#ffffff",
        "text_primary": "#2c3e50",
        "text_secondary": "#7f8c8d"
    },
    "sizes": {
        "header_size": 32,
        "title_size": 24,
        "text_size": 15,
        "button_padding": 12,
        "card_padding": 20,
        "border_radius": 12
    },
    "spacing": {
        "gap_small": 5,
        "gap_medium": 15,
        "gap_large": 25
    },
    "effects": {
        "shadow_enabled": True,
        "shadow_intensity": 0.1,
        "animations_enabled": True,
        "gradient_enabled": True
    },
    "fonts": {
        "family": "Cairo",
        "weight_normal": 400,
        "weight_bold": 700
    }
}


def load_settings():
    """تحميل الإعدادات من الملف"""
    try:
        if DESIGN_FILE.exists():
            with open(DESIGN_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # لو الملف مش موجود، اعمله بالإعدادات الافتراضية
            save_settings(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS
    except Exception as e:
        print(f"⚠️ خطأ في تحميل الإعدادات: {e}")
        return DEFAULT_SETTINGS


def save_settings(settings):
    """حفظ الإعدادات في الملف"""
    try:
        with open(DESIGN_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"⚠️ خطأ في حفظ الإعدادات: {e}")
        return False


def reset_settings():
    """إرجاع الإعدادات للافتراضي"""
    return save_settings(DEFAULT_SETTINGS)


def get_setting(category, key, default=None):
    """جلب إعداد معين"""
    settings = load_settings()
    return settings.get(category, {}).get(key, default)


def update_setting(category, key, value):
    """تحديث إعداد معين"""
    settings = load_settings()
    if category not in settings:
        settings[category] = {}
    settings[category][key] = value
    return save_settings(settings)