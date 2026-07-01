"""
🤖 محلل الكتب الذكي - يقسم الكتاب لفصول ودروس تلقائياً
"""

import json
import streamlit as st


def analyze_book_structure(ai_engine, book_text: str, book_title: str = "") -> dict:
    """
    تحليل الكتاب وتقسيمه لفصول ودروس
    
    Args:
        ai_engine: محرك الـ AI
        book_text: نص الكتاب الكامل
        book_title: عنوان الكتاب (اختياري)
    
    Returns:
        dict: {
            "success": bool,
            "data": {
                "book_title": "...",
                "chapters": [
                    {
                        "name": "...",
                        "description": "...",
                        "lessons": [...]
                    }
                ]
            }
        }
    """
    
    # تقسيم النص لو طويل جداً
    max_chars = 30000  # حد أقصى للنص
    text_for_analysis = book_text[:max_chars]
    
    title_hint = f"\nعنوان الكتاب: {book_title}" if book_title else ""
    
    prompt = f"""
أنت خبير محترف في تحليل وتنظيم المحتوى التعليمي.

عندك كتاب مدرسي وعايزك تحلله وتقسمه بشكل احترافي.
{title_hint}

═══════════════════════════════════════
📚 محتوى الكتاب:
═══════════════════════════════════════
{text_for_analysis}

═══════════════════════════════════════
🎯 المطلوب منك:
═══════════════════════════════════════

1. **اكتشف عدد الفصول والدروس**
2. **استخرج عنوان كل فصل وعنوان كل درس**
3. **اقسم المحتوى بشكل منطقي**
4. **اكتب وصف مختصر لكل فصل ودرس**
5. **محتوى كل درس لازم يكون كامل ومفيد**

📋 قواعد مهمة:
- لو الكتاب فيه فهرس، استخدمه
- لو الكتاب فيه أرقام للفصول/الدروس، استخدمها
- العناوين تكون واضحة ومنظمة
- المحتوى مقسّم بشكل صحيح (مش مقطوع في النص)
- كل درس يحتوي على معلومات كاملة عن موضوعه

🔧 صيغة الإخراج (JSON فقط):

{{
    "book_title": "عنوان الكتاب",
    "book_description": "وصف مختصر للكتاب (2-3 جمل)",
    "total_chapters": عدد الفصول,
    "total_lessons": عدد الدروس الإجمالي,
    "chapters": [
        {{
            "name": "الفصل الأول: العنوان",
            "description": "وصف مختصر للفصل (جملة أو جملتين)",
            "order": 1,
            "lessons": [
                {{
                    "name": "الدرس 1: العنوان",
                    "description": "وصف مختصر (جملة)",
                    "content": "المحتوى الكامل للدرس - مهم جداً يكون كامل ومفيد",
                    "order": 1
                }}
            ]
        }}
    ]
}}

⚠️ تعليمات صارمة:
- أرجع JSON صالح فقط
- بدون أي نص قبل أو بعد JSON
- بدون markdown code blocks
- المحتوى (content) لازم يكون نص كامل ومفيد
- العناوين واضحة ومرتبة
- لو محصلش تحدد فصول/دروس، اعتبر الكتاب كله "فصل واحد" فيه "دروس متعددة"
"""

    try:
        with st.spinner("🤖 الذكاء الاصطناعي بيحلل الكتاب..."):
            response = ai_engine.answer_question(context="", question=prompt)
        
        # تنظيف الرد
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        # محاولة استخراج JSON
        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                result = json.loads(response[start:end])
            else:
                raise
        
        # التحقق من البيانات
        if not result.get("chapters"):
            return {
                "success": False,
                "error": "❌ AI ما قدرش يقسم الكتاب لفصول",
                "raw_response": response[:500]
            }
        
        # إضافة meta data
        total_lessons = sum(len(c.get("lessons", [])) for c in result.get("chapters", []))
        result["total_chapters"] = len(result.get("chapters", []))
        result["total_lessons"] = total_lessons
        
        return {
            "success": True,
            "data": result
        }
    
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"❌ مشكلة في تحليل رد الـ AI: {str(e)}",
            "raw_response": response[:500] if 'response' in dir() else ""
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"❌ خطأ: {str(e)}"
        }


def regenerate_lesson_content(ai_engine, lesson_name: str, original_text: str) -> str:
    """
    إعادة توليد محتوى درس معين (لو الأدمن مش راضي عنه)
    """
    
    prompt = f"""
عندك درس عنوانه: {lesson_name}

والمحتوى الأصلي:
{original_text[:5000]}

المطلوب:
أعد كتابة محتوى الدرس ده بشكل أحسن:
- منظم وواضح
- يحتوي على كل المعلومات المهمة
- مناسب للطلاب
- مكتوب بلغة سهلة

أرجع المحتوى الجديد بس (بدون أي تعليقات).
"""
    
    try:
        response = ai_engine.answer_question(context="", question=prompt)
        return response.strip()
    except Exception as e:
        return original_text


def generate_lesson_outputs_bulk(ai_engine, lessons: list, output_types: list = None) -> dict:
    """
    توليد المخرجات لكل الدروس دفعة واحدة
    
    Args:
        ai_engine: محرك الـ AI
        lessons: قائمة الدروس
        output_types: أنواع المخرجات (summary, quiz, etc)
    
    Returns:
        dict: {lesson_id: {output_type: content}}
    """
    
    if not output_types:
        output_types = ['summary', 'quiz', 'flashcards']
    
    results = {}
    total = len(lessons) * len(output_types)
    progress_bar = st.progress(0)
    status = st.empty()
    current = 0
    
    for lesson in lessons:
        lesson_id = lesson.get('id') or lesson.get('name')
        results[lesson_id] = {}
        
        for output_type in output_types:
            current += 1
            progress = current / total
            progress_bar.progress(progress, text=f"⏳ توليد {output_type} لـ: {lesson.get('name', '')[:30]}")
            
            try:
                content = lesson.get('content', '')
                if not content:
                    continue
                
                if output_type == 'summary':
                    result = generate_summary(ai_engine, content)
                elif output_type == 'quiz':
                    result = generate_quiz(ai_engine, content)
                elif output_type == 'flashcards':
                    result = generate_flashcards(ai_engine, content)
                else:
                    result = None
                
                if result:
                    results[lesson_id][output_type] = result
            
            except Exception as e:
                print(f"خطأ في توليد {output_type}: {e}")
    
    progress_bar.empty()
    status.empty()
    
    return results


def generate_summary(ai_engine, content: str) -> str:
    """توليد ملخص"""
    prompt = f"""
لخّص الدرس التالي بشكل واضح ومنظم:

{content[:5000]}

أرجع الملخص بالعربية في 5-10 نقاط رئيسية.
"""
    try:
        return ai_engine.answer_question(context="", question=prompt)
    except:
        return ""


def generate_quiz(ai_engine, content: str) -> dict:
    """توليد امتحان"""
    prompt = f"""
عندك درس ده:
{content[:5000]}

ولّد 5 أسئلة اختيار من متعدد (MCQ).

أرجع JSON بالشكل:
{{
    "questions": [
        {{
            "question": "السؤال",
            "options": ["خيار1", "خيار2", "خيار3", "خيار4"],
            "correct_answer": 0,
            "explanation": "شرح الإجابة"
        }}
    ]
}}
"""
    try:
        response = ai_engine.answer_question(context="", question=prompt)
        response = response.strip().replace('```json', '').replace('```', '')
        return json.loads(response)
    except:
        return {}


def generate_flashcards(ai_engine, content: str) -> list:
    """توليد بطاقات حفظ"""
    prompt = f"""
عندك درس ده:
{content[:5000]}

ولّد 10 بطاقات حفظ (سؤال + جواب).

أرجع JSON بالشكل:
{{
    "cards": [
        {{"question": "السؤال", "answer": "الإجابة"}}
    ]
}}
"""
    try:
        response = ai_engine.answer_question(context="", question=prompt)
        response = response.strip().replace('```json', '').replace('```', '')
        result = json.loads(response)
        return result.get('cards', [])
    except:
        return []