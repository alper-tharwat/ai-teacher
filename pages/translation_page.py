"""
🌍 صفحة الترجمة
"""
import streamlit as st
from utils.plan_limits import check_plan_limit, increment_usage


def render_translation_page(ai):
    st.markdown("## 🌍 الترجمة الذكية")

    # النص المدخل
    text_input = st.text_area(
        "✍️ اكتب النص اللي عايز تترجمه:",
        value=st.session_state.get('extracted_text', '')[:2000],
        height=150,
        key="trans_text_input"
    )

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox(
            "🌐 من:",
            options=["auto", "ar", "en", "fr", "de", "es", "tr"],
            format_func=lambda x: {
                "auto":"🤖 كشف تلقائي",
                "ar":"🇪🇬 العربية",
                "en":"🇬🇧 الإنجليزية",
                "fr":"🇫🇷 الفرنسية",
                "de":"🇩🇪 الألمانية",
                "es":"🇪🇸 الإسبانية",
                "tr":"🇹🇷 التركية"
            }[x],
            key="trans_from"
        )
    with col2:
        target_lang = st.selectbox(
            "🎯 إلى:",
            options=["ar", "en", "fr", "de", "es", "tr"],
            format_func=lambda x: {
                "ar":"🇪🇬 العربية",
                "en":"🇬🇧 الإنجليزية",
                "fr":"🇫🇷 الفرنسية",
                "de":"🇩🇪 الألمانية",
                "es":"🇪🇸 الإسبانية",
                "tr":"🇹🇷 التركية"
            }[x],
            key="trans_to"
        )

    # 🔒 فحص حدود الباقة (نستخدم حدود explanations)
    can_do, msg = check_plan_limit("explanations")
    if not can_do:
        st.error(msg)
        if st.button("💎 اترقى لباقة أعلى", key="upgrade_translation"):
            st.session_state['current_page'] = 'subscriptions'
            st.rerun()
        return
    else:
        st.caption(msg)

    if st.button("🌍 ترجم", use_container_width=True, type="primary", key="trans_btn"):
        if not text_input or not text_input.strip():
            st.warning("⚠️ اكتب نص الأول!")
            return

        with st.spinner("⏳ بيترجم..."):
            try:
                prompt = f"ترجم النص التالي من {source_lang} إلى {target_lang}:\n\n{text_input}"
                result = ai.generate(prompt, task_type="translate")

                if result and result.get('success'):
                    translation = result['text']
                    increment_usage('explanations')
                    st.success("✅ تم الترجمة!")

                    # عرض المقارنة
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### 📝 النص الأصلي")
                        st.text_area("", text_input, height=200, key="trans_original", disabled=True)
                    with col2:
                        st.markdown("### 🌍 الترجمة")
                        st.text_area("", translation, height=200, key="trans_result")

                    # زرار النسخ
                    st.code(translation)
                    st.success("✅ تم عرض الترجمة في المربع فوق - انسخها من هنا!")
                else:
                    st.error("❌ مشكلة في الترجمة")
            except Exception as e:
                st.error(f"❌ حصل خطأ: {e}")