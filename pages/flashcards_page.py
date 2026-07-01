"""
🎴 صفحة بطاقات الحفظ
"""
import streamlit as st
from utils.plan_limits import check_plan_limit, increment_usage
from modules.auth.outputs_manager import (
    save_output, get_cached_output, save_lesson_output,
    get_lesson_output_cached, is_lesson_from_library, get_current_lesson_id
)


def render_flashcards_page(ai):
    if not st.session_state.extracted_text:
        st.warning("⚠️ ارفع ملف أو اختار درس من الفصول")
        return

    st.markdown("## 🎴 بطاقات الحفظ")

    col_b1, col_b2 = st.columns([3, 1])
    with col_b1:
        # 🔒 فحص حدود الباقة
        can_do, msg = check_plan_limit("flashcards")
        if not can_do:
            st.error(msg)
            if st.button("💎 اترقى لباقة أعلى", key="upgrade_flashcards"):
                st.session_state['current_page'] = 'subscriptions'
                st.rerun()
            return
        else:
            st.caption(msg)

        gen_btn = st.button("🚀 ولّد البطاقات", use_container_width=True, type="primary", key="fc_gen")
    with col_b2:
        if st.session_state.flashcards:
            if st.button("🔄 من الأول", use_container_width=True, key="fc_reset"):
                st.session_state.current_card_idx = 0
                st.session_state.show_answer = False
                st.rerun()

    if gen_btn:
        # فحص الكاش
        cached = get_cached_flashcards()
        if cached:
            st.session_state.flashcards = cached
            st.session_state.current_card_idx = 0
            st.session_state.show_answer = False
            st.success(f"⚡ تم التحميل من الكاش! ({len(cached)} بطاقة)")
        else:
            with st.spinner("⏳..."):
                from utils.quiz_generator import QuizGenerator
                qg = QuizGenerator(ai)
                res = qg.generate_flashcards(st.session_state.extracted_text)
                
                if res and res.get('success'):
                    st.session_state.flashcards = res['cards']
                    st.session_state.current_card_idx = 0
                    st.session_state.show_answer = False
                    st.session_state.stats['flashcards_done'] += res['total']
                    increment_usage('flashcards')
                    save_flashcards_to_cache(res['cards'])
                    st.success(f"✅ تم توليد {res['total']} بطاقة!")
                else:
                    st.error("❌ جرب تاني")

    if st.session_state.flashcards:
        render_flashcard_ui()


def get_cached_flashcards():
    """جلب بطاقات من الكاش"""
    is_from_library = is_lesson_from_library()
    if is_from_library:
        lesson_id = get_current_lesson_id()
        return get_lesson_output_cached(lesson_id=lesson_id, output_type='flashcards', settings={})
    else:
        current_file_id = st.session_state.get('current_file_id')
        if current_file_id:
            return get_cached_output(file_id=current_file_id, output_type='flashcards', settings={})
    return None


def save_flashcards_to_cache(cards):
    """حفظ بطاقات في الكاش"""
    is_from_library = is_lesson_from_library()
    if is_from_library:
        lesson_id = get_current_lesson_id()
        save_lesson_output(lesson_id=lesson_id, output_type='flashcards', content=cards, settings={})
    else:
        current_file_id = st.session_state.get('current_file_id')
        if current_file_id:
            save_output(file_id=current_file_id, output_type='flashcards', content=cards, settings={})


def render_flashcard_ui():
    """عرض البطاقة التفاعلية"""
    cards = st.session_state.flashcards
    idx = st.session_state.current_card_idx

    if idx >= len(cards):
        st.success("🎉 خلصت كل البطاقات!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 ابدأ من الأول", use_container_width=True):
                st.session_state.current_card_idx = 0
                st.session_state.show_answer = False
                st.rerun()
        with col2:
            if st.button("🔀 عشوائي", use_container_width=True):
                import random
                random.shuffle(st.session_state.flashcards)
                st.session_state.current_card_idx = 0
                st.session_state.show_answer = False
                st.rerun()
        return

    card = cards[idx]
    total = len(cards)

    # شريط التقدم
    progress = (idx / total) * 100
    st.progress(progress / 100, text=f"🎴 {idx + 1} / {total}")

    # البطاقة
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                padding: 40px; border-radius: 20px; color: white; 
                text-align: center; font-size: 1.5rem; min-height: 200px;
                display: flex; align-items: center; justify-content: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <div>{card.get('front', '❓')}</div>
    </div>
    """, unsafe_allow_html=True)

    # الإجابة
    if st.session_state.get('show_answer'):
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 25px; border-radius: 15px; 
                    margin-top: 20px; border-right: 5px solid #667eea; font-size: 1.2rem;">
            <strong>✅ الإجابة:</strong><br><br>{card.get('back', '❓')}
        </div>
        """, unsafe_allow_html=True)

    # أزرار التحكم
    col1, col2, col3 = st.columns(3)
    with col1:
        if not st.session_state.get('show_answer'):
            if st.button("👀 إظهار الإجابة", use_container_width=True, type="primary"):
                st.session_state.show_answer = True
                st.rerun()
    with col2:
        if st.button("✅ عرفتها", use_container_width=True):
            st.session_state.show_answer = False
            st.session_state.current_card_idx += 1
            st.rerun()
    with col3:
        if st.button("❌ لسه", use_container_width=True):
            st.session_state.show_answer = False
            # ترجع البطاقة لآخر القائمة
            cards.append(cards.pop(idx))
            st.rerun()