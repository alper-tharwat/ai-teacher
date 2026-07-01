"""
🎭 صفحة الأستاذ الذكي - النسخة النظيفة الاحترافية
✅ بدون تلوين (يسبب مشاكل)
✅ بدون صور (مش دقيقة)
✅ تصميم نظيف واحترافي
✅ أستاذ متحرك
✅ صوت + نص واضح
"""

import streamlit as st
import os
from modules.smart_teacher.teacher_engine import prepare_lesson, answer_student_question
from modules.smart_teacher.teacher_voice import generate_teacher_voice, get_available_voices


def get_avatar_svg():
    """قراءة الأفاتار"""
    avatar_path = os.path.join(os.path.dirname(__file__), "assets", "teacher_avatar.svg")
    try:
        with open(avatar_path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return """<svg viewBox="0 0 200 250" width="200" height="250">
            <circle cx="100" cy="80" r="50" fill="#fdbcb4"/>
            <rect x="60" y="130" width="80" height="100" rx="10" fill="#2c3e50"/>
        </svg>"""


def render_classroom(avatar_svg, audio_base64, board_html, title="", auto_play=True):
    """رسم الفصل النظيف"""
    
    autoplay_script = """
        setTimeout(() => {
            audio.play().catch(e => console.log('Click play to start'));
        }, 500);
    """ if auto_play else ""
    
    html = f"""
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
    <meta charset="UTF-8">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
            background: transparent;
        }}
        
        .classroom {{
            display: flex;
            gap: 20px;
            padding: 25px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 20px;
            min-height: 560px;
            direction: rtl;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            position: relative;
            overflow: hidden;
        }}
        
        .classroom::before {{
            content: '';
            position: absolute;
            inset: 0;
            background: 
                radial-gradient(circle at 80% 20%, rgba(255,255,255,0.05) 0%, transparent 50%),
                radial-gradient(circle at 20% 80%, rgba(102,126,234,0.1) 0%, transparent 50%);
            pointer-events: none;
        }}
        
        .screen-area {{
            flex: 1;
            position: relative;
            z-index: 2;
        }}
        
        .screen-outer {{
            background: #1a1a1a;
            border-radius: 18px;
            padding: 8px;
            box-shadow: 
                0 0 0 3px #2c2c2c,
                0 0 0 7px #555,
                0 30px 60px rgba(0,0,0,0.6);
            position: relative;
        }}
        
        .screen-outer::before {{
            content: '';
            position: absolute;
            top: 50%;
            right: -15px;
            width: 10px;
            height: 40px;
            background: linear-gradient(180deg, #ff6b6b, #ee5a52);
            border-radius: 0 5px 5px 0;
            transform: translateY(-50%);
            box-shadow: 2px 0 10px rgba(238,90,82,0.5);
        }}
        
        .screen-inner {{
            background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 12px;
            min-height: 480px;
            max-height: 480px;
            padding: 30px;
            overflow-y: auto;
            position: relative;
        }}
        
        .screen-inner::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .screen-inner::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 4px;
        }}
        
        .screen-inner::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, #3498db, #2980b9);
            border-radius: 4px;
        }}
        
        .screen-title {{
            background: linear-gradient(90deg, #3498db, #2980b9);
            color: white;
            padding: 14px 22px;
            border-radius: 12px;
            margin-bottom: 25px;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 8px 25px rgba(52,152,219,0.4);
            position: relative;
        }}
        
        .screen-title::before {{
            content: '';
            position: absolute;
            top: -5px;
            left: -5px;
            right: -5px;
            bottom: -5px;
            background: linear-gradient(90deg, #3498db, #2980b9);
            border-radius: 14px;
            opacity: 0.3;
            z-index: -1;
            filter: blur(10px);
        }}
        
        .screen-body {{
            color: #2c3e50;
            font-size: 17px;
            line-height: 2.2;
            text-align: right;
            direction: rtl;
        }}
        
        .screen-body h1, .screen-body h2 {{
            color: #2980b9;
            margin: 15px 0 10px;
            font-weight: 700;
        }}
        
        .screen-body h3 {{
            color: #2980b9;
            margin: 12px 0 8px;
            font-size: 19px;
            padding-right: 10px;
            border-right: 4px solid #3498db;
        }}
        
        .screen-body h4 {{
            color: #16a085;
            margin: 10px 0 6px;
            font-size: 17px;
        }}
        
        .screen-body p {{
            margin: 8px 0;
        }}
        
        .screen-body ul {{
            list-style: none;
            padding: 0;
            margin: 10px 0;
        }}
        
        .screen-body li {{
            padding: 10px 18px;
            margin: 8px 0;
            background: linear-gradient(90deg, rgba(52,152,219,0.08), transparent);
            border-right: 4px solid #3498db;
            border-radius: 0 10px 10px 0;
            transition: all 0.3s ease;
        }}
        
        .screen-body li:hover {{
            background: linear-gradient(90deg, rgba(52,152,219,0.15), transparent);
            transform: translateX(-5px);
        }}
        
        .screen-body strong {{
            color: #e74c3c;
            background: rgba(231,76,60,0.1);
            padding: 2px 6px;
            border-radius: 4px;
        }}
        
        .screen-body em {{
            color: #8e44ad;
            font-style: normal;
            font-weight: bold;
        }}
        
        .screen-stand {{
            width: 80px;
            height: 35px;
            background: linear-gradient(180deg, #555, #2c2c2c);
            margin: 0 auto;
            border-radius: 0 0 12px 12px;
            position: relative;
        }}
        
        .screen-stand::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 50px;
            height: 5px;
            background: #1a1a1a;
            border-radius: 5px;
        }}
        
        .screen-base {{
            width: 160px;
            height: 12px;
            background: linear-gradient(180deg, #444, #1a1a1a);
            margin: 0 auto;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}
        
        .screen-outer::after {{
            content: '';
            position: absolute;
            bottom: 15px;
            right: 15px;
            width: 6px;
            height: 6px;
            background: #2ecc71;
            border-radius: 50%;
            box-shadow: 0 0 8px #2ecc71;
            animation: ledBlink 2s infinite;
        }}
        
        @keyframes ledBlink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
        }}
        
        .teacher-area {{
            flex: 0 0 220px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 2;
        }}
        
        .teacher-wrap {{
            width: 200px;
            height: 250px;
            position: relative;
            transition: transform 0.5s ease;
        }}
        
        .teacher-wrap.walking {{
            animation: teacherWalk 4s ease-in-out infinite;
        }}
        
        @keyframes teacherWalk {{
            0%, 100% {{ transform: translateX(0) translateY(0) rotate(0deg); }}
            25% {{ transform: translateX(-12px) translateY(-4px) rotate(-1deg); }}
            50% {{ transform: translateX(0) translateY(-6px) rotate(0deg); }}
            75% {{ transform: translateX(12px) translateY(-4px) rotate(1deg); }}
        }}
        
        .teacher-wrap.speaking .mouth ellipse {{
            animation: mouthTalk 0.25s infinite alternate;
        }}
        
        @keyframes mouthTalk {{
            0% {{ ry: 5; rx: 12; }}
            50% {{ ry: 11; rx: 14; }}
            100% {{ ry: 6; rx: 11; }}
        }}
        
        .teacher-wrap.speaking .right-arm {{
            animation: armPoint 2s ease-in-out infinite;
            transform-origin: 260px 300px;
        }}
        
        @keyframes armPoint {{
            0%, 100% {{ transform: rotate(0deg); }}
            50% {{ transform: rotate(-15deg) translateY(-8px) translateX(-5px); }}
        }}
        
        .teacher-wrap.speaking line {{
            animation: eyebrowsMove 3s ease-in-out infinite;
        }}
        
        @keyframes eyebrowsMove {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-3px); }}
        }}
        
        .teacher-wrap svg {{
            width: 100%;
            height: 100%;
            filter: drop-shadow(0 15px 25px rgba(0,0,0,0.5));
        }}
        
        .teacher-name {{
            color: #fff;
            font-size: 15px;
            font-weight: bold;
            margin-top: 15px;
            background: rgba(255,255,255,0.15);
            padding: 9px 18px;
            border-radius: 22px;
            backdrop-filter: blur(10px);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .speaking-badge {{
            display: none;
            align-items: center;
            gap: 8px;
            background: linear-gradient(135deg, rgba(46, 204, 113, 0.25), rgba(39, 174, 96, 0.25));
            color: #2ecc71;
            padding: 7px 15px;
            border-radius: 20px;
            margin-top: 10px;
            font-size: 13px;
            font-weight: bold;
            border: 1px solid rgba(46, 204, 113, 0.5);
            box-shadow: 0 4px 12px rgba(46,204,113,0.3);
        }}
        
        .speaking-badge.active {{
            display: flex;
            animation: pulse 1.5s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.7; transform: scale(1.05); }}
        }}
        
        .sound-waves {{
            display: flex;
            gap: 3px;
            align-items: center;
            height: 18px;
        }}
        
        .wave-bar {{
            width: 3px;
            background: linear-gradient(180deg, #2ecc71, #27ae60);
            border-radius: 2px;
            animation: wave 0.6s ease-in-out infinite;
        }}
        
        .wave-bar:nth-child(1) {{ height: 8px; }}
        .wave-bar:nth-child(2) {{ height: 14px; animation-delay: 0.1s; }}
        .wave-bar:nth-child(3) {{ height: 10px; animation-delay: 0.2s; }}
        .wave-bar:nth-child(4) {{ height: 16px; animation-delay: 0.3s; }}
        
        @keyframes wave {{
            0%, 100% {{ transform: scaleY(1); }}
            50% {{ transform: scaleY(0.4); }}
        }}
        
        .audio-container {{
            margin-top: 15px;
            padding: 12px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}
        
        audio {{
            width: 100%;
            height: 45px;
            border-radius: 25px;
        }}
        
        audio::-webkit-media-controls-panel {{
            background: linear-gradient(135deg, #667eea, #764ba2);
        }}
    </style>
    </head>
    <body>
    
    <div class="classroom">
        <div class="screen-area">
            <div class="screen-outer">
                <div class="screen-inner">
                    <div class="screen-title">📖 {title}</div>
                    <div class="screen-body">
                        {board_html}
                    </div>
                </div>
            </div>
            <div class="screen-stand"></div>
            <div class="screen-base"></div>
            
            <div class="audio-container">
                <audio id="teacherAudio" controls>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            </div>
        </div>
        
        <div class="teacher-area">
            <div class="teacher-wrap" id="teacherAvatar">
                {avatar_svg}
            </div>
            <div class="teacher-name">🎓 الأستاذ الذكي</div>
            <div class="speaking-badge" id="speakingBadge">
                <div class="sound-waves">
                    <div class="wave-bar"></div>
                    <div class="wave-bar"></div>
                    <div class="wave-bar"></div>
                    <div class="wave-bar"></div>
                </div>
                <span>يشرح الآن...</span>
            </div>
        </div>
    </div>
    
    <script>
        const audio = document.getElementById('teacherAudio');
        const teacher = document.getElementById('teacherAvatar');
        const badge = document.getElementById('speakingBadge');
        
        audio.addEventListener('play', () => {{
            teacher.classList.add('speaking');
            teacher.classList.add('walking');
            badge.classList.add('active');
        }});
        
        audio.addEventListener('pause', () => {{
            teacher.classList.remove('speaking');
            teacher.classList.remove('walking');
            badge.classList.remove('active');
        }});
        
        audio.addEventListener('ended', () => {{
            teacher.classList.remove('speaking');
            teacher.classList.remove('walking');
            badge.classList.remove('active');
        }});
        
        {autoplay_script}
    </script>
    
    </body>
    </html>
    """
    
    return html


def render_static_classroom(avatar_svg, board_html="", title=""):
    """رسم الفصل بدون صوت (للحالة الأولية)"""
    
    html = f"""
    <style>
        .static-classroom {{
            display: flex;
            gap: 20px;
            padding: 25px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 20px;
            min-height: 540px;
            direction: rtl;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        }}
        
        .static-screen-area {{
            flex: 1;
        }}
        
        .static-screen-outer {{
            background: #1a1a1a;
            border-radius: 18px;
            padding: 8px;
            box-shadow: 0 0 0 3px #2c2c2c, 0 0 0 7px #555;
        }}
        
        .static-screen-inner {{
            background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 12px;
            min-height: 460px;
            padding: 30px;
        }}
        
        .static-title {{
            background: linear-gradient(90deg, #3498db, #2980b9);
            color: white;
            padding: 14px 22px;
            border-radius: 12px;
            margin-bottom: 25px;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
        }}
        
        .static-body {{
            color: #2c3e50;
            font-size: 17px;
            line-height: 2;
            text-align: right;
            direction: rtl;
        }}
        
        .static-body h3 {{
            color: #2980b9;
            margin: 10px 0;
            padding-right: 10px;
            border-right: 4px solid #3498db;
        }}
        
        .static-body ul {{
            list-style: none;
            padding: 0;
        }}
        
        .static-body li {{
            padding: 10px 18px;
            margin: 8px 0;
            background: linear-gradient(90deg, rgba(52,152,219,0.08), transparent);
            border-right: 4px solid #3498db;
            border-radius: 0 10px 10px 0;
        }}
        
        .static-teacher-area {{
            flex: 0 0 220px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        .static-teacher-wrap {{
            width: 200px;
            height: 250px;
        }}
        
        .static-teacher-wrap svg {{
            width: 100%;
            height: 100%;
            filter: drop-shadow(0 15px 25px rgba(0,0,0,0.5));
        }}
        
        .static-name {{
            color: #fff;
            font-size: 15px;
            font-weight: bold;
            margin-top: 15px;
            background: rgba(255,255,255,0.15);
            padding: 9px 18px;
            border-radius: 22px;
            text-align: center;
        }}
    </style>
    
    <div class="static-classroom">
        <div class="static-screen-area">
            <div class="static-screen-outer">
                <div class="static-screen-inner">
                    <div class="static-title">📖 {title or 'في انتظار البدء'}</div>
                    <div class="static-body">
                        {board_html or '<p style="text-align:center; color:#95a5a6; font-size:18px; margin-top:120px;">📚 اضغط على زر <strong style="color:#3498db;">"شغّل الشرح"</strong><br>وهبدأ أشرحلك الدرس!</p>'}
                    </div>
                </div>
            </div>
        </div>
        <div class="static-teacher-area">
            <div class="static-teacher-wrap">{avatar_svg}</div>
            <div class="static-name">🎓 الأستاذ الذكي</div>
        </div>
    </div>
    """
    return html


def render_smart_teacher_page(ai_engine, content: str = ""):
    """الصفحة الرئيسية"""
    
    st.markdown("""
    <style>
        .teacher-header {
            text-align: center;
            padding: 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 18px;
            color: white;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(102,126,234,0.3);
        }
        .teacher-header h2 { 
            margin: 0; 
            font-size: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .teacher-header p { 
            margin: 8px 0 0; 
            opacity: 0.95; 
            font-size: 16px; 
        }
    </style>
    <div class="teacher-header">
        <h2>🎭 الأستاذ الذكي المتحرك</h2>
        <p>أستاذ تفاعلي يشرح بأسلوب احترافي مع لغة ودودة وحماسية</p>
    </div>
    """, unsafe_allow_html=True)
    
    # المحتوى
    if not content:
        content = st.session_state.get("extracted_text", "")
    
    if not content:
        st.warning("⚠️ لازم ترفع ملف أو تدخل محتوى الأول!")
        manual = st.text_area("📝 أو اكتب المحتوى هنا:", height=200,
                              placeholder="اكتب أو الصق المحتوى اللي عايز الأستاذ يشرحه...")
        if manual:
            content = manual
        else:
            avatar = get_avatar_svg()
            st.components.v1.html(render_static_classroom(avatar), height=580)
            return
    
    # الإعدادات
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        style = st.selectbox("🎨 الأسلوب",
                             ["مبسط", "أكاديمي", "ممتع", "تفصيلي"],
                             index=0,
                             key="teacher_style_select")
    with col2:
        voices = get_available_voices()
        voice_name = st.selectbox("🎤 الصوت", 
                                  list(voices.keys()),
                                  index=0,
                                  key="teacher_voice_select")
    with col3:
        speed = st.selectbox("⚡ السرعة",
                             ["بطيء جداً", "بطيء", "عادي", "سريع", "سريع جداً"],
                             index=2,
                             key="teacher_speed_select")
    with col4:
        language = st.selectbox("🌍 اللغة",
                                ["العربية", "English", "Français", "Deutsch",
                                 "Español", "Türkçe"],
                                index=0,
                                key="teacher_lang_select")
    
    # زر بدء الشرح
    if st.button("🎬 حضّر الدرس!", type="primary", use_container_width=True, key="prepare_lesson_btn"):
        with st.spinner("🧠 الأستاذ بيحضّر الدرس..."):
            lesson = prepare_lesson(ai_engine, content, style, language)
        
        # ✅ فحص إن lesson صحيح
        if not lesson or not isinstance(lesson, dict):
            st.error("❌ مشكلة في تحضير الدرس - جرب تاني")
            return
        
        if not lesson.get("success"):
            st.error(f"❌ مشكلة: {lesson.get('error', 'خطأ غير معروف')}")
            return
        
        # ✅ فحص إن data موجودة وصحيحة
        lesson_data = lesson.get("data")
        if not lesson_data or not isinstance(lesson_data, dict):
            st.error("❌ بيانات الدرس فارغة - جرب تاني")
            return
        
        # ✅ حفظ في session
        st.session_state["current_lesson"] = lesson_data
        st.session_state["lesson_content"] = content
        st.session_state["current_point"] = 0
        st.session_state["voice_settings"] = {"voice": voice_name, "speed": speed}
        
        title = lesson_data.get('title', 'الدرس')
        points_count = len(lesson_data.get('points', []) or [])
        
        # رسالة الكاش
        if lesson.get("from_cache"):
            st.success(f"⚡ تم التحميل من الكاش - 0 tokens! **{title}** ({points_count} نقاط)")
        else:
            st.success(f"✅ تم التحضير والحفظ التلقائي: **{title}** ({points_count} نقاط)")
        
        st.rerun()
    
    # ═══════════════════════════════════════════════════
    # عرض الدرس - مع فحص كل حاجة
    # ═══════════════════════════════════════════════════
    if "current_lesson" in st.session_state:
        lesson_data = st.session_state.get("current_lesson")
        
        # ✅ فحص أساسي - لو lesson_data مش موجودة أو مش dict
        if not lesson_data or not isinstance(lesson_data, dict):
            st.warning("⚠️ لا توجد بيانات درس - اضغط على 'حضّر الدرس' من جديد")
            # مسح البيانات المعطلة
            if "current_lesson" in st.session_state:
                del st.session_state["current_lesson"]
            return
        
        # ✅ جلب النقاط بأمان
        points = lesson_data.get("points", []) or []
        
        # ✅ لو مفيش نقاط
        if not points:
            st.warning("⚠️ الدرس مفيهوش نقاط - جرب تحضّر الدرس تاني")
            if st.button("🔄 حاول تاني", key="retry_lesson"):
                if "current_lesson" in st.session_state:
                    del st.session_state["current_lesson"]
                st.rerun()
            return
        
        avatar = get_avatar_svg()
        
        st.markdown("---")
        st.markdown(f"### 📖 {lesson_data.get('title', 'الدرس')}")
        
        if lesson_data.get("intro"):
            st.info(f"💬 **مقدمة:** {lesson_data['intro']}")
        
        # التنقل
        current = st.session_state.get("current_point", 0)
        total = len(points)
        
        # ✅ تأكيد إن current صحيح
        if current >= total:
            current = total - 1
            st.session_state["current_point"] = current
        elif current < 0:
            current = 0
            st.session_state["current_point"] = current
        
        nav1, nav2, nav3, nav4, nav5 = st.columns([1, 1, 2, 1, 1])
        with nav1:
            if st.button("⏮️ الأولى", disabled=(current == 0), use_container_width=True, key="nav_first"):
                st.session_state["current_point"] = 0
                st.rerun()
        with nav2:
            if st.button("◀️ السابقة", disabled=(current == 0), use_container_width=True, key="nav_prev"):
                st.session_state["current_point"] -= 1
                st.rerun()
        with nav3:
            st.markdown(
                f"<div style='text-align:center; padding:10px; font-size:18px; font-weight:bold; background:linear-gradient(135deg, #667eea, #764ba2); color:white; border-radius:10px;'>📍 النقطة {current + 1} من {total}</div>",
                unsafe_allow_html=True)
        with nav4:
            if st.button("التالية ▶️", disabled=(current >= total - 1), use_container_width=True, key="nav_next"):
                st.session_state["current_point"] += 1
                st.rerun()
        with nav5:
            if st.button("الأخيرة ⏭️", disabled=(current >= total - 1), use_container_width=True, key="nav_last"):
                st.session_state["current_point"] = total - 1
                st.rerun()
        
        # عرض النقطة الحالية
        if current < total:
            point = points[current] or {}
            point_title = point.get('title', '')
            explanation = point.get('explanation', '')
            board_text = point.get('board_text', '')
            
            # زر التشغيل
            col_btn1, col_btn2 = st.columns([2, 1])
            
            with col_btn1:
                play_btn = st.button(
                    f"▶️ شغّل شرح: {point_title}",
                    type="primary",
                    use_container_width=True,
                    key=f"play_{current}"
                )
            
            with col_btn2:
                play_all_btn = st.button(
                    "🎬 شغّل الدرس كاملاً",
                    use_container_width=True,
                    key=f"playall_{current}"
                )
            
            # تشغيل النقطة الحالية
            if play_btn and explanation:
                with st.spinner("🎤 الأستاذ بيحضّر الصوت..."):
                    voice_settings = st.session_state.get("voice_settings", {})
                    result = generate_teacher_voice(
                        explanation,
                        voice_settings.get("voice", voice_name),
                        voice_settings.get("speed", speed)
                    )
                
                if result and result.get("success"):
                    if result.get("from_cache"):
                        st.success("⚡ الصوت من الكاش - فوري!")
                    else:
                        st.success("✅ تم توليد الصوت وحفظه التلقائي")
                    
                    classroom = render_classroom(
                        avatar,
                        result["audio_base64"],
                        board_text,
                        point_title,
                        auto_play=True
                    )
                    st.components.v1.html(classroom, height=650)
                    
                    with st.expander("📜 النص الكامل للشرح"):
                        st.write(explanation)
                else:
                    st.error(f"❌ مشكلة في الصوت: {result.get('error', '') if result else 'خطأ غير معروف'}")
            
            # تشغيل كل الدرس
            elif play_all_btn:
                all_text = ""
                if lesson_data.get("intro"):
                    all_text += lesson_data["intro"] + ". ... "
                
                for i, p in enumerate(points, 1):
                    if not p:
                        continue
                    all_text += f"النقطة {i}: {p.get('title', '')}. " + p.get("explanation", "") + " ... "
                
                if lesson_data.get("conclusion"):
                    all_text += "وأخيراً: " + lesson_data["conclusion"]
                
                with st.spinner("🎤 الأستاذ بيحضّر الدرس كاملاً..."):
                    voice_settings = st.session_state.get("voice_settings", {})
                    result = generate_teacher_voice(
                        all_text,
                        voice_settings.get("voice", voice_name),
                        voice_settings.get("speed", speed)
                    )
                
                if result and result.get("success"):
                    if result.get("from_cache"):
                        st.success("⚡ الدرس كامل من الكاش - فوري!")
                    else:
                        st.success("✅ تم توليد الدرس كامل وحفظه التلقائي")
                    
                    # دمج كل نصوص الصبورة
                    all_board = ""
                    if lesson_data.get("intro"):
                        all_board += f"<div style='background:linear-gradient(90deg, #e8f4fd, transparent); padding:15px; border-radius:10px; margin-bottom:20px;'>"
                        all_board += f"<h3 style='color:#3498db; margin:0;'>💬 المقدمة</h3>"
                        all_board += f"<p style='margin:8px 0;'>{lesson_data['intro']}</p>"
                        all_board += "</div>"
                    
                    for i, p in enumerate(points, 1):
                        if not p:
                            continue
                        all_board += f"<div style='margin:20px 0; padding:15px; background:rgba(46,204,113,0.05); border-radius:10px; border-right:4px solid #2ecc71;'>"
                        all_board += f"<h3 style='color:#27ae60;'>{i}. {p.get('title', '')}</h3>"
                        all_board += f"<div>{p.get('board_text', '')}</div>"
                        all_board += "</div>"
                    
                    if lesson_data.get("conclusion"):
                        all_board += f"<div style='background:linear-gradient(90deg, #fef5e7, transparent); padding:15px; border-radius:10px; margin-top:20px;'>"
                        all_board += f"<h3 style='color:#f39c12; margin:0;'>🎯 الخاتمة</h3>"
                        all_board += f"<p style='margin:8px 0;'>{lesson_data['conclusion']}</p>"
                        all_board += "</div>"
                    
                    classroom = render_classroom(
                        avatar,
                        result["audio_base64"],
                        all_board,
                        lesson_data.get('title', 'الدرس الكامل'),
                        auto_play=True
                    )
                    st.components.v1.html(classroom, height=650)
                else:
                    st.error(f"❌ مشكلة: {result.get('error', '') if result else 'خطأ غير معروف'}")
            
            else:
                # عرض ثابت بدون صوت
                classroom = render_static_classroom(avatar, board_text, point_title)
                st.components.v1.html(classroom, height=580)
        
        # عرض الخاتمة لو في آخر نقطة
        if current == total - 1 and lesson_data.get("conclusion"):
            st.success(f"🎯 **خاتمة الدرس:** {lesson_data['conclusion']}")
        
        # ═══════════════════════════════════════════════════
        # قسم الأسئلة
        # ═══════════════════════════════════════════════════
        st.markdown("---")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #00b09b, #96c93d); padding: 18px 25px; 
                    border-radius: 15px; color: white; text-align: center; margin-bottom: 15px;
                    box-shadow: 0 8px 25px rgba(0,176,155,0.3);'>
            <h3 style='margin:0; font-size:24px;'>💬 اسأل الأستاذ</h3>
            <p style='margin:8px 0 0; opacity:0.95; font-size:15px;'>اسأل أي حاجة والأستاذ هيشرحلك بصبر وحماس</p>
        </div>
        """, unsafe_allow_html=True)
        
        if "teacher_chat" not in st.session_state:
            st.session_state["teacher_chat"] = []
        
        question = st.text_input(
            "✍️ اكتب سؤالك:",
            placeholder="مثال: ممكن توضحلي النقطة دي بمثال؟",
            key="teacher_q"
        )
        
        ask_col1, ask_col2 = st.columns([3, 1])
        with ask_col1:
            ask = st.button("📤 اسأل الأستاذ", type="primary", use_container_width=True, key="ask_teacher_btn")
        with ask_col2:
            with_voice = st.checkbox("🔊 مع صوت", value=True, key="with_voice_check")
        
        if ask and question:
            with st.spinner("🤔 الأستاذ بيفكر في إجابة احترافية..."):
                ans = answer_student_question(
                    ai_engine,
                    st.session_state.get("lesson_content", content),
                    question,
                    language
                )
            
            if ans and ans.get("success"):
                ans_data = ans.get("data", {}) or {}
                voice_text = ans_data.get("answer_voice", "")
                board_text = ans_data.get("answer_board", "")
                
                st.session_state["teacher_chat"].append({
                    "question": question,
                    "answer_voice": voice_text,
                    "answer_board": board_text
                })
                
                answer_board = f"""
                    <div style='background:linear-gradient(135deg, #f8f9fa, #e9ecef); padding:15px; 
                                border-radius:10px; margin-bottom:20px; border-right:4px solid #3498db;'>
                        <strong style='color:#3498db;'>❓ سؤال الطالب:</strong>
                        <p style='margin:8px 0 0; color:#2c3e50;'>{question}</p>
                    </div>
                    <div style='background:linear-gradient(135deg, #d5f4e6, #c8e6c9); padding:15px; 
                                border-radius:10px; border-right:4px solid #27ae60;'>
                        <h3 style='color:#27ae60; margin:0 0 12px;'>💡 إجابة الأستاذ</h3>
                        <div>{board_text}</div>
                    </div>
                """
                
                if with_voice and voice_text:
                    with st.spinner("🎤 الأستاذ بيجاوب..."):
                        voice_settings = st.session_state.get("voice_settings", {})
                        result = generate_teacher_voice(
                            voice_text,
                            voice_settings.get("voice", voice_name),
                            voice_settings.get("speed", speed)
                        )
                    
                    if result and result.get("success"):
                        classroom = render_classroom(
                            avatar,
                            result["audio_base64"],
                            answer_board,
                            "💬 إجابة سؤال الطالب",
                            auto_play=True
                        )
                        st.components.v1.html(classroom, height=650)
                else:
                    classroom = render_static_classroom(avatar, answer_board, "💬 إجابة سؤال الطالب")
                    st.components.v1.html(classroom, height=580)
                
                with st.expander("📜 الإجابة الكاملة"):
                    st.write(voice_text)
            else:
                st.error(f"❌ {ans.get('error', 'خطأ غير معروف') if ans else 'مشكلة في الإجابة'}")
        
        # سجل الأسئلة
        if st.session_state.get("teacher_chat"):
            with st.expander(f"📋 سجل الأسئلة السابقة ({len(st.session_state['teacher_chat'])})"):
                for chat in reversed(st.session_state["teacher_chat"]):
                    st.markdown(f"""
                    <div style='background:#f8f9fa; padding:15px; border-radius:12px; margin:10px 0; 
                                border-right:4px solid #3498db; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
                        <strong style='color:#3498db;'>❓ سؤال:</strong> {chat['question']}<br><br>
                        <strong style='color:#27ae60;'>💡 إجابة:</strong> {chat['answer_voice'][:250]}...
                    </div>
                    """, unsafe_allow_html=True)
                
                if st.button("🗑️ مسح السجل", use_container_width=True, key="clear_chat_btn"):
                    st.session_state["teacher_chat"] = []
                    st.rerun()