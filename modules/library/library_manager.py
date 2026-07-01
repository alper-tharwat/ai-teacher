"""
📚 Library Manager - مدير المكتبة
يتعامل مع books_database.json
"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class LibraryManager:
    """مدير المكتبة - إضافة/حذف/قراءة الكتب"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.db_path = self.base_dir / "books_database.json"
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        """التأكد من وجود قاعدة البيانات"""
        if not self.db_path.exists():
            default_db = {
                "metadata": {
                    "version": "1.0",
                    "last_updated": datetime.now().strftime("%Y-%m-%d"),
                    "total_books": 0
                },
                "stages": {}
            }
            self._save_database(default_db)

    def _load_database(self) -> Dict:
        """قراءة قاعدة البيانات"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ خطأ في قراءة المكتبة: {e}")
            return {"metadata": {}, "stages": {}}

    def _save_database(self, data: Dict) -> bool:
        """حفظ قاعدة البيانات"""
        try:
            # تحديث آخر تعديل
            if "metadata" in data:
                data["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                data["metadata"]["total_books"] = self._count_books(data)

            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ خطأ في الحفظ: {e}")
            return False

    def _count_books(self, data: Dict) -> int:
        """عد إجمالي الكتب"""
        count = 0
        for stage_data in data.get("stages", {}).values():
            for grade_data in stage_data.get("grades", {}).values():
                for subject_books in grade_data.get("subjects", {}).values():
                    count += len(subject_books)
        return count

    # ═══════════════════════════════════════════
    # 📖 القراءة (للمستخدم)
    # ═══════════════════════════════════════════

    def get_all_stages(self) -> List[Dict]:
        """جلب كل المراحل"""
        data = self._load_database()
        stages = []
        for name, info in data.get("stages", {}).items():
            stages.append({
                "name": name,
                "icon": info.get("icon", "📚"),
                "description": info.get("description", ""),
                "grades_count": len(info.get("grades", {}))
            })
        return stages

    def get_grades(self, stage: str) -> List[str]:
        """جلب السنوات الدراسية لمرحلة معينة"""
        data = self._load_database()
        stage_data = data.get("stages", {}).get(stage, {})
        return list(stage_data.get("grades", {}).keys())

    def get_subjects(self, stage: str, grade: str) -> List[str]:
        """جلب المواد لسنة معينة"""
        data = self._load_database()
        grade_data = data.get("stages", {}).get(stage, {}).get("grades", {}).get(grade, {})
        return list(grade_data.get("subjects", {}).keys())

    def get_books(self, stage: str, grade: str, subject: str) -> List[Dict]:
        """جلب الكتب لمادة معينة"""
        data = self._load_database()
        return (
            data.get("stages", {})
            .get(stage, {})
            .get("grades", {})
            .get(grade, {})
            .get("subjects", {})
            .get(subject, [])
        )

    def get_book_by_id(self, book_id: str) -> Optional[Dict]:
        """البحث عن كتاب بالـ ID"""
        data = self._load_database()
        for stage_name, stage_data in data.get("stages", {}).items():
            for grade_name, grade_data in stage_data.get("grades", {}).items():
                for subject_name, books in grade_data.get("subjects", {}).items():
                    for book in books:
                        if book.get("id") == book_id:
                            return {
                                **book,
                                "stage": stage_name,
                                "grade": grade_name,
                                "subject": subject_name
                            }
        return None

    def get_statistics(self) -> Dict:
        """إحصائيات المكتبة"""
        data = self._load_database()
        stats = {
            "total_books": 0,
            "total_stages": 0,
            "total_grades": 0,
            "total_subjects": 0,
            "by_stage": {}
        }

        stages = data.get("stages", {})
        stats["total_stages"] = len(stages)

        for stage_name, stage_data in stages.items():
            stage_books = 0
            grades = stage_data.get("grades", {})
            stats["total_grades"] += len(grades)

            for grade_data in grades.values():
                subjects = grade_data.get("subjects", {})
                stats["total_subjects"] += len(subjects)

                for books in subjects.values():
                    stage_books += len(books)

            stats["by_stage"][stage_name] = stage_books
            stats["total_books"] += stage_books

        return stats

    # ═══════════════════════════════════════════
    # ✏️ التعديل (للأدمن فقط)
    # ═══════════════════════════════════════════

    def add_book(
        self,
        stage: str,
        grade: str,
        subject: str,
        title: str,
        url: str,
        author: str = "",
        year: int = 2024,
        description: str = ""
    ) -> Dict:
        """إضافة كتاب جديد"""
        try:
            data = self._load_database()

            # التأكد من وجود المرحلة
            if stage not in data.get("stages", {}):
                return {"success": False, "error": f"المرحلة '{stage}' غير موجودة"}

            # التأكد من وجود السنة
            if grade not in data["stages"][stage].get("grades", {}):
                return {"success": False, "error": f"السنة '{grade}' غير موجودة"}

            # إنشاء المادة لو مش موجودة
            grade_data = data["stages"][stage]["grades"][grade]
            if "subjects" not in grade_data:
                grade_data["subjects"] = {}

            if subject not in grade_data["subjects"]:
                grade_data["subjects"][subject] = []

            # إنشاء ID فريد
            book_id = f"{stage}_{grade}_{subject}_{len(grade_data['subjects'][subject]) + 1}"
            book_id = book_id.replace(" ", "_")

            # إضافة الكتاب
            new_book = {
                "id": book_id,
                "title": title,
                "url": url,
                "author": author,
                "year": year,
                "description": description,
                "added_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            grade_data["subjects"][subject].append(new_book)

            # حفظ
            if self._save_database(data):
                return {"success": True, "book_id": book_id, "book": new_book}
            else:
                return {"success": False, "error": "فشل الحفظ"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_book(self, book_id: str) -> Dict:
        """حذف كتاب بالـ ID"""
        try:
            data = self._load_database()

            for stage_name, stage_data in data.get("stages", {}).items():
                for grade_name, grade_data in stage_data.get("grades", {}).items():
                    for subject_name, books in grade_data.get("subjects", {}).items():
                        for i, book in enumerate(books):
                            if book.get("id") == book_id:
                                deleted = books.pop(i)

                                # حذف المادة لو فاضية
                                if not books:
                                    del grade_data["subjects"][subject_name]

                                if self._save_database(data):
                                    return {"success": True, "deleted": deleted}
                                else:
                                    return {"success": False, "error": "فشل الحفظ"}

            return {"success": False, "error": "الكتاب غير موجود"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_book(self, book_id: str, updates: Dict) -> Dict:
        """تعديل بيانات كتاب"""
        try:
            data = self._load_database()

            for stage_data in data.get("stages", {}).values():
                for grade_data in stage_data.get("grades", {}).values():
                    for books in grade_data.get("subjects", {}).values():
                        for book in books:
                            if book.get("id") == book_id:
                                # تحديث الحقول
                                allowed_fields = ["title", "url", "author", "year", "description"]
                                for field in allowed_fields:
                                    if field in updates:
                                        book[field] = updates[field]

                                book["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

                                if self._save_database(data):
                                    return {"success": True, "book": book}
                                else:
                                    return {"success": False, "error": "فشل الحفظ"}

            return {"success": False, "error": "الكتاب غير موجود"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def add_subject(self, stage: str, grade: str, subject: str) -> Dict:
        """إضافة مادة جديدة"""
        try:
            data = self._load_database()

            if stage not in data.get("stages", {}):
                return {"success": False, "error": f"المرحلة '{stage}' غير موجودة"}

            if grade not in data["stages"][stage].get("grades", {}):
                return {"success": False, "error": f"السنة '{grade}' غير موجودة"}

            grade_data = data["stages"][stage]["grades"][grade]
            if "subjects" not in grade_data:
                grade_data["subjects"] = {}

            if subject in grade_data["subjects"]:
                return {"success": False, "error": f"المادة '{subject}' موجودة بالفعل"}

            grade_data["subjects"][subject] = []

            if self._save_database(data):
                return {"success": True}
            else:
                return {"success": False, "error": "فشل الحفظ"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_subject(self, stage: str, grade: str, subject: str) -> Dict:
        """حذف مادة (وكل كتبها)"""
        try:
            data = self._load_database()

            subjects = (
                data.get("stages", {})
                .get(stage, {})
                .get("grades", {})
                .get(grade, {})
                .get("subjects", {})
            )

            if subject not in subjects:
                return {"success": False, "error": "المادة غير موجودة"}

            del subjects[subject]

            if self._save_database(data):
                return {"success": True}
            else:
                return {"success": False, "error": "فشل الحفظ"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    # ═══════════════════════════════════════════
    # 🔍 البحث
    # ═══════════════════════════════════════════

    def search_books(self, query: str) -> List[Dict]:
        """البحث في الكتب"""
        if not query or not query.strip():
            return []

        query = query.strip().lower()
        results = []
        data = self._load_database()

        for stage_name, stage_data in data.get("stages", {}).items():
            for grade_name, grade_data in stage_data.get("grades", {}).items():
                for subject_name, books in grade_data.get("subjects", {}).items():
                    for book in books:
                        # البحث في العنوان والمؤلف والوصف
                        searchable_text = " ".join([
                            book.get("title", ""),
                            book.get("author", ""),
                            book.get("description", ""),
                            subject_name,
                            grade_name,
                            stage_name
                        ]).lower()

                        if query in searchable_text:
                            results.append({
                                **book,
                                "stage": stage_name,
                                "grade": grade_name,
                                "subject": subject_name
                            })

        return results