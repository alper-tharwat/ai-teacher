"""
🎨 صفحة التحكم في التصميم - للأدمن فقط
"""
import streamlit as st
from utils.design_manager import load_settings, save_settings, reset_settings


def render_design_control_page():
    """صفحة التحكم في التصميم"""
    
    # ═══════════════════════════════════════════
    # 🔙 زر الرجوع
    # ═══════════════════════════════════════════
    col_back, col_empty = st.columns([1, 5])
    with col_back:
        if st.button("🔙 رجوع للرئيسية", key="design_back_top", use_container_width=True):
            st.session_state['current_page'] = 'home'
            st.rerun()
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════
    # 🎨 العنوان
    # ═══════════════════════════════════════════
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102,126,234,0.3);
    ">
        <h1 style="margin: 0; font-size: 2.5rem;">🎨 لوحة التحكم في التصميم</h1>
        <p style="margin: 10px 0 0; opacity: 0.95; font-size: 1.1rem;">
            تحكم كامل في شكل وألوان وأحجام الموقع
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # تحميل الإعدادات الحالية
    settings = load_settings()
    
    # ═══════════════════════════════════════════
    # التابات الرئيسية
    # ═══════════════════════════════════════════
    tabs = st.tabs([
        "🎨 الألوان",
        "📏 الأحجام",
        "📐 المسافات",
        "✨ التأثيرات",
        "🔤 الخطوط",
        "💾 حفظ/استرجاع"
    ])
    
    # ═══════════════════════════════════════════
    # تاب 1: الألوان
    # ═══════════════════════════════════════════
    with tabs[0]:
        st.markdown("### 🎨 تحكم في الألوان")
        st.info("💡 غير الألوان وشوف التأثير فوراً")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### الألوان الأساسية")
            
            primary = st.color_picker(
                "🟣 اللون الأساسي:",
                value=settings['colors']['primary'],
                key="color_primary"
            )
            
            secondary = st.color_picker(
                "🟪 اللون الثانوي:",
                value=settings['colors']['secondary'],
                key="color_secondary"
            )
            
            success = st.color_picker(
                "🟢 لون النجاح:",
                value=settings['colors']['success'],
                key="color_success"
            )
            
            danger = st.color_picker(
                "🔴 لون الخطر:",
                value=settings['colors']['danger'],
                key="color_danger"
            )
        
        with col2:
            st.markdown("#### ألوان النصوص")
            
            warning = st.color_picker(
                "🟡 لون التحذير:",
                value=settings['colors']['warning'],
                key="color_warning"
            )
            
            info = st.color_picker(
                "🔵 لون المعلومات:",
                value=settings['colors']['info'],
                key="color_info"
            )
            
            text_primary = st.color_picker(
                "📝 لون النص الأساسي:",
                value=settings['colors']['text_primary'],
                key="color_text_primary"
            )
            
            text_secondary = st.color_picker(
                "📄 لون النص الثانوي:",
                value=settings['colors']['text_secondary'],
                key="color_text_secondary"
            )
        
        # زر حفظ الألوان
        st.markdown("---")
        if st.button("💾 حفظ الألوان", key="save_colors", type="primary", use_container_width=True):
            settings['colors']['primary'] = primary
            settings['colors']['secondary'] = secondary
            settings['colors']['success'] = success
            settings['colors']['danger'] = danger
            settings['colors']['warning'] = warning
            settings['colors']['info'] = info
            settings['colors']['text_primary'] = text_primary
            settings['colors']['text_secondary'] = text_secondary
            
            if save_settings(settings):
                st.success("✅ تم حفظ الألوان بنجاح!")
                st.info("🔄 قم بتحديث الصفحة (F5) لتفعيل التغييرات")
            else:
                st.error("❌ فشل الحفظ")
    
    # ═══════════════════════════════════════════
    # تاب 2: الأحجام
    # ═══════════════════════════════════════════
    with tabs[1]:
        st.markdown("### 📏 تحكم في الأحجام")
        st.info("💡 غير أحجام العناصر بحرية")
        
        col1, col2 = st.columns(2)
        
        with col1:
            header_size = st.slider(
                "📢 حجم العناوين الكبيرة (px):",
                min_value=20, max_value=60,
                value=settings['sizes']['header_size'],
                key="size_header"
            )
            
            title_size = st.slider(
                "📌 حجم العناوين المتوسطة (px):",
                min_value=16, max_value=40,
                value=settings['sizes']['title_size'],
                key="size_title"
            )
            
            text_size = st.slider(
                "📝 حجم النص العادي (px):",
                min_value=10, max_value=24,
                value=settings['sizes']['text_size'],
                key="size_text"
            )
        
        with col2:
            button_padding = st.slider(
                "🔘 حشو الأزرار (px):",
                min_value=5, max_value=25,
                value=settings['sizes']['button_padding'],
                key="size_button_padding"
            )
            
            card_padding = st.slider(
                "🎴 حشو الكروت (px):",
                min_value=10, max_value=40,
                value=settings['sizes']['card_padding'],
                key="size_card_padding"
            )
            
            border_radius = st.slider(
                "⭕ استدارة الحواف (px):",
                min_value=0, max_value=30,
                value=settings['sizes']['border_radius'],
                key="size_border_radius"
            )
        
        # زر حفظ الأحجام
        st.markdown("---")
        if st.button("💾 حفظ الأحجام", key="save_sizes", type="primary", use_container_width=True):
            settings['sizes']['header_size'] = header_size
            settings['sizes']['title_size'] = title_size
            settings['sizes']['text_size'] = text_size
            settings['sizes']['button_padding'] = button_padding
            settings['sizes']['card_padding'] = card_padding
            settings['sizes']['border_radius'] = border_radius
            
            if save_settings(settings):
                st.success("✅ تم حفظ الأحجام بنجاح!")
                st.info("🔄 قم بتحديث الصفحة (F5) لتفعيل التغييرات")
            else:
                st.error("❌ فشل الحفظ")
    
    # ═══════════════════════════════════════════
    # تاب 3: المسافات
    # ═══════════════════════════════════════════
    with tabs[2]:
        st.markdown("### 📐 تحكم في المسافات")
        
        gap_small = st.slider(
            "📏 مسافة صغيرة (px):",
            min_value=0, max_value=20,
            value=settings['spacing']['gap_small'],
            key="spacing_small"
        )
        
        gap_medium = st.slider(
            "📏 مسافة متوسطة (px):",
            min_value=5, max_value=40,
            value=settings['spacing']['gap_medium'],
            key="spacing_medium"
        )
        
        gap_large = st.slider(
            "📏 مسافة كبيرة (px):",
            min_value=10, max_value=60,
            value=settings['spacing']['gap_large'],
            key="spacing_large"
        )
        
        st.markdown("---")
        if st.button("💾 حفظ المسافات", key="save_spacing", type="primary", use_container_width=True):
            settings['spacing']['gap_small'] = gap_small
            settings['spacing']['gap_medium'] = gap_medium
            settings['spacing']['gap_large'] = gap_large
            
            if save_settings(settings):
                st.success("✅ تم حفظ المسافات بنجاح!")
                st.info("🔄 قم بتحديث الصفحة (F5) لتفعيل التغييرات")
    
    # ═══════════════════════════════════════════
    # تاب 4: التأثيرات
    # ═══════════════════════════════════════════
    with tabs[3]:
        st.markdown("### ✨ تحكم في التأثيرات")
        
        shadow_enabled = st.checkbox(
            "🌗 تفعيل الظلال",
            value=settings['effects']['shadow_enabled'],
            key="effect_shadow"
        )
        
        shadow_intensity = st.slider(
            "🌑 قوة الظل:",
            min_value=0.0, max_value=0.5, step=0.05,
            value=settings['effects']['shadow_intensity'],
            key="effect_shadow_intensity"
        )
        
        animations_enabled = st.checkbox(
            "🎬 تفعيل الحركات",
            value=settings['effects']['animations_enabled'],
            key="effect_animations"
        )
        
        gradient_enabled = st.checkbox(
            "🌈 تفعيل التدرجات اللونية",
            value=settings['effects']['gradient_enabled'],
            key="effect_gradient"
        )
        
        st.markdown("---")
        if st.button("💾 حفظ التأثيرات", key="save_effects", type="primary", use_container_width=True):
            settings['effects']['shadow_enabled'] = shadow_enabled
            settings['effects']['shadow_intensity'] = shadow_intensity
            settings['effects']['animations_enabled'] = animations_enabled
            settings['effects']['gradient_enabled'] = gradient_enabled
            
            if save_settings(settings):
                st.success("✅ تم حفظ التأثيرات بنجاح!")
                st.info("🔄 قم بتحديث الصفحة (F5) لتفعيل التغييرات")
    
    # ═══════════════════════════════════════════
    # تاب 5: الخطوط
    # ═══════════════════════════════════════════
    with tabs[4]:
        st.markdown("### 🔤 تحكم في الخطوط")
        
        font_family = st.selectbox(
            "📝 نوع الخط:",
            options=["Cairo", "Tajawal", "Amiri", "Segoe UI", "Arial"],
            index=0 if settings['fonts']['family'] == "Cairo" else 0,
            key="font_family"
        )
        
        weight_normal = st.slider(
            "🔤 وزن الخط العادي:",
            min_value=300, max_value=600, step=100,
            value=settings['fonts']['weight_normal'],
            key="font_weight_normal"
        )
        
        weight_bold = st.slider(
            "🔤 وزن الخط الغامق:",
            min_value=500, max_value=900, step=100,
            value=settings['fonts']['weight_bold'],
            key="font_weight_bold"
        )
        
        st.markdown("---")
        if st.button("💾 حفظ الخطوط", key="save_fonts", type="primary", use_container_width=True):
            settings['fonts']['family'] = font_family
            settings['fonts']['weight_normal'] = weight_normal
            settings['fonts']['weight_bold'] = weight_bold
            
            if save_settings(settings):
                st.success("✅ تم حفظ الخطوط بنجاح!")
                st.info("🔄 قم بتحديث الصفحة (F5) لتفعيل التغييرات")
    
    # ═══════════════════════════════════════════
    # تاب 6: حفظ/استرجاع
    # ═══════════════════════════════════════════
    with tabs[5]:
        st.markdown("### 💾 حفظ واسترجاع الإعدادات")
        
        st.warning("⚠️ **الإعدادات الحالية:**")
        st.json(settings)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 استرجاع الإعدادات الافتراضية", key="reset_all", use_container_width=True):
                if reset_settings():
                    st.success("✅ تم استرجاع الإعدادات الافتراضية!")
                    st.info("🔄 قم بتحديث الصفحة (F5)")
                    st.rerun()
        
        with col2:
            # تنزيل الإعدادات
            import json
            settings_json = json.dumps(settings, ensure_ascii=False, indent=2)
            st.download_button(
                "⬇️ تنزيل الإعدادات",
                data=settings_json,
                file_name="design_settings.json",
                mime="application/json",
                use_container_width=True
            )
    
    # ═══════════════════════════════════════════
    # 🔙 زر الرجوع (تحت)
    # ═══════════════════════════════════════════
    st.markdown("---")
    col_back_bottom, col_empty_bottom = st.columns([1, 5])
    with col_back_bottom:
        if st.button("🔙 رجوع للرئيسية", key="design_back_bottom", use_container_width=True, type="primary"):
            st.session_state['current_page'] = 'home'
            st.rerun()