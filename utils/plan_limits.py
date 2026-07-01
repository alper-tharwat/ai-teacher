"""
💎 نظام حدود الباقات
- الأدمن استخدام غير محدود
- VIP استخدام غير محدود
"""
import streamlit as st

# ═══════════════════════════════════════════════════
# حدود كل باقة
# ═══════════════════════════════════════════════════
PLAN_LIMITS = {
    "free": {
        "files": 2,
        "summaries": 3,
        "explanations": 3,
        "quizzes": 3,
        "flashcards": 3,
        "mindmaps": 3,
        "teacher": 0,
    },
    "basic": {
        "files": 25,
        "summaries": 50,
        "explanations": 50,
        "quizzes": 50,
        "flashcards": 50,
        "mindmaps": 50,
        "teacher": 20,
    },
    "premium": {
        "files": 50,
        "summaries": 90,
        "explanations": 90,
        "quizzes": 90,
        "flashcards": 90,
        "mindmaps": 90,
        "teacher": 40,
    },
    "pro": {
        "files": 100,
        "summaries": 300,
        "explanations": 300,
        "quizzes": 300,
        "flashcards": 300,
        "mindmaps": 300,
        "teacher": 100,
    },
    "family": {
        "files": 50,
        "summaries": 90,
        "explanations": 90,
        "quizzes": 90,
        "flashcards": 90,
        "mindmaps": 90,
        "teacher": 40,
    },
    "unlimited": {
        "files": 999999,
        "summaries": 999999,
        "explanations": 999999,
        "quizzes": 999999,
        "flashcards": 999999,
        "mindmaps": 999999,
        "teacher": 999999,
    },
}


def is_user_admin():
    """فحص إذا كان المستخدم أدمن"""
    try:
        from modules.auth.auth_manager import is_admin
        return is_admin()
    except Exception:
        return False


def is_special_user():
    """فحص إيميلات VIP"""
    try:
        from modules.auth.auth_manager import get_current_user
        user = get_current_user()
        if not user or not user.get("user"):
            return False
        
        user_obj = user.get("user")
        email = getattr(user_obj, 'email', '').lower()
        
        # ═══════════════════════════════════════
        # 📧 الإيميلات المميزة (استخدام غير محدود)
        # ═══════════════════════════════════════
        SPECIAL_EMAILS = [
            "aaalperr52@gmail.com",           # أنت (الأدمن)
            # ضيف إيميلات مميزة هنا
        ]
        
        return email in SPECIAL_EMAILS
    except Exception:
        return False


def check_plan_limit(feature):
    """هل المستخدم يقدر يستخدم الميزة دي؟"""
    
    # ✅ الأدمن استخدام غير محدود
    if is_user_admin():
        return True, "👨‍💼 أنت أدمن - استخدام غير محدود!"
    
    # ✅ VIP استخدام غير محدود
    if is_special_user():
        return True, "⭐ عضوية VIP - استخدام غير محدود!"
    
    # الفحص العادي
    plan_name = st.session_state.get("user_plan", "free")
    limits = PLAN_LIMITS.get(plan_name, PLAN_LIMITS["free"])
    usage = st.session_state.get('usage_count', {
        'files': 0, 'summaries': 0, 'explanations': 0,
        'quizzes': 0, 'flashcards': 0, 'mindmaps': 0, 'teacher': 0,
    })
    
    limit = limits.get(feature, 0)
    used = usage.get(feature, 0)
    
    if limit == 0:
        return False, "⚠️ الميزة دي غير متاحة في باقتك المجانية. اترقى لباقة أعلى!"
    
    if used >= limit:
        return False, f"⚠️ وصلت للحد ({limit}) في باقتك هذا الشهر. اترقى لباقة أعلى!"
    
    return True, f"✅ متبقي: {limit - used} هذا الشهر"


def increment_usage(feature):
    """زوّد عداد الاستخدام - الأدمن مش بيتحسب"""
    
    # الأدمن و VIP مش بيتحسب عليهم
    if is_user_admin() or is_special_user():
        return
    
    if 'usage_count' not in st.session_state:
        st.session_state.usage_count = {
            'files': 0, 'summaries': 0, 'explanations': 0,
            'quizzes': 0, 'flashcards': 0, 'mindmaps': 0, 'teacher': 0,
        }
    st.session_state.usage_count[feature] = st.session_state.usage_count.get(feature, 0) + 1