"""
🚀 محرك التوليد التلقائي للمخرجات
يولّد كل المخرجات لدرس واحد أو لكل الدروس في فصل
"""

import json
import streamlit as st
from modules.auth.outputs_manager import save_lesson_output, get_lesson_output_cached


# الإعدادات الافتراضية للمخرجات
DEFAULT_OUTPUTS_CONFIG = {
    'summary': {
        'enabled': True,
        'settings': {'style': 'smart'},
        'name': '📝 الملخص الذكي'
    },
    'explanation': {
        'enabled': True,
        'settings': {'level': 'beginner'},
        'name': '💡 الشرح المبسط'
    },
    'quiz': {
        'enabled': True,
        'settings': {
            'type': 'mcq',
            'num_questions': 5,
            'difficulty': 'medium'
        },
        'name': '📋 الامتحان'
    },
    'flashcards': {
        'enabled': True,
        'settings': {
            'num_cards': 10,
            'card_type': 'qa',
            'difficulty': 'medium'
        },
        'name': '🎴 بطاقات الحفظ'
    },
    'mindmap': {
        'enabled': True,
        'settings': {
            'depth_level': 'medium',
            'style': 'colorful'
        },
        'name': '🧠 الخريطة الذهنية'
    }
}


def check_existing_outputs(lesson_id: str) -> dict:
    """
    فحص المخرجات الموجودة بالفعل لدرس
    
    Returns:
        dict: {output_type: True if exists}
    """
    existing = {}
    
    for output_type in DEFAULT_OUTPUTS_CONFIG.keys():
        config = DEFAULT_OUTPUTS_CONFIG[output_type]
        cached = get_lesson_output_cached(
            lesson_id=lesson_id,
            output_type=output_type,
            settings=config['settings']
        )
        existing[output_type] = cached is not None
    
    return existing


def generate_single_output(ai_engine, lesson_content: str, output_type: str, 
                          settings: dict, quiz_gen=None) -> dict:
    """
    توليد مخرج واحد
    
    Returns:
        {success: bool, content: any, error: str}
    """
    try:
        if output_type == 'summary':
            result = ai_engine.summarize(lesson_content, style=settings.get('style', 'smart'))
            return {
                'success': bool(result and result.strip()),
                'content': result,
                'error': None
            }
        
        elif output_type == 'explanation':
            result = ai_engine.explain(lesson_content, level=settings.get('level', 'beginner'))
            return {
                'success': bool(result and result.strip()),
                'content': result,
                'error': None
            }
        
        elif output_type == 'quiz':
            if not quiz_gen:
                return {'success': False, 'error': 'Quiz Generator not provided'}
            
            qt = settings.get('type', 'mcq')
            num = settings.get('num_questions', 5)
            diff = settings.get('difficulty', 'medium')
            
            if qt == 'mcq':
                result = quiz_gen.generate_mcq(lesson_content, num_questions=num, difficulty=diff)
            elif qt == 'true_false':
                result = quiz_gen.generate_true_false(lesson_content, num_questions=num)
            elif qt == 'fill_blank':
                result = quiz_gen.generate_fill_blank(lesson_content, num_questions=num)
            else:
                result = quiz_gen.generate_open_questions(lesson_content, num_questions=num, difficulty=diff)
            
            if result and result.get('success'):
                return {
                    'success': True,
                    'content': result,
                    'error': None
                }
            return {'success': False, 'error': 'Failed to generate quiz'}
        
        elif output_type == 'flashcards':
            try:
                from utils.flashcard_generator import FlashcardGenerator
                fc_gen = FlashcardGenerator(ai_engine)
                
                result = fc_gen.generate(
                    text=lesson_content,
                    num_cards=settings.get('num_cards', 10),
                    card_type=settings.get('card_type', 'qa'),
                    difficulty=settings.get('difficulty', 'medium')
                )
                
                if result['success']:
                    return {
                        'success': True,
                        'content': {'cards': result['cards'], 'total': result['total']},
                        'error': None
                    }
                return {'success': False, 'error': result.get('error', 'Failed')}
            except Exception as e:
                return {'success': False, 'error': str(e)}
        
        elif output_type == 'mindmap':
            try:
                from utils.mindmap_generator import MindMapGenerator
                mm_gen = MindMapGenerator(ai_engine)
                
                result = mm_gen.generate(
                    text=lesson_content,
                    depth_level=settings.get('depth_level', 'medium'),
                    style=settings.get('style', 'colorful')
                )
                
                if result['success']:
                    return {
                        'success': True,
                        'content': {
                            'data': result['data'],
                            'markdown': result['markdown']
                        },
                        'error': None
                    }
                return {'success': False, 'error': result.get('error', 'Failed')}
            except Exception as e:
                return {'success': False, 'error': str(e)}
        
        return {'success': False, 'error': f'Unknown output type: {output_type}'}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def auto_generate_for_lesson(ai_engine, lesson_id: str, lesson_content: str, 
                            outputs_config: dict = None, quiz_gen=None,
                            skip_existing: bool = True) -> dict:
    """
    توليد كل المخرجات المفعّلة لدرس واحد
    
    Args:
        ai_engine: محرك AI
        lesson_id: معرف الدرس
        lesson_content: محتوى الدرس
        outputs_config: إعدادات المخرجات
        quiz_gen: مولد الامتحانات
        skip_existing: تخطي المخرجات الموجودة
    
    Returns:
        {
            'success': bool,
            'generated': [...],
            'skipped': [...],
            'failed': [...],
            'total_tokens_saved': int
        }
    """
    if not outputs_config:
        outputs_config = DEFAULT_OUTPUTS_CONFIG
    
    result = {
        'success': True,
        'generated': [],
        'skipped': [],
        'failed': [],
        'total': 0
    }
    
    # فحص الموجود
    existing = check_existing_outputs(lesson_id) if skip_existing else {}
    
    # توليد كل مخرج
    for output_type, config in outputs_config.items():
        if not config.get('enabled', True):
            continue
        
        result['total'] += 1
        
        # تخطي لو موجود
        if skip_existing and existing.get(output_type):
            result['skipped'].append({
                'type': output_type,
                'name': config['name']
            })
            continue
        
        # توليد جديد
        gen_result = generate_single_output(
            ai_engine=ai_engine,
            lesson_content=lesson_content,
            output_type=output_type,
            settings=config['settings'],
            quiz_gen=quiz_gen
        )
        
        if gen_result['success']:
            # حفظ في الكاش العام
            save_result = save_lesson_output(
                lesson_id=lesson_id,
                output_type=output_type,
                content=gen_result['content'],
                settings=config['settings']
            )
            
            if save_result.get('success'):
                result['generated'].append({
                    'type': output_type,
                    'name': config['name']
                })
            else:
                result['failed'].append({
                    'type': output_type,
                    'name': config['name'],
                    'error': save_result.get('message', 'Save failed')
                })
        else:
            result['failed'].append({
                'type': output_type,
                'name': config['name'],
                'error': gen_result.get('error', 'Unknown')
            })
    
    result['success'] = len(result['generated']) > 0 or len(result['skipped']) > 0
    
    return result


def auto_generate_for_chapter(ai_engine, chapter_id: str, lessons: list,
                             outputs_config: dict = None, quiz_gen=None,
                             skip_existing: bool = True,
                             progress_callback=None) -> dict:
    """
    توليد كل المخرجات لكل الدروس في فصل
    
    Args:
        ai_engine: محرك AI
        chapter_id: معرف الفصل
        lessons: قائمة الدروس
        outputs_config: إعدادات المخرجات
        quiz_gen: مولد الامتحانات
        skip_existing: تخطي الموجود
        progress_callback: دالة لتحديث الـ progress bar
    
    Returns:
        تقرير شامل عن العملية
    """
    total_lessons = len(lessons)
    
    result = {
        'success': True,
        'total_lessons': total_lessons,
        'completed_lessons': 0,
        'failed_lessons': 0,
        'total_generated': 0,
        'total_skipped': 0,
        'total_failed': 0,
        'lessons_results': []
    }
    
    for idx, lesson in enumerate(lessons):
        lesson_id = lesson.get('id')
        lesson_name = lesson.get('name', 'بدون اسم')
        lesson_content = lesson.get('content', '')
        
        if not lesson_content:
            result['failed_lessons'] += 1
            continue
        
        # تحديث الـ progress
        if progress_callback:
            progress = (idx + 1) / total_lessons
            progress_callback(progress, f"⏳ توليد لـ: {lesson_name}")
        
        # توليد المخرجات
        lesson_result = auto_generate_for_lesson(
            ai_engine=ai_engine,
            lesson_id=lesson_id,
            lesson_content=lesson_content,
            outputs_config=outputs_config,
            quiz_gen=quiz_gen,
            skip_existing=skip_existing
        )
        
        result['lessons_results'].append({
            'lesson_name': lesson_name,
            'lesson_id': lesson_id,
            'result': lesson_result
        })
        
        if lesson_result['success']:
            result['completed_lessons'] += 1
            result['total_generated'] += len(lesson_result['generated'])
            result['total_skipped'] += len(lesson_result['skipped'])
            result['total_failed'] += len(lesson_result['failed'])
        else:
            result['failed_lessons'] += 1
    
    return result