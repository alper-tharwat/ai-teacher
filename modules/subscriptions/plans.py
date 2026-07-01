# modules/subscriptions/plans.py

PLANS = {
    "free": {
        "name": "المجانية",
        "price": 0,
        "badge": "",
        "color": "#95a5a6",
        "popular": False,
        "max_accounts": 1,
        "max_files": 2,
        "max_file_size_mb": 5,
        "limits": {
            "summaries": 4,
            "explanations": 3,
            "quizzes": 3,
            "flashcards": 3,
            "mindmaps": 2,
            "teacher_sessions": 1,
        },
        "library_lessons": 2,
        "library_access": "limited",
        "can_export_pdf": False,
        "ai_priority": 1,
        "support": "none",
    },

    "basic": {
        "name": "الأساسية",
        "price": 150,
        "badge": "⭐",
        "color": "#3498db",
        "popular": False,
        "max_accounts": 1,
        "max_files": 30,
        "max_file_size_mb": 30,
        "limits": {
            "summaries": 100,
            "explanations": 100,
            "quizzes": 50,
            "flashcards": 50,
            "mindmaps": 30,
            "teacher_sessions": 15,
        },
        "library_lessons": None,
        "library_access": "single_stage",
        "can_export_pdf": True,
        "ai_priority": 2,
        "support": "normal",
    },

    "premium": {
        "name": "المميزة",
        "price": 250,
        "badge": "💎",
        "color": "#9b59b6",
        "popular": True,
        "max_accounts": 1,
        "max_files": 100,
        "max_file_size_mb": 30,
        "limits": {
            "summaries": 500,
            "explanations": 500,
            "quizzes": 300,
            "flashcards": 300,
            "mindmaps": 200,
            "teacher_sessions": 100,
        },
        "library_lessons": None,
        "library_access": "full",
        "can_export_pdf": True,
        "ai_priority": 3,
        "support": "fast",
    },

    "pro": {
        "name": "الاحترافية",
        "price": 450,
        "badge": "🏆",
        "color": "#f39c12",
        "popular": False,
        "max_accounts": 1,
        "max_files": None,
        "max_file_size_mb": 50,
        "limits": {
            "summaries": None,
            "explanations": None,
            "quizzes": None,
            "flashcards": None,
            "mindmaps": None,
            "teacher_sessions": None,
        },
        "library_lessons": None,
        "library_access": "full",
        "can_export_pdf": True,
        "ai_priority": 4,
        "support": "vip",
    },

    "family": {
        "name": "العائلية",
        "price": 800,
        "badge": "👨‍👩‍👧‍👦",
        "color": "#27ae60",
        "popular": False,
        "max_accounts": 4,
        "max_files": None,
        "max_file_size_mb": 50,
        "limits": {
            "summaries": None,
            "explanations": None,
            "quizzes": None,
            "flashcards": None,
            "mindmaps": None,
            "teacher_sessions": None,
        },
        "library_lessons": None,
        "library_access": "full",
        "can_export_pdf": True,
        "ai_priority": 4,
        "support": "vip",
    },
}


def get_plan(plan_name: str) -> dict:
    """جيب بيانات باقة معينة"""
    return PLANS.get(plan_name, PLANS["free"])


def get_limit(plan_name: str, feature: str):
    """جيب الحد المسموح لميزة معينة - None = غير محدود"""
    plan = get_plan(plan_name)
    return plan["limits"].get(feature)


def is_unlimited(plan_name: str, feature: str) -> bool:
    """هل الميزة دي غير محدودة؟"""
    return get_limit(plan_name, feature) is None


def get_all_plans() -> dict:
    """جيب كل الباقات"""
    return PLANS