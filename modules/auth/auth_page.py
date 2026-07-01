"""
🎨 صفحة تسجيل الدخول والتسجيل
"""

import streamlit as st
from modules.auth.auth_manager import sign_up, sign_in, sign_out, get_current_user


def render_auth_page():
    """رسم صفحة تسجيل الدخول/التسجيل"""
    
    # CSS للتصميم
    st.markdown("""
    <style>
        .auth-header {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            color: white;
            margin-bottom: 30px;
            box-shadow: 0 15px 40px rgba(102,126,234,0.4);
        }
        .auth-header h1 {
            margin: 0;
            font-size: 36px;
        }
        .auth-header p {
            margin: 10px 0 0;
            opacity: 0.95;
            font-size: 18px;
        }
        .auth-icon {
            font-size: 60px;
            margin-bottom: 10px;
        }
    </style>
    
    <div class="auth-header">
        <div class="auth-icon">🎓</div>
        <h1>المعلم الذكي</h1>
        <p>سجّل دخولك للوصول لكل ملفاتك ودروسك المحفوظة</p>
    </div>
    """, unsafe_allow_html=True)
    
    # التابات: دخول / تسجيل
    tab_login, tab_register = st.tabs(["🔐 تسجيل دخول", "✨ حساب جديد"])
    
    # ============ تسجيل الدخول ============
    with tab_login:
        st.markdown("### 🔐 تسجيل الدخول")
        st.markdown("لو عندك حساب بالفعل، سجّل دخولك هنا")
        
        with st.form("login_form", clear_on_submit=False):
            login_email = st.text_input(
                "📧 الإيميل",
                placeholder="example@email.com",
                key="login_email"
            )
            
            login_password = st.text_input(
                "🔑 كلمة المرور",
                type="password",
                placeholder="••••••••",
                key="login_password"
            )
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                login_btn = st.form_submit_button(
                    "🚀 تسجيل دخول",
                    type="primary",
                    use_container_width=True
                )
            
            with col2:
                forgot_btn = st.form_submit_button(
                    "❓ نسيت كلمة المرور",
                    use_container_width=True
                )
            
            if login_btn:
                if not login_email or not login_password:
                    st.error("❌ من فضلك املأ كل الحقول")
                else:
                    with st.spinner("جاري تسجيل الدخول..."):
                        result = sign_in(login_email, login_password)
                    
                    if result["success"]:
                        st.success(result["message"])
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(result["message"])
            
            if forgot_btn:
                st.info("💡 ميزة استعادة كلمة المرور هنضيفها قريباً")
    
    # ============ تسجيل حساب جديد ============
    with tab_register:
        st.markdown("### ✨ إنشاء حساب جديد")
        st.markdown("سجّل دلوقتي وابدأ رحلتك مع المعلم الذكي")
        
        with st.form("register_form", clear_on_submit=False):
            reg_name = st.text_input(
                "👤 الاسم",
                placeholder="اكتب اسمك",
                key="reg_name"
            )
            
            reg_email = st.text_input(
                "📧 الإيميل",
                placeholder="example@email.com",
                key="reg_email"
            )
            
            reg_password = st.text_input(
                "🔑 كلمة المرور",
                type="password",
                placeholder="8 أحرف على الأقل",
                key="reg_password"
            )
            
            reg_password_confirm = st.text_input(
                "🔑 تأكيد كلمة المرور",
                type="password",
                placeholder="اكتب كلمة المرور تاني",
                key="reg_password_confirm"
            )
            
            # شروط الاستخدام
            agree = st.checkbox(
                "✅ أوافق على شروط الاستخدام وسياسة الخصوصية",
                key="agree_terms"
            )
            
            register_btn = st.form_submit_button(
                "🎉 إنشاء حسابي",
                type="primary",
                use_container_width=True
            )
            
            if register_btn:
                # التحقق من البيانات
                if not reg_name or not reg_email or not reg_password:
                    st.error("❌ من فضلك املأ كل الحقول")
                elif reg_password != reg_password_confirm:
                    st.error("❌ كلمات المرور غير متطابقة")
                elif len(reg_password) < 8:
                    st.error("❌ كلمة المرور لازم تكون 8 أحرف على الأقل")
                elif not agree:
                    st.warning("⚠️ لازم توافق على شروط الاستخدام")
                else:
                    with st.spinner("جاري إنشاء حسابك..."):
                        result = sign_up(reg_email, reg_password, reg_name)
                    
                    if result["success"]:
                        st.success(result["message"])
                        st.info("📧 **مهم:** افتح إيميلك وأكد التسجيل من الرسالة اللي وصلتك")
                        st.balloons()
                    else:
                        st.error(result["message"])
    
    # ============ مميزات الحساب ============
    st.markdown("---")
    st.markdown("### 🌟 إيه اللي هتاخده لما تسجل؟")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background:linear-gradient(135deg, #f093fb, #f5576c); 
                    padding:20px; border-radius:15px; color:white; text-align:center; height:180px;'>
            <div style='font-size:40px;'>💾</div>
            <h4 style='margin:10px 0;'>حفظ ذكي</h4>
            <p style='font-size:13px; opacity:0.95;'>كل ملفاتك ودروسك محفوظة دائماً</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background:linear-gradient(135deg, #4facfe, #00f2fe); 
                    padding:20px; border-radius:15px; color:white; text-align:center; height:180px;'>
            <div style='font-size:40px;'>⚡</div>
            <h4 style='margin:10px 0;'>سرعة فائقة</h4>
            <p style='font-size:13px; opacity:0.95;'>مفيش انتظار - كل حاجة جاهزة</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background:linear-gradient(135deg, #43e97b, #38f9d7); 
                    padding:20px; border-radius:15px; color:white; text-align:center; height:180px;'>
            <div style='font-size:40px;'>🔒</div>
            <h4 style='margin:10px 0;'>أمان كامل</h4>
            <p style='font-size:13px; opacity:0.95;'>ملفاتك محمية وخاصة بيك</p>
        </div>
        """, unsafe_allow_html=True)


def render_user_sidebar():
    """عرض معلومات المستخدم في السايد بار - نظيف"""
    
    from .auth_manager import is_logged_in, is_admin, get_current_user, sign_out
    
    if not is_logged_in():
        return
    
    user = get_current_user()
    if not user:
        return
    
    is_admin_user = is_admin()
    user_email = user.email if hasattr(user, 'email') else ""
    user_name = user_email.split('@')[0] if '@' in user_email else "مستخدم"
    first_letter = user_name[0].upper() if user_name else "U"
    
    # تحديد نوع الحساب
    badge_class = "badge-admin" if is_admin_user else "badge-student"
    account_type = "👑 أدمن" if is_admin_user else "🎓 طالب"
    
    import streamlit as st
    
    with st.sidebar:
        # User Card
        st.markdown(f"""
        <div class="sidebar-user-card">
            <div class="sidebar-avatar">{first_letter}</div>
            <p class="sidebar-user-name">{user_name}</p>
            <p class="sidebar-user-email">{user_email}</p>
            <span class="sidebar-user-badge {badge_class}">{account_type}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # زرار تسجيل الخروج
        if st.button("🚪 تسجيل خروج", use_container_width=True, key="sidebar_logout"):
            sign_out()
            st.success("✅ تم تسجيل الخروج")
            st.rerun()