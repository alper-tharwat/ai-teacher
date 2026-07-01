"""
🖥️ ملف CSS للكمبيوتر - v6.0 Complete
كل التصميم والشكل في ملف واحد
"""


def get_desktop_css():
    """يرجع CSS الكمبيوتر - تصميم كامل"""
    
    return """
    <style>
        /* ═══════════════════════════════════════════════════ */
        /* 📦 الإعدادات الأساسية والخطوط                       */
        /* ═══════════════════════════════════════════════════ */
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');
        
        * { 
            font-family: 'Cairo', sans-serif !important; 
        }

        /* ═══════════════════════════════════════════════════ */
        /* 🚫 إخفاء أيقونات Material Icons                    */
        /* ═══════════════════════════════════════════════════ */
        .material-icons,
        .material-icons-outlined,
        .material-symbols-outlined,
        .material-symbols-rounded,
        span[class*="material-symbols"],
        span[class*="material-icons"],
        i[class*="material"] {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            opacity: 0 !important;
            font-size: 0 !important;
            overflow: hidden !important;
        }
        
        [data-testid="stFileUploader"] svg,
        [data-testid="stFileUploaderDropzone"] svg,
        [data-testid="stExpander"] summary svg,
        [data-baseweb="select"] svg {
            display: none !important;
        }
        
        [data-testid="stExpander"] > details > summary::after {
            content: '▼';
            font-size: 14px;
            color: #667eea;
            margin-left: auto;
            margin-right: 10px;
            transition: transform 0.3s ease;
            order: -1;
        }
        
        [data-testid="stExpander"] > details[open] > summary::after {
            transform: rotate(180deg);
        }
        
        .stSelectbox [data-baseweb="select"] > div::after {
            content: '▼';
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 12px;
            color: #667eea;
            pointer-events: none;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 📄 إعدادات الصفحة العامة                            */
        /* ═══════════════════════════════════════════════════ */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6,
        .main p, .main label, .main .stMarkdown {
            direction: rtl;
            text-align: right;
        }
        
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf3 100%);
        }

        /* ═══════════════════════════════════════════════════ */
        /* 🎛️ Sidebar - السايد بار النظيف                     */
        /* ═══════════════════════════════════════════════════ */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
            border-left: 3px solid rgba(255,255,255,0.2) !important;
            box-shadow: -5px 0 20px rgba(0,0,0,0.1) !important;
        }
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stCaption,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            direction: rtl !important;
            text-align: right !important;
            color: white !important;
        }
        
        [data-testid="stSidebar"] .stButton > button {
            background: rgba(255,255,255,0.2) !important;
            backdrop-filter: blur(10px) !important;
            color: white !important;
            border: 2px solid rgba(255,255,255,0.3) !important;
            border-radius: 15px !important;
            padding: 10px 20px !important;
            font-weight: 700 !important;
            transition: all 0.3s !important;
        }
        
        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255,255,255,0.3) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        }
        
        /* Metrics في السايدبار */
        [data-testid="stSidebar"] [data-testid="stMetric"] {
            background: rgba(255,255,255,0.15) !important;
            backdrop-filter: blur(10px) !important;
            padding: 12px !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            margin: 5px 0 !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
            color: rgba(255,255,255,0.9) !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stMetricValue"] {
            color: white !important;
            font-size: 24px !important;
            font-weight: 900 !important;
        }
        
        /* Info boxes في السايدبار */
        [data-testid="stSidebar"] [data-testid="stAlert"] {
            background: rgba(255,255,255,0.15) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stAlert"] p,
        [data-testid="stSidebar"] [data-testid="stAlert"] div {
            color: white !important;
        }
        
        /* زرار الـ Toggle */
        [data-testid="collapsedControl"] {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: white !important;
            border-radius: 15px !important;
            padding: 8px 12px !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
            transition: all 0.3s !important;
            top: 1rem !important;
        }
        
        [data-testid="collapsedControl"]:hover {
            transform: scale(1.1) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
            padding: 20px 15px !important;
        }
        
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.2) !important;
            margin: 20px 0 !important;
        }

        /* Expander في السايدبار */
        [data-testid="stSidebar"] [data-testid="stExpander"] {
            background: rgba(255,255,255,0.1) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stExpander"] summary {
            background: transparent !important;
            color: white !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stExpander"] summary p {
            color: white !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 🎨 الـ Header الرئيسي                                */
        /* ═══════════════════════════════════════════════════ */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            padding: 35px 30px;
            border-radius: 25px;
            text-align: center;
            color: white;
            margin-bottom: 30px;
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
            direction: rtl;
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 8s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }
        
        .main-header h1 {
            font-size: 48px !important;
            margin: 0 !important;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
            font-weight: 900 !important;
            color: white !important;
            position: relative;
            z-index: 1;
        }
        
        .main-header p {
            font-size: 20px;
            margin-top: 12px;
            opacity: 0.95;
            color: white !important;
            position: relative;
            z-index: 1;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 📊 صناديق الإحصائيات (الكروت) - مظبوطة!            */
        /* ═══════════════════════════════════════════════════ */
        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            padding: 20px 15px;
            border-radius: 18px;
            text-align: center;
            margin: 10px 0;
            direction: rtl;
            transition: all 0.3s ease;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .stat-box::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 60%);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .stat-box:hover::before {
            opacity: 1;
        }
        
        .stat-box:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5);
        }
        
        .stat-box .stat-number {
            font-size: 38px !important;
            font-weight: 900 !important;
            margin: 0 !important;
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
        }
        
        .stat-box .stat-label {
            font-size: 14px !important;
            opacity: 0.95;
            margin-top: 8px !important;
            font-weight: 700 !important;
            color: white !important;
            position: relative;
            z-index: 1;
        }
        
        .stat-box p {
            color: white !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 👤 User Card                                        */
        /* ═══════════════════════════════════════════════════ */
        .sidebar-user-card {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(15px);
            padding: 25px 20px;
            border-radius: 20px;
            text-align: center;
            margin: 15px 0;
            border: 2px solid rgba(255,255,255,0.2);
            color: white;
        }
        
        .sidebar-avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #11998e, #38ef7d);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            font-weight: 900;
            color: white;
            margin: 0 auto 15px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.2);
            border: 3px solid rgba(255,255,255,0.3);
        }
        
        .sidebar-user-name {
            font-size: 18px;
            font-weight: 700;
            color: white;
            margin: 8px 0 4px;
        }
        
        .sidebar-user-email {
            font-size: 12px;
            opacity: 0.85;
            color: white;
            margin: 0 0 12px;
            word-break: break-all;
        }
        
        .sidebar-user-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        }
        
        .badge-admin {
            background: linear-gradient(135deg, #FFD700, #FFA500);
            color: #333;
        }
        
        .badge-student {
            background: linear-gradient(135deg, #11998e, #38ef7d);
            color: white;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 🔘 الأزرار الرئيسية                                 */
        /* ═══════════════════════════════════════════════════ */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 12px 30px !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        }
        
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
            box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #38ef7d 0%, #11998e 100%) !important;
            box-shadow: 0 8px 25px rgba(17, 153, 142, 0.6) !important;
        }
        
        [data-testid="stDownloadButton"] > button {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        }
        
        [data-testid="stDownloadButton"] > button:hover {
            background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%) !important;
            box-shadow: 0 8px 25px rgba(245, 87, 108, 0.5) !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 📑 التابات                                          */
        /* ═══════════════════════════════════════════════════ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px !important;
            background: linear-gradient(135deg, #f0f2f6 0%, #e8ecf3 100%) !important;
            padding: 12px !important;
            border-radius: 18px !important;
            direction: rtl !important;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.05) !important;
            margin-bottom: 5px !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: white !important;
            border-radius: 12px !important;
            padding: 10px 20px !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            direction: rtl !important;
            transition: all 0.3s ease !important;
            border: 2px solid transparent !important;
            color: #2c3e50 !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: linear-gradient(135deg, #f8f9ff 0%, #eef0ff 100%) !important;
            border-color: #667eea !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border-color: transparent !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        }
        
        /* مسافة قليلة بين صفوف التابات */
        .stTabs {
            margin-bottom: 8px !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 📤 File Uploader                                    */
        /* ═══════════════════════════════════════════════════ */
        [data-testid="stFileUploader"] {
            direction: ltr;
        }
        
        [data-testid="stFileUploader"] > label {
            direction: rtl !important;
            text-align: right !important;
            width: 100%;
            display: block;
            unicode-bidi: plaintext;
            font-size: 16px !important;
            font-weight: 700 !important;
            color: #2c3e50 !important;
            margin-bottom: 10px !important;
        }
        
        [data-testid="stFileUploader"] section {
            direction: ltr !important;
            padding: 25px !important;
            border-radius: 15px !important;
            background: linear-gradient(135deg, #f8f9ff 0%, #eef0ff 100%) !important;
            border: 2px dashed #667eea !important;
            transition: all 0.3s ease !important;
        }
        
        [data-testid="stFileUploader"] section:hover {
            background: linear-gradient(135deg, #eef0ff 0%, #e0e5ff 100%) !important;
            border-color: #764ba2 !important;
            transform: scale(1.01) !important;
        }
        
        [data-testid="stFileUploaderDropzone"] {
            direction: ltr !important;
            min-height: 100px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            gap: 20px !important;
        }
        
        [data-testid="stFileUploaderDropzone"] button {
            direction: ltr !important;
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 28px !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            order: 1 !important;
            transition: all 0.3s !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
        }
        
        [data-testid="stFileUploaderDropzone"] button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 18px rgba(102, 126, 234, 0.5) !important;
        }
        
        [data-testid="stFileUploaderDropzoneInstructions"] {
            direction: ltr !important;
            order: 2 !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 📋 Expanders                                        */
        /* ═══════════════════════════════════════════════════ */
        [data-testid="stExpander"] {
            border-radius: 12px !important;
            border: 2px solid #e0e0e0 !important;
            margin: 12px 0 !important;
            background: white !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
            transition: all 0.3s ease !important;
            overflow: hidden !important;
        }
        
        [data-testid="stExpander"]:hover {
            border-color: #667eea !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15) !important;
        }
        
        [data-testid="stExpander"] > details > summary {
            direction: rtl !important;
            text-align: right !important;
            padding: 14px 18px !important;
            list-style: none !important;
            display: flex !important;
            flex-direction: row-reverse !important;
            justify-content: space-between !important;
            align-items: center !important;
            cursor: pointer !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%) !important;
            transition: background 0.3s !important;
        }
        
        [data-testid="stExpander"] > details > summary:hover {
            background: linear-gradient(135deg, #eef0ff 0%, #f8f9ff 100%) !important;
        }
        
        [data-testid="stExpander"] > details > summary::-webkit-details-marker {
            display: none !important;
        }
        
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary span,
        [data-testid="stExpander"] summary div {
            direction: rtl !important;
            text-align: right !important;
            flex: 1 !important;
        }
        
        [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
            direction: rtl !important;
            padding: 18px !important;
            background: white !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 📝 Selectbox                                        */
        /* ═══════════════════════════════════════════════════ */
        [data-testid="stSelectbox"] > label {
            direction: rtl !important;
            text-align: right !important;
            width: 100% !important;
            display: block !important;
            unicode-bidi: plaintext;
            font-size: 15px !important;
            font-weight: 700 !important;
            color: #2c3e50 !important;
            margin-bottom: 8px !important;
        }
        
        [data-testid="stSelectbox"] > div {
            direction: ltr !important;
        }
        
        .stSelectbox [data-baseweb="select"] {
            direction: ltr !important;
        }
        
        .stSelectbox [data-baseweb="select"] > div {
            direction: rtl !important;
            text-align: right !important;
            padding: 10px 15px 10px 45px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            border: 2px solid #e0e0e0 !important;
            transition: all 0.3s !important;
            background: white !important;
        }
        
        .stSelectbox [data-baseweb="select"] > div:hover {
            border-color: #667eea !important;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15) !important;
        }
        
        [data-baseweb="popover"] {
            direction: rtl !important;
        }
        
        [data-baseweb="popover"] li {
            direction: rtl !important;
            text-align: right !important;
            font-size: 15px !important;
            padding: 10px 15px !important;
            transition: background 0.2s !important;
        }
        
        [data-baseweb="popover"] li:hover {
            background: linear-gradient(135deg, #f0f4ff, #e8edff) !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 📝 Text Input & Text Area                          */
        /* ═══════════════════════════════════════════════════ */
        [data-testid="stTextInput"] > label,
        [data-testid="stTextArea"] > label,
        [data-testid="stNumberInput"] > label {
            direction: rtl !important;
            text-align: right !important;
            width: 100% !important;
            display: block !important;
            unicode-bidi: plaintext;
            font-size: 15px !important;
            font-weight: 700 !important;
            color: #2c3e50 !important;
            margin-bottom: 8px !important;
        }
        
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input {
            direction: rtl !important;
            text-align: right !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            padding: 12px 16px !important;
            border-radius: 12px !important;
            border: 2px solid #e0e0e0 !important;
            line-height: 1.8 !important;
            transition: all 0.3s !important;
            background: white !important;
        }
        
        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
            outline: none !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 🔘 Radio Buttons                                    */
        /* ═══════════════════════════════════════════════════ */
        [data-testid="stRadio"] > label {
            direction: rtl !important;
            text-align: right !important;
            width: 100% !important;
            display: block !important;
            unicode-bidi: plaintext;
            font-size: 15px !important;
            font-weight: 700 !important;
            color: #2c3e50 !important;
            margin-bottom: 10px !important;
        }
        
        [data-testid="stRadio"] > div {
            direction: rtl !important;
            gap: 10px !important;
        }
        
        [data-testid="stRadio"] > div > label {
            direction: rtl !important;
            flex-direction: row-reverse !important;
            justify-content: flex-start !important;
            padding: 14px 20px !important;
            background: white !important;
            border-radius: 14px !important;
            border: 2px solid #e0e0e0 !important;
            margin: 8px 0 !important;
            transition: all 0.3s !important;
            cursor: pointer !important;
            width: 100% !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        }
        
        [data-testid="stRadio"] > div > label:hover {
            border-color: #667eea !important;
            background: linear-gradient(135deg, #f8f9ff, #f0f4ff) !important;
            transform: translateX(-5px) !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2) !important;
        }
        
        [data-testid="stRadio"] > div > label p {
            font-size: 16px !important;
            font-weight: 600 !important;
            color: #2c3e50 !important;
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Cairo', sans-serif !important;
            line-height: 1.8 !important;
            margin: 0 !important;
            padding: 0 10px !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 📊 Metrics (الافتراضية للصفحة الرئيسية)            */
        /* ═══════════════════════════════════════════════════ */
        [data-testid="stMetric"] {
            direction: rtl;
            text-align: right;
            background: linear-gradient(135deg, white, #f8f9ff);
            padding: 18px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.06);
            border: 2px solid #f0f2f6;
            transition: all 0.3s;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
            border-color: #667eea;
        }
        
        [data-testid="stMetricLabel"] {
            direction: rtl !important;
            text-align: right !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            color: #6c757d !important;
        }
        
        [data-testid="stMetricValue"] {
            direction: rtl !important;
            text-align: right !important;
            font-size: 26px !important;
            font-weight: 900 !important;
            color: #2c3e50 !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 🚨 Alerts                                           */
        /* ═══════════════════════════════════════════════════ */
        [data-testid="stAlert"] {
            direction: rtl !important;
            text-align: right !important;
            border-radius: 14px !important;
            padding: 16px 20px !important;
            font-size: 15px !important;
            font-weight: 500 !important;
            border-right: 5px solid !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        }
        
        [data-testid="stAlert"] > div {
            direction: rtl !important;
            flex-direction: row-reverse !important;
        }
        
        [data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
            direction: rtl !important;
            text-align: right !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 📋 Quiz Questions                                   */
        /* ═══════════════════════════════════════════════════ */
        .quiz-question {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
            padding: 28px !important;
            border-radius: 20px !important;
            margin: 22px 0 !important;
            direction: rtl !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08) !important;
            border-right: 6px solid #667eea !important;
        }
        
        .quiz-question h4 {
            font-size: 19px !important;
            font-weight: 700 !important;
            color: #2c3e50 !important;
            line-height: 1.9 !important;
            margin: 0 !important;
        }
        
        .quiz-correct {
            background: linear-gradient(135deg, #d4edda, #c3e6cb) !important;
            color: #155724 !important;
            padding: 20px !important;
            border-radius: 14px !important;
            border-right: 5px solid #28a745 !important;
            margin-top: 14px !important;
            direction: rtl !important;
            font-size: 15px !important;
            font-weight: 600 !important;
        }
        
        .quiz-wrong {
            background: linear-gradient(135deg, #f8d7da, #f5c6cb) !important;
            color: #721c24 !important;
            padding: 20px !important;
            border-radius: 14px !important;
            border-right: 5px solid #dc3545 !important;
            margin-top: 14px !important;
            direction: rtl !important;
            font-size: 15px !important;
            font-weight: 600 !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 🎯 Range Card                                       */
        /* ═══════════════════════════════════════════════════ */
        .range-card {
            background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
            color: white;
            padding: 25px;
            border-radius: 20px;
            text-align: center;
            margin: 15px 0;
            direction: rtl;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }

        /* ═══════════════════════════════════════════════════ */
        /* 🎴 Flashcards                                       */
        /* ═══════════════════════════════════════════════════ */
        .unknown-card-item {
            background: linear-gradient(135deg, #fff5f5, #ffe0e0);
            padding: 16px;
            border-radius: 12px;
            margin: 10px 0;
            border-right: 5px solid #dc3545;
            direction: rtl;
            font-size: 15px;
            font-weight: 600;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 🧠 Mind Map Info                                    */
        /* ═══════════════════════════════════════════════════ */
        .mindmap-info {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 18px;
            border-radius: 15px;
            text-align: center;
            margin: 10px 0;
            direction: rtl;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        }

        /* ═══════════════════════════════════════════════════ */
        /* 💬 Chat Messages                                    */
        /* ═══════════════════════════════════════════════════ */
        [data-testid="stChatMessage"] {
            direction: rtl !important;
            background: white !important;
            border-radius: 15px !important;
            padding: 15px !important;
            margin: 10px 0 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        }
        
        [data-testid="stChatInput"] {
            direction: rtl !important;
        }
        
        [data-testid="stChatInput"] textarea {
            direction: rtl !important;
            text-align: right !important;
            font-size: 15px !important;
            border-radius: 25px !important;
            padding: 12px 20px !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 📊 Progress Bar                                     */
        /* ═══════════════════════════════════════════════════ */
        .stProgress > div > div {
            direction: ltr !important;
            border-radius: 10px !important;
        }
        
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #667eea, #764ba2, #f093fb) !important;
            border-radius: 10px !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 📝 Markdown Text                                    */
        /* ═══════════════════════════════════════════════════ */
        .stMarkdown {
            font-size: 15px !important;
            line-height: 1.9 !important;
        }
        
        .stMarkdown p {
            font-size: 15px !important;
            line-height: 1.9 !important;
            margin: 12px 0 !important;
        }
        
        .stMarkdown strong {
            color: #667eea !important;
            font-weight: 700 !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 🦶 Footer                                           */
        /* ═══════════════════════════════════════════════════ */
        .footer {
            text-align: center;
            padding: 25px;
            color: #888;
            font-size: 14px;
            margin-top: 60px;
            border-top: 2px solid #eee;
            direction: rtl;
            background: linear-gradient(135deg, transparent, rgba(102, 126, 234, 0.05));
            border-radius: 15px;
        }

/* ═══════════════════════════════════════════════════ */
/* 🔇 إخفاء عناصر Streamlit + السايد بار              */
/* ═══════════════════════════════════════════════════ */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* إخفاء السايد بار كاملاً */
[data-testid="stSidebar"] {
    display: none !important;
}

[data-testid="collapsedControl"] {
    display: none !important;
}

/* استخدام كامل عرض الشاشة */
.main .block-container {
    max-width: 100% !important;
    padding-right: 3rem !important;
    padding-left: 3rem !important;
}
        
        .viewerBadge_container__1QSob {
            display: none !important;
        }

        /* ═══════════════════════════════════════════════════ */
        /* 🎬 Audio Player                                     */
        /* ═══════════════════════════════════════════════════ */
        audio {
            direction: ltr !important;
            width: 100% !important;
            border-radius: 25px !important;
        }
        
        /* ═══════════════════════════════════════════════════ */
        /* 🎨 Animations                                       */
        /* ═══════════════════════════════════════════════════ */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stMarkdown, .stAlert {
            animation: fadeIn 0.4s ease-out;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2, #667eea);
        }

        /* ═══════════════════════════════════════════════════ */
        /* 🌟 تأثيرات إضافية                                   */
        /* ═══════════════════════════════════════════════════ */
        .stImage img {
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
            transition: all 0.3s !important;
        }
        
        .stImage img:hover {
            transform: scale(1.02) !important;
        }
        
        [data-testid="stDataFrame"] {
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        }
        
        [data-testid="stCaptionContainer"] {
            color: #6c757d !important;
            font-size: 13px !important;
            font-style: italic !important;
            direction: rtl !important;
            text-align: right !important;
        }
    </style>
    """