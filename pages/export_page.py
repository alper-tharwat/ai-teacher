"""
📥 صفحة تصدير PDF
"""
import streamlit as st
from datetime import datetime


def render_export_page():
    st.markdown("## 📥 تصدير النتائج")

    # التحقق من وجود نتائج
    has_results = any([
        st.session_state.get('summary'),
        st.session_state.get('explanation'),
        st.session_state.get('quiz_data'),
        st.session_state.get('flashcards'),
        st.session_state.get('mindmap_data')
    ])

    if not has_results:
        st.info("📭 مفيش نتائج للتصدير. استخدم الميزات الأول.")
        return

    st.markdown("### 📋 اختار النتائج للتصدير")

    options = []
    if st.session_state.get('summary'):
        options.append("📝 ملخص")
    if st.session_state.get('explanation'):
        options.append("💡 شرح")
    if st.session_state.get('quiz_data'):
        options.append("📋 امتحان")
    if st.session_state.get('flashcards'):
        options.append("🎴 بطاقات")
    if st.session_state.get('mindmap_data'):
        options.append("🧠 خريطة ذهنية")

    selected = st.multiselect("اختار:", options, default=options, key="export_select")

    export_format = st.selectbox(
        "📁 صيغة التصدير:",
        options=["PDF", "Word (DOCX)", "نص (TXT)", "JSON"],
        key="export_format"
    )

    if st.button("📥 صدّر", use_container_width=True, type="primary", key="export_btn"):
        with st.spinner("⏳ بيصدّر..."):
            try:
                from utils.export_manager import ExportManager
                em = ExportManager()

                content = build_export_content(selected)

                if export_format == "PDF":
                    result = em.export_pdf(content)
                elif export_format == "Word (DOCX)":
                    result = em.export_docx(content)
                elif export_format == "نص (TXT)":
                    result = em.export_txt(content)
                else:
                    result = em.export_json(content)

                if result and result.get('success'):
                    st.session_state.stats['pdfs_exported'] += 1
                    st.success("✅ تم التصدير!")

                    # زرار التحميل
                    if result.get('file_path'):
                        with open(result['file_path'], 'rb') as f:
                            ext = {"PDF":"pdf","Word (DOCX)":"docx","نص (TXT)":"txt","JSON":"json"}[export_format]
                            st.download_button(
                                f"⬇️ تحميل {export_format}",
                                f,
                                file_name=f"lesson_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}",
                                mime={"PDF":"application/pdf","Word (DOCX)":"application/vnd.openxmlformats-officedocument.wordprocessingml.document","نص (TXT)":"text/plain","JSON":"application/json"}[export_format]
                            )
                else:
                    st.error(f"❌ {result.get('error','خطأ في التصدير')}")
            except Exception as e:
                st.error(f"❌ حصل خطأ: {e}")


def build_export_content(selected_items):
    """بناء محتوى التصدير من العناصر المختارة"""
    content = {
        'title': 'المعلم الذكي - تصدير الدرس',
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'sections': []
    }

    if "📝 ملخص" in selected_items and st.session_state.get('summary'):
        content['sections'].append({
            'type': 'summary',
            'title': '📝 الملخص',
            'text': st.session_state.summary
        })

    if "💡 شرح" in selected_items and st.session_state.get('explanation'):
        content['sections'].append({
            'type': 'explanation',
            'title': '💡 الشرح المفصل',
            'text': st.session_state.explanation
        })

    if "📋 امتحان" in selected_items and st.session_state.get('quiz_data'):
        quiz = st.session_state.quiz_data
        content['sections'].append({
            'type': 'quiz',
            'title': f'📋 امتحان ({quiz.get("total", 0)} سؤال)',
            'data': quiz
        })

    if "🎴 بطاقات" in selected_items and st.session_state.get('flashcards'):
        content['sections'].append({
            'type': 'flashcards',
            'title': f'🎴 بطاقات الحفظ ({len(st.session_state.flashcards)} بطاقة)',
            'data': st.session_state.flashcards
        })

    if "🧠 خريطة ذهنية" in selected_items and st.session_state.get('mindmap_data'):
        content['sections'].append({
            'type': 'mindmap',
            'title': '🧠 الخريطة الذهنية',
            'data': st.session_state.mindmap_data
        })

    return content