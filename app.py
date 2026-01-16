"""
نظام التنبؤ الذكي بأداء الطلاب - تصميم احترافي
تحويل من Gradio إلى Streamlit
"""

import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import numpy as np
import warnings
from pathlib import Path
from datetime import datetime
warnings.filterwarnings('ignore')

# ============================================================================
# 2. تهيئة الثوابت والإعدادات
# ============================================================================
class DesignConfig:
    COLORS = {
        'petroleum': '#006666',
        'petroleum_light': '#008787',
        'petroleum_dark': '#004d4d',
        'gold': '#D4AF37',
        'gold_light': '#E6C158',
        'gold_dark': '#B7950B',
        'white': '#FFFFFF',
        'gray_light': '#F8F9FA',
        'gray_medium': '#E9ECEF',
        'gray_dark': '#6C757D',
        'success': '#28A745',
        'warning': '#FFC107',
        'danger': '#DC3545',
        'info': '#17A2B8',
        'text': '#212529',  # لون النصوص الأساسي
        'text_secondary': '#6C757D',  # لون النصوص الثانوي
    }

# ============================================================================
# 3. تطبيق CSS محسن مع إصلاح النصوص البيضاء
# ============================================================================
def apply_custom_css():
    css = f"""
    <style>
    /* إعدادات عامة */
    .stApp {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['gray_light']} 0%, {DesignConfig.COLORS['white']} 100%);
        font-family: 'Tajawal', 'Helvetica Neue', Arial, sans-serif;
        direction: rtl;
        text-align: right;
    }}
    
    /* إصلاح: إظهار جميع النصوص باللون الداكن */
    * {{
        color: {DesignConfig.COLORS['text']} !important;
    }}
    
    .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader {{
        color: {DesignConfig.COLORS['text']} !important;
    }}
    
    .stMarkdown p, .stMarkdown li, .stMarkdown span {{
        color: {DesignConfig.COLORS['text']} !important;
    }}
    
    /* عناصر Streamlit الافتراضية */
    .css-1d391kg, .css-12oz5g7, .css-1v0mbdj {{
        color: {DesignConfig.COLORS['text']} !important;
    }}
    
    /* العناوين */
    h1, h2, h3, h4, h5, h6 {{
        color: {DesignConfig.COLORS['petroleum_dark']} !important;
        font-weight: 700 !important;
    }}
    
    /* الهيدر الرئيسي */
    .main-header {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum_dark']} 0%, {DesignConfig.COLORS['petroleum']} 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        color: {DesignConfig.COLORS['white']} !important;
    }}
    
    .main-header h1, .main-header p {{
        color: {DesignConfig.COLORS['white']} !important;
    }}
    
    /* البطاقات */
    .custom-card {{
        background: {DesignConfig.COLORS['white']};
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-right: 5px solid {DesignConfig.COLORS['gold']};
    }}
    
    /* أزرار */
    .stButton > button {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum']} 0%, {DesignConfig.COLORS['petroleum_dark']} 100%);
        color: {DesignConfig.COLORS['white']} !important;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 4px 12px rgba(0,102,102,0.3);
        transform: translateY(-2px);
    }}
    
    /* حقول الإدخال */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stSlider > div > div {{
        color: {DesignConfig.COLORS['text']} !important;
        background-color: {DesignConfig.COLORS['white']} !important;
        border-color: {DesignConfig.COLORS['gray_medium']} !important;
    }}
    
    .stSlider > div > div > div {{
        background: {DesignConfig.COLORS['gold']} !important;
    }}
    
    /* العلامات */
    .badge {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['gold']}15, {DesignConfig.COLORS['petroleum']}15);
        color: {DesignConfig.COLORS['petroleum_dark']} !important;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        display: inline-block;
        margin: 0.25rem;
        border: 1px solid rgba(212, 175, 55, 0.3);
    }}
    
    /* التنبيهات */
    .alert-box {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['info']}15, {DesignConfig.COLORS['petroleum']}15);
        border: 1px solid rgba(23, 162, 184, 0.3);
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }}
    
    /* الفوتر */
    .footer {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum_dark']} 0%, {DesignConfig.COLORS['petroleum']} 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-top: 3rem;
        text-align: center;
        color: {DesignConfig.COLORS['white']} !important;
    }}
    
    .footer p, .footer span {{
        color: {DesignConfig.COLORS['white']} !important;
    }}
    
    /* علامات التبويب */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: {DesignConfig.COLORS['text_secondary']} !important;
        border-radius: 0.5rem 0.5rem 0 0;
    }}
    
    .stTabs [aria-selected="true"] {{
        color: {DesignConfig.COLORS['petroleum']} !important;
        border-bottom: 3px solid {DesignConfig.COLORS['gold']} !important;
    }}
    
    /* المخططات */
    .stDataFrame, .stTable {{
        color: {DesignConfig.COLORS['text']} !important;
    }}
    
    /* الشريط الجانبي */
    section[data-testid="stSidebar"] {{
        background: {DesignConfig.COLORS['white']} !important;
        color: {DesignConfig.COLORS['text']} !important;
    }}
    
    section[data-testid="stSidebar"] * {{
        color: {DesignConfig.COLORS['text']} !important;
    }}
    
    /* النصوص الصغيرة */
    small {{
        color: {DesignConfig.COLORS['text_secondary']} !important;
    }}
    
    /* الروابط */
    a {{
        color: {DesignConfig.COLORS['petroleum']} !important;
    }}
    
    a:hover {{
        color: {DesignConfig.COLORS['petroleum_dark']} !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# 4. وظائف المساعدة
# ============================================================================
def setup_page_config():
    """إعداد إعدادات الصفحة"""
    st.set_page_config(
        page_title="نظام التنبؤ الذكي بأداء الطلاب",
        page_icon="🎓",
        layout="wide"
    )

def build_gauge(score, color):
    """بناء مؤشر سرعومتر أنيق"""
    rotation = (score / 100) * 180
    
    gauge_html = f"""
    <div style="position: relative; width: 300px; height: 150px; margin: 0 auto;">
        <div style="position: absolute; width: 100%; height: 100%; 
             border-radius: 150px 150px 0 0;
             background: conic-gradient(
                from 0deg,
                {DesignConfig.COLORS['danger']} 0deg,
                {DesignConfig.COLORS['warning']} 108deg,
                {DesignConfig.COLORS['success']} 180deg
             ); overflow: hidden;">
        </div>
        <div style="position: absolute; width: 70%; height: 70%; 
             background: {DesignConfig.COLORS['white']}; 
             border-radius: 50%; top: 15%; left: 15%;
             box-shadow: inset 0 4px 8px rgba(0,0,0,0.1);">
        </div>
        <div style="position: absolute; bottom: 0; left: 50%; 
             width: 4px; height: 70%; background: {color};
             transform-origin: bottom; transform: translateX(-50%) rotate({rotation - 90}deg);
             transition: transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);">
        </div>
        <div style="position: absolute; bottom: 40%; left: 50%; 
             transform: translateX(-50%); font-size: 2.5em; 
             font-weight: 700; color: {DesignConfig.COLORS['text']};">
             {score}
        </div>
    </div>
    
    <div style="display: flex; justify-content: center; gap: 30px; margin: 20px 0;">
        <div style="text-align: center;">
            <div style="width: 15px; height: 15px; background: {DesignConfig.COLORS['danger']}; 
                 border-radius: 50%; display: inline-block; margin-left: 5px;"></div>
            <span style="color: {DesignConfig.COLORS['text_secondary']};">ضعيف</span>
        </div>
        <div style="text-align: center;">
            <div style="width: 15px; height: 15px; background: {DesignConfig.COLORS['warning']}; 
                 border-radius: 50%; display: inline-block; margin-left: 5px;"></div>
            <span style="color: {DesignConfig.COLORS['text_secondary']};">جيد</span>
        </div>
        <div style="text-align: center;">
            <div style="width: 15px; height: 15px; background: {DesignConfig.COLORS['success']}; 
                 border-radius: 50%; display: inline-block; margin-left: 5px;"></div>
            <span style="color: {DesignConfig.COLORS['text_secondary']};">ممتاز</span>
        </div>
    </div>
    """
    return gauge_html

# ============================================================================
# 5. بناء الواجهة الأساسية
# ============================================================================
def build_header():
    """بناء الهيدر الرئيسي"""
    st.markdown("""
    <div class="main-header">
        <h1>🎓 نظام التنبؤ الذكي بأداء الطلاب</h1>
        <p>حل متكامل للتنبؤ الأكاديمي وتحليل البيانات التعليمية</p>
    </div>
    """, unsafe_allow_html=True)

def create_navigation():
    """شريط التنقل الجانبي"""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; 
         background: linear-gradient(135deg, #004d4d 0%, #006666 100%);
         border-radius: 0.75rem; color: white; margin-bottom: 2rem;">
        <h3 style="margin: 0;">🎓</h3>
        <p style="margin: 0.5rem 0 0 0;">نظام التنبؤ الذكي</p>
    </div>
    """, unsafe_allow_html=True)
    
    return st.sidebar.radio(
        "🔍 التنقل",
        ["🏠 الرئيسية", "🎯 أداة التنبؤ", "📈 تحليل البيانات", "📋 التقارير"],
        index=0
    )

# ============================================================================
# 6. الصفحات الرئيسية
# ============================================================================
def show_home_page():
    """الصفحة الرئيسية"""
    st.markdown('<div class="custom-card"><h2>🏠 نظرة عامة على النظام</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h4>🎯 المميزات الرئيسية</h4>
            <ul>
                <li>تنبؤ دقيق بالأداء الأكاديمي</li>
                <li>تحليل بيانات متقدم</li>
                <li>توصيات مخصصة للطلاب</li>
                <li>تقارير تفاعلية</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h4>📊 كيفية الاستخدام</h4>
            <ol>
                <li>اختر "أداة التنبؤ" من القائمة</li>
                <li>أدخل بيانات الطالب</li>
                <li>اضغط على "بدء التنبؤ"</li>
                <li>استعرض النتائج والتوصيات</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

def show_prediction_page():
    """صفحة التنبؤ"""
    st.markdown('<h2 style="color: #004d4d; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">🎯 أداة التنبؤ الذكي بالدرجات</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="alert-box"><p>أدخل البيانات المطلوبة للتنبؤ بالأداء الأكاديمي للطالب</p></div>', unsafe_allow_html=True)
    
    # علامات التبويب
    tab1, tab2, tab3 = st.tabs(["📊 إدخال البيانات", "📈 النتائج", "📋 التوصيات"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            hours_studied = st.slider(
                "ساعات الدراسة الأسبوعية",
                min_value=0,
                max_value=40,
                value=20,
                help="عدد الساعات التي يخصصها الطالب للدراسة أسبوعياً"
            )
            
            attendance_rate = st.slider(
                "نسبة الحضور (%)",
                min_value=0,
                max_value=100,
                value=85,
                help="نسبة حضور الطالب في المحاضرات والأنشطة التعليمية"
            )
        
        with col2:
            previous_scores = st.number_input(
                "متوسط الدرجات السابقة",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                help="متوسط أداء الطالب في الاختبارات السابقة"
            )
            
            tutoring_sessions = st.slider(
                "جلسات الدروس الخصوصية",
                min_value=0,
                max_value=10,
                value=2,
                help="عدد جلسات الدعم الإضافية الأسبوعية"
            )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 إعادة تعيين", use_container_width=True):
                st.session_state.clear()
        
        with col_btn2:
            predict_clicked = st.button("🚀 بدء التنبؤ", type="primary", use_container_width=True)
    
    with tab2:
        if 'prediction_result' in st.session_state:
            result = st.session_state.prediction_result
            st.markdown(f"""
            <div class="custom-card">
                <h3>📊 النتيجة التفصيلية</h3>
                <div style="text-align: center;">
                    {build_gauge(result['score'], result['color'])}
                </div>
                <div style="display: flex; justify-content: space-around; margin: 20px 0;">
                    <div>
                        <p style="color: #6C757D;">الدرجة النهائية</p>
                        <h3 style="color: {result['color']};">{result['score']}/100</h3>
                    </div>
                    <div>
                        <p style="color: #6C757D;">التقييم</p>
                        <h3 style="color: {result['color']};">{result['grade']}</h3>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("⏳ أدخل البيانات واضغط على 'بدء التنبؤ' لرؤية النتائج")
    
    with tab3:
        if 'prediction_result' in st.session_state:
            result = st.session_state.prediction_result
            st.markdown(f"""
            <div class="custom-card">
                <h3>📝 التوصيات</h3>
                <div class="alert-box">
                    <h4 style="color: {result['color']};">{result['feedback']}</h4>
                    <ul>
                        <li>زيادة ساعات الدراسة المنتظمة</li>
                        <li>تحسين نسبة الحضور</li>
                        <li>التركيز على المواد الضعيفة</li>
                        <li>الاستفادة من جلسات الدعم</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("⏳ انتظر نتائج التنبؤ لرؤية التوصيات المخصصة")
    
    return hours_studied, attendance_rate, previous_scores, tutoring_sessions, predict_clicked

def show_analysis_page():
    """صفحة تحليل البيانات"""
    st.markdown('<h2 style="color: #004d4d; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">📈 محلل البيانات المتقدم</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📁 رفع ملف بيانات (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            st.markdown(f"""
            <div class="custom-card">
                <h4>📊 معلومات الملف</h4>
                <p><strong>✅ تم تحميل الملف بنجاح</strong></p>
                <p>عدد الصفوف: <strong>{len(df):,}</strong></p>
                <p>عدد الأعمدة: <strong>{len(df.columns)}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["📋 عرض البيانات", "📊 الإحصائيات"])
            
            with tab1:
                st.dataframe(df.head(10), use_container_width=True)
            
            with tab2:
                st.write("### الإحصائيات الوصفية")
                st.dataframe(df.describe(), use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ حدث خطأ: {str(e)}")

def show_reports_page():
    """صفحة التقارير"""
    st.markdown('<h2 style="color: #004d4d; border-bottom: 2px solid #D4AF37; padding-bottom: 10px;">📋 التقارير والتحليلات</h2>', unsafe_allow_html=True)
    
    if os.path.exists("images") and os.listdir("images"):
        image_files = [f for f in os.listdir("images") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if image_files:
            cols = st.columns(3)
            for idx, img_file in enumerate(image_files[:6]):
                with cols[idx % 3]:
                    img_path = os.path.join("images", img_file)
                    try:
                        st.image(img_path, caption=img_file, use_column_width=True)
                    except:
                        st.error(f"تعذر تحميل: {img_file}")
        else:
            st.info("📭 لا توجد صور متاحة")
    else:
        st.info("📁 مجلد الصور غير موجود")

# ============================================================================
# 7. دالة التنبؤ
# ============================================================================
def predict_score(hours, attendance, prev_scores, tutoring):
    """دالة التنبؤ بالدرجة"""
    try:
        # تحميل النموذج
        model = joblib.load('regression_model.pkl')
        
        # إعداد البيانات (باستخدام قيم افتراضية للمتغيرات الناقصة)
        input_data = [[hours, attendance, prev_scores, tutoring, 3]]  # 3 هو قيمة افتراضية لتأثير الأقران
        
        score = round(model.predict(input_data)[0], 2)
        score = max(0, min(100, score))
        
        # تحديد التصنيف
        if score >= 90:
            color, feedback, grade = DesignConfig.COLORS['success'], "أداء استثنائي", "ممتاز"
        elif score >= 75:
            color, feedback, grade = DesignConfig.COLORS['info'], "أداء جيد جداً", "جيد جداً"
        elif score >= 60:
            color, feedback, grade = DesignConfig.COLORS['warning'], "أداء مقبول", "مقبول"
        else:
            color, feedback, grade = DesignConfig.COLORS['danger'], "أداء ضعيف", "ضعيف"
        
        # حفظ النتيجة
        st.session_state.prediction_result = {
            'score': score,
            'color': color,
            'feedback': feedback,
            'grade': grade
        }
        
        return True
        
    except Exception as e:
        st.error(f"❌ خطأ في التنبؤ: {str(e)}")
        return False

# ============================================================================
# 8. التطبيق الرئيسي
# ============================================================================
def main():
    """الدالة الرئيسية"""
    # إعداد الصفحة
    setup_page_config()
    apply_custom_css()
    
    # الهيدر
    build_header()
    
    # التنقل
    section = create_navigation()
    
    # عرض الصفحة المحددة
    if section == "🏠 الرئيسية":
        show_home_page()
    
    elif section == "🎯 أداة التنبؤ":
        hours, attendance, prev_scores, tutoring, predict_clicked = show_prediction_page()
        
        if predict_clicked:
            with st.spinner("🔍 جاري تحليل البيانات..."):
                predict_score(hours, attendance, prev_scores, tutoring)
                st.rerun()
    
    elif section == "📈 تحليل البيانات":
        show_analysis_page()
    
    elif section == "📋 التقارير":
        show_reports_page()
    
    # الفوتر
    st.markdown("""
    <div class="footer">
        <p>نظام التنبؤ الذكي بأداء الطلاب © 2024</p>
        <p>تم التطوير باستخدام Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# 9. بدء التشغيل
# ============================================================================
if __name__ == "__main__":
    # التحقق من وجود الملفات
    if not os.path.exists("regression_model.pkl"):
        st.warning("⚠️ ملف النموذج غير موجود")
    
    # تشغيل التطبيق
    main()
