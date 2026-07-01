"""
🔐 Supabase Client - اتصال قاعدة البيانات والتسجيل
"""

import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_supabase_client() -> Client:
    """
    إنشاء client للاتصال بـ Supabase
    @st.cache_resource = يتعمل مرة واحدة بس
    """
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        
        if not url or not key:
            return None
        
        client = create_client(url, key)
        return client
    
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال بـ Supabase: {str(e)}")
        return None


def test_connection() -> dict:
    """
    اختبار الاتصال بـ Supabase
    """
    try:
        client = get_supabase_client()
        
        if not client:
            return {
                "success": False,
                "message": "❌ لم يتم إنشاء الـ Client"
            }
        
        # جرب نقرأ من جدول (ولو فاضي)
        response = client.table("user_files").select("id").limit(1).execute()
        
        return {
            "success": True,
            "message": "✅ الاتصال بـ Supabase ناجح!",
            "data": response
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ فشل الاتصال: {str(e)}"
        }