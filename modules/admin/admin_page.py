"""
👨‍💼 Admin Page - لوحة تحكم الأدمن
"""
import streamlit as st
from datetime import datetime
import sys
import os

# عشان نقدر نستورد من library
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library.library_manager import LibraryManager


# ═══════════════════════════════════════════
# 🔐 بيانات الأدمن
# ═══════════════════════════════════════════
ADMIN_USERNAME = "alper"
ADMIN_PASSWORD = "Alp1357951@#"


def check_admin_auth():
    """التحقق من تسجيل دخول الأدمن"""
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False

    return st.session_state.is_admin


def render_admin_page():
    """صفحة الأدمن الرئيسية"""

    # ═══════════════════════════════════════════
    # تسجيل الدخول
    # ═══════════════════════════════════════════
    if not check_admin_auth():
        render_login_page()
        return

    # ═══════════════════════════════════════════
    # لوحة التحكم
    # ═══════════════════════════════════════════
    render_admin_dashboard()


def render_login_page():
    """صفحة تسجيل دخول الأدمن"""

    st.markdown("""
    <div style="background:linear-gradient(135deg,#667eea,#764ba2);
                color:white;padding:30px;border-radius:20px;
                text-align:center;direction:rtl;margin-bottom:30px;">
        <h1 style="margin:0;">🔐 لوحة تحكم الأدمن</h1>
        <p style="margin:10px 0 0 0;opacity:0.9;">
            دخول خاص لإدارة المكتبة
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("### 🔑 سجّل دخول")

        username = st.text_input("اسم المستخدم:", key="admin_user")
        password = st.text_input("كلمة السر:", type="password", key="admin_pass")

        if st.button("🚀 دخول", use_container_width=True, type="primary"):
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.success("✅ تم تسجيل الدخول!")
                st.rerun()
            else:
                st.error("❌ بيانات خاطئة!")

        st.markdown("---")
        st.caption("⚠️ هذه الصفحة للأدمن فقط")


def render_admin_dashboard():
    """لوحة تحكم الأدمن الرئيسية"""

    manager = LibraryManager()

    # ═══════════════════════════════════════════
    # Header مع زرار تسجيل خروج
    # ═══════════════════════════════════════════
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#11998e,#38ef7d);
                    color:white;padding:20px;border-radius:15px;
                    direction:rtl;">
            <h2 style="margin:0;">👨‍💼 لوحة تحكم الأدمن</h2>
            <p style="margin:5px 0 0 0;opacity:0.9;">
                مرحباً {ADMIN_USERNAME} 👋
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 خروج", use_container_width=True):
            st.session_state.is_admin = False
            st.rerun()

    st.markdown("---")

    # ═══════════════════════════════════════════
    # الإحصائيات
    # ═══════════════════════════════════════════
    stats = manager.get_statistics()

    st.markdown("### 📊 إحصائيات المكتبة")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 إجمالي الكتب", stats["total_books"])
    with col2:
        st.metric("🎓 المراحل", stats["total_stages"])
    with col3:
        st.metric("📓 السنوات", stats["total_grades"])
    with col4:
        st.metric("📖 المواد", stats["total_subjects"])

    st.markdown("---")

    # ═══════════════════════════════════════════
    # تابات الأدمن
    # ═══════════════════════════════════════════
    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ إضافة كتاب",
        "📚 عرض/حذف الكتب",
        "📖 إدارة المواد",
        "🔧 الإعدادات"
    ])

    with tab1:
        render_add_book_tab(manager)

    with tab2:
        render_view_books_tab(manager)

    with tab3:
        render_subjects_tab(manager)

    with tab4:
        render_settings_tab(manager)


# ═══════════════════════════════════════════
# ➕ تاب إضافة كتاب
# ═══════════════════════════════════════════
def render_add_book_tab(manager: LibraryManager):
    """تاب إضافة كتاب جديد"""

    st.markdown("### ➕ إضافة كتاب جديد")

    col1, col2 = st.columns(2)

    with col1:
        stages = [s["name"] for s in manager.get_all_stages()]
        if not stages:
            st.error("❌ مفيش مراحل!")
            return

        stage = st.selectbox("🎓 المرحلة:", options=stages, key="add_stage")

    with col2:
        grades = manager.get_grades(stage)
        if not grades:
            st.error("❌ مفيش سنوات!")
            return

        grade = st.selectbox("📓 السنة:", options=grades, key="add_grade")

    # المادة (يقدر يختار موجودة أو يضيف جديدة)
    col1, col2 = st.columns(2)

    with col1:
        existing_subjects = manager.get_subjects(stage, grade)
        subject_mode = st.radio(
            "نوع المادة:",
            options=["موجودة", "جديدة"],
            horizontal=True,
            key="subject_mode"
        )

    with col2:
        if subject_mode == "موجودة" and existing_subjects:
            subject = st.selectbox("📖 المادة:", options=existing_subjects, key="add_subject_existing")
        else:
            subject = st.text_input(
                "📖 اسم المادة الجديدة:",
                placeholder="مثال: اللغة العربية",
                key="add_subject_new"
            )

    st.markdown("---")
    st.markdown("### 📕 بيانات الكتاب")

    title = st.text_input(
        "📕 عنوان الكتاب:",
        placeholder="مثال: كتاب اللغة العربية - الترم الأول",
        key="add_title"
    )

    col1, col2 = st.columns(2)
    with col1:
        author = st.text_input(
            "✍️ المؤلف (اختياري):",
            placeholder="وزارة التربية والتعليم",
            key="add_author"
        )

    with col2:
        year = st.number_input(
            "📅 سنة الإصدار:",
            min_value=2000,
            max_value=2030,
            value=2024,
            step=1,
            key="add_year"
        )

    description = st.text_area(
        "📝 الوصف (اختياري):",
        placeholder="وصف مختصر للكتاب...",
        height=100,
        key="add_description"
    )

    st.markdown("### 🔗 رابط الكتاب")
    st.info("""
    💡 **كيفية الحصول على رابط من Google Drive:**
    1. ارفع الملف على Google Drive
    2. كليك يمين → Share → "Anyone with the link"
    3. انسخ اللينك والصقه هنا
    """)

    url = st.text_input(
        "🔗 رابط الكتاب:",
        placeholder="https://drive.google.com/file/d/...",
        key="add_url"
    )

    st.markdown("")

    if st.button("✅ إضافة الكتاب", use_container_width=True, type="primary"):
        # التحقق من البيانات
        if not title.strip():
            st.error("❌ عنوان الكتاب مطلوب!")
            return

        if not subject or not subject.strip():
            st.error("❌ اسم المادة مطلوب!")
            return

        if not url.strip():
            st.error("❌ رابط الكتاب مطلوب!")
            return

        # إضافة المادة لو جديدة
        if subject_mode == "جديدة":
            result = manager.add_subject(stage, grade, subject.strip())
            if not result["success"] and "موجودة" not in result.get("error", ""):
                st.error(f"❌ {result['error']}")
                return

        # إضافة الكتاب
        result = manager.add_book(
            stage=stage,
            grade=grade,
            subject=subject.strip(),
            title=title.strip(),
            url=url.strip(),
            author=author.strip(),
            year=year,
            description=description.strip()
        )

        if result["success"]:
            st.success(f"✅ تم إضافة الكتاب بنجاح!")
            st.info(f"🆔 ID الكتاب: `{result['book_id']}`")
            st.balloons()
        else:
            st.error(f"❌ {result['error']}")


# ═══════════════════════════════════════════
# 📚 تاب عرض/حذف الكتب
# ═══════════════════════════════════════════
def render_view_books_tab(manager: LibraryManager):
    """تاب عرض وحذف الكتب"""

    st.markdown("### 📚 جميع الكتب")

    col1, col2, col3 = st.columns(3)

    with col1:
        stages = [s["name"] for s in manager.get_all_stages()]
        filter_stage = st.selectbox(
            "🎓 فلتر بالمرحلة:",
            options=["الكل"] + stages,
            key="filter_stage"
        )

    with col2:
        if filter_stage != "الكل":
            grades = manager.get_grades(filter_stage)
            filter_grade = st.selectbox(
                "📓 فلتر بالسنة:",
                options=["الكل"] + grades,
                key="filter_grade"
            )
        else:
            filter_grade = "الكل"

    with col3:
        if filter_stage != "الكل" and filter_grade != "الكل":
            subjects = manager.get_subjects(filter_stage, filter_grade)
            filter_subject = st.selectbox(
                "📖 فلتر بالمادة:",
                options=["الكل"] + subjects,
                key="filter_subject"
            )
        else:
            filter_subject = "الكل"

    st.markdown("---")

    # جمع كل الكتب
    all_books = []
    data = manager._load_database()

    for stage_name, stage_data in data.get("stages", {}).items():
        if filter_stage != "الكل" and stage_name != filter_stage:
            continue

        for grade_name, grade_data in stage_data.get("grades", {}).items():
            if filter_grade != "الكل" and grade_name != filter_grade:
                continue

            for subject_name, books in grade_data.get("subjects", {}).items():
                if filter_subject != "الكل" and subject_name != filter_subject:
                    continue

                for book in books:
                    all_books.append({
                        **book,
                        "stage": stage_name,
                        "grade": grade_name,
                        "subject": subject_name
                    })

    if not all_books:
        st.warning("⚠️ مفيش كتب مطابقة للفلتر")
        return

    st.success(f"📚 {len(all_books)} كتاب")

    for book in all_books:
        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"""
                <div style="background:white;padding:15px;border-radius:10px;
                            margin:10px 0;border-right:4px solid #667eea;direction:rtl;
                            box-shadow:0 2px 5px rgba(0,0,0,0.05);">
                    <h4 style="margin:0;color:#2c3e50;">📕 {book['title']}</h4>
                    <p style="margin:5px 0;color:#666;font-size:13px;">
                        🎓 {book['stage']} | 📓 {book['grade']} | 📖 {book['subject']}
                    </p>
                    <p style="margin:5px 0;color:#888;font-size:12px;">
                        ✍️ {book.get('author', 'غير محدد')} | 📅 {book.get('year', 'N/A')} | 🆔 {book['id']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("<br>", unsafe_allow_html=True)

                if st.button(
                    "🗑️ حذف",
                    key=f"delete_book_{book['id']}",
                    use_container_width=True
                ):
                    # تأكيد قبل الحذف
                    st.session_state[f"confirm_delete_{book['id']}"] = True
                    st.rerun()

                # نافذة التأكيد
                if st.session_state.get(f"confirm_delete_{book['id']}", False):
                    st.warning("⚠️ متأكد؟")
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.button("✅ آه", key=f"yes_{book['id']}"):
                            result = manager.delete_book(book['id'])
                            if result["success"]:
                                st.success("✅ تم الحذف!")
                                st.session_state[f"confirm_delete_{book['id']}"] = False
                                st.rerun()
                            else:
                                st.error(f"❌ {result['error']}")
                    with col_no:
                        if st.button("❌ لا", key=f"no_{book['id']}"):
                            st.session_state[f"confirm_delete_{book['id']}"] = False
                            st.rerun()


# ═══════════════════════════════════════════
# 📖 تاب إدارة المواد
# ═══════════════════════════════════════════
def render_subjects_tab(manager: LibraryManager):
    """تاب إدارة المواد"""

    st.markdown("### 📖 إدارة المواد")

    col1, col2 = st.columns(2)

    with col1:
        stages = [s["name"] for s in manager.get_all_stages()]
        stage = st.selectbox("🎓 المرحلة:", options=stages, key="sub_stage")

    with col2:
        grades = manager.get_grades(stage)
        grade = st.selectbox("📓 السنة:", options=grades, key="sub_grade")

    st.markdown("---")

    # عرض المواد الموجودة
    subjects = manager.get_subjects(stage, grade)

    if subjects:
        st.markdown(f"#### 📋 المواد الموجودة ({len(subjects)})")

        for subject in subjects:
            books = manager.get_books(stage, grade, subject)
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"""
                <div style="background:white;padding:12px;border-radius:8px;
                            margin:5px 0;direction:rtl;border-right:3px solid #667eea;">
                    <strong>📖 {subject}</strong>
                    <span style="color:#888;font-size:13px;"> ({len(books)} كتاب)</span>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                if st.button("🗑️", key=f"del_sub_{subject}", help="حذف المادة وكل كتبها"):
                    if st.session_state.get(f"confirm_del_sub_{subject}", False):
                        result = manager.delete_subject(stage, grade, subject)
                        if result["success"]:
                            st.success("✅ تم الحذف!")
                            st.session_state[f"confirm_del_sub_{subject}"] = False
                            st.rerun()
                        else:
                            st.error(f"❌ {result['error']}")
                    else:
                        st.session_state[f"confirm_del_sub_{subject}"] = True
                        st.warning("⚠️ اضغط مرة تانية للتأكيد")
                        st.rerun()
    else:
        st.info("ℹ️ مفيش مواد - أضف من الأسفل")

    st.markdown("---")

    # إضافة مادة جديدة
    st.markdown("#### ➕ إضافة مادة جديدة")

    new_subject = st.text_input(
        "اسم المادة:",
        placeholder="مثال: اللغة العربية",
        key="new_subject_input"
    )

    if st.button("➕ إضافة المادة", use_container_width=True):
        if new_subject and new_subject.strip():
            result = manager.add_subject(stage, grade, new_subject.strip())
            if result["success"]:
                st.success(f"✅ تم إضافة '{new_subject}'!")
                st.rerun()
            else:
                st.error(f"❌ {result['error']}")
        else:
            st.warning("⚠️ اكتب اسم المادة!")


# ═══════════════════════════════════════════
# 🔧 تاب الإعدادات
# ═══════════════════════════════════════════
def render_settings_tab(manager: LibraryManager):
    """تاب الإعدادات والصيانة"""

    st.markdown("### 🔧 إعدادات وصيانة")

    data = manager._load_database()
    metadata = data.get("metadata", {})

    st.markdown("#### 📊 معلومات قاعدة البيانات")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📅 آخر تحديث", metadata.get("last_updated", "غير معروف"))
    with col2:
        st.metric("📚 إجمالي الكتب", metadata.get("total_books", 0))

    st.markdown("---")

    st.markdown("#### 💾 تصدير قاعدة البيانات")

    if st.button("📥 تصدير JSON", use_container_width=True):
        import json
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        st.download_button(
            "⬇️ تحميل الملف",
            data=json_str,
            file_name=f"library_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

    st.markdown("---")

    st.markdown("#### ⚠️ منطقة الخطر")

    with st.expander("🚨 خيارات متقدمة"):
        st.warning("⚠️ هذه العمليات لا يمكن التراجع عنها!")

        if st.button("🗑️ مسح كل الكتب (الإبقاء على الهيكل)", type="secondary"):
            if st.session_state.get("confirm_clear_all", False):
                # مسح كل الكتب من كل المواد
                cleared_data = data.copy()
                for stage_data in cleared_data.get("stages", {}).values():
                    for grade_data in stage_data.get("grades", {}).values():
                        grade_data["subjects"] = {}

                manager._save_database(cleared_data)
                st.success("✅ تم المسح!")
                st.session_state["confirm_clear_all"] = False
                st.rerun()
            else:
                st.session_state["confirm_clear_all"] = True
                st.error("⚠️ اضغط مرة تانية للتأكيد - هتمسح كل الكتب!")