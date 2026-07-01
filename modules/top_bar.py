import streamlit as st
from modules.auth.auth_manager import is_logged_in, get_current_user, sign_out, is_admin


def render_top_bar():
    """
    شريط علوي للتنقل السريع
    """
    
    # جلب بيانات المستخدم
    user_name = "زائر"
    
    try:
        if is_logged_in():
            user = get_current_user()
            if user and user.get("user"):
                user_obj = user.get("user")
                user_name = getattr(user_obj, 'email', 'مستخدم').split('@')[0]
    except Exception:
        pass
    
    # CSS للشريط العلوي
    st.markdown("""
    <style>
    .top-bar-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 12px 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    .top-bar-title {
        color: white;
        font-size: 22px;
        font-weight: 900;
        margin: 0;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    .top-bar-links {
        display: flex;
        gap: 12px;
        align-items: center;
    }
    .top-bar-link {
        color: white;
        text-decoration: none;
        padding: 8px 20px;
        border-radius: 25px;
        background: rgba(255,255,255,0.15);
        transition: all 0.3s ease;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid rgba(255,255,255,0.1);
        cursor: pointer;
    }
    .top-bar-link:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .top-bar-user {
        color: white;
        font-size: 14px;
        font-weight: 600;
        background: rgba(255,255,255,0.2);
        padding: 6px 15px;
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # HTML للشريط
    admin_badge = ""
    if is_admin():
        admin_badge = '<span class="top-bar-link" style="background:linear-gradient(135deg,#f39c12,#e67e22);">👨‍💼 أدمن</span>'
    
    st.markdown(f"""
    <div class="top-bar-container">
        <div class="top-bar-title">🎓 المعلم الذكي</div>
        <div class="top-bar-links">
            <span class="top-bar-user">👤 {user_name}</span>
            {admin_badge}
            <span class="top-bar-link">💎 الاشتراك</span>
            <span class="top-bar-link">🚪 خروج</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════
    # أزرار تفاعلية
    # ═══════════════════════════════════════════
    
    # لو أدمن: 4 أعمدة (رجوع + تصميم + اشتراك + خروج)
    # لو مش أدمن: 3 أعمدة (فاضي + اشتراك + خروج)
    
    if is_admin():
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.write("")
        
        with col2:
            if st.button("🎨 التصميم", key="topbar_design", use_container_width=True):
                st.session_state['current_page'] = 'design_control'
                st.rerun()
        
        with col3:
            if st.button("💎 الاشتراك", key="topbar_subscription", use_container_width=True):
                st.session_state['current_page'] = 'subscriptions'
                st.rerun()
        
        with col4:
            if st.button("🚪 خروج", key="topbar_logout", use_container_width=True):
                sign_out()
                st.rerun()
    else:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write("")
        
        with col2:
            if st.button("💎 الاشتراك", key="topbar_subscription", use_container_width=True):
                st.session_state['current_page'] = 'subscriptions'
                st.rerun()
        
        with col3:
            if st.button("🚪 خروج", key="topbar_logout", use_container_width=True):
                sign_out()
                st.rerun()