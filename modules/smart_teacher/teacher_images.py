"""
🖼️ محرك الصور التوضيحية من Pixabay
"""

import requests
import json


PIXABAY_API_KEY = "56482640-85070cbc0a7cf3d97c355bac8"
PIXABAY_BASE_URL = "https://pixabay.com/api/"


def search_images(query: str, count: int = 3, lang: str = "ar") -> list:
    """
    البحث عن صور توضيحية
    
    Args:
        query: كلمة البحث
        count: عدد الصور المطلوبة
        lang: لغة البحث (ar, en, fr, etc)
    
    Returns:
        list of dicts: [{"url": str, "thumb": str, "tags": str, "user": str}]
    """
    try:
        params = {
            "key": PIXABAY_API_KEY,
            "q": query,
            "lang": lang,
            "image_type": "photo",
            "orientation": "horizontal",
            "safesearch": "true",
            "per_page": max(count, 3),  # Pixabay minimum is 3
            "order": "popular"
        }
        
        response = requests.get(PIXABAY_BASE_URL, params=params, timeout=10)
        
        if response.status_code != 200:
            # محاولة بالإنجليزية لو العربي مرجعش حاجة
            if lang != "en":
                return search_images(query, count, "en")
            return []
        
        data = response.json()
        hits = data.get("hits", [])
        
        if not hits and lang != "en":
            return search_images(query, count, "en")
        
        images = []
        for hit in hits[:count]:
            images.append({
                "url": hit.get("webformatURL", ""),
                "thumb": hit.get("previewURL", ""),
                "large": hit.get("largeImageURL", ""),
                "tags": hit.get("tags", ""),
                "user": hit.get("user", "Pixabay"),
                "page_url": hit.get("pageURL", "")
            })
        
        return images
    
    except Exception as e:
        print(f"خطأ في جلب الصور: {e}")
        return []


def get_images_for_point(ai_engine, point_title: str, point_content: str) -> dict:
    """
    استخدام AI لاقتراح كلمات بحث ثم جلب الصور
    
    Returns:
        {"keywords": [...], "images": [{...}, {...}]}
    """
    
    prompt = f"""
عندي نقطة في درس وعايز أجيب صور توضيحية ليها من Pixabay.

عنوان النقطة: {point_title}
محتوى النقطة: {point_content[:500]}

المطلوب: اقترحلي 3 كلمات بحث (search keywords) باللغة الإنجليزية فقط 
(لأن Pixabay بيشتغل أفضل بالإنجليزي).

الكلمات لازم تكون:
- محددة وواضحة (مش عامة)
- مناسبة للموضوع
- بترجع صور حقيقية ومفيدة
- كل كلمة بحث من 1-3 كلمات بالكتير

مثال:
لو الموضوع عن الزراعة في مصر، الكلمات تكون:
["egyptian farmer", "wheat field", "nile river agriculture"]

أرجع JSON فقط بدون أي نص إضافي:
{{
    "keywords": ["keyword1", "keyword2", "keyword3"]
}}
"""
    
    try:
        response = ai_engine.answer_question(context="", question=prompt)
        
        # تنظيف الرد
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        # استخراج JSON
        start = response.find("{")
        end = response.rfind("}") + 1
        if start != -1 and end > start:
            result = json.loads(response[start:end])
            keywords = result.get("keywords", [])
        else:
            keywords = [point_title]
        
    except Exception as e:
        keywords = [point_title]
    
    # جلب الصور
    all_images = []
    used_keywords = []
    
    for keyword in keywords[:3]:
        images = search_images(keyword, count=1, lang="en")
        if images:
            all_images.extend(images)
            used_keywords.append(keyword)
        if len(all_images) >= 3:
            break
    
    return {
        "keywords": used_keywords,
        "images": all_images[:3]
    }


def get_quick_images(query: str, count: int = 3) -> list:
    """جلب سريع للصور بدون AI"""
    # محاولة بالعربي الأول
    images = search_images(query, count, "ar")
    if not images:
        images = search_images(query, count, "en")
    return images