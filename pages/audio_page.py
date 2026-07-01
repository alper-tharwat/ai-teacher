"""
🎵 صفحة تحويل الصوت لنص - Groq Whisper
- الإعدادات للأدمن فقط
- الطلبة يرفعو مباشرة
- حفظ الصوت في ملفاتي
"""
import streamlit as st
import os
import time
from pathlib import Path
from utils.plan_limits import check_plan_limit, increment_usage
from modules.auth.auth_manager import is_admin
from modules.auth.file_manager import save_file


def render_audio_page(ai):
    st.markdown("## 🎵 محوّل المحاضرات الصوتية لنص")
    st.markdown("⚡ **سرعة جنونية:** التحويل بياخد ثواني بدل ساعات!")

    # التحقق من المكتبات
    try:
        from groq import Groq
        groq_available = True
    except ImportError:
        groq_available = False

    try:
        import whisper
        whisper_local_available = True
    except ImportError:
        whisper_local_available = False

    if not groq_available and not whisper_local_available:
        st.error("⚠️ **مكتبات التحويل مش موجودة!**\n\n`pip install groq openai-whisper`")
        return

    # فحص الباقة
    can_do, msg = check_plan_limit("files")
    if not can_do:
        st.error(msg)
        if st.button("💎 اترقى لباقة أعلى", key="upgrade_audio"):
            st.session_state['current_page'] = 'subscriptions'
            st.rerun()
        return

    # ═══════════════════════════════════════════
    # 👨‍💼 الإعدادات - للأدمن فقط
    # ═══════════════════════════════════════════
    if is_admin():
        with st.expander("⚙️ إعدادات متقدمة (الأدمن فقط)"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                engine_options = []
                if groq_available:
                    engine_options.append(("groq", "⚡ Groq"))
                if whisper_local_available:
                    engine_options.append(("local", "🐢 Whisper المحلي"))
                engine_options.append(("auto", "🔄 تلقائي"))

                selected_engine = st.selectbox(
                    "محرك التحويل:",
                    options=[e[0] for e in engine_options],
                    format_func=lambda x: next(e[1] for e in engine_options if e[0] == x),
                    index=len(engine_options) - 1,
                    key="audio_engine_select"
                )

            with col2:
                if selected_engine in ['groq', 'auto']:
                    groq_model = st.selectbox(
                        "موديل Groq:",
                        options=['whisper-large-v3-turbo', 'whisper-large-v3'],
                        index=0,
                        key="groq_model_select"
                    )
                else:
                    groq_model = 'whisper-large-v3-turbo'

            with col3:
                language_opt = st.selectbox(
                    "لغة التسجيل:",
                    options=['auto', 'ar', 'en', 'fr', 'de', 'es'],
                    key="audio_lang_select"
                )
                whisper_lang = None if language_opt == 'auto' else language_opt
    else:
        selected_engine = "auto"
        groq_model = 'whisper-large-v3-turbo'
        whisper_lang = None

    local_model = 'base'

    # معلومات سريعة
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:#f0f7ff;padding:15px;border-radius:12px;text-align:center;direction:rtl;">
            <h3 style="margin:0;">⚡</h3>
            <strong>سرعة جنونية</strong><br>
            <small>216x أسرع من العادي</small>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#f0fff4;padding:15px;border-radius:12px;text-align:center;direction:rtl;">
            <h3 style="margin:0;">🎯</h3>
            <strong>دقة عالية</strong><br>
            <small>تفريغ دقيق للكلام</small>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:#fff7f0;padding:15px;border-radius:12px;text-align:center;direction:rtl;">
            <h3 style="margin:0;">💾</h3>
            <strong>حفظ تلقائي</strong><br>
            <small>في ملفاتي</small>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # رفع الملف
    uploaded_audio = st.file_uploader(
        "📂 ارفع الملف الصوتي:",
        type=['mp3', 'wav', 'm4a', 'ogg', 'flac', 'mp4', 'webm', 'aac', 'wma'],
        help="الحد الأقصى: 100MB",
        key="audio_uploader"
    )

    if uploaded_audio is None:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;direction:rtl;
                    background:linear-gradient(135deg,#f5f7fa,#c3cfe2);
                    border-radius:20px;margin-top:20px;">
            <h1 style="margin:0;">🎵</h1>
            <h3>ارفع محاضرتك الصوتية</h3>
            <p style="color:#666;">
                ساعة تسجيل → ثواني تحويل! ⚡
            </p>
        </div>""", unsafe_allow_html=True)
        return

    # حفظ الملف
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    safe_name = "".join(c for c in uploaded_audio.name if c.isalnum() or c in "._-")
    temp_path = os.path.join(temp_dir, f"audio_{safe_name}")

    try:
        with open(temp_path, 'wb') as f:
            f.write(uploaded_audio.getvalue())
    except Exception as e:
        st.error(f"❌ مشكلة في حفظ الملف: {e}")
        return

    st.audio(temp_path)

    file_size_mb = round(uploaded_audio.size / (1024 * 1024), 2)
    file_ext = Path(uploaded_audio.name).suffix.lower()

    duration_str = "غير محدد"
    duration_secs = 0

    try:
        from pydub import AudioSegment
        audio_seg = AudioSegment.from_file(temp_path)
        duration_secs = len(audio_seg) / 1000
        mins = int(duration_secs // 60)
        secs = int(duration_secs % 60)
        duration_str = f"{mins}:{secs:02d}"
    except Exception:
        pass

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 الحجم", f"{file_size_mb} MB")
    with col2:
        st.metric("⏱️ المدة", duration_str)
    with col3:
        if selected_engine in ['groq', 'auto']:
            est_time = max(5, int(duration_secs / 30))
            st.metric("⏳ الوقت المتوقع", f"~{est_time}s")
        else:
            est_time = int(duration_secs * 0.5)
            st.metric("⏳ الوقت المتوقع", f"~{est_time//60}m")

    if file_size_mb > 100:
        st.error(f"❌ الملف كبير جداً ({file_size_mb} MB)! الحد الأقصى 100MB")
        return

    st.markdown("---")

    # ═══════════════════════════════════════════
    # 📝 اسم المحاضرة (قبل التحويل)
    # ═══════════════════════════════════════════
    st.markdown("### 📝 اسم المحاضرة:")
    lecture_name = st.text_input(
        "اكتب اسم للمحاضرة:",
        value=Path(uploaded_audio.name).stem,
        placeholder="مثال: محاضرة الفيزياء - الفصل الأول",
        key="lecture_name_input",
        label_visibility="collapsed"
    )

    st.markdown("---")

    # زرار التحويل
    if st.button("🚀 حوّل الصوت لنص واحفظه", type="primary", use_container_width=True):
        
        if not lecture_name.strip():
            st.warning("⚠️ اكتب اسم للمحاضرة الأول!")
            return

        progress_bar = st.progress(0)
        status_txt = st.empty()

        def update_progress(val, msg):
            progress_bar.progress(min(float(val), 1.0))
            status_txt.info(msg)

        start_time = time.time()
        result = {
            'success': False,
            'text': '',
            'language': 'unknown',
            'error': None,
            'processing_time': 0,
            'engine_used': None
        }

        # ═══════════════════════════════════════════
        # الطريقة 1: Groq Whisper
        # ═══════════════════════════════════════════
        if selected_engine in ['groq', 'auto'] and groq_available:
            try:
                update_progress(0.1, "⚡ بيتصل بـ Groq...")

                # جلب المفتاح
                groq_key = None
                
                try:
                    from config import GROQ_API_KEYS
                    if GROQ_API_KEYS and len(GROQ_API_KEYS) > 0:
                        for key in GROQ_API_KEYS:
                            if key and "XXXXX" not in str(key) and len(str(key)) > 20:
                                groq_key = str(key)
                                break
                except ImportError:
                    pass
                
                if not groq_key:
                    try:
                        keys = st.secrets.get("GROQ_KEYS", [])
                        if keys and len(keys) > 0:
                            for key in keys:
                                if key and "XXXXX" not in str(key) and len(str(key)) > 20:
                                    groq_key = str(key)
                                    break
                    except Exception:
                        pass

                if not groq_key:
                    raise Exception("مفتاح Groq غير متاح")

                groq_client = Groq(api_key=groq_key)

                if file_size_mb > 25:
                    update_progress(0.2, f"📦 الملف كبير - بيتقطع لأجزاء...")
                    result = transcribe_large_file_groq(
                        groq_client, temp_path, groq_model,
                        whisper_lang, duration_secs, update_progress
                    )
                else:
                    update_progress(0.3, "🎙️ بيحوّل الكلام لنص...")

                    with open(temp_path, 'rb') as audio_file:
                        transcription = groq_client.audio.transcriptions.create(
                            file=(temp_path, audio_file.read()),
                            model=groq_model,
                            language=whisper_lang,
                            response_format="json",
                            temperature=0.0
                        )

                    result['text'] = transcription.text.strip()
                    result['language'] = whisper_lang or 'auto'
                    result['success'] = True
                    result['engine_used'] = f"Groq ({groq_model})"

                update_progress(0.95, "✨ بيخلص...")

            except Exception as e:
                error_msg = str(e)
                if selected_engine == 'groq':
                    result['error'] = f"Groq فشل: {error_msg}"
                else:
                    st.warning(f"⚠️ Groq فشل - جاري التحويل للموديل المحلي...")

        # ═══════════════════════════════════════════
        # الطريقة 2: Whisper المحلي
        # ═══════════════════════════════════════════
        if not result['success'] and selected_engine in ['local', 'auto'] and whisper_local_available:
            try:
                update_progress(0.2, "⏳ بيحمّل موديل Whisper المحلي...")

                @st.cache_resource
                def load_whisper_model(name):
                    import whisper as _w
                    return _w.load_model(name)

                model = load_whisper_model(local_model)
                update_progress(0.4, "✅ الموديل اتحمل - بيحوّل...")

                wav_path = temp_path
                if file_ext != '.wav':
                    try:
                        from pydub import AudioSegment
                        a = AudioSegment.from_file(temp_path)
                        wav_path = temp_path + "_conv.wav"
                        a.export(wav_path, format='wav', parameters=['-ar', '16000', '-ac', '1'])
                    except Exception:
                        wav_path = temp_path

                opts = {'fp16': False, 'verbose': False}
                if whisper_lang:
                    opts['language'] = whisper_lang

                update_progress(0.5, "🎙️ بيحوّل (بطيء شوية)...")
                tr = model.transcribe(wav_path, **opts)
                result['text'] = tr.get('text', '').strip()
                result['language'] = tr.get('language', 'unknown')
                result['success'] = bool(result['text'].strip())
                result['engine_used'] = "Whisper Local"

                try:
                    if wav_path != temp_path and os.path.exists(wav_path):
                        os.remove(wav_path)
                except Exception:
                    pass

            except Exception as e:
                result['error'] = f"Whisper المحلي فشل: {str(e)}"

        # تنظيف النص
        if result['text']:
            import re
            result['text'] = re.sub(r'\s+', ' ', result['text']).strip()

        result['processing_time'] = round(time.time() - start_time, 1)

        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass

        progress_bar.empty()
        status_txt.empty()

        # ═══════════════════════════════════════════
        # عرض النتيجة + الحفظ التلقائي
        # ═══════════════════════════════════════════
        if result['success'] and result['text']:
            if duration_secs > 0:
                speed = duration_secs / result['processing_time']
                speed_text = f"⚡ {speed:.1f}x من الوقت الحقيقي"
            else:
                speed_text = ""

            st.success(f"""
            ✅ **تم التحويل بنجاح!**
            - ⏱️ الوقت: {result['processing_time']} ثانية
            - {speed_text}
            """)

            # ═══════════════════════════════════════
            # 💾 الحفظ التلقائي في ملفاتي
            # ═══════════════════════════════════════
            with st.spinner("💾 بيحفظ المحاضرة في ملفاتك..."):
                # إضافة الامتداد .txt للاسم
                final_name = lecture_name.strip()
                if not final_name.endswith('.txt'):
                    final_name += '.txt'
                
                save_result = save_file(
                    file_name=final_name,
                    file_type='audio_text',  # نوع مميز للصوت المحول
                    extracted_text=result['text'],
                    file_size=uploaded_audio.size,
                    metadata={
                        'original_audio_name': uploaded_audio.name,
                        'duration_seconds': duration_secs,
                        'duration_str': duration_str,
                        'language': result.get('language', 'unknown'),
                        'engine_used': result.get('engine_used', 'unknown'),
                        'word_count': len(result['text'].split()),
                        'char_count': len(result['text']),
                        'total_pages': 1,
                        'upload_date': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                )
                
                if save_result['success']:
                    if save_result.get('is_duplicate'):
                        st.info(f"📁 المحاضرة موجودة بالفعل باسم: {save_result.get('message', '')}")
                    else:
                        st.success(f"✅ تم حفظ المحاضرة في ملفاتك باسم: **{final_name}**")
                        st.balloons()
                    
                    st.session_state['current_file_id'] = save_result['file_id']
                else:
                    st.warning(f"⚠️ فشل الحفظ: {save_result.get('message', '')}")

            words = len(result['text'].split())
            lang_names = {
                'ar': '🇸🇦 عربي', 'en': '🇺🇸 إنجليزي',
                'fr': '🇫🇷 فرنسي', 'unknown': '🌍 غير محدد', 'auto': '🌍 تلقائي'
            }

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📝 الكلمات", f"{words:,}")
            with col2:
                st.metric("🔤 الحروف", f"{len(result['text']):,}")
            with col3:
                st.metric("⏱️ الوقت", f"{result['processing_time']}s")
            with col4:
                det = result.get('language', 'unknown')
                st.metric("🌍 اللغة", lang_names.get(det, det))

            st.session_state.stats['audio_converted'] += 1
            increment_usage('files')
            st.session_state.audio_transcription = result['text']
            
            # حفظ النص في session للاستخدام المباشر
            st.session_state.extracted_text = result['text']
            st.session_state.file_info = {
                'name': final_name,
                'size_readable': f"{file_size_mb} MB",
                'extension': 'TXT',
            }
            st.session_state.all_pages = [result['text']]
            st.session_state.total_pages = 1
            st.session_state.selected_range = (1, 1)
            st.session_state.chapters = None

            st.markdown("### 📄 النص المحوّل:")
            st.text_area("النص:", value=result['text'], height=300, key="aud_res")

            # ═══════════════════════════════════════
            # 🚀 استخدام النص فوراً
            # ═══════════════════════════════════════
            st.markdown("### 🚀 استخدم النص:")
            
            st.info("💡 المحاضرة اتحفظت في **ملفاتي** ✅ - تقدر تدخل عليها في أي وقت!")
            
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if st.button("📝 لخّصها", use_container_width=True, key="a_s"):
                    st.success("✅ روح لتاب الشرح والتلخيص!")
            with col2:
                if st.button("📋 امتحان", use_container_width=True, key="a_q"):
                    st.success("✅ روح لتاب الامتحانات!")
            with col3:
                if st.button("🎴 بطاقات", use_container_width=True, key="a_f"):
                    st.success("✅ روح لتاب البطاقات!")
            with col4:
                st.download_button(
                    "⬇️ حمّل النص",
                    data=result['text'],
                    file_name=final_name,
                    mime="text/plain",
                    use_container_width=True,
                    key="a_d"
                )

        else:
            st.error(f"""
            ❌ **فشل التحويل!**

            {result.get('error', 'خطأ غير معروف')}
            """)


# ═══════════════════════════════════════════════════════
# دالة تقطيع الملفات الكبيرة لـ Groq
# ═══════════════════════════════════════════════════════
def transcribe_large_file_groq(client, file_path, model, language, total_duration, progress_callback):
    """تقطيع الملف الكبير وإرساله لـ Groq قطعة قطعة"""

    result = {
        'success': False,
        'text': '',
        'language': language or 'auto',
        'engine_used': f"Groq ({model})",
        'error': None
    }

    try:
        from pydub import AudioSegment

        progress_callback(0.25, "✂️ بيقطع الملف لأجزاء صغيرة...")

        audio = AudioSegment.from_file(file_path)
        chunk_duration_ms = 10 * 60 * 1000
        chunks = []

        for i, start in enumerate(range(0, len(audio), chunk_duration_ms)):
            chunk = audio[start:start + chunk_duration_ms]
            chunk_path = file_path + f"_chunk_{i}.mp3"
            chunk.export(chunk_path, format='mp3', bitrate='128k')
            chunks.append(chunk_path)

        total_chunks = len(chunks)
        progress_callback(0.3, f"📦 تم التقطيع لـ {total_chunks} جزء")

        text_parts = []
        for i, chunk_path in enumerate(chunks):
            prog = 0.3 + (0.6 * (i + 1) / total_chunks)
            progress_callback(prog, f"⚡ بيحوّل الجزء {i+1}/{total_chunks}...")

            try:
                with open(chunk_path, 'rb') as audio_file:
                    transcription = client.audio.transcriptions.create(
                        file=(chunk_path, audio_file.read()),
                        model=model,
                        language=language,
                        response_format="json",
                        temperature=0.0
                    )

                if transcription.text:
                    text_parts.append(transcription.text.strip())

            except Exception as e:
                print(f"⚠️ فشل الجزء {i+1}: {e}")

            try:
                os.remove(chunk_path)
            except Exception:
                pass

        result['text'] = ' '.join(text_parts)
        result['success'] = bool(result['text'].strip())

    except Exception as e:
        result['error'] = str(e)

    return result