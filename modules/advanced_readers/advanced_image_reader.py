"""
🖼️ Advanced Image Reader - قارئ الصور المتطور
يستخدم OCR.space API (أسرع وأدق من Tesseract)
"""
import io
import time
import requests
from pathlib import Path
from typing import Dict, Optional, Union


class AdvancedImageReader:
    """قارئ الصور المتطور باستخدام OCR.space"""

    OCR_SPACE_URL = "https://api.ocr.space/parse/image"

    # الصيغ المدعومة
    SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'pdf', 'tiff']

    # الحد الأقصى لحجم الملف (1 MB في OCR.space المجاني)
    MAX_FILE_SIZE_MB = 1

    def __init__(self, api_key: str):
        """
        تهيئة القارئ

        Args:
            api_key: مفتاح OCR.space API
        """
        self.api_key = api_key
        self.is_ready = bool(api_key and api_key.strip())

    def read(
        self,
        file_data: Union[bytes, str, Path],
        language: str = 'ara',
        progress_callback=None
    ) -> Dict:
        """
        قراءة النص من صورة

        Args:
            file_data: bytes أو مسار الملف
            language: اللغة (ara/eng/ara+eng)
            progress_callback: دالة التقدم

        Returns:
            dict: {
                'success': bool,
                'text': str,
                'language': str,
                'processing_time': float,
                'engine_used': str,
                'error': str
            }
        """
        result = {
            'success': False,
            'text': '',
            'language': language,
            'processing_time': 0,
            'engine_used': 'OCR.space',
            'error': None
        }

        start_time = time.time()

        if not self.is_ready:
            result['error'] = "مفتاح OCR.space غير متاح"
            return result

        try:
            # تحويل لـ bytes لو لازم
            if progress_callback:
                progress_callback(0.1, "📂 بيحضّر الصورة...")

            image_bytes = self._get_image_bytes(file_data)

            if not image_bytes:
                result['error'] = "فشل قراءة الصورة"
                return result

            # تحضير الصورة (ضغط لو لازم)
            if progress_callback:
                progress_callback(0.3, "🔧 بيحضّر الصورة للإرسال...")

            image_bytes = self._optimize_image(image_bytes)

            # إرسال للـ API
            if progress_callback:
                progress_callback(0.5, "🌐 بيرسل لـ OCR.space (سريع جداً)...")

            ocr_text = self._send_to_ocr_space(image_bytes, language)

            if progress_callback:
                progress_callback(0.9, "✨ بيخلص...")

            # محاولة fallback لو فشل
            if not ocr_text or not ocr_text.strip():
                if language == 'ara':
                    # جرب عربي + إنجليزي
                    if progress_callback:
                        progress_callback(0.7, "🔄 بيحاول مرة تانية بـ ara+eng...")
                    ocr_text = self._send_to_ocr_space(image_bytes, 'ara,eng')

            result['text'] = ocr_text.strip() if ocr_text else ''
            result['success'] = bool(result['text'])
            result['processing_time'] = round(time.time() - start_time, 2)

            if not result['success']:
                result['error'] = "مقدرتش أقرأ نص من الصورة"

            if progress_callback:
                progress_callback(1.0, "✅ تم!")

        except Exception as e:
            result['error'] = f"خطأ: {str(e)}"
            result['processing_time'] = round(time.time() - start_time, 2)

        return result

    def _get_image_bytes(self, file_data) -> Optional[bytes]:
        """تحويل الـ input لـ bytes"""
        try:
            if isinstance(file_data, bytes):
                return file_data
            elif isinstance(file_data, (str, Path)):
                with open(file_data, 'rb') as f:
                    return f.read()
            elif hasattr(file_data, 'read'):
                # File-like object
                file_data.seek(0)
                return file_data.read()
            else:
                return None
        except Exception:
            return None

    def _optimize_image(self, image_bytes: bytes) -> bytes:
        """
        تحسين الصورة (ضغط لو حجمها كبير)
        """
        try:
            size_mb = len(image_bytes) / (1024 * 1024)

            # لو الحجم أقل من 1 MB، رجّعها زي ما هي
            if size_mb <= self.MAX_FILE_SIZE_MB:
                return image_bytes

            # ضغط الصورة
            from PIL import Image
            img = Image.open(io.BytesIO(image_bytes))

            # تحويل لـ RGB لو لازم
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # تصغير لو الأبعاد كبيرة
            max_dim = 2500
            if img.width > max_dim or img.height > max_dim:
                img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

            # حفظ بجودة أقل
            output = io.BytesIO()
            quality = 85

            # محاولة الوصول للحجم المطلوب
            while quality > 30:
                output.seek(0)
                output.truncate()
                img.save(output, format='JPEG', quality=quality, optimize=True)

                new_size_mb = len(output.getvalue()) / (1024 * 1024)
                if new_size_mb <= self.MAX_FILE_SIZE_MB:
                    break

                quality -= 10

            return output.getvalue()

        except Exception as e:
            print(f"⚠️ فشل تحسين الصورة: {e}")
            return image_bytes

    def _send_to_ocr_space(self, image_bytes: bytes, language: str = 'ara') -> str:
        """
        إرسال الصورة لـ OCR.space API

        Args:
            image_bytes: bytes الصورة
            language: اللغة

        Returns:
            str: النص المستخرج
        """
        try:
            payload = {
                'apikey': self.api_key,
                'language': language,
                'isOverlayRequired': False,
                'detectOrientation': True,
                'scale': True,
                'OCREngine': 2,  # محرك أحدث وأدق
            }

            files = {
                'file': ('image.jpg', image_bytes, 'image/jpeg')
            }

            response = requests.post(
                self.OCR_SPACE_URL,
                data=payload,
                files=files,
                timeout=60
            )

            if response.status_code != 200:
                print(f"⚠️ OCR.space status: {response.status_code}")
                return ""

            data = response.json()

            # التحقق من الأخطاء
            if data.get('IsErroredOnProcessing'):
                error_msg = data.get('ErrorMessage', ['Unknown error'])
                if isinstance(error_msg, list):
                    error_msg = ' | '.join(error_msg)
                print(f"⚠️ OCR.space error: {error_msg}")
                return ""

            # استخراج النص
            parsed_results = data.get('ParsedResults', [])
            if not parsed_results:
                return ""

            text = parsed_results[0].get('ParsedText', '')
            return text.strip()

        except requests.Timeout:
            print("⚠️ OCR.space timeout")
            return ""
        except Exception as e:
            print(f"⚠️ OCR.space exception: {e}")
            return ""

    def check_availability(self) -> Dict:
        """التحقق من حالة الخدمة"""
        return {
            'available': self.is_ready,
            'engine': 'OCR.space',
            'api_key_set': bool(self.api_key),
        }