"""
🔐 Auth Manager - إدارة تسجيل الدخول والمستخدمين
"""

import streamlit as st
from modules.auth.supabase_client import get_supabase_client


def sign_up(email: str, password: str, display_name: str = "") -> dict:
    """
    تسجيل حساب جديد
    
    Args:
        email: الإيميل
        password: كلمة المرور (8 أحرف على الأقل)
        display_name: الاسم المعروض
    
    Returns:
        dict: {success, message, user}
    """
    try:
        client = get_supabase_client()
        
        if not client:
            return {
                "success": False,
                "message": "❌ فشل الاتصال بقاعدة البيانات"
            }
        
        # التحقق من البيانات
        if not email or not password:
            return {
                "success": False,
                "message": "❌ الإيميل وكلمة المرور مطلوبين"
            }
        
        if len(password) < 8:
            return {
                "success": False,
                "message": "❌ كلمة المرور لازم تكون 8 أحرف على الأقل"
            }
        
        # إنشاء الحساب
        response = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "display_name": display_name or email.split("@")[0]
                }
            }
        })
        
        if response.user:
            # إنشاء سجل في user_settings
            try:
                client.table("user_settings").insert({
                    "user_id": response.user.id,
                    "display_name": display_name or email.split("@")[0],
                    "plan": "free"
                }).execute()
            except:
                pass  # السجل ممكن يكون اتعمل بالفعل
            
            return {
                "success": True,
                "message": "✅ تم إنشاء الحساب بنجاح! اتأكد من الإيميل لتفعيل الحساب",
                "user": response.user
            }
        else:
            return {
                "success": False,
                "message": "❌ فشل إنشاء الحساب"
            }
    
    except Exception as e:
        error_msg = str(e)
        
        # رسائل خطأ مفهومة
        if "already registered" in error_msg.lower():
            return {
                "success": False,
                "message": "❌ الإيميل ده مسجل بالفعل. سجّل دخول بدل التسجيل"
            }
        elif "invalid email" in error_msg.lower():
            return {
                "success": False,
                "message": "❌ الإيميل غير صحيح"
            }
        else:
            return {
                "success": False,
                "message": f"❌ خطأ: {error_msg}"
            }


def sign_in(email: str, password: str) -> dict:
    """
    تسجيل دخول
    """
    try:
        client = get_supabase_client()
        
        if not client:
            return {
                "success": False,
                "message": "❌ فشل الاتصال بقاعدة البيانات"
            }
        
        if not email or not password:
            return {
                "success": False,
                "message": "❌ الإيميل وكلمة المرور مطلوبين"
            }
        
        # تسجيل الدخول
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user and response.session:
            # حفظ في session_state
            st.session_state["user"] = response.user
            st.session_state["session"] = response.session
            st.session_state["is_logged_in"] = True
            
            return {
                "success": True,
                "message": f"✅ أهلاً بيك يا {response.user.email}",
                "user": response.user,
                "session": response.session
            }
        else:
            return {
                "success": False,
                "message": "❌ فشل تسجيل الدخول"
            }
    
    except Exception as e:
        error_msg = str(e)
        
        if "invalid login credentials" in error_msg.lower():
            return {
                "success": False,
                "message": "❌ الإيميل أو كلمة المرور غير صحيحة"
            }
        elif "email not confirmed" in error_msg.lower():
            return {
                "success": False,
                "message": "⚠️ لازم تأكد الإيميل الأول من الرسالة اللي وصلتك"
            }
        else:
            return {
                "success": False,
                "message": f"❌ خطأ: {error_msg}"
            }



def sign_out() -> dict:
    """
    تسجيل خروج
    """
    try:
        client = get_supabase_client()
        
        if client:
            client.auth.sign_out()
        
        # مسح session_state
        keys_to_remove = ["user", "session", "is_logged_in", "is_admin_cached"]
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        
        return {
            "success": True,
            "message": "✅ تم تسجيل الخروج بنجاح"
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ خطأ: {str(e)}"
        }


def get_current_user() -> dict:
    """
    معرفة المستخدم الحالي (لو مسجّل دخول)
    """
    try:
        if st.session_state.get("is_logged_in"):
            user = st.session_state.get("user")
            return {
                "logged_in": True,
                "user": user,
                "email": user.email if user else None,
                "user_id": user.id if user else None
            }
        
        return {
            "logged_in": False,
            "user": None,
            "email": None,
            "user_id": None
        }
    
    except Exception as e:
        return {
            "logged_in": False,
            "user": None,
            "error": str(e)
        }


def is_logged_in() -> bool:
    """
    هل المستخدم مسجّل دخول؟
    """
    return st.session_state.get("is_logged_in", False)


def reset_password(email: str) -> dict:
    """
    طلب إعادة تعيين كلمة المرور
    """
    try:
        client = get_supabase_client()
        
        if not client:
            return {
                "success": False,
                "message": "❌ فشل الاتصال"
            }
        
        client.auth.reset_password_email(email)
        
        return {
            "success": True,
            "message": "✅ تم إرسال رسالة لإعادة تعيين كلمة المرور"
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ خطأ: {str(e)}"
        }



# ============================================
# 🔐 نظام الصلاحيات (Admin/Student)
# ============================================

def is_admin() -> bool:
    """
    التحقق إذا كان المستخدم الحالي أدمن
    
    Returns:
        bool: True لو أدمن
    """
    try:
        if not is_logged_in():
            return False
        
        # نشوف الكاش الأول
        if "is_admin_cached" in st.session_state:
            return st.session_state["is_admin_cached"]
        
        from modules.auth.supabase_client import get_supabase_client
        
        client = get_supabase_client()
        if not client:
            return False
        
        user_info = get_current_user()
        user_id = user_info.get("user_id")
        
        if not user_id:
            return False
        
        # جلب من قاعدة البيانات
        response = client.table("user_settings") \
            .select("is_admin") \
            .eq("user_id", user_id) \
            .execute()
        
        if response.data and len(response.data) > 0:
            admin_status = response.data[0].get("is_admin", False)
            # حفظ في الكاش
            st.session_state["is_admin_cached"] = admin_status
            return admin_status
        
        return False
    
    except Exception as e:
        print(f"خطأ في التحقق من صلاحية الأدمن: {e}")
        return False


def require_admin() -> bool:
    """
    التحقق من صلاحية الأدمن وعرض رسالة لو مش أدمن
    
    Returns:
        bool: True لو أدمن، False وبيعرض رسالة لو لأ
    """
    if not is_admin():
        st.error("❌ هذه الصفحة للأدمن فقط")
        st.info("💡 تواصل مع مدير الموقع لو محتاج صلاحيات إضافية")
        return False
    return True


def clear_admin_cache():
    """مسح كاش صلاحية الأدمن (يستخدم عند تسجيل الخروج)"""
    if "is_admin_cached" in st.session_state:
        del st.session_state["is_admin_cached"]


def get_user_role() -> str:
    """
    جلب دور المستخدم الحالي
    
    Returns:
        str: 'admin' أو 'student'
    """
    if is_admin():
        return 'admin'
    return 'student'