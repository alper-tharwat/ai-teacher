"""
📤 صفحة رفع الملفات - تصميم جديد (فصل + دروسه في مربع واحد)
"""
import streamlit as st
import re
from datetime import datetime
from utils.plan_limits import check_plan_limit, increment_usage
from modules.auth.file_manager import save_file


def render_upload_page(file_reader, ai):
    # ═══════════════════════════════════════
    # الهيدر
    # ═══════════════════════════════════════
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    ">
        <h1 style="margin: 0; font-size: 2rem;">📤 ارفع ملفك</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">🤖 هقسمهولك فصول ودروس ذكياً!</p>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # أنواع الملفات - 3 كروت صغيرة
    # ═══════════════════════════════════════
    cols = st.columns(3)
    cards = [
        ("📕", "مستندات", "PDF, DOCX, TXT", "#e3f2fd", "#1565c0"),
        ("🖼️", "صور", "PNG, JPG, GIF", "#f3e5f5", "#7b1fa2"),
        ("📊", "ملفات أخرى", "PPT, XLSX, CSV", "#e8f5e9", "#2e7d32"),
    ]
    for i, (icon, title, desc, bg, color) in enumerate(cards):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background: {bg};
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
                border: 2px solid {color}30;
            ">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="font-weight: 700; color: {color}; font-size: 1rem;">{title}</div>
                <div style="color: #666; font-size: 0.8rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # فحص الباقة
    # ═══════════════════════════════════════
    can_upload, msg = check_plan_limit("files")
    if not can_upload:
        st.error(msg)
        if st.button("💎 اترقى لباقة أعلى", key="upgrade_from_upload"):
            st.session_state['current_page'] = 'subscriptions'
            st.rerun()
        return
    else:
        st.caption(msg)

    # ═══════════════════════════════════════
    # رفع الملف
    # ═══════════════════════════════════════
    uploaded_file = st.file_uploader(
        "📎 اسحب الملف هنا أو اضغط للاختيار", 
        type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'gif', 'pptx', 'xlsx', 'csv']
    )

    if uploaded_file:
        # معلومات الملف - 3 كروت صغيرة
        cols = st.columns(3)
        info = [
            ("📄", "الاسم", uploaded_file.name[:20] + "..." if len(uploaded_file.name) > 20 else uploaded_file.name, "#e3f2fd", "#1565c0"),
            ("📦", "الحجم", f"{uploaded_file.size / (1024 * 1024):.2f} MB", "#f3e5f5", "#7b1fa2"),
            ("📁", "النوع", uploaded_file.name.split('.')[-1].upper(), "#e8f5e9", "#2e7d32"),
        ]
        for i, (icon, label, value, bg, color) in enumerate(info):
            with cols[i]:
                st.markdown(f"""
                <div style="
                    background: {bg};
                    border-radius: 12px;
                    padding: 1rem;
                    text-align: center;
                ">
                    <div style="font-size: 1.5rem;">{icon}</div>
                    <div style="font-weight: 700; color: {color}; font-size: 0.9rem;">{value}</div>
                    <div style="color: #666; font-size: 0.75rem;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        # زر البدء
        if st.button("🚀 ابدأ قراءة وتقسيم ذكي", use_container_width=True, type="primary"):
            with st.spinner("⏳..."):
                uploaded_file.seek(0)
                result = file_reader.read(uploaded_file)

            if result['success']:
                st.session_state.stats['files_processed'] += 1
                increment_usage('files')

                save_result = save_file(
                    file_name=uploaded_file.name,
                    file_type=uploaded_file.name.split('.')[-1].lower(),
                    extracted_text=result['text'],
                    file_size=uploaded_file.size,
                    metadata={
                        'total_pages': result.get('total_pages', 0),
                        'word_count': result.get('word_count', 0),
                        'upload_date': datetime.now().isoformat()
                    }
                )
                if save_result['success']:
                    st.session_state['current_file_id'] = save_result['file_id']

                text = result['text']
                total_pages = result.get('total_pages', 0)

                if total_pages > 20 or len(text) > 10000:
                    st.info("📚 بقسم الملف...")
                    chapters = smart_split(ai, text, total_pages)
                    # ✅ ترتيب وتنظيف الفصول
                    chapters = sort_chapters(chapters)
                    st.session_state['chapters'] = chapters
                    st.session_state['current_chapter'] = None
                    st.session_state['current_lesson'] = None
                    st.session_state['extracted_text'] = ''
                    st.success(f"✅ {len(chapters)} فصل")
                else:
                    st.session_state.extracted_text = text
                    st.session_state['chapters'] = None
                    st.success(f"✅ تم! ({result.get('word_count', 0)} كلمة)")
            else:
                st.error(result['error'])

    # ═══════════════════════════════════════
    # عرض الفصول (لو موجودة)
    # ═══════════════════════════════════════
    if st.session_state.get('chapters'):
        display_chapters(st.session_state['chapters'])


# ═══════════════════════════════════════════════════════
# التقسيم الذكي بالـ AI
# ═══════════════════════════════════════════════════════
def smart_split(ai, text, total_pages):
    """تقسيم النص لفصول ودروس باستخدام AI"""
    try:
        prompt = f"""قسم النص لفصول ودروس. ارد بصيغة:
فصل 1: [العنوان]
- درس 1: [العنوان]
- درس 2: [العنوان]
فصل 2: [العنوان]

النص: {text[:5000]}..."""
        result = ai.generate(prompt, task_type="summarize")
        if result and result.get('success'):
            return parse_chapters(result['text'], text, total_pages)
    except Exception as e:
        st.warning(f"⚠️ التقسيم الذكي فشل: {e}")
    return auto_split(text, total_pages)


# ═══════════════════════════════════════════════════════
# تحليل رد الـ AI
# ═══════════════════════════════════════════════════════
def parse_chapters(ai_response, full_text, total_pages):
    """تحليل الرد وتحويله لهيكل فصول ودروس"""
    chapters = []
    current_chapter = None
    for line in ai_response.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('فصل') or line.startswith('##'):
            if current_chapter:
                chapters.append(current_chapter)
            title = line.replace('##', '').replace(':', '').strip()
            current_chapter = {'title': title, 'lessons': []}
        elif line.startswith('-') or line.startswith('درس'):
            if current_chapter:
                lesson_info = parse_lesson_line(line, full_text, total_pages)
                current_chapter['lessons'].append(lesson_info)
    if current_chapter:
        chapters.append(current_chapter)
    if not chapters:
        return auto_split(full_text, total_pages)
    return chapters


# ═══════════════════════════════════════════════════════
# تحليل سطر الدرس
# ═══════════════════════════════════════════════════════
def parse_lesson_line(line, full_text, total_pages):
    """تحليل سطر الدرس واستخراج معلوماته"""
    line = line.replace('-', '').strip()
    pages_match = re.search(r'صفحات?:?\s*(\d+)-(\d+)', line)
    if pages_match:
        start_page = int(pages_match.group(1))
        end_page = int(pages_match.group(2))
        title = re.sub(r'\|.*$', '', line).strip()
    else:
        start_page = 1
        end_page = total_pages
        title = line
    text_start = int((start_page / total_pages) * len(full_text)) if total_pages > 0 else 0
    text_end = int((end_page / total_pages) * len(full_text)) if total_pages > 0 else len(full_text)
    return {
        'title': title,
        'start_page': start_page,
        'end_page': end_page,
        'text': full_text[text_start:text_end][:3000]
    }


# ═══════════════════════════════════════════════════════
# التقسيم التلقائي (Fallback)
# ═══════════════════════════════════════════════════════
def auto_split(text, total_pages):
    """تقسيم تلقائي لو التقسيم الذكي فشل"""
    chapters = []
    found_chapters = []
    for pattern in [
        r'الفصل\s+(الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر)', 
        r'الفصل\s+\d+', 
        r'Chapter\s+\d+'
    ]:
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            for match in matches:
                found_chapters.append({'pos': match.start(), 'title': match.group(0)})
            break
    if found_chapters:
        for i, chap in enumerate(found_chapters):
            start = chap['pos']
            end = found_chapters[i + 1]['pos'] if i + 1 < len(found_chapters) else len(text)
            chapter_text = text[start:end]
            lessons = split_into_lessons(chapter_text, 20)
            chapters.append({'title': chap['title'], 'lessons': lessons})
    else:
        lessons = split_into_lessons(text, 20)
        chapters.append({'title': 'الفصل 1', 'lessons': lessons})
    return chapters


# ═══════════════════════════════════════════════════════
# تقسيم النص لدروس
# ═══════════════════════════════════════════════════════
def split_into_lessons(text, pages_per_lesson):
    """تقسيم النص لدروس صغيرة"""
    total_chars = len(text)
    chars_per_lesson = int(total_chars / max(1, total_chars // (pages_per_lesson * 500)))
    lessons = []
    start = 0
    while start < total_chars:
        end = min(start + chars_per_lesson, total_chars)
        if end < total_chars:
            next_break = text.find('\n\n', end)
            if next_break == -1:
                next_break = text.find('.', end)
            if next_break != -1 and next_break < end + 500:
                end = next_break + 1
        lesson_text = text[start:end].strip()
        if lesson_text:
            lessons.append({
                'title': f'درس {len(lessons) + 1}', 
                'start_page': 0, 
                'end_page': 0, 
                'text': lesson_text[:3000]
            })
        start = end
    return lessons


# ═══════════════════════════════════════════════════════
# دالة ترتيب وتنظيف الفصول (بدون تكرار)
# ═══════════════════════════════════════════════════════
def sort_chapters(chapters):
    """ترتيب الفصول حسب الرقم + إزالة التكرارات"""
    
    arabic_numbers = {
        'الأول': 1, 'الأولى': 1, 'الاول': 1,
        'الثاني': 2, 'الثانية': 2,
        'الثالث': 3, 'الثالثة': 3,
        'الرابع': 4, 'الرابعة': 4,
        'الخامس': 5, 'الخامسة': 5,
        'السادس': 6, 'السادسة': 6,
        'السابع': 7, 'السابعة': 7,
        'الثامن': 8, 'الثامنة': 8,
        'التاسع': 9, 'التاسعة': 9,
        'العاشر': 10, 'العاشرة': 10,
        'الحادي عشر': 11, 'الثاني عشر': 12,
        'الثالث عشر': 13, 'الرابع عشر': 14,
        'الخامس عشر': 15, 'السادس عشر': 16,
        'السابع عشر': 17, 'الثامن عشر': 18,
        'التاسع عشر': 19, 'العشرون': 20,
    }
    
    def get_chapter_number(chapter):
        title = chapter.get('title', '').strip()
        number_match = re.search(r'\d+', title)
        if number_match:
            return int(number_match.group())
        for arabic_word, number in arabic_numbers.items():
            if arabic_word in title:
                return number
        return 999
    
    # تجميع الفصول المكررة
    chapters_dict = {}
    for chapter in chapters:
        chapter_num = get_chapter_number(chapter)
        if chapter_num not in chapters_dict:
            chapters_dict[chapter_num] = {
                'title': chapter['title'],
                'lessons': list(chapter.get('lessons', []))
            }
        else:
            existing_lessons = chapters_dict[chapter_num]['lessons']
            new_lessons = chapter.get('lessons', [])
            for lesson in new_lessons:
                lesson_title = lesson.get('title', '')
                already_exists = any(
                    l.get('title') == lesson_title 
                    for l in existing_lessons
                )
                if not already_exists:
                    existing_lessons.append(lesson)
    
    # إعادة ترقيم الدروس
    for chapter_num, chapter_data in chapters_dict.items():
        for i, lesson in enumerate(chapter_data['lessons'], 1):
            if 'درس' in lesson.get('title', '').lower():
                lesson['title'] = f'الدرس {get_arabic_ordinal(i)}'
    
    # ترتيب الفصول
    sorted_nums = sorted(chapters_dict.keys())
    
    arabic_ordinals = {
        1: 'الأول', 2: 'الثاني', 3: 'الثالث', 4: 'الرابع',
        5: 'الخامس', 6: 'السادس', 7: 'السابع', 8: 'الثامن',
        9: 'التاسع', 10: 'العاشر', 11: 'الحادي عشر',
        12: 'الثاني عشر', 13: 'الثالث عشر', 14: 'الرابع عشر',
        15: 'الخامس عشر', 16: 'السادس عشر', 17: 'السابع عشر',
        18: 'الثامن عشر', 19: 'التاسع عشر', 20: 'العشرون',
    }
    
    result = []
    for num in sorted_nums:
        chapter_data = chapters_dict[num]
        if num in arabic_ordinals:
            chapter_data['title'] = f'الفصل {arabic_ordinals[num]}'
        elif num != 999:
            chapter_data['title'] = f'الفصل {num}'
        result.append(chapter_data)
    
    return result


def get_arabic_ordinal(num):
    """تحويل الرقم لكلمة عربية"""
    ordinals = {
        1: 'الأول', 2: 'الثاني', 3: 'الثالث', 4: 'الرابع',
        5: 'الخامس', 6: 'السادس', 7: 'السابع', 8: 'الثامن',
        9: 'التاسع', 10: 'العاشر', 11: 'الحادي عشر',
        12: 'الثاني عشر', 13: 'الثالث عشر', 14: 'الرابع عشر',
        15: 'الخامس عشر', 16: 'السادس عشر', 17: 'السابع عشر',
        18: 'الثامن عشر', 19: 'التاسع عشر', 20: 'العشرون',
    }
    return ordinals.get(num, str(num))


# ═══════════════════════════════════════════════════════
# عرض الفصول - كل فصل في مربع كامل مع دروسه
# ═══════════════════════════════════════════════════════
def display_chapters(chapters, key_prefix="main"):
    """
    عرض الفصول - كل فصل في مربع فيه:
    - عنوان الفصل
    - كل الدروس بتاعته
    ضغطة واحدة على الدرس تحمّله
    """
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h2 style="color: #1a237e; margin: 0;">📚 فصول الملف</h2>
        <p style="color: #666;">اضغط على الدرس عشان تحمّله</p>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════
    # عرض الدرس الحالي - مع فحص كامل للأنواع
    # ═══════════════════════════════════════════════
    try:
        current_ch = st.session_state.get('current_chapter')
        current_ls = st.session_state.get('current_lesson')
        
        # ✅ التأكد إنهم أرقام صحيحة (integers)
        if (current_ch is not None and 
            current_ls is not None and 
            isinstance(current_ch, int) and 
            isinstance(current_ls, int) and 
            0 <= current_ch < len(chapters)):
            
            chapter_lessons = chapters[current_ch].get('lessons', [])
            
            if 0 <= current_ls < len(chapter_lessons):
                ch_title = chapters[current_ch].get('title', 'فصل')
                ls_title = chapter_lessons[current_ls].get('title', 'درس')
                st.success(f"📖 الدرس الحالي: {ch_title} - {ls_title}")
    except Exception as e:
        # تجاهل أي خطأ في عرض الدرس الحالي
        pass

    # ألوان الكروت
    colors = [
        ("#e3f2fd", "#1565c0", "#90caf9", "📘"),
        ("#f3e5f5", "#7b1fa2", "#ce93d8", "📗"),
        ("#e8f5e9", "#2e7d32", "#a5d6a7", "📙"),
        ("#fff3e0", "#e65100", "#ffb74d", "📕"),
        ("#fce4ec", "#c62828", "#f48fb1", "📓"),
        ("#e0f2f1", "#00695c", "#80cbc4", "📔"),
    ]

    # عرض الفصول - 2 في الصف
    for row_start in range(0, len(chapters), 2):
        cols = st.columns(2)
        for i in range(2):
            idx = row_start + i
            if idx >= len(chapters):
                break
            chapter = chapters[idx]
            bg, title_color, border, icon = colors[idx % len(colors)]

            with cols[i]:
                # المربع الكامل للفصل
                st.markdown(f"""
                <div style="
                    background: {bg};
                    border: 3px solid {title_color};
                    border-radius: 20px;
                    padding: 1.5rem;
                    margin-bottom: 1rem;
                    min-height: 100px;
                ">
                    <div style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 1rem;
                        border-radius: 12px;
                        text-align: center;
                        margin-bottom: 1rem;
                        font-size: 1.2rem;
                        font-weight: bold;
                    ">
                        {icon} {chapter.get('title', 'فصل')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # الدروس تحت العنوان (زرارير)
                lessons = chapter.get('lessons', [])
                
                # عرض الدروس - 2 في الصف داخل الفصل
                for lesson_row in range(0, len(lessons), 2):
                    lesson_cols = st.columns(2)
                    for j in range(2):
                        lesson_idx = lesson_row + j
                        if lesson_idx >= len(lessons):
                            break
                        lesson = lessons[lesson_idx]
                        
                        with lesson_cols[j]:
                            lesson_label = f"📌 {lesson.get('title', 'درس')}"
                            # ✅ key فريد بـ prefix
                            unique_key = f"{key_prefix}_lesson_{idx}_{lesson_idx}"
                            
                            if st.button(
                                lesson_label,
                                key=unique_key,
                                use_container_width=True,
                            ):
                                st.session_state.extracted_text = lesson.get('text', '')
                                # ✅ حفظ الأرقام كـ integers صريحة
                                st.session_state.current_chapter = int(idx)
                                st.session_state.current_lesson = int(lesson_idx)
                                st.success(f"✅ تم تحميل {lesson.get('title', 'الدرس')}!")
                                st.info("👆 روح لتاب الشرح والتلخيص")
                                st.rerun()