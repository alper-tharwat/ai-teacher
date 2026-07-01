"""
👨‍💼 صفحة الأدمن للمكتبة التعليمية الذكية
"""

import streamlit as st
from modules.library.smart_library_manager import (
    # المراحل
    get_all_stages, create_stage, delete_stage,
    # الصفوف
    get_grades_by_stage, create_grade, delete_grade,
    # المواد
    get_subjects_by_grade, create_subject, delete_subject,
    # الفصول
    get_chapters_by_subject, create_chapter, delete_chapter,
    # الدروس
    get_lessons_by_chapter, create_lesson, delete_lesson, update_lesson,
    get_lesson_by_id,
    # المخرجات
    get_all_outputs_for_lesson,
    # الإحصائيات
    get_library_stats
)
from utils.file_reader import FileReader
from modules.library.book_analyzer import (
    analyze_book_structure,
    regenerate_lesson_content,
    generate_lesson_outputs_bulk
)
from modules.library.auto_generator import (
    auto_generate_for_lesson,
    auto_generate_for_chapter,
    check_existing_outputs,
    DEFAULT_OUTPUTS_CONFIG
)
from modules.library.templates import (
    STAGES, GRADES_BY_STAGE, TERMS,
    get_stage_grades, get_terms_for_stage
)
from modules.library.smart_book_uploader import (
    smart_upload_book,
    get_book_estimated_time
)
def render_smart_library_admin():
    """صفحة إدارة المكتبة التعليمية الذكية"""
    
    st.markdown("""
    <style>
        .admin-header {
            background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
            color: white;
            padding: 25px;
            border-radius: 18px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .breadcrumb {
            background: #f8f9fa;
            padding: 12px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            direction: rtl;
        }
        .stat-mini {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
        }
    </style>
    
    <div class="admin-header">
        <h1 style='margin:0;'>📚 إدارة المكتبة التعليمية الذكية</h1>
        <p style='margin:8px 0 0; opacity:0.95;'>أضف المراحل، الصفوف، المواد، الفصول، والدروس</p>
    </div>
    """, unsafe_allow_html=True)
    
    # الإحصائيات
    stats = get_library_stats()
    
    st.markdown("### 📊 إحصائيات المكتبة")
    cols = st.columns(6)
    
    stats_items = [
        ("🎓", stats.get("stages_count", 0), "مراحل"),
        ("📖", stats.get("grades_count", 0), "صفوف"),
        ("📚", stats.get("subjects_count", 0), "مواد"),
        ("📑", stats.get("chapters_count", 0), "فصول"),
        ("📝", stats.get("lessons_count", 0), "دروس"),
        ("💾", stats.get("outputs_count", 0), "مخرجات"),
    ]
    
    for col, (icon, num, label) in zip(cols, stats_items):
        with col:
            st.markdown(f"""
            <div class="stat-mini">
                <h2 style='margin:0;'>{icon}</h2>
                <h3 style='margin:5px 0;'>{num}</h3>
                <p style='margin:0;'>{label}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # التابات - بس الأساسي
    tab1, tab2 = st.tabs([
        "⚡ إضافة ذكية",
        "📝 إدارة الدروس"
    ])
    
    # ============================================
    # ⚡ الإضافة الذكية
    # ============================================
    with tab1:
        render_smart_upload_page()
    
    # ============================================
    # 📝 إدارة الدروس (للتعديل والمراجعة)
    # ============================================
    with tab2:
        render_lessons_management()

# ============================================
# 🎓 إدارة المراحل
# ============================================

def render_stages_management():
    st.markdown("### 🎓 إدارة المراحل التعليمية")
    
    # إضافة مرحلة جديدة
    with st.expander("➕ إضافة مرحلة جديدة", expanded=False):
        with st.form("add_stage_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("اسم المرحلة:", placeholder="مثال: ابتدائي")
                icon = st.text_input("الأيقونة:", value="🎓", max_chars=2)
            with col2:
                description = st.text_input("الوصف:", placeholder="وصف مختصر للمرحلة")
                order = st.number_input("الترتيب:", min_value=0, value=0)
            
            if st.form_submit_button("➕ إضافة المرحلة", type="primary", use_container_width=True):
                if not name:
                    st.error("❌ اسم المرحلة مطلوب")
                else:
                    result = create_stage(name, description, icon, order)
                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])
    
    # عرض المراحل الموجودة
    st.markdown("### 📋 المراحل الموجودة")
    
    stages = get_all_stages()
    
    if not stages:
        st.info("📭 مفيش مراحل بعد. أضف أول مرحلة!")
        return
    
    for stage in stages:
        col1, col2, col3 = st.columns([4, 1, 1])
        
        with col1:
            grades_count = len(get_grades_by_stage(stage['id']))
            st.markdown(f"""
            <div style='background:#f8f9fa; padding:15px; border-radius:10px; 
                        border-right:4px solid #667eea;'>
                <h3 style='margin:0;'>{stage.get('icon', '🎓')} {stage.get('name', '')}</h3>
                <p style='margin:5px 0; color:#7f8c8d;'>{stage.get('description', '')}</p>
                <small style='color:#95a5a6;'>📖 {grades_count} صف</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("")
        
        with col3:
            if st.button("🗑️", key=f"del_stage_{stage['id']}", use_container_width=True):
                st.session_state[f"confirm_del_stage_{stage['id']}"] = True
                st.rerun()
        
        if st.session_state.get(f"confirm_del_stage_{stage['id']}"):
            st.warning(f"⚠️ هتمسح **{stage['name']}** وكل اللي تحتها (صفوف، مواد، فصول، دروس)!")
            col_y, col_n = st.columns(2)
            with col_y:
                if st.button("✅ نعم احذف", key=f"yes_stage_{stage['id']}", type="primary"):
                    result = delete_stage(stage['id'])
                    if result["success"]:
                        st.success(result["message"])
                        del st.session_state[f"confirm_del_stage_{stage['id']}"]
                        st.rerun()
            with col_n:
                if st.button("❌ تراجع", key=f"no_stage_{stage['id']}"):
                    del st.session_state[f"confirm_del_stage_{stage['id']}"]
                    st.rerun()
        
        st.markdown("---")


# ============================================
# 📖 إدارة الصفوف
# ============================================

def render_grades_management():
    st.markdown("### 📖 إدارة الصفوف الدراسية")
    
    stages = get_all_stages()
    
    if not stages:
        st.warning("⚠️ لازم تضيف مرحلة الأول")
        return
    
    # اختيار المرحلة
    stage_options = {s['id']: f"{s.get('icon', '🎓')} {s['name']}" for s in stages}
    selected_stage_id = st.selectbox(
        "اختار المرحلة:",
        options=list(stage_options.keys()),
        format_func=lambda x: stage_options[x],
        key="grade_stage_select"
    )
    
    if not selected_stage_id:
        return
    
    # إضافة صف جديد
    with st.expander("➕ إضافة صف جديد", expanded=False):
        with st.form("add_grade_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("اسم الصف:", placeholder="مثال: الصف الرابع")
                grade_number = st.number_input("رقم الصف:", min_value=0, value=1)
            with col2:
                icon = st.text_input("الأيقونة:", value="📖", max_chars=2)
                order = st.number_input("الترتيب:", min_value=0, value=0, key="grade_order")
            
            if st.form_submit_button("➕ إضافة الصف", type="primary", use_container_width=True):
                if not name:
                    st.error("❌ اسم الصف مطلوب")
                else:
                    result = create_grade(selected_stage_id, name, grade_number, icon, order)
                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])
    
    # عرض الصفوف
    st.markdown("### 📋 الصفوف الموجودة")
    
    grades = get_grades_by_stage(selected_stage_id)
    
    if not grades:
        st.info("📭 مفيش صفوف في المرحلة دي")
        return
    
    for grade in grades:
        col1, col2 = st.columns([5, 1])
        
        with col1:
            subjects_count = len(get_subjects_by_grade(grade['id']))
            st.markdown(f"""
            <div style='background:#f8f9fa; padding:15px; border-radius:10px;
                        border-right:4px solid #4ECDC4;'>
                <h4 style='margin:0;'>{grade.get('icon', '📖')} {grade.get('name', '')}</h4>
                <small style='color:#7f8c8d;'>📚 {subjects_count} مادة</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🗑️", key=f"del_grade_{grade['id']}", use_container_width=True):
                result = delete_grade(grade['id'])
                if result["success"]:
                    st.rerun()
        
        st.markdown("---")


# ============================================
# 📚 إدارة المواد
# ============================================

def render_subjects_management():
    st.markdown("### 📚 إدارة المواد الدراسية")
    
    stages = get_all_stages()
    if not stages:
        st.warning("⚠️ لازم تضيف مرحلة وصف الأول")
        return
    
    # اختيار المرحلة والصف
    col_s, col_g = st.columns(2)
    
    with col_s:
        stage_options = {s['id']: f"{s.get('icon', '🎓')} {s['name']}" for s in stages}
        selected_stage = st.selectbox(
            "المرحلة:",
            options=list(stage_options.keys()),
            format_func=lambda x: stage_options[x],
            key="subj_stage"
        )
    
    grades = get_grades_by_stage(selected_stage) if selected_stage else []
    
    if not grades:
        st.warning("⚠️ مفيش صفوف في المرحلة دي")
        return
    
    with col_g:
        grade_options = {g['id']: f"{g.get('icon', '📖')} {g['name']}" for g in grades}
        selected_grade = st.selectbox(
            "الصف:",
            options=list(grade_options.keys()),
            format_func=lambda x: grade_options[x],
            key="subj_grade"
        )
    
    if not selected_grade:
        return
    
    # إضافة مادة جديدة
    with st.expander("➕ إضافة مادة جديدة", expanded=False):
        with st.form("add_subject_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("اسم المادة:", placeholder="مثال: دراسات اجتماعية")
                icon = st.text_input("الأيقونة:", value="📚", max_chars=2)
            with col2:
                color = st.color_picker("اللون:", value="#667eea")
                order = st.number_input("الترتيب:", min_value=0, value=0, key="subj_order")
            
            description = st.text_area("الوصف:", placeholder="وصف المادة", height=80)
            
            if st.form_submit_button("➕ إضافة المادة", type="primary", use_container_width=True):
                if not name:
                    st.error("❌ اسم المادة مطلوب")
                else:
                    result = create_subject(selected_grade, name, description, icon, color, order)
                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])
    
    # عرض المواد
    st.markdown("### 📋 المواد الموجودة")
    
    subjects = get_subjects_by_grade(selected_grade)
    
    if not subjects:
        st.info("📭 مفيش مواد في الصف ده")
        return
    
    for subject in subjects:
        col1, col2 = st.columns([5, 1])
        
        with col1:
            chapters_count = len(get_chapters_by_subject(subject['id']))
            color = subject.get('color', '#667eea')
            st.markdown(f"""
            <div style='background:#f8f9fa; padding:15px; border-radius:10px;
                        border-right:4px solid {color};'>
                <h4 style='margin:0; color:{color};'>{subject.get('icon', '📚')} {subject.get('name', '')}</h4>
                <p style='margin:5px 0; color:#7f8c8d; font-size:13px;'>{subject.get('description', '')}</p>
                <small style='color:#95a5a6;'>📑 {chapters_count} فصل</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🗑️", key=f"del_subj_{subject['id']}", use_container_width=True):
                result = delete_subject(subject['id'])
                if result["success"]:
                    st.rerun()
        
        st.markdown("---")


# ============================================
# 📑 إدارة الفصول
# ============================================

def render_chapters_management():
    st.markdown("### 📑 إدارة الفصول")
    
    stages = get_all_stages()
    if not stages:
        st.warning("⚠️ لازم تضيف مرحلة وصف ومادة الأول")
        return
    
    # اختيار المرحلة، الصف، المادة
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stage_options = {s['id']: f"{s.get('icon', '🎓')} {s['name']}" for s in stages}
        selected_stage = st.selectbox(
            "المرحلة:",
            options=list(stage_options.keys()),
            format_func=lambda x: stage_options[x],
            key="chap_stage"
        )
    
    grades = get_grades_by_stage(selected_stage) if selected_stage else []
    if not grades:
        st.warning("⚠️ مفيش صفوف")
        return
    
    with col2:
        grade_options = {g['id']: f"{g.get('icon', '📖')} {g['name']}" for g in grades}
        selected_grade = st.selectbox(
            "الصف:",
            options=list(grade_options.keys()),
            format_func=lambda x: grade_options[x],
            key="chap_grade"
        )
    
    subjects = get_subjects_by_grade(selected_grade) if selected_grade else []
    if not subjects:
        st.warning("⚠️ مفيش مواد")
        return
    
    with col3:
        subject_options = {s['id']: f"{s.get('icon', '📚')} {s['name']}" for s in subjects}
        selected_subject = st.selectbox(
            "المادة:",
            options=list(subject_options.keys()),
            format_func=lambda x: subject_options[x],
            key="chap_subject"
        )
    
    if not selected_subject:
        return
    
    # إضافة فصل
    with st.expander("➕ إضافة فصل جديد", expanded=False):
        with st.form("add_chapter_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("اسم الفصل:", placeholder="مثال: الفصل الأول - البيئة")
                icon = st.text_input("الأيقونة:", value="📑", max_chars=2)
            with col2:
                order = st.number_input("الترتيب:", min_value=0, value=0, key="chap_order")
            
            description = st.text_area("الوصف:", placeholder="وصف الفصل", height=80)
            
            if st.form_submit_button("➕ إضافة الفصل", type="primary", use_container_width=True):
                if not name:
                    st.error("❌ اسم الفصل مطلوب")
                else:
                    result = create_chapter(selected_subject, name, description, icon, order)
                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])
    
    # عرض الفصول
    st.markdown("### 📋 الفصول الموجودة")
    
    chapters = get_chapters_by_subject(selected_subject)
    
    if not chapters:
        st.info("📭 مفيش فصول")
        return
    
    for chapter in chapters:
        col1, col2 = st.columns([5, 1])
        
        with col1:
            lessons_count = len(get_lessons_by_chapter(chapter['id']))
            st.markdown(f"""
            <div style='background:#f8f9fa; padding:15px; border-radius:10px;
                        border-right:4px solid #FF6B6B;'>
                <h4 style='margin:0;'>{chapter.get('icon', '📑')} {chapter.get('name', '')}</h4>
                <p style='margin:5px 0; color:#7f8c8d; font-size:13px;'>{chapter.get('description', '')}</p>
                <small style='color:#95a5a6;'>📝 {lessons_count} درس</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🗑️", key=f"del_chap_{chapter['id']}", use_container_width=True):
                result = delete_chapter(chapter['id'])
                if result["success"]:
                    st.rerun()
        
        st.markdown("---")


# ============================================
# 📝 إدارة الدروس
# ============================================

def render_lessons_management():
    st.markdown("### 📝 إدارة الدروس")
    
    stages = get_all_stages()
    if not stages:
        st.warning("⚠️ لازم تضيف مرحلة وصف ومادة وفصل الأول")
        return
    
    # اختيار المسار
    col1, col2 = st.columns(2)
    
    with col1:
        stage_options = {s['id']: f"{s.get('icon', '🎓')} {s['name']}" for s in stages}
        selected_stage = st.selectbox(
            "المرحلة:",
            options=list(stage_options.keys()),
            format_func=lambda x: stage_options[x],
            key="less_stage"
        )
    
    grades = get_grades_by_stage(selected_stage) if selected_stage else []
    if not grades:
        st.warning("⚠️ مفيش صفوف")
        return
    
    with col2:
        grade_options = {g['id']: f"{g.get('icon', '📖')} {g['name']}" for g in grades}
        selected_grade = st.selectbox(
            "الصف:",
            options=list(grade_options.keys()),
            format_func=lambda x: grade_options[x],
            key="less_grade"
        )
    
    col3, col4 = st.columns(2)
    
    subjects = get_subjects_by_grade(selected_grade) if selected_grade else []
    if not subjects:
        st.warning("⚠️ مفيش مواد")
        return
    
    with col3:
        subject_options = {s['id']: f"{s.get('icon', '📚')} {s['name']}" for s in subjects}
        selected_subject = st.selectbox(
            "المادة:",
            options=list(subject_options.keys()),
            format_func=lambda x: subject_options[x],
            key="less_subject"
        )
    
    chapters = get_chapters_by_subject(selected_subject) if selected_subject else []
    if not chapters:
        st.warning("⚠️ مفيش فصول")
        return
    
    with col4:
        chapter_options = {c['id']: f"{c.get('icon', '📑')} {c['name']}" for c in chapters}
        selected_chapter = st.selectbox(
            "الفصل:",
            options=list(chapter_options.keys()),
            format_func=lambda x: chapter_options[x],
            key="less_chapter"
        )
    
    if not selected_chapter:
        return
    
    # إضافة درس جديد
    with st.expander("➕ إضافة درس جديد", expanded=False):
        
        # طريقة الإدخال
        input_method = st.radio(
            "طريقة إدخال محتوى الدرس:",
            options=["📝 كتابة يدوية", "📤 رفع ملف"],
            horizontal=True,
            key="lesson_input_method"
        )
        
        with st.form("add_lesson_form"):
            col1, col2 = st.columns([2, 1])
            with col1:
                name = st.text_input("اسم الدرس:", placeholder="مثال: الدرس الأول - المياه ومصادرها")
            with col2:
                icon = st.text_input("الأيقونة:", value="📝", max_chars=2)
            
            description = st.text_input("الوصف المختصر:", placeholder="وصف قصير للدرس")
            
            content = ""
            
            if input_method == "📝 كتابة يدوية":
                content = st.text_area(
                    "محتوى الدرس:",
                    height=300,
                    placeholder="اكتب محتوى الدرس الكامل هنا...",
                    help="هذا المحتوى سيتم استخدامه لتوليد الملخصات والامتحانات والبطاقات"
                )
            else:
                uploaded_file = st.file_uploader(
                    "ارفع ملف الدرس:",
                    type=['pdf', 'docx', 'txt'],
                    help="سيتم استخراج النص من الملف"
                )
                if uploaded_file:
                    with st.spinner("📖 جاري استخراج النص..."):
                        file_reader = FileReader()
                        result = file_reader.read(uploaded_file)
                    
                    if result['success']:
                        content = result['text']
                        st.success(f"✅ تم استخراج {len(content)} حرف")
                        with st.expander("👁️ معاينة النص"):
                            st.text_area("", value=content[:500] + "...", height=150, label_visibility="collapsed")
                    else:
                        st.error(f"❌ {result['error']}")
            
            order = st.number_input("الترتيب:", min_value=0, value=0, key="less_order")
            
            if st.form_submit_button("➕ إضافة الدرس", type="primary", use_container_width=True):
                if not name:
                    st.error("❌ اسم الدرس مطلوب")
                elif not content or not content.strip():
                    st.error("❌ محتوى الدرس مطلوب")
                else:
                    result = create_lesson(selected_chapter, name, content, description, icon, order)
                    if result["success"]:
                        st.success(result["message"])
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(result["message"])
    
    # عرض الدروس
    st.markdown("### 📋 الدروس الموجودة")
    
    lessons = get_lessons_by_chapter(selected_chapter)
    
    if not lessons:
        st.info("📭 مفيش دروس في الفصل ده")
        return
    
    for lesson in lessons:
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        
        with col1:
            outputs = get_all_outputs_for_lesson(lesson['id'])
            outputs_count = len(outputs)
            
            outputs_badges = ""
            if outputs:
                badges = []
                for ot in outputs.keys():
                    badges.append(f'<span style="background:#28a745; color:white; padding:2px 8px; border-radius:8px; font-size:11px; margin:2px;">{ot} ✓</span>')
                outputs_badges = ' '.join(badges)
            
            st.markdown(f"""
            <div style='background:#f8f9fa; padding:15px; border-radius:10px;
                        border-right:4px solid #4ECDC4;'>
                <h4 style='margin:0;'>{lesson.get('icon', '📝')} {lesson.get('name', '')}</h4>
                <p style='margin:5px 0; color:#7f8c8d; font-size:13px;'>{lesson.get('description', '')}</p>
                <small style='color:#95a5a6;'>
                    📊 {lesson.get('views_count', 0)} مشاهدة | 
                    💾 {outputs_count} مخرج محفوظ
                </small>
                <div style='margin-top:8px;'>{outputs_badges}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🚀", key=f"gen_less_{lesson['id']}", use_container_width=True, help="ولّد المخرجات تلقائياً"):
                st.session_state[f"gen_lesson_{lesson['id']}"] = True
                st.rerun()
        
        with col3:
            if st.button("👁️", key=f"view_less_{lesson['id']}", use_container_width=True, help="معاينة"):
                st.session_state[f"preview_less_{lesson['id']}"] = not st.session_state.get(f"preview_less_{lesson['id']}", False)
                st.rerun()
        
        with col4:
            if st.button("🗑️", key=f"del_less_{lesson['id']}", use_container_width=True, help="حذف"):
                result = delete_lesson(lesson['id'])
                if result["success"]:
                    st.rerun()
        
        # توليد المخرجات لدرس واحد
        if st.session_state.get(f"gen_lesson_{lesson['id']}"):
            st.markdown("---")
            with st.container():
                st.markdown(f"### 🚀 توليد المخرجات لـ: {lesson.get('name')}")
                
                full_lesson = get_lesson_by_id(lesson['id'])
                if not full_lesson:
                    st.error("❌ مشكلة في جلب الدرس")
                    del st.session_state[f"gen_lesson_{lesson['id']}"]
                    st.rerun()
                
                # عرض الموجود
                existing = check_existing_outputs(lesson['id'])
                
                st.markdown("**حالة المخرجات الحالية:**")
                cols_status = st.columns(5)
                output_types_display = {
                    'summary': '📝',
                    'explanation': '💡',
                    'quiz': '📋',
                    'flashcards': '🎴',
                    'mindmap': '🧠'
                }
                
                for i, (ot, icon) in enumerate(output_types_display.items()):
                    with cols_status[i]:
                        status = "✅" if existing.get(ot) else "⏳"
                        st.markdown(f"<div style='text-align:center; padding:10px; background:{'#d4edda' if existing.get(ot) else '#fff3cd'}; border-radius:8px;'>{icon}<br>{status}</div>", unsafe_allow_html=True)
                
                st.markdown("")
                
                # خيارات
                col_a, col_b = st.columns(2)
                
                with col_a:
                    skip_existing = st.checkbox(
                        "تخطي المخرجات الموجودة",
                        value=True,
                        key=f"skip_{lesson['id']}",
                        help="لو مفعّل، مش هيعيد توليد المخرجات الموجودة"
                    )
                
                with col_b:
                    pass
                
                # زرار التنفيذ
                col_x, col_y = st.columns(2)
                
                with col_x:
                    if st.button("🚀 ابدأ التوليد", type="primary", use_container_width=True, key=f"start_gen_{lesson['id']}"):
                        from utils.ai_engine import AIEngine
                        from utils.quiz_generator import QuizGenerator
                        
                        ai_engine = AIEngine()
                        quiz_gen = QuizGenerator(ai_engine)
                        
                        progress_bar = st.progress(0)
                        status = st.empty()
                        
                        with st.spinner("⏳ جاري التوليد..."):
                            result = auto_generate_for_lesson(
                                ai_engine=ai_engine,
                                lesson_id=lesson['id'],
                                lesson_content=full_lesson.get('content', ''),
                                quiz_gen=quiz_gen,
                                skip_existing=skip_existing
                            )
                        
                        progress_bar.progress(1.0)
                        status.empty()
                        
                        if result['success']:
                            st.success(f"""
                            ✅ **تم التوليد بنجاح!**
                            - 🆕 توليد جديد: {len(result['generated'])}
                            - ⏭️ تم تخطيه (موجود): {len(result['skipped'])}
                            - ❌ فشل: {len(result['failed'])}
                            """)
                            
                            if result['generated']:
                                with st.expander("✅ المخرجات اللي اتولدت"):
                                    for item in result['generated']:
                                        st.write(f"- {item['name']}")
                            
                            if result['failed']:
                                with st.expander("❌ المخرجات اللي فشلت"):
                                    for item in result['failed']:
                                        st.error(f"- {item['name']}: {item.get('error', '')}")
                            
                            st.balloons()
                            
                            del st.session_state[f"gen_lesson_{lesson['id']}"]
                            st.rerun()
                        else:
                            st.error("❌ فشل التوليد")
                
                with col_y:
                    if st.button("❌ إلغاء", use_container_width=True, key=f"cancel_gen_{lesson['id']}"):
                        del st.session_state[f"gen_lesson_{lesson['id']}"]
                        st.rerun()
        
        # معاينة الدرس
        if st.session_state.get(f"preview_less_{lesson['id']}"):
            full_lesson = get_lesson_by_id(lesson['id'])
            if full_lesson:
                st.text_area(
                    "محتوى الدرس:",
                    value=full_lesson.get('content', '')[:1000] + ("..." if len(full_lesson.get('content', '')) > 1000 else ""),
                    height=200,
                    key=f"preview_text_{lesson['id']}",
                    label_visibility="collapsed"
                )
        
        st.markdown("---")
    
    # ============================================
    # 🚀 زر توليد لكل الدروس في الفصل
    # ============================================
    if lessons:
        st.markdown("---")
        st.markdown("### 🚀 توليد المخرجات لكل دروس الفصل")
        
        st.info(f"💡 ده هيولّد كل المخرجات لـ **{len(lessons)} درس** دفعة واحدة")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            skip_all = st.checkbox(
                "تخطي المخرجات الموجودة",
                value=True,
                key="skip_chapter_existing",
                help="مش هيعيد توليد المخرجات اللي موجودة بالفعل"
            )
        
        with col2:
            if st.button("🚀 ولّد لكل الدروس", type="primary", use_container_width=True, key="gen_all_chapter"):
                st.session_state["bulk_generating"] = True
                st.rerun()
        
        # التوليد للكل
        if st.session_state.get("bulk_generating"):
            st.markdown("---")
            
            from utils.ai_engine import AIEngine
            from utils.quiz_generator import QuizGenerator
            
            ai_engine = AIEngine()
            quiz_gen = QuizGenerator(ai_engine)
            
            progress_bar = st.progress(0)
            status = st.empty()
            
            def update_progress(progress, message):
                progress_bar.progress(progress, text=message)
            
            # تحضير الدروس مع المحتوى الكامل
            lessons_with_content = []
            for lesson in lessons:
                full = get_lesson_by_id(lesson['id'])
                if full:
                    lessons_with_content.append(full)
            
            with st.spinner("⏳ جاري التوليد لكل الدروس..."):
                result = auto_generate_for_chapter(
                    ai_engine=ai_engine,
                    chapter_id=selected_chapter,
                    lessons=lessons_with_content,
                    quiz_gen=quiz_gen,
                    skip_existing=skip_all,
                    progress_callback=update_progress
                )
            
            progress_bar.progress(1.0, text="✅ تم!")
            status.empty()
            
            # عرض النتائج
            st.success(f"""
            ✅ **تم التوليد بنجاح!**
            
            📊 **التقرير:**
            - ✅ دروس مكتملة: {result['completed_lessons']}/{result['total_lessons']}
            - ❌ دروس فاشلة: {result['failed_lessons']}
            - 🆕 إجمالي المخرجات الجديدة: {result['total_generated']}
            - ⏭️ مخرجات تم تخطيها: {result['total_skipped']}
            - ❌ مخرجات فشلت: {result['total_failed']}
            """)
            
            # تفاصيل لكل درس
            with st.expander("📋 تفاصيل كل درس"):
                for item in result['lessons_results']:
                    lesson_name = item['lesson_name']
                    lesson_result = item['result']
                    
                    status_icon = "✅" if lesson_result['success'] else "❌"
                    st.markdown(f"**{status_icon} {lesson_name}**")
                    st.write(f"  - 🆕 جديد: {len(lesson_result['generated'])}")
                    st.write(f"  - ⏭️ تخطي: {len(lesson_result['skipped'])}")
                    st.write(f"  - ❌ فشل: {len(lesson_result['failed'])}")
                    st.markdown("---")
            
            st.balloons()
            
            del st.session_state["bulk_generating"]
            
            if st.button("🔄 تحديث الصفحة"):
                st.rerun()


# ============================================
# 🤖 رفع كتاب كامل وتحليله بالذكاء الاصطناعي
# ============================================

def render_book_analyzer_page():
    """صفحة تحليل الكتاب الكامل بالذكاء الاصطناعي"""
    
    st.markdown("""
    <div style='background:linear-gradient(135deg, #FF6B6B, #4ECDC4);
                color:white; padding:20px; border-radius:15px; text-align:center;
                margin-bottom:20px;'>
        <h2 style='margin:0;'>🤖 رفع كتاب كامل بالذكاء الاصطناعي</h2>
        <p style='margin:8px 0 0; opacity:0.95;'>
            ارفع الكتاب وAI هيقسمه لفصول ودروس تلقائياً!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # الخطوة 1: اختيار المسار (مرحلة → مادة)
    # ============================================
    st.markdown("### 1️⃣ اختار المسار اللي هتضيف الكتاب فيه")
    
    stages = get_all_stages()
    if not stages:
        st.warning("⚠️ لازم تضيف مرحلة الأول من تاب '🎓 المراحل'")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        stage_options = {s['id']: f"{s.get('icon', '🎓')} {s['name']}" for s in stages}
        selected_stage = st.selectbox(
            "المرحلة:",
            options=list(stage_options.keys()),
            format_func=lambda x: stage_options[x],
            key="book_stage"
        )
    
    grades = get_grades_by_stage(selected_stage) if selected_stage else []
    if not grades:
        st.warning("⚠️ مفيش صفوف. أضف صف الأول")
        return
    
    with col2:
        grade_options = {g['id']: f"{g.get('icon', '📖')} {g['name']}" for g in grades}
        selected_grade = st.selectbox(
            "الصف:",
            options=list(grade_options.keys()),
            format_func=lambda x: grade_options[x],
            key="book_grade"
        )
    
    subjects = get_subjects_by_grade(selected_grade) if selected_grade else []
    if not subjects:
        st.warning("⚠️ مفيش مواد")
        return
    
    subject_options = {s['id']: f"{s.get('icon', '📚')} {s['name']}" for s in subjects}
    selected_subject = st.selectbox(
        "المادة:",
        options=list(subject_options.keys()),
        format_func=lambda x: subject_options[x],
        key="book_subject"
    )
    
    if not selected_subject:
        return
    
    st.markdown("---")
    
    # ============================================
    # الخطوة 2: رفع الكتاب
    # ============================================
    st.markdown("### 2️⃣ ارفع الكتاب")
    
    book_title = st.text_input(
        "📖 اسم الكتاب (اختياري):",
        placeholder="مثال: دراسات اجتماعية - الترم الأول"
    )
    
    uploaded_file = st.file_uploader(
        "ارفع الكتاب:",
        type=['pdf', 'docx', 'txt'],
        help="ارفع الكتاب كامل وAI هيقسمه تلقائياً",
        key="book_uploader"
    )
    
    if not uploaded_file:
        st.info("👆 ارفع الكتاب لبدء التحليل")
        return
    
    # عرض معلومات الملف
    file_size_mb = uploaded_file.size / (1024 * 1024)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 الحجم", f"{file_size_mb:.2f} MB")
    with col2:
        st.metric("📁 النوع", uploaded_file.name.split('.')[-1].upper())
    with col3:
        st.metric("📄 الاسم", uploaded_file.name[:20])
    
    st.markdown("---")
    
    # ============================================
    # الخطوة 3: تحليل الكتاب
    # ============================================
    st.markdown("### 3️⃣ تحليل الكتاب")
    
    # خيارات إضافية
    with st.expander("⚙️ خيارات إضافية"):
        auto_generate = st.checkbox(
            "🚀 ولّد كل المخرجات تلقائياً بعد الحفظ",
            value=False,
            help="هيولّد ملخص + امتحان + بطاقات لكل درس"
        )
        
        if auto_generate:
            st.markdown("**اختار المخرجات اللي تتولد:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                gen_summary = st.checkbox("📝 ملخص", value=True)
            with col2:
                gen_quiz = st.checkbox("📋 امتحان", value=True)
            with col3:
                gen_flashcards = st.checkbox("🎴 بطاقات", value=True)
    
    if st.button("🤖 ابدأ تحليل الكتاب بالذكاء الاصطناعي", type="primary", use_container_width=True):
        
        # استخراج النص
        with st.spinner("📖 جاري استخراج النص من الكتاب..."):
            file_reader = FileReader()
            result = file_reader.read(uploaded_file)
        
        if not result['success']:
            st.error(f"❌ {result['error']}")
            return
        
        book_text = result['text']
        
        st.success(f"✅ تم استخراج {len(book_text):,} حرف من الكتاب")
        
        # تحليل بالـ AI
        from utils.ai_engine import AIEngine
        ai_engine = AIEngine()
        
        analysis = analyze_book_structure(ai_engine, book_text, book_title)
        
        if not analysis['success']:
            st.error(f"❌ {analysis.get('error', '')}")
            if analysis.get('raw_response'):
                with st.expander("تفاصيل الخطأ"):
                    st.code(analysis['raw_response'])
            return
        
        # حفظ في session للمعاينة
        st.session_state['book_analysis'] = analysis['data']
        st.session_state['book_subject_id'] = selected_subject
        st.session_state['book_auto_generate'] = auto_generate
        if auto_generate:
            output_types = []
            if gen_summary: output_types.append('summary')
            if gen_quiz: output_types.append('quiz')
            if gen_flashcards: output_types.append('flashcards')
            st.session_state['book_output_types'] = output_types
        
        st.success("✅ تم التحليل! شوف النتيجة وعدّل لو محتاج")
        st.rerun()
    
    # ============================================
    # الخطوة 4: عرض المعاينة والتعديل
    # ============================================
    if 'book_analysis' in st.session_state:
        st.markdown("---")
        render_book_preview()


def render_book_preview():
    """عرض معاينة الكتاب بعد التحليل"""
    
    analysis = st.session_state.get('book_analysis')
    if not analysis:
        return
    
    st.markdown("### 4️⃣ معاينة وتعديل")
    
    # معلومات عامة
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📑 الفصول", analysis.get('total_chapters', 0))
    with col2:
        st.metric("📝 الدروس", analysis.get('total_lessons', 0))
    with col3:
        st.metric("📖 الكتاب", analysis.get('book_title', 'بدون عنوان')[:20])
    
    if analysis.get('book_description'):
        st.info(f"💬 {analysis['book_description']}")
    
    # عرض الفصول والدروس
    st.markdown("### 📚 الفصول والدروس")
    st.caption("💡 تقدر تعدّل أي عنوان أو محتوى قبل الحفظ")
    
    chapters = analysis.get('chapters', [])
    
    for chap_idx, chapter in enumerate(chapters):
        with st.expander(f"📑 {chapter.get('name', f'الفصل {chap_idx+1}')}", expanded=False):
            
            # تعديل اسم الفصل
            new_chap_name = st.text_input(
                "اسم الفصل:",
                value=chapter.get('name', ''),
                key=f"chap_name_{chap_idx}"
            )
            
            new_chap_desc = st.text_input(
                "وصف الفصل:",
                value=chapter.get('description', ''),
                key=f"chap_desc_{chap_idx}"
            )
            
            # تحديث في الـ session
            if new_chap_name != chapter.get('name'):
                st.session_state['book_analysis']['chapters'][chap_idx]['name'] = new_chap_name
            if new_chap_desc != chapter.get('description'):
                st.session_state['book_analysis']['chapters'][chap_idx]['description'] = new_chap_desc
            
            st.markdown(f"**📝 الدروس ({len(chapter.get('lessons', []))}):**")
            
            lessons = chapter.get('lessons', [])
            
            for less_idx, lesson in enumerate(lessons):
                st.markdown("---")
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    new_lesson_name = st.text_input(
                        f"اسم الدرس {less_idx+1}:",
                        value=lesson.get('name', ''),
                        key=f"less_name_{chap_idx}_{less_idx}"
                    )
                
                with col2:
                    if st.button("🗑️", key=f"del_less_{chap_idx}_{less_idx}", use_container_width=True):
                        # حذف الدرس
                        st.session_state['book_analysis']['chapters'][chap_idx]['lessons'].pop(less_idx)
                        st.rerun()
                
                new_lesson_desc = st.text_input(
                    "وصف الدرس:",
                    value=lesson.get('description', ''),
                    key=f"less_desc_{chap_idx}_{less_idx}"
                )
                
                new_content = st.text_area(
                    "محتوى الدرس:",
                    value=lesson.get('content', ''),
                    height=200,
                    key=f"less_content_{chap_idx}_{less_idx}"
                )
                
                # تحديث في session
                st.session_state['book_analysis']['chapters'][chap_idx]['lessons'][less_idx]['name'] = new_lesson_name
                st.session_state['book_analysis']['chapters'][chap_idx]['lessons'][less_idx]['description'] = new_lesson_desc
                st.session_state['book_analysis']['chapters'][chap_idx]['lessons'][less_idx]['content'] = new_content
    
    st.markdown("---")
    
    # ============================================
    # الخطوة 5: الحفظ
    # ============================================
    st.markdown("### 5️⃣ احفظ كل ده في المكتبة")
    
    total_chapters = len(chapters)
    total_lessons = sum(len(c.get('lessons', [])) for c in chapters)
    
    st.info(f"""
    📊 **اللي هيتحفظ:**
    - 📑 {total_chapters} فصل
    - 📝 {total_lessons} درس
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 احفظ كل ده في المكتبة", type="primary", use_container_width=True):
            save_book_to_library()
    
    with col2:
        if st.button("🗑️ إلغاء والبدء من جديد", use_container_width=True):
            del st.session_state['book_analysis']
            if 'book_subject_id' in st.session_state:
                del st.session_state['book_subject_id']
            st.rerun()


def save_book_to_library():
    """حفظ الكتاب بالكامل في المكتبة"""
    
    analysis = st.session_state.get('book_analysis')
    subject_id = st.session_state.get('book_subject_id')
    
    if not analysis or not subject_id:
        st.error("❌ بيانات ناقصة")
        return
    
    chapters = analysis.get('chapters', [])
    
    if not chapters:
        st.error("❌ مفيش فصول للحفظ")
        return
    
    progress_bar = st.progress(0)
    status = st.empty()
    
    total_items = len(chapters) + sum(len(c.get('lessons', [])) for c in chapters)
    current_item = 0
    
    success_chapters = 0
    success_lessons = 0
    failed_items = []
    
    for chap_idx, chapter in enumerate(chapters):
        current_item += 1
        progress_bar.progress(current_item / total_items, text=f"📑 جاري حفظ: {chapter.get('name', '')}")
        
        # حفظ الفصل
        chap_result = create_chapter(
            subject_id=subject_id,
            name=chapter.get('name', f'الفصل {chap_idx+1}'),
            description=chapter.get('description', ''),
            order=chap_idx
        )
        
        if not chap_result.get('success'):
            failed_items.append(f"الفصل: {chapter.get('name', '')}")
            continue
        
        success_chapters += 1
        chapter_id = chap_result['chapter_id']
        
        # حفظ الدروس
        lessons = chapter.get('lessons', [])
        for less_idx, lesson in enumerate(lessons):
            current_item += 1
            progress_bar.progress(current_item / total_items, text=f"📝 جاري حفظ: {lesson.get('name', '')}")
            
            lesson_result = create_lesson(
                chapter_id=chapter_id,
                name=lesson.get('name', f'الدرس {less_idx+1}'),
                content=lesson.get('content', ''),
                description=lesson.get('description', ''),
                order=less_idx
            )
            
            if lesson_result.get('success'):
                success_lessons += 1
            else:
                failed_items.append(f"الدرس: {lesson.get('name', '')}")
    
    progress_bar.empty()
    status.empty()
    
    # عرض النتيجة
    if success_lessons > 0:
        st.success(f"""
        ✅ **تم الحفظ بنجاح!**
        - 📑 {success_chapters} فصل تم حفظه
        - 📝 {success_lessons} درس تم حفظه
        """)
        
        if failed_items:
            with st.expander(f"⚠️ {len(failed_items)} عنصر فشل"):
                for item in failed_items:
                    st.write(f"- {item}")
        
        # مسح البيانات من session
        del st.session_state['book_analysis']
        if 'book_subject_id' in st.session_state:
            del st.session_state['book_subject_id']
        
        st.balloons()
        
        # رسالة نهائية
        st.success("🎉 الكتاب جاهز في المكتبة! روح للمكتبة الذكية وشوف الدروس")
        
        if st.button("🔄 ارفع كتاب جديد"):
            st.rerun()
    else:
        st.error("❌ فشل الحفظ")
        if failed_items:
            for item in failed_items:
                st.write(f"- {item}")

# ============================================
# ⚡ صفحة الإضافة الذكية (الجديد)
# ============================================

def render_smart_upload_page():
    """صفحة الإضافة الذكية - كل حاجة في خطوة واحدة"""
    
    st.markdown("""
    <div style='background:linear-gradient(135deg, #11998e, #38ef7d);
                color:white; padding:25px; border-radius:18px; text-align:center;
                margin-bottom:25px; box-shadow: 0 10px 30px rgba(17,153,142,0.3);'>
        <h1 style='margin:0;'>⚡ الإضافة الذكية</h1>
        <p style='margin:10px 0 0; opacity:0.95; font-size:16px;'>
            ارفع الكتاب واختار المعلومات.. والباقي علينا! 🚀
        </p>
        <p style='margin:5px 0 0; opacity:0.85; font-size:14px;'>
            هنعمل كل حاجة: المرحلة، الصف، المادة، الفصول، الدروس، والمخرجات!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════
    # الخطوة 1: المرحلة
    # ═══════════════════════════════════════════
    st.markdown("### 🎓 اختار المرحلة")
    
    stage_names = list(STAGES.keys())
    selected_stage = st.selectbox(
        "المرحلة:",
        options=stage_names,
        format_func=lambda x: f"{STAGES[x]['icon']} {STAGES[x]['name']}",
        key="smart_stage"
    )
    
    # ═══════════════════════════════════════════
    # الخطوة 1.5: الكلية (للجامعي فقط)
    # ═══════════════════════════════════════════
    selected_college = None
    
    if selected_stage == 'جامعي':
        st.markdown("### 🏛️ اختار الكلية")
        
        from modules.library.templates import COLLEGES, get_colleges_by_category
        
        # تقسيم حسب التخصص
        colleges_by_cat = get_colleges_by_category()
        
        # عرض الكليات في تابات حسب التخصص
        category_names = list(colleges_by_cat.keys())
        category_icons = {
            'طبي': '⚕️',
            'هندسي': '⚙️',
            'علمي': '🔬',
            'أدبي': '📚',
            'تجاري': '💼',
            'متنوع': '🎓'
        }
        
        # اختيار التخصص
        selected_category = st.radio(
            "التخصص:",
            options=category_names,
            format_func=lambda x: f"{category_icons.get(x, '🎓')} {x}",
            horizontal=True,
            key="smart_category"
        )
        
        # عرض كليات التخصص
        colleges_in_cat = colleges_by_cat[selected_category]
        college_options = {c['name']: c for c in colleges_in_cat}
        
        selected_college_name = st.selectbox(
            "الكلية:",
            options=list(college_options.keys()),
            format_func=lambda x: f"{college_options[x]['icon']} {x}",
            key="smart_college"
        )
        
        selected_college = selected_college_name
        st.success(f"✅ الكلية المختارة: **{selected_college}**")
    
    # ═══════════════════════════════════════════
    # الخطوة 2: الصف/الفرقة
    # ═══════════════════════════════════════════
    st.markdown("### 📖 اختار " + ("الفرقة" if selected_stage == 'جامعي' else "الصف"))
    
    grades_for_stage = get_stage_grades(selected_stage)
    if not grades_for_stage:
        st.warning("⚠️ مفيش صفوف للمرحلة دي")
        return
    
    grade_options = {g['name']: g for g in grades_for_stage}
    selected_grade_name = st.selectbox(
        "الصف/الفرقة:",
        options=list(grade_options.keys()),
        format_func=lambda x: f"{grade_options[x]['icon']} {x}",
        key="smart_grade",
        label_visibility="collapsed"
    )
    
    # ═══════════════════════════════════════════
    # الخطوة 3: الترم والمادة
    # ═══════════════════════════════════════════
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 الترم")
        terms_for_stage = get_terms_for_stage(selected_stage)
        term_options = {t['name']: t for t in terms_for_stage}
        selected_term = st.selectbox(
            "الترم:",
            options=list(term_options.keys()),
            format_func=lambda x: f"{term_options[x]['icon']} {x}",
            key="smart_term",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("### 📚 اسم المادة")
        subject_name = st.text_input(
            "اسم المادة:",
            placeholder="مثال: تشريح" if selected_stage == 'جامعي' else "مثال: دراسات اجتماعية",
            key="smart_subject",
            label_visibility="collapsed"
        )
    
    # عنوان الكتاب
    book_title = st.text_input(
        "📖 عنوان الكتاب (اختياري):",
        placeholder="مثال: كتاب التشريح للفرقة الأولى",
        key="smart_book_title"
    )
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════
    # الخطوة 4: رفع الكتاب
    # ═══════════════════════════════════════════
    st.markdown("### 📤 ارفع الكتاب")
    
    uploaded_file = st.file_uploader(
        "اختار الكتاب:",
        type=['pdf', 'docx', 'txt'],
        help="ارفع الكتاب كامل وAI هيقسمه تلقائياً",
        key="smart_book_uploader"
    )
    
    if uploaded_file:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("📦 الحجم", f"{file_size_mb:.2f} MB")
        with col_b:
            st.metric("📁 النوع", uploaded_file.name.split('.')[-1].upper())
        with col_c:
            st.metric("📄 الاسم", uploaded_file.name[:20])
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════
    # الخطوة 5: خيارات إضافية
    # ═══════════════════════════════════════════
    st.markdown("### ⚙️ خيارات إضافية")
    
    col_x, col_y = st.columns(2)
    
    with col_x:
        auto_generate = st.checkbox(
            "🚀 ولّد كل المخرجات تلقائياً",
            value=True,
            help="هيولّد ملخص + شرح + امتحان + بطاقات + خريطة لكل درس",
            key="smart_auto_gen"
        )
    
    with col_y:
        if uploaded_file and auto_generate:
            estimated_time = get_book_estimated_time(
                num_pages=int(file_size_mb * 50),
                generate_outputs=True
            )
            st.info(f"⏱️ الوقت المتوقع: ~{estimated_time}")
    
    if auto_generate:
        st.markdown("""
        <div style='background:#fff3cd; padding:12px; border-radius:8px; border-right:4px solid #ffc107;'>
            <strong>💡 ملاحظة:</strong> التوليد التلقائي بياخد وقت لكن بيوفر كتير tokens بعد كده!
            <br>كل المستخدمين هيستفيدوا من المخرجات (مرة واحدة بس!)
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════
    # الخطوة 6: التحقق وبدء العملية
    # ═══════════════════════════════════════════
    st.markdown("### 🚀 ابدأ")
    
    # عرض ملخص الاختيارات
    summary_parts = [f"🎓 {selected_stage}"]
    if selected_college:
        summary_parts.append(f"🏛️ {selected_college}")
    summary_parts.append(f"📖 {selected_grade_name}")
    summary_parts.append(f"📅 {selected_term}")
    if subject_name:
        summary_parts.append(f"📚 {subject_name}")
    
    st.info(" | ".join(summary_parts))
    
    # التحقق
    can_start = True
    errors = []
    
    if not subject_name or not subject_name.strip():
        errors.append("❌ اسم المادة مطلوب")
        can_start = False
    
    if not uploaded_file:
        errors.append("❌ ارفع الكتاب الأول")
        can_start = False
    
    if errors:
        for error in errors:
            st.error(error)
    
    # زر البدء
    if can_start:
        if st.button(
            "🚀 ابدأ الإضافة الذكية",
            type="primary",
            use_container_width=True,
            key="smart_start_btn"
        ):
            # استخراج النص
            with st.spinner("📖 جاري قراءة الكتاب..."):
                from utils.file_reader import FileReader
                file_reader = FileReader()
                file_result = file_reader.read(uploaded_file)
            
            if not file_result['success']:
                st.error(f"❌ فشل قراءة الملف: {file_result.get('error', '')}")
                return
            
            book_content = file_result['text']
            
            if not book_content or len(book_content) < 100:
                st.error("❌ محتوى الكتاب قصير جداً")
                return
            
            st.success(f"✅ تم استخراج {len(book_content):,} حرف")
            
            # تجهيز AI
            from utils.ai_engine import AIEngine
            from utils.quiz_generator import QuizGenerator
            
            ai_engine = AIEngine()
            quiz_gen = QuizGenerator(ai_engine) if auto_generate else None
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(progress, message):
                progress_bar.progress(progress, text=message)
                status_text.info(message)
            
            # بدء الإضافة
            with st.spinner("⏳ جاري التنفيذ..."):
                result = smart_upload_book(
                    ai_engine=ai_engine,
                    stage_name=selected_stage,
                    grade_name=selected_grade_name,
                    term=selected_term,
                    subject_name=subject_name.strip(),
                    book_title=book_title.strip() or subject_name,
                    book_content=book_content,
                    college_name=selected_college,  # 🆕
                    auto_generate_outputs=auto_generate,
                    quiz_gen=quiz_gen,
                    progress_callback=update_progress
                )
            
            progress_bar.empty()
            status_text.empty()
            
            # عرض النتيجة
            if result['success']:
                st.balloons()
                
                summary_lines = [
                    f"- 🎓 المرحلة: **{selected_stage}**"
                ]
                if selected_college:
                    summary_lines.append(f"- 🏛️ الكلية: **{selected_college}**")
                summary_lines.extend([
                    f"- 📖 الصف/الفرقة: **{selected_grade_name}**",
                    f"- 📚 المادة: **{subject_name}** ({selected_term})",
                    f"- 📑 الفصول: **{result['chapters_created']}**",
                    f"- 📝 الدروس: **{result['lessons_created']}**",
                    f"- 🚀 المخرجات: **{result['outputs_generated']}**"
                ])
                
                st.success(f"""
                ## 🎉 تم بنجاح!
                
                ### 📊 التقرير:
                {chr(10).join(summary_lines)}
                """)
                
                if result['errors']:
                    with st.expander(f"⚠️ {len(result['errors'])} تحذيرات"):
                        for error in result['errors']:
                            st.warning(error)
                
                st.markdown("---")
                st.info("""
                💡 الكتاب جاهز دلوقتي في المكتبة الذكية!
                
                - 🎓 روح لتاب **"المكتبة الذكية"** (الصف الأول)
                - 📖 اختار: المرحلة → الصف → المادة → الفصل → الدرس
                - ✨ هتلاقي كل المخرجات جاهزة!
                """)
                
                if st.button("➕ ارفع كتاب جديد", use_container_width=True):
                    st.rerun()
            
            else:
                st.error("❌ حصلت مشكلة!")
                if result['errors']:
                    for error in result['errors']:
                        st.error(error)
    
    # شرح
    with st.expander("ℹ️ إزاي بيشتغل ده؟"):
        st.markdown("""
        ### 🤖 الإضافة الذكية بتعمل إيه؟
        
        1. **بتاخد منك**: المرحلة (والكلية لو جامعي)، الصف/الفرقة، الترم، اسم المادة، وملف الكتاب
        
        2. **بتعمل تلقائياً**:
           - ✅ بتشوف لو المرحلة موجودة، لو لأ بتعملها
           - ✅ للجامعي: كل كلية لها مكان منفصل
           - ✅ بتشوف لو الصف/الفرقة موجود، لو لأ بتعمله
           - ✅ بتشوف لو المادة موجودة، لو لأ بتعملها
           - ✅ بتحلل الكتاب بالـ AI
           - ✅ بتقسمه لفصول ودروس
           - ✅ بتحفظ كل ده في المكتبة
        
        3. **لو فعّلت "توليد المخرجات"**:
           - ✅ بتولّد ملخص لكل درس
           - ✅ بتولّد شرح مفصل
           - ✅ بتولّد امتحان
           - ✅ بتولّد بطاقات حفظ
           - ✅ بتولّد خريطة ذهنية
        
        4. **النتيجة**: كل المستخدمين يلاقوا الكتاب جاهز كاملاً! 🎉
        """)