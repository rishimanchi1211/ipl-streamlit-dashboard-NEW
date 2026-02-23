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

    /* --- PREMIUM ANALYTICAL OBJECTIVE --- */
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

    /* --- PREMIUM INSIGHT CARDS --- */
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
