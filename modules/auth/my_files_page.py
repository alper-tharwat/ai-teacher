"""
📂 صفحة ملفاتي - تصميم احترافي + تقسيم فصول ذكي
"""

import streamlit as st
from datetime import datetime
from modules.auth.file_manager import (
    get_user_files, get_file_by_id, delete_file, 
    toggle_favorite, get_files_stats
)
from modules.auth.outputs_manager import get_all_outputs_for_file, OUTPUT_TYPES

# استيراد دوال التقسيم من upload_page
from pages.upload_page import smart_split, sort_chapters, display_chapters


def format_file_size(size_bytes):
    """تحويل حجم الملف لصيغة مقروءة"""
    if not size_bytes:
        return "غير محدد"
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def format_date(date_str):
    """تحويل التاريخ لصيغة مقروءة"""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
        diff = now - dt
        
        if diff.days == 0:
            if diff.seconds < 3600:
                return f"من {diff.seconds // 60} د"
            else:
                return f"من {diff.seconds // 3600} س"
        elif diff.days == 1:
            return "أمس"
        elif diff.days < 7:
            return f"من {diff.days} أيام"
        elif diff.days < 30:
            return f"من {diff.days // 7} أسبوع"
        else:
            return dt.strftime("%Y-%m-%d")
    except:
        return date_str[:10] if date_str else "غير محدد"


def get_file_icon(file_type):
    """أيقونة حسب نوع الملف"""
    icons = {
        'pdf': '📕', 'docx': '📘', 'doc': '📘', 'txt': '📄',
        'png': '🖼️', 'jpg': '🖼️', 'jpeg': '🖼️',
        'mp3': '🎵', 'wav': '🎵', 'm4a': '🎵',
        'mp4': '🎥', 'pptx': '📊', 'xlsx': '📊', 'csv': '📊',
    }
    return icons.get(file_type.lower(), '📁')


def load_file_to_session(file_data, ai=None):
    """تحميل الملف في session_state + تقسيم فصول ذكي"""
    extracted_text = file_data.get('extracted_text', '')
    metadata = file_data.get('metadata', {}) or {}
    total_pages = metadata.get('total_pages', 1) or 1
    
    # المعلومات الأساسية
    st.session_state.extracted_text = extracted_text
    st.session_state.file_info = {
        'name': file_data.get('file_name', ''),
        'size_readable': format_file_size(file_data.get('file_size', 0)),
        'extension': file_data.get('file_type', '').upper(),
    }
    st.session_state.all_pages = [extracted_text]
    st.session_state.total_pages = total_pages
    st.session_state.selected_range = (1, total_pages)
    st.session_state['current_file_id'] = file_data.get('id')
    
    # مسح المخرجات القديمة
    st.session_state.summary = ''
    st.session_state.explanation = ''
    st.session_state.quiz_data = None
    st.session_state.flashcards = []
    st.session_state.mindmap_data = None
    st.session_state.mindmap_html = ''
    
    # ✅ التقسيم الذكي للفصول (لو الملف كبير)
    if total_pages > 20 or len(extracted_text) > 10000:
        if ai:
            with st.spinner("📚 بقسم الملف لفصول ودروس..."):
                chapters = smart_split(ai, extracted_text, total_pages)
                chapters = sort_chapters(chapters)
                st.session_state['chapters'] = chapters
                st.session_state['current_chapter'] = None
                st.session_state['current_lesson'] = None
                st.session_state['extracted_text'] = ''
                st.session_state['opened_chapter_idx'] = None
    else:
        # ملف صغير - مفيش فصول
        st.session_state['chapters'] = None


def render_my_files_page():
    """صفحة ملفاتي - تصميم مضغوط واحترافي + فصول"""
    
    # ═══════════════════════════════════════════════════════
    # CSS مخصص
    # ═══════════════════════════════════════════════════════
    st.markdown("""
    <style>
        .files-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
        }
        .stat-mini {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 12px;
            border-radius: 10px;
            text-align: center;
        }
        .badge-mini {
            background: linear-gradient(135deg, #11998e, #38ef7d);
            color: white;
            padding: 2px 8px;
            border-radius: 8px;
            font-size: 10px;
            margin: 2px;
            display: inline-block;
        }
    </style>
    
    <div class="files-header">
        <h2 style='margin:0;'>📂 ملفاتي</h2>
        <p style='margin:5px 0 0; opacity:0.95; font-size:14px;'>كل ملفاتك محفوظة هنا</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════
    # لو فيه ملف محمل وعنده فصول → اعرض الفصول الأول
    # ═══════════════════════════════════════════════════════
    if st.session_state.get('chapters') and st.session_state.get('show_chapters_from_files'):
        render_chapters_view()
        return  # نخرج من الصفحة عشان نعرض الفصول بس
    
    # ═══════════════════════════════════════════════════════
    # الإحصائيات
    # ═══════════════════════════════════════════════════════
    stats = get_files_stats()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-mini">
            <h3 style='margin:0;'>📚 {stats.get('total', 0)}</h3>
            <p style='margin:2px 0 0; font-size:12px;'>إجمالي الملفات</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-mini" style='background:linear-gradient(135deg, #f093fb, #f5576c);'>
            <h3 style='margin:0;'>⭐ {stats.get('favorites', 0)}</h3>
            <p style='margin:2px 0 0; font-size:12px;'>المفضلة</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_mb = stats.get('total_size', 0) / (1024 * 1024)
        st.markdown(f"""
        <div class="stat-mini" style='background:linear-gradient(135deg, #43e97b, #38f9d7);'>
            <h3 style='margin:0;'>💾 {total_mb:.1f} MB</h3>
            <p style='margin:2px 0 0; font-size:12px;'>المساحة</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════
    # جلب الملفات
    # ═══════════════════════════════════════════════════════
    result = get_user_files(limit=100)
    
    if not result["success"]:
        st.error(result.get("message", "❌ خطأ في جلب الملفات"))
        return
    
    files = result["files"]
    
    if not files:
        st.markdown("""
        <div style='text-align:center; padding:40px 20px; background:#f8f9fa; border-radius:15px;'>
            <h1 style='font-size:50px; margin:0;'>📭</h1>
            <h4 style='color:#7f8c8d; margin:10px 0;'>لسه مفيش أي ملفات</h4>
            <p style='color:#95a5a6; font-size:14px;'>روح لتاب "📤 رفع ملف" وارفع ملفك الأول</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # ═══════════════════════════════════════════════════════
    # شريط البحث والفلترة
    # ═══════════════════════════════════════════════════════
    col_search, col_filter = st.columns([3, 1])
    
    with col_search:
        search_query = st.text_input(
            "🔍 ابحث:",
            placeholder="اكتب اسم الملف...",
            key="files_search",
            label_visibility="collapsed"
        )
    
    with col_filter:
        filter_option = st.selectbox(
            "🔧 الفلتر:",
            ["الكل", "المفضلة ⭐", "PDF", "Word", "صور", "صوت"],
            key="files_filter",
            label_visibility="collapsed"
        )
    
    # ═══════════════════════════════════════════════════════
    # فلترة الملفات
    # ═══════════════════════════════════════════════════════
    filtered_files = files
    
    if search_query:
        filtered_files = [
            f for f in filtered_files 
            if search_query.lower() in f.get('file_name', '').lower()
        ]
    
    if filter_option == "المفضلة ⭐":
        filtered_files = [f for f in filtered_files if f.get('is_favorite')]
    elif filter_option == "PDF":
        filtered_files = [f for f in filtered_files if f.get('file_type', '').lower() == 'pdf']
    elif filter_option == "Word":
        filtered_files = [f for f in filtered_files if f.get('file_type', '').lower() in ['docx', 'doc']]
    elif filter_option == "صور":
        filtered_files = [f for f in filtered_files if f.get('file_type', '').lower() in ['png', 'jpg', 'jpeg']]
    elif filter_option == "صوت":
        filtered_files = [f for f in filtered_files if f.get('file_type', '').lower() in ['mp3', 'wav', 'm4a']]
    
    st.markdown(f"### 📋 عدد الملفات: {len(filtered_files)}")
    
    if not filtered_files:
        st.info("🔍 مفيش نتائج للبحث ده")
        return
    
    # ═══════════════════════════════════════════════════════
    # عرض الملفات - 3 كروت في الصف
    # ═══════════════════════════════════════════════════════
    for row_start in range(0, len(filtered_files), 3):
        cols = st.columns(3)
        
        for i in range(3):
            idx = row_start + i
            if idx >= len(filtered_files):
                break
            
            file = filtered_files[idx]
            file_id = file.get('id')
            file_name = file.get('file_name', 'بدون اسم')
            file_type = file.get('file_type', '').lower()
            file_size = file.get('file_size', 0)
            is_favorite = file.get('is_favorite', False)
            last_accessed = file.get('last_accessed', '')
            metadata = file.get('metadata', {}) or {}
            
            icon = get_file_icon(file_type)
            
            # جلب المخرجات المحفوظة
            saved_outputs = get_all_outputs_for_file(file_id)
            
            # بناء badges للمخرجات
            badges_html = ""
            if saved_outputs:
                for output_type, _ in saved_outputs.items():
                    if output_type in OUTPUT_TYPES:
                        icon_text = OUTPUT_TYPES[output_type]
                        badges_html += f'<span class="badge-mini">{icon_text} ✓</span>'
            
            # قصر الاسم لو طويل
            display_name = file_name if len(file_name) <= 22 else file_name[:20] + "..."
            
            with cols[i]:
                # ═══════════════════════════════════════════════
                # كارت الملف - كبير وواضح
                # ═══════════════════════════════════════════════
                fav_star = "⭐" if is_favorite else ""
                
                # زر فتح الملف (الكارت كله)
                if st.button(
                    f"📖 {display_name}\n\n"
                    f"📦 {format_file_size(file_size)}  |  "
                    f"📅 {format_date(last_accessed)}\n"
                    f"📝 {metadata.get('word_count', 0)} كلمة {fav_star}",
                    key=f"open_file_{file_id}",
                    use_container_width=True,
                    type="primary",
                    help=f"اضغط لفتح: {file_name}"
                ):
                    # ═══════════════════════════════════════════
                    # فتح الملف + تقسيم فصول
                    # ═══════════════════════════════════════════
                    file_result = get_file_by_id(file_id)
                    if file_result["success"]:
                        # جلب الـ AI engine
                        from utils.ai_engine import AIEngine
                        ai = AIEngine()
                        
                        # تحميل الملف + تقسيم فصول
                        load_file_to_session(file_result["file"], ai=ai)
                        
                        # ✅ علم إننا جايين من "ملفاتي"
                        st.session_state['show_chapters_from_files'] = True
                        st.session_state['selected_file_name'] = file_name
                        
                        st.success(f"✅ تم تحميل: {file_name}")
                        st.rerun()
                    else:
                        st.error(file_result.get("message", "❌ خطأ"))
                
                # عرض المخرجات المحفوظة
                if badges_html:
                    st.markdown(f'{badges_html}', unsafe_allow_html=True)
                
                # زرار المفضلة والحذف
                col_fav, col_del = st.columns(2)
                
                with col_fav:
                    fav_icon = "⭐" if is_favorite else "☆"
                    if st.button(fav_icon, key=f"fav_{file_id}", use_container_width=True, help="مفضلة"):
                        toggle_result = toggle_favorite(file_id)
                        if toggle_result["success"]:
                            st.rerun()
                
                with col_del:
                    if st.button("🗑️", key=f"del_{file_id}", use_container_width=True, help="حذف"):
                        st.session_state[f"confirm_del_{file_id}"] = True
                        st.rerun()
                
                # تأكيد الحذف
                if st.session_state.get(f"confirm_del_{file_id}"):
                    st.warning(f"⚠️ حذف؟")
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.button("✅", key=f"yes_{file_id}", use_container_width=True, type="primary"):
                            del_result = delete_file(file_id)
                            if del_result["success"]:
                                if f"confirm_del_{file_id}" in st.session_state:
                                    del st.session_state[f"confirm_del_{file_id}"]
                                st.rerun()
                    with col_no:
                        if st.button("❌", key=f"no_{file_id}", use_container_width=True):
                            del st.session_state[f"confirm_del_{file_id}"]
                            st.rerun()


def render_chapters_view():
    """
    عرض الفصول زي الصورة - كروت كبيرة + دروس تحتها على طول
    """
    chapters = st.session_state.get('chapters', [])
    file_name = st.session_state.get('selected_file_name', 'الملف')
    
    if not chapters:
        st.warning("⚠️ مفيش فصول للملف ده")
        return
    
    # ═══════════════════════════════════════════════════════
    # هيدر الفصول
    # ═══════════════════════════════════════════════════════
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    ">
        <h2 style="margin: 0;">📚 فصول الملف</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">{file_name}</p>
        <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem;">{len(chapters)} فصل | اختار الفصل اللي عايز تذاكره</p>
    </div>
    """, unsafe_allow_html=True)
    
    # زر رجوع لملفاتي
    if st.button("⬅️ رجوع لملفاتي", use_container_width=True):
        st.session_state['show_chapters_from_files'] = False
        st.session_state['selected_file_name'] = None
        st.session_state['chapters'] = None
        st.session_state['extracted_text'] = ''
        st.rerun()
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════
    # عرض الفصول - 2 في الصف (زي الصورة)
    # ═══════════════════════════════════════════════════════
    # ألوان الكروت (خلفية + border)
    chapter_colors = [
        ('#e3f2fd', '#1565c0'),  # أزرق فاتح
        ('#f3e5f5', '#7b1fa2'),  # بنفسجي فاتح
        ('#e8f5e9', '#2e7d32'),  # أخضر فاتح
        ('#fff3e0', '#e65100'),  # برتقالي فاتح
        ('#fce4ec', '#c62828'),  # وردي فاتح
        ('#e0f2f1', '#00695c'),  # فيروزي فاتح
    ]
    
    for row_start in range(0, len(chapters), 2):
        cols = st.columns(2)
        
        for i in range(2):
            idx = row_start + i
            if idx >= len(chapters):
                break
            
            chapter = chapters[idx]
            bg_color, border_color = chapter_colors[idx % len(chapter_colors)]
            num_lessons = len(chapter['lessons'])
            
            with cols[i]:
                # ═══════════════════════════════════════════════
                # كارت الفصل الكبير (زي الصورة)
                # ═══════════════════════════════════════════════
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {bg_color}, white);
                    border: 3px solid {border_color};
                    border-radius: 20px;
                    padding: 1.5rem;
                    margin-bottom: 1rem;
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                ">
                    <div style="
                        background: linear-gradient(135deg, #667eea, #764ba2);
                        color: white;
                        padding: 1rem;
                        border-radius: 12px;
                        font-size: 1.3rem;
                        font-weight: 700;
                    ">
                        📖 {chapter['title']}
                    </div>
                    <div style="color: #666; margin-top: 0.5rem; font-size: 0.9rem;">
                        {num_lessons} درس
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # ═══════════════════════════════════════════════
                # دروس الفصل - تحت الكارت على طول (زي الصورة)
                # ═══════════════════════════════════════════════
                # 2 درس في الصف
                for lesson_row in range(0, num_lessons, 2):
                    lesson_cols = st.columns(2)
                    
                    for j in range(2):
                        lesson_idx = lesson_row + j
                        if lesson_idx >= num_lessons:
                            break
                        
                        lesson = chapter['lessons'][lesson_idx]
                        
                        with lesson_cols[j]:
                            # زر الدرس (شكل كارت صغير)
                            if st.button(
                                f"🚀 {lesson['title']}",
                                key=f"lesson_{idx}_{lesson_idx}",
                                use_container_width=True,
                                type="secondary"
                            ):
                                # تحميل الدرس
                                st.session_state.extracted_text = lesson['text']
                                st.session_state.current_chapter = idx
                                st.session_state.current_lesson = lesson_idx
                                st.session_state['show_chapters_from_files'] = False
                                st.success(f"✅ تم تحميل {lesson['title']}!")
                                st.info("💡 روح لتاب الشرح أو الامتحان!")
    
    # زر اذاكر الملف كله
    st.markdown("---")
    if st.button("📚 اذاكر الملف كله", use_container_width=True, type="primary"):
        all_text = ''
        for chapter in chapters:
            for lesson in chapter['lessons']:
                all_text += lesson['text'] + '\n\n'
        st.session_state.extracted_text = all_text
        st.session_state.current_chapter = None
        st.session_state.current_lesson = None
        st.session_state['show_chapters_from_files'] = False
        st.success("✅ تم تحميل الملف كله!")
        st.info("💡 روح لتاب الشرح!")