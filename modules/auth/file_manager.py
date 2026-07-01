"""
📂 File Manager - إدارة ملفات المستخدم في Supabase
"""

import streamlit as st
import hashlib
from datetime import datetime
from modules.auth.supabase_client import get_supabase_client
from modules.auth.auth_manager import get_current_user


def calculate_file_hash(text: str) -> str:
    """حساب hash للملف للتحقق من التكرار"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def save_file(file_name: str, file_type: str, extracted_text: str, 
              file_size: int = 0, metadata: dict = None) -> dict:
    """
    حفظ ملف جديد في قاعدة البيانات
    
    Args:
        file_name: اسم الملف
        file_type: نوع الملف (pdf, audio, etc)
        extracted_text: النص المستخرج
        file_size: حجم الملف
        metadata: معلومات إضافية
    
    Returns:
        dict: {success, file_id, message, is_duplicate}
    """
    try:
        client = get_supabase_client()
        user_info = get_current_user()
        
        if not client or not user_info["logged_in"]:
            return {
                "success": False,
                "message": "❌ لازم تسجل دخول الأول"
            }
        
        user_id = user_info["user_id"]
        file_hash = calculate_file_hash(extracted_text)
        
        # التحقق من التكرار
        existing = client.table("user_files") \
            .select("id, file_name") \
            .eq("user_id", user_id) \
            .eq("file_hash", file_hash) \
            .execute()
        
        if existing.data and len(existing.data) > 0:
            existing_file = existing.data[0]
            
            # تحديث آخر وصول
            client.table("user_files") \
                .update({"last_accessed": datetime.now().isoformat()}) \
                .eq("id", existing_file["id"]) \
                .execute()
            
            return {
                "success": True,
                "file_id": existing_file["id"],
                "message": f"📁 الملف موجود بالفعل! ({existing_file['file_name']})",
                "is_duplicate": True
            }
        
        # حفظ الملف الجديد
        file_data = {
            "user_id": user_id,
            "file_name": file_name,
            "file_type": file_type,
            "file_size": file_size,
            "file_hash": file_hash,
            "extracted_text": extracted_text,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat()
        }
        
        response = client.table("user_files").insert(file_data).execute()
        
        if response.data and len(response.data) > 0:
            return {
                "success": True,
                "file_id": response.data[0]["id"],
                "message": "✅ تم حفظ الملف بنجاح!",
                "is_duplicate": False
            }
        
        return {
            "success": False,
            "message": "❌ فشل حفظ الملف"
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ خطأ: {str(e)}"
        }


def get_user_files(limit: int = 50) -> dict:
    """
    جلب كل ملفات المستخدم الحالي
    """
    try:
        client = get_supabase_client()
        user_info = get_current_user()
        
        if not client or not user_info["logged_in"]:
            return {"success": False, "files": [], "message": "غير مسجّل"}
        
        user_id = user_info["user_id"]
        
        response = client.table("user_files") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("last_accessed", desc=True) \
            .limit(limit) \
            .execute()
        
        return {
            "success": True,
            "files": response.data if response.data else [],
            "count": len(response.data) if response.data else 0
        }
    
    except Exception as e:
        return {
            "success": False,
            "files": [],
            "message": f"❌ خطأ: {str(e)}"
        }


def get_file_by_id(file_id: str) -> dict:
    """جلب ملف معين بالـ ID"""
    try:
        client = get_supabase_client()
        user_info = get_current_user()
        
        if not client or not user_info["logged_in"]:
            return {"success": False, "message": "غير مسجّل"}
        
        response = client.table("user_files") \
            .select("*") \
            .eq("id", file_id) \
            .eq("user_id", user_info["user_id"]) \
            .execute()
        
        if response.data and len(response.data) > 0:
            # تحديث آخر وصول
            client.table("user_files") \
                .update({"last_accessed": datetime.now().isoformat()}) \
                .eq("id", file_id) \
                .execute()
            
            return {
                "success": True,
                "file": response.data[0]
            }
        
        return {
            "success": False,
            "message": "❌ الملف غير موجود"
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ خطأ: {str(e)}"
        }


def delete_file(file_id: str) -> dict:
    """حذف ملف"""
    try:
        client = get_supabase_client()
        user_info = get_current_user()
        
        if not client or not user_info["logged_in"]:
            return {"success": False, "message": "غير مسجّل"}
        
        # حذف الملف (والمخرجات هتتحذف تلقائياً بـ CASCADE)
        client.table("user_files") \
            .delete() \
            .eq("id", file_id) \
            .eq("user_id", user_info["user_id"]) \
            .execute()
        
        return {
            "success": True,
            "message": "✅ تم حذف الملف"
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ خطأ: {str(e)}"
        }


def toggle_favorite(file_id: str) -> dict:
    """تبديل المفضلة"""
    try:
        client = get_supabase_client()
        user_info = get_current_user()
        
        if not client or not user_info["logged_in"]:
            return {"success": False}
        
        # جلب الحالة الحالية
        current = client.table("user_files") \
            .select("is_favorite") \
            .eq("id", file_id) \
            .eq("user_id", user_info["user_id"]) \
            .execute()
        
        if current.data:
            new_status = not current.data[0].get("is_favorite", False)
            
            client.table("user_files") \
                .update({"is_favorite": new_status}) \
                .eq("id", file_id) \
                .execute()
            
            return {
                "success": True,
                "is_favorite": new_status
            }
        
        return {"success": False}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_files_stats() -> dict:
    """إحصائيات ملفات المستخدم"""
    try:
        client = get_supabase_client()
        user_info = get_current_user()
        
        if not client or not user_info["logged_in"]:
            return {"total": 0, "favorites": 0, "total_size": 0}
        
        user_id = user_info["user_id"]
        
        # كل الملفات
        all_files = client.table("user_files") \
            .select("id, is_favorite, file_size") \
            .eq("user_id", user_id) \
            .execute()
        
        if not all_files.data:
            return {"total": 0, "favorites": 0, "total_size": 0}
        
        total = len(all_files.data)
        favorites = sum(1 for f in all_files.data if f.get("is_favorite"))
        total_size = sum(f.get("file_size", 0) or 0 for f in all_files.data)
        
        return {
            "total": total,
            "favorites": favorites,
            "total_size": total_size
        }
    
    except Exception as e:
        return {"total": 0, "favorites": 0, "total_size": 0, "error": str(e)}