"""
🎭 مولد الأفاتار المتكلم
بيخلق أستاذ ذكي تفاعلي بيشرح بالصوت والصورة
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base64
from config import Config


class AvatarGenerator:
    """
    مولد الأفاتار المتكلم
    
    أنواع الأفاتار:
    1. CSS Avatar - أفاتار بسيط مرسوم بـ CSS (مجاني، سريع)
    2. Image Avatar - أفاتار بصورة حقيقية + حركة
    3. Animated Avatar - أفاتار متحرك بالكامل (SVG + Animation)
    4. Realistic Avatar - أفاتار واقعي (لاحقاً مع D-ID)
    
    المميزات:
    - حركة شفاه متزامنة مع الصوت
    - تعبيرات وجه متغيرة
    - خلفيات متعددة
    - أصوات متعددة
    - متجاوب مع كل الشاشات
    """
    
    # 🎨 الشخصيات المتاحة
    CHARACTERS = {
        "ostaz_ahmed": {
            "name": "👨‍🏫 الأستاذ أحمد",
            "gender": "male",
            "color_primary": "#667eea",
            "color_secondary": "#764ba2",
            "voice": "male_1",
            "personality": "ودود ومرح"
        },
        "miss_salma": {
            "name": "👩‍🏫 ميس سلمى",
            "gender": "female",
            "color_primary": "#f093fb",
            "color_secondary": "#f5576c",
            "voice": "female_1",
            "personality": "صبورة ومتفهمة"
        },
        "dr_hamed": {
            "name": "🧑‍⚕️ دكتور حامد",
            "gender": "male",
            "color_primary": "#4facfe",
            "color_secondary": "#00f2fe",
            "voice": "male_2",
            "personality": "محترف وأكاديمي"
        },
        "miss_zariyah": {
            "name": "👩‍🔬 ميس زارية",
            "gender": "female",
            "color_primary": "#fa709a",
            "color_secondary": "#fee140",
            "voice": "female_2",
            "personality": "حماسية وملهمة"
        }
    }
    
    # 🎬 الخلفيات
    BACKGROUNDS = {
        "classroom": {
            "name": "🏫 فصل دراسي",
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        },
        "library": {
            "name": "📚 مكتبة",
            "gradient": "linear-gradient(135deg, #8B4513 0%, #D2691E 100%)"
        },
        "studio": {
            "name": "🎬 استوديو",
            "gradient": "linear-gradient(135deg, #232526 0%, #414345 100%)"
        },
        "nature": {
            "name": "🌿 طبيعة",
            "gradient": "linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)"
        },
        "ocean": {
            "name": "🌊 محيط",
            "gradient": "linear-gradient(135deg, #2E3192 0%, #1BFFFF 100%)"
        },
        "sunset": {
            "name": "🌅 غروب",
            "gradient": "linear-gradient(135deg, #ff6e7f 0%, #bfe9ff 100%)"
        }
    }
    
    def __init__(self):
        """تهيئة المولد"""
        pass
    
    # ============================================
    # 🎨 الأفاتار 1: CSS Avatar (الأبسط والأسرع)
    # ============================================
    
    def generate_css_avatar(self, audio_path=None, character="ostaz_ahmed", background="classroom"):
        """
        أفاتار بسيط بـ CSS - بدون صور خارجية
        
        Args:
            audio_path: مسار ملف الصوت
            character: اسم الشخصية
            background: اسم الخلفية
        
        Returns:
            str: HTML كامل للأفاتار
        """
        char = self.CHARACTERS.get(character, self.CHARACTERS["ostaz_ahmed"])
        bg = self.BACKGROUNDS.get(background, self.BACKGROUNDS["classroom"])
        
        audio_html = self._get_audio_html(audio_path)
        
        # اختيار شكل الشعر حسب الجنس
        if char["gender"] == "female":
            hair = '<div class="hair-female"></div>'
        else:
            hair = '<div class="hair-male"></div>'
        
        html = f"""
        <div style="
            background: {bg['gradient']};
            padding: 40px 20px;
            border-radius: 20px;
            text-align: center;
            min-height: 500px;
            position: relative;
            overflow: hidden;
        ">
            <!-- نجوم متحركة في الخلفية -->
            <div class="stars-bg"></div>
            
            <!-- اسم الأستاذ -->
            <h2 style="
                color: white;
                font-family: 'Cairo', sans-serif;
                margin-bottom: 30px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                font-size: 28px;
            ">
                {char['name']}
            </h2>
            
            <!-- الأفاتار -->
            <div class="avatar-container" id="avatar-{character}">
                <div class="avatar-body">
                    <!-- الرأس -->
                    <div class="head">
                        {hair}
                        
                        <!-- الوجه -->
                        <div class="face">
                            <!-- العيون -->
                            <div class="eyes">
                                <div class="eye left-eye">
                                    <div class="pupil"></div>
                                </div>
                                <div class="eye right-eye">
                                    <div class="pupil"></div>
                                </div>
                            </div>
                            
                            <!-- الحاجبين -->
                            <div class="eyebrows">
                                <div class="eyebrow left-eyebrow"></div>
                                <div class="eyebrow right-eyebrow"></div>
                            </div>
                            
                            <!-- الأنف -->
                            <div class="nose"></div>
                            
                            <!-- الفم -->
                            <div class="mouth" id="mouth"></div>
                        </div>
                    </div>
                    
                    <!-- الجسم -->
                    <div class="body-suit" style="background: {char['color_primary']};">
                        <div class="tie"></div>
                    </div>
                </div>
            </div>
            
            <!-- شخصية الأستاذ -->
            <p style="
                color: white;
                margin-top: 20px;
                font-size: 16px;
                opacity: 0.9;
            ">
                💬 {char['personality']}
            </p>
            
            <!-- مشغل الصوت -->
            <div style="margin-top: 25px;">
                {audio_html}
            </div>
        </div>
        
        <style>
            /* استيراد الخط */
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
            
            /* النجوم المتحركة */
            .stars-bg {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: 
                    radial-gradient(2px 2px at 20% 30%, white, transparent),
                    radial-gradient(2px 2px at 60% 70%, white, transparent),
                    radial-gradient(1px 1px at 50% 50%, white, transparent),
                    radial-gradient(1px 1px at 80% 10%, white, transparent),
                    radial-gradient(2px 2px at 90% 60%, white, transparent);
                background-size: 200% 200%;
                opacity: 0.3;
                animation: twinkle 5s infinite;
            }}
            
            @keyframes twinkle {{
                0%, 100% {{ opacity: 0.3; }}
                50% {{ opacity: 0.6; }}
            }}
            
            /* حاوية الأفاتار */
            .avatar-container {{
                display: inline-block;
                position: relative;
                z-index: 1;
            }}
            
            .avatar-body {{
                position: relative;
                width: 200px;
                margin: 0 auto;
            }}
            
            /* الرأس */
            .head {{
                width: 140px;
                height: 160px;
                background: #FFE0BD;
                border-radius: 50% 50% 45% 45%;
                margin: 0 auto;
                position: relative;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                animation: headBob 4s ease-in-out infinite;
            }}
            
            @keyframes headBob {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-5px); }}
            }}
            
            /* الشعر للذكر */
            .hair-male {{
                position: absolute;
                top: -10px;
                left: 50%;
                transform: translateX(-50%);
                width: 150px;
                height: 80px;
                background: #2C1810;
                border-radius: 50% 50% 30% 30%;
                z-index: 1;
            }}
            
            /* الشعر للأنثى */
            .hair-female {{
                position: absolute;
                top: -20px;
                left: 50%;
                transform: translateX(-50%);
                width: 170px;
                height: 200px;
                background: #4A2C2A;
                border-radius: 50% 50% 30% 30%;
                z-index: 1;
            }}
            
            .hair-female:after {{
                content: '';
                position: absolute;
                top: 50px;
                left: -20px;
                width: 50px;
                height: 100px;
                background: #4A2C2A;
                border-radius: 50%;
            }}
            
            .hair-female:before {{
                content: '';
                position: absolute;
                top: 50px;
                right: -20px;
                width: 50px;
                height: 100px;
                background: #4A2C2A;
                border-radius: 50%;
            }}
            
            /* الوجه */
            .face {{
                position: relative;
                z-index: 2;
                padding-top: 50px;
            }}
            
            /* العيون */
            .eyes {{
                display: flex;
                justify-content: center;
                gap: 25px;
                margin-bottom: 5px;
            }}
            
            .eye {{
                width: 18px;
                height: 22px;
                background: white;
                border-radius: 50%;
                position: relative;
                border: 2px solid #333;
                animation: blink 4s infinite;
            }}
            
            @keyframes blink {{
                0%, 90%, 100% {{ height: 22px; }}
                95% {{ height: 3px; }}
            }}
            
            .pupil {{
                width: 8px;
                height: 8px;
                background: #2C1810;
                border-radius: 50%;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                animation: lookAround 6s infinite;
            }}
            
            @keyframes lookAround {{
                0%, 100% {{ transform: translate(-50%, -50%); }}
                25% {{ transform: translate(-30%, -50%); }}
                50% {{ transform: translate(-70%, -50%); }}
                75% {{ transform: translate(-50%, -30%); }}
            }}
            
            /* الحواجب */
            .eyebrows {{
                display: flex;
                justify-content: center;
                gap: 25px;
                position: absolute;
                top: 45px;
                width: 100%;
            }}
            
            .eyebrow {{
                width: 20px;
                height: 4px;
                background: #2C1810;
                border-radius: 2px;
            }}
            
            /* الأنف */
            .nose {{
                width: 8px;
                height: 15px;
                background: #FFD0A0;
                margin: 8px auto;
                border-radius: 0 0 50% 50%;
            }}
            
            /* الفم */
            .mouth {{
                width: 35px;
                height: 8px;
                background: #C0392B;
                margin: 5px auto;
                border-radius: 0 0 50% 50%;
                transition: all 0.1s;
            }}
            
            /* حالات الفم لما يتكلم */
            .mouth.talking {{
                animation: talk 0.3s infinite alternate;
            }}
            
            @keyframes talk {{
                0% {{ 
                    height: 8px;
                    width: 35px;
                    border-radius: 0 0 50% 50%;
                }}
                25% {{ 
                    height: 20px;
                    width: 30px;
                    border-radius: 50%;
                }}
                50% {{
                    height: 12px;
                    width: 40px;
                    border-radius: 0 0 50% 50%;
                }}
                75% {{
                    height: 25px;
                    width: 35px;
                    border-radius: 50%;
                }}
                100% {{ 
                    height: 5px;
                    width: 30px;
                    border-radius: 50px;
                }}
            }}
            
            /* الجسم */
            .body-suit {{
                width: 180px;
                height: 100px;
                margin: -10px auto 0;
                border-radius: 50% 50% 10% 10%;
                position: relative;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }}
            
            /* الكرافتة */
            .tie {{
                position: absolute;
                top: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 20px;
                height: 60px;
                background: #C0392B;
                clip-path: polygon(0 0, 100% 0, 80% 100%, 20% 100%);
            }}
            
            /* مشغل الصوت */
            .custom-audio {{
                width: 90%;
                max-width: 400px;
                margin: 0 auto;
                border-radius: 30px;
            }}
            
            audio::-webkit-media-controls-panel {{
                background-color: rgba(255, 255, 255, 0.9);
            }}
        </style>
        
        <script>
            (function() {{
                const audio = document.querySelector('#audio-player-{character}');
                const mouth = document.querySelector('#mouth');
                
                if (audio && mouth) {{
                    audio.addEventListener('play', () => {{
                        mouth.classList.add('talking');
                    }});
                    
                    audio.addEventListener('pause', () => {{
                        mouth.classList.remove('talking');
                    }});
                    
                    audio.addEventListener('ended', () => {{
                        mouth.classList.remove('talking');
                    }});
                }}
            }})();
        </script>
        """
        
        return html
    
    # ============================================
    # 🖼️ الأفاتار 2: Image Avatar (بصورة حقيقية)
    # ============================================
    
    def generate_image_avatar(self, audio_path=None, image_url=None, character="ostaz_ahmed", background="classroom"):
        """
        أفاتار بصورة حقيقية + إطار متحرك
        
        Args:
            audio_path: مسار الصوت
            image_url: رابط صورة الأفاتار (None = صورة افتراضية)
            character: الشخصية
            background: الخلفية
        """
        char = self.CHARACTERS.get(character, self.CHARACTERS["ostaz_ahmed"])
        bg = self.BACKGROUNDS.get(background, self.BACKGROUNDS["classroom"])
        
        # صورة افتراضية لو مفيش
        if not image_url:
            # استخدام UI-Avatars (مجاني)
            name_encoded = char['name'].replace('👨‍🏫', '').replace('👩‍🏫', '').replace('🧑‍⚕️', '').replace('👩‍🔬', '').strip()
            image_url = f"https://ui-avatars.com/api/?name={name_encoded}&background={char['color_primary'].replace('#', '')}&color=fff&size=300&bold=true&font-size=0.4"
        
        audio_html = self._get_audio_html(audio_path)
        
        html = f"""
        <div style="
            background: {bg['gradient']};
            padding: 40px 20px;
            border-radius: 20px;
            text-align: center;
            min-height: 500px;
            position: relative;
            overflow: hidden;
        ">
            <!-- شريط زخرفي علوي -->
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 5px;
                background: linear-gradient(90deg, transparent, white, transparent);
                animation: shimmer 3s infinite;
            "></div>
            
            <!-- العنوان -->
            <h2 style="
                color: white;
                font-family: 'Cairo', sans-serif;
                margin-bottom: 30px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                font-size: 28px;
            ">
                {char['name']}
            </h2>
            
            <!-- الأفاتار -->
            <div style="position: relative; display: inline-block;">
                <!-- الإطار الخارجي المتحرك -->
                <div class="avatar-ring"></div>
                
                <!-- الإطار الداخلي -->
                <div class="avatar-ring-inner"></div>
                
                <!-- صورة الأفاتار -->
                <img 
                    src="{image_url}" 
                    id="avatar-image-{character}"
                    style="
                        width: 220px;
                        height: 220px;
                        border-radius: 50%;
                        object-fit: cover;
                        border: 6px solid white;
                        position: relative;
                        z-index: 2;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
                        transition: all 0.3s ease;
                    "
                />
                
                <!-- أيقونة الميكروفون -->
                <div 
                    id="mic-indicator-{character}"
                    style="
                        position: absolute;
                        bottom: 15px;
                        right: 15px;
                        width: 50px;
                        height: 50px;
                        background: #4CAF50;
                        border-radius: 50%;
                        display: none;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                        z-index: 3;
                        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.5);
                        animation: pulse 1s infinite;
                    "
                >
                    🎤
                </div>
                
                <!-- موجات صوتية -->
                <div class="sound-waves" id="waves-{character}">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            
            <!-- وصف الشخصية -->
            <div style="margin-top: 25px;">
                <p style="
                    color: white;
                    font-size: 16px;
                    opacity: 0.95;
                    margin: 0;
                ">
                    💬 {char['personality']}
                </p>
                <p style="
                    color: white;
                    font-size: 14px;
                    opacity: 0.7;
                    margin-top: 5px;
                ">
                    اضغط Play عشان أبدأ أشرحلك ⬇️
                </p>
            </div>
            
            <!-- مشغل الصوت -->
            <div style="margin-top: 20px;">
                {audio_html}
            </div>
        </div>
        
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
            
            /* الإطار الخارجي المتحرك */
            .avatar-ring {{
                position: absolute;
                top: -15px;
                left: -15px;
                right: -15px;
                bottom: -15px;
                border: 3px solid rgba(255, 255, 255, 0.3);
                border-top-color: white;
                border-radius: 50%;
                animation: rotate 3s linear infinite;
            }}
            
            .avatar-ring-inner {{
                position: absolute;
                top: -8px;
                left: -8px;
                right: -8px;
                bottom: -8px;
                border: 2px dashed rgba(255, 255, 255, 0.5);
                border-radius: 50%;
                animation: rotate-reverse 4s linear infinite;
            }}
            
            @keyframes rotate {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}
            
            @keyframes rotate-reverse {{
                from {{ transform: rotate(360deg); }}
                to {{ transform: rotate(0deg); }}
            }}
            
            @keyframes shimmer {{
                0%, 100% {{ opacity: 0.3; }}
                50% {{ opacity: 1; }}
            }}
            
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.15); }}
            }}
            
            /* الموجات الصوتية */
            .sound-waves {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                display: none;
                pointer-events: none;
            }}
            
            .sound-waves.active {{
                display: block;
            }}
            
            .sound-waves span {{
                position: absolute;
                width: 220px;
                height: 220px;
                border: 3px solid white;
                border-radius: 50%;
                opacity: 0;
                top: -110px;
                left: -110px;
                animation: wave 2s infinite;
            }}
            
            .sound-waves span:nth-child(2) {{
                animation-delay: 0.6s;
            }}
            
            .sound-waves span:nth-child(3) {{
                animation-delay: 1.2s;
            }}
            
            @keyframes wave {{
                0% {{
                    transform: scale(0.8);
                    opacity: 0.8;
                }}
                100% {{
                    transform: scale(2);
                    opacity: 0;
                }}
            }}
            
            /* تأثير الصورة لما تشتغل */
            .speaking-image {{
                animation: subtle-bounce 0.5s infinite alternate !important;
            }}
            
            @keyframes subtle-bounce {{
                0% {{ transform: scale(1); }}
                100% {{ transform: scale(1.03); }}
            }}
        </style>
        
        <script>
            (function() {{
                const audio = document.querySelector('#audio-player-{character}');
                const img = document.querySelector('#avatar-image-{character}');
                const mic = document.querySelector('#mic-indicator-{character}');
                const waves = document.querySelector('#waves-{character}');
                
                if (audio) {{
                    audio.addEventListener('play', () => {{
                        if (img) img.classList.add('speaking-image');
                        if (mic) mic.style.display = 'flex';
                        if (waves) waves.classList.add('active');
                    }});
                    
                    audio.addEventListener('pause', () => {{
                        if (img) img.classList.remove('speaking-image');
                        if (mic) mic.style.display = 'none';
                        if (waves) waves.classList.remove('active');
                    }});
                    
                    audio.addEventListener('ended', () => {{
                        if (img) img.classList.remove('speaking-image');
                        if (mic) mic.style.display = 'none';
                        if (waves) waves.classList.remove('active');
                    }});
                }}
            }})();
        </script>
        """
        
        return html
    
    # ============================================
    # ✨ الأفاتار 3: Animated SVG Avatar (متحرك بالكامل)
    # ============================================
    
    def generate_animated_avatar(self, audio_path=None, character="ostaz_ahmed", background="classroom"):
        """
        أفاتار متحرك بـ SVG - الأحلى والأكثر تفاعلية
        """
        char = self.CHARACTERS.get(character, self.CHARACTERS["ostaz_ahmed"])
        bg = self.BACKGROUNDS.get(background, self.BACKGROUNDS["classroom"])
        
        audio_html = self._get_audio_html(audio_path)
        
        # ألوان مختلفة حسب الجنس
        skin_color = "#FFE0BD"
        hair_color = "#2C1810" if char["gender"] == "male" else "#8B4513"
        shirt_color = char["color_primary"]
        
        html = f"""
        <div style="
            background: {bg['gradient']};
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            min-height: 550px;
            position: relative;
            overflow: hidden;
        ">
            <h2 style="
                color: white;
                font-family: 'Cairo', sans-serif;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                font-size: 28px;
            ">
                {char['name']}
            </h2>
            
            <!-- SVG Avatar -->
            <div style="display: inline-block; position: relative;">
                <svg id="avatar-svg" width="280" height="320" viewBox="0 0 280 320" xmlns="http://www.w3.org/2000/svg">
                    
                    <!-- ظل -->
                    <ellipse cx="140" cy="305" rx="80" ry="8" fill="rgba(0,0,0,0.2)" />
                    
                    <!-- الجسم -->
                    <path d="M 80 220 Q 80 200 100 195 L 180 195 Q 200 200 200 220 L 200 300 L 80 300 Z" 
                          fill="{shirt_color}" />
                    
                    <!-- الكرافتة -->
                    <path d="M 135 195 L 145 195 L 150 250 L 140 270 L 130 250 Z" 
                          fill="#C0392B" />
                    
                    <!-- الرقبة -->
                    <rect x="125" y="170" width="30" height="30" fill="{skin_color}" />
                    
                    <!-- الرأس -->
                    <ellipse cx="140" cy="120" rx="65" ry="75" fill="{skin_color}" />
                    
                    <!-- الشعر -->
                    <path d="M 75 100 Q 70 50 140 45 Q 210 50 205 100 L 200 80 Q 180 60 140 60 Q 100 60 80 80 Z" 
                          fill="{hair_color}" />
                    
                    <!-- الأذنين -->
                    <ellipse cx="78" cy="125" rx="8" ry="12" fill="{skin_color}" />
                    <ellipse cx="202" cy="125" rx="8" ry="12" fill="{skin_color}" />
                    
                    <!-- الحاجبين -->
                    <path id="left-eyebrow" d="M 100 105 Q 115 100 125 105" stroke="{hair_color}" stroke-width="3" fill="none" stroke-linecap="round" />
                    <path id="right-eyebrow" d="M 155 105 Q 165 100 180 105" stroke="{hair_color}" stroke-width="3" fill="none" stroke-linecap="round" />
                    
                    <!-- العين اليسرى -->
                    <g id="left-eye">
                        <ellipse cx="113" cy="120" rx="10" ry="13" fill="white" />
                        <circle id="left-pupil" cx="113" cy="120" r="5" fill="#2C1810" />
                        <circle cx="115" cy="118" r="2" fill="white" />
                    </g>
                    
                    <!-- العين اليمنى -->
                    <g id="right-eye">
                        <ellipse cx="167" cy="120" rx="10" ry="13" fill="white" />
                        <circle id="right-pupil" cx="167" cy="120" r="5" fill="#2C1810" />
                        <circle cx="169" cy="118" r="2" fill="white" />
                    </g>
                    
                    <!-- الأنف -->
                    <path d="M 140 130 Q 135 145 140 155 Q 145 145 140 130" 
                          fill="#FFD0A0" stroke="#E0B080" stroke-width="1" />
                    
                    <!-- الفم -->
                    <g id="mouth-group">
                        <ellipse id="mouth-shape" cx="140" cy="170" rx="20" ry="5" fill="#C0392B" />
                        <ellipse id="mouth-inner" cx="140" cy="170" rx="15" ry="2" fill="#8B0000" />
                    </g>
                    
                    <!-- خد أيمن -->
                    <ellipse cx="95" cy="145" rx="10" ry="6" fill="#FFB6C1" opacity="0.5" />
                    <!-- خد أيسر -->
                    <ellipse cx="185" cy="145" rx="10" ry="6" fill="#FFB6C1" opacity="0.5" />
                    
                    <!-- نظارات (اختياري - للأستاذ المحترم) -->
                    <g opacity="0.6">
                        <circle cx="113" cy="120" r="16" stroke="#333" stroke-width="2" fill="none" />
                        <circle cx="167" cy="120" r="16" stroke="#333" stroke-width="2" fill="none" />
                        <line x1="129" y1="120" x2="151" y2="120" stroke="#333" stroke-width="2" />
                    </g>
                    
                </svg>
                
                <!-- مؤشر النشاط -->
                <div id="activity-indicator" style="
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    width: 15px;
                    height: 15px;
                    background: #4CAF50;
                    border-radius: 50%;
                    box-shadow: 0 0 10px #4CAF50;
                    animation: blink-light 1s infinite;
                "></div>
            </div>
            
            <!-- معلومات -->
            <div style="margin-top: 20px;">
                <p style="
                    color: white;
                    font-size: 16px;
                    margin: 5px 0;
                    opacity: 0.95;
                ">
                    💬 {char['personality']}
                </p>
                <p id="status-text" style="
                    color: white;
                    font-size: 14px;
                    opacity: 0.8;
                    margin-top: 10px;
                ">
                    🎯 جاهز للشرح - اضغط Play
                </p>
            </div>
            
            <!-- مشغل الصوت -->
            <div style="margin-top: 20px;">
                {audio_html}
            </div>
        </div>
        
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
            
            @keyframes blink-light {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.3; }}
            }}
            
            /* رمشة العين */
            @keyframes blink-eyes {{
                0%, 95%, 100% {{ ry: 13; }}
                97% {{ ry: 1; }}
            }}
            
            #left-eye ellipse, #right-eye ellipse {{
                animation: blink-eyes 4s infinite;
            }}
            
            /* حركة الفم لما يتكلم */
            .mouth-talking {{
                animation: talk-svg 0.3s infinite alternate;
            }}
            
            @keyframes talk-svg {{
                0% {{
                    transform: scale(1, 1);
                    transform-origin: 140px 170px;
                }}
                25% {{
                    transform: scale(0.8, 2.5);
                    transform-origin: 140px 170px;
                }}
                50% {{
                    transform: scale(1.2, 1.5);
                    transform-origin: 140px 170px;
                }}
                75% {{
                    transform: scale(0.9, 3);
                    transform-origin: 140px 170px;
                }}
                100% {{
                    transform: scale(1.1, 1);
                    transform-origin: 140px 170px;
                }}
            }}
            
            /* حركة الجسم */
            #avatar-svg {{
                animation: gentle-sway 3s ease-in-out infinite;
            }}
            
            @keyframes gentle-sway {{
                0%, 100% {{ transform: translateY(0) rotate(0deg); }}
                50% {{ transform: translateY(-5px) rotate(0.5deg); }}
            }}
            
            /* حركة الحواجب لما يتكلم */
            .eyebrows-talking {{
                animation: eyebrow-move 1s infinite;
            }}
            
            @keyframes eyebrow-move {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-3px); }}
            }}
        </style>
        
        <script>
            (function() {{
                const audio = document.querySelector('#audio-player-{character}');
                const mouthGroup = document.querySelector('#mouth-group');
                const leftEyebrow = document.querySelector('#left-eyebrow');
                const rightEyebrow = document.querySelector('#right-eyebrow');
                const statusText = document.querySelector('#status-text');
                const indicator = document.querySelector('#activity-indicator');
                
                if (audio) {{
                    audio.addEventListener('play', () => {{
                        if (mouthGroup) mouthGroup.classList.add('mouth-talking');
                        if (leftEyebrow) leftEyebrow.classList.add('eyebrows-talking');
                        if (rightEyebrow) rightEyebrow.classList.add('eyebrows-talking');
                        if (statusText) statusText.innerHTML = '🎙️ بتكلم دلوقتي...';
                        if (indicator) indicator.style.background = '#FF5722';
                    }});
                    
                    audio.addEventListener('pause', () => {{
                        if (mouthGroup) mouthGroup.classList.remove('mouth-talking');
                        if (leftEyebrow) leftEyebrow.classList.remove('eyebrows-talking');
                        if (rightEyebrow) rightEyebrow.classList.remove('eyebrows-talking');
                        if (statusText) statusText.innerHTML = '⏸️ متوقف مؤقتاً';
                        if (indicator) indicator.style.background = '#FFC107';
                    }});
                    
                    audio.addEventListener('ended', () => {{
                        if (mouthGroup) mouthGroup.classList.remove('mouth-talking');
                        if (leftEyebrow) leftEyebrow.classList.remove('eyebrows-talking');
                        if (rightEyebrow) rightEyebrow.classList.remove('eyebrows-talking');
                        if (statusText) statusText.innerHTML = '✅ خلصت الشرح! عجبك؟';
                        if (indicator) indicator.style.background = '#4CAF50';
                    }});
                }}
            }})();
        </script>
        """
        
        return html
    
    # ============================================
    # 🔧 أدوات مساعدة
    # ============================================
    
    def _get_audio_html(self, audio_path):
        """تحويل ملف الصوت لـ HTML"""
        if not audio_path or not os.path.exists(audio_path):
            return """
            <div style="
                background: rgba(255,255,255,0.2);
                padding: 15px 25px;
                border-radius: 30px;
                color: white;
                display: inline-block;
            ">
                ⚠️ مفيش ملف صوتي
            </div>
            """
        
        try:
            with open(audio_path, 'rb') as f:
                audio_base64 = base64.b64encode(f.read()).decode()
            
            return f"""
            <audio 
                id="audio-player-ostaz_ahmed"
                controls 
                style="
                    width: 90%;
                    max-width: 400px;
                    border-radius: 30px;
                    background: rgba(255,255,255,0.9);
                "
            >
                <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
                المتصفح بتاعك مش بيدعم تشغيل الصوت
            </audio>
            """
        except Exception as e:
            return f"<p style='color: white;'>❌ خطأ في الصوت: {str(e)}</p>"
    
    def get_characters_list(self):
        """قائمة بكل الشخصيات المتاحة"""
        return [
            {
                'key': key,
                'name': char['name'],
                'gender': char['gender'],
                'personality': char['personality']
            }
            for key, char in self.CHARACTERS.items()
        ]
    
    def get_backgrounds_list(self):
        """قائمة بكل الخلفيات المتاحة"""
        return [
            {
                'key': key,
                'name': bg['name']
            }
            for key, bg in self.BACKGROUNDS.items()
        ]
    
    # ============================================
    # 🎬 توليد فيديو كامل (الصوت + الأفاتار)
    # ============================================
    
    def create_lesson(self, audio_path, character="ostaz_ahmed", background="classroom", style="animated"):
        """
        إنشاء درس كامل بالأفاتار المتكلم
        
        Args:
            audio_path: ملف الصوت
            character: الشخصية
            background: الخلفية
            style: 'css' / 'image' / 'animated'
        
        Returns:
            str: HTML الكامل
        """
        if style == "css":
            return self.generate_css_avatar(audio_path, character, background)
        elif style == "image":
            return self.generate_image_avatar(audio_path, None, character, background)
        else:
            return self.generate_animated_avatar(audio_path, character, background)