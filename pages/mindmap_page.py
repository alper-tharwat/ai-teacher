"""
🧠 صفحة الخرائط الذهنية
"""
import streamlit as st
import json
from utils.plan_limits import check_plan_limit, increment_usage
from modules.auth.outputs_manager import (
    save_output, get_cached_output, save_lesson_output,
    get_lesson_output_cached, is_lesson_from_library, get_current_lesson_id
)


def render_mindmap_page(ai):
    if not st.session_state.extracted_text:
        st.warning("⚠️ ارفع ملف أو اختار درس من الفصول")
        return

    st.markdown("## 🧠 الخرائط الذهنية")

    col1, col2 = st.columns(2)
    with col1:
        depth_level = st.selectbox(
            "مستوى التفصيل:",
            options=["simple", "normal", "detailed"],
            format_func=lambda x: {"simple":"🟢 بسيط","normal":"🟡 متوسط","detailed":"🔴 مفصل"}[x],
            index=1, key="mm_depth"
        )
    with col2:
        map_style = st.selectbox(
            "🎨 ستايل الألوان:",
            options=["default", "colorful", "dark", "minimal"],
            index=0, key="mm_style"
        )

    # 🔒 فحص حدود الباقة
    can_do, msg = check_plan_limit("mindmaps")
    if not can_do:
        st.error(msg)
        if st.button("💎 اترقى لباقة أعلى", key="upgrade_mindmap"):
            st.session_state['current_page'] = 'subscriptions'
            st.rerun()
        return
    else:
        st.caption(msg)

    # فحص الكاش
    cached = get_cached_mindmap({'depth': depth_level, 'style': map_style})
    if cached:
        st.session_state.mindmap_data = cached
        st.success("⚡ تم التحميل من الكاش!")

    if st.button("🧠 ولّد الخريطة", use_container_width=True, type="primary", key="mm_gen"):
        if cached:
            st.rerun()
        else:
            with st.spinner("⏳..."):
                try:
                    from utils.mindmap_generator import MindMapGenerator
                    mm_gen = MindMapGenerator(ai)
                    
                    result = mm_gen.generate(
                        st.session_state.extracted_text,
                        depth=depth_level,
                        style=map_style
                    )
                    
                    if result and result.get('success'):
                        st.session_state.mindmap_data = result['data']
                        st.session_state.mindmap_markdown = result.get('markdown', '')
                        st.session_state.stats['mindmaps_made'] += 1
                        increment_usage('mindmaps')
                        save_mindmap_to_cache(result['data'], {'depth': depth_level, 'style': map_style})
                        st.success("✅ تم توليد الخريطة!")
                    else:
                        st.error("❌ جرب تاني")
                except Exception as e:
                    st.error(f"❌ حصل خطأ: {e}")

    if st.session_state.mindmap_data:
        render_mindmap_display()


def get_cached_mindmap(settings):
    """جلب خريطة من الكاش"""
    is_from_library = is_lesson_from_library()
    if is_from_library:
        lesson_id = get_current_lesson_id()
        return get_lesson_output_cached(lesson_id=lesson_id, output_type='mindmap', settings=settings)
    else:
        current_file_id = st.session_state.get('current_file_id')
        if current_file_id:
            return get_cached_output(file_id=current_file_id, output_type='mindmap', settings=settings)
    return None


def save_mindmap_to_cache(content, settings):
    """حفظ خريطة في الكاش"""
    is_from_library = is_lesson_from_library()
    if is_from_library:
        lesson_id = get_current_lesson_id()
        save_lesson_output(lesson_id=lesson_id, output_type='mindmap', content=content, settings=settings)
    else:
        current_file_id = st.session_state.get('current_file_id')
        if current_file_id:
            save_output(file_id=current_file_id, output_type='mindmap', content=content, settings=settings)


def render_mindmap_display():
    """عرض الخريطة الذهنية"""
    st.markdown("---")
    st.markdown("### 🧠 خريطتك الذهنية")
    
    data = st.session_state.mindmap_data
    
    # عرض تفاعلي بـ D3.js
    try:
        if isinstance(data, dict):
            # JSON format
            st.json(data)
        elif isinstance(data, str):
            # Markdown format
            st.markdown(data)
        else:
            st.write(data)
    except Exception as e:
        st.warning(f"⚠️ مشكلة في العرض: {e}")
        st.write(data)
    
    # زرار التصدير
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 نسخ النص", use_container_width=True):
            st.code(st.session_state.get('mindmap_markdown', str(data)))
            st.success("✅ تم النسخ!")
    with col2:
        if st.button("🖼️ حفظ كصورة", use_container_width=True):
            st.info("⏳ قريباً...")