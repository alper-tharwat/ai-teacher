"""
🎭 صفحة الأستاذ الذكي
"""
import streamlit as st
import time
from utils.plan_limits import check_plan_limit, increment_usage
from modules.auth.outputs_manager import (
    save_output, get_cached_output, save_lesson_output,
    get_lesson_output_cached, is_lesson_from_library, get_current_lesson_id
)


def render_avatar_page(ai, voice_gen, avatar_gen):
    if not st.session_state.extracted_text:
        st.warning("⚠️ ارفع ملف أو اختار درس من الفصول")
        return

    st.markdown("## 🎭 الأستاذ الذكي بيشرحلك")

    col1, col2, col3 = st.columns(3)
    with col1:
        characters = avatar_gen.get_characters_list() if hasattr(avatar_gen, 'get_characters_list') else [
            {'key': 'teacher', 'name': '👨‍🏫 أستاذ'},
            {'key': 'doctor', 'name': '👩‍⚕️ دكتورة'},
            {'key': 'student', 'name': '👦 طالب'}
        ]
        character_key = st.selectbox(
            "👤 الشخصية:",
            options=[c['key'] for c in characters],
            format_func=lambda x: next(c['name'] for c in characters if c['key'] == x),
            key="av_char"
        )
    with col2:
        backgrounds = avatar_gen.get_backgrounds_list() if hasattr(avatar_gen, 'get_backgrounds_list') else [
            {'key': 'classroom', 'name': '🏫 فصل'},
            {'key': 'library', 'name': '📚 مكتبة'},
            {'key': 'nature', 'name': '🌳 طبيعة'}
        ]
        bg_key = st.selectbox(
            "🎬 الخلفية:",
            options=[b['key'] for b in backgrounds],
            format_func=lambda x: next(b['name'] for b in backgrounds if b['key'] == x),
            key="av_bg"
        )
    with col3:
        duration = st.selectbox(
            "⏱️ المدة:",
            options=[("short","⚡ قصير"),("medium","📚 متوسط"),("long","🎓 طويل")],
            format_func=lambda x: x[1], index=1, key="av_dur"
        )

    # 🔒 فحص حدود الباقة
    can_do, msg = check_plan_limit("teacher")
    if not can_do:
        st.error(msg)
        if st.button("💎 اترقى لباقة أعلى", key="upgrade_teacher"):
            st.session_state['current_page'] = 'subscriptions'
            st.rerun()
        return
    else:
        st.caption(msg)

    if st.button("🎬 ابدأ", use_container_width=True, key="av_go"):
        with st.spinner("⏳ بيشرح..."):
            try:
                # توليد الشرح
                prompt = f"اشرح الموضوع ده بشكل تفاعلي وممتع:\n\n{st.session_state.extracted_text[:3000]}"
                result = ai.generate(prompt, task_type="explain")
                
                if result and result.get('success'):
                    explanation = result['text']
                    
                    # توليد الصوت
                    voice_result = voice_gen.generate_voice(explanation, character_key)
                    
                    if voice_result and voice_result.get('success'):
                        st.session_state.audio_path = voice_result['audio_path']
                        increment_usage('teacher')
                        
                        # توليد الأفاتار
                        ah = avatar_gen.create_lesson(
                            audio_path=voice_result['audio_path'],
                            character=character_key,
                            background=bg_key,
                            style="animated"
                        ) if hasattr(avatar_gen, 'create_lesson') else None
                        
                        st.session_state.avatar_html = ah or ""
                        st.session_state.stats['teacher_sessions'] += 1
                        st.success("✅ تم التوليد!")
                        
                        # عرض الصوت
                        if voice_result.get('audio_path') and st.session_state.audio_path:
                            st.audio(st.session_state.audio_path, format='audio/mp3')
                        
                        # عرض الأفاتار
                        if st.session_state.avatar_html:
                            st.markdown(st.session_state.avatar_html, unsafe_allow_html=True)
                        
                        # النص
                        st.markdown("### 📝 النص")
                        st.markdown(explanation)
                    else:
                        st.error(f"❌ مشكلة في الصوت: {voice_result.get('error','')}")
                else:
                    st.error("❌ مشكلة في الشرح")
            except Exception as e:
                st.error(f"❌ حصل خطأ: {e}")