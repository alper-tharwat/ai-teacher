"""
📚 Smart Library Manager - مدير المكتبة التعليمية الذكية
"""

import streamlit as st
from datetime import datetime
from modules.auth.supabase_client import get_supabase_client


# ============================================
# 🎓 المراحل التعليمية
# ============================================

def get_all_stages():
    """جلب كل المراحل التعليمية"""
    try:
        client = get_supabase_client()
        if not client:
            return []
        
        response = client.table("educational_stages") \
            .select("*") \
            .eq("is_active", True) \
            .order("display_order") \
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"خطأ في جلب المراحل: {e}")
        return []


def create_stage(name: str, description: str = "", icon: str = "🎓", order: int = 0) -> dict:
    """إنشاء مرحلة تعليمية جديدة"""
    try:
        client = get_supabase_client()
        if not client:
            return {"success": False, "message": "❌ خطأ في الاتصال"}
        
        data = {
            "name": name,
            "description": description,
            "icon": icon,
            "display_order": order,
            "is_active": True
        }
        
        response = client.table("educational_stages").insert(data).execute()
        
        if response.data:
            return {
                "success": True,
                "message": "✅ تم إنشاء المرحلة بنجاح",
                "stage_id": response.data[0]["id"]
            }
        return {"success": False, "message": "❌ فشل الإنشاء"}
    
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


def delete_stage(stage_id: str) -> dict:
    """حذف مرحلة تعليمية"""
    try:
        client = get_supabase_client()
        if not client:
            return {"success": False}
        
        client.table("educational_stages") \
            .delete() \
            .eq("id", stage_id) \
            .execute()
        
        return {"success": True, "message": "✅ تم الحذف"}
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


# ============================================
# 📖 الصفوف
# ============================================

def get_grades_by_stage(stage_id: str):
    """جلب صفوف مرحلة معينة"""
    try:
        client = get_supabase_client()
        if not client:
            return []
        
        response = client.table("grades") \
            .select("*") \
            .eq("stage_id", stage_id) \
            .eq("is_active", True) \
            .order("display_order") \
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"خطأ في جلب الصفوف: {e}")
        return []


def create_grade(stage_id: str, name: str, grade_number: int = 0, icon: str = "📖", order: int = 0) -> dict:
    """إنشاء صف جديد"""
    try:
        client = get_supabase_client()
        if not client:
            return {"success": False, "message": "❌ خطأ في الاتصال"}
        
        data = {
            "stage_id": stage_id,
            "name": name,
            "grade_number": grade_number,
            "icon": icon,
            "display_order": order,
            "is_active": True
        }
        
        response = client.table("grades").insert(data).execute()
        
        if response.data:
            return {
                "success": True,
                "message": "✅ تم إنشاء الصف",
                "grade_id": response.data[0]["id"]
            }
        return {"success": False, "message": "❌ فشل"}
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


def delete_grade(grade_id: str) -> dict:
    """حذف صف"""
    try:
        client = get_supabase_client()
        if not client:
            return {"success": False}
        
        client.table("grades").delete().eq("id", grade_id).execute()
        return {"success": True, "message": "✅ تم الحذف"}
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


# ============================================
# 📚 المواد
# ============================================

def get_subjects_by_grade(grade_id: str):
    """جلب مواد صف معين"""
    try:
        client = get_supabase_client()
        if not client:
            return []
        
        response = client.table("subjects") \
            .select("*") \
            .eq("grade_id", grade_id) \
            .eq("is_active", True) \
            .order("display_order") \
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"خطأ في جلب المواد: {e}")
        return []


def create_subject(grade_id: str, name: str, description: str = "", 
                   icon: str = "📚", color: str = "#667eea", order: int = 0) -> dict:
    """إنشاء مادة جديدة"""
    try:
        client = get_supabase_client()
        if not client:
            return {"success": False, "message": "❌ خطأ في الاتصال"}
        
        data = {
            "grade_id": grade_id,
            "name": name,
            "description": description,
            "icon": icon,
            "color": color,
            "display_order": order,
            "is_active": True
        }
        
        response = client.table("subjects").insert(data).execute()
        
        if response.data:
            return {
                "success": True,
                "message": "✅ تم إنشاء المادة",
                "subject_id": response.data[0]["id"]
            }
        return {"success": False, "message": "❌ فشل"}
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


def delete_subject(subject_id: str) -> dict:
    """حذف مادة"""
    try:
        client = get_supabase_client()
        if not client:
            return {"success": False}
        
        client.table("subjects").delete().eq("id", subject_id).execute()
        return {"success": True, "message": "✅ تم الحذف"}
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


# ============================================
# 📑 الفصول
# ============================================

def get_chapters_by_subject(subject_id: str):
    """جلب فصول مادة معينة"""
    try:
        client = get_supabase_client()
        if not client:
            return []
        
        response = client.table("chapters") \
            .select("*") \
            .eq("subject_id", subject_id) \
            .eq("is_active", True) \
            .order("display_order") \
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"خطأ في جلب الفصول: {e}")
        return []


def create_chapter(subject_id: str, name: str, description: str = "",
                   icon: str = "📑", order: int = 0) -> dict:
    """إنشاء فصل جديد"""
    try:
        client = get_supabase_client()
        if not client:
            return {"success": False, "message": "❌ خطأ في الاتصال"}
        
        data = {
            "subject_id": subject_id,
            "name": name,
            "description": description,
            "icon": icon,
            "display_order": order,
            "is_active": True
        }
        
        response = client.table("chapters").insert(data).execute()
        
        if response.data:
            return {
                "success": True,
                "message": "✅ تم إنشاء الفصل",
                "chapter_id": response.data[0]["id"]
            }
        return {"success": False, "message": "❌ فشل"}
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


def delete_chapter(chapter_id: str) -> dict:
    """حذف فصل"""
    try:
        client = get_supabase_client()
        if not client:
            return {"success": False}
        
        client.table("chapters").delete().eq("id", chapter_id).execute()
        return {"success": True, "message": "✅ تم الحذف"}
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


# ============================================
# 📝 الدروس
# ============================================

def get_lessons_by_chapter(chapter_id: str):
    """جلب دروس فصل معين"""
    try:
        client = get_supabase_client()
        if not client:
            return []
        
        response = client.table("lessons") \
            .select("*") \
            .eq("chapter_id", chapter_id) \
            .eq("is_active", True) \
            .order("display_order") \
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"خطأ في جلب الدروس: {e}")
        return []


def get_lesson_by_id(lesson_id: str):
    """جلب درس معين بكامل بياناته"""
    try:
        client = get_supabase_client()
        if not client:
            return None
        
        response = client.table("lessons") \
            .select("*") \
            .eq("id", lesson_id) \
            .execute()
        
        if response.data:
            # تحديث عدد المشاهدات
            try:
                client.table("lessons") \
                    .update({"views_count": response.data[0].get("views_count", 0) + 1}) \
                    .eq("id", lesson_id) \
                    .execute()
            except:
                pass
            
            return response.data[0]
        return None
    except Exception as e:
        print(f"خطأ في جلب الدرس: {e}")
        return None


def create_lesson(chapter_id: str, name: str, content: str, 
                  description: str = "", icon: str = "📝", order: int = 0) -> dict:
    """إنشاء درس جديد"""
    try:
        client = get_supabase_client()
        if not client:
            return {"success": False, "message": "❌ خطأ في الاتصال"}
        
        if not content or not content.strip():
            return {"success": False, "message": "❌ محتوى الدرس فارغ"}
        
        data = {
            "chapter_id": chapter_id,
            "name": name,
            "description": description,
            "content": content,
            "icon": icon,
            "display_order": order,
            "is_active": True,
            "views_count": 0
        }
        
        response = client.table("lessons").insert(data).execute()
        
        if response.data:
            return {
                "success": True,
                "message": "✅ تم إنشاء الدرس بنجاح",
                "lesson_id": response.data[0]["id"]
            }
        return {"success": False, "message": "❌ فشل"}
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


def update_lesson(lesson_id: str, name: str = None, content: str = None, 
                  description: str = None) -> dict:
    """تحديث درس"""
    try:
        client = get_supabase_client()
        if not client:
            return {"success": False}
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if content is not None:
            update_data["content"] = content
        if description is not None:
            update_data["description"] = description
        
        update_data["updated_at"] = datetime.now().isoformat()
        
        client.table("lessons") \
            .update(update_data) \
            .eq("id", lesson_id) \
            .execute()
        
        return {"success": True, "message": "✅ تم التحديث"}
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


def delete_lesson(lesson_id: str) -> dict:
    """حذف درس"""
    try:
        client = get_supabase_client()
        if not client:
            return {"success": False}
        
        client.table("lessons").delete().eq("id", lesson_id).execute()
        return {"success": True, "message": "✅ تم الحذف"}
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


# ============================================
# 💾 مخرجات الدروس (الكاش العام)
# ============================================

def save_lesson_output(lesson_id: str, output_type: str, content, settings: dict = None) -> dict:
    """حفظ مخرج لدرس (يستفيد منه كل المستخدمين)"""
    try:
        client = get_supabase_client()
        if not client:
            return {"success": False}
        
        # تحويل المحتوى
        if isinstance(content, str):
            content_data = {"text": content}
        elif isinstance(content, (dict, list)):
            content_data = content
        else:
            content_data = {"text": str(content)}
        
        settings = settings or {}
        
        # Upsert (update or insert)
        data = {
            "lesson_id": lesson_id,
            "output_type": output_type,
            "content": content_data,
            "settings": settings
        }
        
        response = client.table("lesson_outputs").upsert(data).execute()
        
        if response.data:
            return {
                "success": True,
                "message": "✅ تم الحفظ",
                "output_id": response.data[0]["id"]
            }
        return {"success": False}
    except Exception as e:
        return {"success": False, "message": f"❌ {str(e)}"}


def get_lesson_output(lesson_id: str, output_type: str, settings: dict = None):
    """جلب مخرج محفوظ لدرس"""
    try:
        client = get_supabase_client()
        if not client:
            return None
        
        query = client.table("lesson_outputs") \
            .select("*") \
            .eq("lesson_id", lesson_id) \
            .eq("output_type", output_type)
        
        response = query.execute()
        
        if not response.data:
            return None
        
        # لو مفيش settings محدد، نرجع الأول
        if not settings:
            item = response.data[0]
            content = item.get("content", {})
            
            # زيادة عدد المشاهدات
            try:
                client.table("lesson_outputs") \
                    .update({"views_count": item.get("views_count", 0) + 1}) \
                    .eq("id", item["id"]) \
                    .execute()
            except:
                pass
            
            if isinstance(content, dict) and "text" in content and len(content) == 1:
                return content["text"]
            return content
        
        # مع settings - ندور على المطابق
        for item in response.data:
            if item.get("settings") == settings:
                content = item.get("content", {})
                
                try:
                    client.table("lesson_outputs") \
                        .update({"views_count": item.get("views_count", 0) + 1}) \
                        .eq("id", item["id"]) \
                        .execute()
                except:
                    pass
                
                if isinstance(content, dict) and "text" in content and len(content) == 1:
                    return content["text"]
                return content
        
        return None
    except Exception as e:
        print(f"خطأ في جلب المخرج: {e}")
        return None


def get_all_outputs_for_lesson(lesson_id: str) -> dict:
    """جلب كل المخرجات المتاحة لدرس"""
    try:
        client = get_supabase_client()
        if not client:
            return {}
        
        response = client.table("lesson_outputs") \
            .select("output_type, views_count") \
            .eq("lesson_id", lesson_id) \
            .execute()
        
        if not response.data:
            return {}
        
        outputs = {}
        for item in response.data:
            output_type = item.get("output_type")
            if output_type:
                outputs[output_type] = {
                    "available": True,
                    "views": item.get("views_count", 0)
                }
        
        return outputs
    except Exception as e:
        return {}


# ============================================
# 📊 الإحصائيات
# ============================================

def get_library_stats() -> dict:
    """إحصائيات المكتبة"""
    try:
        client = get_supabase_client()
        if not client:
            return {}
        
        stages = client.table("educational_stages").select("id").execute()
        grades = client.table("grades").select("id").execute()
        subjects = client.table("subjects").select("id").execute()
        chapters = client.table("chapters").select("id").execute()
        lessons = client.table("lessons").select("id, views_count").execute()
        outputs = client.table("lesson_outputs").select("id, views_count").execute()
        
        total_views = sum(l.get("views_count", 0) for l in (lessons.data or []))
        total_output_views = sum(o.get("views_count", 0) for o in (outputs.data or []))
        
        return {
            "stages_count": len(stages.data) if stages.data else 0,
            "grades_count": len(grades.data) if grades.data else 0,
            "subjects_count": len(subjects.data) if subjects.data else 0,
            "chapters_count": len(chapters.data) if chapters.data else 0,
            "lessons_count": len(lessons.data) if lessons.data else 0,
            "outputs_count": len(outputs.data) if outputs.data else 0,
            "total_lesson_views": total_views,
            "total_output_views": total_output_views,
        }
    except Exception as e:
        return {}