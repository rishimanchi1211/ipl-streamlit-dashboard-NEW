import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

st.set_page_config(
    page_title="IPL Analytics Hub",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #f4f7fa;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
    }

    /* --- TOP HEADER STYLING --- */
    .glow-header-container {
        background: linear-gradient(135deg, #0A1A3C 0%, #1B3A6B 100%);
        padding: 25px 35px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 25px;
        box-shadow: 0 10px 30px -5px rgba(27, 58, 107, 0.4), inset 0 0 10px rgba(255,255,255,0.1);
        margin-bottom: 30px;
        margin-top: -10px;
        border: 1px solid #2c4a7c;
        flex-wrap: wrap;
    }

    .ipl-logo-glow {
        width: 70px;
        filter: brightness(0) invert(1) drop-shadow(0 0 8px rgba(255,255,255,0.5));
    }

    .glow-text {
        color: #FFFFFF !important;
        margin: 0;
        font-size: clamp(28px, 5vw, 42px);
        font-weight: 800;
        letter-spacing: 1px;
        text-shadow: 0 0 15px rgba(255,255,255,0.5);
    }

    /* --- NEW PREMIUM ANALYTICAL OBJECTIVE --- */
    .objective-wrapper {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-bottom: 40px;
    }

    .analytical-objective {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 24px;
        padding: 35px 45px;
        max-width: 900px;
        box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
        text-align: center;
        position: relative;
        z-index: 10;
        transition: transform 0.3s ease;
    }

    .analytical-objective:hover {
        transform: translateY(-3px);
        box-shadow: 0 25px 50px -15px rgba(15, 23, 42, 0.12);
    }

    .obj-title {
        font-family: 'Outfit', sans-serif;
        font-size: clamp(20px, 3vw, 26px);
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        /* Beautiful gradient text */
        background: linear-gradient(90deg, #2563eb, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }

    .obj-text {
        color: #475569;
        font-size: clamp(15px, 2.5vw, 17px);
        line-height: 1.8;
        font-weight: 500;
    }

    /* --- NEW PREMIUM INSIGHT CARDS --- */
    .insight-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 25px 30px;
        margin-top: 30px;
        margin-bottom: 15px;
        position: relative;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04);
        border: 1px solid #f1f5f9;
        display: flex;
        gap: 20px;
        align-items: flex-start;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .insight-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 20px 35px -10px rgba(139, 92, 246, 0.15);
        border-color: #ddd6fe;
    }

    .insight-icon {
        background: linear-gradient(135deg, #8b5cf6, #3b82f6);
        color: white;
        min-width: 50px;
        height: 50px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 8px 16px -6px rgba(139, 92, 246, 0.6);
        flex-shrink: 0;
    }

    .insight-content {
        color: #334155;
        font-size: clamp(14px, 2.5vw, 15px);
        line-height: 1.7;
    }

    .insight-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        color: #0f172a;
        font-size: 19px;
        margin-bottom: 8px;
        display: block;
        letter-spacing: 0.5px;
    }

    /* --- EXISTING STYLES --- */
    .logo-banner {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 35px;
    }

    .logo-card {
        background: white;
        border-radius: 14px;
        padding: 10px 18px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .logo-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.08);
        border-color: #3b82f6;
    }

    .logo-card img {
        height: clamp(35px, 5vw, 55px);
        object-fit: contain;
    }

    [data-testid="stPlotlyChart"], .stDataFrame {
        background-color: white;
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        border: 1px solid #e2e8f0;
        width: 100%;
        overflow-x: auto;
    }

    .stTabs [data-baseweb="tab-list"] { 
        gap: 12px; 
        padding-bottom: 15px;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] { 
        border-radius: 10px; 
        background-color: #fff; 
        border: 1px solid #e2e8f0; 
        padding: 10px 20px;
        margin-bottom: 5px;
        font-size: clamp(13px, 3vw, 16px);
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] { 
        background-color: #eff6ff; 
        border-color: #3b82f6; 
        color: #1e40af; 
        border-bottom: 3px solid #2563eb !important;
    }

    .kpi-wrapper {
        background-color: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.03);
        border: 1px solid #e2e8f0;
        display: flex;
        flex-direction: column;
        transition: all 0.3s ease;
        margin-bottom: 15px;
        align-items: center;
        text-align: center;
    }
    
    .kpi-wrapper:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 25px rgba(0,0,0,0.08);
        border-color: #3b82f6;
    }
    
    .kpi-title {
        color: #64748b;
        font-size: clamp(12px, 2vw, 14px);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    
    .kpi-value {
        color: #0f172a;
        font-family: 'Outfit', sans-serif;
        font-size: clamp(28px, 5vw, 40px);
        font-weight: 800;
        line-height: 1.2;
    }
    
    .kpi-icon {
        font-size: clamp(24px, 4vw, 32px);
        margin-bottom: 10px;
    }
    
    /* Mobile Adjustments */
    @media (max-width: 768px) {
        .glow-header-container { padding: 20px; gap: 15px; }
        .ipl-logo-glow { width: 55
