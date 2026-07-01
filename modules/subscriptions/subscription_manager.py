# modules/subscriptions/subscription_manager.py

from datetime import datetime
from modules.subscriptions.plans import get_plan, get_limit, is_unlimited
from modules.auth.supabase_client import get_supabase_client

supabase = None

def _get_supabase():
    global supabase
    if supabase is None:
        supabase = get_supabase_client()
    return supabase


# =============================================
# جيب اشتراك المستخدم
# =============================================
def get_user_subscription(user_id: str) -> dict:
    """جيب بيانات اشتراك المستخدم"""
    try:
        result = _get_supabase().table("user_subscriptions") \
            .select("*") \
            .eq("user_id", user_id) \
            .single() \
            .execute()

        if result.data:
            return result.data

        # لو مفيش اشتراك، سجّله كمجاني تلقائياً
        return _create_free_subscription(user_id)

    except Exception:
        return _create_free_subscription(user_id)


def _create_free_subscription(user_id: str) -> dict:
    """سجّل المستخدم على الباقة المجانية تلقائياً"""
    try:
        data = {
            "user_id": user_id,
            "plan_name": "free",
            "status": "active",
            "started_at": datetime.now().isoformat(),
            "expires_at": None,
        }
        _get_supabase().table("user_subscriptions").insert(data).execute()
        return data
    except Exception:
        return {"plan_name": "free", "status": "active"}


# =============================================
# جيب اسم الباقة
# =============================================
def get_user_plan_name(user_id: str) -> str:
    """جيب اسم باقة المستخدم"""
    sub = get_user_subscription(user_id)
    return sub.get("plan_name", "free")


def get_user_plan(user_id: str) -> dict:
    """جيب بيانات باقة المستخدم كاملة"""
    plan_name = get_user_plan_name(user_id)
    return get_plan(plan_name)


# =============================================
# تتبع الاستخدام
# =============================================
def get_usage(user_id: str) -> dict:
    """جيب استخدام المستخدم الشهر الحالي"""
    now = datetime.now()
    try:
        result = _get_supabase().table("usage_tracking") \
            .select("*") \
            .eq("user_id", user_id) \
            .eq("month", now.month) \
            .eq("year", now.year) \
            .single() \
            .execute()

        if result.data:
            return result.data

        # لو مفيش سجل للشهر ده، ابدأ من صفر
        return _create_usage_record(user_id, now.month, now.year)

    except Exception:
        return _empty_usage()


def _create_usage_record(user_id: str, month: int, year: int) -> dict:
    """اعمل سجل استخدام جديد للشهر"""
    try:
        data = {
            "user_id": user_id,
            "month": month,
            "year": year,
            "summaries_used": 0,
            "explanations_used": 0,
            "quizzes_used": 0,
            "flashcards_used": 0,
            "mindmaps_used": 0,
            "teacher_sessions_used": 0,
            "files_count": 0,
        }
        _get_supabase().table("usage_tracking").insert(data).execute()
        return data
    except Exception:
        return _empty_usage()


def _empty_usage() -> dict:
    """استخدام فاضي لو حصل خطأ"""
    return {
        "summaries_used": 0,
        "explanations_used": 0,
        "quizzes_used": 0,
        "flashcards_used": 0,
        "mindmaps_used": 0,
        "teacher_sessions_used": 0,
        "files_count": 0,
    }


# =============================================
# التحقق من الحدود
# =============================================
def can_use_feature(user_id: str, feature: str) -> tuple[bool, str]:
    """
    هل المستخدم يقدر يستخدم الميزة دي؟
    بيرجع (True/False, رسالة)
    
    feature: summaries, explanations, quizzes, 
             flashcards, mindmaps, teacher_sessions
    """
    plan_name = get_user_plan_name(user_id)

    # لو غير محدود
    if is_unlimited(plan_name, feature):
        return True, ""

    # جيب الحد المسموح
    limit = get_limit(plan_name, feature)
    if limit is None:
        return True, ""

    # جيب الاستخدام الحالي
    usage = get_usage(user_id)
    used = usage.get(f"{feature}_used", 0)

    if used >= limit:
        plan = get_plan(plan_name)
        msg = f"وصلت للحد الأقصى ({limit}) في باقة {plan['name']} هذا الشهر"
        return False, msg

    return True, ""


def can_upload_file(user_id: str, file_size_mb: float) -> tuple[bool, str]:
    """هل يقدر يرفع ملف؟"""
    plan_name = get_user_plan_name(user_id)
    plan = get_plan(plan_name)

    # تحقق من حجم الملف
    max_size = plan.get("max_file_size_mb", 5)
    if file_size_mb > max_size:
        return False, f"حجم الملف ({file_size_mb:.1f}MB) أكبر من الحد المسموح ({max_size}MB)"

    # تحقق من عدد الملفات
    max_files = plan.get("max_files")
    if max_files is None:
        return True, ""

    usage = get_usage(user_id)
    files_count = usage.get("files_count", 0)

    if files_count >= max_files:
        return False, f"وصلت للحد الأقصى ({max_files} ملف) في باقتك الحالية"

    return True, ""


# =============================================
# زيادة العداد
# =============================================
def increment_usage(user_id: str, feature: str) -> bool:
    """زوّد عداد الاستخدام بعد كل عملية"""
    now = datetime.now()
    field = f"{feature}_used"

    try:
        # جيب السجل الحالي
        result = _get_supabase().table("usage_tracking") \
            .select("*") \
            .eq("user_id", user_id) \
            .eq("month", now.month) \
            .eq("year", now.year) \
            .single() \
            .execute()

        if result.data:
            current = result.data.get(field, 0)
            _get_supabase().table("usage_tracking") \
                .update({
                    field: current + 1,
                    "updated_at": datetime.now().isoformat()
                }) \
                .eq("user_id", user_id) \
                .eq("month", now.month) \
                .eq("year", now.year) \
                .execute()
        else:
            _create_usage_record(user_id, now.month, now.year)
            increment_usage(user_id, feature)

        return True

    except Exception as e:
        print(f"خطأ في increment_usage: {e}")
        return False


def increment_files_count(user_id: str) -> bool:
    """زوّد عداد الملفات"""
    return increment_usage(user_id, "files_count".replace("_used", ""))


# =============================================
# ملخص الاستخدام للمستخدم
# =============================================
def get_usage_summary(user_id: str) -> dict:
    """
    جيب ملخص الاستخدام مع الحدود
    بيرجع dict فيه كل ميزة مع المستخدم والحد والباقي
    """
    plan_name = get_user_plan_name(user_id)
    plan = get_plan(plan_name)
    usage = get_usage(user_id)

    features = {
        "summaries": "الملخصات",
        "explanations": "الشروحات",
        "quizzes": "الامتحانات",
        "flashcards": "البطاقات",
        "mindmaps": "الخرائط الذهنية",
        "teacher_sessions": "الأستاذ الذكي",
    }

    summary = {}
    for feature, label in features.items():
        limit = get_limit(plan_name, feature)
        used = usage.get(f"{feature}_used", 0)

        summary[feature] = {
            "label": label,
            "used": used,
            "limit": limit,
            "unlimited": limit is None,
            "remaining": None if limit is None else max(0, limit - used),
            "percentage": 0 if limit is None else min(100, int(used / limit * 100)),
        }

    return {
        "plan_name": plan_name,
        "plan": plan,
        "features": summary,
        "files": {
            "count": usage.get("files_count", 0),
            "limit": plan.get("max_files"),
            "unlimited": plan.get("max_files") is None,
        }
    }