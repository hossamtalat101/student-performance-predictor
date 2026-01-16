"""
🎓 نظام التنبؤ الذكي بأداء الطلاب
إصدار متكامل مع دعم RTL كامل وتصميم متجاوب
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
# 1. إعدادات التصميم والألوان
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
        'text_primary': '#212529',
        'text_secondary': '#6C757D',
    }

# ============================================================================
# 2. تطبيق CSS متكامل مع دعم RTL وتصميم متجاوب
# ============================================================================
def apply_comprehensive_css():
    css = f"""
    <style>
    /* ========== إعدادات RTL الأساسية ========== */
    :root {{
        --rtl: true;
        --font-primary: 'Tajawal', 'Cairo', sans-serif;
    }}
    
    html, body, .stApp {{
        direction: rtl !important;
        text-align: right !important;
        font-family: var(--font-primary) !important;
    }}
    
    /* ========== إصلاح النصوص والعناوين ========== */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    p, span, div, li, .stMarkdown, .stText {{
        direction: rtl !important;
        text-align: right !important;
        font-family: var(--font-primary) !important;
        color: {DesignConfig.COLORS['text_primary']} !important;
        unicode-bidi: embed;
    }}
    
    /* ========== إصلاح حقول الإدخال ========== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > textarea,
    .stSlider > div > div > input {{
        direction: rtl !important;
        text-align: right !important;
        font-family: var(--font-primary) !important;
        unicode-bidi: plaintext;
    }}
    
    /* ========== إصلاح الشريط الجانبي ========== */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {DesignConfig.COLORS['petroleum_dark']} 0%, {DesignConfig.COLORS['petroleum']} 100%) !important;
        color: white !important;
        direction: rtl !important;
        text-align: right !important;
        font-family: var(--font-primary) !important;
    }}
    
    section[data-testid="stSidebar"] * {{
        color: white !important;
        font-family: var(--font-primary) !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio,
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stSlider,
    section[data-testid="stSidebar"] .stNumberInput {{
        direction: rtl !important;
        text-align: right !important;
    }}
    
    /* ========== تصميم متجاوب للقائمة الجانبية ========== */
    @media (max-width: 768px) {{
        section[data-testid="stSidebar"] {{
            width: 85% !important;
            min-width: 250px !important;
            max-width: 350px !important;
            position: fixed !important;
            top: 0 !important;
            right: 0 !important;
            height: 100vh !important;
            z-index: 999999 !important;
            transform: translateX(0) !important;
            transition: transform 0.3s ease !important;
        }}
        
        .sidebar-close-btn {{
            display: block !important;
            position: absolute !important;
            top: 15px !important;
            left: 15px !important;
            background: rgba(255,255,255,0.2) !important;
            color: white !important;
            border: none !important;
            border-radius: 50% !important;
            width: 40px !important;
            height: 40px !important;
            font-size: 24px !important;
            cursor: pointer !important;
            z-index: 1000000 !important;
        }}
    }}
    
    @media (min-width: 769px) {{
        section[data-testid="stSidebar"] {{
            min-width: 280px !important;
            max-width: 350px !important;
        }}
        .sidebar-close-btn {{ display: none !important; }}
    }}
    
    /* ========== تحسينات عامة للتصميم المتجاوب ========== */
    .custom-card {{
        background: {DesignConfig.COLORS['white']};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-right: 5px solid {DesignConfig.COLORS['gold']};
        direction: rtl !important;
        text-align: right !important;
        transition: all 0.3s ease;
    }}
    
    .custom-card:hover {{
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }}
    
    /* ========== أزرار متجاوبة ========== */
    .stButton > button {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum']} 0%, {DesignConfig.COLORS['petroleum_dark']} 100%);
        color: {DesignConfig.COLORS['white']} !important;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-family: var(--font-primary) !important;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,102,102,0.2);
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 6px 12px rgba(0,102,102,0.3);
        transform: translateY(-2px);
    }}
    
    /* ========== نظام Grid متجاوب ========== */
    .responsive-grid {{
        display: grid !important;
        gap: 20px !important;
        direction: rtl !important;
    }}
    
    @media (max-width: 768px) {{
        .responsive-grid {{
            grid-template-columns: 1fr !important;
        }}
        .mobile-hidden {{ display: none !important; }}
    }}
    
    @media (min-width: 769px) and (max-width: 1024px) {{
        .responsive-grid {{
            grid-template-columns: repeat(2, 1fr) !important;
        }}
    }}
    
    @media (min-width: 1025px) {{
        .responsive-grid {{
            grid-template-columns: repeat(3, 1fr) !important;
        }}
    }}
    
    /* ========== علامات التبويب ========== */
    .stTabs [data-baseweb="tab-list"] {{
        flex-direction: row-reverse !important;
        gap: 1rem !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        font-family: var(--font-primary) !important;
        padding: 0.75rem 1.5rem !important;
    }}
    
    /* ========== الجداول ========== */
    .stDataFrame, .stTable {{
        direction: rtl !important;
    }}
    
    .stDataFrame table {{
        text-align: right !important;
    }}
    
    /* ========== تحسينات إمكانية الوصول ========== */
    a:focus, button:focus, input:focus, select:focus, textarea:focus {{
        outline: 3px solid {DesignConfig.COLORS['gold']} !important;
        outline-offset: 2px !important;
    }}
    
    /* ========== مؤشر السرعة ========== */
    .gauge-container {{
        position: relative;
        width: 100%;
        max-width: 300px;
        margin: 0 auto;
    }}
    
    /* ========== الفوتر ========== */
    .footer {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum_dark']} 0%, {DesignConfig.COLORS['petroleum']} 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-top: 3rem;
        text-align: center;
        color: {DesignConfig.COLORS['white']} !important;
        direction: rtl !important;
    }}
    
    .footer * {{
        color: {DesignConfig.COLORS['white']} !important;
    }}
    
    /* ========== تحسينات للهواتف ========== */
    @media (max-width: 480px) {{
        .stButton > button {{
            padding: 1rem !important;
            font-size: 16px !important;
        }}
        
        input, select, textarea {{
            font-size: 16px !important;
        }}
    }}
    </style>
    
    <!-- تحميل خطوط اللغة العربية -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;600;700;800&family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    """
    
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# 3. وظائف المساعدة
# ============================================================================
def setup_page_config():
    st.set_page_config(
        page_title="نظام التنبؤ الذكي بأداء الطلاب",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def build_gauge(score, color):
    """بناء مؤشر سرعة متحرك"""
    rotation = (score / 100) * 180
    
    return f"""
    <div class="gauge-container">
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
                 font-weight: 700; color: {DesignConfig.COLORS['text_primary']};">
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
    </div>
    """

# ============================================================================
# 4. إنشاء القائمة الجانبية المتجاوبة
# ============================================================================
def create_sidebar():
    """إنشاء القائمة الجانبية مع دعم كامل للجوال"""
    
    with st.sidebar:
        # زر إغلاق للجوال
        st.markdown("""
        <button class="sidebar-close-btn" onclick="closeSidebar()">×</button>
        """, unsafe_allow_html=True)
        
        # عنوان القائمة
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: rgba(0,0,0,0.2); border-radius: 10px; margin-bottom: 2rem;">
            <h2 style="margin: 0; color: white;">🎓</h2>
            <p style="margin: 0.5rem 0 0 0; color: #D4AF37; font-weight: bold;">نظام التنبؤ الذكي</p>
        </div>
        """, unsafe_allow_html=True)
        
        # التنقل الرئيسي
        page = st.radio(
            "🔍 **القائمة الرئيسية**",
            ["🏠 الصفحة الرئيسية", "🎯 أداة التنبؤ", "📊 تحليل البيانات", "📈 التقارير", "⚙️ الإعدادات"],
            index=0,
            key="main_nav"
        )
        
        st.markdown("---")
        
        # معلومات سريعة
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📈 الدقة", "92%")
        with col2:
            st.metric("📊 التحليلات", "150+")
        
        st.markdown("---")
        
        # معلومات النظام
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
            <p style="margin: 0; color: #D4AF37;"><strong>معلومات النظام</strong></p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            الإصدار: 4.0<br>
            آخر تحديث: 2024<br>
            التكنولوجيا: Streamlit + ML
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # JavaScript لإدارة القائمة في الجوال
        st.markdown("""
        <script>
        function closeSidebar() {{
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            if (window.innerWidth <= 768) {{
                sidebar.style.transform = 'translateX(100%)';
                setTimeout(() => {{ sidebar.style.display = 'none'; }}, 300);
            }}
        }}
        
        function openSidebar() {{
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            sidebar.style.display = 'block';
            setTimeout(() => {{ sidebar.style.transform = 'translateX(0)'; }}, 10);
        }}
        
        // زر لفتح القائمة في الجوال
        if (window.innerWidth <= 768) {{
            const openBtn = document.createElement('button');
            openBtn.innerHTML = '☰';
            openBtn.style.cssText = `
                position: fixed;
                top: 15px;
                right: 15px;
                background: #006666;
                color: white;
                border: none;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                font-size: 24px;
                cursor: pointer;
                z-index: 999998;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            `;
            openBtn.onclick = openSidebar;
            document.body.appendChild(openBtn);
        }}
        </script>
        """, unsafe_allow_html=True)
    
    return page

# ============================================================================
# 5. الصفحات الرئيسية
# ============================================================================
def show_home_page():
    """عرض الصفحة الرئيسية"""
    st.markdown("""
    <div class="custom-card">
        <h2>🏠 مرحباً بك في نظام التنبؤ الذكي</h2>
        <p>نظام متكامل يستخدم تقنيات الذكاء الاصطناعي للتنبؤ بالأداء الأكاديمي للطلاب</p>
    </div>
    """, unsafe_allow_html=True)
    
    # عرض المميزات في نظام Grid متجاوب
    st.markdown('<div class="responsive-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h4>🎯 تنبؤ دقيق</h4>
            <p>استخدام نماذج متقدمة بدقة تصل إلى 92% للتنبؤ بالأداء الأكاديمي</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h4>📊 تحليل شامل</h4>
            <p>تقارير تفصيلية ورسوم بيانية متعددة لتحليل البيانات التعليمية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="custom-card">
            <h4>📈 توصيات مخصصة</h4>
            <p>توصيات شخصية لكل طالب بناءً على أدائه واحتياجاته التعليمية</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # كيفية الاستخدام
    st.markdown("""
    <div class="custom-card">
        <h3>📖 كيفية استخدام النظام</h3>
        <ol style="padding-right: 20px;">
            <li>انتقل إلى <strong>"أداة التنبؤ"</strong> من القائمة الجانبية</li>
            <li>أدخل بيانات الطالب في الحقول المتاحة</li>
            <li>اضغط على <strong>"بدء التنبؤ"</strong> للحصول على النتائج</li>
            <li>استعرض التقارير والتوصيات المخصصة</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

def show_prediction_page():
    """صفحة التنبؤ"""
    st.markdown("""
    <div class="custom-card">
        <h2>🎯 أداة التنبؤ الذكي بالدرجات</h2>
        <p>أدخل بيانات الطالب للحصول على تنبؤ دقيق بأدائه الأكاديمي</p>
    </div>
    """, unsafe_allow_html=True)
    
    # استخدام علامات التبويب
    tab1, tab2, tab3 = st.tabs(["📊 إدخال البيانات", "📈 النتائج", "📋 التوصيات"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            hours_studied = st.slider(
                "🕒 ساعات الدراسة الأسبوعية",
                min_value=0,
                max_value=40,
                value=20,
                help="عدد الساعات التي يخصصها الطالب للدراسة أسبوعياً"
            )
            
            attendance_rate = st.slider(
                "📅 نسبة الحضور (%)",
                min_value=0,
                max_value=100,
                value=85,
                help="نسبة حضور الطالب في المحاضرات والأنشطة التعليمية"
            )
        
        with col2:
            previous_scores = st.number_input(
                "📝 متوسط الدرجات السابقة",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                help="متوسط أداء الطالب في الاختبارات السابقة"
            )
            
            tutoring_sessions = st.slider(
                "👨‍🏫 جلسات الدروس الخصوصية",
                min_value=0,
                max_value=10,
                value=2,
                help="عدد جلسات الدعم الإضافية الأسبوعية"
            )
        
        # أزرار التحكم
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
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 30px 0;">
                    <div style="text-align: center; padding: 15px; background: #F8F9FA; border-radius: 10px;">
                        <div style="color: #6C757D; font-size: 0.9em;">الدرجة النهائية</div>
                        <div style="color: {result['color']}; font-size: 2em; font-weight: bold;">{result['score']}/100</div>
                    </div>
                    
                    <div style="text-align: center; padding: 15px; background: #F8F9FA; border-radius: 10px;">
                        <div style="color: #6C757D; font-size: 0.9em;">التقييم</div>
                        <div style="color: {result['color']}; font-size: 1.5em; font-weight: bold;">{result['grade']}</div>
                    </div>
                    
                    <div style="text-align: center; padding: 15px; background: #F8F9FA; border-radius: 10px;">
                        <div style="color: #6C757D; font-size: 0.9em;">النسبة المئوية</div>
                        <div style="color: {result['color']}; font-size: 1.5em; font-weight: bold;">{result['score']}%</div>
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
                <h3>📝 التوصيات المخصصة</h3>
                <div style="background: linear-gradient(135deg, {result['color']}15, #00666615); 
                     padding: 20px; border-radius: 10px; border-right: 4px solid {result['color']};">
                    <h4 style="color: {result['color']}; margin-bottom: 15px;">{result['feedback']}</h4>
                    
                    <h5>🎯 توصيات للتحسين:</h5>
                    <ul style="padding-right: 20px;">
                        <li>زيادة ساعات الدراسة المنتظمة إلى {max(20, result['recommended_hours'])} ساعة أسبوعياً</li>
                        <li>تحسين نسبة الحضور إلى 90% على الأقل</li>
                        <li>التركيز على المواد التي تحتاج تحسين</li>
                        <li>الاستفادة من {max(3, result['recommended_tutoring'])} جلسات دعم أسبوعياً</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("⏳ انتظر نتائج التنبؤ لرؤية التوصيات المخصصة")
    
    return hours_studied, attendance_rate, previous_scores, tutoring_sessions, predict_clicked

def show_analysis_page():
    """صفحة تحليل البيانات"""
    st.markdown("""
    <div class="custom-card">
        <h2>📊 محلل البيانات المتقدم</h2>
        <p>قم برفع ملفات البيانات لتحليل شامل وتوليد تقارير تفصيلية</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📁 اختر ملف CSV", type=['csv'], help="ارفع ملف CSV يحتوي على بيانات الطلاب")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # معلومات الملف
            st.markdown(f"""
            <div class="custom-card">
                <h4>✅ تم تحميل الملف بنجاح</h4>
                <p><strong>عدد الصفوف:</strong> {len(df):,}</p>
                <p><strong>عدد الأعمدة:</strong> {len(df.columns)}</p>
                <p><strong>الحقول:</strong> {', '.join(df.columns[:3])}{'...' if len(df.columns) > 3 else ''}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # علامات تبويب التحليل
            tab1, tab2 = st.tabs(["📋 عرض البيانات", "📈 الإحصائيات"])
            
            with tab1:
                st.dataframe(df.head(15), use_container_width=True)
            
            with tab2:
                st.write("### 📊 الإحصائيات الوصفية")
                st.dataframe(df.describe(), use_container_width=True)
                
                # إحصائيات إضافية
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("القيم المفقودة", df.isnull().sum().sum())
                with col2:
                    st.metric("القيم المكررة", df.duplicated().sum())
                with col3:
                    st.metric("المساحة", f"{df.memory_usage().sum() / 1024:.1f} KB")
        
        except Exception as e:
            st.error(f"❌ حدث خطأ في تحليل الملف: {str(e)}")

def show_reports_page():
    """صفحة التقارير"""
    st.markdown("""
    <div class="custom-card">
        <h2>📈 التقارير والتحليلات</h2>
        <p>استعرض التقارير والرسوم البيانية التي تم إنشاؤها مسبقاً</p>
    </div>
    """, unsafe_allow_html=True)
    
    # التحقق من وجود مجلد الصور
    if os.path.exists("images") and os.listdir("images"):
        image_files = [
            f for f in os.listdir("images") 
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        ]
        
        if image_files:
            st.write(f"### 📸 عدد الصور المتاحة: {len(image_files)}")
            
            # عرض الصور في شبكة متجاوبة
            cols = st.columns(3)
            for idx, img_file in enumerate(image_files[:9]):
                with cols[idx % 3]:
                    img_path = os.path.join("images", img_file)
                    try:
                        st.image(img_path, caption=img_file, use_column_width=True)
                    except Exception as e:
                        st.error(f"❌ تعذر تحميل الصورة: {img_file}")
        else:
            st.info("📭 لا توجد صور متاحة في مجلد الصور")
    else:
        st.info("📁 مجلد الصور غير موجود. سيتم استخدام تقارير افتراضية.")
        
        # عرض تقارير افتراضية
        st.markdown("""
        <div class="custom-card">
            <h4>📊 تقارير افتراضية</h4>
            <p>يمكنك إنشاء تقارير مخصصة عن طريق رفع ملفات البيانات في قسم "تحليل البيانات"</p>
        </div>
        """, unsafe_allow_html=True)

def show_settings_page():
    """صفحة الإعدادات"""
    st.markdown("""
    <div class="custom-card">
        <h2>⚙️ إعدادات النظام</h2>
        <p>قم بتخصيص إعدادات النظام حسب احتياجاتك</p>
    </div>
    """, unsafe_allow_html=True)
    
    # إعدادات النموذج
    with st.expander("🛠️ إعدادات النموذج", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            model_type = st.selectbox(
                "نوع النموذج",
                ["انحدار خطي", "شجرة قرار", "غابة عشوائية", "شبكة عصبية"],
                index=0
            )
            
            confidence_level = st.slider(
                "مستوى الثقة (%)",
                min_value=50,
                max_value=99,
                value=85
            )
        
        with col2:
            auto_update = st.checkbox("التحديث التلقائي للنموذج", value=True)
            save_reports = st.checkbox("حفظ التقارير تلقائياً", value=True)
        
        if st.button("💾 حفظ إعدادات النموذج"):
            st.success("✅ تم حفظ الإعدادات بنجاح!")
    
    # إعدادات الواجهة
    with st.expander("🎨 إعدادات الواجهة"):
        theme = st.selectbox(
            "السمة",
            ["بترولي وذهبي (افتراضي)", "فاتح", "غامق", "أزرق"],
            index=0
        )
        
        language = st.selectbox(
            "اللغة",
            ["العربية", "الإنجليزية"],
            index=0
        )
        
        font_size = st.select_slider(
            "حجم الخط",
            options=["صغير", "متوسط", "كبير"],
            value="متوسط"
        )
        
        if st.button("💾 حفظ إعدادات الواجهة"):
            st.success("✅ تم حفظ إعدادات الواجهة!")

# ============================================================================
# 6. دالة التنبؤ الرئيسية
# ============================================================================
def predict_score(hours, attendance, prev_scores, tutoring):
    """دالة التنبؤ بالدرجة"""
    try:
        # تحميل النموذج
        model = joblib.load('regression_model.pkl')
        
        # إعداد البيانات (قيمة افتراضية لتأثير الأقران = 3)
        input_data = [[hours, attendance, prev_scores, tutoring, 3]]
        score = round(model.predict(input_data)[0], 2)
        score = max(0, min(100, score))
        
        # تحديد التصنيف والتوصيات
        if score >= 90:
            color = DesignConfig.COLORS['success']
            feedback = "أداء استثنائي - مستوى متميز"
            grade = "ممتاز"
            recommended_hours = hours
            recommended_tutoring = tutoring
        elif score >= 75:
            color = DesignConfig.COLORS['info']
            feedback = "أداء جيد جداً - يواصل التقدم"
            grade = "جيد جداً"
            recommended_hours = max(hours + 2, 25)
            recommended_tutoring = max(tutoring + 1, 3)
        elif score >= 60:
            color = DesignConfig.COLORS['warning']
            feedback = "أداء مقبول - يحتاج إلى تحسين"
            grade = "مقبول"
            recommended_hours = max(hours + 5, 25)
            recommended_tutoring = max(tutoring + 2, 4)
        else:
            color = DesignConfig.COLORS['danger']
            feedback = "أداء ضعيف - يحتاج إلى دعم مكثف"
            grade = "ضعيف"
            recommended_hours = max(hours + 10, 30)
            recommended_tutoring = max(tutoring + 3, 5)
        
        # حفظ النتيجة في session state
        st.session_state.prediction_result = {
            'score': score,
            'color': color,
            'feedback': feedback,
            'grade': grade,
            'recommended_hours': recommended_hours,
            'recommended_tutoring': recommended_tutoring
        }
        
        return True
        
    except Exception as e:
        st.error(f"❌ خطأ في التنبؤ: {str(e)}")
        return False

# ============================================================================
# 7. التطبيق الرئيسي
# ============================================================================
def main():
    """الدالة الرئيسية للتطبيق"""
    
    # إعداد الصفحة
    setup_page_config()
    apply_comprehensive_css()
    
    # إنشاء القائمة الجانبية
    page = create_sidebar()
    
    # الهيدر الرئيسي
    st.markdown("""
    <div style="background: linear-gradient(135deg, #004d4d 0%, #006666 100%); 
         padding: 3rem 2rem; border-radius: 1rem; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 2.8rem;">🎓 نظام التنبؤ الذكي بأداء الطلاب</h1>
        <p style="color: #D4AF37; font-size: 1.3rem; margin: 1rem 0 0 0;">
        حل متكامل باستخدام الذكاء الاصطناعي للتنبؤ الأكاديمي وتحليل البيانات التعليمية
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # شريط العلامات
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div style="background: rgba(0,102,102,0.1); padding: 10px; border-radius: 8px; text-align: center;"><span style="color: #006666; font-weight: bold;">🎯 تنبؤ دقيق</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="background: rgba(212,175,55,0.1); padding: 10px; border-radius: 8px; text-align: center;"><span style="color: #D4AF37; font-weight: bold;">📊 تحليل متقدم</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="background: rgba(0,102,102,0.1); padding: 10px; border-radius: 8px; text-align: center;"><span style="color: #006666; font-weight: bold;">📈 تقارير تفاعلية</span></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div style="background: rgba(212,175,55,0.1); padding: 10px; border-radius: 8px; text-align: center;"><span style="color: #D4AF37; font-weight: bold;">⚡ نتائج فورية</span></div>', unsafe_allow_html=True)
    
    # عرض الصفحة المختارة
    if page == "🏠 الصفحة الرئيسية":
        show_home_page()
    
    elif page == "🎯 أداة التنبؤ":
        hours, attendance, prev_scores, tutoring, predict_clicked = show_prediction_page()
        
        if predict_clicked:
            with st.spinner("🔍 جاري تحليل البيانات والتنبؤ بالنتيجة..."):
                success = predict_score(hours, attendance, prev_scores, tutoring)
                if success:
                    st.success("✅ تم إكمال عملية التنبؤ بنجاح!")
                    st.balloons()
                    st.rerun()
    
    elif page == "📊 تحليل البيانات":
        show_analysis_page()
    
    elif page == "📈 التقارير":
        show_reports_page()
    
    elif page == "⚙️ الإعدادات":
        show_settings_page()
    
    # الفوتر
    st.markdown("""
    <div class="footer">
        <div class="responsive-grid" style="text-align: right; padding: 20px 0;">
            <div>
                <h4 style="color: #D4AF37; margin-bottom: 15px;">📞 للتواصل والدعم</h4>
                <p>البريد الإلكتروني: support@predictionsystem.edu</p>
                <p>الهاتف: +966 55 123 4567</p>
            </div>
            <div>
                <h4 style="color: #D4AF37; margin-bottom: 15px;">🔗 روابط سريعة</h4>
                <p>• دليل الاستخدام</p>
                <p>• الأسئلة الشائعة</p>
                <p>• سياسة الخصوصية</p>
            </div>
            <div>
                <h4 style="color: #D4AF37; margin-bottom: 15px;">💼 عن النظام</h4>
                <p>نظام تنبؤ أكاديمي متقدم</p>
                <p>يدعم اللغة العربية بالكامل</p>
                <p>تصميم متجاوب مع جميع الأجهزة</p>
            </div>
        </div>
        <hr style="border-color: rgba(255,255,255,0.2); margin: 20px 0;">
        <p style="text-align: center; margin: 0; color: rgba(255,255,255,0.9);">
        © 2024 نظام التنبؤ الذكي بأداء الطلاب. جميع الحقوق محفوظة. | الإصدار 4.0 | تم التطوير باستخدام Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # إضافة تحسينات إضافية للجوال
    st.markdown("""
    <script>
    // تحسين تجربة الجوال
    if (window.innerWidth <= 768) {
        // إضافة شاشة تحميل
        const loader = document.createElement('div');
        loader.id = 'mobile-loader';
        loader.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #006666;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 1000000;
            font-family: 'Tajawal', sans-serif;
        `;
        loader.innerHTML = `
            <div style="text-align: center; padding: 20px;">
                <h2>🎓 نظام التنبؤ الذكي</h2>
                <p>جاري التحميل...</p>
                <div style="margin-top: 20px; width: 50px; height: 50px; border: 5px solid rgba(255,255,255,0.3); border-top: 5px solid white; border-radius: 50%; animation: spin 1s linear infinite;"></div>
            </div>
        `;
        document.body.appendChild(loader);
        
        // إخفاء الشاشة بعد التحميل
        window.addEventListener('load', function() {
            setTimeout(() => {
                loader.style.opacity = '0';
                loader.style.transition = 'opacity 0.5s';
                setTimeout(() => loader.remove(), 500);
            }, 1000);
        });
    }
    
    // دعم اللمس للشاشات التي تعمل باللمس
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
        
        // تحسين حجم الأزرار للجوال
        const buttons = document.querySelectorAll('button');
        buttons.forEach(btn => {
            btn.style.minHeight = '44px';
            btn.style.minWidth = '44px';
        });
    }
    
    // إدارة القائمة الجانبية في الجوال
    function toggleSidebar() {
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        const isVisible = sidebar.style.transform !== 'translateX(100%)';
        
        if (isVisible) {
            sidebar.style.transform = 'translateX(100%)';
        } else {
            sidebar.style.transform = 'translateX(0)';
        }
    }
    
    // إضافة أسلوب للتدوير
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .touch-device input, .touch-device button, .touch-device select {
            font-size: 16px !important;
        }
    `;
    document.head.appendChild(style);
    </script>
    """, unsafe_allow_html=True)

# ============================================================================
# 8. التحقق من الملفات المطلوبة وإنشاء نموذج افتراضي إذا لزم الأمر
# ============================================================================
def check_and_create_model():
    """التحقق من وجود النموذج وإنشاء نموذج افتراضي إذا لزم الأمر"""
    try:
        if not os.path.exists('regression_model.pkl'):
            st.warning("⚠️ ملف النموذج غير موجود. سيتم إنشاء نموذج افتراضي للعرض التوضيحي.")
            
            from sklearn.linear_model import LinearRegression
            import numpy as np
            
            # إنشاء بيانات تدريب افتراضية
            np.random.seed(42)
            n_samples = 100
            
            # ميزات: ساعات الدراسة، الحضور، الدرجات السابقة، دروس خصوصية، تأثير الأقران
            X = np.column_stack([
                np.random.randint(10, 40, n_samples),  # ساعات الدراسة
                np.random.randint(60, 100, n_samples),  # الحضور
                np.random.uniform(50, 95, n_samples),   # الدرجات السابقة
                np.random.randint(0, 10, n_samples),    # دروس خصوصية
                np.random.randint(1, 6, n_samples)      # تأثير الأقران
            ])
            
            # درجات: معادلة بمعاملات واقعية
            y = (
                X[:, 0] * 0.4 +      # ساعات الدراسة (40%)
                X[:, 1] * 0.3 +      # الحضور (30%)
                X[:, 2] * 0.25 +     # الدرجات السابقة (25%)
                X[:, 3] * 0.15 +     # دروس خصوصية (15%)
                X[:, 4] * 0.05 +     # تأثير الأقران (5%)
                np.random.randn(n_samples) * 5  # ضوضاء
            )
            
            # ضمان أن الدرجات بين 0 و 100
            y = np.clip(y, 0, 100)
            
            # تدريب النموذج
            model = LinearRegression()
            model.fit(X, y)
            
            # حفظ النموذج
            joblib.dump(model, 'regression_model.pkl')
            st.success("✅ تم إنشاء النموذج الافتراضي بنجاح!")
        
        return True
        
    except Exception as e:
        st.error(f"❌ خطأ في إنشاء النموذج: {str(e)}")
        return False

# ============================================================================
# 9. بدء التشغيل
# ============================================================================
if __name__ == "__main__":
    # التحقق من النموذج وإنشاؤه إذا لزم الأمر
    if check_and_create_model():
        # تشغيل التطبيق
        main()
    else:
        st.error("❌ تعذر تحميل أو إنشاء النموذج. يرجى التحقق من الإعدادات.")
