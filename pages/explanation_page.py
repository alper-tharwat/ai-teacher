"""
📝 صفحة التلخيص والشرح - تصميم بسيط ومنظم بـ Radio Buttons
"""
import streamlit as st
from utils.plan_limits import check_plan_limit, increment_usage
from modules.auth.outputs_manager import (
    save_output, get_cached_output, save_lesson_output,
    get_lesson_output_cached, is_lesson_from_library, get_current_lesson_id
)


def render_explanation_page(ai):
    if not st.session_state.extracted_text:
        st.warning("⚠️ ارفع ملف أو اختار درس من الفصول")
        return

    st.markdown("## 📝 الشرح والتلخيص")

    # ═══════════════════════════════════════════════════════
    # عرض النطاق أو الدرس الحالي - مع فحص كامل للأنواع
    # ═══════════════════════════════════════════════════════
    try:
        if st.session_state.get('selected_range'):
            s, e = st.session_state['selected_range']
            if isinstance(s, int) and isinstance(e, int):
                st.info(f"📚 النطاق الحالي: صفحة {s} - {e}")
        else:
            current_ch = st.session_state.get('current_chapter')
            current_ls = st.session_state.get('current_lesson')
            
            # ✅ التأكد إنهم أرقام صحيحة
            if isinstance(current_ch, int) and isinstance(current_ls, int):
                st.info(f"📖 الفصل: {current_ch + 1} | الدرس: {current_ls + 1}")
    except Exception:
        # تجاهل أي خطأ في العرض
        pass

    # ═══════════════════════════════════════════════════════
    # لغة الإخراج - Radio Buttons جنب بعض
    # ═══════════════════════════════════════════════════════
    output_language = st.radio(
        "🌐 لغة الإخراج:",
        options=["ar", "en"],
        format_func=lambda x: {"ar": "🇪🇬 العربية", "en": "🇬🇧 English"}[x],
        horizontal=True,
        key="output_language_radio"
    )

    # ═══════════════════════════════════════════════════════
    # التابس الداخلية الصغيرة
    # ═══════════════════════════════════════════════════════
    sub_tabs = st.tabs(["📋 تلخيص", "💡 شرح مفصل", "🔍 تحليل", "📖 مصطلحات"])

    # ─────────────────────────────────────
    # تاب 1: التلخيص
    # ─────────────────────────────────────
    with sub_tabs[0]:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### ✨ أسلوب التلخيص:")
            summary_style_key = st.radio(
                "اختار الأسلوب:",
                options=["smart", "short", "detailed", "bullets", "eli5"],
                format_func=lambda x: {
                    "smart": "🧠 ذكي",
                    "short": "⚡ مختصر",
                    "detailed": "📚 مفصل",
                    "bullets": "📌 نقاط",
                    "eli5": "👶 كأني عندي 5 سنين"
                }[x],
                key="sum_style_radio",
                label_visibility="collapsed"
            )
            
            # فحص الكاش
            cached_summary = get_cached_output_or_lesson(
                'summary', 
                {'style': summary_style_key, 'lang': output_language}
            )
            
            if cached_summary:
                if is_lesson_from_library():
                    st.success("🎓 الملخص جاهز من المكتبة الذكية!")
                else:
                    st.info("💾 الملخص محفوظ من قبل!")
            
            # زر التلخيص
            if st.button("📋 لخّص", key="sum_btn", use_container_width=True, type="primary"):
                # فحص الحدود
                can_do, msg = check_plan_limit("summaries")
                if not can_do:
                    st.error(msg)
                    if st.button("💎 اترقى", key="up_sum"):
                        st.session_state['current_page'] = 'subscriptions'
                        st.rerun()
                elif cached_summary:
                    st.session_state.summary = cached_summary
                    st.success("⚡ تم التحميل من الكاش - 0 tokens!")
                    st.rerun()
                else:
                    with st.spinner("⏳ جاري التلخيص..."):
                        try:
                            summary = ai.summarize(
                                st.session_state.extracted_text, 
                                style=summary_style_key
                            )
                            
                            # ترجمة لو انجليزي
                            if output_language == "en" and summary:
                                summary = translate_text(ai, summary, "en")
                            
                            if summary and summary.strip():
                                st.session_state.summary = summary
                                st.session_state.stats['summaries_made'] += 1
                                increment_usage('summaries')
                                save_to_cache(
                                    'summary', 
                                    summary, 
                                    {'style': summary_style_key, 'lang': output_language}
                                )
                                st.success("✅ تم التلخيص والحفظ!")
                                st.rerun()
                            else:
                                st.error("❌ التلخيص فارغ - جرب تاني")
                        except Exception as e:
                            st.error(f"❌ {str(e)}")

        with col2:
            if st.session_state.summary:
                st.markdown("### ✨ التلخيص:")
                st.markdown(st.session_state.summary)
            else:
                st.info("👈 اختار الأسلوب واضغط على زر التلخيص")

    # ─────────────────────────────────────
    # تاب 2: الشرح المفصل
    # ─────────────────────────────────────
    with sub_tabs[1]:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### 🎯 مستوى الشرح:")
            
            from config import Config
            level_opts = list(Config.EXPLANATION_LEVELS.keys())
            level = st.radio(
                "اختار المستوى:",
                options=level_opts,
                format_func=lambda x: f"{Config.EXPLANATION_LEVELS[x]['icon']} {Config.EXPLANATION_LEVELS[x]['name']}",
                key="exp_level_radio",
                label_visibility="collapsed"
            )
            
            # فحص الكاش
            cached_explanation = get_cached_output_or_lesson(
                'explanation', 
                {'level': level, 'lang': output_language}
            )
            
            if cached_explanation:
                if is_lesson_from_library():
                    st.success("🎓 الشرح جاهز من المكتبة الذكية!")
                else:
                    st.info("💾 الشرح محفوظ من قبل!")
            
            # زر الشرح
            if st.button("💡 اشرحلي", key="exp_btn", use_container_width=True, type="primary"):
                # فحص الحدود
                can_do, msg = check_plan_limit("explanations")
                if not can_do:
                    st.error(msg)
                    if st.button("💎 اترقى", key="up_exp"):
                        st.session_state['current_page'] = 'subscriptions'
                        st.rerun()
                elif cached_explanation:
                    st.session_state.explanation = cached_explanation
                    st.success("⚡ تم التحميل من الكاش - 0 tokens!")
                    st.rerun()
                else:
                    with st.spinner("⏳ جاري الشرح..."):
                        try:
                            exp = ai.explain(
                                st.session_state.extracted_text, 
                                level=level
                            )
                            
                            # ترجمة لو انجليزي
                            if output_language == "en" and exp:
                                exp = translate_text(ai, exp, "en")
                            
                            if exp and exp.strip():
                                st.session_state.explanation = exp
                                st.session_state.stats['explanations_made'] += 1
                                increment_usage('explanations')
                                save_to_cache(
                                    'explanation', 
                                    exp, 
                                    {'level': level, 'lang': output_language}
                                )
                                st.success("✅ تم الشرح والحفظ!")
                                st.rerun()
                            else:
                                st.error("❌ الشرح فارغ - جرب تاني")
                        except Exception as e:
                            st.error(f"❌ {str(e)}")

        with col2:
            if st.session_state.explanation:
                st.markdown("### 🎓 الشرح:")
                st.markdown(st.session_state.explanation)
            else:
                st.info("👈 اختار المستوى واضغط على زر الشرح")

    # ─────────────────────────────────────
    # تاب 3: التحليل
    # ─────────────────────────────────────
    with sub_tabs[2]:
        st.markdown("#### 🔍 تحليل المحتوى")
        st.info("💡 هيقوم بتحليل شامل للنص وإظهار النقاط الأساسية والأفكار الرئيسية")
        
        if st.button("🔍 ابدأ التحليل", use_container_width=True, type="primary", key="analyze_btn"):
            with st.spinner("⏳ جاري التحليل..."):
                try:
                    result = ai.analyze_content(st.session_state.extracted_text)
                    
                    # ترجمة لو انجليزي
                    if output_language == "en" and result:
                        result = translate_text(ai, result, "en")
                    
                    if result:
                        st.markdown("### 🔍 نتيجة التحليل:")
                        st.markdown(result)
                    else:
                        st.error("❌ جرب تاني")
                except Exception as e:
                    st.error(f"❌ {str(e)}")

    # ─────────────────────────────────────
    # تاب 4: المصطلحات
    # ─────────────────────────────────────
    with sub_tabs[3]:
        st.markdown("#### 📖 استخراج المصطلحات")
        st.info("💡 هيستخرج المصطلحات المهمة من النص ويشرحها بشكل مبسط")
        
        if st.button("📖 استخرج المصطلحات", use_container_width=True, type="primary", key="terms_btn"):
            with st.spinner("⏳ جاري استخراج المصطلحات..."):
                try:
                    result = ai.simplify_terms(st.session_state.extracted_text)
                    
                    # ترجمة لو انجليزي
                    if output_language == "en" and result:
                        result = translate_text(ai, result, "en")
                    
                    if result:
                        st.markdown("### 📖 المصطلحات:")
                        st.markdown(result)
                    else:
                        st.error("❌ جرب تاني")
                except Exception as e:
                    st.error(f"❌ {str(e)}")


# ═══════════════════════════════════════════════════════
# دالة الترجمة - بتجرب أكتر من طريقة
# ═══════════════════════════════════════════════════════

def translate_text(ai, text, target_language):
    """ترجمة النص - بتجرب أكتر من طريقة"""
    if not text:
        return text
    
    try:
        return ai.translate(text, target_language)
    except (TypeError, Exception):
        pass
    
    try:
        return ai.translate(text, target=target_language)
    except (TypeError, Exception):
        pass
    
    try:
        return ai.translate(text, language=target_language)
    except (TypeError, Exception):
        pass
    
    try:
        return ai.translate(text, to_language=target_language)
    except (TypeError, Exception):
        pass
    
    try:
        lang_name = "English" if target_language == "en" else "العربية"
        prompt = f"Translate the following text to {lang_name}, keep the same formatting:\n\n{text}"
        return ai.answer_question(context="", question=prompt)
    except Exception as e:
        return f"⚠️ Translation failed. Original text:\n\n{text}"


# ═══════════════════════════════════════════════════════
# دوال مساعدة للكاش
# ═══════════════════════════════════════════════════════

def get_cached_output_or_lesson(output_type, settings):
    """جلب من الكاش - سواء مكتبة أو شخصي"""
    is_from_library = is_lesson_from_library()
    if is_from_library:
        lesson_id = get_current_lesson_id()
        return get_lesson_output_cached(
            lesson_id=lesson_id, 
            output_type=output_type, 
            settings=settings
        )
    else:
        current_file_id = st.session_state.get('current_file_id')
        if current_file_id:
            return get_cached_output(
                file_id=current_file_id, 
                output_type=output_type, 
                settings=settings
            )
    return None


def save_to_cache(output_type, content, settings):
    """حفظ في الكاش"""
    is_from_library = is_lesson_from_library()
    if is_from_library:
        lesson_id = get_current_lesson_id()
        save_lesson_output(
            lesson_id=lesson_id, 
            output_type=output_type, 
            content=content, 
            settings=settings
        )
    else:
        current_file_id = st.session_state.get('current_file_id')
        if current_file_id:
            save_output(
                file_id=current_file_id, 
                output_type=output_type, 
                content=content, 
                settings=settings
            )