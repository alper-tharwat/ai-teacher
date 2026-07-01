"""
📝 مولد الامتحانات الذكي
بيعمل 5 أنواع امتحانات مختلفة + تصحيح تلقائي ذكي
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import re
from config import Config


class QuizGenerator:
    """
    مولد امتحانات احترافي
    
    الأنواع المدعومة:
    1. اختيار من متعدد (MCQ)
    2. صح وغلط (True/False)
    3. أكمل الفراغ (Fill in the blank)
    4. أسئلة مقالية (Open questions)
    5. توصيل (Matching)
    
    المميزات:
    - تصحيح تلقائي ذكي
    - شرح كل إجابة
    - مستويات صعوبة
    - تقييم الأداء
    - اقتراحات للتحسين
    """
    
    def __init__(self, ai_engine):
        """
        Args:
            ai_engine: كائن من AIEngine
        """
        self.ai = ai_engine
    
    # ============================================
    # 1️⃣ اختيار من متعدد
    # ============================================
    
    def generate_mcq(self, text, num_questions=5, difficulty="medium"):
        """
        إنشاء أسئلة اختيار من متعدد
        
        Args:
            text: المحتوى
            num_questions: عدد الأسئلة (3-20)
            difficulty: easy / medium / hard
        
        Returns:
            dict: {
                'success': True/False,
                'type': 'mcq',
                'questions': [...],
                'total': عدد الأسئلة
            }
        """
        difficulty_map = {
            "easy": "سهلة - أسئلة مباشرة من النص",
            "medium": "متوسطة - أسئلة تحتاج فهم",
            "hard": "صعبة - أسئلة تحليلية واستنتاجية"
        }
        
        prompt = f"""
        أنت معلم محترف بتعمل امتحان. اقرأ المحتوى ده كويس وعمل {num_questions} أسئلة اختيار من متعدد.
        
        مستوى الصعوبة: {difficulty_map.get(difficulty, difficulty_map['medium'])}
        
        المحتوى:
        ─────────────────────
        {text[:Config.MAX_INPUT_LENGTH]}
        ─────────────────────
        
        قواعد مهمة:
        1. كل سؤال له 4 اختيارات
        2. اختيار واحد بس صح
        3. الاختيارات الغلط تبقى منطقية مش غبية
        4. السؤال يكون واضح ومفهوم
        5. الشرح يبقى بالعامية المصرية
        6. اختلط بين الأسئلة المباشرة والتحليلية
        
        ⚠️ مهم جداً: رد بـ JSON بس بدون أي كلام تاني، بالشكل ده بالظبط:
        
        {{
            "questions": [
                {{
                    "id": 1,
                    "question": "نص السؤال؟",
                    "options": [
                        "الاختيار الأول",
                        "الاختيار الثاني",
                        "الاختيار الثالث",
                        "الاختيار الرابع"
                    ],
                    "correct_index": 0,
                    "explanation": "شرح ليه الإجابة دي صح بالعامية المصرية",
                    "difficulty": "easy",
                    "topic": "الموضوع اللي السؤال عليه"
                }}
            ]
        }}
        """
        
        response = self.ai._ask(prompt)
        result = self._parse_json(response)
        
        if result and 'questions' in result:
            return {
                'success': True,
                'type': 'mcq',
                'questions': result['questions'],
                'total': len(result['questions'])
            }
        else:
            return {
                'success': False,
                'error': 'مقدرتش أعمل الامتحان، جرب تاني',
                'raw': response[:500]
            }
    
    # ============================================
    # 2️⃣ صح وغلط
    # ============================================
    
    def generate_true_false(self, text, num_questions=5):
        """
        إنشاء أسئلة صح وغلط
        """
        prompt = f"""
        اقرأ المحتوى ده وعمل {num_questions} أسئلة صح وغلط.
        
        المحتوى:
        ─────────────────────
        {text[:Config.MAX_INPUT_LENGTH]}
        ─────────────────────
        
        قواعد:
        1. خلط بين أسئلة صح وأسئلة غلط (نسبة 50/50)
        2. الأسئلة الغلط تكون فيها تعديل بسيط من النص الأصلي
        3. الشرح يوضح ليه صح أو غلط
        4. الشرح بالعامية المصرية
        
        ⚠️ رد بـ JSON بس:
        
        {{
            "questions": [
                {{
                    "id": 1,
                    "statement": "الجملة المطلوب الحكم عليها",
                    "is_true": true,
                    "explanation": "شرح بالعامية المصرية",
                    "correct_version": "النسخة الصحيحة لو الجملة غلط"
                }}
            ]
        }}
        """
        
        response = self.ai._ask(prompt)
        result = self._parse_json(response)
        
        if result and 'questions' in result:
            return {
                'success': True,
                'type': 'true_false',
                'questions': result['questions'],
                'total': len(result['questions'])
            }
        else:
            return {
                'success': False,
                'error': 'مقدرتش أعمل الامتحان',
                'raw': response[:500]
            }
    
    # ============================================
    # 3️⃣ أكمل الفراغ
    # ============================================
    
    def generate_fill_blank(self, text, num_questions=5):
        """
        إنشاء أسئلة أكمل الفراغ
        """
        prompt = f"""
        اقرأ المحتوى ده وعمل {num_questions} أسئلة أكمل الفراغ.
        
        المحتوى:
        ─────────────────────
        {text[:Config.MAX_INPUT_LENGTH]}
        ─────────────────────
        
        قواعد:
        1. اختار كلمات أو مفاهيم مهمة وحطها فراغ
        2. الفراغ يبقى واحد بس في كل سؤال (للسهولة)
        3. ادي تلميح بسيط لو السؤال صعب
        4. حط البدائل المحتملة لو الإجابة ممكن تتقال بأكثر من طريقة
        
        ⚠️ رد بـ JSON بس:
        
        {{
            "questions": [
                {{
                    "id": 1,
                    "sentence": "الجملة فيها ___ في مكان الفراغ",
                    "correct_answer": "الكلمة الصحيحة",
                    "alternatives": ["بديل 1", "بديل 2"],
                    "hint": "تلميح بسيط",
                    "explanation": "شرح ليه دي الإجابة"
                }}
            ]
        }}
        """
        
        response = self.ai._ask(prompt)
        result = self._parse_json(response)
        
        if result and 'questions' in result:
            return {
                'success': True,
                'type': 'fill_blank',
                'questions': result['questions'],
                'total': len(result['questions'])
            }
        else:
            return {
                'success': False,
                'error': 'مقدرتش أعمل الامتحان',
                'raw': response[:500]
            }
    
    # ============================================
    # 4️⃣ أسئلة مقالية
    # ============================================
    
    def generate_open_questions(self, text, num_questions=3, difficulty="medium"):
        """
        إنشاء أسئلة مقالية
        """
        difficulty_map = {
            "easy": "أسئلة مباشرة بإجابات قصيرة (2-3 أسطر)",
            "medium": "أسئلة متوسطة بإجابات متوسطة (5-7 أسطر)",
            "hard": "أسئلة تحليلية بإجابات طويلة (10+ أسطر)"
        }
        
        prompt = f"""
        اقرأ المحتوى ده وعمل {num_questions} أسئلة مقالية.
        
        المستوى: {difficulty_map.get(difficulty, difficulty_map['medium'])}
        
        المحتوى:
        ─────────────────────
        {text[:Config.MAX_INPUT_LENGTH]}
        ─────────────────────
        
        قواعد:
        1. الأسئلة تكون متنوعة (اشرح، قارن، حلل، ناقش)
        2. ادي النقاط الرئيسية المطلوبة في الإجابة
        3. ادي إجابة نموذجية مفصلة
        4. حدد الدرجة لكل نقطة
        
        ⚠️ رد بـ JSON بس:
        
        {{
            "questions": [
                {{
                    "id": 1,
                    "question": "السؤال المقالي؟",
                    "question_type": "اشرح/قارن/حلل/ناقش",
                    "key_points": [
                        {{"point": "النقطة 1", "marks": 3}},
                        {{"point": "النقطة 2", "marks": 3}},
                        {{"point": "النقطة 3", "marks": 4}}
                    ],
                    "model_answer": "الإجابة النموذجية الكاملة",
                    "total_marks": 10,
                    "tips": "نصائح للإجابة"
                }}
            ]
        }}
        """
        
        response = self.ai._ask(prompt)
        result = self._parse_json(response)
        
        if result and 'questions' in result:
            return {
                'success': True,
                'type': 'open',
                'questions': result['questions'],
                'total': len(result['questions'])
            }
        else:
            return {
                'success': False,
                'error': 'مقدرتش أعمل الامتحان',
                'raw': response[:500]
            }
    
    # ============================================
    # 5️⃣ توصيل
    # ============================================
    
    def generate_matching(self, text, num_pairs=5):
        """
        إنشاء أسئلة توصيل
        """
        prompt = f"""
        اقرأ المحتوى ده وعمل سؤال توصيل بـ {num_pairs} أزواج.
        
        المحتوى:
        ─────────────────────
        {text[:Config.MAX_INPUT_LENGTH]}
        ─────────────────────
        
        قواعد:
        1. العمود (أ) فيه مصطلحات أو مفاهيم
        2. العمود (ب) فيه التعريفات أو الشرح
        3. الأزواج تكون واضحة ومتميزة
        
        ⚠️ رد بـ JSON بس:
        
        {{
            "instructions": "وصّل من العمود (أ) إلى العمود (ب)",
            "column_a": [
                {{"id": 1, "text": "المصطلح الأول"}},
                {{"id": 2, "text": "المصطلح الثاني"}}
            ],
            "column_b": [
                {{"id": "أ", "text": "التعريف الأول"}},
                {{"id": "ب", "text": "التعريف الثاني"}}
            ],
            "correct_matches": [
                {{"a_id": 1, "b_id": "أ", "explanation": "ليه دول مع بعض"}},
                {{"a_id": 2, "b_id": "ب", "explanation": "ليه دول مع بعض"}}
            ]
        }}
        """
        
        response = self.ai._ask(prompt)
        result = self._parse_json(response)
        
        if result and 'correct_matches' in result:
            return {
                'success': True,
                'type': 'matching',
                'data': result,
                'total': len(result.get('correct_matches', []))
            }
        else:
            return {
                'success': False,
                'error': 'مقدرتش أعمل الامتحان',
                'raw': response[:500]
            }
    
    # ============================================
    # 🎯 تصحيح الإجابات
    # ============================================
    
    def grade_mcq(self, question, user_answer_index):
        """
        تصحيح سؤال اختيار من متعدد
        
        Args:
            question: dict السؤال
            user_answer_index: index الإجابة اللي اختارها المستخدم
        
        Returns:
            dict: نتيجة التصحيح
        """
        correct_index = question.get('correct_index', 0)
        is_correct = user_answer_index == correct_index
        
        return {
            'is_correct': is_correct,
            'correct_answer': question['options'][correct_index],
            'user_answer': question['options'][user_answer_index] if user_answer_index < len(question['options']) else "لم يجب",
            'explanation': question.get('explanation', ''),
            'score': 1 if is_correct else 0
        }
    
    def grade_true_false(self, question, user_answer):
        """
        تصحيح سؤال صح وغلط
        
        Args:
            question: dict السؤال
            user_answer: bool إجابة المستخدم
        """
        is_correct = user_answer == question.get('is_true', True)
        
        return {
            'is_correct': is_correct,
            'correct_answer': 'صح ✅' if question['is_true'] else 'غلط ❌',
            'user_answer': 'صح ✅' if user_answer else 'غلط ❌',
            'explanation': question.get('explanation', ''),
            'correct_version': question.get('correct_version', ''),
            'score': 1 if is_correct else 0
        }
    
    def grade_fill_blank(self, question, user_answer):
        """
        تصحيح سؤال أكمل الفراغ
        """
        user_clean = user_answer.strip().lower()
        correct = question.get('correct_answer', '').strip().lower()
        alternatives = [alt.strip().lower() for alt in question.get('alternatives', [])]
        
        is_correct = user_clean == correct or user_clean in alternatives
        
        # تصحيح ذكي - لو الإجابة قريبة
        if not is_correct and user_clean:
            similarity = self._calculate_similarity(user_clean, correct)
            if similarity > 0.8:
                is_correct = True
        
        return {
            'is_correct': is_correct,
            'correct_answer': question['correct_answer'],
            'user_answer': user_answer,
            'explanation': question.get('explanation', ''),
            'score': 1 if is_correct else 0
        }
    
    def grade_open_question(self, question, user_answer):
        """
        تصحيح سؤال مقالي باستخدام AI
        
        Args:
            question: dict السؤال
            user_answer: str إجابة المستخدم
        
        Returns:
            dict: تصحيح مفصل
        """
        prompt = f"""
        أنت مصحح امتحانات محترف. صحح إجابة الطالب بدقة وعدالة.
        
        السؤال: {question.get('question', '')}
        
        النقاط المطلوبة في الإجابة:
        {json.dumps(question.get('key_points', []), ensure_ascii=False, indent=2)}
        
        الإجابة النموذجية:
        {question.get('model_answer', '')}
        
        إجابة الطالب:
        ─────────────────────
        {user_answer}
        ─────────────────────
        
        صحح الإجابة وارجع JSON بالشكل ده:
        
        {{
            "score": 8,
            "max_score": 10,
            "percentage": 80,
            "grade": "ممتاز/جيد جداً/جيد/مقبول/ضعيف",
            "feedback": "تعليق عام بالعامية المصرية",
            "correct_points": ["النقاط الصحيحة اللي ذكرها"],
            "missing_points": ["النقاط الناقصة"],
            "wrong_points": ["النقاط الغلط لو موجودة"],
            "suggestions": "اقتراحات للتحسين",
            "strengths": "نقاط القوة في الإجابة"
        }}
        """
        
        response = self.ai._ask(prompt)
        result = self._parse_json(response)
        
        if result:
            return {
                'success': True,
                'is_correct': result.get('percentage', 0) >= 60,
                **result
            }
        else:
            return {
                'success': False,
                'error': 'مقدرتش أصحح الإجابة'
            }
    
    def grade_matching(self, quiz_data, user_matches):
        """
        تصحيح سؤال التوصيل
        
        Args:
            quiz_data: dict بيانات السؤال
            user_matches: dict {a_id: b_id} توصيلات المستخدم
        """
        correct_matches = quiz_data.get('correct_matches', [])
        correct_dict = {m['a_id']: m['b_id'] for m in correct_matches}
        
        results = []
        score = 0
        
        for match in correct_matches:
            a_id = match['a_id']
            correct_b = match['b_id']
            user_b = user_matches.get(a_id)
            is_correct = user_b == correct_b
            
            if is_correct:
                score += 1
            
            results.append({
                'a_id': a_id,
                'correct_b': correct_b,
                'user_b': user_b,
                'is_correct': is_correct,
                'explanation': match.get('explanation', '')
            })
        
        total = len(correct_matches)
        percentage = (score / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'correct': score,
            'percentage': percentage,
            'results': results
        }
    
    # ============================================
    # 📊 تقييم الأداء الكلي
    # ============================================
    
    def evaluate_performance(self, results):
        """
        تقييم أداء الطالب بشكل كامل
        
        Args:
            results: list نتائج كل الأسئلة
        
        Returns:
            dict: تقييم شامل
        """
        if not results:
            return {'error': 'مفيش نتائج للتقييم'}
        
        total = len(results)
        correct = sum(1 for r in results if r.get('is_correct', False))
        percentage = (correct / total * 100)
        
        # تحديد التقدير
        if percentage >= 90:
            grade = "🏆 ممتاز - أنت أسطورة!"
            emoji = "🎉"
            message = "أداء استثنائي! إنت فاهم المحتوى ده فهم عميق جداً"
        elif percentage >= 80:
            grade = "⭐ جيد جداً"
            emoji = "😊"
            message = "أداء رائع! شوية مذاكرة كمان وهتبقى نمبر وان"
        elif percentage >= 70:
            grade = "👍 جيد"
            emoji = "🙂"
            message = "أداء كويس بس محتاج تركيز أكتر في بعض النقاط"
        elif percentage >= 60:
            grade = "📚 مقبول"
            emoji = "😐"
            message = "أداء مقبول، محتاج تراجع أكتر على المحتوى"
        else:
            grade = "💪 محتاج تذاكر أكتر"
            emoji = "😔"
            message = "متزعلش! المذاكرة محتاجة وقت. ركز وأعد تاني"
        
        return {
            'total_questions': total,
            'correct_answers': correct,
            'wrong_answers': total - correct,
            'percentage': round(percentage, 1),
            'grade': grade,
            'emoji': emoji,
            'message': message,
            'stars': self._get_stars(percentage)
        }
    
    # ============================================
    # 🔧 أدوات مساعدة
    # ============================================
    
    def _parse_json(self, response):
        """استخراج JSON من رد الـ AI"""
        if not response:
            return None
        
        try:
            # تنظيف الرد
            response = response.strip()
            
            # إزالة code blocks
            response = re.sub(r'```json\s*', '', response)
            response = re.sub(r'```\s*', '', response)
            
            # البحث عن JSON
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            
            return None
            
        except json.JSONDecodeError as e:
            print(f"JSON Error: {e}")
            return None
        except Exception as e:
            print(f"Parse Error: {e}")
            return None
    
    def _calculate_similarity(self, str1, str2):
        """حساب التشابه بين نصين (للتصحيح المرن)"""
        if not str1 or not str2:
            return 0
        
        # تطبيع
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()
        
        if str1 == str2:
            return 1.0
        
        # خوارزمية بسيطة
        longer = max(len(str1), len(str2))
        if longer == 0:
            return 1.0
        
        # عدد الحروف المشتركة
        common = sum(1 for c in str1 if c in str2)
        return common / longer
    
    def _get_stars(self, percentage):
        """تحويل النسبة لنجوم"""
        if percentage >= 90:
            return "⭐⭐⭐⭐⭐"
        elif percentage >= 75:
            return "⭐⭐⭐⭐"
        elif percentage >= 60:
            return "⭐⭐⭐"
        elif percentage >= 40:
            return "⭐⭐"
        else:
            return "⭐"