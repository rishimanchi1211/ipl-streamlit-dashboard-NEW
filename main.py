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

    /* --- NEW ANALYTICAL OBJECTIVE STYLING --- */
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
