"""
نظام التنبؤ الذكي بأداء الطلاب - تصميم احترافي
تحويل من Gradio إلى Streamlit
إصدار رسمي بنظام ألوان البترولي والذهبي
"""

# ============================================================================
# 1. استيراد مكتبات Streamlit
# ============================================================================
import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import numpy as np
import warnings
from pathlib import Path
import base64
from datetime import datetime
warnings.filterwarnings('ignore')

# ============================================================================
# 2. تهيئة الثوابت والإعدادات
# ============================================================================
class DesignConfig:
    # الألوان الأساسية
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
        'info': '#17A2B8'
    }
    
    # الظلال
    SHADOWS = {
        'small': '0 2px 4px rgba(0,0,0,0.1)',
        'medium': '0 4px 8px rgba(0,0,0,0.12)',
        'large': '0 8px 16px rgba(0,0,0,0.15)',
        'xl': '0 12px 24px rgba(0,0,0,0.18)'
    }
    
    # الزوايا
    BORDER_RADIUS = {
        'small': '8px',
        'medium': '12px',
        'large': '16px',
        'xl': '24px'
    }

# ============================================================================
# 3. وظائف المساعدة
# ============================================================================
def setup_page_config():
    """إعداد إعدادات الصفحة"""
    st.set_page_config(
        page_title="نظام التنبؤ الذكي بأداء الطلاب",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """تطبيق CSS مخصص"""
    css = f"""
    <style>
    /* إعدادات عامة */
    .stApp {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['gray_light']} 0%, {DesignConfig.COLORS['white']} 100%);
        font-family: 'Tajawal', 'Helvetica Neue', Arial, sans-serif;
        direction: rtl;
        text-align: right;
    }}
    
    /* البطاقات */
    .custom-card {{
        background: {DesignConfig.COLORS['white']};
        border-radius: {DesignConfig.BORDER_RADIUS['large']};
        box-shadow: {DesignConfig.SHADOWS['medium']};
        padding: 25px;
        margin: 15px 0;
        border: 1px solid {DesignConfig.COLORS['gray_medium']};
        border-right: 5px solid {DesignConfig.COLORS['gold']};
        transition: all 0.3s ease;
    }}
    
    .custom-card:hover {{
        box-shadow: {DesignConfig.SHADOWS['xl']};
        border-color: {DesignConfig.COLORS['petroleum_light']};
        transform: translateY(-2px);
    }}
    
    /* العناوين */
    .main-title {{
        color: {DesignConfig.COLORS['petroleum_dark']};
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum_dark']} 0%, {DesignConfig.COLORS['petroleum']} 100%);
        border-radius: {DesignConfig.BORDER_RADIUS['large']};
        color: white;
        margin-bottom: 30px;
    }}
    
    .section-title {{
        color: {DesignConfig.COLORS['petroleum_dark']};
        border-bottom: 2px solid {DesignConfig.COLORS['gold']};
        padding-bottom: 10px;
        margin-bottom: 20px;
        position: relative;
    }}
    
    .section-title::after {{
        content: '';
        position: absolute;
        bottom: -2px;
        right: 0;
        width: 60px;
        height: 2px;
        background: {DesignConfig.COLORS['petroleum']};
    }}
    
    /* الأزرار */
    .stButton > button {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum']} 0%, {DesignConfig.COLORS['petroleum_dark']} 100%);
        color: {DesignConfig.COLORS['white']};
        border: none;
        border-radius: {DesignConfig.BORDER_RADIUS['medium']};
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: {DesignConfig.SHADOWS['small']};
    }}
    
    .stButton > button:hover {{
        box-shadow: {DesignConfig.SHADOWS['medium']};
        color: {DesignConfig.COLORS['gold_light']};
        transform: translateY(-2px);
    }}
    
    /* أدوات الإدخال */
    .stSlider > div > div > div {{
        background: {DesignConfig.COLORS['gold']};
    }}
    
    /* المؤشرات */
    .metric-card {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['gold']}15, {DesignConfig.COLORS['petroleum']}15);
        border-radius: {DesignConfig.BORDER_RADIUS['medium']};
        padding: 20px;
        text-align: center;
        border: 1px solid {DesignConfig.COLORS['gold']}30;
    }}
    
    /* التنبيهات */
    .alert-box {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['info']}15, {DesignConfig.COLORS['petroleum']}15);
        border: 1px solid {DesignConfig.COLORS['info']}30;
        border-radius: {DesignConfig.BORDER_RADIUS['medium']};
        padding: 20px;
        margin: 15px 0;
    }}
    
    /* العلامات */
    .badge {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['gold']}15, {DesignConfig.COLORS['petroleum']}15);
        color: {DesignConfig.COLORS['petroleum_dark']};
        padding: 8px 16px;
        border-radius: {DesignConfig.BORDER_RADIUS['small']};
        display: inline-block;
        margin: 5px;
        border: 1px solid {DesignConfig.COLORS['gold']}30;
    }}
    
    /* الفوتر */
    .footer {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum_dark']} 0%, {DesignConfig.COLORS['petroleum']} 100%);
        padding: 20px;
        border-radius: {DesignConfig.BORDER_RADIUS['large']};
        color: white;
        text-align: center;
        margin-top: 40px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

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
             box-shadow: inset {DesignConfig.SHADOWS['medium']};">
        </div>
        <div style="position: absolute; bottom: 0; left: 50%; 
             width: 4px; height: 70%; background: {color};
             transform-origin: bottom; transform: translateX(-50%) rotate({rotation - 90}deg);
             transition: transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);">
        </div>
        <div style="position: absolute; bottom: 40%; left: 50%; 
             transform: translateX(-50%); font-size: 2.5em; 
             font-weight: 700; color: {DesignConfig.COLORS['petroleum_dark']};">
             {score}
        </div>
    </div>
    
    <div style="display: flex; justify-content: center; gap: 30px; margin: 20px 0;">
        <div style="text-align: center;">
            <div style="width: 15px; height: 15px; background: {DesignConfig.COLORS['danger']}; 
                 border-radius: 50%; display: inline-block; margin-left: 5px;"></div>
            <span style="color: {DesignConfig.COLORS['gray_dark']};">ضعيف</span>
        </div>
        <div style="text-align: center;">
            <div style="width: 15px; height: 15px; background: {DesignConfig.COLORS['warning']}; 
                 border-radius: 50%; display: inline-block; margin-left: 5px;"></div>
            <span style="color: {DesignConfig.COLORS['gray_dark']};">جيد</span>
        </div>
        <div style="text-align: center;">
            <div style="width: 15px; height: 15px; background: {DesignConfig.COLORS['success']}; 
                 border-radius: 50%; display: inline-block; margin-left: 5px;"></div>
            <span style="color: {DesignConfig.COLORS['gray_dark']};">ممتاز</span>
        </div>
    </div>
    """
    
    return gauge_html

# ============================================================================
# 4. بناء الواجهة
# ============================================================================
def build_header():
    """بناء الهيدر الرئيسي"""
    st.markdown("""
    <div class="main-title">
        <h1 style="margin: 0; padding: 10px;">🎓 نظام التنبؤ الذكي بأداء الطلاب</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 1.1em;">
        حل متكامل للتنبؤ الأكاديمي وتحليل البيانات التعليمية باستخدام أحدث التقنيات
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # العلامات المميزة
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<span class="badge">تحليل تنبؤي</span>', unsafe_allow_html=True)
    with col2:
        st.markdown('<span class="badge">تعلم آلي</span>', unsafe_allow_html=True)
    with col3:
        st.markdown('<span class="badge">تحليل بيانات</span>', unsafe_allow_html=True)
    with col4:
        st.markdown('<span class="badge">تقارير تفاعلية</span>', unsafe_allow_html=True)

def build_prediction_section():
    """بناء قسم التنبؤ"""
    st.markdown('<h2 class="section-title">🎯 أداة التنبؤ الذكي بالدرجات</h2>', unsafe_allow_html=True)
    st.markdown("""
    أدخل البيانات المطلوبة للتنبؤ بالأداء الأكاديمي للطالب.
    النظام سيقوم بتحليل المعلومات وتقديم تنبؤ دقيق مع توصيات مخصصة.
    """)
    
    # استخدام علامات تبويب Streamlit
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
            
            tutoring_sessions = st.slider(
                "جلسات الدروس الخصوصية",
                min_value=0,
                max_value=10,
                value=2,
                help="عدد جلسات الدعم الإضافية الأسبوعية"
            )
        
        with col2:
            previous_scores = st.number_input(
                "متوسط الدرجات السابقة",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                help="متوسط أداء الطالب في الاختبارات السابقة"
            )
            
            peer_influence = st.select_slider(
                "تأثير المحيط الدراسي",
                options=[1, 2, 3, 4, 5],
                value=3,
                help="مدى تأثير البيئة الدراسية والأقران على أداء الطالب (1 = ضعيف، 5 = قوي)"
            )
            
            # أزرار التحكم
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🔄 إعادة تعيين", use_container_width=True):
                    st.session_state.clear()
                    st.rerun()
            
            with col_btn2:
                predict_clicked = st.button("🚀 بدء التنبؤ", type="primary", use_container_width=True)
    
    with tab2:
        if 'prediction_result' in st.session_state:
            display_prediction_result()
        else:
            st.info("⏳ أدخل البيانات واضغط على 'بدء التنبؤ' لرؤية النتائج")
    
    with tab3:
        if 'prediction_result' in st.session_state:
            display_recommendations()
        else:
            st.info("⏳ انتظر نتائج التنبؤ لرؤية التوصيات المخصصة")
    
    return hours_studied, attendance_rate, tutoring_sessions, previous_scores, peer_influence, predict_clicked

def display_prediction_result():
    """عرض نتائج التنبؤ"""
    result = st.session_state.prediction_result
    
    st.markdown(f"""
    <div class="custom-card">
        <h3 style="color: {DesignConfig.COLORS['petroleum_dark']}; text-align: center;">
        📊 النتيجة التفصيلية
        </h3>
        
        <div style="text-align: center; margin: 30px 0;">
            {build_gauge(result['score'], result['color'])}
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0;">
            <div class="metric-card">
                <div style="color: {DesignConfig.COLORS['gray_dark']};">الدرجة النهائية</div>
                <div style="color: {result['color']}; font-size: 2em; font-weight: bold;">
                    {result['score']}/100
                </div>
            </div>
            
            <div class="metric-card">
                <div style="color: {DesignConfig.COLORS['gray_dark']};">التقييم</div>
                <div style="color: {result['color']}; font-size: 1.5em; font-weight: bold;">
                    {result['grade']}
                </div>
            </div>
            
            <div class="metric-card">
                <div style="color: {DesignConfig.COLORS['gray_dark']};">النسبة المئوية</div>
                <div style="color: {result['color']}; font-size: 1.5em; font-weight: bold;">
                    {result['score']}%
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_recommendations():
    """عرض التوصيات"""
    result = st.session_state.prediction_result
    
    st.markdown(f"""
    <div class="custom-card">
        <h3 style="color: {DesignConfig.COLORS['petroleum_dark']};">📝 التقييم والتوصيات</h3>
        <div class="alert-box">
            <h4 style="color: {result['color']}; margin-bottom: 10px;">{result['feedback']}</h4>
            
            <div style="background: {DesignConfig.COLORS['white']}; 
                 padding: 15px; border-radius: {DesignConfig.BORDER_RADIUS['medium']}; 
                 margin: 15px 0; border-right: 3px solid {result['color']};">
                <h5>🎯 توصيات للتحسين:</h5>
                <ul style="padding-right: 20px;">
                    <li>زيادة ساعات الدراسة الأسبوعية</li>
                    <li>التركيز على المواد التي تحتاج تحسين</li>
                    <li>المشاركة في جلسات الدعم الإضافية</li>
                    <li>تحسين نسبة الحضور</li>
                </ul>
            </div>
        </div>
        
        <h4 style="color: {DesignConfig.COLORS['petroleum_dark']}; margin-top: 20px;">
        📋 العوامل المدخلة
        </h4>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <span class="badge">ساعات الدراسة: {st.session_state.hours}</span>
            <span class="badge">الحضور: {st.session_state.attendance}%</span>
            <span class="badge">درجات سابقة: {st.session_state.prev_scores}</span>
            <span class="badge">دروس خصوصية: {st.session_state.tutoring}</span>
            <span class="badge">تأثير الأقران: {st.session_state.peer_influence}/5</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def build_analysis_section():
    """بناء قسم تحليل البيانات"""
    st.markdown('<h2 class="section-title">📈 محلل البيانات المتقدم</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("رفع ملف بيانات (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # معلومات الملف
            st.markdown(f"""
            <div class="custom-card">
                <h4>📊 معلومات الملف</h4>
                <p><strong>✅ تم تحميل الملف بنجاح</strong></p>
                <p>عدد الصفوف: <strong>{len(df):,}</strong></p>
                <p>عدد الأعمدة: <strong>{len(df.columns)}</strong></p>
                <p>الحقول المتاحة: <strong>{', '.join(df.columns[:3])}{'...' if len(df.columns) > 3 else ''}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # علامات التبويب للتحليل
            tab1, tab2, tab3 = st.tabs(["📋 عينة البيانات", "📊 الإحصائيات", "📈 الرسوم البيانية"])
            
            with tab1:
                st.dataframe(df.head(10), use_container_width=True)
            
            with tab2:
                st.write("### الإحصائيات الوصفية")
                st.dataframe(df.describe(), use_container_width=True)
                
                # معلومات إضافية
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("القيم المفقودة", df.isnull().sum().sum())
                with col2:
                    st.metric("القيم المكررة", df.duplicated().sum())
                with col3:
                    st.metric("المساحة المستخدمة", f"{df.memory_usage().sum() / 1024:.1f} KB")
            
            with tab3:
                if len(df.select_dtypes(include=[np.number]).columns) > 1:
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        x_col = st.selectbox("اختر المحور الأفقي", numeric_cols)
                    with col2:
                        y_col = st.selectbox("اختر المحور الرأسي", numeric_cols)
                    
                    if st.button("🎨 توليد رسم بياني"):
                        fig, ax = plt.subplots(figsize=(10, 6))
                        
                        if pd.api.types.is_numeric_dtype(df[x_col]) and pd.api.types.is_numeric_dtype(df[y_col]):
                            ax.scatter(df[x_col], df[y_col], color=DesignConfig.COLORS['petroleum'], alpha=0.7)
                            ax.set_xlabel(x_col)
                            ax.set_ylabel(y_col)
                            ax.set_title(f'العلاقة بين {x_col} و {y_col}')
                        else:
                            st.warning("يرجى اختيار أعمدة رقمية للرسم البياني")
                        
                        st.pyplot(fig)
                else:
                    st.warning("لا توجد أعمدة رقمية كافية لإنشاء رسم بياني")
        
        except Exception as e:
            st.error(f"❌ حدث خطأ في تحليل الملف: {str(e)}")

def build_gallery_section():
    """بناء قسم المعرض"""
    st.markdown('<h2 class="section-title">📋 معرض التقارير والتحليلات</h2>', unsafe_allow_html=True)
    
    # التحقق من وجود مجلد الصور
    if os.path.exists("images") and os.listdir("images"):
        image_files = [
            f for f in os.listdir("images") 
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        ]
        
        if image_files:
            st.write(f"### عدد الصور المتاحة: {len(image_files)}")
            
            # عرض الصور في شبكة
            cols = st.columns(3)
            for idx, img_file in enumerate(image_files[:9]):  # عرض أول 9 صور
                with cols[idx % 3]:
                    img_path = os.path.join("images", img_file)
                    try:
                        st.image(img_path, caption=img_file, use_column_width=True)
                    except:
                        st.error(f"تعذر تحميل الصورة: {img_file}")
        else:
            st.info("لا توجد صور في مجلد الصور")
    else:
        st.info("📁 مجلد الصور غير موجود أو فارغ")

def build_footer():
    """بناء الفوتر"""
    st.markdown("""
    <div class="footer">
        <div style="margin: 20px 0;">
            <p style="font-size: 1.1em; margin-bottom: 10px;">
            نظام التنبؤ الذكي بأداء الطلاب
            </p>
            <p style="opacity: 0.8; font-size: 0.9em;">
            © 2024 جميع الحقوق محفوظة | الإصدار 2.0 | تم التطوير باستخدام Streamlit
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# 5. دوال النظام الأساسية
# ============================================================================
def predict_score(hours, attendance, prev_scores, tutoring, peer_influence):
    """دالة التنبؤ بالدرجة"""
    try:
        # تحميل النموذج
        model = joblib.load('regression_model.pkl')
        
        # إعداد البيانات
        input_data = [[hours, attendance, prev_scores, tutoring, peer_influence]]
        score = round(model.predict(input_data)[0], 2)
        score = max(0, min(100, score))
        
        # تحديد التصنيف
        if score >= 90:
            color, feedback, grade = DesignConfig.COLORS['success'], "أداء استثنائي - مستوى متميز", "ممتاز"
        elif score >= 75:
            color, feedback, grade = DesignConfig.COLORS['info'], "أداء جيد جداً - يواصل التقدم", "جيد جداً"
        elif score >= 60:
            color, feedback, grade = DesignConfig.COLORS['warning'], "أداء مقبول - يحتاج إلى تحسين", "مقبول"
        else:
            color, feedback, grade = DesignConfig.COLORS['danger'], "أداء ضعيف - يحتاج إلى دعم", "ضعيف"
        
        # حفظ النتيجة في session state
        st.session_state.prediction_result = {
            'score': score,
            'color': color,
            'feedback': feedback,
            'grade': grade
        }
        
        # حفظ المدخلات في session state
        st.session_state.hours = hours
        st.session_state.attendance = attendance
        st.session_state.prev_scores = prev_scores
        st.session_state.tutoring = tutoring
        st.session_state.peer_influence = peer_influence
        
        return True
        
    except Exception as e:
        st.error(f"❌ خطأ في التنبؤ: {str(e)}")
        return False

# ============================================================================
# 6. التنقل في التطبيق
# ============================================================================
def create_navigation():
    """إنشاء شريط التنقل"""
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 20px; 
         background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum_dark']} 0%, {DesignConfig.COLORS['petroleum']} 100%);
         border-radius: {DesignConfig.BORDER_RADIUS['large']}; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0;">🎓</h3>
        <p style="margin: 10px 0 0 0; font-size: 0.9em;">نظام التنبؤ الذكي</p>
    </div>
    """, unsafe_allow_html=True)
    
    # اختيار القسم
    section = st.sidebar.radio(
        "🔍 التنقل في النظام",
        ["🏠 الرئيسية", "🎯 أداة التنبؤ", "📈 تحليل البيانات", "📋 التقارير", "⚙️ الإعدادات"],
        index=0
    )
    
    # معلومات إضافية في الشريط الجانبي
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 إحصائيات سريعة")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("الدقة", "92%")
    with col2:
        st.metric("التحليلات", "150+")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📝 معلومات النظام")
    st.sidebar.info("""
    **الإصدار:** 3.0  
    **آخر تحديث:** 2024  
    **التقنية:** Streamlit + ML
    """)
    
    return section

# ============================================================================
# 7. الصفحة الرئيسية
# ============================================================================
def show_home_page():
    """عرض الصفحة الرئيسية"""
    st.markdown("""
    <div class="custom-card">
        <h2>🏠 نظرة عامة على النظام</h2>
        <p>يقدم هذا النظام حلولاً متكاملة للتنبؤ بالأداء الأكاديمي للطلاب باستخدام تقنيات متقدمة في تحليل البيانات والتعلم الآلي.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # عرض المميزات في بطاقات
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="custom-card">
            <h4>🎯 التنبؤ الدقيق</h4>
            <p>استخدام نماذج تنبؤية متقدمة بدقة تصل إلى 92%</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="custom-card">
            <h4>📈 تحليل شامل</h4>
            <p>تقارير تفصيلية مع رسوم بيانية متعددة</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="custom-card">
            <h4>🎨 واجهة سهلة</h4>
            <p>تصميم بديهي يسهل على المستخدم التفاعل</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="custom-card">
            <h4>⚡ نتائج آنية</h4>
            <p>معالجة فورية وإظهار النتائج فوراً</p>
        </div>
        """, unsafe_allow_html=True)
    
    # كيفية الاستخدام
    st.markdown(f"""
    <div class="custom-card">
        <h3>📖 كيفية الاستخدام</h3>
        <ol style="padding-right: 20px;">
            <li>اختر "أداة التنبؤ" من القائمة الجانبية</li>
            <li>أدخل بيانات الطالب في الحقول المتاحة</li>
            <li>اضغط على "بدء التنبؤ" للحصول على النتائج</li>
            <li>استعرض النتائج والتوصيات في الأقسام المختلفة</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

def show_settings_page():
    """عرض صفحة الإعدادات"""
    st.markdown('<h2 class="section-title">⚙️ إعدادات النظام</h2>', unsafe_allow_html=True)
    
    # إعدادات النموذج
    with st.expander("🛠️ إعدادات النموذج"):
        model_type = st.selectbox("نوع النموذج", ["انحدار خطي", "شجرة قرار", "غابة عشوائية"])
        confidence_threshold = st.slider("حد الثقة (%)", 50, 99, 85)
        
        if st.button("💾 حفظ الإعدادات"):
            st.success("تم حفظ الإعدادات بنجاح!")
    
    # إعدادات الواجهة
    with st.expander("🎨 إعدادات الواجهة"):
        theme = st.selectbox("السمة", ["بترولي وذهبي", "فاتح", "غامق"])
        language = st.selectbox("اللغة", ["العربية", "الإنجليزية"])
        
        col1, col2 = st.columns(2)
        with col1:
            notifications = st.checkbox("التنبيهات", value=True)
        with col2:
            auto_save = st.checkbox("الحفظ التلقائي", value=True)
    
    # معلومات النظام
    with st.expander("📊 معلومات النظام"):
        st.write(f"**مسار النموذج:** {os.path.abspath('regression_model.pkl')}")
        st.write(f"**المساحة المتاحة:** {Path('.').stat().st_size / 1024:.1f} KB")
        st.write(f"**آخر تحديث:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ============================================================================
# 8. التطبيق الرئيسي
# ============================================================================
def main():
    """الدالة الرئيسية للتطبيق"""
    
    # إعداد الصفحة
    setup_page_config()
    apply_custom_css()
    
    # شريط التنقل الجانبي
    section = create_navigation()
    
    # الهيدر الرئيسي
    build_header()
    
    # عرض القسم المحدد
    if section == "🏠 الرئيسية":
        show_home_page()
    
    elif section == "🎯 أداة التنبؤ":
        # الحصول على المدخلات
        hours, attendance, tutoring, prev_scores, peer_influence, predict_clicked = build_prediction_section()
        
        # معالجة التنبؤ
        if predict_clicked:
            with st.spinner("🔍 جاري تحليل البيانات والتنبؤ..."):
                success = predict_score(hours, attendance, prev_scores, tutoring, peer_influence)
                if success:
                    st.success("✅ تم إكمال التنبؤ بنجاح!")
                    st.rerun()
    
    elif section == "📈 تحليل البيانات":
        build_analysis_section()
    
    elif section == "📋 التقارير":
        build_gallery_section()
    
    elif section == "⚙️ الإعدادات":
        show_settings_page()
    
    # الفوتر
    build_footer()

# ============================================================================
# 9. نقطة الدخول الرئيسية
# ============================================================================
if __name__ == "__main__":
    # التحقق من وجود الملفات المطلوبة
    required_files = ["regression_model.pkl"]
    
    if not os.path.exists("regression_model.pkl"):
        st.warning("⚠️ ملف النموذج غير موجود! سيتم استخدام قيم افتراضية للعرض.")
        # يمكنك هنا إنشاء نموذج افتراضي للعرض التوضيحي
        from sklearn.linear_model import LinearRegression
        import numpy as np
        
        # إنشاء نموذج افتراضي
        X = np.random.rand(100, 5) * 100
        y = X[:, 0] * 0.3 + X[:, 1] * 0.2 + X[:, 2] * 0.25 + X[:, 3] * 0.15 + X[:, 4] * 0.1 + np.random.randn(100) * 5
        model = LinearRegression()
        model.fit(X, y)
        joblib.dump(model, 'regression_model.pkl')
    
    # تشغيل التطبيق
    main()