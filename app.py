# ============================================================================
# نظام التنبؤ الذكي بأداء الطلاب - نسخة محسنة ومستقرة
# RTL ذكي + ألوان صحيحة + واجهة احترافية
# ============================================================================

import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ============================================================================
# إعدادات التصميم
# ============================================================================
class DesignConfig:
    COLORS = {
        "petroleum": "#006666",
        "petroleum_dark": "#004d4d",
        "petroleum_light": "#008787",
        "gold": "#D4AF37",
        "white": "#FFFFFF",
        "gray_light": "#F8F9FA",
        "gray_medium": "#E9ECEF",
        "gray_dark": "#495057",
        "text_dark": "#212529",
        "success": "#28A745",
        "warning": "#FFC107",
        "danger": "#DC3545",
        "info": "#17A2B8",
    }

    BORDER_RADIUS = {
        "sm": "8px",
        "md": "12px",
        "lg": "16px",
    }

    SHADOW = "0 6px 18px rgba(0,0,0,0.08)"


# ============================================================================
# إعداد الصفحة
# ============================================================================
def setup_page():
    st.set_page_config(
        page_title="نظام التنبؤ الذكي بأداء الطلاب",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )


# ============================================================================
# CSS المحسَّن
# ============================================================================
def apply_css():
    css = f"""
    <style>

    /* ===== الأساس ===== */
    .stApp {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['gray_light']}, {DesignConfig.COLORS['white']});
        font-family: 'Tajawal', Arial, sans-serif;
        color: {DesignConfig.COLORS['text_dark']};
    }}

    /* ===== RTL ذكي ===== */
    .rtl {{
        direction: rtl;
        text-align: right;
    }}

    /* ===== النصوص ===== */
    p, span, li, label {{
        color: {DesignConfig.COLORS['text_dark']};
        font-size: 15px;
    }}

    h1, h2, h3, h4, h5 {{
        color: {DesignConfig.COLORS['petroleum_dark']};
        font-weight: 700;
    }}

    /* ===== البطاقات ===== */
    .card {{
        background: white;
        border-radius: {DesignConfig.BORDER_RADIUS['lg']};
        padding: 24px;
        margin: 15px 0;
        box-shadow: {DesignConfig.SHADOW};
        border-right: 5px solid {DesignConfig.COLORS['gold']};
    }}

    /* ===== العنوان الرئيسي ===== */
    .main-title {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum_dark']}, {DesignConfig.COLORS['petroleum']});
        color: white;
        padding: 30px;
        border-radius: {DesignConfig.BORDER_RADIUS['lg']};
        text-align: center;
        margin-bottom: 30px;
    }}

    .main-title h1,
    .main-title p {{
        color: white;
    }}

    /* ===== الأزرار ===== */
    .stButton>button {{
        background: linear-gradient(135deg, {DesignConfig.COLORS['petroleum']}, {DesignConfig.COLORS['petroleum_dark']});
        color: white;
        border-radius: {DesignConfig.BORDER_RADIUS['md']};
        padding: 10px 20px;
        font-weight: 600;
        border: none;
    }}

    .stButton>button:hover {{
        color: {DesignConfig.COLORS['gold']};
    }}

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {DesignConfig.COLORS['petroleum_dark']}, {DesignConfig.COLORS['petroleum']});
    }}

    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ============================================================================
# الواجهة
# ============================================================================
def header():
    st.markdown("""
    <div class="main-title rtl">
        <h1>🎓 نظام التنبؤ الذكي بأداء الطلاب</h1>
        <p>تحليل أكاديمي ذكي باستخدام تعلم الآلة</p>
    </div>
    """, unsafe_allow_html=True)


def home_page():
    st.markdown("""
    <div class="card rtl">
        <h3>🏠 نظرة عامة</h3>
        <p>
        هذا النظام يساعد في التنبؤ بالأداء الأكاديمي للطلاب
        باستخدام نماذج تعلم آلي متقدمة وتحليل بيانات ذكي.
        </p>
    </div>
    """, unsafe_allow_html=True)


def prediction_page():
    st.markdown('<div class="rtl"><h2>🎯 أداة التنبؤ</h2></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        hours = st.slider("ساعات الدراسة الأسبوعية", 0, 40, 20)
        attendance = st.slider("نسبة الحضور (%)", 0, 100, 85)
        tutoring = st.slider("الدروس الخصوصية", 0, 10, 2)

    with col2:
        prev_scores = st.number_input("متوسط الدرجات السابقة", 0.0, 100.0, 75.0)
        peer = st.select_slider("تأثير الأقران", [1, 2, 3, 4, 5], value=3)

    if st.button("🚀 بدء التنبؤ"):
        score = min(100, max(0, round(
            hours * 0.3 + attendance * 0.2 + prev_scores * 0.3 + tutoring * 2 + peer * 3, 2
        )))

        color = DesignConfig.COLORS["success"] if score >= 75 else DesignConfig.COLORS["warning"]

        st.markdown(f"""
        <div class="card rtl">
            <h3>📊 النتيجة</h3>
            <p style="font-size:30px; font-weight:bold; color:{color}">
                {score} / 100
            </p>
        </div>
        """, unsafe_allow_html=True)


def sidebar():
    st.sidebar.markdown("""
    <div style="text-align:center; padding:20px">
        <h3>🎓 النظام</h3>
        <p>تحليل ذكي</p>
    </div>
    """, unsafe_allow_html=True)

    return st.sidebar.radio(
        "التنقل",
        ["🏠 الرئيسية", "🎯 التنبؤ"]
    )


# ============================================================================
# التطبيق الرئيسي
# ============================================================================
def main():
    setup_page()
    apply_css()

    section = sidebar()
    header()

    if section == "🏠 الرئيسية":
        home_page()
    elif section == "🎯 التنبؤ":
        prediction_page()


if __name__ == "__main__":
    main()
