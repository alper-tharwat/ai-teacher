"""
📚 Library Page - صفحة المكتبة للمستخدم
"""
import streamlit as st
import requests
import tempfile
from pathlib import Path
from .library_manager import LibraryManager


def render_library_page(file_reader):
    """صفحة المكتبة الرئيسية"""

    st.markdown("## 📚 مكتبة الكتب التعليمية")
    st.markdown("اختار كتابك من المكتبة وابدأ المذاكرة فوراً!")

    manager = LibraryManager()
    stats = manager.get_statistics()

    # ═══════════════════════════════════════════
    # إحصائيات سريعة
    # ═══════════════════════════════════════════
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
    # البحث السريع
    # ═══════════════════════════════════════════
    with st.expander("🔍 بحث سريع", expanded=False):
        search_query = st.text_input(
            "ابحث في الكتب:",
            placeholder="اكتب اسم الكتاب أو المادة...",
            key="lib_search"
        )

        if search_query:
            results = manager.search_books(search_query)
            if results:
                st.success(f"✅ تم العثور على {len(results)} كتاب")
                for book in results[:10]:
                    with st.container():
                        st.markdown(f"""
                        <div style="background:white;padding:15px;border-radius:10px;
                                    margin:8px 0;border-right:4px solid #667eea;direction:rtl;">
                            <strong>📕 {book['title']}</strong><br>
                            <small>📚 {book['stage']} | 📓 {book['grade']} | 📖 {book['subject']}</small>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.button(f"📥 تحميل ودراسة", key=f"search_load_{book['id']}"):
                            load_and_study_book(book, file_reader)
            else:
                st.warning("⚠️ مفيش نتائج")

    st.markdown("---")

    # ═══════════════════════════════════════════
    # اختيار المرحلة → السنة → المادة → الكتاب
    # ═══════════════════════════════════════════

    # المرحلة
    st.markdown("### 🎓 اختار المرحلة")
    stages = manager.get_all_stages()

    if not stages:
        st.warning("⚠️ مفيش مراحل دراسية - أضف من لوحة الأدمن")
        return

    # عرض المراحل كـ buttons
    stage_cols = st.columns(len(stages))
    for i, stage in enumerate(stages):
        with stage_cols[i]:
            count = stats["by_stage"].get(stage["name"], 0)
            if st.button(
                f"{stage['icon']}\n{stage['name']}\n({count} كتاب)",
                use_container_width=True,
                key=f"stage_{stage['name']}"
            ):
                st.session_state.lib_selected_stage = stage["name"]
                st.session_state.lib_selected_grade = None
                st.session_state.lib_selected_subject = None
                st.rerun()

    selected_stage = st.session_state.get("lib_selected_stage")

    if not selected_stage:
        st.info("👆 اختار مرحلة دراسية للبدء")
        return

    st.markdown("---")
    st.success(f"✅ المرحلة المختارة: **{selected_stage}**")

    # السنة
    st.markdown("### 📓 اختار السنة الدراسية")
    grades = manager.get_grades(selected_stage)

    if not grades:
        st.warning("⚠️ مفيش سنوات في هذه المرحلة")
        return

    selected_grade = st.selectbox(
        "السنة:",
        options=grades,
        index=grades.index(st.session_state.lib_selected_grade) if st.session_state.get("lib_selected_grade") in grades else 0,
        key="lib_grade_select"
    )

    if selected_grade != st.session_state.get("lib_selected_grade"):
        st.session_state.lib_selected_grade = selected_grade
        st.session_state.lib_selected_subject = None
        st.rerun()

    # المادة
    st.markdown("### 📖 اختار المادة")
    subjects = manager.get_subjects(selected_stage, selected_grade)

    if not subjects:
        st.warning(f"⚠️ مفيش مواد في {selected_grade} - أضف من لوحة الأدمن")
        return

    selected_subject = st.selectbox(
        "المادة:",
        options=subjects,
        index=subjects.index(st.session_state.lib_selected_subject) if st.session_state.get("lib_selected_subject") in subjects else 0,
        key="lib_subject_select"
    )

    st.session_state.lib_selected_subject = selected_subject

    # الكتب
    st.markdown("### 📕 الكتب المتاحة")
    books = manager.get_books(selected_stage, selected_grade, selected_subject)

    if not books:
        st.warning(f"⚠️ مفيش كتب في {selected_subject} - أضف من لوحة الأدمن")
        return

    st.success(f"📚 {len(books)} كتاب متاح")

    for book in books:
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#667eea,#764ba2);
                            color:white;padding:20px;border-radius:15px;
                            margin:10px 0;direction:rtl;">
                    <h3 style="margin:0;">📕 {book['title']}</h3>
                    <p style="margin:10px 0 5px 0;opacity:0.9;">
                        ✍️ {book.get('author', 'غير محدد')} | 📅 {book.get('year', 'N/A')}
                    </p>
                    {f"<p style='margin:5px 0;opacity:0.9;font-size:14px;'>{book['description']}</p>" if book.get('description') else ""}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(
                    "📥 تحميل ودراسة",
                    key=f"load_book_{book['id']}",
                    use_container_width=True,
                    type="primary"
                ):
                    load_and_study_book(book, file_reader)


def load_and_study_book(book: dict, file_reader):
    """تحميل كتاب وتجهيزه للدراسة"""

    book_url = book.get('url', '').strip()

    if not book_url:
        st.error("❌ مفيش لينك للكتاب!")
        return

    # تحويل لينك Google Drive لـ direct download
    if 'drive.google.com' in book_url:
        book_url = convert_gdrive_url(book_url)

    progress = st.progress(0, text="⏳ جاري تحميل الكتاب...")

    try:
        # تحميل الملف
        progress.progress(30, text="📥 جاري التحميل من السيرفر...")
        response = requests.get(book_url, timeout=60, stream=True)

        if response.status_code != 200:
            progress.empty()
            st.error(f"❌ فشل التحميل (Status: {response.status_code})")
            return

        # حفظ في ملف مؤقت
        progress.progress(60, text="💾 جاري الحفظ المؤقت...")

        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)

        # تحديد امتداد الملف من الـ URL أو الـ Content-Type
        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' in content_type or book_url.lower().endswith('.pdf'):
            ext = '.pdf'
        else:
            ext = '.pdf'  # افتراضي

        safe_title = "".join(c for c in book['title'] if c.isalnum() or c in " _-")[:50]
        temp_path = temp_dir / f"book_{book['id']}_{safe_title}{ext}"

        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # قراءة الملف
        progress.progress(80, text="📖 جاري قراءة الكتاب...")

        # محاكاة UploadedFile لـ Streamlit
        class FakeUploadedFile:
            def __init__(self, path, name):
                self.path = path
                self.name = name
                self.size = path.stat().st_size
                self._file = open(path, 'rb')

            def read(self):
                return self._file.read()

            def seek(self, pos):
                self._file.seek(pos)

            def getvalue(self):
                self.seek(0)
                return self._file.read()

            def close(self):
                self._file.close()

        fake_file = FakeUploadedFile(temp_path, f"{safe_title}{ext}")
        result = file_reader.read(fake_file)
        fake_file.close()

        # حذف الملف المؤقت
        try:
            temp_path.unlink()
        except Exception:
            pass

        progress.progress(100, text="✅ تم!")

        if result['success']:
            # حفظ في session state
            st.session_state.file_info = result['file_info']
            st.session_state.file_info['name'] = book['title']
            st.session_state.all_pages = result.get('pages', [])
            st.session_state.total_pages = result.get('total_pages', 0)
            st.session_state.stats['files_processed'] += 1

            total = st.session_state.total_pages
            chunk = st.session_state.chunk_size

            if total <= chunk:
                st.session_state.extracted_text = result['text']
                st.session_state.selected_range = (1, total) if total > 0 else None
            else:
                st.session_state.extracted_text = ''
                st.session_state.selected_range = None

            # مسح المحتوى القديم
            st.session_state.summary = ''
            st.session_state.explanation = ''
            st.session_state.quiz_data = None
            st.session_state.flashcards = []
            st.session_state.mindmap_data = None

            progress.empty()
            st.success(f"""
            ✅ **تم تحميل الكتاب بنجاح!**
            - 📕 {book['title']}
            - 📄 {total} صفحة
            - 📝 {result.get('word_count', 0):,} كلمة
            """)

            if total > chunk:
                st.warning(f"⚠️ الكتاب كبير - روح لتاب 'رفع ملف' لاختيار النطاق")
            else:
                st.info("💡 روح لباقي التابات للمذاكرة!")

            st.balloons()

        else:
            progress.empty()
            st.error(f"❌ {result.get('error', 'مشكلة في القراءة')}")

    except requests.Timeout:
        progress.empty()
        st.error("⏱️ انتهت المهلة - الملف كبير جداً أو الاتصال بطيء")
    except Exception as e:
        progress.empty()
        st.error(f"❌ خطأ: {str(e)}")


def convert_gdrive_url(url: str) -> str:
    """تحويل لينك Google Drive لـ direct download"""
    # https://drive.google.com/file/d/FILE_ID/view
    # → https://drive.google.com/uc?export=download&id=FILE_ID

    if '/file/d/' in url:
        try:
            file_id = url.split('/file/d/')[1].split('/')[0]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        except Exception:
            return url

    if 'id=' in url:
        return url  # already direct

    return url