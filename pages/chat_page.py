"""
💬 صفحة الشات الذكي
"""
import streamlit as st
from datetime import datetime
from utils.plan_limits import check_plan_limit, increment_usage


def render_chat_page(ai, voice_gen):
    st.markdown("## 💬 اسأل سؤال")

    # عرض المحادثة السابقة
    if st.session_state.get('chat_history'):
        st.markdown("### 📜 المحادثة")
        for msg in st.session_state.chat_history[-10:]:  # آخر 10 رسايل
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'user':
                st.markdown(f'<div style="background:#e3f2fd;padding:10px;border-radius:10px;margin:5px 0;text-align:right;"><strong>👤 أنت:</strong> {content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background:#f3e5f5;padding:10px;border-radius:10px;margin:5px 0;text-align:right;"><strong>🤖 المعلم:</strong> {content}</div>', unsafe_allow_html=True)

    # مربع السؤال
    question = st.text_area(
        "✍️ اكتب سؤالك:",
        placeholder="مثال: اشرحلي الفرق بين...",
        height=100,
        key="chat_question"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        context = st.checkbox(
            "📚 استخدم النص المرفوع كسياق",
            value=True,
            key="chat_context"
        )
    with col2:
        read_aloud = st.checkbox(
            "🔊 اقرأ الرد",
            value=False,
            key="chat_voice"
        )

    # 🔒 فحص حدود الباقة (نستخدم حدود explanations)
    can_do, msg = check_plan_limit("explanations")
    if not can_do:
        st.error(msg)
        if st.button("💎 اترقى لباقة أعلى", key="upgrade_chat"):
            st.session_state['current_page'] = 'subscriptions'
            st.rerun()
        return
    else:
        st.caption(msg)

    if st.button("🚀 أرسل", use_container_width=True, type="primary", key="chat_send"):
        if not question or not question.strip():
            st.warning("⚠️ اكتب سؤال الأول!")
            return

        with st.spinner("⏳ بيفكر..."):
            try:
                # بناء السياق
                context_text = ""
                if context and st.session_state.get('extracted_text'):
                    context_text = f"بناءً على النص التالي:\n\n{st.session_state.extracted_text[:2000]}\n\n"

                full_prompt = f"{context_text}السؤال: {question}"

                # إرسال للـ AI
                result = ai.generate(full_prompt, task_type="explain")

                if result and result.get('success'):
                    answer = result['text']

                    # حفظ في المحادثة
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': question,
                        'time': datetime.now().isoformat()
                    })
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': answer,
                        'time': datetime.now().isoformat()
                    })

                    st.session_state.stats['questions_asked'] += 1
                    increment_usage('explanations')
                    st.success("✅ تم الرد!")

                    # قراءة الرد بصوت
                    if read_aloud and voice_gen:
                        try:
                            voice_result = voice_gen.generate_voice(answer[:500], "female")
                            if voice_result and voice_result.get('audio_path'):
                                st.audio(voice_result['audio_path'], format='audio/mp3')
                        except Exception as e:
                            st.warning(f"⚠️ مشكلة في الصوت: {e}")

                    # عرض الرد
                    st.markdown("### 📝 الرد:")
                    st.markdown(answer)
                else:
                    st.error("❌ مشكلة في الرد")
            except Exception as e:
                st.error(f"❌ حصل خطأ: {e}")