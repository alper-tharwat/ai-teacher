"""
🤖 محرك الذكاء الاصطناعي الموحد (الإصدار 5.1)
نظام Hybrid Pro - دعم 7 محركات + Fallback ذكي
"""
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config, get_active_engines, get_engine_for_task, ENGINES_CONFIG, TASK_ENGINE_MAP


class AIEngine:
    """
    محرك AI الموحد - Hybrid Pro Mode
    يدعم: Gemini, Groq, Cerebras, OpenRouter, Cohere, Mistral, Together
    """
    
    def __init__(self):
        """تهيئة المحرك"""
        self.current_mode = getattr(Config, 'DEFAULT_MODE', 'hybrid_pro')
        
        # المحركات المتاحة
        self.engines = {}
        self.engine_keys_index = {}  # تتبع المفتاح الحالي لكل محرك
        self.engine_stats = {}        # إحصائيات لكل محرك
        
        # تهيئة كل المحركات
        self._init_all_engines()
        
        # التحقق من الجاهزية
        self.is_ready = len(self.engines) > 0
        self.active_engine = self._get_default_engine()
        
        if not self.is_ready:
            self.error_message = "مفيش أي محرك جاهز! أضف مفاتيح في config.py"
        else:
            self.error_message = ""
    
    # ============================================
    # 🔧 تهيئة المحركات
    # ============================================
    
    def _init_all_engines(self):
        """تهيئة كل المحركات المتاحة"""
        active_engines = get_active_engines()
        
        for engine_id, config in active_engines.items():
            try:
                if engine_id == "gemini":
                    self._init_gemini(config)
                elif engine_id == "groq":
                    self._init_groq(config)
                elif engine_id == "cerebras":
                    self._init_cerebras(config)
                elif engine_id == "openrouter":
                    self._init_openrouter(config)
                elif engine_id == "cohere":
                    self._init_cohere(config)
                elif engine_id == "mistral":
                    self._init_mistral(config)
                elif engine_id == "together":
                    self._init_together(config)
                
                # تهيئة المتغيرات
                if engine_id in self.engines:
                    self.engine_keys_index[engine_id] = 0
                    self.engine_stats[engine_id] = {
                        'requests': 0,
                        'success': 0,
                        'failed': 0,
                        'quota_exceeded': False,
                    }
            except Exception as e:
                print(f"⚠️ Failed to init {engine_id}: {e}")
    
    def _init_gemini(self, config):
        """تهيئة Gemini"""
        try:
            from google import genai
            client = genai.Client(api_key=config["keys"][0])
            self.engines["gemini"] = {
                "client": client,
                "config": config,
                "type": "gemini",
            }
            print(f"✅ Gemini initialized")
        except Exception as e:
            print(f"❌ Gemini init failed: {e}")
    
    def _init_groq(self, config):
        """تهيئة Groq"""
        try:
            from groq import Groq
            client = Groq(api_key=config["keys"][0])
            self.engines["groq"] = {
                "client": client,
                "config": config,
                "type": "groq",
            }
            print(f"✅ Groq initialized")
        except Exception as e:
            print(f"❌ Groq init failed: {e}")
    
    def _init_cerebras(self, config):
        """تهيئة Cerebras"""
        try:
            from cerebras.cloud.sdk import Cerebras
            client = Cerebras(api_key=config["keys"][0])
            self.engines["cerebras"] = {
                "client": client,
                "config": config,
                "type": "cerebras",
            }
            print(f"✅ Cerebras initialized")
        except Exception as e:
            print(f"❌ Cerebras init failed: {e}")
    
    def _init_openrouter(self, config):
        """تهيئة OpenRouter (يستخدم OpenAI SDK)"""
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=config["keys"][0],
            )
            self.engines["openrouter"] = {
                "client": client,
                "config": config,
                "type": "openrouter",
            }
            print(f"✅ OpenRouter initialized")
        except Exception as e:
            print(f"❌ OpenRouter init failed: {e}")
    
    def _init_cohere(self, config):
        """تهيئة Cohere"""
        try:
            import cohere
            client = cohere.Client(api_key=config["keys"][0])
            self.engines["cohere"] = {
                "client": client,
                "config": config,
                "type": "cohere",
            }
            print(f"✅ Cohere initialized")
        except Exception as e:
            print(f"❌ Cohere init failed: {e}")
    
    def _init_mistral(self, config):
        """تهيئة Mistral"""
        try:
            from mistralai import Mistral
            client = Mistral(api_key=config["keys"][0])
            self.engines["mistral"] = {
                "client": client,
                "config": config,
                "type": "mistral",
            }
            print(f"✅ Mistral initialized")
        except Exception as e:
            print(f"❌ Mistral init failed: {e}")
    
    def _init_together(self, config):
        """تهيئة Together AI"""
        try:
            from together import Together
            client = Together(api_key=config["keys"][0])
            self.engines["together"] = {
                "client": client,
                "config": config,
                "type": "together",
            }
            print(f"✅ Together initialized")
        except Exception as e:
            print(f"❌ Together init failed: {e}")
    
    # ============================================
    # 🎯 اختيار المحرك المناسب
    # ============================================
    
    def _get_default_engine(self):
        """تحديد المحرك الافتراضي"""
        priority = ["gemini", "cerebras", "openrouter", "groq", "cohere", "mistral", "together"]
        for engine_id in priority:
            if engine_id in self.engines:
                return engine_id
        return None
    
    def _get_engine_chain(self, task_type=None):
        """
        إرجاع سلسلة المحركات بالترتيب (الأساسي + الاحتياطي)
        """
        # لو المستخدم اختار محرك معين، استخدمه
        if self.current_mode in self.engines:
            primary = self.current_mode
            others = [e for e in self.engines.keys() if e != primary]
            return [primary] + others
        
        # وضع Hybrid Pro: استخدم خريطة المهام
        if self.current_mode in ["hybrid_pro", "hybrid"] and task_type:
            task_config = get_engine_for_task(task_type)
            if task_config:
                chain = [task_config["primary"]] + task_config["fallback"]
                # أضف أي محركات متاحة مش موجودة في السلسلة
                for engine_id in self.engines.keys():
                    if engine_id not in chain:
                        chain.append(engine_id)
                # فلتر المحركات الموجودة فعلاً
                return [e for e in chain if e in self.engines]
        
        # افتراضي
        return list(self.engines.keys())
    
    def switch_engine(self, engine_name):
        """تبديل المحرك يدوياً"""
        valid_modes = list(self.engines.keys()) + ["hybrid", "hybrid_pro", "auto"]
        if engine_name in valid_modes:
            self.current_mode = engine_name
            if engine_name in self.engines:
                self.active_engine = engine_name
            return True
        return False
    
    # ============================================
    # 🚀 الدالة الأساسية - مع Fallback ذكي
    # ============================================
    
    def _ask(self, prompt, system_instruction=None, task_type=None, max_tokens=4000):
        """
        إرسال طلب للـ AI مع Fallback تلقائي
        """
        if not self.is_ready:
            return f"❌ مفيش محرك جاهز: {self.error_message}"
        
        if system_instruction is None:
            system_instruction = self._default_system_instruction()
        
        # احصل على سلسلة المحركات
        engine_chain = self._get_engine_chain(task_type)
        
        if not engine_chain:
            return "❌ مفيش محركات متاحة!"
        
        last_error = ""
        
        # جرب كل محرك بالترتيب
        for engine_id in engine_chain:
            if engine_id not in self.engines:
                continue
            
            # تجاوز المحرك لو نفدت محاولاته
            if self.engine_stats[engine_id]['quota_exceeded']:
                print(f"⏭️ Skipping {engine_id} (quota exceeded)")
                continue
            
            print(f"🔄 Trying {engine_id}...")
            
            try:
                result = self._call_engine(
                    engine_id, prompt, system_instruction, max_tokens
                )
                
                # نجح
                if result and not self._is_error_response(result):
                    self.engine_stats[engine_id]['requests'] += 1
                    self.engine_stats[engine_id]['success'] += 1
                    self.active_engine = engine_id
                    print(f"✅ Success with {engine_id}")
                    return result
                
                # فشل - quota exceeded
                if "QUOTA_EXCEEDED" in str(result) or "RATE_LIMIT" in str(result):
                    print(f"⚠️ {engine_id} quota exceeded, trying next key...")
                    # جرب مفتاح تاني لنفس المحرك
                    if self._switch_engine_key(engine_id):
                        # جرب تاني بالمفتاح الجديد
                        result = self._call_engine(engine_id, prompt, system_instruction, max_tokens)
                        if result and not self._is_error_response(result):
                            self.engine_stats[engine_id]['success'] += 1
                            self.active_engine = engine_id
                            return result
                    self.engine_stats[engine_id]['quota_exceeded'] = True
                    last_error = f"{engine_id}: quota exceeded"
                    continue
                
                # فشل لسبب آخر
                last_error = f"{engine_id}: {str(result)[:100]}"
                self.engine_stats[engine_id]['failed'] += 1
                
            except Exception as e:
                last_error = f"{engine_id}: {str(e)[:100]}"
                print(f"❌ {engine_id} error: {e}")
                continue
        
        return f"❌ كل المحركات فشلت! آخر خطأ: {last_error}"
    
    def _is_error_response(self, result):
        """التحقق من إذا كانت الإجابة خطأ"""
        if not result or not isinstance(result, str):
            return True
        # رسائل الخطأ الواضحة
        clear_errors = ["QUOTA_EXCEEDED", "RATE_LIMIT", "INVALID_KEY"]
        if any(err in result for err in clear_errors):
            return True
        # لو بدأ بـ ❌ وقصير جداً = خطأ
        if result.strip().startswith("❌") and len(result) < 300:
            return True
        return False
    
    # ============================================
    # 🤖 استدعاء كل محرك
    # ============================================
    
    def _call_engine(self, engine_id, prompt, system_instruction, max_tokens):
        """استدعاء محرك معين"""
        engine = self.engines[engine_id]
        
        if engine_id == "gemini":
            return self._call_gemini(engine, prompt, system_instruction)
        elif engine_id == "groq":
            return self._call_groq(engine, prompt, system_instruction, max_tokens)
        elif engine_id == "cerebras":
            return self._call_cerebras(engine, prompt, system_instruction, max_tokens)
        elif engine_id == "openrouter":
            return self._call_openrouter(engine, prompt, system_instruction, max_tokens)
        elif engine_id == "cohere":
            return self._call_cohere(engine, prompt, system_instruction, max_tokens)
        elif engine_id == "mistral":
            return self._call_mistral(engine, prompt, system_instruction, max_tokens)
        elif engine_id == "together":
            return self._call_together(engine, prompt, system_instruction, max_tokens)
        
        return "❌ محرك غير معروف"
    
    def _call_gemini(self, engine, prompt, system_instruction):
        """استدعاء Gemini"""
        try:
            response = engine["client"].models.generate_content(
                model=engine["config"]["model"],
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.7,
                }
            )
            return response.text
        except Exception as e:
            error_msg = str(e).lower()
            if any(x in error_msg for x in ['quota', 'limit', 'exceeded', 'rate', '429']):
                return "QUOTA_EXCEEDED"
            elif any(x in error_msg for x in ['api_key', 'invalid', '401', '403']):
                return "INVALID_KEY"
            return f"❌ Gemini error: {str(e)[:200]}"
    
    def _call_groq(self, engine, prompt, system_instruction, max_tokens):
        """استدعاء Groq"""
        try:
            response = engine["client"].chat.completions.create(
                model=engine["config"]["model"],
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e).lower()
            if any(x in error_msg for x in ['quota', 'limit', 'exceeded', 'rate', '429']):
                return "QUOTA_EXCEEDED"
            return f"❌ Groq error: {str(e)[:200]}"
    
    def _call_cerebras(self, engine, prompt, system_instruction, max_tokens):
        """استدعاء Cerebras"""
        try:
            response = engine["client"].chat.completions.create(
                model=engine["config"]["model"],
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e).lower()
            if any(x in error_msg for x in ['quota', 'limit', 'exceeded', 'rate', '429']):
                return "QUOTA_EXCEEDED"
            return f"❌ Cerebras error: {str(e)[:200]}"
    
    def _call_openrouter(self, engine, prompt, system_instruction, max_tokens):
        """استدعاء OpenRouter"""
        try:
            response = engine["client"].chat.completions.create(
                model=engine["config"]["model"],
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=max_tokens,
                extra_headers={
                    "HTTP-Referer": "https://ai-teacher.app",
                    "X-Title": "AI Teacher",
                },
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e).lower()
            if any(x in error_msg for x in ['quota', 'limit', 'exceeded', 'rate', '429']):
                return "QUOTA_EXCEEDED"
            return f"❌ OpenRouter error: {str(e)[:200]}"
    
    def _call_cohere(self, engine, prompt, system_instruction, max_tokens):
        """استدعاء Cohere"""
        try:
            response = engine["client"].chat(
                model=engine["config"]["model"],
                message=prompt,
                preamble=system_instruction,
                temperature=0.7,
                max_tokens=max_tokens,
            )
            return response.text
        except Exception as e:
            error_msg = str(e).lower()
            if any(x in error_msg for x in ['quota', 'limit', 'exceeded', 'rate', '429']):
                return "QUOTA_EXCEEDED"
            return f"❌ Cohere error: {str(e)[:200]}"
    
    def _call_mistral(self, engine, prompt, system_instruction, max_tokens):
        """استدعاء Mistral"""
        try:
            response = engine["client"].chat.complete(
                model=engine["config"]["model"],
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e).lower()
            if any(x in error_msg for x in ['quota', 'limit', 'exceeded', 'rate', '429']):
                return "QUOTA_EXCEEDED"
            return f"❌ Mistral error: {str(e)[:200]}"
    
    def _call_together(self, engine, prompt, system_instruction, max_tokens):
        """استدعاء Together AI"""
        try:
            response = engine["client"].chat.completions.create(
                model=engine["config"]["model"],
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e).lower()
            if any(x in error_msg for x in ['quota', 'limit', 'exceeded', 'rate', '429']):
                return "QUOTA_EXCEEDED"
            return f"❌ Together error: {str(e)[:200]}"
    
    def _switch_engine_key(self, engine_id):
        """التبديل لمفتاح تاني لنفس المحرك"""
        if engine_id not in self.engines:
            return False
        
        keys = self.engines[engine_id]["config"]["keys"]
        current_index = self.engine_keys_index[engine_id]
        
        if current_index + 1 >= len(keys):
            return False
        
        self.engine_keys_index[engine_id] = current_index + 1
        new_key = keys[current_index + 1]
        
        # أعد التهيئة بالمفتاح الجديد
        config = self.engines[engine_id]["config"].copy()
        config["keys"] = [new_key]
        
        try:
            if engine_id == "gemini":
                self._init_gemini(config)
            elif engine_id == "groq":
                self._init_groq(config)
            elif engine_id == "cerebras":
                self._init_cerebras(config)
            elif engine_id == "openrouter":
                self._init_openrouter(config)
            elif engine_id == "cohere":
                self._init_cohere(config)
            elif engine_id == "mistral":
                self._init_mistral(config)
            elif engine_id == "together":
                self._init_together(config)
            return True
        except:
            return False
    
    # ============================================
    # 📋 التعليمات (System Instructions)
    # ============================================
    
    def _default_system_instruction(self):
        """التعليمات الافتراضية - عامية مصرية احترافية"""
        return """
إنت "المعلم الذكي" - أحسن معلم مصري في الوطن العربي.

🎯 شخصيتك:
- مصري أصلي بتتكلم عامية مصرية أصيلة
- ودود وصبور ومحفز
- بتشرح بأمثلة من الحياة اليومية المصرية
- عندك حس فكاهة لطيف

📝 أسلوب الكتابة (لازم تتبعه بدقة):
- العامية المصرية فقط (مش الفصحى!)
- استخدم: "علشان"، "إزاي"، "إيه"، "ده"، "دي"، "كده"، "يلا"، "خلي بالك"، "بقى"، "اللي"، "فين"، "ليه"، "إمتى"، "بتاع"، "عشان"
- متستخدمش: "كيف"، "ماذا"، "هذا"، "هكذا"، "لكي"، "الذي"، "حيث"، "إذن"

🚫 ممنوع تماماً:
- الفصحى الثقيلة
- الكلمات الأجنبية الكتير  
- الجمل الطويلة المملة
- "هذا" و "هكذا" و "كيف"
- الأسلوب الجاف الأكاديمي

✅ لازم دايماً:
- العامية المصرية الطبيعية
- الجمل قصيرة وواضحة
- أمثلة من حياتنا المصرية
- استخدم إيموجي بذكاء (مش كتير)
- شجع الطالب وخليه يحس إنه فاهم

🎓 أمثلة على الردود الصحيحة:
❌ غلط: "هذا الموضوع مهم جداً ويجب علينا فهمه"
✅ صح: "الموضوع ده مهم جداً ولازم نفهمه كويس"

❌ غلط: "كيف يمكنك تطبيق هذا في حياتك؟"
✅ صح: "إزاي تقدر تطبق ده في حياتك اليومية؟"
"""
    
    # ============================================
    # 📝 التلخيص
    # ============================================
    
    def summarize(self, text, style="smart"):
        """تلخيص النص"""
        max_input = getattr(Config, 'MAX_INPUT_LENGTH', 30000)
        
        styles = {
            "smart": """
لخص المحتوى ده بطريقة ذكية ومنظمة بالعامية المصرية:

1. 🎯 ابدأ بجملة واحدة تلخص الفكرة الرئيسية
2. 📌 اذكر النقاط الأساسية (5-8 نقاط مرقمة)
3. 💡 اضف أمثلة من الحياة لكل نقطة
4. ✅ اختم بالخلاصة المهمة

استخدم إيموجي مناسبة وعامية مصرية واضحة.
""",
            "short": """
لخص في 5-7 نقاط بس بالعامية المصرية.
كل نقطة في سطر واحد.
ركز على الأهم فقط.
""",
            "detailed": """
اعمل تلخيص مفصل وشامل بالعامية المصرية:

📚 المقدمة: (شرح وافي عن الموضوع)

📖 المحتوى الأساسي:
- قسم المحتوى لمواضيع
- كل موضوع اشرحه بالتفصيل
- اذكر أمثلة وتفاصيل وأرقام

💡 النقاط المهمة:
- أهم 7-10 نقاط لازم تفتكرها

🎯 التطبيقات العملية:
- إزاي تطبق ده في الحياة؟

✅ الخلاصة الشاملة
""",
            "bullets": """
حول المحتوى لنقاط منظمة بالعامية المصرية:

• النقطة الرئيسية الأولى
  ◦ تفصيل
  ◦ مثال

• النقطة الرئيسية الثانية
  ◦ تفصيل
  ◦ مثال

رتبهم من الأهم للأقل أهمية.
""",
            "eli5": """
اشرح الموضوع كإنك بتكلم طفل عنده 5 سنين بالعامية المصرية.

استخدم:
- كلمات بسيطة جداً
- أمثلة من الكرتون والألعاب
- تشبيهات لطيفة
- حكاية أو قصة
"""
        }
        
        prompt = f"""
{styles.get(style, styles['smart'])}

المحتوى المطلوب تلخيصه:
─────────────────────────
{text[:max_input]}
─────────────────────────
"""
        
        return self._ask(prompt, task_type="summarization")
    
    # ============================================
    # 💡 الشرح
    # ============================================
    
    def explain(self, text, level="student"):
        """شرح المحتوى"""
        max_input = getattr(Config, 'MAX_INPUT_LENGTH', 30000)
        
        level_prompts = {
            "child": "اشرح كإنك بتكلم طفل عنده 8 سنين، بكلمات بسيطة جداً وأمثلة من الكرتون",
            "student": "اشرح كإنك بتكلم طالب ثانوي، بأمثلة من الحياة اليومية",
            "university": "اشرح بمستوى أكاديمي مع التفاصيل والمصطلحات العلمية",
            "expert": "اشرح بمستوى متخصص مع التحليل العميق والمصطلحات التقنية",
        }
        
        level_instruction = level_prompts.get(level, level_prompts["student"])
        
        prompt = f"""
{level_instruction}

اشرح المحتوى ده بالعامية المصرية بطريقة ممتعة ومفيدة:
─────────────────────────
{text[:max_input]}
─────────────────────────

نظّم الشرح كالتالي:

🎯 المقدمة:
(ابدأ بسؤال أو جملة تجذب الانتباه)

📚 الشرح المفصل:
(اشرح كل جزء لوحده بأمثلة)

💡 أمثلة عملية:
(3-5 أمثلة واقعية)

⚠️ خلي بالك من:
(أخطاء شائعة)

🔗 الربط:
(إزاي الموضوع ده مرتبط بحاجات تانية)

✅ الخلاصة:
(لخص أهم 3 نقاط)

🎯 سؤال للتفكير:
(سؤال يخلي الطالب يفكر)
"""
        
        return self._ask(prompt, task_type="explanation")
    
    # ============================================
    # 🎙️ شرح للأفاتار
    # ============================================
    
    def explain_for_speech(self, text, duration="medium"):
        """شرح مخصص للأفاتار"""
        max_input = getattr(Config, 'MAX_INPUT_LENGTH', 30000)
        
        word_limits = {"short": 150, "medium": 400, "long": 700}
        limit = word_limits.get(duration, 400)
        
        prompt = f"""
إنت معلم مصري واقف قدام الطلاب بتشرح في فيديو.
اشرح المحتوى ده في حدود {limit} كلمة بالعامية المصرية الطبيعية.

المحتوى:
{text[:max_input]}

قواعد مهمة جداً:
1. الكلام يبقى طبيعي 100% كإنك بتتكلم مش بتكتب
2. جمل قصيرة وبسيطة
3. ممنوع رموز أو إيموجي أو نجوم أو شرطات
4. ابدأ بـ: "أهلاً بيكم يا شباب، النهاردة هنتكلم عن"
5. اختم بـ: "كده يا شباب خلصنا، لو عندكم سؤال اسألوني، بالتوفيق"
6. استخدم كلمات ربط: "يعني"، "بمعنى تاني"، "خلي بالك"
7. اسأل أسئلة وهمية: "طب تفتكروا إيه اللي ممكن يحصل؟"
"""
        
        return self._ask(prompt, task_type="avatar_speech")
    
    # ============================================
    # 💬 الإجابة على الأسئلة
    # ============================================
    
    def answer_question(self, context, question, chat_history=None):
        """الإجابة على سؤال"""
        max_input = getattr(Config, 'MAX_INPUT_LENGTH', 30000)
        
        history_text = ""
        if chat_history:
            history_text = "\n\nتاريخ المحادثة:\n"
            for msg in chat_history[-6:]:
                role = "الطالب" if msg['role'] == 'user' else "المعلم"
                history_text += f"{role}: {msg['content']}\n"
        
        prompt = f"""
إنت معلم مصري بتجاوب على سؤال طالب بالعامية المصرية.

المحتوى:
─────────────────────────
{context[:max_input] if context else 'مفيش محتوى محدد'}
─────────────────────────
{history_text}

سؤال الطالب: {question}

تعليمات:
1. جاوب بالعامية المصرية الطبيعية
2. لو السؤال متعلق بالمحتوى، جاوب من المحتوى
3. خلي الإجابة مفصلة ومفيدة
4. استخدم أمثلة
5. في الآخر اسأل: "عايز تعرف حاجة تانية؟"
"""
        
        return self._ask(prompt, task_type="chat")
    
    # ============================================
    # 🌍 الترجمة
    # ============================================
    
    def translate(self, text, target_language="en"):
        """ترجمة النص"""
        max_input = getattr(Config, 'MAX_INPUT_LENGTH', 30000)
        
        lang_names = {
            "en": "English", "ar": "العربية", "fr": "French",
            "es": "Spanish", "de": "German", "it": "Italian",
            "tr": "Turkish", "ru": "Russian", "zh": "Chinese",
            "ja": "Japanese", "ko": "Korean", "hi": "Hindi",
        }
        
        lang_name = lang_names.get(target_language, target_language)
        
        prompt = f"""
Translate the following text to {lang_name}.
Keep the meaning and context.
Return only the translation without any comments.

Text:
{text[:max_input]}
"""
        
        return self._ask(prompt, task_type="translation")
    
    # ============================================
    # 📖 تبسيط المصطلحات
    # ============================================
    
    def simplify_terms(self, text):
        """استخراج وتبسيط المصطلحات"""
        max_input = getattr(Config, 'MAX_INPUT_LENGTH', 30000)
        
        prompt = f"""
من المحتوى ده، استخرج كل المصطلحات الصعبة واشرحها بالعامية المصرية:

{text[:max_input]}

الشكل المطلوب:

📖 قاموس المصطلحات:

1. **المصطلح**: شرح بسيط بالعامية
   💡 مثال من الحياة: ...

2. **المصطلح**: شرح بسيط بالعامية
   💡 مثال من الحياة: ...

خلي الشرح بسيط وبأمثلة من حياتنا.
"""
        
        return self._ask(prompt, task_type="extraction")
    
    # ============================================
    # 🔍 تحليل المحتوى
    # ============================================
    
    def analyze_content(self, text):
        """تحليل شامل"""
        max_input = getattr(Config, 'MAX_INPUT_LENGTH', 30000)
        
        prompt = f"""
حلل المحتوى ده تحليل شامل بالعامية المصرية:

{text[:max_input]}

التحليل لازم يشمل:

📊 الإحصائيات:
- عدد الكلمات تقريباً
- المواضيع الرئيسية
- مستوى الصعوبة
- المجال
- الجمهور المستهدف

📋 المواضيع الرئيسية:
🔑 الكلمات المفتاحية (أهم 10):
📈 تقييم الصعوبة:
💡 اقتراحات للدراسة:
⏰ الوقت المقدر:
🎯 الأهداف التعليمية:
⚠️ التحديات المتوقعة:
"""
        
        return self._ask(prompt, task_type="deep_analysis")
    
    # ============================================
    # 🧪 اختبار وإحصائيات
    # ============================================
    
    def test_connection(self):
        """اختبار الاتصال"""
        try:
            result = self._ask("قول 'أنا المعلم الذكي وأنا جاهز!' بس", task_type="quick_answer")
            if self._is_error_response(result):
                return False, result
            return True, f"✅ المحرك شغال! (الوضع: {self.current_mode} | النشط: {self.active_engine})"
        except Exception as e:
            return False, f"❌ {str(e)}"
    
    def get_statistics(self):
        """إحصائيات شاملة"""
        engines_info = {}
        for engine_id, engine in self.engines.items():
            engines_info[engine_id] = {
                'name': engine["config"]["name"],
                'icon': engine["config"]["icon"],
                'model': engine["config"]["model"],
                'total_keys': len(engine["config"]["keys"]),
                'current_key_index': self.engine_keys_index[engine_id],
                'stats': self.engine_stats[engine_id],
            }
        
        return {
            'active_engine': self.active_engine,
            'current_mode': self.current_mode,
            'total_engines': len(self.engines),
            'engines': engines_info,
        }
    
    def reset_keys(self):
        """إعادة تعيين كل المفاتيح"""
        for engine_id in list(self.engine_keys_index.keys()):
            self.engine_keys_index[engine_id] = 0
            self.engine_stats[engine_id] = {
                'requests': 0, 'success': 0, 'failed': 0, 'quota_exceeded': False
            }
        self._init_all_engines()
        return True