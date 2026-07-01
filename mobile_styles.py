"""
📱 تصميم موبايل احترافي - كل حاجة مظبوطة
"""

def get_mobile_css():
    """CSS احترافي للموبايل"""
    
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');
        
        /* ═══════════════════════════════════════════════ */
        /* 📱 تصميم الموبايل - شاشات أصغر من 768px */
        /* ═══════════════════════════════════════════════ */
        
        @media only screen and (max-width: 768px) {
            
            /* ═══════════════════════════════════════ */
            /* 📄 الصفحة الرئيسية */
            /* ═══════════════════════════════════════ */
            
            .main .block-container {
                padding: 1rem 0.8rem !important;
                padding-top: 0.5rem !important;
                max-width: 100% !important;
            }
            
            /* الخلفية */
            .stApp {
                background: #f8f9fc !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 🎓 التوب بار */
            /* ═══════════════════════════════════════ */
            
            .top-bar-container {
                padding: 10px 15px !important;
                border-radius: 12px !important;
                margin-bottom: 15px !important;
                flex-direction: column !important;
                gap: 10px !important;
            }
            
            .top-bar-title {
                font-size: 18px !important;
                text-align: center !important;
            }
            
            .top-bar-links {
                width: 100% !important;
                justify-content: center !important;
                gap: 8px !important;
                flex-wrap: wrap !important;
            }
            
            .top-bar-user {
                font-size: 12px !important;
                padding: 5px 12px !important;
            }
            
            .top-bar-link {
                font-size: 12px !important;
                padding: 6px 14px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 🎨 الـ Header الرئيسي */
            /* ═══════════════════════════════════════ */
            
            .main-header {
                padding: 20px 15px !important;
                border-radius: 15px !important;
                margin-bottom: 15px !important;
            }
            
            .main-header h1 {
                font-size: 22px !important;
                margin: 0 !important;
                line-height: 1.4 !important;
            }
            
            .main-header p {
                font-size: 13px !important;
                margin-top: 8px !important;
                line-height: 1.6 !important;
            }
            
            .main-header span {
                font-size: 11px !important;
                padding: 3px 10px !important;
                display: inline-block !important;
                margin: 3px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 📊 كروت الإحصائيات - 4 في الصف */
            /* ═══════════════════════════════════════ */
            
            .stat-box {
                padding: 10px 5px !important;
                margin: 3px !important;
                border-radius: 10px !important;
                min-height: 65px !important;
            }
            
            .stat-number {
                font-size: 18px !important;
                margin: 0 !important;
                font-weight: 900 !important;
            }
            
            .stat-label {
                font-size: 10px !important;
                margin-top: 3px !important;
                font-weight: 600 !important;
            }
            
            /* الأعمدة - 4 في الصف للإحصائيات */
            div[data-testid="column"]:has(.stat-box) {
                flex: 0 0 25% !important;
                max-width: 25% !important;
                padding: 2px !important;
                min-width: 0 !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 📑 التابات - قابلة للتمرير */
            /* ═══════════════════════════════════════ */
            
            .stTabs [data-baseweb="tab-list"] {
                gap: 5px !important;
                padding: 6px !important;
                border-radius: 12px !important;
                overflow-x: auto !important;
                overflow-y: hidden !important;
                flex-wrap: nowrap !important;
                -webkit-overflow-scrolling: touch !important;
                scrollbar-width: thin !important;
            }
            
            .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
                height: 4px !important;
            }
            
            .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
                background: #667eea !important;
                border-radius: 10px !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                font-size: 12px !important;
                padding: 8px 12px !important;
                white-space: nowrap !important;
                min-width: fit-content !important;
                border-radius: 8px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 🔘 الأزرار */
            /* ═══════════════════════════════════════ */
            
            .stButton > button {
                font-size: 13px !important;
                padding: 10px 15px !important;
                border-radius: 10px !important;
                min-height: 44px !important;
                line-height: 1.4 !important;
                white-space: pre-wrap !important;
                word-wrap: break-word !important;
            }
            
            /* أزرار التنزيل */
            [data-testid="stDownloadButton"] > button {
                font-size: 13px !important;
                padding: 10px 15px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 📝 النصوص والعناوين */
            /* ═══════════════════════════════════════ */
            
            h1 { 
                font-size: 22px !important;
                line-height: 1.4 !important;
            }
            h2 { 
                font-size: 19px !important;
                line-height: 1.4 !important;
            }
            h3 { 
                font-size: 16px !important;
                line-height: 1.5 !important;
            }
            h4 { 
                font-size: 15px !important;
            }
            h5 { 
                font-size: 14px !important;
            }
            
            p, .stMarkdown p {
                font-size: 14px !important;
                line-height: 1.8 !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 🎛️ السايدبار */
            /* ═══════════════════════════════════════ */
            
            [data-testid="stSidebar"] {
                width: 280px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 📤 File Uploader */
            /* ═══════════════════════════════════════ */
            
            [data-testid="stFileUploader"] section {
                padding: 15px !important;
                border-radius: 12px !important;
            }
            
            [data-testid="stFileUploaderDropzone"] {
                min-height: 80px !important;
                flex-direction: column !important;
                gap: 10px !important;
            }
            
            [data-testid="stFileUploaderDropzone"] button {
                font-size: 12px !important;
                padding: 8px 20px !important;
                min-height: 40px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 📋 Expanders */
            /* ═══════════════════════════════════════ */
            
            [data-testid="stExpander"] {
                border-radius: 10px !important;
                margin: 6px 0 !important;
            }
            
            [data-testid="stExpander"] > details > summary {
                padding: 12px 15px !important;
                font-size: 13px !important;
            }
            
            [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
                padding: 12px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 📝 Selectbox و Radio */
            /* ═══════════════════════════════════════ */
            
            [data-testid="stSelectbox"] > label,
            [data-testid="stRadio"] > label,
            [data-testid="stTextInput"] > label,
            [data-testid="stTextArea"] > label,
            [data-testid="stNumberInput"] > label {
                font-size: 13px !important;
                margin-bottom: 5px !important;
            }
            
            .stSelectbox [data-baseweb="select"] > div {
                font-size: 13px !important;
                padding: 8px 12px !important;
                min-height: 40px !important;
            }
            
            [data-testid="stRadio"] > div > label {
                padding: 10px 12px !important;
                margin: 4px 0 !important;
                border-radius: 8px !important;
            }
            
            [data-testid="stRadio"] > div > label p {
                font-size: 13px !important;
                padding: 0 5px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 📝 Text Inputs */
            /* ═══════════════════════════════════════ */
            
            .stTextInput input,
            .stTextArea textarea,
            .stNumberInput input {
                font-size: 14px !important;
                padding: 10px 12px !important;
                border-radius: 10px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 📊 Metrics */
            /* ═══════════════════════════════════════ */
            
            [data-testid="stMetric"] {
                padding: 12px !important;
                border-radius: 10px !important;
            }
            
            [data-testid="stMetricLabel"] {
                font-size: 11px !important;
            }
            
            [data-testid="stMetricValue"] {
                font-size: 18px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 🚨 Alerts */
            /* ═══════════════════════════════════════ */
            
            [data-testid="stAlert"] {
                padding: 12px 15px !important;
                font-size: 13px !important;
                border-radius: 10px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 💬 Chat */
            /* ═══════════════════════════════════════ */
            
            [data-testid="stChatMessage"] {
                padding: 10px !important;
                border-radius: 10px !important;
                margin: 6px 0 !important;
            }
            
            [data-testid="stChatInput"] textarea {
                font-size: 13px !important;
                padding: 10px 15px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 🎴 كروت الفصول والدروس */
            /* ═══════════════════════════════════════ */
            
            /* الفصول - 1 في الصف */
            div[data-testid="column"] {
                flex: 0 0 100% !important;
                max-width: 100% !important;
                padding: 3px !important;
            }
            
            /* الإحصائيات فقط - 4 في الصف */
            div[data-testid="column"]:has(.stat-box) {
                flex: 0 0 25% !important;
                max-width: 25% !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 📋 Quiz */
            /* ═══════════════════════════════════════ */
            
            .quiz-question {
                padding: 15px !important;
                border-radius: 12px !important;
                margin: 10px 0 !important;
            }
            
            .quiz-question h4 {
                font-size: 15px !important;
                line-height: 1.7 !important;
            }
            
            .quiz-correct, .quiz-wrong {
                padding: 12px !important;
                font-size: 13px !important;
                border-radius: 10px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 🎯 Range Card */
            /* ═══════════════════════════════════════ */
            
            .range-card {
                padding: 15px !important;
                border-radius: 12px !important;
                font-size: 13px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 🎵 Audio */
            /* ═══════════════════════════════════════ */
            
            audio {
                height: 40px !important;
                border-radius: 20px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 📊 Progress Bar */
            /* ═══════════════════════════════════════ */
            
            .stProgress > div > div {
                border-radius: 6px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 🖼️ Images */
            /* ═══════════════════════════════════════ */
            
            .stImage img {
                border-radius: 10px !important;
                max-width: 100% !important;
                height: auto !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 🎨 Data Frames */
            /* ═══════════════════════════════════════ */
            
            [data-testid="stDataFrame"] {
                font-size: 11px !important;
                border-radius: 8px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 🔤 Markdown */
            /* ═══════════════════════════════════════ */
            
            .stMarkdown {
                font-size: 14px !important;
                line-height: 1.8 !important;
            }
            
            .stMarkdown code {
                font-size: 12px !important;
                padding: 2px 6px !important;
            }
            
            /* ═══════════════════════════════════════ */
            /* 🦶 Footer */
            /* ═══════════════════════════════════════ */
            
            .footer {
                padding: 15px !important;
                font-size: 11px !important;
                margin-top: 20px !important;
            }
        }
        
        /* ═══════════════════════════════════════════════ */
        /* 📱 شاشات صغيرة جداً - أقل من 480px (الفون العادي) */
        /* ═══════════════════════════════════════════════ */
        
        @media only screen and (max-width: 480px) {
            
            /* Header أصغر */
            .main-header {
                padding: 15px 12px !important;
                border-radius: 12px !important;
            }
            
            .main-header h1 {
                font-size: 19px !important;
            }
            
            .main-header p {
                font-size: 11px !important;
            }
            
            /* الإحصائيات أصغر */
            .stat-box {
                padding: 8px 3px !important;
                min-height: 58px !important;
            }
            
            .stat-number {
                font-size: 15px !important;
            }
            
            .stat-label {
                font-size: 9px !important;
            }
            
            /* التابات أصغر */
            .stTabs [data-baseweb="tab"] {
                font-size: 11px !important;
                padding: 6px 10px !important;
            }
            
            /* الأزرار أصغر */
            .stButton > button {
                font-size: 12px !important;
                padding: 8px 12px !important;
                min-height: 40px !important;
            }
            
            /* العناوين أصغر */
            h1 { font-size: 19px !important; }
            h2 { font-size: 17px !important; }
            h3 { font-size: 15px !important; }
            
            /* Padding أقل */
            .main .block-container {
                padding: 0.5rem !important;
            }
        }
        
        /* ═══════════════════════════════════════════════ */
        /* 📱 Landscape (الفون بالعرض) */
        /* ═══════════════════════════════════════════════ */
        
        @media only screen and (max-width: 768px) and (orientation: landscape) {
            
            .main-header {
                padding: 15px !important;
            }
            
            .main-header h1 {
                font-size: 20px !important;
            }
            
            .stat-box {
                min-height: 55px !important;
            }
        }
    </style>
    """