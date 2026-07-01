# modules/subscriptions/pricing_page.py

import streamlit as st


def render_pricing_page():
    """
    صفحة أسعار الاشتراكات
    """
    
    # ═══════════════════════════════════════════
    # 🔙 زر الرجوع للرئيسية (في الأعلى)
    # ═══════════════════════════════════════════
    col_back, col_empty = st.columns([1, 5])
    with col_back:
        if st.button("🔙 رجوع للرئيسية", key="back_to_home_top", use_container_width=True):
            st.session_state['current_page'] = 'home'
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <style>
    .pricing-container {
        text-align: center;
        padding: 20px 0;
        direction: rtl;
    }
    .pricing-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .pricing-subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 30px;
    }
    .pricing-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        transition: all 0.3s;
        border: 2px solid #e0e0e0;
        direction: rtl;
        height: 100%;
    }
    .pricing-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }
    .pricing-card.popular {
        border-color: #667eea;
        transform: scale(1.05);
    }
    .pricing-card.popular:hover {
        transform: scale(1.05) translateY(-10px);
    }
    .plan-badge {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .plan-name {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 8px 0;
    }
    .plan-price {
        font-size: 2.5rem;
        font-weight: 900;
        color: #667eea;
        margin: 15px 0;
    }
    .plan-price span {
        font-size: 1rem;
        color: #888;
        font-weight: 400;
    }
    .plan-features {
        text-align: right;
        font-size: 0.95rem;
        line-height: 2.2;
        margin-top: 15px;
    }
    .popular-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        text-align: center;
        padding: 8px;
        border-radius: 12px 12px 0 0;
        font-size: 0.9rem;
        font-weight: bold;
        margin: -25px -25px 15px -25px;
    }
    .save-badge {
        background: #e74c3c;
        color: white;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 0.75rem;
        display: inline-block;
        margin-top: 5px;
    }
    .not-available {
        color: #bbb;
        text-decoration: line-through;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # العنوان
    st.markdown("""
    <div class="pricing-container">
        <div class="pricing-title">💎 خطط الاشتراك</div>
        <div class="pricing-subtitle">اختار الخطة المناسبة ليك وابدأ رحلة التعلم</div>
    </div>
    """, unsafe_allow_html=True)
    
    # الصف الأول: 3 باقات
    col1, col2, col3 = st.columns(3)
    
    # 🆓 المجانية
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <div class="plan-badge">🆓</div>
            <div class="plan-name" style="color: #95a5a6;">المجانية</div>
            <div class="plan-price">0 <span>جنيه/شهر</span></div>
            <hr>
            <div class="plan-features">
                📁 <b>2 ملف/شهر</b><br>
                📝 <b>تلخيص: 3</b><br>
                📖 <b>شرح: 3</b><br>
                📋 <b>امتحانات: 3</b><br>
                🎴 <b>بطاقات: 3</b><br>
                🧠 <b>خرائط: 3</b><br>
                <span class="not-available">🎭 أستاذ ذكي</span><br>
                <span class="not-available">📥 تصدير PDF</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("ابدأ مجاناً", key="plan_free_btn", use_container_width=True):
            st.info("✅ أنت بالفعل على الخطة المجانية!")
    
    # ⭐ الأساسية
    with col2:
        st.markdown("""
        <div class="pricing-card">
            <div class="plan-badge">⭐</div>
            <div class="plan-name" style="color: #3498db;">الأساسية</div>
            <div class="plan-price">150 <span>جنيه/شهر</span></div>
            <hr>
            <div class="plan-features">
                📁 <b>25 ملف/شهر</b><br>
                📝 <b>تلخيص: 50</b><br>
                📖 <b>شرح: 50</b><br>
                📋 <b>امتحانات: 50</b><br>
                🎴 <b>بطاقات: 50</b><br>
                🧠 <b>خرائط: 50</b><br>
                🎭 <b>أستاذ ذكي: 20</b><br>
                <span class="not-available">📥 تصدير PDF</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("اشترك الآن", key="plan_basic_btn", use_container_width=True):
            st.session_state['selected_plan'] = 'basic'
            st.success("✅ تم اختيار خطة الأساسية! (ربط الدفع قريباً)")
    
    # 💎 المميزة
    with col3:
        st.markdown("""
        <div class="pricing-card popular">
            <div class="popular-badge">⭐ الأكثر مبيعاً</div>
            <div class="plan-badge">💎</div>
            <div class="plan-name" style="color: #9b59b6;">المميزة</div>
            <div class="plan-price">250 <span>جنيه/شهر</span></div>
            <div class="save-badge">وفر 40%</div>
            <hr>
            <div class="plan-features">
                📁 <b>50 ملف/شهر</b><br>
                📝 <b>تلخيص: 90</b><br>
                📖 <b>شرح: 90</b><br>
                📋 <b>امتحانات: 90</b><br>
                🎴 <b>بطاقات: 90</b><br>
                🧠 <b>خرائط: 90</b><br>
                🎭 <b>أستاذ ذكي: 40</b><br>
                <span class="not-available">📥 تصدير PDF</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("اشترك الآن", key="plan_premium_btn", type="primary", use_container_width=True):
            st.session_state['selected_plan'] = 'premium'
            st.success("✅ تم اختيار خطة المميزة! (ربط الدفع قريباً)")
    
    # الصف الثاني: باقتين
    st.markdown("---")
    col4, col5 = st.columns(2)
    
    # 🏆 الاحترافية
    with col4:
        st.markdown("""
        <div class="pricing-card">
            <div class="plan-badge">🏆</div>
            <div class="plan-name" style="color: #f39c12;">الاحترافية</div>
            <div class="plan-price">450 <span>جنيه/شهر</span></div>
            <hr>
            <div class="plan-features">
                📁 <b>100 ملف/شهر</b><br>
                📝 <b>تلخيص: 300</b><br>
                📖 <b>شرح: 300</b><br>
                📋 <b>امتحانات: 300</b><br>
                🎴 <b>بطاقات: 300</b><br>
                🧠 <b>خرائط: 300</b><br>
                🎭 <b>أستاذ ذكي: 100</b><br>
                <span class="not-available">📥 تصدير PDF</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("اشترك الآن", key="plan_pro_btn", use_container_width=True):
            st.session_state['selected_plan'] = 'pro'
            st.success("✅ تم اختيار خطة الاحترافية! (ربط الدفع قريباً)")
    
    # 👨‍👩‍👧‍👦 العائلية
    with col5:
        st.markdown("""
        <div class="pricing-card" style="background: linear-gradient(135deg, #f0fff4, #fff);">
            <div class="plan-badge">👨‍👩‍👧‍👦</div>
            <div class="plan-name" style="color: #27ae60;">العائلية</div>
            <div class="plan-price">800 <span>جنيه/شهر</span></div>
            <div class="save-badge">وفر 200 جنيه</div>
            <hr>
            <div class="plan-features">
                👥 <b>4 حسابات</b><br>
                📁 <b>50 ملف/شخص</b><br>
                📝 <b>تلخيص: 90/شخص</b><br>
                📖 <b>شرح: 90/شخص</b><br>
                📋 <b>امتحانات: 90/شخص</b><br>
                🎴 <b>بطاقات: 90/شخص</b><br>
                🧠 <b>خرائط: 90/شخص</b><br>
                🎭 <b>أستاذ ذكي: 40/شخص</b><br>
                <span class="not-available">📥 تصدير PDF</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("تواصل للاشتراك", key="plan_family_btn", use_container_width=True):
            st.info("📧 بعت لنا على: aaalperr52@gmail.com")
    
    # ═══════════════════════════════════════════
    # 🔙 زر الرجوع للرئيسية (في الأسفل)
    # ═══════════════════════════════════════════
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_back_bottom, col_empty_bottom = st.columns([1, 5])
    with col_back_bottom:
        if st.button("🔙 رجوع للرئيسية", key="back_to_home_bottom", use_container_width=True, type="primary"):
            st.session_state['current_page'] = 'home'
            st.rerun()


def get_plan_limits(plan_name: str) -> dict:
    """
    حدود الباقات للاستخدام في باقي الموقع
    """
    limits = {
        "free": {
            "max_files_per_month": 2,
            "max_file_size_mb": 5,
            "summaries": 3,
            "explanations": 3,
            "quizzes": 3,
            "flashcards": 3,
            "mindmaps": 3,
            "teacher_sessions": 0,
            "can_export_pdf": False,
        },
        "basic": {
            "max_files_per_month": 25,
            "max_file_size_mb": 10,
            "summaries": 50,
            "explanations": 50,
            "quizzes": 50,
            "flashcards": 50,
            "mindmaps": 50,
            "teacher_sessions": 20,
            "can_export_pdf": False,
        },
        "premium": {
            "max_files_per_month": 50,
            "max_file_size_mb": 20,
            "summaries": 90,
            "explanations": 90,
            "quizzes": 90,
            "flashcards": 90,
            "mindmaps": 90,
            "teacher_sessions": 40,
            "can_export_pdf": False,
        },
        "pro": {
            "max_files_per_month": 100,
            "max_file_size_mb": 30,
            "summaries": 300,
            "explanations": 300,
            "quizzes": 300,
            "flashcards": 300,
            "mindmaps": 300,
            "teacher_sessions": 100,
            "can_export_pdf": False,
        },
        "family": {
            "max_files_per_month": 50,
            "max_file_size_mb": 20,
            "summaries": 90,
            "explanations": 90,
            "quizzes": 90,
            "flashcards": 90,
            "mindmaps": 90,
            "teacher_sessions": 40,
            "can_export_pdf": False,
            "max_accounts": 4,
        },
    }
    return limits.get(plan_name, limits["free"])