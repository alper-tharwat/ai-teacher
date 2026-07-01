"""
📕 Advanced PDF Reader - قارئ PDF متطور
يستخدم PyMuPDF (أسرع 10x من PyPDF2) + OCR.space للصور
"""
import os
import io
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional


class AdvancedPDFReader:
    """قارئ PDF متطور وسريع"""

    OCR_SPACE_URL = "https://api.ocr.space/parse/image"

    def __init__(self, ocr_api_key: Optional[str] = None):
        """
        تهيئة القارئ

        Args:
            ocr_api_key: مفتاح OCR.space (اختياري - للـ OCR)
        """
        self.ocr_api_key = ocr_api_key
        self.fitz_available = False
        self.ocr_available = bool(ocr_api_key and ocr_api_key.strip())

        # التحقق من PyMuPDF
        try:
            import fitz
            self.fitz = fitz
            self.fitz_available = True
        except ImportError:
            print("⚠️ PyMuPDF مش موجود! ثبته: pip install PyMuPDF")

    def read(self, file_path_or_bytes, progress_callback=None) -> Dict:
        """
        قراءة ملف PDF بشكل سريع وذكي

        Args:
            file_path_or_bytes: مسار الملف أو bytes
            progress_callback: دالة لتحديث التقدم (val, msg)

        Returns:
            dict: {
                'success': bool,
                'text': str (النص الكامل),
                'pages': list (كل صفحة منفصلة),
                'total_pages': int,
                'method_used': str,
                'has_images': bool,
                'processing_time': float,
                'error': str
            }
        """
        result = {
            'success': False,
            'text': '',
            'pages': [],
            'total_pages': 0,
            'method_used': None,
            'has_images': False,
            'processing_time': 0,
            'error': None
        }

        start_time = time.time()

        if not self.fitz_available:
            result['error'] = "PyMuPDF غير مثبت! pip install PyMuPDF"
            return result

        try:
            # فتح الملف
            if progress_callback:
                progress_callback(0.05, "📂 بيفتح الملف...")

            if isinstance(file_path_or_bytes, (str, Path)):
                doc = self.fitz.open(str(file_path_or_bytes))
            elif isinstance(file_path_or_bytes, bytes):
                doc = self.fitz.open(stream=file_path_or_bytes, filetype="pdf")
            else:
                # File-like object
                file_path_or_bytes.seek(0)
                doc = self.fitz.open(stream=file_path_or_bytes.read(), filetype="pdf")

            total_pages = len(doc)
            result['total_pages'] = total_pages

            if progress_callback:
                progress_callback(0.1, f"✅ تم فتح الملف ({total_pages} صفحة)")

            # ═══════════════════════════════════════════
            # المرحلة 1: محاولة استخراج النص مباشرة (سريع)
            # ═══════════════════════════════════════════
            if progress_callback:
                progress_callback(0.15, "📝 بيستخرج النص مباشرة (سريع)...")

            pages_text = []
            pages_with_images = []
            full_text = ""
            total_text_length = 0

            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                page_text = page.get_text("text")

                # تحديث التقدم
                if progress_callback and page_num % 5 == 0:
                    prog = 0.15 + (0.35 * (page_num / total_pages))
                    progress_callback(prog, f"📄 صفحة {page_num + 1}/{total_pages}...")

                if page_text and page_text.strip():
                    pages_text.append(page_text.strip())
                    full_text += f"\n\n=== صفحة {page_num + 1} ===\n{page_text}\n"
                    total_text_length += len(page_text.strip())
                else:
                    # الصفحة فاضية (ممكن تكون صورة)
                    pages_text.append("")
                    pages_with_images.append(page_num)

            # ═══════════════════════════════════════════
            # المرحلة 2: OCR للصفحات اللي مفيهاش نص (لو متاح)
            # ═══════════════════════════════════════════
            avg_text_per_page = total_text_length / total_pages if total_pages > 0 else 0
            needs_ocr = (
                len(pages_with_images) > 0 and  # في صفحات فاضية
                avg_text_per_page < 100  # ومتوسط النص قليل (يعني PDF صور)
            )

            if needs_ocr:
                result['has_images'] = True

                if self.ocr_available:
                    if progress_callback:
                        progress_callback(0.5, f"🖼️ بيقرأ {len(pages_with_images)} صفحة صور...")

                    ocr_results = self._ocr_pages(doc, pages_with_images, progress_callback)

                    # دمج نتائج OCR مع النصوص الأصلية
                    for i, page_num in enumerate(pages_with_images):
                        if i < len(ocr_results) and ocr_results[i]:
                            pages_text[page_num] = ocr_results[i]
                            full_text += f"\n\n=== صفحة {page_num + 1} (OCR) ===\n{ocr_results[i]}\n"

                    result['method_used'] = "PyMuPDF + OCR.space"
                else:
                    if progress_callback:
                        progress_callback(0.9, "⚠️ PDF فيه صور - OCR غير متاح")
                    result['method_used'] = "PyMuPDF فقط (بدون OCR)"
            else:
                result['method_used'] = "PyMuPDF (نص مباشر)"

            doc.close()

            if progress_callback:
                progress_callback(0.95, "✨ بيخلص...")

            # تحضير النتيجة
            result['text'] = full_text.strip()
            result['pages'] = pages_text
            result['success'] = bool(result['text'].strip())
            result['processing_time'] = round(time.time() - start_time, 2)

            if progress_callback:
                progress_callback(1.0, "✅ تم!")

        except Exception as e:
            import traceback
            result['error'] = f"خطأ: {str(e)}"
            result['processing_time'] = round(time.time() - start_time, 2)
            print(f"❌ PDF Error: {traceback.format_exc()}")

        return result

    def _ocr_pages(self, doc, page_numbers: List[int], progress_callback=None) -> List[str]:
        """
        تطبيق OCR على صفحات معينة

        Args:
            doc: PyMuPDF document
            page_numbers: قائمة بأرقام الصفحات

        Returns:
            list: النصوص المستخرجة
        """
        results = []
        total = len(page_numbers)

        for i, page_num in enumerate(page_numbers):
            if progress_callback:
                prog = 0.5 + (0.4 * (i / total))
                progress_callback(prog, f"🖼️ OCR للصفحة {page_num + 1} ({i+1}/{total})...")

            try:
                # تحويل الصفحة لصورة
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=200)
                img_bytes = pix.tobytes("png")

                # إرسال لـ OCR.space
                ocr_text = self._ocr_space_request(img_bytes)
                results.append(ocr_text)

            except Exception as e:
                print(f"⚠️ OCR فشل للصفحة {page_num + 1}: {e}")
                results.append("")

        return results

    def _ocr_space_request(self, image_bytes: bytes) -> str:
        """
        إرسال طلب لـ OCR.space API

        Args:
            image_bytes: bytes الصورة

        Returns:
            str: النص المستخرج
        """
        try:
            payload = {
                'apikey': self.ocr_api_key,
                'language': 'ara',  # عربي
                'isOverlayRequired': False,
                'detectOrientation': True,
                'scale': True,
                'OCREngine': 2,  # محرك أحدث
            }

            files = {
                'file': ('image.png', image_bytes, 'image/png')
            }

            response = requests.post(
                self.OCR_SPACE_URL,
                data=payload,
                files=files,
                timeout=60
            )

            if response.status_code != 200:
                return ""

            data = response.json()

            if data.get('IsErroredOnProcessing'):
                return ""

            parsed_results = data.get('ParsedResults', [])
            if not parsed_results:
                return ""

            text = parsed_results[0].get('ParsedText', '')
            return text.strip()

        except Exception as e:
            print(f"⚠️ OCR.space error: {e}")
            return ""

    @staticmethod
    def get_pages_range(pages: List[str], start_page: int, end_page: int) -> str:
        """دالة للحصول على نص من نطاق صفحات (متوافقة مع FileReader القديم)"""
        if not pages:
            return ""

        start_idx = max(0, start_page - 1)
        end_idx = min(len(pages), end_page)

        selected_pages = pages[start_idx:end_idx]

        combined_text = ""
        for i, page_text in enumerate(selected_pages, start=start_page):
            if page_text and page_text.strip():
                combined_text += f"\n{'='*50}\n📄 صفحة {i}\n{'='*50}\n{page_text}\n"

        return combined_text.strip()