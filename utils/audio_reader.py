# utils/audio_reader.py
# Audio Reader - محول الصوت لنص
# يدعم: MP3, WAV, M4A, OGG, FLAC, MP4

import os
import sys
import time
import tempfile
import traceback
from pathlib import Path

# =====================================================
# التحقق من المكتبات المطلوبة
# =====================================================
WHISPER_AVAILABLE = False
PYDUB_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    pass

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    pass


class AudioReader:
    """
    محول الصوت لنص باستخدام OpenAI Whisper
    يدعم: MP3, WAV, M4A, OGG, FLAC, MP4, WEBM
    """

    # الصيغ المدعومة
    SUPPORTED_FORMATS = {
        '.mp3': 'MP3',
        '.wav': 'WAV', 
        '.m4a': 'M4A',
        '.ogg': 'OGG',
        '.flac': 'FLAC',
        '.mp4': 'MP4',
        '.webm': 'WebM',
        '.aac': 'AAC',
        '.wma': 'WMA'
    }

    # موديلات Whisper المتاحة
    WHISPER_MODELS = {
        'tiny':   {'size': '39M',  'speed': 'سريع جداً',  'accuracy': 'منخفضة'},
        'base':   {'size': '74M',  'speed': 'سريع',       'accuracy': 'متوسطة'},
        'small':  {'size': '244M', 'speed': 'متوسط',      'accuracy': 'جيدة'},
        'medium': {'size': '769M', 'speed': 'بطيء',       'accuracy': 'عالية'},
    }

    # الحد الأقصى لحجم الملف (50MB)
    MAX_FILE_SIZE = 50 * 1024 * 1024

    # الحد الأقصى لطول الصوت قبل التقطيع (10 دقايق = 600 ثانية)
    MAX_CHUNK_DURATION = 600

    def __init__(self, model_name: str = 'base'):
        """
        تهيئة محول الصوت
        
        Args:
            model_name: اسم موديل Whisper (tiny/base/small/medium)
        """
        self.model_name = model_name
        self.model = None
        self.is_ready = False
        self.error_message = None
        self.temp_files = []  # تتبع الملفات المؤقتة لحذفها

        # التحقق من المتطلبات
        self._check_requirements()

    def _check_requirements(self):
        """التحقق من توفر كل المتطلبات"""
        
        # 1. التحقق من Whisper
        if not WHISPER_AVAILABLE:
            self.error_message = (
                "مكتبة Whisper مش موجودة!\n"
                "الحل: pip install openai-whisper"
            )
            return

        # 2. التحقق من FFmpeg
        if not self._check_ffmpeg():
            self.error_message = (
                "FFmpeg مش موجود!\n"
                "الحل: winget install ffmpeg\n"
                "أو حمله من: https://ffmpeg.org/download.html"
            )
            return

        # 3. التحقق من pydub (اختياري بس مفيد)
        if not PYDUB_AVAILABLE:
            # مش مشكلة كبيرة، بس نسجل تحذير
            print("⚠️ pydub مش موجودة - مش هينقطع الصوت الطويل")

        self.is_ready = True

    def _check_ffmpeg(self) -> bool:
        """التحقق من وجود FFmpeg"""
        import subprocess
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            return False

    def load_model(self, progress_callback=None) -> bool:
        """
        تحميل موديل Whisper
        
        Args:
            progress_callback: دالة لتحديث شريط التقدم (اختياري)
            
        Returns:
            True لو نجح التحميل
        """
        if not self.is_ready:
            return False

        if self.model is not None:
            return True  # الموديل محمّل بالفعل

        try:
            if progress_callback:
                progress_callback(0.1, f"⏳ بيحمّل موديل Whisper ({self.model_name})...")

            self.model = whisper.load_model(self.model_name)

            if progress_callback:
                progress_callback(0.3, "✅ الموديل اتحمل!")

            return True

        except Exception as e:
            self.error_message = f"فشل تحميل الموديل: {str(e)}"
            return False

    def get_audio_info(self, file_path: str) -> dict:
        """
        استخراج معلومات الملف الصوتي
        
        Returns:
            dict: معلومات الملف (مدة، حجم، صيغة...)
        """
        info = {
            'path': file_path,
            'name': os.path.basename(file_path),
            'size': 0,
            'size_mb': 0,
            'duration': 0,
            'duration_str': '0:00',
            'format': 'unknown',
            'channels': 1,
            'sample_rate': 0,
            'is_valid': False,
            'error': None
        }

        try:
            # حجم الملف
            file_size = os.path.getsize(file_path)
            info['size'] = file_size
            info['size_mb'] = round(file_size / (1024 * 1024), 2)

            # صيغة الملف
            ext = Path(file_path).suffix.lower()
            info['format'] = self.SUPPORTED_FORMATS.get(ext, ext.upper())

            # معلومات الصوت بـ pydub
            if PYDUB_AVAILABLE:
                try:
                    audio = AudioSegment.from_file(file_path)
                    duration_seconds = len(audio) / 1000  # تحويل من ms لـ seconds
                    info['duration'] = duration_seconds
                    info['duration_str'] = self._format_duration(duration_seconds)
                    info['channels'] = audio.channels
                    info['sample_rate'] = audio.frame_rate
                    info['is_valid'] = True
                except Exception as e:
                    info['error'] = f"تعذر قراءة معلومات الصوت: {str(e)}"
                    info['is_valid'] = True  # ممكن Whisper يقراه بردو
            else:
                info['is_valid'] = True  # هنجرب مع Whisper

        except Exception as e:
            info['error'] = str(e)
            info['is_valid'] = False

        return info

    def _format_duration(self, seconds: float) -> str:
        """تحويل الثواني لصيغة mm:ss أو hh:mm:ss"""
        seconds = int(seconds)
        if seconds < 3600:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes}:{secs:02d}"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            return f"{hours}:{minutes:02d}:{secs:02d}"

    def _convert_to_wav(self, file_path: str) -> str:
        """
        تحويل أي صيغة صوتية لـ WAV
        عشان Whisper يقدر يقراها بشكل أفضل
        
        Returns:
            مسار ملف WAV المؤقت
        """
        if not PYDUB_AVAILABLE:
            return file_path  # نرجع الملف الأصلي لو pydub مش موجود

        ext = Path(file_path).suffix.lower()
        
        # لو بالفعل WAV، رجّع نفس الملف
        if ext == '.wav':
            return file_path

        try:
            # تحويل للـ WAV
            audio = AudioSegment.from_file(file_path)
            
            # إنشاء ملف مؤقت
            temp_wav = tempfile.NamedTemporaryFile(
                suffix='.wav',
                delete=False,
                prefix='audio_reader_'
            )
            temp_wav.close()

            # تصدير بإعدادات مناسبة لـ Whisper
            audio.export(
                temp_wav.name,
                format='wav',
                parameters=[
                    '-ar', '16000',  # sample rate مناسب لـ Whisper
                    '-ac', '1'       # mono channel
                ]
            )

            self.temp_files.append(temp_wav.name)
            return temp_wav.name

        except Exception as e:
            print(f"⚠️ فشل التحويل لـ WAV: {e} - هنجرب الملف الأصلي")
            return file_path

    def _split_audio(self, file_path: str, chunk_duration: int = 300) -> list:
        """
        تقطيع الصوت لأجزاء صغيرة (للملفات الطويلة)
        
        Args:
            file_path: مسار الملف
            chunk_duration: مدة كل جزء بالثواني (افتراضي 5 دقايق)
            
        Returns:
            list: مسارات الأجزاء المقطعة
        """
        if not PYDUB_AVAILABLE:
            return [file_path]  # نرجع الملف كله لو pydub مش موجود

        try:
            audio = AudioSegment.from_file(file_path)
            duration_seconds = len(audio) / 1000

            # لو الملف قصير، مش محتاج تقطيع
            if duration_seconds <= chunk_duration:
                return [file_path]

            chunks = []
            chunk_duration_ms = chunk_duration * 1000

            for i, start in enumerate(range(0, len(audio), chunk_duration_ms)):
                chunk = audio[start:start + chunk_duration_ms]
                
                # حفظ الجزء في ملف مؤقت
                temp_chunk = tempfile.NamedTemporaryFile(
                    suffix='.wav',
                    delete=False,
                    prefix=f'chunk_{i}_'
                )
                temp_chunk.close()
                
                chunk.export(
                    temp_chunk.name,
                    format='wav',
                    parameters=['-ar', '16000', '-ac', '1']
                )
                
                chunks.append(temp_chunk.name)
                self.temp_files.append(temp_chunk.name)

            return chunks

        except Exception as e:
            print(f"⚠️ فشل التقطيع: {e} - هنجرب الملف كله")
            return [file_path]

    def transcribe(
        self,
        file_path: str,
        language: str = None,
        progress_callback=None
    ) -> dict:
        """
        تحويل الصوت لنص (الدالة الرئيسية)
        
        Args:
            file_path: مسار الملف الصوتي
            language: كود اللغة (ar/en/None للاكتشاف التلقائي)
            progress_callback: دالة لتحديث التقدم
            
        Returns:
            dict: {
                'success': bool,
                'text': str,
                'language': str,
                'duration': float,
                'segments': list,
                'error': str
            }
        """
        result = {
            'success': False,
            'text': '',
            'language': language or 'auto',
            'duration': 0,
            'segments': [],
            'error': None,
            'processing_time': 0
        }

        start_time = time.time()

        try:
            # 1. التحقق من جاهزية النظام
            if not self.is_ready:
                result['error'] = self.error_message
                return result

            # 2. التحقق من وجود الملف
            if not os.path.exists(file_path):
                result['error'] = f"الملف مش موجود: {file_path}"
                return result

            # 3. التحقق من الصيغة
            ext = Path(file_path).suffix.lower()
            if ext not in self.SUPPORTED_FORMATS:
                result['error'] = (
                    f"صيغة '{ext}' مش مدعومة!\n"
                    f"الصيغ المدعومة: {', '.join(self.SUPPORTED_FORMATS.keys())}"
                )
                return result

            # 4. التحقق من الحجم
            file_size = os.path.getsize(file_path)
            if file_size > self.MAX_FILE_SIZE:
                size_mb = file_size / (1024 * 1024)
                result['error'] = (
                    f"الملف كبير جداً ({size_mb:.1f}MB)!\n"
                    f"الحد الأقصى: {self.MAX_FILE_SIZE // (1024*1024)}MB"
                )
                return result

            # 5. تحميل الموديل
            if progress_callback:
                progress_callback(0.1, "⏳ بيحمّل موديل Whisper...")
            
            if not self.load_model(progress_callback):
                result['error'] = self.error_message or "فشل تحميل الموديل"
                return result

            # 6. تحويل الصيغة لـ WAV
            if progress_callback:
                progress_callback(0.3, "🔄 بيحضّر الملف الصوتي...")

            converted_path = self._convert_to_wav(file_path)

            # 7. التحقق من المدة وتقطيع الملفات الطويلة
            audio_info = self.get_audio_info(converted_path)
            result['duration'] = audio_info.get('duration', 0)

            if progress_callback:
                duration_str = audio_info.get('duration_str', '??:??')
                progress_callback(0.4, f"🎵 مدة الملف: {duration_str} - بيحوّل...")

            # 8. التحويل للنص
            if (result['duration'] > self.MAX_CHUNK_DURATION and PYDUB_AVAILABLE):
                # ملف طويل - نقطعه
                text_parts = self._transcribe_long_audio(
                    converted_path,
                    language,
                    progress_callback
                )
                result['text'] = ' '.join(text_parts)
                result['success'] = bool(result['text'].strip())
            else:
                # ملف عادي - نحوله مباشرة
                transcription = self._transcribe_single(
                    converted_path,
                    language,
                    progress_callback
                )
                result['text'] = transcription.get('text', '')
                result['language'] = transcription.get('language', 'unknown')
                result['segments'] = transcription.get('segments', [])
                result['success'] = bool(result['text'].strip())

            # 9. تنظيف النص
            if result['text']:
                result['text'] = self._clean_text(result['text'])

            result['processing_time'] = round(time.time() - start_time, 1)

            if progress_callback:
                progress_callback(1.0, "✅ تم التحويل!")

        except Exception as e:
            result['error'] = f"خطأ غير متوقع: {str(e)}"
            result['processing_time'] = round(time.time() - start_time, 1)
            print(f"❌ Audio Reader Error: {traceback.format_exc()}")

        finally:
            # 10. حذف الملفات المؤقتة
            self._cleanup_temp_files()

        return result

    def _transcribe_single(
        self,
        file_path: str,
        language: str = None,
        progress_callback=None
    ) -> dict:
        """تحويل ملف صوتي واحد"""
        
        options = {
            'fp16': False,          # أكثر استقراراً
            'verbose': False,       # بدون output زيادة
        }

        # لو محدد لغة
        if language and language != 'auto':
            options['language'] = language
        
        if progress_callback:
            progress_callback(0.5, "🎙️ بيحوّل الكلام لنص...")

        result = self.model.transcribe(file_path, **options)

        if progress_callback:
            progress_callback(0.9, "✨ بيرتب النص...")

        return result

    def _transcribe_long_audio(
        self,
        file_path: str,
        language: str = None,
        progress_callback=None
    ) -> list:
        """تحويل ملف صوتي طويل (بالتقطيع)"""
        
        chunks = self._split_audio(file_path, chunk_duration=300)
        text_parts = []
        total_chunks = len(chunks)

        for i, chunk_path in enumerate(chunks):
            progress = 0.4 + (0.5 * (i / total_chunks))
            if progress_callback:
                progress_callback(
                    progress,
                    f"🎙️ بيحوّل الجزء {i+1} من {total_chunks}..."
                )

            try:
                options = {'fp16': False, 'verbose': False}
                if language and language != 'auto':
                    options['language'] = language

                result = self.model.transcribe(chunk_path, **options)
                text = result.get('text', '').strip()

                if text:
                    text_parts.append(text)

            except Exception as e:
                print(f"⚠️ فشل تحويل الجزء {i+1}: {e}")
                continue

        return text_parts

    def _clean_text(self, text: str) -> str:
        """تنظيف النص المحوّل"""
        if not text:
            return ""

        # إزالة مسافات زيادة
        import re
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        # إزالة تكرار النقاط
        text = re.sub(r'\.{3,}', '...', text)

        return text

    def _cleanup_temp_files(self):
        """حذف الملفات المؤقتة"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass  # مش مشكلة لو مفشلش الحذف
        self.temp_files = []

    def check_availability(self) -> dict:
        """
        التحقق من جاهزية النظام كله
        
        Returns:
            dict: حالة كل مكون
        """
        status = {
            'whisper': WHISPER_AVAILABLE,
            'pydub': PYDUB_AVAILABLE,
            'ffmpeg': self._check_ffmpeg(),
            'ready': self.is_ready,
            'error': self.error_message,
            'model': self.model_name,
            'model_loaded': self.model is not None
        }
        return status


# =====================================================
# دالة مساعدة للاستخدام السريع
# =====================================================
_audio_reader_instance = None

def get_audio_reader(model_name: str = 'base') -> AudioReader:
    """
    الحصول على instance واحد من AudioReader (Singleton)
    عشان مين حمّل الموديل مرة واحدة بس
    """
    global _audio_reader_instance
    
    if _audio_reader_instance is None or _audio_reader_instance.model_name != model_name:
        _audio_reader_instance = AudioReader(model_name=model_name)
    
    return _audio_reader_instance