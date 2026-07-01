"""
📺 صفحة تحميل من YouTube
"""
import streamlit as st
from utils.plan_limits import check_plan_limit, increment_usage


def render_youtube_page(ai):
    st.markdown("## 📺 تحميل من YouTube")

    st.info("📌 الصق رابط فيديو YouTube وهنحمله ونلخّصه لك!")

    url = st.text_input(
        "🔗 رابط الفيديو:",
        placeholder="https://www.youtube.com/watch?v=...",
        key="yt_url"
    )

    col1, col2 = st.columns(2)
    with col1:
        download_type = st.selectbox(
            "📥 نوع التحميل:",
            options=["audio", "video"],
            format_func=lambda x: {"audio":"🎵 صوت فقط","video":"🎬 فيديو"}[x],
            key="yt_type"
        )
    with col2:
        language = st.selectbox(
            "🌐 لغة الترجمة:",
            options=["auto", "ar", "en"],
            format_func=lambda x: {"auto":"🤖 تلقائي","ar":"🇪🇬 عربي","en":"🇬🇧 إنجليزي"}[x],
            key="yt_lang"
        )

    # 🔒 فحص حدود الباقة (نستخدم حدود files)
    can_do, msg = check_plan_limit("files")
    if not can_do:
        st.error(msg)
        if st.button("💎 اترقى لباقة أعلى", key="upgrade_youtube"):
            st.session_state['current_page'] = 'subscriptions'
            st.rerun()
        return
    else:
        st.caption(msg)

    if st.button("📥 حمل ولخّص", use_container_width=True, type="primary", key="yt_download"):
        if not url or not url.strip():
            st.warning("⚠️ الصق رابط الأول!")
            return

        with st.spinner("⏳ بيحمل..."):
            try:
                from utils.youtube_handler import YouTubeHandler
                yh = YouTubeHandler()
                
                result = yh.download_and_process(
                    url=url,
                    download_type=download_type,
                    language=language
                )
                
                if result and result.get('success'):
                    st.session_state.extracted_text = result['text']
                    st.session_state.stats['files_processed'] += 1
                    increment_usage('files')
                    st.success("✅ تم التحميل والتلخيص!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("📄 العنوان", result.get('title', 'بدون عنوان')[:30])
                    with col2:
                        st.metric("⏱️ المدة", f"{result.get('duration', 0)//60} دقيقة")
                    with col3:
                        st.metric("📝 الكلمات", result.get('word_count', 0))
                    
                    st.info("💡 روح لتاب الشرح عشان تبدأ!")
                else:
                    st.error(f"❌ {result.get('error','خطأ في التحميل')}")
            except Exception as e:
                st.error(f"❌ حصل خطأ: {e}")