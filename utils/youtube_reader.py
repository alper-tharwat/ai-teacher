"""
📺 قارئ فيديوهات YouTube
بيحول أي فيديو يوتيوب لنص قابل للتلخيص والشرح
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import tempfile
from config import Config


class YouTubeReader:
    """
    قارئ فيديوهات YouTube الذكي
    
    المميزات:
    - استخراج معلومات الفيديو
    - تحميل الترجمة لو موجودة (أسرع)
    - تحويل الصوت لنص باستخدام Whisper (لو مفيش ترجمة)
    - دعم اللغة العربية والإنجليزية
    - معالجة الفيديوهات الطويلة
    """
    
    def __init__(self):
        """تهيئة القارئ"""
        self.whisper_model = None
        self.whisper_loaded = False
    
    # ============================================
    # 🔍 استخراج معلومات الفيديو
    # ============================================
    
    def extract_video_id(self, url):
        """
        استخراج ID الفيديو من اللينك
        
        Args:
            url: لينك يوتيوب
        
        Returns:
            str: ID الفيديو أو None
        """
        if not url:
            return None
        
        # أنماط مختلفة للينكات يوتيوب
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # youtube.com/watch?v=ID
            r'(?:embed\/)([0-9A-Za-z_-]{11})',   # youtube.com/embed/ID
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',  # youtu.be/ID
            r'(?:shorts\/)([0-9A-Za-z_-]{11})',  # youtube.com/shorts/ID
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def get_video_info(self, url):
        """
        الحصول على معلومات الفيديو
        
        Args:
            url: لينك الفيديو
        
        Returns:
            dict: معلومات الفيديو
        """
        try:
            import yt_dlp
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'success': True,
                    'video_id': info.get('id'),
                    'title': info.get('title', 'بدون عنوان'),
                    'channel': info.get('channel', 'غير معروف'),
                    'duration': info.get('duration', 0),
                    'duration_formatted': self._format_duration(info.get('duration', 0)),
                    'thumbnail': info.get('thumbnail'),
                    'description': info.get('description', '')[:500],
                    'views': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', ''),
                    'language': info.get('language', 'unknown')
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': f"❌ خطأ في قراءة الفيديو: {str(e)}"
            }
    
    # ============================================
    # 📝 الحصول على النص (الطريقة الأولى - الترجمة)
    # ============================================
    
    def get_transcript(self, url, languages=['ar', 'en']):
        """
        الحصول على نص الفيديو من الترجمة (أسرع طريقة)
        
        Args:
            url: لينك الفيديو
            languages: اللغات المفضلة بالترتيب
        
        Returns:
            dict: النتيجة
        """
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            from youtube_transcript_api._errors import (
                TranscriptsDisabled,
                NoTranscriptFound,
                VideoUnavailable
            )
            
            video_id = self.extract_video_id(url)
            if not video_id:
                return {
                    'success': False,
                    'error': '❌ لينك يوتيوب غير صحيح'
                }
            
            # محاولة الحصول على الترجمة
            try:
                # محاولة اللغات المفضلة
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                
                transcript = None
                used_language = None
                
                # محاولة كل لغة
                for lang in languages:
                    try:
                        transcript = transcript_list.find_transcript([lang])
                        used_language = lang
                        break
                    except:
                        continue
                
                # لو مفيش، خد أي ترجمة متاحة
                if not transcript:
                    try:
                        transcript = transcript_list.find_manually_created_transcript()
                        used_language = transcript.language_code
                    except:
                        # خد أول ترجمة تلقائية
                        transcript = list(transcript_list)[0]
                        used_language = transcript.language_code
                
                # تحميل الترجمة
                transcript_data = transcript.fetch()
                
                # تجميع النص
                full_text = ""
                for entry in transcript_data:
                    full_text += entry['text'] + " "
                
                full_text = full_text.strip()
                
                return {
                    'success': True,
                    'text': full_text,
                    'method': 'transcript',
                    'language': used_language,
                    'is_auto': transcript.is_generated,
                    'word_count': len(full_text.split()),
                    'char_count': len(full_text)
                }
            
            except TranscriptsDisabled:
                return {
                    'success': False,
                    'error': '⚠️ الترجمة معطلة في الفيديو ده',
                    'use_whisper': True
                }
            except NoTranscriptFound:
                return {
                    'success': False,
                    'error': '⚠️ مفيش ترجمة متاحة، هنحاول نحول الصوت لنص',
                    'use_whisper': True
                }
            
        except ImportError:
            return {
                'success': False,
                'error': '❌ المكتبة مش متثبتة. شغل: pip install youtube-transcript-api'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'❌ خطأ: {str(e)}',
                'use_whisper': True
            }
    
    # ============================================
    # 🎤 الحصول على النص (الطريقة الثانية - Whisper)
    # ============================================
    
    def download_audio(self, url, output_path=None):
        """
        تحميل صوت الفيديو
        
        Args:
            url: لينك الفيديو
            output_path: مسار الحفظ
        
        Returns:
            dict: مسار الملف
        """
        try:
            import yt_dlp
            
            if not output_path:
                output_path = os.path.join(
                    Config.TEMP_DIR,
                    f"yt_audio_{self.extract_video_id(url)}"
                )
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_path + '.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '128',
                }],
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            audio_file = output_path + '.mp3'
            
            if os.path.exists(audio_file):
                return {
                    'success': True,
                    'audio_path': audio_file,
                    'size_mb': os.path.getsize(audio_file) / (1024 * 1024)
                }
            else:
                return {
                    'success': False,
                    'error': '❌ مقدرتش أحمل الصوت'
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'❌ خطأ في تحميل الصوت: {str(e)}'
            }
    
    def transcribe_with_whisper(self, audio_path, language='ar'):
        """
        تحويل الصوت لنص باستخدام Whisper
        
        Args:
            audio_path: مسار ملف الصوت
            language: اللغة (ar/en)
        
        Returns:
            dict: النص
        """
        try:
            # تحميل Whisper لو مش محمل
            if not self.whisper_loaded:
                self._load_whisper()
            
            if not self.whisper_model:
                return {
                    'success': False,
                    'error': '❌ مقدرش أحمل Whisper'
                }
            
            # تحويل الصوت لنص
            result = self.whisper_model.transcribe(
                audio_path,
                language=language,
                fp16=False
            )
            
            return {
                'success': True,
                'text': result['text'],
                'language': result.get('language', language),
                'method': 'whisper',
                'word_count': len(result['text'].split()),
                'char_count': len(result['text']),
                'segments': result.get('segments', [])
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'❌ خطأ في Whisper: {str(e)}'
            }
    
    def _load_whisper(self):
        """تحميل موديل Whisper"""
        try:
            import whisper
            print("⏳ جاري تحميل Whisper (المرة الأولى تاخد وقت)...")
            
            # نستخدم الموديل الصغير عشان السرعة
            # الموديلات: tiny, base, small, medium, large
            self.whisper_model = whisper.load_model("base")
            self.whisper_loaded = True
            print("✅ Whisper جاهز!")
        except Exception as e:
            print(f"❌ خطأ في تحميل Whisper: {e}")
            self.whisper_model = None
    
    # ============================================
    # 🎯 الدالة الرئيسية
    # ============================================
    
    def read_video(self, url, prefer_transcript=True):
        """
        قراءة الفيديو واستخراج النص
        
        Args:
            url: لينك الفيديو
            prefer_transcript: استخدم الترجمة لو متاحة (أسرع)
        
        Returns:
            dict: النتيجة الكاملة
        """
        # 1. الحصول على معلومات الفيديو
        video_info = self.get_video_info(url)
        
        if not video_info.get('success'):
            return video_info
        
        # 2. محاولة الحصول على الترجمة
        if prefer_transcript:
            transcript_result = self.get_transcript(url)
            
            if transcript_result.get('success'):
                return {
                    'success': True,
                    'video_info': video_info,
                    'text': transcript_result['text'],
                    'method': 'transcript',
                    'language': transcript_result.get('language'),
                    'word_count': transcript_result.get('word_count'),
                    'message': '✅ تم استخراج النص من الترجمة (سريع)'
                }
        
        # 3. لو مفيش ترجمة، استخدم Whisper
        print("📥 جاري تحميل الصوت...")
        audio_result = self.download_audio(url)
        
        if not audio_result.get('success'):
            return audio_result
        
        print("🎤 جاري تحويل الصوت لنص (يحتاج وقت)...")
        transcribe_result = self.transcribe_with_whisper(
            audio_result['audio_path'],
            language='ar'
        )
        
        # حذف ملف الصوت بعد الانتهاء
        try:
            os.remove(audio_result['audio_path'])
        except:
            pass
        
        if transcribe_result.get('success'):
            return {
                'success': True,
                'video_info': video_info,
                'text': transcribe_result['text'],
                'method': 'whisper',
                'language': transcribe_result.get('language'),
                'word_count': transcribe_result.get('word_count'),
                'message': '✅ تم تحويل الصوت لنص باستخدام Whisper'
            }
        
        return {
            'success': False,
            'error': '❌ فشل في استخراج النص من الفيديو'
        }
    
    # ============================================
    # 🔧 أدوات مساعدة
    # ============================================
    
    @staticmethod
    def _format_duration(seconds):
        """تحويل الثواني لصيغة مقروءة"""
        if not seconds:
            return "غير معروف"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
    @staticmethod
    def is_valid_youtube_url(url):
        """التحقق من صحة لينك يوتيوب"""
        if not url:
            return False
        
        patterns = [
            r'^https?://(?:www\.)?youtube\.com/watch\?v=',
            r'^https?://(?:www\.)?youtube\.com/embed/',
            r'^https?://(?:www\.)?youtube\.com/shorts/',
            r'^https?://youtu\.be/',
        ]
        
        return any(re.match(pattern, url) for pattern in patterns)