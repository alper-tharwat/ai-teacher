"""
🔑 مدير المفاتيح الذكي
بيدير عدة مفاتيح Gemini ويبدّل بينهم تلقائياً
"""
import os
import sys
import json
import time
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config


class KeyManager:
    """
    مدير المفاتيح المتعددة
    
    المميزات:
    - بدائل تلقائي للمفاتيح
    - تتبع المفاتيح المستنفذة
    - استرجاع المفاتيح بعد 24 ساعة
    - إحصائيات الاستخدام
    - حفظ الحالة بين الجلسات
    """
    
    def __init__(self):
        """تهيئة المدير"""
        self.keys = self._load_valid_keys()
        self.state_path = Config.KEYS_STATE_PATH
        self.state = self._load_state()
        self.current_index = self._get_best_key_index()
    
    # ============================================
    # 📦 تحميل المفاتيح
    # ============================================
    
    def _load_valid_keys(self):
        """تحميل المفاتيح الصحيحة فقط"""
        valid_keys = []
        for i, key in enumerate(Config.GEMINI_API_KEYS):
            if key and key.startswith("AIza") and "XXXX" not in key:
                valid_keys.append({
                    'id': i,
                    'key': key,
                    'short': f"{key[:10]}...{key[-4:]}"  # للعرض الآمن
                })
        return valid_keys
    
    # ============================================
    # 💾 إدارة الحالة
    # ============================================
    
    def _load_state(self):
        """تحميل حالة المفاتيح المحفوظة"""
        if os.path.exists(self.state_path):
            try:
                with open(self.state_path, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # تنظيف المفاتيح المستنفذة القديمة (بعد 24 ساعة)
                now = datetime.now().isoformat()
                for key_id in list(state.get('exhausted_keys', {}).keys()):
                    exhausted_at = datetime.fromisoformat(
                        state['exhausted_keys'][key_id]['exhausted_at']
                    )
                    if datetime.now() - exhausted_at > timedelta(hours=24):
                        del state['exhausted_keys'][key_id]
                
                return state
            except Exception as e:
                print(f"خطأ في تحميل حالة المفاتيح: {e}")
        
        return self._default_state()
    
    def _default_state(self):
        """الحالة الافتراضية"""
        return {
            'exhausted_keys': {},  # المفاتيح المستنفذة
            'usage_stats': {},     # إحصائيات الاستخدام
            'last_used_key': 0,    # آخر مفتاح مستخدم
            'total_requests': 0    # إجمالي الطلبات
        }
    
    def _save_state(self):
        """حفظ الحالة"""
        try:
            os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
            with open(self.state_path, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ حالة المفاتيح: {e}")
    
    # ============================================
    # 🎯 الحصول على المفتاح
    # ============================================
    
    def _get_best_key_index(self):
        """الحصول على أحسن مفتاح متاح"""
        if not self.keys:
            return -1
        
        # البحث عن مفتاح غير مستنفذ
        for i, key_info in enumerate(self.keys):
            key_id = str(key_info['id'])
            if key_id not in self.state.get('exhausted_keys', {}):
                return i
        
        # كل المفاتيح مستنفذة - نرجع الأول (يمكن يكون رجع للحياة)
        return 0
    
    def get_current_key(self):
        """الحصول على المفتاح الحالي"""
        if not self.keys:
            return None
        
        if 0 <= self.current_index < len(self.keys):
            return self.keys[self.current_index]['key']
        return None
    
    def get_current_key_info(self):
        """معلومات المفتاح الحالي"""
        if not self.keys or self.current_index < 0:
            return None
        
        key_info = self.keys[self.current_index]
        key_id = str(key_info['id'])
        
        return {
            'index': self.current_index,
            'short': key_info['short'],
            'requests': self.state.get('usage_stats', {}).get(key_id, 0),
            'is_exhausted': key_id in self.state.get('exhausted_keys', {}),
            'total_keys': len(self.keys),
            'available_keys': self._count_available_keys()
        }
    
    def _count_available_keys(self):
        """عدد المفاتيح المتاحة"""
        exhausted = set(self.state.get('exhausted_keys', {}).keys())
        return len([k for k in self.keys if str(k['id']) not in exhausted])
    
    # ============================================
    # 🔄 تبديل المفاتيح
    # ============================================
    
    def switch_to_next_key(self, reason="quota_exceeded"):
        """
        التبديل للمفتاح التالي
        
        Args:
            reason: سبب التبديل
        
        Returns:
            bool: نجح التبديل أم لا
        """
        if not self.keys:
            return False
        
        # تعليم المفتاح الحالي كمستنفذ
        current_key_info = self.keys[self.current_index]
        key_id = str(current_key_info['id'])
        
        self.state.setdefault('exhausted_keys', {})[key_id] = {
            'exhausted_at': datetime.now().isoformat(),
            'reason': reason
        }
        
        # البحث عن المفتاح التالي المتاح
        original_index = self.current_index
        attempts = 0
        
        while attempts < len(self.keys):
            self.current_index = (self.current_index + 1) % len(self.keys)
            attempts += 1
            
            next_key_id = str(self.keys[self.current_index]['id'])
            if next_key_id not in self.state['exhausted_keys']:
                # لقينا مفتاح متاح
                self.state['last_used_key'] = self.current_index
                self._save_state()
                return True
        
        # كل المفاتيح مستنفذة
        self.current_index = original_index
        self._save_state()
        return False
    
    # ============================================
    # 📊 الإحصائيات
    # ============================================
    
    def record_request(self, success=True):
        """تسجيل طلب"""
        if self.current_index < 0:
            return
        
        key_id = str(self.keys[self.current_index]['id'])
        
        # إحصائيات الاستخدام
        if 'usage_stats' not in self.state:
            self.state['usage_stats'] = {}
        
        self.state['usage_stats'][key_id] = \
            self.state['usage_stats'].get(key_id, 0) + 1
        
        # إجمالي الطلبات
        self.state['total_requests'] = \
            self.state.get('total_requests', 0) + 1
        
        self._save_state()
    
    def get_statistics(self):
        """الحصول على إحصائيات شاملة"""
        total_keys = len(self.keys)
        exhausted = len(self.state.get('exhausted_keys', {}))
        available = total_keys - exhausted
        
        stats = {
            'total_keys': total_keys,
            'available_keys': available,
            'exhausted_keys': exhausted,
            'total_requests': self.state.get('total_requests', 0),
            'current_key': self.get_current_key_info(),
            'keys_details': []
        }
        
        # تفاصيل كل مفتاح
        for key_info in self.keys:
            key_id = str(key_info['id'])
            is_exhausted = key_id in self.state.get('exhausted_keys', {})
            requests = self.state.get('usage_stats', {}).get(key_id, 0)
            
            status = "🔴 مستنفذ" if is_exhausted else "🟢 متاح"
            
            stats['keys_details'].append({
                'id': key_info['id'],
                'short': key_info['short'],
                'status': status,
                'requests': requests,
                'is_current': key_info['id'] == self.keys[self.current_index]['id']
            })
        
        return stats
    
    # ============================================
    # 🧹 إدارة الحالة
    # ============================================
    
    def reset_exhausted_keys(self):
        """إعادة تعيين المفاتيح المستنفذة (للاختبار)"""
        self.state['exhausted_keys'] = {}
        self.current_index = 0
        self._save_state()
        return True
    
    def reset_all_stats(self):
        """إعادة تعيين كل الإحصائيات"""
        self.state = self._default_state()
        self.current_index = 0
        self._save_state()
        return True
    
    def has_available_keys(self):
        """التحقق من وجود مفاتيح متاحة"""
        return self._count_available_keys() > 0
    
    def is_ready(self):
        """التحقق من جاهزية النظام"""
        return len(self.keys) > 0 and self.has_available_keys()