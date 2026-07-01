"""
📋 صفحة الامتحانات التفاعلية
"""
import streamlit as st
from utils.plan_limits import check_plan_limit, increment_usage
from modules.auth.outputs_manager import (
    save_output, get_cached_output, save_lesson_output,
    get_lesson_output_cached, is_lesson_from_library, get_current_lesson_id
)


def render_quiz_page(quiz_gen):
    if not st.session_state.extracted_text:
        st.warning("⚠️ ارفع ملف أو اختار درس من الفصول")
        return

    st.markdown("## 📋 الامتحانات التفاعلية")

    if st.session_state.selected_range:
        s, e = st.session_state.selected_range
        st.info(f"📚 النطاق الحالي: صفحة {s} - {e}")

    col1, col2, col3 = st.columns(3)
    with col1:
        quiz_type = st.selectbox(
            "نوع الامتحان:",
            options=[("mcq","🔤 اختيار من متعدد"), ("true_false","✅ صح وغلط"),
                     ("fill_blank","📝 أكمل الفراغ"), ("open","📄 مقالية")],
            format_func=lambda x: x[1], key="quiz_type_sel"
        )
    with col2:
        num_questions = st.slider("عدد الأسئلة:", 3, 15, 5, key="quiz_num")
    with col3:
        difficulty = st.selectbox(
            "الصعوبة:",
            options=["easy","medium","hard"],
            format_func=lambda x: {"easy":"🟢 سهل","medium":"🟡 متوسط","hard":"🔴 صعب"}[x],
            index=1, key="quiz_diff"
        )

    # 🔒 فحص حدود الباقة
    can_do, msg = check_plan_limit("quizzes")
    if not can_do:
        st.error(msg)
        if st.button("💎 اترقى لباقة أعلى", key="upgrade_quiz"):
            st.session_state['current_page'] = 'subscriptions'
            st.rerun()
        return
    else:
        st.caption(msg)

    # فحص الكاش
    qt = quiz_type[0]
    quiz_settings = {'type': qt, 'num_questions': num_questions, 'difficulty': difficulty}
    cached_quiz = get_cached_quiz(quiz_settings)

    if st.button("🎯 ولّد الامتحان", use_container_width=True):
        if cached_quiz:
            st.session_state.quiz_data = cached_quiz
            st.session_state.quiz_answers = {}
            st.session_state.quiz_results = {}
            st.success(f"⚡ تم التحميل من الكاش! ({cached_quiz.get('total', 0)} أسئلة)")
        else:
            with st.spinner("⏳..."):
                if qt == "mcq":
                    res = quiz_gen.generate_mcq(st.session_state.extracted_text, num_questions=num_questions, difficulty=difficulty)
                elif qt == "true_false":
                    res = quiz_gen.generate_true_false(st.session_state.extracted_text, num_questions=num_questions)
                elif qt == "fill_blank":
                    res = quiz_gen.generate_fill_blank(st.session_state.extracted_text, num_questions=num_questions)
                else:
                    res = quiz_gen.generate_open_questions(st.session_state.extracted_text, num_questions=num_questions, difficulty=difficulty)

                if res and res.get('success'):
                    st.session_state.quiz_data = res
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_results = {}
                    st.success(f"✅ تم! {res['total']} أسئلة")
                    st.session_state.stats['quizzes_taken'] += 1
                    increment_usage('quizzes')
                    save_quiz_to_cache(res, quiz_settings)
                else:
                    st.error("❌ جرب تاني")

    if st.session_state.quiz_data:
        render_quiz_results(quiz_gen)


def get_cached_quiz(settings):
    """جلب امتحان من الكاش"""
    is_from_library = is_lesson_from_library()
    if is_from_library:
        lesson_id = get_current_lesson_id()
        return get_lesson_output_cached(lesson_id=lesson_id, output_type='quiz', settings=settings)
    else:
        current_file_id = st.session_state.get('current_file_id')
        if current_file_id:
            return get_cached_output(file_id=current_file_id, output_type='quiz', settings=settings)
    return None


def save_quiz_to_cache(content, settings):
    """حفظ امتحان في الكاش"""
    is_from_library = is_lesson_from_library()
    if is_from_library:
        lesson_id = get_current_lesson_id()
        save_lesson_output(lesson_id=lesson_id, output_type='quiz', content=content, settings=settings)
    else:
        current_file_id = st.session_state.get('current_file_id')
        if current_file_id:
            save_output(file_id=current_file_id, output_type='quiz', content=content, settings=settings)


def render_quiz_results(quiz_gen):
    """عرض نتائج الامتحان"""
    st.markdown("---")
    st.markdown("### 📝 الأسئلة")
    
    qtype = st.session_state.quiz_data['type']
    questions = st.session_state.quiz_data.get('questions', [])
    
    if qtype == "mcq":
        render_mcq_questions(questions, quiz_gen)
    elif qtype == "true_false":
        render_true_false_questions(questions, quiz_gen)
    elif qtype == "fill_blank":
        render_fill_blank_questions(questions, quiz_gen)
    elif qtype == "open":
        render_open_questions(questions, quiz_gen)

    if st.session_state.quiz_results:
        st.markdown("---")
        if st.button("📊 النتيجة", use_container_width=True):
            ev = quiz_gen.evaluate_performance(list(st.session_state.quiz_results.values()))
            st.markdown(f"### {ev['emoji']} {ev['grade']}")
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("النسبة", f"{ev['percentage']}%")
            with col2: st.metric("الصح", f"{ev['correct_answers']}/{ev['total_questions']}")
            with col3: st.metric("التقييم", ev['stars'])
            st.info(ev['message'])


def render_mcq_questions(questions, quiz_gen):
    for i, q in enumerate(questions):
        st.markdown(f'<div style="background:#f0f7ff;padding:15px;border-radius:10px;margin:10px 0;"><h4>❓ {i+1}: {q.get("question","")}</h4></div>', unsafe_allow_html=True)
        answer = st.radio("اختار:", options=range(len(q.get('options',[]))),
                          format_func=lambda x, q=q: q['options'][x],
                          key=f"mcq_{i}")
        if st.button("✅ تحقق", key=f"chk_mcq_{i}"):
            r = quiz_gen.grade_mcq(q, answer)
            st.session_state.quiz_results[i] = r
            if r['is_correct']:
                st.success(f"✅ صحيح! {r['explanation']}")
            else:
                st.error(f"❌ خطأ! الصح: {r['correct_answer']}")
        st.markdown("---")


def render_true_false_questions(questions, quiz_gen):
    for i, q in enumerate(questions):
        st.markdown(f'<div style="background:#f0f7ff;padding:15px;border-radius:10px;margin:10px 0;"><h4>❓ {i+1}: {q.get("statement","")}</h4></div>', unsafe_allow_html=True)
        answer = st.radio("اختار:", options=[True, False],
                          format_func=lambda x: "✅ صح" if x else "❌ غلط",
                          key=f"tf_{i}", horizontal=True)
        if st.button("✅ تحقق", key=f"chk_tf_{i}"):
            r = quiz_gen.grade_true_false(q, answer)
            st.session_state.quiz_results[i] = r
            if r['is_correct']:
                st.success(f"✅ صحيح! {r['explanation']}")
            else:
                st.error(f"❌ خطأ! الصح: {r['correct_answer']}")
        st.markdown("---")


def render_fill_blank_questions(questions, quiz_gen):
    for i, q in enumerate(questions):
        st.markdown(f'<div style="background:#f0f7ff;padding:15px;border-radius:10px;margin:10px 0;"><h4>❓ {i+1}:</h4><p>{q.get("sentence","")}</p></div>', unsafe_allow_html=True)
        answer = st.text_input("اكتب إجابتك:", key=f"fb_{i}")
        if st.button("✅ تحقق", key=f"chk_fb_{i}"):
            if answer:
                r = quiz_gen.grade_fill_blank(q, answer)
                st.session_state.quiz_results[i] = r
                if r['is_correct']:
                    st.success(f"✅ صحيح! {r['explanation']}")
                else:
                    st.error(f"❌ خطأ! الصح: {r['correct_answer']}")
            else:
                st.warning("⚠️ اكتب إجابة!")
        st.markdown("---")


def render_open_questions(questions, quiz_gen):
    for i, q in enumerate(questions):
        st.markdown(f'<div style="background:#f0f7ff;padding:15px;border-radius:10px;margin:10px 0;"><h4>❓ {i+1}: {q.get("question","")}</h4></div>', unsafe_allow_html=True)
        answer = st.text_area("اكتب إجابتك:", key=f"open_{i}", height=150)
        if st.button("✅ صحّحلي", key=f"grd_{i}"):
            if answer:
                with st.spinner("⏳..."):
                    r = quiz_gen.grade_open_question(q, answer)
                    st.session_state.quiz_results[i] = r
                if r.get('success'):
                    col1, col2 = st.columns(2)
                    with col1: st.metric("التقييم", f"{r['score']}/10")
                    with col2: st.metric("النسبة", f"{r['percentage']}%")
                    st.markdown(f"**ملاحظات:** {r['feedback']}")
                    st.markdown(f"**إجابة نموذجية:** {r['model_answer']}")
                else:
                    st.error("❌ مشكلة في التصحيح")
            else:
                st.warning("⚠️ اكتب إجابة!")
        st.markdown("---")