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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #f4f7f9;
    }

    .glow-header-container {
        background: linear-gradient(135deg, #0A1A3C 0%, #1B3A6B 100%);
        padding: 25px 35px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        gap: 25px;
        box-shadow: 0 0 25px rgba(66, 153, 225, 0.5), inset 0 0 10px rgba(255,255,255,0.1);
        margin-bottom: 30px;
        margin-top: -20px;
        border: 1px solid #2c4a7c;
        flex-wrap: wrap;
        justify-content: center;
    }

    .ipl-logo-glow {
        width: 75px;
        filter: brightness(0) invert(1) drop-shadow(0 0 5px rgba(255,255,255,0.6));
    }

    .glow-text {
        color: #FFFFFF !important;
        margin: 0;
        font-size: clamp(24px, 4vw, 36px);
        font-weight: 800;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(255,255,255,0.7);
        text-align: center;
    }

    /* --- ANALYTICAL OBJECTIVE STYLING --- */
    .analytical-objective {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        color: #f8fafc;
        padding: 24px 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
        border: 1px solid #334155;
        font-size: clamp(15px, 2.5vw, 17px);
        line-height: 1.7;
        text-align: center;
        position: relative;
    }

    .analytical-objective strong {
        color: #38bdf8;
        font-size: clamp(18px, 3vw, 22px);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        display: block;
        margin-bottom: 12px;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }

    /* --- ANALYSIS TEXT STYLING --- */
    .analysis-text {
        background: linear-gradient(to right, #f8fafc, #ffffff);
        padding: 20px 25px;
        border-radius: 12px;
        border-left: 5px solid #8b5cf6;
        border-top: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        color: #475569;
        margin-top: 25px;
        font-size: clamp(14px, 2.5vw, 15px);
        line-height: 1.8;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .analysis-text:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
        border-left-color: #7c3aed;
    }
    
    .analysis-text strong {
        color: #7c3aed;
        font-weight: 800;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-right: 5px;
    }

    .logo-banner {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 30px;
    }

    .logo-card {
        background: white;
        border-radius: 12px;
        padding: 10px 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .logo-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
        border-color: #3b82f6;
    }

    .logo-card img {
        height: clamp(35px, 5vw, 55px);
        object-fit: contain;
    }

    [data-testid="stPlotlyChart"], .stDataFrame {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        width: 100%;
        overflow-x: auto;
    }

    .stTabs [data-baseweb="tab-list"] { 
        gap: 10px; 
        padding-bottom: 10px;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] { 
        border-radius: 8px; 
        background-color: #fff; 
        border: 1px solid #e2e8f0; 
        padding: 8px 16px;
        margin-bottom: 5px;
        font-size: clamp(12px, 3vw, 16px);
    }
    
    .stTabs [aria-selected="true"] { 
        background-color: #ebf8ff; 
        border-color: #3b82f6; 
        color: #1e40af; 
        font-weight: 600; 
        border-bottom: 3px solid #3b82f6 !important;
    }

    .kpi-wrapper {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        display: flex;
        flex-direction: column;
        transition: all 0.3s ease;
        margin-bottom: 10px;
        align-items: center;
        text-align: center;
    }
    
    .kpi-wrapper:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
        border-color: #3b82f6;
    }
    
    .kpi-title {
        color: #64748b;
        font-size: clamp(11px, 2vw, 14px);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        color: #0f172a;
        font-size: clamp(24px, 5vw, 36px);
        font-weight: 800;
        line-height: 1.2;
    }
    
    .kpi-icon {
        font-size: clamp(20px, 4vw, 28px);
        margin-bottom: 8px;
    }
    
    @media (max-width: 768px) {
        .glow-header-container {
            padding: 15px;
            gap: 15px;
        }
        .ipl-logo-glow
