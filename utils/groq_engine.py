"""
⚡ محرك Groq AI
محرك سريع جداً مع 14,400 طلب يومي مجاناً
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from config import Config


class GroqEngine:
    """
    محرك Groq - الأسرع في العالم
    
    المميزات:
    - سرعة جنونية (10x أسرع من البقية)
    - 14,400 طلب يومي مجاناً
    - موديلات قوية (Llama 3.3 70B)
    - دعم العربي ممتاز
    """
    
    def __init__(self, api_key=None):
        """تهيئة المحرك"""
        try:
            # استخدم المفتاح المرسل أو الأول من القائمة
            if api_key:
                self.api_key = api_key
            else:
                valid_keys = [
                    k for k in Config.GROQ_API_KEYS 
                    if k and k.startswith("gsk_") and "XXXX" not in k
                ]
                self.api_key = valid_keys[0] if valid_keys else None
            
            if not self.api_key:
                self.is_ready = False
                self.error_message = "مفيش مفتاح Groq صحيح"
                self.client = None
            else:
                self.client = Groq(api_key=self.api_key)
                self.model = Config.GROQ_MODEL
                self.is_ready = True
                self.error_message = ""
        except Exception as e:
            self.is_ready = False
            self.error_message = str(e)
            self.client = None
    
    def _ask(self, prompt, system_instruction=None):
        """
        إرسال طلب للـ AI
        
        Args:
            prompt: السؤال أو الطلب
            system_instruction: تعليمات للـ AI
        
        Returns:
            str: رد الـ AI
        """
        if not self.is_ready:
            return f"❌ Groq مش جاهز: {self.error_message}"
        
        try:
            # التعليمات الأساسية
            if system_instruction is None:
                system_instruction = """
                أنت "المعلم الذكي" - أفضل معلم في الوطن العربي.
                
                قواعدك:
                1. بتشرح بالعامية المصرية البسيطة
                2. بتستخدم أمثلة من الحياة اليومية
                3. بتقسم الشرح لأجزاء صغيرة ومفهومة
                4. بتستخدم إيموجي عشان الشرح يبقى ممتع
                5. بتنبه على الأخطاء الشائعة
                6. بتشجع الطالب وتحفزه
                7. لو الطالب سأل سؤال مش متعلق بالمحتوى، حاول تساعده برضو
                """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                temperature=Config.AI_TEMPERATURE,
                max_tokens=4000,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = str(e).lower()
            
            if any(x in error_msg for x in ['quota', 'limit', 'rate', '429']):
                return "QUOTA_EXCEEDED"  # علامة خاصة للمدير
            
            elif any(x in error_msg for x in ['api_key', 'authenticate', 'invalid', '401']):
                return "INVALID_KEY"
            
            elif any(x in error_msg for x in ['network', 'connection', 'timeout']):
                return f"❌ مشكلة في الاتصال"
            
            else:
                return f"❌ خطأ Groq: {str(e)[:200]}"
    
    def test_connection(self):
        """اختبار الاتصال"""
        try:
            result = self._ask("قول 'أنا شغال!' بس")
            if "❌" in result or "QUOTA" in result or "INVALID" in result:
                return False, result
            return True, "✅ Groq شغال تمام!"
        except Exception as e:
            return False, f"❌ {str(e)}"