"""
📤 PDF Exporter - مصدّر PDF احترافي بدعم كامل للعربي
يستخدم ReportLab + Arabic Reshaper + Python BiDi
"""
import os
import sys
import io
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# مكتبات PDF
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm, mm
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak,
        Table, TableStyle, Image, KeepTogether, Frame, PageTemplate
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# مكتبات العربي
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_AVAILABLE = True
except ImportError:
    ARABIC_AVAILABLE = False


class PDFExporter:
    """
    مصدّر PDF احترافي
    - دعم كامل للعربي (RTL)
    - تصميم احترافي بألوان
    - أقسام منفصلة (تلخيص، شرح، امتحان، بطاقات، خريطة)
    """

    # ─── إعدادات الألوان ───
    COLORS = {
        'primary':   HexColor('#667eea'),
        'secondary': HexColor('#764ba2'),
        'success':   HexColor('#11998e'),
        'success_light': HexColor('#38ef7d'),
        'danger':    HexColor('#f5576c'),
        'warning':   HexColor('#FFA500'),
        'info':      HexColor('#3498db'),
        'dark':      HexColor('#2c3e50'),
        'light':     HexColor('#ecf0f1'),
        'gray':      HexColor('#95a5a6'),
        'bg_light':  HexColor('#f8f9fa'),
        'border':    HexColor('#dee2e6'),
    }

    # ─── إعدادات الخط ───
    FONT_NAME = 'Amiri'
    FONT_NAME_BOLD = 'Amiri-Bold'

    # روابط تحميل الخط (Google Fonts)
    FONT_URLS = {
        'Amiri-Regular.ttf': 'https://github.com/aliftype/amiri/raw/master/fonts/Amiri-Regular.ttf',
        'Amiri-Bold.ttf':    'https://github.com/aliftype/amiri/raw/master/fonts/Amiri-Bold.ttf',
    }

    def __init__(self, fonts_dir: str = None):
        """
        تهيئة المصدّر

        Args:
            fonts_dir: فولدر الخطوط (اختياري)
        """
        if not REPORTLAB_AVAILABLE:
            raise ImportError(
                "مكتبة reportlab مش موجودة!\n"
                "ثبتها: pip install reportlab"
            )

        if not ARABIC_AVAILABLE:
            raise ImportError(
                "مكتبات العربي ناقصة!\n"
                "ثبتها: pip install arabic-reshaper python-bidi"
            )

        # تحديد فولدر الخطوط
        if fonts_dir is None:
            base_dir = Path(__file__).parent.parent
            fonts_dir = base_dir / 'assets' / 'fonts'

        self.fonts_dir = Path(fonts_dir)
        self.fonts_dir.mkdir(parents=True, exist_ok=True)

        # تحميل وتسجيل الخطوط
        self.fonts_ready = self._setup_fonts()

    # ─────────────────────────────────────────
    # إعداد الخطوط
    # ─────────────────────────────────────────
    def _setup_fonts(self) -> bool:
        """تحميل وتسجيل خطوط العربي"""
        try:
            # تحميل الخطوط لو مش موجودة
            for font_file, url in self.FONT_URLS.items():
                font_path = self.fonts_dir / font_file
                if not font_path.exists():
                    print(f"⏳ بيحمّل خط {font_file}...")
                    self._download_font(url, font_path)
                    print(f"✅ تم تحميل {font_file}")

            # تسجيل الخطوط في ReportLab
            regular_path = self.fonts_dir / 'Amiri-Regular.ttf'
            bold_path    = self.fonts_dir / 'Amiri-Bold.ttf'

            if regular_path.exists():
                pdfmetrics.registerFont(TTFont(self.FONT_NAME, str(regular_path)))

            if bold_path.exists():
                pdfmetrics.registerFont(TTFont(self.FONT_NAME_BOLD, str(bold_path)))

            return True

        except Exception as e:
            print(f"⚠️ مشكلة في إعداد الخطوط: {e}")
            return False

    def _download_font(self, url: str, save_path: Path):
        """تحميل خط من الإنترنت"""
        try:
            # User-Agent عشان GitHub مش يرفض الطلب
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                font_data = response.read()

            with open(save_path, 'wb') as f:
                f.write(font_data)

        except Exception as e:
            raise Exception(f"فشل تحميل الخط: {e}")

    # ─────────────────────────────────────────
    # معالجة النص العربي
    # ─────────────────────────────────────────
    def _fix_arabic(self, text: str) -> str:
        """
        إصلاح النص العربي للعرض الصحيح في PDF
        (reshape + bidi)
        """
        if not text:
            return ""

        text = str(text)

        try:
            # إعادة تشكيل الأحرف العربية
            reshaped = arabic_reshaper.reshape(text)
            # تطبيق خوارزمية BiDi (RTL)
            display_text = get_display(reshaped)
            return display_text
        except Exception:
            return text

    def _clean_text(self, text: str) -> str:
        """تنظيف النص من Markdown والرموز"""
        if not text:
            return ""

        # إزالة Markdown
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)      # italic
        text = re.sub(r'`(.+?)`', r'\1', text)        # code
        text = re.sub(r'#+\s*', '', text)             # headers
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # links
        text = re.sub(r'^\s*[-*]\s*', '• ', text, flags=re.MULTILINE)

        return text.strip()

    # ─────────────────────────────────────────
    # إنشاء الأنماط (Styles)
    # ─────────────────────────────────────────
    def _create_styles(self) -> Dict:
        """إنشاء أنماط النصوص"""
        font = self.FONT_NAME if self.fonts_ready else 'Helvetica'
        font_bold = self.FONT_NAME_BOLD if self.fonts_ready else 'Helvetica-Bold'

        styles = {
            'title': ParagraphStyle(
                name='ArabicTitle',
                fontName=font_bold,
                fontSize=24,
                textColor=self.COLORS['primary'],
                alignment=TA_CENTER,
                spaceAfter=20,
                leading=32,
            ),
            'subtitle': ParagraphStyle(
                name='ArabicSubtitle',
                fontName=font_bold,
                fontSize=18,
                textColor=self.COLORS['secondary'],
                alignment=TA_RIGHT,
                spaceAfter=15,
                spaceBefore=20,
                leading=24,
            ),
            'section_header': ParagraphStyle(
                name='SectionHeader',
                fontName=font_bold,
                fontSize=16,
                textColor=white,
                alignment=TA_RIGHT,
                spaceAfter=12,
                leading=22,
                backColor=self.COLORS['primary'],
                borderPadding=10,
                borderRadius=8,
            ),
            'body': ParagraphStyle(
                name='ArabicBody',
                fontName=font,
                fontSize=13,
                textColor=self.COLORS['dark'],
                alignment=TA_RIGHT,
                spaceAfter=10,
                leading=22,
                rightIndent=10,
                leftIndent=10,
                wordWrap='RTL',
            ),
            'body_bold': ParagraphStyle(
                name='ArabicBodyBold',
                fontName=font_bold,
                fontSize=13,
                textColor=self.COLORS['dark'],
                alignment=TA_RIGHT,
                spaceAfter=10,
                leading=22,
                wordWrap='RTL',
            ),
            'small': ParagraphStyle(
                name='ArabicSmall',
                fontName=font,
                fontSize=11,
                textColor=self.COLORS['gray'],
                alignment=TA_RIGHT,
                spaceAfter=6,
                leading=16,
                wordWrap='RTL',
            ),
            'center': ParagraphStyle(
                name='ArabicCenter',
                fontName=font,
                fontSize=12,
                textColor=self.COLORS['dark'],
                alignment=TA_CENTER,
                spaceAfter=10,
                leading=18,
                wordWrap='RTL',
            ),
            'info_box': ParagraphStyle(
                name='InfoBox',
                fontName=font,
                fontSize=12,
                textColor=self.COLORS['dark'],
                alignment=TA_RIGHT,
                spaceAfter=8,
                leading=18,
                backColor=self.COLORS['bg_light'],
                borderPadding=10,
                wordWrap='RTL',
            ),
            'success_box': ParagraphStyle(
                name='SuccessBox',
                fontName=font,
                fontSize=12,
                textColor=HexColor('#155724'),
                alignment=TA_RIGHT,
                spaceAfter=8,
                leading=18,
                backColor=HexColor('#d4edda'),
                borderPadding=10,
                wordWrap='RTL',
            ),
            'danger_box': ParagraphStyle(
                name='DangerBox',
                fontName=font,
                fontSize=12,
                textColor=HexColor('#721c24'),
                alignment=TA_RIGHT,
                spaceAfter=8,
                leading=18,
                backColor=HexColor('#f8d7da'),
                borderPadding=10,
                wordWrap='RTL',
            ),
            'footer': ParagraphStyle(
                name='Footer',
                fontName=font,
                fontSize=9,
                textColor=self.COLORS['gray'],
                alignment=TA_CENTER,
                leading=14,
            ),
        }
        return styles

    # ─────────────────────────────────────────
    # رسم Header & Footer
    # ─────────────────────────────────────────
    def _draw_header_footer(self, canvas, doc):
        """رسم Header و Footer لكل صفحة"""
        canvas.saveState()

        # ─── Header ───
        canvas.setFillColor(self.COLORS['primary'])
        canvas.rect(0, A4[1] - 1.5*cm, A4[0], 1.5*cm, fill=True, stroke=False)

        # عنوان في الـ Header
        canvas.setFillColor(white)
        font_b = self.FONT_NAME_BOLD if self.fonts_ready else 'Helvetica-Bold'
        canvas.setFont(font_b, 14)
        header_text = self._fix_arabic("🎓 المعلم الذكي - AI Teacher")
        canvas.drawCentredString(A4[0]/2, A4[1] - 1*cm, header_text)

        # ─── Footer ───
        canvas.setFillColor(self.COLORS['gray'])
        canvas.setFont(self.FONT_NAME if self.fonts_ready else 'Helvetica', 9)

        # رقم الصفحة (يسار)
        page_num = f"صفحة {doc.page}"
        page_num_ar = self._fix_arabic(page_num)
        canvas.drawString(2*cm, 1*cm, page_num_ar)

        # التاريخ (وسط)
        date_str = datetime.now().strftime("%Y-%m-%d")
        canvas.drawCentredString(A4[0]/2, 1*cm, date_str)

        # موقع (يمين)
        website = self._fix_arabic("المعلم الذكي v3.0 Pro")
        canvas.drawRightString(A4[0] - 2*cm, 1*cm, website)

        # خط فوق الـ Footer
        canvas.setStrokeColor(self.COLORS['border'])
        canvas.setLineWidth(0.5)
        canvas.line(2*cm, 1.5*cm, A4[0] - 2*cm, 1.5*cm)

        canvas.restoreState()

    # ─────────────────────────────────────────
    # بناء الأقسام
    # ─────────────────────────────────────────
    def _build_cover(self, title: str, file_info: Dict, styles: Dict) -> List:
        """صفحة الغلاف"""
        elements = []

        elements.append(Spacer(1, 3*cm))

        # شعار/أيقونة
        elements.append(Paragraph(
            self._fix_arabic("🎓"),
            ParagraphStyle(
                'icon',
                fontName=styles['title'].fontName,
                fontSize=80,
                alignment=TA_CENTER,
                spaceAfter=20,
            )
        ))

        # العنوان الرئيسي
        elements.append(Paragraph(
            self._fix_arabic("المعلم الذكي"),
            ParagraphStyle(
                'main_title',
                fontName=styles['title'].fontName,
                fontSize=36,
                textColor=self.COLORS['primary'],
                alignment=TA_CENTER,
                spaceAfter=10,
            )
        ))

        # العنوان الفرعي
        elements.append(Paragraph(
            self._fix_arabic("تقرير شامل"),
            ParagraphStyle(
                'sub_title',
                fontName=styles['title'].fontName,
                fontSize=20,
                textColor=self.COLORS['secondary'],
                alignment=TA_CENTER,
                spaceAfter=40,
            )
        ))

        # خط فاصل
        elements.append(Paragraph(
            "═" * 30,
            ParagraphStyle(
                'sep',
                fontSize=14,
                textColor=self.COLORS['primary'],
                alignment=TA_CENTER,
                spaceAfter=30,
            )
        ))

        # معلومات الملف
        if file_info:
            info_data = [
                ['القيمة', 'البيان'],
            ]

            if file_info.get('name'):
                info_data.append([
                    self._fix_arabic(file_info['name'][:50]),
                    self._fix_arabic('📄 اسم الملف')
                ])

            if file_info.get('size_readable'):
                info_data.append([
                    str(file_info['size_readable']),
                    self._fix_arabic('📦 الحجم')
                ])

            if file_info.get('extension'):
                info_data.append([
                    str(file_info['extension']),
                    self._fix_arabic('📁 النوع')
                ])

            info_data.append([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                self._fix_arabic('📅 تاريخ التقرير')
            ])

            font = self.FONT_NAME if self.fonts_ready else 'Helvetica'
            font_b = self.FONT_NAME_BOLD if self.fonts_ready else 'Helvetica-Bold'

            t = Table(info_data, colWidths=[10*cm, 6*cm])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['primary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), font_b),
                ('FONTNAME', (0, 1), (-1, -1), font),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, self.COLORS['border']),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1),
                 [white, self.COLORS['bg_light']]),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(t)

        elements.append(PageBreak())
        return elements

    def _build_section_header(self, title: str, icon: str = "") -> List:
        """عنوان قسم بتصميم جذاب"""
        elements = []
        font_b = self.FONT_NAME_BOLD if self.fonts_ready else 'Helvetica-Bold'

        header_data = [[
            self._fix_arabic(f"{icon} {title}")
        ]]

        t = Table(header_data, colWidths=[17*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, -1), white),
            ('FONTNAME', (0, 0), (-1, -1), font_b),
            ('FONTSIZE', (0, 0), (-1, -1), 18),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ]))

        elements.append(Spacer(1, 0.3*cm))
        elements.append(t)
        elements.append(Spacer(1, 0.5*cm))
        return elements

    def _build_text_section(self, text: str, styles: Dict) -> List:
        """قسم نصي عادي"""
        elements = []

        if not text:
            return elements

        # تنظيف النص
        text = self._clean_text(text)

        # تقسيم لفقرات
        paragraphs = text.split('\n')

        for para in paragraphs:
            para = para.strip()
            if not para:
                elements.append(Spacer(1, 0.2*cm))
                continue

            # معالجة عربي
            fixed = self._fix_arabic(para)
            elements.append(Paragraph(fixed, styles['body']))

        return elements

    def _build_summary_section(self, summary: str, styles: Dict) -> List:
        """قسم التلخيص"""
        elements = []
        elements.extend(self._build_section_header("التلخيص", "📝"))
        elements.extend(self._build_text_section(summary, styles))
        return elements

    def _build_explanation_section(self, explanation: str, styles: Dict) -> List:
        """قسم الشرح"""
        elements = []
        elements.extend(self._build_section_header("الشرح المفصل", "💡"))
        elements.extend(self._build_text_section(explanation, styles))
        return elements

    def _build_quiz_section(
        self,
        quiz_data: Dict,
        quiz_results: Dict,
        styles: Dict
    ) -> List:
        """قسم الامتحان"""
        elements = []
        elements.extend(self._build_section_header("الامتحان", "📋"))

        if not quiz_data or not quiz_data.get('questions'):
            elements.append(Paragraph(
                self._fix_arabic("لا توجد أسئلة"),
                styles['body']
            ))
            return elements

        questions = quiz_data['questions']
        qtype = quiz_data.get('type', 'mcq')

        for i, q in enumerate(questions):
            # السؤال
            q_text = q.get('question', q.get('statement', q.get('sentence', '')))
            elements.append(Paragraph(
                self._fix_arabic(f"السؤال {i+1}: {q_text}"),
                styles['body_bold']
            ))

            # الخيارات (لو MCQ)
            if qtype == 'mcq' and q.get('options'):
                for j, opt in enumerate(q['options']):
                    letter = ['أ', 'ب', 'ج', 'د'][j] if j < 4 else str(j+1)
                    elements.append(Paragraph(
                        self._fix_arabic(f"   {letter}) {opt}"),
                        styles['body']
                    ))

            # الإجابة الصحيحة
            correct = q.get('correct_answer', q.get('answer', ''))
            if qtype == 'true_false':
                correct = "صح ✓" if correct else "غلط ✗"
            elif qtype == 'mcq' and isinstance(correct, int) and q.get('options'):
                if correct < len(q['options']):
                    correct = q['options'][correct]

            if correct:
                elements.append(Paragraph(
                    self._fix_arabic(f"✅ الإجابة الصحيحة: {correct}"),
                    styles['success_box']
                ))

            # الشرح
            explanation = q.get('explanation', '')
            if explanation:
                elements.append(Paragraph(
                    self._fix_arabic(f"💬 الشرح: {explanation}"),
                    styles['info_box']
                ))

            elements.append(Spacer(1, 0.4*cm))

        return elements

    def _build_flashcards_section(
        self,
        flashcards: List[Dict],
        styles: Dict
    ) -> List:
        """قسم البطاقات"""
        elements = []
        elements.extend(self._build_section_header("بطاقات الحفظ", "🎴"))

        if not flashcards:
            elements.append(Paragraph(
                self._fix_arabic("لا توجد بطاقات"),
                styles['body']
            ))
            return elements

        font = self.FONT_NAME if self.fonts_ready else 'Helvetica'
        font_b = self.FONT_NAME_BOLD if self.fonts_ready else 'Helvetica-Bold'

        for i, card in enumerate(flashcards):
            q = card.get('question', '')
            a = card.get('answer', '')
            cat = card.get('category', 'عام')

            # جدول للبطاقة
            card_data = [
                [self._fix_arabic(f"بطاقة {i+1}"), self._fix_arabic(f"📂 {cat}")],
                [self._fix_arabic(f"❓ {q}"), ''],
                [self._fix_arabic(f"✅ {a}"), ''],
            ]

            t = Table(card_data, colWidths=[14*cm, 3*cm])
            t.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['primary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), font_b),
                ('FONTSIZE', (0, 0), (-1, 0), 12),

                # السؤال
                ('BACKGROUND', (0, 1), (-1, 1), HexColor('#fff9e6')),
                ('FONTNAME', (0, 1), (-1, 1), font_b),
                ('FONTSIZE', (0, 1), (-1, 1), 13),

                # الإجابة
                ('BACKGROUND', (0, 2), (-1, 2), HexColor('#e8f5e9')),
                ('FONTNAME', (0, 2), (-1, 2), font),
                ('FONTSIZE', (0, 2), (-1, 2), 12),

                # عام
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, self.COLORS['border']),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),

                # دمج خلايا الإجابة
                ('SPAN', (0, 1), (1, 1)),
                ('SPAN', (0, 2), (1, 2)),
            ]))

            elements.append(t)
            elements.append(Spacer(1, 0.3*cm))

        return elements

    def _build_mindmap_section(
        self,
        mindmap_data: Dict,
        mindmap_markdown: str,
        styles: Dict
    ) -> List:
        """قسم الخريطة الذهنية"""
        elements = []
        elements.extend(self._build_section_header("الخريطة الذهنية", "🧠"))

        if not mindmap_data:
            elements.append(Paragraph(
                self._fix_arabic("لا توجد خريطة"),
                styles['body']
            ))
            return elements

        # عرض كنص هرمي
        def render_node(node, level=0):
            items = []
            title = node.get('title', '')
            if title:
                indent = "    " * level
                prefix = "🎯 " if level == 0 else ("▸ " if level == 1 else "• ")

                style_to_use = styles['body_bold'] if level == 0 else styles['body']

                items.append(Paragraph(
                    self._fix_arabic(f"{indent}{prefix}{title}"),
                    style_to_use
                ))

            for child in node.get('children', []):
                items.extend(render_node(child, level + 1))

            return items

        elements.extend(render_node(mindmap_data))

        return elements

    # ─────────────────────────────────────────
    # دالة التصدير الرئيسية
    # ─────────────────────────────────────────
    def export(
        self,
        output_path: str = None,
        file_info: Dict = None,
        extracted_text: str = '',
        summary: str = '',
        explanation: str = '',
        quiz_data: Dict = None,
        quiz_results: Dict = None,
        flashcards: List = None,
        mindmap_data: Dict = None,
        mindmap_markdown: str = '',
        sections: List[str] = None
    ) -> Dict[str, Any]:
        """
        تصدير PDF شامل

        Args:
            output_path: مسار الحفظ (لو None هيرجع bytes)
            file_info: معلومات الملف
            extracted_text: النص الأصلي
            summary: التلخيص
            explanation: الشرح
            quiz_data: الامتحان
            quiz_results: نتائج الامتحان
            flashcards: البطاقات
            mindmap_data: الخريطة
            mindmap_markdown: نص الخريطة
            sections: الأقسام المطلوبة (default: all)

        Returns:
            {
                'success': bool,
                'pdf_bytes': bytes (لو مفيش output_path),
                'output_path': str,
                'pages': int,
                'error': str
            }
        """
        result = {
            'success': False,
            'pdf_bytes': None,
            'output_path': None,
            'pages': 0,
            'error': None
        }

        try:
            # تحديد المخرجات
            if output_path:
                buffer = output_path
            else:
                buffer = io.BytesIO()

            # إنشاء المستند
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2.5*cm,
                bottomMargin=2.5*cm,
                title="تقرير المعلم الذكي",
                author="AI Teacher",
            )

            # الأنماط
            styles = self._create_styles()

            # بناء المحتوى
            story = []

            # ─── الغلاف ───
            story.extend(self._build_cover(
                title="تقرير شامل",
                file_info=file_info or {},
                styles=styles
            ))

            # ─── الأقسام ───
            if sections is None:
                sections = ['summary', 'explanation', 'quiz', 'flashcards', 'mindmap']

            sections_added = 0

            if 'summary' in sections and summary:
                story.extend(self._build_summary_section(summary, styles))
                story.append(PageBreak())
                sections_added += 1

            if 'explanation' in sections and explanation:
                story.extend(self._build_explanation_section(explanation, styles))
                story.append(PageBreak())
                sections_added += 1

            if 'quiz' in sections and quiz_data:
                story.extend(self._build_quiz_section(
                    quiz_data, quiz_results or {}, styles
                ))
                story.append(PageBreak())
                sections_added += 1

            if 'flashcards' in sections and flashcards:
                story.extend(self._build_flashcards_section(flashcards, styles))
                story.append(PageBreak())
                sections_added += 1

            if 'mindmap' in sections and mindmap_data:
                story.extend(self._build_mindmap_section(
                    mindmap_data, mindmap_markdown, styles
                ))
                sections_added += 1

            # لو مفيش أقسام
            if sections_added == 0:
                story.append(Paragraph(
                    self._fix_arabic("⚠️ مفيش محتوى للتصدير"),
                    styles['body']
                ))
                story.append(Paragraph(
                    self._fix_arabic("ولّد تلخيص أو شرح أو امتحان أو بطاقات الأول"),
                    styles['body']
                ))

            # ─── البناء النهائي ───
            doc.build(
                story,
                onFirstPage=self._draw_header_footer,
                onLaterPages=self._draw_header_footer
            )

            result['pages'] = doc.page
            result['success'] = True

            if isinstance(buffer, io.BytesIO):
                buffer.seek(0)
                result['pdf_bytes'] = buffer.getvalue()
                buffer.close()
            else:
                result['output_path'] = output_path

        except Exception as e:
            import traceback
            result['error'] = f"{str(e)}\n{traceback.format_exc()}"
            print(f"❌ PDF Error: {result['error']}")

        return result

    # ─────────────────────────────────────────
    # دوال مساعدة
    # ─────────────────────────────────────────
    def check_availability(self) -> Dict[str, bool]:
        """التحقق من المتطلبات"""
        return {
            'reportlab': REPORTLAB_AVAILABLE,
            'arabic': ARABIC_AVAILABLE,
            'fonts_ready': self.fonts_ready,
            'all_ready': REPORTLAB_AVAILABLE and ARABIC_AVAILABLE and self.fonts_ready
        }