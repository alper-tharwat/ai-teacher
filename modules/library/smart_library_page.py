"""
📚 صفحة المكتبة التعليمية الذكية - تصميم احترافي
"""

import streamlit as st
from modules.library.smart_library_manager import (
    get_all_stages,
    get_grades_by_stage,
    get_subjects_by_grade,
    get_chapters_by_subject,
    get_lessons_by_chapter,
    get_lesson_by_id,
    get_all_outputs_for_lesson
)


def render_smart_library_page():
    """صفحة المكتبة التعليمية للطلاب - تصميم احترافي"""
    
    st.markdown("""
    <style>
        /* ============================================
           التصميم الاحترافي الجديد
           ============================================ */
        
        .lib-header {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
            color: white;
            padding: 24px 20px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .lib-header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 200px;
            height: 200px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
        }
        
        .lib-header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 800;
            position: relative;
            z-index: 1;
        }
        
        .lib-header p {
            margin: 8px 0 0;
            opacity: 0.95;
            font-size: 13px;
            position: relative;
            z-index: 1;
        }
        
        .breadcrumb {
            background: white;
            padding: 12px 18px;
            border-radius: 12px;
            margin-bottom: 16px;
            direction: rtl;
            font-size: 13px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid #E5E7EB;
        }
        
        .section-title {
            color: #111827;
            font-size: 18px;
            font-weight: 700;
            margin: 16px 0 12px;
            padding-right: 12px;
            border-right: 4px solid #6366F1;
        }
        
        /* أزرار الكروت - تصميم احترافي */
        div[data-testid="column"] .stButton > button {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 18px 12px !important;
            font-weight: 700 !important;
            font-size: 13px !important;
            min-height: 110px !important;
            width: 100% !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            white-space: pre-line !important;
            line-height: 1.5 !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        div[data-testid="column"] .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            right: -100%;
            width: 50%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: right 0.5s ease;
        }
        
        div[data-testid="column"] .stButton > button:hover {
            transform: translateY(-4px) !important;
            box-shadow: 0 12px 24px rgba(99, 102, 241, 0.4) !important;
        }
        
        div[data-testid="column"] .stButton > button:hover::before {
            right: 100%;
        }
        
        div[data-testid="column"] .stButton > button:active {
            transform: translateY(-1px) !important;
        }
        
        /* الأزرار العادية */
        .stButton > button {
            border-radius: 12px !important;
            font-weight: 700 !important;
            transition: all 0.3s ease !important;
        }
    </style>
    
    <div class="lib-header">
        <h1>📚 المكتبة التعليمية الذكية</h1>
        <p>كل الدروس جاهزة - مفيش انتظار - كل مخرج جاهز فوراً</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تهيئة session state
    if "lib_selected_stage" not in st.session_state:
        st.session_state["lib_selected_stage"] = None
    if "lib_selected_grade" not in st.session_state:
        st.session_state["lib_selected_grade"] = None
    if "lib_selected_subject" not in st.session_state:
        st.session_state["lib_selected_subject"] = None
    if "lib_selected_chapter" not in st.session_state:
        st.session_state["lib_selected_chapter"] = None
    if "lib_selected_lesson" not in st.session_state:
        st.session_state["lib_selected_lesson"] = None
    
    # عرض المسار (Breadcrumb)
    render_breadcrumb()
    
    # عرض المحتوى حسب المستوى
    if not st.session_state["lib_selected_stage"]:
        render_stages_selection()
    elif not st.session_state["lib_selected_grade"]:
        render_grades_selection()
    elif not st.session_state["lib_selected_subject"]:
        render_subjects_selection()
    elif not st.session_state["lib_selected_chapter"]:
        render_chapters_selection()
    elif not st.session_state["lib_selected_lesson"]:
        render_lessons_selection()
    else:
        render_lesson_details()


def render_breadcrumb():
    """عرض المسار الحالي"""
    
    parts = []
    
    if st.session_state.get("lib_selected_stage"):
        parts.append(f"🎓 {st.session_state.get('lib_stage_name', '')}")
    
    if st.session_state.get("lib_selected_grade"):
        parts.append(f"📖 {st.session_state.get('lib_grade_name', '')}")
    
    if st.session_state.get("lib_selected_subject"):
        parts.append(f"📚 {st.session_state.get('lib_subject_name', '')}")
    
    if st.session_state.get("lib_selected_chapter"):
        parts.append(f"📑 {st.session_state.get('lib_chapter_name', '')}")
    
    if st.session_state.get("lib_selected_lesson"):
        parts.append(f"📝 {st.session_state.get('lib_lesson_name', '')}")
    
    if parts:
        col_path, col_back = st.columns([4, 1])
        with col_path:
            path_text = " ← ".join(parts)
            st.markdown(f"""
            <div class="breadcrumb">
                <strong style='color:#6366F1;'>📍</strong> {path_text}
            </div>
            """, unsafe_allow_html=True)
        with col_back:
            if st.button("🏠 الرئيسية", use_container_width=True, key="back_home_btn"):
                reset_navigation()
                st.rerun()


def reset_navigation():
    """إعادة تعيين التنقل"""
    for key in ["lib_selected_stage", "lib_selected_grade", "lib_selected_subject",
                "lib_selected_chapter", "lib_selected_lesson",
                "lib_stage_name", "lib_grade_name", "lib_subject_name",
                "lib_chapter_name", "lib_lesson_name"]:
        if key in st.session_state:
            st.session_state[key] = None if "selected" in key else ""


def render_stages_selection():
    """اختيار المرحلة"""
    
    st.markdown('<div class="section-title">🎓 اختار المرحلة التعليمية</div>', unsafe_allow_html=True)
    
    stages = get_all_stages()
    
    if not stages:
        st.info("📭 لسه مفيش مراحل في المكتبة")
        return
    
    # 3 أعمدة
    cols = st.columns(3)
    
    for idx, stage in enumerate(stages):
        with cols[idx % 3]:
            grades_count = len(get_grades_by_stage(stage['id']))
            
            button_label = f"{stage.get('icon', '🎓')}\n\n**{stage['name']}**\n\n📖 {grades_count} صف"
            
            if st.button(
                button_label,
                key=f"stage_btn_{stage['id']}",
                use_container_width=True
            ):
                st.session_state["lib_selected_stage"] = stage['id']
                st.session_state["lib_stage_name"] = stage['name']
                st.rerun()


def render_grades_selection():
    """اختيار الصف"""
    
    st.markdown(f'<div class="section-title">📖 اختار الصف في {st.session_state.get("lib_stage_name", "")}</div>', unsafe_allow_html=True)
    
    grades = get_grades_by_stage(st.session_state["lib_selected_stage"])
    
    if not grades:
        st.info("📭 مفيش صفوف")
        if st.button("⬅️ ارجع للمراحل", key="back_to_stages"):
            st.session_state["lib_selected_stage"] = None
            st.rerun()
        return
    
    cols = st.columns(3)
    
    for idx, grade in enumerate(grades):
        with cols[idx % 3]:
            subjects_count = len(get_subjects_by_grade(grade['id']))
            
            button_label = f"{grade.get('icon', '📖')}\n\n**{grade['name']}**\n\n📚 {subjects_count} مادة"
            
            if st.button(
                button_label,
                key=f"grade_btn_{grade['id']}",
                use_container_width=True
            ):
                st.session_state["lib_selected_grade"] = grade['id']
                st.session_state["lib_grade_name"] = grade['name']
                st.rerun()


def render_subjects_selection():
    """اختيار المادة"""
    
    st.markdown(f'<div class="section-title">📚 اختار المادة في {st.session_state.get("lib_grade_name", "")}</div>', unsafe_allow_html=True)
    
    subjects = get_subjects_by_grade(st.session_state["lib_selected_grade"])
    
    if not subjects:
        st.info("📭 مفيش مواد")
        if st.button("⬅️ ارجع للصفوف", key="back_to_grades"):
            st.session_state["lib_selected_grade"] = None
            st.rerun()
        return
    
    cols = st.columns(3)
    
    for idx, subject in enumerate(subjects):
        with cols[idx % 3]:
            chapters_count = len(get_chapters_by_subject(subject['id']))
            
            # تقصير اسم المادة لو طويل
            subject_name = subject['name']
            if len(subject_name) > 25:
                subject_name = subject_name[:25] + "..."
            
            button_label = f"{subject.get('icon', '📚')}\n\n**{subject_name}**\n\n📑 {chapters_count} فصل"
            
            if st.button(
                button_label,
                key=f"subj_btn_{subject['id']}",
                use_container_width=True
            ):
                st.session_state["lib_selected_subject"] = subject['id']
                st.session_state["lib_subject_name"] = subject['name']
                st.rerun()


def render_chapters_selection():
    """اختيار الفصل"""
    
    st.markdown(f'<div class="section-title">📑 الفصول في {st.session_state.get("lib_subject_name", "")}</div>', unsafe_allow_html=True)
    
    chapters = get_chapters_by_subject(st.session_state["lib_selected_subject"])
    
    if not chapters:
        st.info("📭 مفيش فصول")
        if st.button("⬅️ ارجع للمواد", key="back_to_subjects"):
            st.session_state["lib_selected_subject"] = None
            st.rerun()
        return
    
    cols = st.columns(3)
    
    for idx, chapter in enumerate(chapters):
        with cols[idx % 3]:
            lessons_count = len(get_lessons_by_chapter(chapter['id']))
            
            chapter_name = chapter['name']
            if len(chapter_name) > 30:
                chapter_name = chapter_name[:30] + "..."
            
            button_label = f"{chapter.get('icon', '📑')}\n\n**{chapter_name}**\n\n📝 {lessons_count} درس"
            
            if st.button(
                button_label,
                key=f"chap_btn_{chapter['id']}",
                use_container_width=True
            ):
                st.session_state["lib_selected_chapter"] = chapter['id']
                st.session_state["lib_chapter_name"] = chapter['name']
                st.rerun()


def render_lessons_selection():
    """اختيار الدرس"""
    
    st.markdown(f'<div class="section-title">📝 الدروس في {st.session_state.get("lib_chapter_name", "")}</div>', unsafe_allow_html=True)
    
    lessons = get_lessons_by_chapter(st.session_state["lib_selected_chapter"])
    
    if not lessons:
        st.info("📭 مفيش دروس")
        if st.button("⬅️ ارجع للفصول", key="back_to_chapters"):
            st.session_state["lib_selected_chapter"] = None
            st.rerun()
        return
    
    cols = st.columns(3)
    
    for idx, lesson in enumerate(lessons):
        with cols[idx % 3]:
            outputs = get_all_outputs_for_lesson(lesson['id'])
            outputs_count = len(outputs)
            
            lesson_name = lesson['name']
            if len(lesson_name) > 25:
                lesson_name = lesson_name[:25] + "..."
            
            if outputs_count > 0:
                status = f"✅ {outputs_count} مخرج جاهز"
            else:
                status = "⏳ قريباً"
            
            button_label = f"{lesson.get('icon', '📝')}\n\n**{lesson_name}**\n\n{status}"
            
            if st.button(
                button_label,
                key=f"less_btn_{lesson['id']}",
                use_container_width=True
            ):
                st.session_state["lib_selected_lesson"] = lesson['id']
                st.session_state["lib_lesson_name"] = lesson['name']
                
                load_lesson_to_session(lesson['id'])
                
                st.rerun()


def load_lesson_to_session(lesson_id: str):
    """تحميل الدرس في session_state"""
    
    lesson = get_lesson_by_id(lesson_id)
    
    if not lesson:
        return
    
    st.session_state.extracted_text = lesson.get('content', '')
    st.session_state.file_info = {
        'name': lesson.get('name', ''),
        'size_readable': f"{len(lesson.get('content', ''))} حرف",
        'extension': 'LESSON',
    }
    st.session_state.all_pages = [lesson.get('content', '')]
    st.session_state.total_pages = 1
    st.session_state.selected_range = (1, 1)
    
    st.session_state['current_lesson_id'] = lesson_id
    st.session_state['current_file_id'] = f"lesson_{lesson_id}"
    
    st.session_state.summary = ''
    st.session_state.explanation = ''
    st.session_state.quiz_data = None
    st.session_state.flashcards = []
    st.session_state.mindmap_data = None
    st.session_state.mindmap_html = ''


def render_lesson_details():
    """تفاصيل الدرس - تصميم احترافي"""
    
    lesson_id = st.session_state["lib_selected_lesson"]
    lesson = get_lesson_by_id(lesson_id)
    
    if not lesson:
        st.error("❌ الدرس مش موجود")
        return
    
    # عرض الدرس بتصميم احترافي
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
                color: white; padding: 22px; border-radius: 18px; margin-bottom: 16px;
                box-shadow: 0 10px 25px rgba(99, 102, 241, 0.25);
                position: relative; overflow: hidden;'>
        <div style='position: absolute; top: -30%; left: -10%; width: 150px; height: 150px;
                    background: rgba(255,255,255,0.1); border-radius: 50%;'></div>
        <h2 style='margin:0; font-size: 20px; position: relative; z-index: 1; font-weight: 800;'>
            {lesson.get('icon', '📝')} {lesson['name']}
        </h2>
        <p style='margin: 8px 0 0; opacity: 0.95; font-size: 13px; position: relative; z-index: 1;'>
            {lesson.get('description', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    outputs = get_all_outputs_for_lesson(lesson_id)
    
    if outputs:
        st.success(f"🎉 الدرس فيه **{len(outputs)} مخرج جاهز** - اختار من التابات في الأعلى!")
    else:
        st.info("⏳ المخرجات لسه بتتحضّر")
    
    # المخرجات - تصميم احترافي
    output_info = {
        'summary': {'icon': '📝', 'name': 'الملخص', 'color': '#10B981'},
        'explanation': {'icon': '💡', 'name': 'الشرح', 'color': '#F59E0B'},
        'quiz': {'icon': '📋', 'name': 'الامتحان', 'color': '#3B82F6'},
        'flashcards': {'icon': '🎴', 'name': 'البطاقات', 'color': '#EC4899'},
        'mindmap': {'icon': '🧠', 'name': 'الخريطة', 'color': '#8B5CF6'},
        'smart_teacher_lesson': {'icon': '🎭', 'name': 'الأستاذ', 'color': '#EF4444'},
    }
    
    st.markdown('<div style="margin: 16px 0 12px; font-size: 15px; font-weight: 700; color: #111827;">✨ المخرجات المتاحة</div>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    
    for idx, (output_type, info) in enumerate(output_info.items()):
        with cols[idx % 3]:
            is_available = output_type in outputs
            
            if is_available:
                bg = f"linear-gradient(135deg, {info['color']}, {info['color']}cc)"
                status = "✅"
                views = outputs[output_type].get('views', 0)
                shadow = f"0 4px 12px {info['color']}40"
            else:
                bg = "linear-gradient(135deg, #9CA3AF, #6B7280)"
                status = "⏳"
                views = 0
                shadow = "0 2px 6px rgba(0,0,0,0.1)"
            
            st.markdown(f"""
            <div style='background: {bg}; color: white; padding: 14px 8px; border-radius: 14px;
                        text-align: center; margin: 4px 0; min-height: 95px;
                        display: flex; flex-direction: column; justify-content: center;
                        box-shadow: {shadow}; transition: transform 0.3s ease;'>
                <div style='font-size: 28px; margin: 0; line-height: 1;'>{info['icon']}</div>
                <div style='font-size: 12px; font-weight: 700; margin: 6px 0 2px;'>{info['name']}</div>
                <div style='font-size: 10px; opacity: 0.9;'>{status} {views} مرة</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.info("💡 **روح لأي تاب** من الصف التاني (شرح، امتحانات، بطاقات...) واستخدم المحتوى مباشرة!")
    
    with st.expander("📄 محتوى الدرس الكامل"):
        st.text_area(
            "",
            value=lesson.get('content', ''),
            height=300,
            label_visibility="collapsed"
        )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ ارجع للدروس", use_container_width=True, key="back_to_lessons"):
            st.session_state["lib_selected_lesson"] = None
            st.rerun()
    
    with col2:
        if st.button("🏠 الرئيسية", use_container_width=True, key="back_to_start"):
            reset_navigation()
            st.rerun()