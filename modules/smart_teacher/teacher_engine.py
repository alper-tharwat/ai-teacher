"""
🧠 محرك شرح الأستاذ الذكي - مع كاش عام للمكتبة الذكية
"""

import json
import streamlit as st
from modules.auth.outputs_manager import (
    save_output, 
    get_cached_output,
    save_lesson_output,
    get_lesson_output_cached,
    is_lesson_from_library,
    get_current_lesson_id
)


def prepare_lesson(ai_engine, content: str, style: str = "مبسط", language: str = "العربية") -> dict:
    """
    تحضير الدرس بأسلوب معلم خبير - مع كاش (شخصي أو عام)
    """

    # ============ فحص الكاش ============
    cache_settings = {
        'style': style,
        'language': language
    }
    
    cached_lesson = None
    is_from_library = is_lesson_from_library()
    
    if is_from_library:
        # من المكتبة الذكية - كاش عام
        lesson_id = get_current_lesson_id()
        cached_lesson = get_lesson_output_cached(
            lesson_id=lesson_id,
            output_type='smart_teacher_lesson',
            settings=cache_settings
        )
        
        if cached_lesson:
            return {
                "success": True,
                "data": cached_lesson,
                "from_cache": True,
                "from_library": True
            }
    else:
        # ملف شخصي - كاش شخصي
        current_file_id = st.session_state.get('current_file_id')
        if current_file_id:
            cached_lesson = get_cached_output(
                file_id=current_file_id,
                output_type='smart_teacher_lesson',
                settings=cache_settings
            )
            
            if cached_lesson:
                return {
                    "success": True,
                    "data": cached_lesson,
                    "from_cache": True,
                    "from_library": False
                }

    # ============ توليد جديد ============
    lang_instruction = ""
    if language != "العربية":
        lang_instruction = f"\n🌍 اشرح باللغة: {language}"

    style_instructions = {
        "مبسط": """
🎯 أسلوب الشرح: مبسط جداً
- اشرح كأنك بتتكلم مع طفل عمره 10 سنوات
- استخدم كلمات سهلة ومفهومة
- اربط كل فكرة بحاجة من الحياة اليومية
- استخدم تشبيهات بسيطة وممتعة
""",
        "أكاديمي": """
🎯 أسلوب الشرح: أكاديمي محترف
- استخدم مصطلحات علمية دقيقة مع توضيحها
- اذكر تعريفات واضحة ومحددة
- اشرح بأسلوب منطقي ومنظم
""",
        "ممتع": """
🎯 أسلوب الشرح: ممتع وقصصي
- ابدأ كل نقطة بقصة قصيرة أو موقف شيق
- استخدم تشبيهات مثيرة من الواقع
- استخدم تعجب وحماس في الشرح
""",
        "تفصيلي": """
🎯 أسلوب الشرح: تفصيلي عميق
- اشرح كل جزئية بعمق وتفصيل
- اذكر الأسباب، النتائج، والآثار
- قدم أمثلة متعددة
"""
    }

    style_text = style_instructions.get(style, style_instructions["مبسط"])

    prompt = f"""
أنت معلم خبير ومحترف بخبرة 20 سنة في التدريس.
ستظهر كأستاذ متحرك على شاشة، تشرح للطلاب درساً تفاعلياً.

📚 المحتوى:
{content[:6000]}

المطلوب:
قسّم المحتوى إلى 5-8 نقاط رئيسية، ولكل نقطة:

1. عنوان النقطة (title): قصير وجذاب
2. الشرح الصوتي (explanation): كأنك بتتكلم مع طلاب أمامك
   - استخدم عبارات تفاعلية
   - 100-180 كلمة لكل نقطة
3. نص الصبورة (board_text): مختصر ومنظم بـ HTML بسيط
   - استخدم رموز تعبيرية

{style_text}
{lang_instruction}

أرجع JSON فقط:
{{
    "title": "عنوان الدرس",
    "intro": "مقدمة قصيرة تشويقية",
    "points": [
        {{
            "title": "عنوان النقطة",
            "explanation": "الشرح الصوتي الكامل",
            "board_text": "<h3>📌 عنوان</h3><ul><li>نقطة</li></ul>"
        }}
    ],
    "conclusion": "خاتمة تلخص أهم النقاط"
}}

مهم: أرجع JSON صالح فقط بدون أي نص إضافي.
"""

    try:
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
        
        # ============ حفظ في الكاش ============
        if is_from_library:
            lesson_id = get_current_lesson_id()
            save_lesson_output(
                lesson_id=lesson_id,
                output_type='smart_teacher_lesson',
                content=result,
                settings=cache_settings
            )
        else:
            current_file_id = st.session_state.get('current_file_id')
            if current_file_id:
                save_output(
                    file_id=current_file_id,
                    output_type='smart_teacher_lesson',
                    content=result,
                    settings=cache_settings
                )
        
        return {
            "success": True,
            "data": result,
            "from_cache": False,
            "from_library": is_from_library
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"خطأ: {str(e)}",
            "raw_response": response if 'response' in dir() else ""
        }


def answer_student_question(ai_engine, lesson_content: str, question: str, language: str = "العربية") -> dict:
    """
    الأستاذ يجاوب على سؤال الطالب
    """

    prompt = f"""
أنت معلم خبير ومحبوب من طلابك، وطالب سأل سؤال أثناء الدرس.

📚 محتوى الدرس:
{lesson_content[:4000]}

❓ سؤال الطالب:
{question}

جاوب بأسلوب معلم محترف:

1. الشرح الصوتي (answer_voice):
   - ابدأ بتشجيع للطالب
   - اشرح بمثال واضح
   - 100-150 كلمة

2. نص الصبورة (answer_board):
   - مختصر ومنظم بـ HTML
   - 4-7 سطور

{"اكتب بالعربية" if language == "العربية" else f"اكتب باللغة: {language}"}

أرجع JSON فقط:
{{
    "answer_voice": "الشرح الصوتي",
    "answer_board": "<h3>💡 الإجابة</h3><ul><li>نقطة</li></ul>"
}}
"""

    try:
        response = ai_engine.answer_question(context="", question=prompt)

        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                result = json.loads(response[start:end])
            else:
                raise

        return {"success": True, "data": result}

    except Exception as e:
        return {
            "success": False,
            "data": {
                "answer_voice": response if 'response' in dir() else "حدث خطأ",
                "answer_board": "<p>حدث خطأ في الإجابة</p>"
            },
            "error": str(e)
        }