"""
💾 Outputs Manager - حفظ وجلب المخرجات (ملخصات، امتحانات، إلخ)
"""

import streamlit as st
import hashlib
import json
from datetime import datetime
from modules.auth.supabase_client import get_supabase_client
from modules.auth.auth_manager import get_current_user


# أنواع المخرجات المدعومة
OUTPUT_TYPES = {
    'summary': '📝 ملخص',
    'explanation': '💡 شرح',
    'quiz': '📋 امتحان',
    'flashcards': '🎴 بطاقات',
    'mindmap': '🧠 خريطة ذهنية',
    'translation': '🌍 ترجمة',
    'analysis': '🔍 تحليل',
    'terms': '📖 مصطلحات',
    'smart_teacher_lesson': '🎭 درس الأستاذ الذكي',
    'teacher_voice_audio': '🔊 صوت الأستاذ',
}


def generate_settings_hash(settings: dict) -> str:
    """
    حساب hash للإعدادات للتمييز بين الإعدادات المختلفة
    
    مثال:
    - ملخص ذكي ≠ ملخص مختصر ≠ ملخص مفصل
    - شرح مبتدئ ≠ شرح متقدم
    - امتحان 5 أسئلة ≠ امتحان 10 أسئلة
    """
    try:
        # نشيل أي مفاتيح داخلية لو موجودة
        clean_settings = {k: v for k, v in settings.items() if not k.startswith('_')}
        settings_str = json.dumps(clean_settings, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(settings_str.encode('utf-8')).hexdigest()[:10]
    except:
        return "default"


# ============================================
# 💾 الكاش الشخصي (file_outputs)
# ============================================

def save_output(file_id: str, output_type: str, content, settings: dict = None) -> dict:
    """
    حفظ مخرج جديد (كاش شخصي)
    """
    try:
        client = get_supabase_client()
        user_info = get_current_user()
        
        if not client or not user_info["logged_in"]:
            return {
                "success": False,
                "message": "❌ لازم تسجل دخول"
            }
        
        if not file_id:
            return {
                "success": False,
                "message": "❌ مفيش ملف محدد"
            }
        
        if output_type not in OUTPUT_TYPES:
            return {
                "success": False,
                "message": f"❌ نوع غير معروف: {output_type}"
            }
        
        # تحويل المحتوى لـ JSON
        if isinstance(content, str):
            content_data = {"text": content}
        elif isinstance(content, (dict, list)):
            content_data = content
        else:
            content_data = {"text": str(content)}
        
        # حساب hash للإعدادات
        settings = settings or {}
        settings_hash = generate_settings_hash(settings)
        
        # نضيف الـ hash للـ settings عشان نقدر نلاقيه
        settings_with_hash = dict(settings)
        settings_with_hash['_hash'] = settings_hash
        
        # التحقق من وجود نفس المخرج بنفس الإعدادات
        existing = client.table("file_outputs") \
            .select("*") \
            .eq("file_id", file_id) \
            .eq("user_id", user_info["user_id"]) \
            .eq("output_type", output_type) \
            .execute()
        
        # نشوف لو في واحد بنفس الإعدادات
        if existing.data:
            for item in existing.data:
                existing_settings = item.get("settings", {}) or {}
                if existing_settings.get("_hash") == settings_hash:
                    # تحديث الموجود
                    client.table("file_outputs") \
                        .update({
                            "content": content_data,
                            "created_at": datetime.now().isoformat()
                        }) \
                        .eq("id", item["id"]) \
                        .execute()
                    
                    return {
                        "success": True,
                        "output_id": item["id"],
                        "message": "✅ تم تحديث المخرج",
                        "is_update": True
                    }
        
        # حفظ جديد
        output_data = {
            "file_id": file_id,
            "user_id": user_info["user_id"],
            "output_type": output_type,
            "content": content_data,
            "settings": settings_with_hash,
            "created_at": datetime.now().isoformat(),
            "tokens_used": 0
        }
        
        response = client.table("file_outputs").insert(output_data).execute()
        
        if response.data:
            return {
                "success": True,
                "output_id": response.data[0]["id"],
                "message": "✅ تم الحفظ",
                "is_update": False
            }
        
        return {
            "success": False,
            "message": "❌ فشل الحفظ"
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ خطأ: {str(e)}"
        }


def get_cached_output(file_id: str, output_type: str, settings: dict = None):
    """
    جلب مخرج محفوظ بنفس الإعدادات (كاش شخصي)
    """
    try:
        client = get_supabase_client()
        user_info = get_current_user()
        
        if not client or not user_info["logged_in"] or not file_id:
            return None
        
        # حساب hash للإعدادات
        settings = settings or {}
        target_hash = generate_settings_hash(settings)
        
        # جلب كل المخرجات من نفس النوع
        response = client.table("file_outputs") \
            .select("*") \
            .eq("file_id", file_id) \
            .eq("user_id", user_info["user_id"]) \
            .eq("output_type", output_type) \
            .order("created_at", desc=True) \
            .execute()
        
        if not response.data:
            return None

        # ندور على المخرج بنفس الإعدادات
        for item in response.data:
            item_settings = item.get("settings", {}) or {}
            if item_settings.get("_hash") == target_hash:
                content = item.get("content", {})
                
                # لو المحتوى نص بسيط (محفوظ كـ {"text": "..."})
                if isinstance(content, dict) and "text" in content:
                    keys = [k for k in content.keys() if not k.startswith('_')]
                    if len(keys) == 1 and keys[0] == "text":
                        return content["text"]
                
                # لو المحتوى dict أو list
                return content
        
        return None
    
    except Exception as e:
        print(f"خطأ في جلب الكاش: {e}")
        return None


def get_all_outputs_for_file(file_id: str) -> dict:
    """
    جلب كل المخرجات المحفوظة لملف معين
    """
    try:
        client = get_supabase_client()
        user_info = get_current_user()
        
        if not client or not user_info["logged_in"] or not file_id:
            return {}
        
        response = client.table("file_outputs") \
            .select("output_type") \
            .eq("file_id", file_id) \
            .eq("user_id", user_info["user_id"]) \
            .execute()
        
        if not response.data:
            return {}
        
        outputs = {}
        for item in response.data:
            output_type = item.get("output_type")
            if output_type:
                outputs[output_type] = True
        
        return outputs
    
    except Exception as e:
        return {}


def delete_output(output_id: str) -> dict:
    """حذف مخرج معين"""
    try:
        client = get_supabase_client()
        user_info = get_current_user()
        
        if not client or not user_info["logged_in"]:
            return {"success": False}
        
        client.table("file_outputs") \
            .delete() \
            .eq("id", output_id) \
            .eq("user_id", user_info["user_id"]) \
            .execute()
        
        return {"success": True, "message": "✅ تم الحذف"}
    
    except Exception as e:
        return {"success": False, "message": str(e)}


def delete_all_outputs_for_file(file_id: str) -> dict:
    """حذف كل المخرجات لملف معين"""
    try:
        client = get_supabase_client()
        user_info = get_current_user()
        
        if not client or not user_info["logged_in"]:
            return {"success": False}
        
        client.table("file_outputs") \
            .delete() \
            .eq("file_id", file_id) \
            .eq("user_id", user_info["user_id"]) \
            .execute()
        
        return {"success": True, "message": "✅ تم حذف كل المخرجات"}
    
    except Exception as e:
        return {"success": False, "message": str(e)}


# ============================================
# 💾 دوال للمكتبة الذكية (كاش عام)
# ============================================

def save_lesson_output(lesson_id: str, output_type: str, content, settings: dict = None) -> dict:
    """
    حفظ مخرج لدرس من المكتبة الذكية (كاش عام لكل المستخدمين)
    """
    try:
        client = get_supabase_client()
        
        if not client:
            return {"success": False, "message": "❌ مفيش اتصال"}
        
        # تحويل المحتوى
        if isinstance(content, str):
            content_data = {"text": content}
        elif isinstance(content, (dict, list)):
            content_data = content
        else:
            content_data = {"text": str(content)}
        
        # حساب hash للإعدادات
        settings = settings or {}
        settings_hash = generate_settings_hash(settings)
        
        # نضيف الـ hash للـ settings
        settings_with_hash = dict(settings)
        settings_with_hash['_hash'] = settings_hash
        
        # نشوف لو موجود بنفس الإعدادات
        existing = client.table("lesson_outputs") \
            .select("*") \
            .eq("lesson_id", lesson_id) \
            .eq("output_type", output_type) \
            .execute()
        
        # مطابقة الـ settings بالـ hash
        if existing.data:
            for item in existing.data:
                existing_settings = item.get("settings", {}) or {}
                if existing_settings.get("_hash") == settings_hash:
                    # تحديث الموجود
                    client.table("lesson_outputs") \
                        .update({"content": content_data}) \
                        .eq("id", item["id"]) \
                        .execute()
                    
                    return {
                        "success": True,
                        "output_id": item["id"],
                        "message": "✅ تم التحديث",
                        "is_update": True
                    }
        
        # حفظ جديد
        output_data = {
            "lesson_id": lesson_id,
            "output_type": output_type,
            "content": content_data,
            "settings": settings_with_hash,
            "views_count": 0
        }
        
        response = client.table("lesson_outputs").insert(output_data).execute()
        
        if response.data:
            return {
                "success": True,
                "output_id": response.data[0]["id"],
                "message": "✅ تم الحفظ",
                "is_update": False
            }
        
        return {"success": False, "message": "❌ فشل"}
    
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


def get_lesson_output_cached(lesson_id: str, output_type: str, settings: dict = None):
    """
    جلب مخرج محفوظ لدرس من المكتبة الذكية (بالـ hash)
    """
    try:
        client = get_supabase_client()
        
        if not client or not lesson_id:
            return None
        
        # حساب hash للإعدادات
        settings = settings or {}
        target_hash = generate_settings_hash(settings)
        
        response = client.table("lesson_outputs") \
            .select("*") \
            .eq("lesson_id", lesson_id) \
            .eq("output_type", output_type) \
            .execute()
        
        if not response.data:
            return None
        
        # ندور على المخرج بنفس الـ hash
        for item in response.data:
            item_settings = item.get("settings", {}) or {}
            if item_settings.get("_hash") == target_hash:
                content = item.get("content", {})
                
                # زيادة عدد المشاهدات
                try:
                    client.table("lesson_outputs") \
                        .update({"views_count": item.get("views_count", 0) + 1}) \
                        .eq("id", item["id"]) \
                        .execute()
                except:
                    pass
                
                # لو نص بسيط
                if isinstance(content, dict) and "text" in content:
                    keys = [k for k in content.keys() if not k.startswith('_')]
                    if len(keys) == 1 and keys[0] == "text":
                        return content["text"]
                
                return content
        
        return None
    
    except Exception as e:
        print(f"خطأ في جلب الكاش العام: {e}")
        return None


def is_lesson_from_library() -> bool:
    """
    معرفة إذا كان الملف الحالي من المكتبة الذكية أم لا
    """
    return st.session_state.get('current_lesson_id') is not None


def get_current_lesson_id() -> str:
    """
    جلب معرف الدرس الحالي (لو من المكتبة الذكية)
    """
    return st.session_state.get('current_lesson_id')