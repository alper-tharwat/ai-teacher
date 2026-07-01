"""
🎴 Flashcard Generator - مولّد بطاقات الحفظ
يولّد بطاقات سؤال/إجابة من أي محتوى
"""
import json
import re
from typing import List, Dict, Any


class FlashcardGenerator:
    """
    مولّد بطاقات الحفظ الذكي
    يستخدم AI لتوليد بطاقات سؤال/إجابة
    """

    # أنواع البطاقات
    CARD_TYPES = {
        "definition": {
            "name": "📖 تعريفات",
            "description": "سؤال عن تعريف مصطلح أو مفهوم",
            "icon": "📖"
        },
        "concept": {
            "name": "💡 مفاهيم",
            "description": "سؤال عن فهم مفهوم معين",
            "icon": "💡"
        },
        "fact": {
            "name": "📌 حقائق",
            "description": "سؤال عن حقيقة أو معلومة محددة",
            "icon": "📌"
        },
        "mixed": {
            "name": "🎯 مختلط",
            "description": "مزيج من كل الأنواع",
            "icon": "🎯"
        }
    }

    # مستويات الصعوبة
    DIFFICULTY_LEVELS = {
        "easy":   {"name": "🟢 سهل",    "description": "أسئلة مباشرة وبسيطة"},
        "medium": {"name": "🟡 متوسط",  "description": "أسئلة تحتاج فهم"},
        "hard":   {"name": "🔴 صعب",    "description": "أسئلة تحتاج تحليل"},
    }

    def __init__(self, ai_engine):
        self.ai = ai_engine

    # ─────────────────────────────────────────
    # توليد البطاقات
    # ─────────────────────────────────────────
    def generate(
        self,
        text: str,
        num_cards: int = 10,
        card_type: str = "mixed",
        difficulty: str = "medium",
        language: str = "ar"
    ) -> Dict[str, Any]:
        """
        توليد بطاقات الحفظ من النص

        Returns:
            {
                'success': bool,
                'cards': [...],
                'total': int,
                'error': str
            }
        """
        if not text or len(text.strip()) < 50:
            return {
                'success': False,
                'cards': [],
                'total': 0,
                'error': 'النص قصير جداً! محتاج على الأقل 50 حرف'
            }

        # تحديد عدد البطاقات المنطقي
        num_cards = max(3, min(num_cards, 20))

        prompt = self._build_prompt(text, num_cards, card_type, difficulty)

        try:
            response = self.ai.answer_question(context="", question=prompt)
            cards    = self._parse_response(response, num_cards)

            if not cards:
                # محاولة ثانية بـ prompt أبسط
                simple_prompt = self._build_simple_prompt(text, num_cards)
                response2 = self.ai.answer_question(context="", question=simple_prompt)
                cards         = self._parse_response(response2, num_cards)

            if not cards:
                return {
                    'success': False,
                    'cards': [],
                    'total': 0,
                    'error': 'مقدرتش أولّد البطاقات، جرب تاني'
                }

            # إضافة معلومات لكل بطاقة
            for i, card in enumerate(cards):
                card['id']         = i + 1
                card['known']      = None   # None = لم يُجب عليها بعد
                card['flipped']    = False
                card['difficulty'] = card.get('difficulty', difficulty)

            return {
                'success':    True,
                'cards':      cards,
                'total':      len(cards),
                'card_type':  card_type,
                'difficulty': difficulty,
                'error':      None
            }

        except Exception as e:
            return {
                'success': False,
                'cards':   [],
                'total':   0,
                'error':   f'خطأ: {str(e)}'
            }

    # ─────────────────────────────────────────
    # بناء الـ Prompt
    # ─────────────────────────────────────────
    def _build_prompt(
        self,
        text: str,
        num_cards: int,
        card_type: str,
        difficulty: str
    ) -> str:

        type_instructions = {
            "definition": "ركّز على تعريفات المصطلحات والمفاهيم",
            "concept":    "ركّز على الأفكار الرئيسية وكيف تترابط",
            "fact":       "ركّز على الحقائق والأرقام والمعلومات المحددة",
            "mixed":      "اعمل مزيج من التعريفات والمفاهيم والحقائق",
        }

        diff_instructions = {
            "easy":   "أسئلة بسيطة ومباشرة، الإجابة واضحة من النص",
            "medium": "أسئلة تحتاج فهم المحتوى",
            "hard":   "أسئلة تحتاج تحليل وربط المعلومات",
        }

        # تقطيع النص لو طويل
        max_chars = 3000
        text_to_use = text[:max_chars] + "..." if len(text) > max_chars else text

        return f"""أنت مساعد تعليمي متخصص في عمل بطاقات الحفظ (Flashcards).

المحتوى:
\"\"\"
{text_to_use}
\"\"\"

المطلوب: اعمل {num_cards} بطاقة حفظ من المحتوى ده.

التعليمات:
- نوع البطاقات: {type_instructions.get(card_type, type_instructions['mixed'])}
- مستوى الصعوبة: {diff_instructions.get(difficulty, diff_instructions['medium'])}
- السؤال: واضح ومحدد
- الإجابة: مختصرة وواضحة (2-3 جمل كحد أقصى)
- تلميح: جملة صغيرة تساعد لو المستخدم اتعثر

الرد يكون JSON فقط بالشكل ده:
{{
  "cards": [
    {{
      "question": "السؤال هنا",
      "answer": "الإجابة هنا",
      "hint": "التلميح هنا",
      "category": "تصنيف الموضوع",
      "difficulty": "easy/medium/hard"
    }}
  ]
}}

مهم جداً:
- ارجع JSON فقط بدون أي كلام تاني
- الأسئلة من المحتوى المذكور بس
- الإجابات مختصرة ومفيدة
- التلميح يكون مفيد فعلاً"""

    def _build_simple_prompt(self, text: str, num_cards: int) -> str:
        """Prompt بسيط كـ Fallback"""
        text_short = text[:2000]
        return f"""من النص ده اعمل {num_cards} بطاقة حفظ.

النص: {text_short}

الرد JSON فقط:
{{
  "cards": [
    {{"question": "سؤال", "answer": "إجابة", "hint": "تلميح", "category": "عام", "difficulty": "medium"}}
  ]
}}"""

    # ─────────────────────────────────────────
    # تحليل الرد
    # ─────────────────────────────────────────
    def _parse_response(self, response: str, expected_count: int) -> List[Dict]:
        """تحليل رد AI واستخراج البطاقات"""
        if not response:
            return []

        # محاولة 1: JSON مباشر
        try:
            data  = json.loads(response.strip())
            cards = data.get('cards', [])
            if cards and self._validate_cards(cards):
                return cards[:expected_count]
        except json.JSONDecodeError:
            pass

        # محاولة 2: استخراج JSON من النص
        try:
            pattern = r'\{[\s\S]*"cards"[\s\S]*\}'
            matches = re.findall(pattern, response)
            for match in matches:
                try:
                    data  = json.loads(match)
                    cards = data.get('cards', [])
                    if cards and self._validate_cards(cards):
                        return cards[:expected_count]
                except Exception:
                    continue
        except Exception:
            pass

        # محاولة 3: استخراج بطاقات فردية
        try:
            card_pattern = r'\{[^{}]*"question"[^{}]*"answer"[^{}]*\}'
            matches      = re.findall(card_pattern, response, re.DOTALL)
            cards = []
            for match in matches:
                try:
                    card = json.loads(match)
                    if 'question' in card and 'answer' in card:
                        card.setdefault('hint',       'فكر كويس!')
                        card.setdefault('category',   'عام')
                        card.setdefault('difficulty', 'medium')
                        cards.append(card)
                except Exception:
                    continue
            if cards:
                return cards[:expected_count]
        except Exception:
            pass

        return []

    def _validate_cards(self, cards: List[Dict]) -> bool:
        """التحقق من صحة البطاقات"""
        if not cards or not isinstance(cards, list):
            return False
        for card in cards[:3]:  # نتحقق من أول 3 بس
            if not isinstance(card, dict):
                return False
            if 'question' not in card or 'answer' not in card:
                return False
            if not card['question'] or not card['answer']:
                return False
        return True

    # ─────────────────────────────────────────
    # تقييم الأداء
    # ─────────────────────────────────────────
    def evaluate_session(self, cards: List[Dict]) -> Dict:
        """تقييم جلسة المذاكرة"""
        total   = len(cards)
        known   = sum(1 for c in cards if c.get('known') is True)
        unknown = sum(1 for c in cards if c.get('known') is False)
        skipped = total - known - unknown

        if total == 0:
            return {
                'total': 0, 'known': 0, 'unknown': 0,
                'skipped': 0, 'percentage': 0,
                'grade': 'لم تبدأ', 'emoji': '😴',
                'message': 'ابدأ المذاكرة الأول!'
            }

        answered   = known + unknown
        percentage = round((known / answered * 100) if answered > 0 else 0)

        if percentage >= 90:
            grade, emoji, msg = 'ممتاز', '🌟', 'أنت نجم! حافظ على الإيقاع ده'
        elif percentage >= 75:
            grade, emoji, msg = 'جيد جداً', '😊', 'شغل عظيم! بس كرر اللي مش عارفه'
        elif percentage >= 60:
            grade, emoji, msg = 'جيد', '🙂', 'كويس! راجع البطاقات اللي غلطت فيها'
        elif percentage >= 40:
            grade, emoji, msg = 'مقبول', '😐', 'تحتاج مراجعة أكتر، ركز على الأساسيات'
        else:
            grade, emoji, msg = 'يحتاج مراجعة', '😅', 'مش مشكلة! اقرأ المحتوى تاني وكرر'

        return {
            'total':      total,
            'known':      known,
            'unknown':    unknown,
            'skipped':    skipped,
            'answered':   answered,
            'percentage': percentage,
            'grade':      grade,
            'emoji':      emoji,
            'message':    msg,
            'stars':      '⭐' * min(5, max(1, percentage // 20))
        }

    def get_unknown_cards(self, cards: List[Dict]) -> List[Dict]:
        """استخراج البطاقات اللي المستخدم مش عارفها"""
        return [c for c in cards if c.get('known') is False]

    def reset_session(self, cards: List[Dict]) -> List[Dict]:
        """إعادة تعيين الجلسة"""
        for card in cards:
            card['known']   = None
            card['flipped'] = False
        return cards