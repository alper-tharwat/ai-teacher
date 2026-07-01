"""
🚀 الإضافة الذكية للكتب - كل حاجة في خطوة واحدة
"""

import streamlit as st
from modules.library.smart_library_manager import (
    get_all_stages, create_stage,
    get_grades_by_stage, create_grade,
    get_subjects_by_grade, create_subject,
    create_chapter, create_lesson
)
from modules.library.templates import (
    STAGES, GRADES_BY_STAGE, TERMS, COLLEGES,
    get_subject_icon, get_random_color, get_stage_grades, get_terms_for_stage
)
from modules.library.book_analyzer import analyze_book_structure
from modules.library.auto_generator import auto_generate_for_chapter
from modules.auth.supabase_client import get_supabase_client


def find_or_create_stage(stage_name, college_name=None):
    """يدور على المرحلة، لو مش موجودة يعملها"""
    
    if stage_name == 'جامعي' and college_name:
        full_stage_name = "جامعي - " + college_name
    else:
        full_stage_name = stage_name
    
    existing_stages = get_all_stages()
    for stage in existing_stages:
        if stage['name'] == full_stage_name:
            return stage['id']
    
    template = STAGES.get(stage_name, {})
    
    if stage_name == 'جامعي' and college_name:
        college_icon = '🎓'
        for c in COLLEGES:
            if c['name'] == college_name:
                college_icon = c['icon']
                break
        icon = college_icon
        description = "كلية: " + college_name
    else:
        icon = template.get('icon', '🎓')
        description = template.get('description', '')
    
    result = create_stage(
        name=full_stage_name,
        description=description,
        icon=icon,
        order=template.get('order', 0)
    )
    
    if result['success']:
        return result['stage_id']
    
    return None


def find_or_create_grade(stage_id, grade_name):
    """يدور على الصف، لو مش موجود يعمله"""
    
    existing_grades = get_grades_by_stage(stage_id)
    for grade in existing_grades:
        if grade['name'] == grade_name:
            return grade['id']
    
    grade_info = {'number': 0, 'icon': '📖'}
    for stage_name, grades_list in GRADES_BY_STAGE.items():
        for g in grades_list:
            if g['name'] == grade_name:
                grade_info = g
                break
    
    result = create_grade(
        stage_id=stage_id,
        name=grade_name,
        grade_number=grade_info.get('number', 0),
        icon=grade_info.get('icon', '📖'),
        order=grade_info.get('number', 0)
    )
    
    if result['success']:
        return result['grade_id']
    
    return None


def find_or_create_subject(grade_id, subject_name, term=None):
    """يدور على المادة، لو مش موجودة يعملها"""
    
    if term and term != 'سنة كاملة':
        full_name = subject_name + " - " + term
    else:
        full_name = subject_name
    
    existing_subjects = get_subjects_by_grade(grade_id)
    for subject in existing_subjects:
        if subject['name'] == full_name:
            return subject['id']
    
    icon = get_subject_icon(subject_name)
    color = get_random_color()
    
    if term:
        description = subject_name + " - " + term
    else:
        description = subject_name
    
    result = create_subject(
        grade_id=grade_id,
        name=full_name,
        description=description,
        icon=icon,
        color=color,
        order=0
    )
    
    if result['success']:
        return result['subject_id']
    
    return None


def smart_upload_book(
    ai_engine,
    stage_name,
    grade_name,
    term,
    subject_name,
    book_title,
    book_content,
    college_name=None,
    auto_generate_outputs=True,
    quiz_gen=None,
    progress_callback=None
):
    """الإضافة الذكية الكاملة للكتاب"""
    
    result = {
        'success': False,
        'stage_id': None,
        'grade_id': None,
        'subject_id': None,
        'chapters_created': 0,
        'lessons_created': 0,
        'outputs_generated': 0,
        'errors': []
    }
    
    try:
        # 1. إنشاء/إيجاد المرحلة
        if progress_callback:
            if stage_name == 'جامعي' and college_name:
                progress_callback(0.05, "🎓 جاري إعداد " + college_name)
            else:
                progress_callback(0.05, "🎓 جاري إعداد المرحلة...")
        
        stage_id = find_or_create_stage(stage_name, college_name)
        if not stage_id:
            result['errors'].append("❌ فشل إعداد المرحلة")
            return result
        result['stage_id'] = stage_id
        
        # 2. إنشاء/إيجاد الصف
        if progress_callback:
            progress_callback(0.1, "📖 جاري إعداد الصف...")
        
        grade_id = find_or_create_grade(stage_id, grade_name)
        if not grade_id:
            result['errors'].append("❌ فشل إعداد الصف: " + grade_name)
            return result
        result['grade_id'] = grade_id
        
        # 3. إنشاء/إيجاد المادة
        if progress_callback:
            progress_callback(0.15, "📚 جاري إعداد المادة...")
        
        subject_id = find_or_create_subject(grade_id, subject_name, term)
        if not subject_id:
            result['errors'].append("❌ فشل إعداد المادة: " + subject_name)
            return result
        result['subject_id'] = subject_id
        
        # 4. تحليل الكتاب
        if progress_callback:
            progress_callback(0.2, "🤖 الذكاء الاصطناعي بيحلل الكتاب...")
        
        analysis = analyze_book_structure(ai_engine, book_content, book_title)
        
        if not analysis['success']:
            error_msg = analysis.get('error', '')
            result['errors'].append("❌ فشل تحليل الكتاب: " + error_msg)
            return result
        
        chapters_data = analysis['data'].get('chapters', [])
        
        if not chapters_data:
            result['errors'].append("❌ مفيش فصول في الكتاب")
            return result
        
        # 5. حفظ الفصول والدروس
        total_chapters = len(chapters_data)
        all_lessons = []
        
        for chap_idx, chapter_data in enumerate(chapters_data):
            chapter_progress = 0.3 + (0.4 * (chap_idx + 1) / total_chapters)
            
            chap_name = chapter_data.get('name', '')[:30]
            chap_num = chap_idx + 1
            msg = "📑 حفظ الفصل " + str(chap_num) + "/" + str(total_chapters) + ": " + chap_name
            
            if progress_callback:
                progress_callback(chapter_progress, msg)
            
            default_chap_name = "الفصل " + str(chap_idx + 1)
            chapter_result = create_chapter(
                subject_id=subject_id,
                name=chapter_data.get('name', default_chap_name),
                description=chapter_data.get('description', ''),
                order=chap_idx
            )
            
            if not chapter_result.get('success'):
                error_chap_name = chapter_data.get('name', '')
                result['errors'].append("❌ فشل حفظ فصل: " + error_chap_name)
                continue
            
            result['chapters_created'] += 1
            chapter_id = chapter_result['chapter_id']
            
            lessons_data = chapter_data.get('lessons', [])
            for less_idx, lesson_data in enumerate(lessons_data):
                default_less_name = "الدرس " + str(less_idx + 1)
                lesson_result = create_lesson(
                    chapter_id=chapter_id,
                    name=lesson_data.get('name', default_less_name),
                    content=lesson_data.get('content', ''),
                    description=lesson_data.get('description', ''),
                    order=less_idx
                )
                
                if lesson_result.get('success'):
                    result['lessons_created'] += 1
                    all_lessons.append({
                        'id': lesson_result['lesson_id'],
                        'name': lesson_data.get('name', ''),
                        'content': lesson_data.get('content', ''),
                        'chapter_id': chapter_id
                    })
                else:
                    error_less_name = lesson_data.get('name', '')
                    result['errors'].append("❌ فشل حفظ درس: " + error_less_name)
        
        # 6. توليد المخرجات
        if auto_generate_outputs and all_lessons and quiz_gen:
            total_lessons = len(all_lessons)
            
            for less_idx, lesson in enumerate(all_lessons):
                gen_progress = 0.7 + (0.3 * (less_idx + 1) / total_lessons)
                
                less_name = lesson['name'][:30]
                less_num = less_idx + 1
                msg = "🚀 توليد مخرجات الدرس " + str(less_num) + "/" + str(total_lessons) + ": " + less_name
                
                if progress_callback:
                    progress_callback(gen_progress, msg)
                
                from modules.library.auto_generator import auto_generate_for_lesson
                
                gen_result = auto_generate_for_lesson(
                    ai_engine=ai_engine,
                    lesson_id=lesson['id'],
                    lesson_content=lesson['content'],
                    quiz_gen=quiz_gen,
                    skip_existing=True
                )
                
                if gen_result['success']:
                    result['outputs_generated'] += len(gen_result['generated'])
        
        if progress_callback:
            progress_callback(1.0, "✅ تم الانتهاء بنجاح!")
        
        result['success'] = True
        return result
    
    except Exception as e:
        result['errors'].append("❌ خطأ غير متوقع: " + str(e))
        return result


def get_book_estimated_time(num_pages, generate_outputs=True):
    """تقدير الوقت المتوقع"""
    
    estimated_lessons = max(5, num_pages // 5)
    analysis_time = 30 + (num_pages * 0.5)
    save_time = estimated_lessons * 2
    
    if generate_outputs:
        generation_time = estimated_lessons * 60
    else:
        generation_time = 0
    
    total_seconds = analysis_time + save_time + generation_time
    
    if total_seconds < 60:
        return str(int(total_seconds)) + " ثانية"
    elif total_seconds < 3600:
        return str(int(total_seconds / 60)) + " دقيقة"
    else:
        hours = int(total_seconds / 3600)
        mins = int((total_seconds % 3600) / 60)
        return str(hours) + " ساعة و " + str(mins) + " دقيقة"