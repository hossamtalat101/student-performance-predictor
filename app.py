"""
نظام التنبؤ الذكي بأداء الطلاب - تصميم احترافي
إصدار رسمي بنظام ألوان البترولي والذهبي
"""

# ============================================================================
# 1. استيراد المكتبات
# ============================================================================
import gradio as gr
import pandas as pd
import joblib
import io
import zipfile
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
import gradio.themes as gr_themes
import warnings
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
    
    # الخطوط
    FONT_FAMILY = "Tajawal, Arial, sans-serif"
    
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
# 3. CSS مخصص مصحح (مع إصلاح مشكلة النصوص)
# ============================================================================
CUSTOM_CSS = f"""
/* إعادة تعيين كاملة */
.gradio-container * {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
    color: {DesignConfig.COLORS['petroleum_dark']} !important;
}}

/* تأكيد عرض النصوص العربية */
[data-testid], .prose, .markdown, .block, .form, .panel {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
    direction: rtl !important;
    text-align: right !important;
}}

/* إعدادات عامة */
body, .gradio-container {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
    background: linear-gradient(135deg, {DesignConfig.COLORS['gray_light']} 0%, {DesignConfig.COLORS['white']} 100%) !important;
    min-height: 100vh !important;
    direction: rtl !important;
    line-height: 1.6 !important;
    color: {DesignConfig.COLORS['petroleum_dark']} !important;
}}

/* تأمين عرض جميع النصوص */
h1, h2, h3, h4, h5, h6, p, span, div, label, input, textarea, select, button {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
    color: {DesignConfig.COLORS['petroleum_dark']} !important;
}}

/* ========== الهيدر الرئيسي ========== */
.main-header {{
    background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum_dark']} 0%, {DesignConfig.COLORS['petroleum']} 100%) !important;
    padding: 40px 20px !important;
    border-radius: 0 0 {DesignConfig.BORDER_RADIUS['xl']} {DesignConfig.BORDER_RADIUS['xl']} !important;
    box-shadow: {DesignConfig.SHADOWS['large']} !important;
    position: relative !important;
    overflow: hidden !important;
    margin-bottom: 40px !important;
}}

.header-title {{
    color: {DesignConfig.COLORS['white']} !important;
    font-size: 2.8em !important;
    font-weight: 700 !important;
    text-align: center !important;
    margin-bottom: 15px !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2) !important;
    font-family: {DesignConfig.FONT_FAMILY} !important;
}}

.header-subtitle {{
    color: {DesignConfig.COLORS['gold_light']} !important;
    font-size: 1.3em !important;
    text-align: center !important;
    max-width: 800px !important;
    margin: 0 auto 30px auto !important;
    font-weight: 300 !important;
    font-family: {DesignConfig.FONT_FAMILY} !important;
}}

/* ========== البطاقات ========== */
.design-card {{
    background: {DesignConfig.COLORS['white']} !important;
    border-radius: {DesignConfig.BORDER_RADIUS['large']} !important;
    box-shadow: {DesignConfig.SHADOWS['medium']} !important;
    padding: 32px !important;
    margin: 20px 0 !important;
    border: 1px solid {DesignConfig.COLORS['gray_medium']} !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}}

.card-title {{
    color: {DesignConfig.COLORS['petroleum_dark']} !important;
    font-size: 1.8em !important;
    font-weight: 600 !important;
    margin-bottom: 20px !important;
    padding-bottom: 15px !important;
    border-bottom: 2px solid {DesignConfig.COLORS['gold_light']} !important;
    position: relative !important;
    font-family: {DesignConfig.FONT_FAMILY} !important;
    text-align: right !important;
}}

.card-title::after {{
    content: '';
    position: absolute;
    bottom: -2px;
    right: 0;
    width: 60px;
    height: 2px;
    background: {DesignConfig.COLORS['petroleum']};
}}

/* ========== الأزرار ========== */
.btn-elegant {{
    background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum']} 0%, {DesignConfig.COLORS['petroleum_dark']} 100%) !important;
    color: {DesignConfig.COLORS['white']} !important;
    border: none !important;
    border-radius: {DesignConfig.BORDER_RADIUS['medium']} !important;
    padding: 14px 32px !important;
    font-size: 1.1em !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: {DesignConfig.SHADOWS['small']} !important;
    position: relative !important;
    overflow: hidden !important;
    font-family: {DesignConfig.FONT_FAMILY} !important;
}}

.btn-elegant:hover {{
    transform: translateY(-2px) !important;
    box-shadow: {DesignConfig.SHADOWS['medium']} !important;
    color: {DesignConfig.COLORS['gold_light']} !important;
}}

.btn-elegant-secondary {{
    background: transparent !important;
    color: {DesignConfig.COLORS['petroleum']} !important;
    border: 2px solid {DesignConfig.COLORS['petroleum']} !important;
    border-radius: {DesignConfig.BORDER_RADIUS['medium']} !important;
    padding: 12px 28px !important;
    font-size: 1em !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    font-family: {DesignConfig.FONT_FAMILY} !important;
}}

/* ========== أدوات الإدخال ========== */
.input-field {{
    border: 2px solid {DesignConfig.COLORS['gray_medium']} !important;
    border-radius: {DesignConfig.BORDER_RADIUS['medium']} !important;
    padding: 14px 18px !important;
    font-size: 1em !important;
    transition: all 0.3s ease !important;
    background: {DesignConfig.COLORS['white']} !important;
    font-family: {DesignConfig.FONT_FAMILY} !important;
    color: {DesignConfig.COLORS['petroleum_dark']} !important;
}}

.input-label {{
    color: {DesignConfig.COLORS['petroleum_dark']} !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
    display: block !important;
    font-size: 1em !important;
    font-family: {DesignConfig.FONT_FAMILY} !important;
    text-align: right !important;
}}

/* ========== التنقل ========== */
.navigation-bar {{
    display: flex !important;
    justify-content: center !important;
    gap: 15px !important;
    margin: 30px 0 !important;
    flex-wrap: wrap !important;
}}

.nav-btn-large {{
    min-width: 200px !important;
    height: 80px !important;
    font-size: 1.2em !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 5px !important;
    font-family: {DesignConfig.FONT_FAMILY} !important;
}}

/* ========== الفوتر ========== */
.footer {{
    background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum_dark']} 0%, {DesignConfig.COLORS['petroleum']} 100%) !important;
    padding: 40px 20px !important;
    border-radius: {DesignConfig.BORDER_RADIUS['xl']} {DesignConfig.BORDER_RADIUS['xl']} 0 0 !important;
    margin-top: 60px !important;
    color: {DesignConfig.COLORS['white']} !important;
    text-align: center !important;
    font-family: {DesignConfig.FONT_FAMILY} !important;
}}

/* ========== إصلاح خاص للعناوين والنصوص ========== */
.gr-markdown, .gr-md {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
    color: {DesignConfig.COLORS['petroleum_dark']} !important;
    direction: rtl !important;
    text-align: right !important;
    line-height: 1.8 !important;
}}

.gr-markdown h1, .gr-markdown h2, .gr-markdown h3, .gr-markdown h4, .gr-markdown h5, .gr-markdown h6 {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
    color: {DesignConfig.COLORS['petroleum_dark']} !important;
    text-align: right !important;
    margin-bottom: 15px !important;
}}

.gr-markdown p {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
    color: {DesignConfig.COLORS['gray_dark']} !important;
    text-align: right !important;
    margin-bottom: 10px !important;
    line-height: 1.8 !important;
}}

.gr-markdown ul, .gr-markdown ol {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
    color: {DesignConfig.COLORS['gray_dark']} !important;
    text-align: right !important;
    padding-right: 20px !important;
    margin-bottom: 15px !important;
}}

/* إصلاح خاص لعناصر Gradio */
.gr-box, .gr-form, .gr-panel {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
    color: {DesignConfig.COLORS['petroleum_dark']} !important;
}}

.gr-textbox, .gr-number, .gr-slider {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
}}

.gr-button {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
}}

/* إصلاح علامات التبويب */
.gr-tabs {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
}}

.gr-tab {{
    font-family: {DesignConfig.FONT_FAMILY} !important;
    color: {DesignConfig.COLORS['petroleum_dark']} !important;
}}
"""

# ============================================================================
# 4. بناء الواجهة الرئيسية
# ============================================================================
def build_header():
    """بناء الهيدر الرئيسي"""
    return gr.HTML(f"""
    <div class="main-header">
        <h1 class="header-title">نظام التنبؤ الذكي بأداء الطلاب</h1>
        <p class="header-subtitle">حل متكامل للتنبؤ الأكاديمي وتحليل البيانات التعليمية باستخدام أحدث التقنيات</p>
    </div>
    """)

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
            color, feedback = DesignConfig.COLORS['success'], "أداء استثنائي - مستوى متميز"
            grade = "ممتاز"
        elif score >= 75:
            color, feedback = DesignConfig.COLORS['info'], "أداء جيد جداً - يواصل التقدم"
            grade = "جيد جداً"
        elif score >= 60:
            color, feedback = DesignConfig.COLORS['warning'], "أداء مقبول - يحتاج إلى تحسين"
            grade = "مقبول"
        else:
            color, feedback = DesignConfig.COLORS['danger'], "أداء ضعيف - يحتاج إلى دعم"
            grade = "ضعيف"
        
        # بناء النتيجة
        result_html = f"""
        <div style="text-align: center; padding: 20px; font-family: {DesignConfig.FONT_FAMILY};">
            <h2 style="color: {DesignConfig.COLORS['petroleum_dark']}; margin-bottom: 20px;">النتيجة التفصيلية</h2>
            
            <div style="margin: 30px auto; width: 300px; height: 150px; background: conic-gradient(
                from 0deg,
                {DesignConfig.COLORS['danger']} 0deg,
                {DesignConfig.COLORS['warning']} 108deg,
                {DesignConfig.COLORS['success']} 180deg
            ); border-radius: 150px 150px 0 0; position: relative; overflow: hidden;">
                <div style="position: absolute; width: 70%; height: 70%; background: white; border-radius: 50%; top: 15%; left: 15%;"></div>
                <div style="position: absolute; bottom: 0; left: 50%; width: 4px; height: 70%; background: {color}; 
                    transform-origin: bottom; transform: translateX(-50%) rotate({(score/100)*180 - 90}deg);"></div>
                <div style="position: absolute; bottom: 40%; left: 50%; transform: translateX(-50%); 
                    font-size: 3em; font-weight: bold; color: {color};">{score}</div>
            </div>
            
            <div style="margin-top: 30px; padding: 20px; background: {DesignConfig.COLORS['gray_light']}; border-radius: {DesignConfig.BORDER_RADIUS['medium']};">
                <div style="color: {color}; font-size: 1.5em; font-weight: bold; margin-bottom: 15px;">{grade}</div>
                <p style="color: {DesignConfig.COLORS['gray_dark']}; font-size: 1.1em;">{feedback}</p>
            </div>
        </div>
        """
        
        return result_html
        
    except Exception as e:
        error_html = f"""
        <div style="padding: 20px; background: {DesignConfig.COLORS['warning']}15; border-radius: {DesignConfig.BORDER_RADIUS['medium']}; 
            border: 1px solid {DesignConfig.COLORS['warning']}30; font-family: {DesignConfig.FONT_FAMILY};">
            <h4 style="color: {DesignConfig.COLORS['danger']}; margin-bottom: 10px;">⚠️ حدث خطأ</h4>
            <p>تفاصيل الخطأ: {str(e)}</p>
        </div>
        """
        return error_html

def build_footer():
    """بناء الفوتر"""
    return gr.HTML(f"""
    <div class="footer">
        <p style="color: {DesignConfig.COLORS['gold_light']}; font-size: 1.1em; margin-bottom: 10px;">
            نظام التنبؤ الذكي بأداء الطلاب
        </p>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9em;">
            © 2024 جميع الحقوق محفوظة
        </p>
    </div>
    """)

# ============================================================================
# 6. بناء واجهة مبسطة ومباشرة
# ============================================================================
def create_simple_interface():
    """إنشاء واجهة مبسطة تعمل بشكل صحيح"""
    
    with gr.Blocks(
        css=CUSTOM_CSS,
        title="نظام التنبؤ الذكي بأداء الطلاب",
        theme=gr.themes.Default(
            primary_hue="teal",
            secondary_hue="gray",
            font=[gr.themes.GoogleFont("Tajawal")]
        )
    ) as app:
        
        # الهيدر الرئيسي
        build_header()
        
        # قسم التنبؤ (الصفحة الرئيسية)
        with gr.Column(elem_classes="design-card"):
            # استخدام HTML مباشرة للتحكم الكامل في التنسيق
            gr.HTML("""
            <div style="text-align: right; direction: rtl; font-family: Tajawal, Arial, sans-serif;">
                <h2 style="color: #004d4d; margin-bottom: 20px;">نظرة عامة على النظام</h2>
                <p style="color: #6C757D; line-height: 1.8; margin-bottom: 15px;">
                    يقدم هذا النظام حلولاً متكاملة للتنبؤ بالأداء الأكاديمي للطلاب باستخدام تقنيات متقدمة 
                    في تحليل البيانات والتعلم الآلي. تم تصميم النظام ليكون أداة فعالة للمؤسسات التعليمية 
                    لاتخاذ قرارات مستنيرة وتحسين النتائج التعليمية.
                </p>
                
                <h3 style="color: #006666; margin: 25px 0 15px 0;">المميزات الرئيسية:</h3>
                <ul style="color: #6C757D; padding-right: 20px; line-height: 1.8;">
                    <li style="margin-bottom: 8px;"><strong>تنبؤ دقيق:</strong> استخدام نماذج تنبؤية متقدمة</li>
                    <li style="margin-bottom: 8px;"><strong>تحليل شامل:</strong> تقارير تفصيلية مع رسوم بيانية متعددة</li>
                    <li style="margin-bottom: 8px;"><strong>واجهة سهلة:</strong> تصميم بديهي يسهل على المستخدم التفاعل</li>
                    <li style="margin-bottom: 8px;"><strong>نتائج آنية:</strong> معالجة فورية وإظهار النتائج فوراً</li>
                    <li><strong>توصيات مخصصة:</strong> اقتراحات تحسين بناءً على أداء الطالب</li>
                </ul>
                
                <h3 style="color: #006666; margin: 25px 0 15px 0;">كيفية الاستخدام:</h3>
                <p style="color: #6C757D; line-height: 1.8;">
                    اختر الأداة المناسبة من الأزرار أدناه لبدء التحليل أو التنبؤ.
                </p>
            </div>
            """)
        
        # شريط التنقل
        with gr.Row(elem_classes="navigation-bar"):
            nav_predict = gr.Button(
                "📊 أداة التنبؤ",
                elem_classes=["btn-elegant", "nav-btn-large"],
                size="lg"
            )
            nav_analyze = gr.Button(
                "📈 تحليل البيانات",
                elem_classes=["btn-elegant", "nav-btn-large"],
                size="lg"
            )
        
        # قسم أداة التنبؤ
        with gr.Column(visible=True, elem_classes="design-card") as prediction_section:
            gr.HTML("""
            <div style="text-align: right; direction: rtl; font-family: Tajawal, Arial, sans-serif;">
                <h2 style="color: #004d4d; margin-bottom: 20px;">🎯 أداة التنبؤ الذكي بالدرجات</h2>
                <p style="color: #6C757D; line-height: 1.8; margin-bottom: 25px;">
                    أدخل البيانات المطلوبة للتنبؤ بالأداء الأكاديمي للطالب.
                    النظام سيقوم بتحليل المعلومات وتقديم تنبؤ دقيق مع توصيات مخصصة.
                </p>
            </div>
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    # استخدام HTML للعنوان والمعلومات
                    gr.HTML("""
                    <div style="text-align: right; direction: rtl; font-family: Tajawal, Arial, sans-serif; margin-bottom: 8px;">
                        <strong style="color: #004d4d; font-size: 1em;">ساعات الدراسة الأسبوعية</strong>
                        <div style="color: #6C757D; font-size: 0.9em; margin-top: 5px;">
                            عدد الساعات التي يخصصها الطالب للدراسة أسبوعياً
                        </div>
                    </div>
                    """)
                    hours_studied = gr.Slider(
                        minimum=0,
                        maximum=40,
                        value=20,
                        elem_classes="input-field"
                    )
                    
                    gr.HTML("""
                    <div style="text-align: right; direction: rtl; font-family: Tajawal, Arial, sans-serif; margin-bottom: 8px; margin-top: 20px;">
                        <strong style="color: #004d4d; font-size: 1em;">نسبة الحضور (%)</strong>
                        <div style="color: #6C757D; font-size: 0.9em; margin-top: 5px;">
                            نسبة حضور الطالب في المحاضرات والأنشطة التعليمية
                        </div>
                    </div>
                    """)
                    attendance_rate = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=85,
                        elem_classes="input-field"
                    )
                    
                    gr.HTML("""
                    <div style="text-align: right; direction: rtl; font-family: Tajawal, Arial, sans-serif; margin-bottom: 8px; margin-top: 20px;">
                        <strong style="color: #004d4d; font-size: 1em;">جلسات الدروس الخصوصية</strong>
                        <div style="color: #6C757D; font-size: 0.9em; margin-top: 5px;">
                            عدد جلسات الدعم الإضافية الأسبوعية
                        </div>
                    </div>
                    """)
                    tutoring_sessions = gr.Slider(
                        minimum=0,
                        maximum=10,
                        step=1,
                        value=2,
                        elem_classes="input-field"
                    )
                
                with gr.Column(scale=1):
                    gr.HTML("""
                    <div style="text-align: right; direction: rtl; font-family: Tajawal, Arial, sans-serif; margin-bottom: 8px;">
                        <strong style="color: #004d4d; font-size: 1em;">متوسط الدرجات السابقة</strong>
                        <div style="color: #6C757D; font-size: 0.9em; margin-top: 5px;">
                            متوسط أداء الطالب في الاختبارات السابقة
                        </div>
                    </div>
                    """)
                    previous_scores = gr.Number(
                        value=75,
                        elem_classes="input-field"
                    )
                    
                    gr.HTML("""
                    <div style="text-align: right; direction: rtl; font-family: Tajawal, Arial, sans-serif; margin-bottom: 8px; margin-top: 20px;">
                        <strong style="color: #004d4d; font-size: 1em;">تأثير المحيط الدراسي</strong>
                        <div style="color: #6C757D; font-size: 0.9em; margin-top: 5px;">
                            مدى تأثير البيئة الدراسية والأقران على أداء الطالب (1 = ضعيف، 5 = قوي)
                        </div>
                    </div>
                    """)
                    peer_influence = gr.Slider(
                        minimum=1,
                        maximum=5,
                        step=1,
                        value=3,
                        elem_classes="input-field"
                    )
                    
                    # أزرار التحكم
                    with gr.Row():
                        reset_btn = gr.Button(
                            "🔄 إعادة تعيين",
                            elem_classes="btn-elegant-secondary",
                            size="sm"
                        )
                        predict_btn = gr.Button(
                            "🚀 بدء التنبؤ",
                            elem_classes="btn-elegant",
                            size="lg",
                            scale=2
                        )
            
            # مساحة النتائج
            results_display = gr.HTML(
                value=f"""
                <div style="text-align: center; padding: 40px; background: {DesignConfig.COLORS['gray_light']}; 
                     border-radius: {DesignConfig.BORDER_RADIUS['medium']}; margin-top: 20px; font-family: {DesignConfig.FONT_FAMILY};">
                    <div style="color: {DesignConfig.COLORS['petroleum']}; font-size: 1.2em; margin-bottom: 15px;">
                        ⏳ أدخل البيانات واضغط على "بدء التنبؤ"
                    </div>
                    <p style="color: {DesignConfig.COLORS['gray_dark']}; line-height: 1.6;">
                        سيظهر هنا التنبؤ بالدرجة والتقييم التفصيلي والتوصيات المخصصة.
                    </p>
                </div>
                """
            )
        
        # قسم تحليل البيانات
        with gr.Column(visible=False, elem_classes="design-card") as analysis_section:
            gr.HTML("""
            <div style="text-align: right; direction: rtl; font-family: Tajawal, Arial, sans-serif;">
                <h2 style="color: #004d4d; margin-bottom: 20px;">📈 محلل البيانات المتقدم</h2>
                <p style="color: #6C757D; line-height: 1.8; margin-bottom: 25px;">
                    قم برفع ملف البيانات لتحليل شامل وتوليد تقارير تفصيلية.
                    النظام يدعم ملفات CSV ويقدم تحليلاً إحصائياً كاملاً.
                </p>
            </div>
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML("""
                    <div style="text-align: right; direction: rtl; font-family: Tajawal, Arial, sans-serif; margin-bottom: 8px;">
                        <strong style="color: #004d4d; font-size: 1em;">رفع ملف البيانات</strong>
                        <div style="color: #6C757D; font-size: 0.9em; margin-top: 5px;">
                            اختر ملف CSV يحتوي على بيانات الطلاب
                        </div>
                    </div>
                    """)
                    file_upload = gr.File(
                        file_types=[".csv"],
                        elem_classes="input-field"
                    )
                    
                    with gr.Row():
                        analyze_file_btn = gr.Button(
                            "🔍 تحليل البيانات",
                            elem_classes="btn-elegant"
                        )
                        clear_analysis_btn = gr.Button(
                            "🗑️ مسح",
                            elem_classes="btn-elegant-secondary"
                        )
                
                with gr.Column(scale=2):
                    gr.HTML("""
                    <div style="text-align: right; direction: rtl; font-family: Tajawal, Arial, sans-serif; margin-bottom: 8px;">
                        <strong style="color: #004d4d; font-size: 1em;">معلومات الملف</strong>
                    </div>
                    """)
                    file_info = gr.Textbox(
                        interactive=False,
                        lines=5,
                        elem_classes="input-field"
                    )
            
            # علامات التبويب
            with gr.Tabs():
                with gr.TabItem("📋 عينة البيانات"):
                    data_preview = gr.Dataframe(
                        label="معاينة البيانات",
                        interactive=False,
                        wrap=True
                    )
                
                with gr.TabItem("📊 الإحصائيات"):
                    statistics_display = gr.Textbox(
                        label="التحليل الإحصائي",
                        interactive=False,
                        lines=10,
                        elem_classes="input-field"
                    )
        
        # الفوتر
        build_footer()
        
        # ===========================================
        # دوال المعالجة والأحداث
        # ===========================================
        
        def clear_prediction_inputs():
            """إعادة تعيين حقول التنبؤ"""
            return [20, 85, 75, 2, 3, ""]
        
        def analyze_uploaded_file(file):
            """تحليل الملف المرفوع"""
            if file is None:
                return [
                    "⚠️ يرجى رفع ملف بيانات أولاً",
                    pd.DataFrame(),
                    "لا توجد بيانات للعرض"
                ]
            
            try:
                # قراءة الملف
                df = pd.read_csv(file.name)
                
                # معلومات الملف
                file_info_text = f"""
                ✅ تم تحميل الملف بنجاح
                
                📊 معلومات الملف:
                - عدد الصفوف: {len(df):,}
                - عدد الأعمدة: {len(df.columns)}
                - الحقول المتاحة: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}
                
                📈 ملخص سريع:
                - القيم المفقودة: {df.isnull().sum().sum()}
                - القيم المكررة: {df.duplicated().sum()}
                """
                
                return [
                    file_info_text,
                    df.head(10),
                    df.describe().to_string()
                ]
                
            except Exception as e:
                error_message = f"""
                ❌ حدث خطأ في تحليل الملف
                
                التفاصيل: {str(e)}
                
                نصائح:
                1. تأكد أن الملف بصيغة CSV
                2. تأكد من ترميز الملف (يفضل UTF-8)
                3. تأكد من صحة هيكل البيانات
                """
                return [error_message, pd.DataFrame(), ""]
        
        def switch_section(section):
            """التبديل بين أقسام الواجهة"""
            sections = [prediction_section, analysis_section]
            visibility = [False, False]
            
            if section == "prediction":
                visibility[0] = True
            elif section == "analysis":
                visibility[1] = True
            
            return [gr.update(visible=v) for v in visibility]
        
        # ===========================================
        # ربط الأحداث
        # ===========================================
        
        # أحداث التنقل
        nav_predict.click(
            fn=lambda: switch_section("prediction"),
            outputs=[prediction_section, analysis_section]
        )
        
        nav_analyze.click(
            fn=lambda: switch_section("analysis"),
            outputs=[prediction_section, analysis_section]
        )
        
        # أحداث التنبؤ
        predict_btn.click(
            fn=predict_score,
            inputs=[hours_studied, attendance_rate, previous_scores, tutoring_sessions, peer_influence],
            outputs=results_display
        )
        
        reset_btn.click(
            fn=clear_prediction_inputs,
            outputs=[hours_studied, attendance_rate, previous_scores, tutoring_sessions, peer_influence, results_display]
        )
        
        # أحداث تحليل البيانات
        analyze_file_btn.click(
            fn=analyze_uploaded_file,
            inputs=file_upload,
            outputs=[file_info, data_preview, statistics_display]
        )
        
        clear_analysis_btn.click(
            fn=lambda: ["", pd.DataFrame(), ""],
            outputs=[file_info, data_preview, statistics_display]
        )
    
    return app

# ============================================================================
# 7. دالة التشغيل الرئيسية
# ============================================================================
def run_application():
    """تشغيل التطبيق"""
    
    print("=" * 60)
    print("🎓 نظام التنبؤ الذكي بأداء الطلاب")
    print("=" * 60)
    print("\n✅ التطبيق يعمل الآن...")
    print("🌐 افتح المتصفح على: http://localhost:7860")
    print("=" * 60)
    
    # إنشاء التطبيق
    app = create_simple_interface()
    
    # تشغيل التطبيق
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
        show_error=True
    )

# ============================================================================
# 8. نقطة الدخول الرئيسية
# ============================================================================
if __name__ == "__main__":
    run_application()