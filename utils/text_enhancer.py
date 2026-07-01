"""
🎯 محسّن النص للنطق
بيحول النص العربي لنص قابل للنطق بشكل طبيعي
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re


class TextEnhancer:
    """
    محسّن النص العربي للنطق الصوتي
    
    الميزات:
    1. تصحيح نطق الكلمات الشائعة
    2. تحويل الأرقام لحروف
    3. إضافة وقفات طبيعية
    4. تحويل الرموز لكلمات
    5. تنظيف النص من الإيموجي والرموز
    6. تطبيع الكلمات العامية
    """
    
    # 📚 قاموس تصحيح النطق
    # الكلمة الأصلية → النطق الصحيح
    PRONUNCIATION_FIXES = {
        # كلمات شائعة بتتقرا غلط
        "علشان": "عَشان",
        "عشان": "عَشان",
        "إزاي": "إِزّاي",
        "ازاي": "إِزّاي",
        "إيه": "إيه",
        "ايه": "إيه",
        "ده": "دَه",
        "دي": "دي",
        "دول": "دول",
        "كده": "كِدَه",
        "كدا": "كِدَه",
        "بقى": "بَئَى",
        "بقا": "بَئَى",
        "ماشي": "ماشي",
        "خلاص": "خَلاص",
        "تمام": "تَمام",
        "يلا": "يَلّا",
        "هنا": "هِنا",
        "هناك": "هِناك",
        "فين": "فين",
        "إمتى": "إِمتى",
        "امتى": "إِمتى",
        "ليه": "ليه",
        "مين": "مين",
        "أنا": "أنا",
        "انا": "أنا",
        "إنت": "إنتَ",
        "انت": "إنتَ",
        "إنتي": "إنتي",
        "انتي": "إنتي",
        "احنا": "إحنا",
        "إحنا": "إحنا",
        "بتاع": "بِتاع",
        "بتاعة": "بِتاعة",
        "علي": "عَلى",
        "اللي": "اللي",
        "اللى": "اللي",
        "في": "في",
        "فى": "في",
        
        # مصطلحات تعليمية
        "AI": "إيه آي",
        "ai": "إيه آي",
        "PDF": "بي دي إف",
        "pdf": "بي دي إف",
        "API": "إيه بي آي",
        "URL": "يو آر إل",
        "GPT": "جي بي تي",
        "HTML": "إتش تي إم إل",
        "CSS": "سي إس إس",
        "JavaScript": "جافا سكريبت",
        "Python": "بايثون",
        "Google": "جوجل",
        "YouTube": "يوتيوب",
        "Facebook": "فيسبوك",
        "WhatsApp": "واتساب",
        "Instagram": "إنستجرام",
        
        # كلمات إنجليزية شائعة
        "OK": "أوكي",
        "ok": "أوكي",
        "Hi": "هاي",
        "Hello": "هالو",
        "Bye": "باي",
    }
    
    # 🔢 الأرقام بالحروف
    NUMBERS = {
        "0": "صفر",
        "1": "واحد",
        "2": "اتنين",
        "3": "تلاتة",
        "4": "أربعة",
        "5": "خمسة",
        "6": "ستة",
        "7": "سبعة",
        "8": "تمانية",
        "9": "تسعة",
        "10": "عشرة",
        "11": "إحداشر",
        "12": "اتناشر",
        "13": "تلتاشر",
        "14": "أربعتاشر",
        "15": "خمستاشر",
        "16": "ستاشر",
        "17": "سبعتاشر",
        "18": "تمنتاشر",
        "19": "تسعتاشر",
        "20": "عشرين",
        "30": "تلاتين",
        "40": "أربعين",
        "50": "خمسين",
        "60": "ستين",
        "70": "سبعين",
        "80": "تمانين",
        "90": "تسعين",
        "100": "ميّة",
        "200": "ميتين",
        "300": "تلتميّة",
        "400": "أربعميّة",
        "500": "خمسميّة",
        "1000": "ألف",
        "2000": "ألفين",
        "1000000": "مليون",
    }
    
    # 📛 الرموز الخاصة
    SYMBOLS = {
        "%": "في الميّة",
        "&": "و",
        "@": "آت",
        "#": "هاش",
        "$": "دولار",
        "€": "يورو",
        "£": "جنيه إسترليني",
        "+": "زائد",
        "=": "يساوي",
        "<": "أصغر من",
        ">": "أكبر من",
        "→": "ييؤدي إلى",
        "←": "يرجع إلى",
        "✓": "صح",
        "✗": "غلط",
        "★": "نجمة",
    }
    
    def __init__(self, ai_engine=None):
        """
        Args:
            ai_engine: محرك AI لتحسين متقدم (اختياري)
        """
        self.ai = ai_engine
    
    # ============================================
    # 🎯 الدالة الرئيسية
    # ============================================
    
    def enhance(self, text, use_ai=False):
        """
        تحسين النص للنطق
        
        Args:
            text: النص الأصلي
            use_ai: استخدم AI لتحسين متقدم (أبطأ بس أحسن)
        
        Returns:
            str: النص المحسّن
        """
        if not text or not text.strip():
            return ""
        
        # 1. تنظيف أساسي
        text = self._basic_clean(text)
        
        # 2. تحويل الرموز
        text = self._convert_symbols(text)
        
        # 3. تحويل الأرقام
        text = self._convert_numbers(text)
        
        # 4. تصحيح النطق
        text = self._fix_pronunciation(text)
        
        # 5. إضافة وقفات
        text = self._add_pauses(text)
        
        # 6. تحسين متقدم بالـ AI (اختياري)
        if use_ai and self.ai:
            text = self._ai_enhance(text)
        
        # 7. تنظيف نهائي
        text = self._final_cleanup(text)
        
        return text
    
    # ============================================
    # 🧹 التنظيف الأساسي
    # ============================================
    
    def _basic_clean(self, text):
        """تنظيف أساسي من الرموز غير المرغوبة"""
        
        # إزالة الإيموجي
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002500-\U00002BEF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001F900-\U0001F9FF"
            "\U0001FA00-\U0001FA6F"
            "\U0001FA70-\U0001FAFF"
            "\U00002600-\U000026FF"
            "]+",
            flags=re.UNICODE
        )
        text = emoji_pattern.sub(' ', text)
        
        # إزالة Markdown
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        text = re.sub(r'`(.+?)`', r'\1', text)
        text = re.sub(r'#{1,6}\s*', '', text)
        text = re.sub(r'```[\s\S]*?```', '', text)
        
        # إزالة الخطوط
        text = re.sub(r'─{2,}', '', text)
        text = re.sub(r'={2,}', '', text)
        text = re.sub(r'-{3,}', '', text)
        text = re.sub(r'_{3,}', '', text)
        
        # إزالة الأقواس الزخرفية
        text = re.sub(r'【|】|〖|〗', '', text)
        
        # إزالة الروابط
        text = re.sub(r'https?://\S+', ' ', text)
        text = re.sub(r'www\.\S+', ' ', text)
        
        # إزالة المسافات الزائدة
        text = re.sub(r' {2,}', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    # ============================================
    # 🔣 تحويل الرموز
    # ============================================
    
    def _convert_symbols(self, text):
        """تحويل الرموز لكلمات"""
        for symbol, word in self.SYMBOLS.items():
            text = text.replace(symbol, f" {word} ")
        return text
    
    # ============================================
    # 🔢 تحويل الأرقام
    # ============================================
    
    def _convert_numbers(self, text):
        """تحويل الأرقام لحروف"""
        
        def number_to_arabic(match):
            num_str = match.group()
            try:
                num = int(num_str)
                return self._number_to_words(num)
            except ValueError:
                return num_str
        
        # الأرقام الصحيحة
        text = re.sub(r'\b\d+\b', number_to_arabic, text)
        
        # الأرقام العربية
        arabic_nums = '٠١٢٣٤٥٦٧٨٩'
        english_nums = '0123456789'
        
        for i in range(10):
            text = text.replace(arabic_nums[i], english_nums[i])
        
        text = re.sub(r'\b\d+\b', number_to_arabic, text)
        
        return text
    
    def _number_to_words(self, num):
        """تحويل رقم لكلمات بالعامية"""
        if num == 0:
            return "صفر"
        
        # لو الرقم موجود في القاموس
        if str(num) in self.NUMBERS:
            return self.NUMBERS[str(num)]
        
        # أرقام بين 21-99
        if 21 <= num <= 99:
            tens = (num // 10) * 10
            ones = num % 10
            if ones == 0:
                return self.NUMBERS.get(str(tens), str(num))
            return f"{self.NUMBERS.get(str(ones), '')} و {self.NUMBERS.get(str(tens), '')}"
        
        # أرقام بين 100-999
        if 100 <= num <= 999:
            hundreds = (num // 100) * 100
            remainder = num % 100
            if remainder == 0:
                return self.NUMBERS.get(str(hundreds), str(num))
            return f"{self.NUMBERS.get(str(hundreds), '')} و {self._number_to_words(remainder)}"
        
        # أرقام أكبر
        if 1000 <= num < 1000000:
            thousands = num // 1000
            remainder = num % 1000
            thousand_word = "ألف" if thousands == 1 else "ألاف" if thousands < 11 else "ألف"
            if remainder == 0:
                return f"{self._number_to_words(thousands)} {thousand_word}"
            return f"{self._number_to_words(thousands)} {thousand_word} و {self._number_to_words(remainder)}"
        
        # لو الرقم كبير جداً، رجعه كنص
        return str(num)
    
    # ============================================
    # 🗣️ تصحيح النطق
    # ============================================
    
    def _fix_pronunciation(self, text):
        """تصحيح نطق الكلمات الشائعة"""
        words = text.split()
        fixed_words = []
        
        for word in words:
            # تنظيف الكلمة من علامات الترقيم
            clean_word = re.sub(r'[^\w\u0600-\u06FF]', '', word)
            punctuation = re.sub(r'[\w\u0600-\u06FF]', '', word)
            
            # البحث في القاموس
            if clean_word in self.PRONUNCIATION_FIXES:
                fixed_words.append(self.PRONUNCIATION_FIXES[clean_word] + punctuation)
            elif clean_word.lower() in self.PRONUNCIATION_FIXES:
                fixed_words.append(self.PRONUNCIATION_FIXES[clean_word.lower()] + punctuation)
            else:
                fixed_words.append(word)
        
        return ' '.join(fixed_words)
    
    # ============================================
    # ⏸️ إضافة وقفات
    # ============================================
    
    def _add_pauses(self, text):
        """إضافة وقفات طبيعية للنطق"""
        
        # وقفة بعد علامات الترقيم
        text = re.sub(r'([.!?؟])\s*', r'\1 ... ', text)
        text = re.sub(r'([,،])\s*', r'\1 . ', text)
        text = re.sub(r'([:؛])\s*', r'\1 .. ', text)
        
        # وقفة بعد علامات النداء
        text = re.sub(r'(يا\s+\w+)', r'\1 . ', text)
        
        # إزالة الوقفات الزائدة
        text = re.sub(r'\.{4,}', '...', text)
        text = re.sub(r' {2,}', ' ', text)
        
        return text
    
    # ============================================
    # 🤖 تحسين متقدم بالـ AI
    # ============================================
    
    def _ai_enhance(self, text):
        """تحسين النص باستخدام AI"""
        if not self.ai:
            return text
        
        try:
            prompt = f"""
            حسّن النص ده عشان يتقرا صوتياً بشكل طبيعي بالعامية المصرية:
            
            القواعد:
            1. استبدل الكلمات اللي ممكن تتقرا غلط بنطقها الصحيح
            2. متضيفش تشكيل كتير، بس على الكلمات اللي محتاجة
            3. حافظ على المعنى الأصلي تماماً
            4. اكتب الأرقام بالحروف لو موجودة
            5. اقسم الجمل الطويلة لجمل أقصر
            6. استخدم علامات الترقيم بشكل طبيعي
            
            النص:
            {text[:2000]}
            
            ⚠️ مهم: ارجع النص المحسّن بس بدون أي شرح أو ملاحظات
            """
            
            enhanced = self.ai._ask(prompt)
            
            # تنظيف الرد
            if enhanced and len(enhanced) > 50:
                # إزالة أي تعليقات من AI
                enhanced = re.sub(r'^(النص المحسّن:|التحسين:|الناتج:)\s*', '', enhanced)
                return enhanced.strip()
            
            return text
            
        except Exception as e:
            print(f"AI enhancement error: {e}")
            return text
    
    # ============================================
    # 🧽 التنظيف النهائي
    # ============================================
    
    def _final_cleanup(self, text):
        """تنظيف نهائي قبل النطق"""
        
        # إزالة الأقواس الفاضية
        text = re.sub(r'\(\s*\)', '', text)
        text = re.sub(r'\[\s*\]', '', text)
        
        # إزالة المسافات الزائدة
        text = re.sub(r' {2,}', ' ', text)
        text = re.sub(r'\n{2,}', '\n', text)
        
        # إزالة المسافات قبل علامات الترقيم
        text = re.sub(r' +([.!?؟,،:;؛])', r'\1', text)
        
        # تنظيف نهائي
        text = text.strip()
        
        return text
    
    # ============================================
    # 🎯 دوال جاهزة
    # ============================================
    
    def quick_enhance(self, text):
        """تحسين سريع بدون AI"""
        return self.enhance(text, use_ai=False)
    
    def smart_enhance(self, text):
        """تحسين ذكي بـ AI"""
        return self.enhance(text, use_ai=True)
    
    def prepare_for_speech(self, text, style="natural"):
        """
        تجهيز النص للنطق بأسلوب معين
        
        Args:
            text: النص
            style: 'natural' / 'slow' / 'fast' / 'storytelling'
        """
        # تحسين أساسي
        text = self.enhance(text, use_ai=False)
        
        if style == "slow":
            # إضافة وقفات أكتر
            text = re.sub(r'([.!?])', r'\1 ... ... ', text)
            text = re.sub(r'([,،])', r'\1 ... ', text)
        
        elif style == "fast":
            # تقليل الوقفات
            text = re.sub(r'\.\.\.', '.', text)
            text = re.sub(r'\.\.', '.', text)
        
        elif style == "storytelling":
            # وقفات درامية
            text = re.sub(r'([.!?])', r'\1 ... ', text)
            text = text.replace('!', '! ... ')
            text = text.replace('؟', '؟ ... ')
        
        return text