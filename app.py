"""
🎓 المعلم الذكي - AI Teacher v4.0 Pro
الواجهة الرئيسية - بدون سايدبار + مع توب بار
"""
import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import check_config, APP_CONFIG

# المحركات والأدوات
from utils.ai_engine import AIEngine
from utils.file_reader import FileReader
from utils.quiz_generator import QuizGenerator
from utils.voice_generator import VoiceGenerator
from utils.avatar_generator import AvatarGenerator

# التصميم
from desktop_styles import get_desktop_css
from mobile_styles import get_mobile_css

# نظام Auth
from modules.auth.auth_page import render_auth_page
from modules.auth.auth_manager import is_logged_in, is_admin

# Top Bar
from modules.top_bar import render_top_bar

# المكتبة الذكية
from modules.library.smart_library_page import render_smart_library_page
from modules.library.smart_library_admin import render_smart_library_admin

# الأستاذ الذكي
from modules.smart_teacher.teacher_page import render_smart_teacher_page

# الصفحات المنفصلة
from pages.upload_page import render_upload_page
from pages.explanation_page import render_explanation_page
from pages.quiz_page import render_quiz_page
from pages.flashcards_page import render_flashcards_page
from pages.mindmap_page import render_mindmap_page
from pages.avatar_page import render_avatar_page
from pages.audio_page import render_audio_page
from pages.youtube_page import render_youtube_page
from pages.export_page import render_export_page
from pages.chat_page import render_chat_page
from pages.translation_page import render_translation_page


# ═══════════════════════════════════════════════════
# إعدادات الصفحة (بدون سايدبار)
# ═══════════════════════════════════════════════════
st.set_page_config(
    page_title=APP_CONFIG['title'],
    page_icon=APP_CONFIG['icon'],
    layout=APP_CONFIG['layout'],
    initial_sidebar_state="collapsed",
    menu_items={'About': "🎓 المعلم الذكي v4.0 Pro"}
)


# ═══════════════════════════════════════════════════
# تحميل التصميم
# ═══════════════════════════════════════════════════
def load_styles():
    """تحميل كل ملفات CSS"""
    st.markdown(get_desktop_css(), unsafe_allow_html=True)
    st.markdown(get_mobile_css(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# تهيئة Session State
# ═══════════════════════════════════════════════════
def init_session_state():
    """تهيئة المتغيرات"""
    defaults = {
        'extracted_text': '',
        'file_info': {},
        'summary': '',
        'explanation': '',
        'quiz_data': None,
        'quiz_answers': {},
        'quiz_results': {},
        'chat_history': [],
        'audio_path': None,
        'avatar_html': '',
        'current_character': 'ostaz_ahmed',
        'current_background': 'classroom',
        'audio_transcription': '',
        'audio_file_info': {},
        'flashcards': [],
        'current_card_idx': 0,
        'show_answer': False,
        'mindmap_data': None,
        'mindmap_html': '',
        'mindmap_markdown': '',
        'all_pages': [],
        'total_pages': 0,
        'selected_range': None,
        'range_start': 1,
        'range_end': 15,
        'chunk_size': 15,
        'chapters': None,
        'current_chapter': None,
        'current_lesson': None,
        'output_language': 'ar',
        'current_page': 'home',
        'user_plan': 'free',
        'usage_count': {
            'files': 0,
            'summaries': 0,
            'explanations': 0,
            'quizzes': 0,
            'flashcards': 0,
            'mindmaps': 0,
            'teacher': 0,
        },
        'stats': {
            'files_processed': 0,
            'summaries_made': 0,
            'explanations_made': 0,
            'quizzes_taken': 0,
            'questions_asked': 0,
            'audio_converted': 0,
            'flashcards_done': 0,
            'mindmaps_made': 0,
            'pdfs_exported': 0,
            'teacher_sessions': 0,
        }
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ═══════════════════════════════════════════════════
# تهيئة المحركات
# ═══════════════════════════════════════════════════
@st.cache_resource
def init_components():
    """تهيئة المحركات مرة واحدة"""
    ai = AIEngine()
    file_reader = FileReader()
    quiz_gen = QuizGenerator(ai)
    voice_gen = VoiceGenerator(method="edge", ai_engine=ai)
    avatar_gen = AvatarGenerator()
    return ai, file_reader, quiz_gen, voice_gen, avatar_gen


# ═══════════════════════════════════════════════════
# Header الرئيسي
# ═══════════════════════════════════════════════════
def render_header(ai):
    """العنوان الرئيسي"""
    try:
        stats = ai.get_statistics()
        mode = stats.get('current_mode', 'hybrid_pro')
        active = stats.get('active_engine', 'غير محدد')
        total_engines = stats.get('total_engines', 0)

        mode_info = {
            'hybrid_pro': ('🔥', 'Hybrid Pro'),
            'hybrid': ('🧠', 'Hybrid'),
            'gemini': ('🟢', 'Gemini'),
            'cerebras': ('⚡', 'Cerebras'),
            'groq': ('🟣', 'Groq'),
            'openrouter': ('🧠', 'OpenRouter'),
            'cohere': ('🟠', 'Cohere'),
            'mistral': ('🔴', 'Mistral'),
            'together': ('⚪', 'Together'),
            'auto': ('🔄', 'تلقائي'),
        }
        icon, name = mode_info.get(mode, ('🤖', mode))
    except Exception:
        icon, name, active, total_engines = '🤖', 'AI', 'غير محدد', 0

    st.markdown(f"""
    <div class="main-header">
        <h1>🎓 المعلم الذكي</h1>
        <p>أول منصة عربية بتشرحلك أي حاجة بـ {total_engines} محركات ذكاء اصطناعي!</p>
        <div style="margin-top:15px;">
            <span style="background:rgba(255,255,255,0.2);padding:5px 15px;
                         border-radius:15px;font-size:14px;margin:5px;display:inline-block;">
                {icon} الوضع: {name}
            </span>
            <span style="background:rgba(255,255,255,0.2);padding:5px 15px;
                         border-radius:15px;font-size:14px;margin:5px;display:inline-block;">
                ⚡ النشط: {active.upper()}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# الإحصائيات
# ═══════════════════════════════════════════════════
def render_stats():
    """عرض كروت الإحصائيات"""
    s = st.session_state.stats
    cols = st.columns(8)
    items = [
        ("📁", s["files_processed"], "ملفات"),
        ("📝", s["summaries_made"], "تلخيصات"),
        ("📋", s["quizzes_taken"], "امتحانات"),
        ("💬", s["questions_asked"], "أسئلة"),
        ("🎵", s["audio_converted"], "صوتيات"),
        ("🎴", s["flashcards_done"], "بطاقات"),
        ("🧠", s["mindmaps_made"], "خرائط"),
        ("📥", s["pdfs_exported"], "PDFs"),
    ]
    for col, (icon, num, label) in zip(cols, items):
        with col:
            st.markdown(
                f'<div class="stat-box">'
                f'<p class="stat-number">{num}</p>'
                f'<p class="stat-label">{icon} {label}</p>'
                f'</div>',
                unsafe_allow_html=True
            )


# ═══════════════════════════════════════════════════
# Footer
# ═══════════════════════════════════════════════════
def render_footer(ai):
    """الفوتر"""
    try:
        stats = ai.get_statistics()
        ec = stats.get('total_engines', 0)
        active = stats.get('active_engine', '?')
        st.markdown(
            f'<div class="footer">'
            f'<p>🎓 المعلم الذكي v{APP_CONFIG["version"]} Pro</p>'
            f'<p>🔥 {ec} محركات | ⚡ {active.upper()} | ❤️ للتعليم العربي</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    except Exception:
        st.markdown('<div class="footer"><p>🎓 المعلم الذكي Pro</p></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# Main - الدالة الرئيسية
# ═══════════════════════════════════════════════════
def main():
    """الدالة الرئيسية"""
    
    # تحميل التصميم
    load_styles()
    init_session_state()

    # فحص تسجيل الدخول
    if not is_logged_in():
        render_auth_page()
        st.stop()

    # شغّل الـ Top Bar
    render_top_bar()

    # فحص الإعدادات
    config_check = check_config()
    if config_check['status'] == 'error':
        st.error("❌ مفيش أي محرك مفعّل!")
        for issue in config_check['issues']:
            st.warning(issue)
        st.stop()

    # تهيئة المحركات
    try:
        ai, file_reader, quiz_gen, voice_gen, avatar_gen = init_components()
    except Exception as e:
        st.error(f"❌ {str(e)}")
        st.stop()

    if not ai.is_ready:
        st.error(f"❌ {ai.error_message}")
        st.stop()

    # صفحة الاشتراكات
    if st.session_state.get('current_page') == 'subscriptions':
        try:
            from modules.subscriptions.pricing_page import render_pricing_page
            render_pricing_page()
            return
        except Exception as e:
            st.error(f"❌ مشكلة في صفحة الاشتراكات: {e}")
            if st.button("🔙 رجوع للرئيسية"):
                st.session_state['current_page'] = 'home'
                st.rerun()
            return

    # صفحة التحكم في التصميم (للأدمن فقط)
    if st.session_state.get('current_page') == 'design_control':
        if is_admin():
            try:
                from pages.design_control_page import render_design_control_page
                render_design_control_page()
                return
            except Exception as e:
                st.error(f"❌ مشكلة: {e}")
                if st.button("🔙 رجوع"):
                    st.session_state['current_page'] = 'home'
                    st.rerun()
                return
        else:
            st.error("❌ هذه الصفحة للأدمن فقط!")
            if st.button("🔙 رجوع"):
                st.session_state['current_page'] = 'home'
                st.rerun()
            return

    # صفحة إدارة المكتبة الذكية
    if st.session_state.get('show_smart_library_admin') and is_admin():
        try:
            render_smart_library_admin()
            return
        except Exception as e:
            st.error(f"❌ {e}")
            return

    # ═══════════════════════════════════════════════
    # المحتوى الرئيسي
    # ═══════════════════════════════════════════════
    render_header(ai)
    render_stats()

    st.markdown("---")

    # ═══════════════════════════════════════════════
    # الصف الأول: 5 تابات الإدخال
    # ═══════════════════════════════════════════════
    input_tabs = st.tabs([
        "📤 رفع ملف",
        "🎵 صوت",
        "📺 YouTube",
        "🎓 المكتبة الذكية",
        "📂 ملفاتي"
    ])

    with input_tabs[0]:
        render_upload_page(file_reader, ai)
    with input_tabs[1]:
        render_audio_page(ai)
    with input_tabs[2]:
        render_youtube_page(ai)
    with input_tabs[3]:
        render_smart_library_page()
    with input_tabs[4]:
        try:
            from modules.auth.my_files_page import render_my_files_page
            render_my_files_page()
        except Exception as e:
            st.info(f"📂 قريباً... ({e})")

    # ═══════════════════════════════════════════════
    # الصف الثاني: تابات المعالجة (مع الأدمن لو موجود)
    # ═══════════════════════════════════════════════
    output_tab_names = [
        "📝 شرح وتلخيص",
        "📋 امتحانات",
        "🎴 بطاقات الحفظ",
        "🧠 خريطة ذهنية",
        "🎭 الأستاذ الذكي",
        "💬 اسأل سؤال",
        "🌍 ترجمة",
        "📥 تصدير PDF",
    ]

    # إضافة تاب الأدمن
    if is_admin():
        output_tab_names.append("👨‍💼 الأدمن")

    output_tabs = st.tabs(output_tab_names)

    with output_tabs[0]:
        render_explanation_page(ai)
    with output_tabs[1]:
        render_quiz_page(quiz_gen)
    with output_tabs[2]:
        render_flashcards_page(ai)
    with output_tabs[3]:
        render_mindmap_page(ai)
    with output_tabs[4]:
        render_smart_teacher_page(
            ai_engine=ai,
            content=st.session_state.get("extracted_text", "")
        )
    with output_tabs[5]:
        render_chat_page(ai, voice_gen)
    with output_tabs[6]:
        render_translation_page(ai)
    with output_tabs[7]:
        render_export_page()

    # تاب الأدمن (للأدمن فقط)
    if is_admin() and len(output_tabs) > 8:
        with output_tabs[8]:
            admin_inner_tabs = st.tabs([
                "🎓 إدارة المكتبة الذكية",
                "👨‍💼 الأدمن العادي"
            ])

            with admin_inner_tabs[0]:
                render_smart_library_admin()

            with admin_inner_tabs[1]:
                try:
                    from modules.admin.admin_page import render_admin_page
                    render_admin_page()
                except Exception as e:
                    st.error(f"❌ {e}")

    # Footer
    render_footer(ai)


# ═══════════════════════════════════════════════════
# تشغيل التطبيق
# ═══════════════════════════════════════════════════
if __name__ == "__main__":
    main()