import math
import re
from pathlib import Path
from urllib.parse import quote

import numpy as np
import pandas as pd
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap

# ============================================================
# QUANTYX 86 — Estadística fácil
# ============================================================

DARK_LOGO_PATH = Path(__file__).with_name("Quantyx 86_ Neon Data Emblem-1.png")
LIGHT_LOGO_PATH = Path(__file__).with_name("Quantyx 86 Neon Data Emblem-2.png")
PAGE_ICON_PATH = Path(__file__).with_name("Neon Data Emblem_ Quantyx 86-3.png")

st.set_page_config(
    page_title="Quantyx 86 | Estadística fácil",
    page_icon=PAGE_ICON_PATH,
    layout="wide",
    initial_sidebar_state="collapsed",
)

THEME_PALETTES = {
    "dark": {
        "background": "#282828",
        "panel": "#3c3836",
        "secondary": "#504945",
        "text": "#ebdbb2",
        "muted": "#d5c4a1",
        "border": "#665c54",
        "accent": "#fabd2f",
        "button_text": "#282828",
        "glyph": "#a89984",
        "grid": "rgba(168, 153, 132, .28)",
        "table_alt": "rgba(80, 73, 69, .72)",
    },
    "light": {
        "background": "#fbf1c7",
        "panel": "#ebdbb2",
        "secondary": "#f2e5bc",
        "text": "#3c3836",
        "muted": "#665c54",
        "border": "#a89984",
        "accent": "#d79921",
        "button_text": "#282828",
        "glyph": "#928374",
        "grid": "rgba(102, 92, 84, .32)",
        "table_alt": "#f2e5bc",
    },
}
dark_mode = st.session_state.get("theme-dark-mode", True)
theme_palette = THEME_PALETTES["dark" if dark_mode else "light"]

# ----------------------------- ESTILOS ----------------------------
st.markdown("""
<style>
/* 1. RESET Y FONDO */
html, body, [class*="css"] { 
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
.stApp {
    background:
        radial-gradient(ellipse at 12% 8%, rgba(216, 180, 254, 0.45), transparent 34%),
        radial-gradient(ellipse at 88% 18%, rgba(153, 246, 228, 0.4), transparent 32%),
        radial-gradient(ellipse at 72% 92%, rgba(251, 207, 232, 0.42), transparent 38%),
        linear-gradient(135deg, #f9f7ff 0%, #f3f8ff 52%, #f5fffc 100%);
    color: #243047;
    background-attachment: fixed;
}

/* 2. TARJETAS GLASS (Usando clases propias en lugar de border=True) */
.glass-card {
    background: rgba(255, 255, 255, 0.55) !important;
    backdrop-filter: blur(20px) saturate(160%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(160%) !important;
    border: 1px solid rgba(255, 255, 255, 0.9) !important;
    border-radius: 24px !important;
    box-shadow: 0 12px 35px -5px rgba(112, 71, 245, 0.12), inset 0 1px 0 rgba(255,255,255,0.9) !important;
    padding: 1.8rem !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    margin-bottom: 20px;
}
.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 45px -5px rgba(112, 71, 245, 0.2), inset 0 1px 0 rgba(255,255,255,1) !important;
}

/* 3. TEXTAREA (Forzar transparencia) */
[data-testid="stSidebar"] .stTextArea textarea {
    background: rgba(255, 255, 255, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 1) !important;
    border-radius: 16px !important;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.02) !important;
    color: #1F2937 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 12px !important;
}
[data-testid="stSidebar"] .stTextArea textarea:focus {
    border-color: #A78BFA !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.2) !important;
}

/* 4. SIDEBAR */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.5) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.8) !important;
}

/* 5. BOTONES */
.stButton > button {
    background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.6rem 1.2rem !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 6px 18px -4px rgba(109, 40, 217, 0.4) !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 22px -4px rgba(109, 40, 217, 0.5) !important;
}

/* 6. TÍTULOS */
h1, h2, h3, h4 {
    font-family: 'Manrope', sans-serif !important;
    color: #111827 !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    margin-top: 0;
}
.hero-title {
    font-size: 2.8rem;
    background: -webkit-linear-gradient(45deg, #6D28D9, #3B82F6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
    line-height: 1.1;
}
.hero-sub {
    color: #6B7280;
    font-size: 1.1rem;
    margin-top: 8px;
    font-weight: 500;
}

/* 7. MÉTRICAS */
div[data-testid="stMetric"] {
    background: transparent !important;
    padding: 0 !important;
}
div[data-testid="stMetricLabel"] {
    font-family: 'Manrope', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    color: #6B7280 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
div[data-testid="stMetricValue"] {
    font-family: 'Manrope', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: #111827 !important;
}

/* 8. TABLAS */
[data-testid="stDataFrame"] {
    background: rgba(255, 255, 255, 0.7) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 1) !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.02) !important;
    padding: 10px;
}
[data-testid="stDataFrame"] * {
    color: #1F2937 !important;
}

/* 9. BADGES */
.badge {
    background: rgba(16, 185, 129, 0.15);
    color: #047857;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    display: inline-block;
    margin-bottom: 15px;
}

/* 10. ACABADO, CONTRASTE Y ACCESIBILIDAD */
.main .block-container {
    max-width: 1500px;
    padding: 2.5rem clamp(1rem, 3vw, 3rem) 4rem;
}

p, li, label, [data-testid="stCaptionContainer"] {
    color: #40506a;
    line-height: 1.65;
}

.hero-title {
    color: #4c2882;
    background: linear-gradient(100deg, #54258b 5%, #315c91 58%, #187d70 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    color: #46566e;
}

.glass-card,
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.72) !important;
    border: 1px solid rgba(255, 255, 255, 0.96) !important;
    border-radius: 24px !important;
    box-shadow: 0 14px 38px rgba(67, 56, 103, 0.09),
                inset 0 1px 0 rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(18px) saturate(145%) !important;
    -webkit-backdrop-filter: blur(18px) saturate(145%) !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    padding: 0.35rem 0.7rem !important;
    transition: transform 180ms ease, box-shadow 180ms ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 42px rgba(67, 56, 103, 0.13),
                inset 0 1px 0 rgba(255, 255, 255, 0.95) !important;
}

.glass-card {
    color: #243047 !important;
}

.glass-card p,
.glass-card span {
    color: #46566e !important;
}

[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.78) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.95) !important;
    box-shadow: 8px 0 32px rgba(67, 56, 103, 0.06);
    backdrop-filter: blur(22px) saturate(145%) !important;
    -webkit-backdrop-filter: blur(22px) saturate(145%) !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] label {
    color: #34445d !important;
}

[data-testid="stSidebar"] .stTextArea textarea {
    background: rgba(255, 255, 255, 0.94) !important;
    color: #1f2c42 !important;
    border: 1px solid #d9d4eb !important;
    line-height: 1.65 !important;
}

[data-testid="stSidebar"] .stTextArea textarea::placeholder {
    color: #66748a !important;
    opacity: 1;
}

.stButton > button,
.stDownloadButton > button {
    min-height: 2.8rem;
    border-radius: 14px !important;
    font-weight: 750 !important;
    transition: transform 180ms ease, box-shadow 180ms ease !important;
}

.stButton > button:focus-visible,
.stDownloadButton > button:focus-visible,
[data-testid="stSidebar"] .stTextArea textarea:focus-visible {
    outline: 3px solid #7c3aed !important;
    outline-offset: 3px !important;
}

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.58) !important;
    border: 1px solid rgba(255, 255, 255, 0.92) !important;
    border-radius: 16px !important;
    padding: 0.8rem !important;
}

div[data-testid="stMetricLabel"] {
    color: #52617a !important;
}

div[data-testid="stMetricValue"] {
    color: #202b42 !important;
}

[data-testid="stDataFrame"] {
    overflow: hidden;
    border: 1px solid #e3deef !important;
    border-radius: 16px !important;
}

[data-testid="stDataFrame"] * {
    color: #26344b !important;
}

[data-testid="stAlert"] {
    border-radius: 16px !important;
}

.badge {
    background: rgba(124, 58, 237, 0.12);
    color: #54258b;
    border: 1px solid rgba(124, 58, 237, 0.16);
}

@media (max-width: 700px) {
    .main .block-container {
        padding: 1.25rem 1rem 2.5rem;
    }

    .hero-title {
        font-size: 2.1rem;
    }

    .hero-sub {
        font-size: 1rem;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
        animation-duration: 0.01ms !important;
    }
}

/* Ajustes finales: el tema de Streamlit también colorea el texto interno de los botones. */
html, body, [data-testid="stAppViewContainer"] {
    font-family: Inter, "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stMarkdown p,
.stCaptionContainer,
[data-testid="stSidebar"] label {
    font-size: 0.98rem;
}

h1, h2, h3, h4,
.stButton > button,
.stDownloadButton > button {
    font-family: Inter, "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.glass-card,
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(
        145deg,
        rgba(255, 255, 255, 0.84),
        rgba(244, 239, 255, 0.72) 58%,
        rgba(235, 250, 249, 0.7)
    ) !important;
    border: 1px solid rgba(255, 255, 255, 0.96) !important;
    box-shadow: 0 16px 38px rgba(67, 56, 103, 0.11),
                inset 0 1px 0 rgba(255, 255, 255, 0.98) !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(99, 82, 130, 0.18) !important;
}

[data-testid="stSidebar"] div[data-baseweb="textarea"] {
    overflow: hidden;
    background: rgba(255, 255, 255, 0.94) !important;
    border: 1px solid #d7cbea !important;
    border-radius: 14px !important;
    box-shadow: 0 3px 12px rgba(67, 56, 103, 0.06) !important;
}

[data-testid="stSidebar"] div[data-baseweb="textarea"]:focus-within {
    border-color: #8052c8 !important;
    box-shadow: 0 0 0 3px rgba(128, 82, 200, 0.17) !important;
}

[data-testid="stSidebar"] .stTextArea textarea {
    background: transparent !important;
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    color: #26344b !important;
    font-size: 0.96rem !important;
}

.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(120deg, #7140c5, #51309d) !important;
    border: 1px solid rgba(73, 40, 137, 0.22) !important;
    color: #fff !important;
    box-shadow: 0 8px 18px rgba(81, 48, 157, 0.26) !important;
}

.stButton > button[kind="primary"] *,
.stButton > button[data-testid="stBaseButton-primary"] * {
    color: #fff !important;
}

.stButton > button[kind="secondary"],
.stButton > button[data-testid="stBaseButton-secondary"] {
    background: rgba(255, 255, 255, 0.82) !important;
    border: 1px solid #d8cdec !important;
    color: #49356d !important;
    box-shadow: 0 4px 12px rgba(67, 56, 103, 0.08) !important;
}

.stButton > button[kind="secondary"] *,
.stButton > button[data-testid="stBaseButton-secondary"] * {
    color: #49356d !important;
}

.stDownloadButton > button {
    background: rgba(255, 255, 255, 0.82) !important;
    border: 1px solid #d8cdec !important;
    color: #49356d !important;
}

.stDownloadButton > button * {
    color: #49356d !important;
}

.stApp {
    background:
        radial-gradient(ellipse at 9% 9%, rgba(201, 168, 255, 0.42), transparent 32%),
        radial-gradient(ellipse at 92% 17%, rgba(144, 235, 220, 0.38), transparent 30%),
        radial-gradient(ellipse at 78% 92%, rgba(255, 191, 215, 0.30), transparent 35%),
        #f7f6fc !important;
    background-attachment: fixed !important;
}

[data-testid="stSidebar"] {
    display: none !important;
}

.main .block-container {
    max-width: 1480px !important;
    padding: .8rem clamp(1rem, 3vw, 2.6rem) 2rem !important;
}

.stMarkdown, .stText, .stCaptionContainer, label {
    color: #3e4960;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, rgba(255,255,255,.82), rgba(250,247,255,.74) 55%, rgba(240,253,250,.72)) !important;
    border: 1px solid rgba(255,255,255,.95) !important;
    border-radius: 26px !important;
    box-shadow: 0 16px 42px rgba(80, 66, 122, .10), inset 0 1px 0 rgba(255,255,255,.95) !important;
    backdrop-filter: blur(22px) saturate(145%) !important;
    -webkit-backdrop-filter: blur(22px) saturate(145%) !important;
    padding: clamp(1rem, 2.5vw, 1.7rem) !important;
}

[data-testid="stTextArea"] label {
    color: #37445c !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
}

div[data-baseweb="textarea"] {
    background: rgba(255,255,255,.92) !important;
    border: 1px solid #dcd4ed !important;
    border-radius: 17px !important;
    box-shadow: 0 4px 14px rgba(60, 48, 96, .06) !important;
    overflow: hidden !important;
}

div[data-baseweb="textarea"]:hover {
    border-color: #b8a4df !important;
}

div[data-baseweb="textarea"]:focus-within {
    border-color: #7952bd !important;
    box-shadow: 0 0 0 3px rgba(121,82,189,.16) !important;
}

div[data-baseweb="textarea"] textarea {
    background: transparent !important;
    color: #26334b !important;
    -webkit-text-fill-color: #26334b !important;
    caret-color: #5f3c9b !important;
    border: 0 !important;
    box-shadow: none !important;
    font-family: Inter, "Segoe UI", sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
    padding: .9rem 1rem !important;
}

div[data-baseweb="textarea"] textarea::placeholder {
    color: #78839a !important;
    -webkit-text-fill-color: #78839a !important;
    opacity: 1 !important;
}

.stButton > button,
.stDownloadButton > button {
    min-height: 2.9rem;
    border-radius: 15px !important;
    font-weight: 700 !important;
    transition: transform .18s ease, box-shadow .18s ease !important;
}

.stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(115deg, #7146b6, #59368f) !important;
    color: #fff !important;
    border: 1px solid rgba(74, 44, 125, .22) !important;
    box-shadow: 0 9px 20px rgba(89, 54, 143, .24) !important;
}

.stButton > button[data-testid="stBaseButton-primary"] *,
.stButton > button[kind="primary"] * {
    color: #fff !important;
}

.stButton > button[data-testid="stBaseButton-secondary"],
.stDownloadButton > button {
    background: rgba(255,255,255,.77) !important;
    color: #513b71 !important;
    border: 1px solid #d9cfea !important;
    box-shadow: 0 4px 12px rgba(73, 56, 112, .07) !important;
}

.stButton > button[data-testid="stBaseButton-secondary"] *,
.stDownloadButton > button * {
    color: #513b71 !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px);
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,.55) !important;
    border: 1px solid rgba(255,255,255,.9) !important;
    border-radius: 18px !important;
    padding: .9rem !important;
}

div[data-testid="stMetricLabel"] {
    color: #59667d !important;
    font-size: .78rem !important;
    font-weight: 700 !important;
}

div[data-testid="stMetricValue"] {
    color: #28334a !important;
}

[data-testid="stTabs"] button {
    color: #59667d !important;
    font-weight: 650 !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    color: #59368f !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #e3deef !important;
    border-radius: 15px !important;
    overflow: hidden !important;
}

.hero-kicker {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .4rem .8rem;
    border: 1px solid rgba(112, 78, 162, .14);
    border-radius: 999px;
    background: rgba(255,255,255,.62);
    color: #63458d;
    font-size: .76rem;
    font-weight: 750;
    letter-spacing: .08em;
    text-transform: none;
}

.hero-heading {
    margin: .7rem 0 .4rem;
    color: #34284d;
    font-size: clamp(2rem, 3.5vw, 3rem);
    font-weight: 800;
    letter-spacing: -.055em;
    line-height: 1.05;
}

.hero-heading span {
    color: #7952ad;
}

.hero-copy {
    max-width: 650px;
    margin: 0 0 .8rem;
    color: #566178;
    font-size: 1rem;
    line-height: 1.55;
}

.insight-strip {
    display: flex;
    align-items: center;
    gap: .75rem;
    margin: .5rem 0 .9rem;
    padding: .75rem 1rem;
    border: 1px solid rgba(255,255,255,.88);
    border-radius: 18px;
    background: linear-gradient(105deg, rgba(255,246,215,.72), rgba(255,255,255,.65) 48%, rgba(223,247,239,.68));
    box-shadow: 0 8px 22px rgba(84,74,108,.06);
    color: #554663;
    font-size: .9rem;
    line-height: 1.5;
}

.insight-icon {
    display: grid;
    flex: 0 0 2.15rem;
    width: 2.15rem;
    height: 2.15rem;
    place-items: center;
    border-radius: 13px;
    background: rgba(255,255,255,.82);
    font-size: 1.15rem;
}

.hero-compact .hero-heading {
    font-size: clamp(1.7rem, 2.8vw, 2.3rem);
    margin-top: .55rem;
}

.hero-compact .hero-copy {
    margin-bottom: .35rem;
}

.stButton > button[data-testid="stBaseButton-tertiary"] {
    min-height: 2rem;
    padding: .25rem .55rem !important;
    border: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    color: #67547f !important;
}

.stButton > button[data-testid="stBaseButton-tertiary"] * {
    color: #67547f !important;
}

.st-key-data-card {
    padding: .9rem 1.1rem !important;
}

.st-key-data-card [data-testid="stTextArea"] textarea {
    min-height: 68px !important;
}

.st-key-chart-card,
.st-key-table-card {
    padding: 1rem 1.1rem !important;
}

.st-key-table-card [data-testid="stDataFrame"] {
    max-height: 275px;
}

.section-eyebrow {
    color: #76599c;
    font-size: .75rem;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
}

@media (max-width: 640px) {
    .main .block-container {
        padding: .7rem .8rem 1.8rem !important;
    }

    .hero-copy {
        font-size: .97rem;
    }

    .result-card [data-testid="stVerticalBlockBorderWrapper"] {
        padding: .8rem !important;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        scroll-behavior: auto !important;
        transition: none !important;
    }
}

/* Ocultar elementos de Streamlit */
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { visibility: hidden; }
footer { display: none; }

:root {
    color-scheme: dark;
}

.stApp,
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 12% 8%, rgba(211, 134, 155, .11), transparent 34%),
        radial-gradient(ellipse at 88% 16%, rgba(131, 165, 152, .12), transparent 32%),
        radial-gradient(ellipse at 74% 94%, rgba(215, 153, 33, .08), transparent 38%),
        #282828 !important;
    background-attachment: fixed !important;
    color: #ebdbb2 !important;
}

.stMarkdown,
.stText,
.stCaptionContainer,
p,
li,
label,
[data-testid="stCaptionContainer"] {
    color: #d5c4a1 !important;
}

h1,
h2,
h3,
h4,
.hero-heading {
    color: #fbf1c7 !important;
}

.hero-heading span {
    color: #fabd2f !important;
}

.hero-copy {
    color: #d5c4a1 !important;
}

.hero-kicker {
    color: #fabd2f !important;
    background: rgba(60, 56, 54, .82) !important;
    border-color: rgba(168, 153, 132, .34) !important;
}

.section-eyebrow {
    color: #d79921 !important;
}

.glass-card,
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(
        145deg,
        rgba(60, 56, 54, .94),
        rgba(50, 48, 46, .92) 58%,
        rgba(40, 40, 40, .9)
    ) !important;
    border: 1px solid rgba(168, 153, 132, .28) !important;
    box-shadow: 0 16px 38px rgba(0, 0, 0, .24),
                inset 0 1px 0 rgba(235, 219, 178, .08) !important;
    backdrop-filter: blur(18px) saturate(125%) !important;
    -webkit-backdrop-filter: blur(18px) saturate(125%) !important;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 18px 42px rgba(0, 0, 0, .32),
                inset 0 1px 0 rgba(235, 219, 178, .1) !important;
}

.glass-card,
.glass-card p,
.glass-card span {
    color: #d5c4a1 !important;
}

div[data-baseweb="textarea"] {
    background: rgba(40, 40, 40, .82) !important;
    border: 1px solid #665c54 !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, .18) !important;
}

div[data-baseweb="textarea"]:hover {
    border-color: #a89984 !important;
}

div[data-baseweb="textarea"]:focus-within {
    border-color: #fabd2f !important;
    box-shadow: 0 0 0 3px rgba(250, 189, 47, .2) !important;
}

div[data-baseweb="textarea"] textarea,
[data-testid="stSidebar"] .stTextArea textarea {
    color: #ebdbb2 !important;
    -webkit-text-fill-color: #ebdbb2 !important;
    caret-color: #fabd2f !important;
}

div[data-baseweb="textarea"] textarea::placeholder {
    color: #a89984 !important;
    -webkit-text-fill-color: #a89984 !important;
}

.stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(120deg, #d79921, #b57614) !important;
    border: 1px solid rgba(250, 189, 47, .45) !important;
    color: #282828 !important;
    box-shadow: 0 8px 18px rgba(0, 0, 0, .25) !important;
}

.stButton > button[data-testid="stBaseButton-primary"] *,
.stButton > button[kind="primary"] * {
    color: #282828 !important;
}

.stButton > button[data-testid="stBaseButton-secondary"],
.stDownloadButton > button {
    background: rgba(80, 73, 69, .78) !important;
    border: 1px solid #665c54 !important;
    color: #ebdbb2 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, .18) !important;
}

.stButton > button[data-testid="stBaseButton-secondary"] *,
.stDownloadButton > button * {
    color: #ebdbb2 !important;
}

.stButton > button[data-testid="stBaseButton-tertiary"],
.stButton > button[data-testid="stBaseButton-tertiary"] * {
    color: #d5c4a1 !important;
}

.stButton > button:focus-visible,
.stDownloadButton > button:focus-visible,
div[data-baseweb="textarea"]:focus-within {
    outline-color: #fabd2f !important;
}

div[data-testid="stMetric"] {
    background: rgba(40, 40, 40, .48) !important;
    border-color: rgba(168, 153, 132, .28) !important;
}

div[data-testid="stMetricLabel"] {
    color: #a89984 !important;
}

div[data-testid="stMetricValue"] {
    color: #fabd2f !important;
}

[data-testid="stTabs"] button,
[data-testid="stSegmentedControl"] button {
    color: #d5c4a1 !important;
}

[data-testid="stTabs"] button[aria-selected="true"],
[data-testid="stSegmentedControl"] button[aria-pressed="true"] {
    color: #fabd2f !important;
}

[data-testid="stDataFrame"] {
    background: rgba(40, 40, 40, .42) !important;
    border-color: #665c54 !important;
}

[data-testid="stDataFrame"] * {
    color: #ebdbb2 !important;
}

.insight-strip {
    color: #ebdbb2 !important;
    background: linear-gradient(105deg, rgba(102, 92, 84, .72), rgba(60, 56, 54, .78) 52%, rgba(69, 88, 72, .62)) !important;
    border-color: rgba(168, 153, 132, .28) !important;
    box-shadow: 0 8px 22px rgba(0, 0, 0, .18) !important;
}

.insight-icon {
    background: rgba(80, 73, 69, .9) !important;
}

.badge {
    background: rgba(250, 189, 47, .12) !important;
    color: #fabd2f !important;
    border-color: rgba(250, 189, 47, .28) !important;
}

[data-testid="stAlert"] {
    background: rgba(251, 73, 52, .12) !important;
    border-color: rgba(251, 73, 52, .35) !important;
    color: #fbf1c7 !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* Gruvbox retro finish */
html,
body,
[data-testid="stAppViewContainer"],
p,
label,
button,
textarea,
[data-testid="stCaptionContainer"] {
    font-family: "Inter", "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif !important;
}

h1,
h2,
h3,
h4 {
    font-family: "Pixelify Sans", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace !important;
}

.stApp,
[data-testid="stAppViewContainer"] {
    background: #282828 !important;
    background-image: none !important;
}

.stMarkdown,
.stText,
.stCaptionContainer,
p,
li,
label,
[data-testid="stCaptionContainer"] {
    color: #d5c4a1 !important;
}

h1,
h2,
h3,
h4,
.hero-heading {
    color: #fbf1c7 !important;
    letter-spacing: 0 !important;
}

.hero-heading span,
.section-eyebrow {
    color: #fabd2f !important;
}

.hero-kicker,
.badge {
    background: #3c3836 !important;
    color: #fabd2f !important;
    border: 2px solid #665c54 !important;
    border-radius: 999px !important;
    box-shadow: none !important;
}

.glass-card,
[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stMetric"],
[data-testid="stDataFrame"] {
    background: #3c3836 !important;
    border: 2px solid #665c54 !important;
    border-radius: 18px !important;
    box-shadow: none !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    transition: border-color 160ms ease, transform 160ms ease !important;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: none !important;
    transform: translateY(-2px) !important;
}

.glass-card,
.glass-card p,
.glass-card span,
.hero-copy,
div[data-testid="stMetricLabel"] {
    color: #d5c4a1 !important;
}

div[data-testid="stMetricValue"] {
    color: #fabd2f !important;
}

.insight-strip {
    background: #504945 !important;
    color: #fbf1c7 !important;
    border: 2px solid #d79921 !important;
    border-radius: 16px !important;
    box-shadow: none !important;
}

.insight-icon {
    background: #3c3836 !important;
    border: 2px solid #665c54 !important;
    border-radius: 12px !important;
}

div[data-baseweb="textarea"] {
    background: #282828 !important;
    border: 2px solid #665c54 !important;
    border-radius: 12px !important;
    box-shadow: none !important;
    transition: border-color 140ms ease, box-shadow 140ms ease !important;
}

div[data-baseweb="textarea"]:focus-within {
    border-color: #fabd2f !important;
    box-shadow: none !important;
    outline: 2px solid #fabd2f !important;
}

div[data-baseweb="textarea"] textarea,
[data-testid="stSidebar"] .stTextArea textarea {
    background: transparent !important;
    color: #ebdbb2 !important;
    -webkit-text-fill-color: #ebdbb2 !important;
}

div[data-baseweb="textarea"] textarea::placeholder {
    color: #a89984 !important;
    -webkit-text-fill-color: #a89984 !important;
}

.stButton > button,
.stDownloadButton > button {
    border: 2px solid #665c54 !important;
    border-radius: 12px !important;
    box-shadow: none !important;
    transition: transform 160ms ease, filter 160ms ease !important;
}

.stButton > button[data-testid="stBaseButton-primary"] {
    background: #fabd2f !important;
    border-color: #d79921 !important;
    color: #282828 !important;
}

.stButton > button[data-testid="stBaseButton-primary"] *,
.stButton > button[kind="primary"] * {
    color: #282828 !important;
}

.stButton > button[data-testid="stBaseButton-secondary"],
.stDownloadButton > button {
    background: #504945 !important;
    color: #ebdbb2 !important;
}

.stButton > button[data-testid="stBaseButton-secondary"] *,
.stDownloadButton > button * {
    color: #ebdbb2 !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    filter: brightness(1.12);
    transform: translateY(-1px) !important;
    box-shadow: none !important;
}

.stButton > button:focus-visible,
.stDownloadButton > button:focus-visible {
    outline: 2px solid #fabd2f !important;
    outline-offset: 2px !important;
}

[data-testid="stSegmentedControl"] button {
    background: #3c3836 !important;
    border-radius: 10px !important;
    color: #ebdbb2 !important;
    box-shadow: none !important;
}

[data-testid="stSegmentedControl"] button[aria-pressed="true"] {
    background: #665c54 !important;
    color: #fabd2f !important;
}

[data-testid="stDataFrame"] * {
    color: #ebdbb2 !important;
}

[data-testid="stAlert"] {
    background: #3c3836 !important;
    border: 2px solid #fb4934 !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

glyph_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="190" height="190" viewBox="0 0 190 190">
<g fill="none" stroke="{theme_palette['glyph']}" stroke-width="3" stroke-linecap="square" stroke-linejoin="miter" opacity=".06">
<path d="M18 18h42v42H18z M28 31h22 M28 40h22 M28 49h22"/>
<circle cx="34" cy="24" r="2" fill="{theme_palette['glyph']}"/><circle cx="44" cy="24" r="2" fill="{theme_palette['glyph']}"/>
<path d="M111 20h42v42h-42z M121 31h22v20h-22z M121 57h22"/>
<path d="M23 111h42v42H23z M34 132c0-11 20-11 20 0s-20 11-20 0z M42 128v8"/>
<path d="M111 111h42v42h-42z M122 123h20 M132 123v20 M122 143h20"/>
<circle cx="128" cy="132" r="2" fill="{theme_palette['glyph']}"/><circle cx="138" cy="132" r="2" fill="{theme_palette['glyph']}"/>
</g></svg>"""
glyph_pattern = quote(glyph_svg, safe="")
glass_surface = "rgba(60, 56, 54, .78)" if dark_mode else "rgba(251, 241, 199, .78)"
glass_highlight = "rgba(255, 255, 255, .14)" if dark_mode else "rgba(255, 255, 255, .55)"
glass_edge = "rgba(235, 219, 178, .44)" if dark_mode else "rgba(102, 92, 84, .34)"
glass_shadow = "rgba(0, 0, 0, .30)" if dark_mode else "rgba(102, 92, 84, .16)"
glass_glow = "rgba(250, 189, 47, .14)" if dark_mode else "rgba(215, 153, 33, .16)"
summary_colors = {
    "media": "#fabd2f" if dark_mode else "#b57614",
    "mediana": "#d3869b" if dark_mode else "#b16286",
    "desviacion": "#b16286" if dark_mode else "#8f3f71",
    "moda": "#8ec07c" if dark_mode else "#578c55",
}
st.markdown(
    f"""
<style>
:root {{ color-scheme: {"dark" if dark_mode else "light"}; }}
.main .block-container {{
    max-width: 1680px !important;
    padding: .5rem clamp(.75rem, 1.5vw, 1.25rem) .8rem !important;
}}
[data-testid="stMainBlockContainer"] {{
    padding-top: .5rem !important;
}}
.quantyx-about {{
    margin: .75rem auto .2rem;
    padding: .65rem .5rem;
    border-top: 1px solid {glass_edge};
    color: {theme_palette["muted"]};
    font-size: .85rem;
    text-align: center;
}}
html, body {{
    background-color: {theme_palette["background"]} !important;
    color: {theme_palette["text"]} !important;
}}
.stApp {{
    background-color: {theme_palette["background"]} !important;
    background-image:
        radial-gradient(ellipse at 10% 12%, rgba(251, 73, 52, .12), transparent 34%),
        radial-gradient(ellipse at 88% 18%, rgba(131, 165, 152, .14), transparent 32%),
        radial-gradient(ellipse at 76% 88%, rgba(250, 189, 47, .12), transparent 38%),
        url("data:image/svg+xml,{glyph_pattern}") !important;
    background-attachment: fixed !important;
    background-repeat: no-repeat, no-repeat, no-repeat, repeat !important;
    background-size: auto, auto, auto, 260px 260px !important;
}}
[data-testid="stAppViewContainer"] {{
    background: transparent !important;
    color: {theme_palette["text"]} !important;
}}
body, input, textarea, button, [data-testid="stDataFrame"] {{
    font-family: "Inter", "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif !important;
}}
h1, h2, h3, h4, .hero-heading {{
    font-family: "Pixelify Sans", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace !important;
}}
.stMarkdown, .stText, .stCaptionContainer, p, li, label,
[data-testid="stCaptionContainer"] {{
    color: {theme_palette["muted"]} !important;
}}
h1, h2, h3, h4, .hero-heading {{
    color: {theme_palette["text"]} !important;
}}
.hero-heading span, .section-eyebrow {{
    color: {theme_palette["accent"]} !important;
}}
.hero-copy, .glass-card, .glass-card p, .glass-card span {{
    color: {theme_palette["muted"]} !important;
}}
.hero-kicker, .badge {{
    background: {theme_palette["panel"]} !important;
    color: {theme_palette["accent"]} !important;
    border-color: {theme_palette["border"]} !important;
}}
.glass-card, [data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stMetric"], [data-testid="stDataFrame"],
.st-key-data-card, .st-key-chart-card-bars, .st-key-chart-card-proportion,
.st-key-chart-card-histogram, .st-key-table-card, .st-key-summary-card {{
    background:
        linear-gradient(135deg, {glass_highlight}, rgba(255, 255, 255, .025) 42%, {glass_glow}),
        {glass_surface} !important;
    border-color: {glass_edge} !important;
    border-width: 3px !important;
    box-shadow: 0 16px 38px {glass_shadow},
        inset 0 1px 0 {glass_highlight},
        inset 0 -1px 0 rgba(0, 0, 0, .16),
        0 0 22px {glass_glow} !important;
    backdrop-filter: blur(18px) saturate(145%) !important;
    -webkit-backdrop-filter: blur(18px) saturate(145%) !important;
}}
[data-testid="stVerticalBlockBorderWrapper"],
.st-key-data-card, .st-key-chart-card-bars, .st-key-chart-card-proportion,
.st-key-chart-card-histogram, .st-key-table-card, .st-key-summary-card {{
    padding: .7rem !important;
}}
.st-key-data-card {{
    border-color: {theme_palette["accent"]} !important;
    border-width: 3px !important;
}}
.st-key-data-card, .st-key-chart-card-bars, .st-key-chart-card-proportion,
.st-key-chart-card-histogram, .st-key-table-card, .st-key-summary-card {{
    border-radius: 20px !important;
}}
.st-key-summary-stat-media, .st-key-summary-stat-mediana,
.st-key-summary-stat-desviacion, .st-key-summary-stat-moda {{
    min-height: 92px !important;
    padding: .55rem !important;
    border: 2px solid {glass_edge} !important;
    border-radius: 18px !important;
    background:
        linear-gradient(135deg, {glass_highlight}, rgba(255, 255, 255, .025) 42%, {glass_glow}),
        {glass_surface} !important;
    box-shadow: 0 10px 24px {glass_shadow}, inset 0 1px 0 {glass_highlight} !important;
    backdrop-filter: blur(14px) saturate(140%) !important;
    -webkit-backdrop-filter: blur(14px) saturate(140%) !important;
}}
.st-key-summary-stat-media [data-testid="stMarkdownContainer"] span[role="img"] {{
    color: {summary_colors["media"]} !important;
}}
.st-key-summary-stat-mediana [data-testid="stMarkdownContainer"] span[role="img"] {{
    color: {summary_colors["mediana"]} !important;
}}
.st-key-summary-stat-desviacion [data-testid="stMarkdownContainer"] span[role="img"] {{
    color: {summary_colors["desviacion"]} !important;
}}
.st-key-summary-stat-moda [data-testid="stMarkdownContainer"] span[role="img"] {{
    color: {summary_colors["moda"]} !important;
}}
.st-key-summary-stat-media [data-testid="stMarkdownContainer"] span[role="img"],
.st-key-summary-stat-mediana [data-testid="stMarkdownContainer"] span[role="img"],
.st-key-summary-stat-desviacion [data-testid="stMarkdownContainer"] span[role="img"],
.st-key-summary-stat-moda [data-testid="stMarkdownContainer"] span[role="img"] {{
    font-size: 2rem !important;
    line-height: 1 !important;
}}
.st-key-summary-stat-media [data-testid="stMarkdownContainer"] p,
.st-key-summary-stat-mediana [data-testid="stMarkdownContainer"] p,
.st-key-summary-stat-moda [data-testid="stMarkdownContainer"] p {{
    margin: .2rem 0 !important;
}}
.st-key-summary-stat-media [data-testid="stCaptionContainer"],
.st-key-summary-stat-mediana [data-testid="stCaptionContainer"],
.st-key-summary-stat-desviacion [data-testid="stCaptionContainer"],
.st-key-summary-stat-moda [data-testid="stCaptionContainer"],
.st-key-summary-stat-media .summary-value,
.st-key-summary-stat-mediana .summary-value,
.st-key-summary-stat-desviacion .summary-value,
.st-key-summary-stat-moda .summary-value {{
    text-align: left !important;
}}
.summary-value {{
    font-family: "Inter", "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 1.45rem;
    font-variant-numeric: tabular-nums lining-nums;
    font-weight: 800;
    line-height: 1.15;
}}
.summary-value-media {{ color: {summary_colors["media"]}; }}
.summary-value-mediana {{ color: {summary_colors["mediana"]}; }}
.summary-value-desviacion {{ color: {summary_colors["desviacion"]}; }}
.summary-value-moda {{ color: {summary_colors["moda"]}; }}
.st-key-chart-card-bars {{
    border-color: rgba(184, 187, 38, .68) !important;
    box-shadow: 0 16px 38px {glass_shadow}, inset 0 1px 0 {glass_highlight},
        0 0 22px rgba(184, 187, 38, .14) !important;
}}
.st-key-chart-card-proportion {{
    border-color: rgba(211, 134, 155, .72) !important;
    box-shadow: 0 16px 38px {glass_shadow}, inset 0 1px 0 {glass_highlight},
        0 0 22px rgba(211, 134, 155, .16) !important;
}}
.st-key-chart-card-histogram {{
    border-color: rgba(131, 165, 152, .72) !important;
    box-shadow: 0 16px 38px {glass_shadow}, inset 0 1px 0 {glass_highlight},
        0 0 22px rgba(131, 165, 152, .16) !important;
}}
.st-key-chart-card-bars, .st-key-chart-card-proportion,
.st-key-chart-card-histogram {{
    transition: border-color 180ms ease, transform 180ms ease, box-shadow 180ms ease !important;
}}
.st-key-chart-card-bars:hover, .st-key-chart-card-proportion:hover,
.st-key-chart-card-histogram:hover {{
    border-color: {theme_palette["accent"]} !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 20px 44px {glass_shadow}, inset 0 1px 0 {glass_highlight},
        0 0 28px {glass_glow} !important;
}}
.st-key-table-card [data-testid="stDataFrame"] {{
    max-height: none !important;
    max-width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
    border-width: 3px !important;
}}
.st-key-table-card [data-testid="stDataFrameResizable"] {{
    max-width: 100% !important;
    min-width: 0 !important;
}}
div[data-testid="stMetric"] {{
    padding: .5rem .65rem !important;
}}
div[data-testid="stMetricLabel"] {{
    color: {theme_palette["muted"]} !important;
}}
div[data-testid="stMetricValue"] {{
    color: {theme_palette["accent"]} !important;
    font-size: 1.7rem !important;
    font-family: "Inter", "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-variant-numeric: tabular-nums lining-nums;
    font-weight: 700 !important;
}}
div[data-testid="stMetricValue"] * {{
    font-family: "Inter", "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-variant-numeric: tabular-nums lining-nums;
}}
.numeric-value {{
    font-family: "Inter", "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-variant-numeric: tabular-nums lining-nums;
    font-weight: 700;
}}
.hero-kicker {{
    padding: .3rem .6rem !important;
}}
.hero-heading {{
    margin: .35rem 0 !important;
    font-size: clamp(1.8rem, 2.8vw, 2.5rem) !important;
}}
.hero-copy {{
    margin: .25rem 0 .5rem !important;
}}
.insight-strip {{
    background: {theme_palette["secondary"]} !important;
    color: {theme_palette["text"]} !important;
    border-color: {theme_palette["accent"]} !important;
    margin: .3rem 0 .65rem !important;
    padding: .5rem .75rem !important;
}}
.insight-icon {{
    background: {theme_palette["panel"]} !important;
    border-color: {theme_palette["border"]} !important;
}}
div[data-baseweb="textarea"] {{
    background: {glass_surface} !important;
    border-color: {glass_edge} !important;
    box-shadow: inset 0 1px 0 {glass_highlight}, 0 8px 20px {glass_shadow} !important;
    backdrop-filter: blur(14px) saturate(140%) !important;
    -webkit-backdrop-filter: blur(14px) saturate(140%) !important;
}}
div[data-baseweb="textarea"]:focus-within {{
    border-color: {theme_palette["accent"]} !important;
    outline-color: {theme_palette["accent"]} !important;
}}
div[data-baseweb="textarea"] textarea,
[data-testid="stSidebar"] .stTextArea textarea {{
    color: {theme_palette["text"]} !important;
    -webkit-text-fill-color: {theme_palette["text"]} !important;
}}
div[data-baseweb="textarea"] textarea::placeholder {{
    color: {theme_palette["muted"]} !important;
    -webkit-text-fill-color: {theme_palette["muted"]} !important;
}}
.st-key-raw_values [data-testid="stTextAreaRootElement"] {{
    background: {glass_surface} !important;
    border: 2px solid {glass_edge} !important;
    border-radius: 16px !important;
    box-shadow: inset 0 1px 0 {glass_highlight}, 0 8px 20px {glass_shadow} !important;
    backdrop-filter: blur(14px) saturate(140%) !important;
    -webkit-backdrop-filter: blur(14px) saturate(140%) !important;
    transition: border-color 180ms ease, box-shadow 180ms ease !important;
}}
.st-key-raw_values:focus-within [data-testid="stTextAreaRootElement"] {{
    border-color: {theme_palette["accent"]} !important;
    box-shadow: inset 0 1px 0 {glass_highlight}, 0 0 22px {glass_glow} !important;
}}
.st-key-raw_values textarea {{
    background: transparent !important;
    color: {theme_palette["text"]} !important;
    -webkit-text-fill-color: {theme_palette["text"]} !important;
    font-family: "Inter", "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-variant-numeric: tabular-nums lining-nums;
    font-size: 1.05rem !important;
    line-height: 1.55 !important;
}}
.st-key-raw_values textarea::placeholder {{
    color: {theme_palette["muted"]} !important;
    -webkit-text-fill-color: {theme_palette["muted"]} !important;
}}
.stButton button[data-testid="stBaseButton-primary"] {{
    background: linear-gradient(115deg, #fabd2f, #fe8019) !important;
    border-color: rgba(250, 189, 47, .9) !important;
    color: {theme_palette["button_text"]} !important;
    box-shadow: 0 8px 24px rgba(250, 189, 47, .24),
        inset 0 1px 0 rgba(255, 255, 255, .35) !important;
}}
.stButton button[data-testid="stBaseButton-primary"] *,
.stButton button[kind="primary"] * {{
    color: {theme_palette["button_text"]} !important;
}}
.stButton button[data-testid="stBaseButton-secondary"],
.stDownloadButton button {{
    background: linear-gradient(135deg, {glass_highlight}, {glass_surface}) !important;
    border-color: {glass_edge} !important;
    color: {theme_palette["text"]} !important;
    box-shadow: 0 8px 20px {glass_shadow}, inset 0 1px 0 {glass_highlight} !important;
    backdrop-filter: blur(12px) saturate(135%) !important;
    -webkit-backdrop-filter: blur(12px) saturate(135%) !important;
}}
.stButton button[data-testid="stBaseButton-secondary"] *,
.stDownloadButton button * {{
    color: {theme_palette["text"]} !important;
}}
.stButton button[data-testid="stBaseButton-tertiary"],
.stButton button[data-testid="stBaseButton-tertiary"] * {{
    color: {theme_palette["text"]} !important;
}}
.stButton button:focus-visible, .stDownloadButton button:focus-visible {{
    outline-color: {theme_palette["accent"]} !important;
}}
[data-testid="stSegmentedControl"] button {{
    background: {theme_palette["panel"]} !important;
    color: {theme_palette["text"]} !important;
}}
[data-testid="stSegmentedControl"] button[aria-pressed="true"] {{
    background: {theme_palette["accent"]} !important;
    color: {theme_palette["button_text"]} !important;
}}
[data-testid="stDataFrame"] * {{
    color: {theme_palette["text"]} !important;
}}
[data-testid="stAlert"] {{
    background: {theme_palette["panel"]} !important;
    color: {theme_palette["text"]} !important;
}}
.st-key-theme-dark-mode label {{
    color: {theme_palette["text"]} !important;
}}
.stButton button, .stDownloadButton button,
div[data-baseweb="textarea"], [data-testid="stSegmentedControl"] button {{
    transition: background-color 180ms ease, color 180ms ease,
        border-color 180ms ease, filter 180ms ease, transform 180ms ease,
        box-shadow 180ms ease !important;
}}
.stButton button:hover, .stDownloadButton button:hover {{
    filter: brightness(1.06) !important;
    transform: translateY(-2px) !important;
}}
img[alt*="Quantyx 86"] {{
    filter: drop-shadow(0 8px 18px rgba(250, 189, 47, .20))
        drop-shadow(0 0 14px rgba(131, 165, 152, .12));
}}
@media (prefers-reduced-motion: reduce) {{
    .stButton button, .stDownloadButton button,
    div[data-baseweb="textarea"], [data-testid="stSegmentedControl"] button {{
        transition-duration: .01ms !important;
    }}
}}
@media (max-width: 760px) {{
    .st-key-summary-stat-media [data-testid="stHorizontalBlock"],
    .st-key-summary-stat-mediana [data-testid="stHorizontalBlock"],
    .st-key-summary-stat-desviacion [data-testid="stHorizontalBlock"],
    .st-key-summary-stat-moda [data-testid="stHorizontalBlock"] {{
        flex-wrap: nowrap !important;
        column-gap: .5rem !important;
    }}
    .st-key-summary-stat-media [data-testid="stHorizontalBlock"] > div:first-child,
    .st-key-summary-stat-mediana [data-testid="stHorizontalBlock"] > div:first-child,
    .st-key-summary-stat-desviacion [data-testid="stHorizontalBlock"] > div:first-child,
    .st-key-summary-stat-moda [data-testid="stHorizontalBlock"] > div:first-child {{
        flex: 0 0 2.25rem !important;
        min-width: 2.25rem !important;
    }}
    .st-key-summary-stat-media [data-testid="stHorizontalBlock"] > div:nth-child(2),
    .st-key-summary-stat-mediana [data-testid="stHorizontalBlock"] > div:nth-child(2),
    .st-key-summary-stat-desviacion [data-testid="stHorizontalBlock"] > div:nth-child(2),
    .st-key-summary-stat-moda [data-testid="stHorizontalBlock"] > div:nth-child(2) {{
        flex: 1 1 0% !important;
        min-width: 0 !important;
    }}
}}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------ FUNCIONES ---------------------------
def parse_numbers(raw: str) -> list[float]:
    parts = [p for p in re.split(r"[,;\s]+", raw.strip()) if p]
    if not parts:
        raise ValueError("Escribe al menos un valor numérico.")
    values = []
    for part in parts:
        try:
            value = float(part)
        except ValueError:
            raise ValueError(f"«{part}» no es un número válido. Usa solo valores numéricos.")
        if not math.isfinite(value):
            raise ValueError(f"«{part}» no es un número válido. Usa solo valores numéricos.")
        values.append(value)
    return values

def frequency_distribution(values: list[float]):
    data = np.asarray(values, dtype=float)
    n = len(data)
    xmin, xmax = float(np.min(data)), float(np.max(data))
    data_range = xmax - xmin
    integer_data = bool(np.all(data == np.trunc(data)))

    if data_range == 0:
        k = 1
        width = 1.0
        edges = np.array([xmin, xmin + width], dtype=float)
    else:
        k = max(1, int(round(1 + 3.322 * math.log10(n))))
        if integer_data:
            integer_span = int(round(data_range)) + 1
            k = min(k, integer_span)
            width = math.ceil(integer_span / k)
            k = math.ceil(integer_span / width)
            edges = xmin + np.arange(k + 1, dtype=float) * width
        else:
            raw_width = data_range / k
            width = math.ceil(raw_width * 100 - 1e-10) / 100
            width = max(width, 0.01)
            edges = xmin + np.arange(k + 1, dtype=float) * width
            if edges[-1] < xmax:
                k += 1
                edges = xmin + np.arange(k + 1, dtype=float) * width

    fi, edges = np.histogram(data, bins=edges)
    xi = (edges[:-1] + edges[1:]) / 2
    Fi = np.cumsum(fi)
    hi = fi / n
    pct = hi * 100
    unique_values, value_counts = np.unique(data, return_counts=True)
    mode_index = int(np.argmax(value_counts))

    labels = []
    for i in range(len(fi)):
        if integer_data:
            lower = int(round(float(edges[i])))
            upper = int(round(float(edges[i + 1]))) - 1
            if i == len(fi) - 1 and math.isclose(
                float(edges[i + 1]), xmax, rel_tol=0, abs_tol=1e-9
            ):
                upper = int(round(xmax))
            labels.append(f"{lower}–{upper}")
        else:
            is_closed_final_edge = (
                i == len(fi) - 1
                and math.isclose(float(edges[i + 1]), xmax, rel_tol=0, abs_tol=1e-9)
            )
            right = "]" if is_closed_final_edge else ")"
            labels.append(f"[{edges[i]:g}, {edges[i+1]:g}{right}")

    table = pd.DataFrame({
        "Intervalo": labels,
        "Marca de clase (Xi)": xi,
        "Frecuencia absoluta (fi)": fi,
        "Frecuencia acumulada (Fi)": Fi,
        "Frecuencia relativa (hi)": hi,
        "Porcentaje (%)": pct,
    })
    return {
        "data": data, "n": n, "min": xmin, "max": xmax, "range": data_range,
        "k": len(fi), "width": float(edges[1] - edges[0]), "edges": edges,
        "fi": fi, "xi": xi, "table": table, "integer_data": integer_data,
        "mean": float(np.mean(data)), "median": float(np.median(data)),
        "std_dev": float(np.std(data)),
        "mode": float(unique_values[mode_index]), "mode_count": int(value_counts[mode_index]),
    }

# -------------------- GRÁFICOS --------------------
CHART_COLORS = ["#b8bb26", "#83a598", "#fb4934", "#fabd2f", "#d3869b", "#8ec07c", "#fe8019", "#a89984"]
TABLE_GRADIENTS = {
    "absolute_frequency": LinearSegmentedColormap.from_list("gruvbox_green", ["#3c3836", "#625c24", "#98971a"]),
    "class_mark": LinearSegmentedColormap.from_list("gruvbox_blue", ["#3c3836", "#3c5555", "#458588"]),
    "cumulative_frequency": LinearSegmentedColormap.from_list("gruvbox_yellow", ["#3c3836", "#66542a", "#d79921"]),
    "relative_frequency": LinearSegmentedColormap.from_list("gruvbox_aqua", ["#3c3836", "#455b3d", "#689d6a"]),
    "percentage": LinearSegmentedColormap.from_list("gruvbox_orange", ["#3c3836", "#704623", "#d65d0e"]),
}
TABLE_GRADIENTS_LIGHT = {
    "absolute_frequency": LinearSegmentedColormap.from_list("gruvbox_light_green", ["#fbf1c7", "#e7d895", "#c5c761"]),
    "class_mark": LinearSegmentedColormap.from_list("gruvbox_light_blue", ["#fbf1c7", "#c8d8c8", "#a9c5b7"]),
    "cumulative_frequency": LinearSegmentedColormap.from_list("gruvbox_light_yellow", ["#fbf1c7", "#f0d48b", "#e3b75b"]),
    "relative_frequency": LinearSegmentedColormap.from_list("gruvbox_light_aqua", ["#fbf1c7", "#c8d7a8", "#a9c486"]),
    "percentage": LinearSegmentedColormap.from_list("gruvbox_light_orange", ["#fbf1c7", "#f3c08b", "#e6a16c"]),
}

def chart_option(result: dict, chart_kind: str, palette: dict[str, str]) -> dict:
    table = result["table"]
    intervals = table["Intervalo"].tolist()
    frequencies = [int(value) for value in table["Frecuencia absoluta (fi)"]]
    colors = [CHART_COLORS[index % len(CHART_COLORS)] for index in range(len(intervals))]

    base = {
        "animation": True,
        "animationDuration": 650,
        "animationDurationUpdate": 400,
        "animationEasing": "cubicOut",
        "animationEasingUpdate": "cubicOut",
        "color": colors,
        "backgroundColor": "transparent",
        "textStyle": {
            "fontFamily": 'Inter, "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif',
            "fontSize": 14,
        },
        "tooltip": {
            "trigger": "axis",
            "backgroundColor": palette["panel"],
            "borderColor": palette["border"],
            "textStyle": {"color": palette["text"]},
        },
        "grid": {"left": 38, "right": 22, "top": 30, "bottom": 62, "containLabel": True},
    }

    if chart_kind == "Barras":
        base.update({
            "xAxis": {
                "type": "category",
                "data": intervals,
                "axisLabel": {"color": palette["muted"], "rotate": 18, "fontSize": 13},
                "axisLine": {"lineStyle": {"color": palette["border"]}},
                "axisTick": {"show": False},
            },
            "yAxis": {
                "type": "value",
                "minInterval": 1,
                "axisLabel": {"color": palette["muted"]},
                "splitLine": {"lineStyle": {"color": palette["grid"], "type": "dashed"}},
            },
            "series": [{
                "name": "Frecuencia",
                "type": "bar",
                "data": [
                    {"value": value, "itemStyle": {"color": colors[index]}}
                    for index, value in enumerate(frequencies)
                ],
                "barMaxWidth": 48,
                "label": {"show": True, "position": "top", "color": palette["text"], "fontWeight": 700},
                "emphasis": {"focus": "self"},
            }],
        })
    elif chart_kind == "Circular":
        base.update({
            "tooltip": {
                "trigger": "item",
                "backgroundColor": palette["panel"],
                "borderColor": palette["border"],
                "textStyle": {"color": palette["text"]},
                "valueFormatter": "localized",
            },
            "legend": {
                "type": "scroll",
                "orient": "vertical",
                "right": 0,
                "top": "middle",
                "itemWidth": 10,
                "itemHeight": 10,
                "textStyle": {"color": palette["muted"], "fontSize": 14},
            },
            "graphic": [
                {
                    "type": "group",
                    "left": "35%",
                    "top": "50%",
                    "width": 0,
                    "height": 0,
                    "bounding": "raw",
                    "z": 100,
                    "silent": True,
                    "children": [{
                        "type": "text",
                        "position": [0, 0],
                        "style": {
                            "text": str(result["n"]),
                            "fontFamily": base["textStyle"]["fontFamily"],
                            "fontSize": 36,
                            "fontWeight": 800,
                            "fill": palette["accent"],
                            "align": "center",
                            "verticalAlign": "middle",
                        },
                    }],
                },
                {
                    "type": "group",
                    "left": "35%",
                    "top": "58%",
                    "width": 0,
                    "height": 0,
                    "bounding": "raw",
                    "z": 100,
                    "silent": True,
                    "children": [{
                        "type": "text",
                        "position": [0, 0],
                        "style": {
                            "text": "datos",
                            "fontFamily": base["textStyle"]["fontFamily"],
                            "fontSize": 14,
                            "fill": palette["muted"],
                            "align": "center",
                            "verticalAlign": "middle",
                        },
                    }],
                },
            ],
            "series": [{
                "name": "Frecuencia",
                "type": "pie",
                "radius": ["48%", "68%"],
                "center": ["35%", "50%"],
                "startAngle": 90,
                "avoidLabelOverlap": True,
                "itemStyle": {"borderColor": palette["panel"], "borderWidth": 2},
                "label": {"show": False},
                "labelLine": {"show": False},
                "emphasis": {"scale": True, "scaleSize": 5},
                "data": [
                    {"name": label, "value": value, "itemStyle": {"color": colors[index]}}
                    for index, (label, value) in enumerate(zip(intervals, frequencies))
                ],
            }],
        })
    else:
        base.update({
            "xAxis": {
                "type": "category",
                "data": intervals,
                "axisLabel": {"color": palette["muted"], "rotate": 18, "fontSize": 13, "interval": 0},
                "axisLine": {"lineStyle": {"color": palette["border"]}},
                "axisTick": {"show": False},
            },
            "yAxis": {
                "type": "value",
                "min": 0,
                "minInterval": 1,
                "axisLabel": {"color": palette["muted"]},
                "splitLine": {"lineStyle": {"color": palette["grid"], "type": "dashed"}},
            },
            "series": [
                {
                    "name": "Frecuencia",
                    "type": "bar",
                    "data": [
                        {"value": value, "itemStyle": {"color": colors[index]}}
                        for index, value in enumerate(frequencies)
                    ],
                    "barWidth": "100%",
                    "barCategoryGap": "0%",
                    "barGap": "0%",
                    "itemStyle": {"borderColor": palette["panel"], "borderWidth": 1},
                    "label": {"show": True, "position": "top", "color": palette["text"], "fontWeight": 700},
                    "emphasis": {"focus": "self"},
                },
                {
                    "name": "Polígono de frecuencias",
                    "type": "line",
                    "data": frequencies,
                    "symbol": "circle",
                    "symbolSize": 8,
                    "lineStyle": {"color": palette["text"], "width": 3},
                    "itemStyle": {
                        "color": palette["text"],
                        "borderColor": palette["panel"],
                        "borderWidth": 2,
                    },
                    "z": 10,
                    "markPoint": {
                        "symbol": "circle",
                        "symbolSize": 16,
                        "itemStyle": {
                            "color": palette["accent"],
                            "borderColor": palette["panel"],
                            "borderWidth": 3,
                        },
                        "label": {"show": False},
                        "data": [{"type": "max", "name": "Frecuencia máxima"}],
                    },
                },
            ],
        })

    return base

EXAMPLE_DATA = "12, 15, 18, 22, 25, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 55, 60, 65, 70"

def restore_example():
    st.session_state.raw_values = EXAMPLE_DATA
    st.session_state.analysis_result = frequency_distribution(parse_numbers(EXAMPLE_DATA))
    st.session_state.pop("analysis_error", None)

def clear_data():
    st.session_state.raw_values = ""
    st.session_state.pop("analysis_result", None)
    st.session_state.pop("analysis_error", None)

if "raw_values" not in st.session_state:
    st.session_state.raw_values = ""

result = st.session_state.get("analysis_result")
brand_column, theme_column = st.columns(
    [1, 0.45],
    gap="small",
    vertical_alignment="center",
)
with brand_column:
    st.image(
        DARK_LOGO_PATH if dark_mode else LIGHT_LOGO_PATH,
        width=240,
        alt="Quantyx 86: El lenguaje de los datos",
    )
with theme_column:
    dark_mode = st.toggle(
        "Modo oscuro",
        value=dark_mode,
        key="theme-dark-mode",
        help="Cambia entre las paletas Gruvbox clara y oscura.",
    )

with st.container(border=True, key="data-card"):
    prompt_column, input_column = st.columns([1.08, 1.92], gap="small", vertical_alignment="center")
    with prompt_column:
        st.subheader("Tus datos, en claro")
        st.caption("Pégalos separados por comas, espacios o saltos de línea.")
    with input_column:
        values_column, action_column, example_column = st.columns(
            [3.8, 1.7, 1.3],
            gap="small",
            vertical_alignment="center",
        )
        with values_column:
            raw = st.text_area(
                "Conjunto de datos",
                key="raw_values",
                height=68,
                help="Separa los valores con comas, espacios, punto y coma o saltos de línea.",
                placeholder="Por ejemplo: 12, 15, 18, 22, 25",
                label_visibility="collapsed",
            )
        with action_column:
            run = st.button(
                "Calcular",
                type="primary",
                width="stretch",
                icon=":material/calculate:",
            )
        with example_column:
            st.button(
                "Ejemplo",
                type="secondary",
                width="stretch",
                help="Cargar un conjunto de datos de ejemplo.",
                icon=":material/auto_awesome:",
                on_click=restore_example,
            )

if run:
    try:
        st.session_state.analysis_result = frequency_distribution(parse_numbers(raw))
        st.session_state.analysis_error = None
    except ValueError as exc:
        st.session_state.analysis_result = None
        st.session_state.analysis_error = str(exc)

result = st.session_state.get("analysis_result")
error = st.session_state.get("analysis_error")

if error:
    st.error(f"Revisa tus datos: {error}")

if result is not None:
    title_column, clear_column = st.columns([1, 0.22], gap="medium", vertical_alignment="center")
    width_label = f"{result['width']:g}" if result["integer_data"] else f"{result['width']:.2f}"
    with title_column:
        st.subheader("Resultados", icon=":material/analytics:")
        st.caption(
            f"{result['n']} datos · {result['k']} intervalos · amplitud {width_label}"
        )
    with clear_column:
        st.button("Limpiar", type="tertiary", width="stretch", on_click=clear_data)

    chart_cards = (
        ("bars", ":material/bar_chart:", "Barras", "Barras", "Frecuencia absoluta de cada intervalo."),
        ("proportion", ":material/pie_chart:", "Circular", "Circular", "Proporción de los datos por intervalo."),
        (
            "histogram",
            ":material/analytics:",
            "Histograma",
            "Histograma",
            "La línea une las frecuencias por intervalo y señala el máximo.",
        ),
    )
    chart_grid = st.grid(3, min_column_width=320, gap="small")
    for chart_id, icon, title, chart_kind, description in chart_cards:
        with chart_grid.cell():
            with st.container(border=True, key=f"chart-card-{chart_id}"):
                st.markdown(f"#### {icon} {title}")
                st.echarts_chart(
                    chart_option(result, chart_kind, theme_palette),
                    height=260,
                    key=f"frequency-chart-{chart_id}",
                    alt=description,
                )

    if result["mode_count"] > 1:
        insight = (
            f"El valor <strong class=\"numeric-value\">{result['mode']:g}</strong> es el más repetido "
            f"(<span class=\"numeric-value\">{result['mode_count']}</span> veces). "
            f"La mediana es <strong class=\"numeric-value\">{result['median']:,.2f}</strong>."
        )
    else:
        insight = (
            f"No hay valores repetidos: cada dato es único. "
            f"El promedio es <strong class=\"numeric-value\">{result['mean']:,.2f}</strong>."
        )
    bottom_grid = st.grid("auto", min_column_width=500, gap="small")
    with bottom_grid.cell():
        with st.container(border=True, key="table-card"):
            st.subheader("Tabla de frecuencias", icon=":material/table_chart:")
            st.caption("Xi: marca · fi: absoluta · Fi: acumulada · hi: relativa")
            display_df = result["table"].copy()
            xi_format = "%.2f"
            if result["integer_data"]:
                xi_format = "%.0f" if np.all(result["xi"] == np.rint(result["xi"])) else "%.1f"
            table_gradients = TABLE_GRADIENTS if dark_mode else TABLE_GRADIENTS_LIGHT
            styled_df = (
                display_df.style
                .background_gradient(cmap=table_gradients["absolute_frequency"], subset=["Frecuencia absoluta (fi)"])
                .background_gradient(cmap=table_gradients["class_mark"], subset=["Marca de clase (Xi)"])
                .background_gradient(cmap=table_gradients["cumulative_frequency"], subset=["Frecuencia acumulada (Fi)"])
                .background_gradient(cmap=table_gradients["relative_frequency"], subset=["Frecuencia relativa (hi)"])
                .background_gradient(cmap=table_gradients["percentage"], subset=["Porcentaje (%)"])
                .set_table_styles([
                    {
                        "selector": "th",
                        "props": [
                            ("background-color", theme_palette["secondary"]),
                            ("color", theme_palette["accent"]),
                            ("font-weight", "700"),
                            ("border-bottom", f"2px solid {theme_palette['border']}"),
                        ],
                    },
                    {
                        "selector": "tbody tr:nth-child(even) td",
                        "props": [("background-color", theme_palette["table_alt"])],
                    },
                    {
                        "selector": "tbody tr:hover td",
                        "props": [("filter", "brightness(1.16)")],
                    },
                ])
                .set_properties(**{"color": theme_palette["text"], "border-color": theme_palette["border"]})
                .set_properties(
                    subset=["Intervalo"],
                    **{"background-color": theme_palette["panel"]},
                )
            )
            st.dataframe(
                styled_df,
                width="stretch",
                hide_index=True,
                height="content",
                row_height=32,
                column_config={
                    "Intervalo": st.column_config.TextColumn(
                        "Intervalo",
                        width=110,
                        help="Rango de valores que define el grupo.",
                    ),
                    "Marca de clase (Xi)": st.column_config.NumberColumn(
                        "Xi",
                        width=70,
                        format=xi_format,
                        help="Punto medio del intervalo.",
                    ),
                    "Frecuencia absoluta (fi)": st.column_config.NumberColumn(
                        "fi",
                        width=60,
                        format="%d",
                        help="Cantidad de datos en el intervalo.",
                    ),
                    "Frecuencia acumulada (Fi)": st.column_config.NumberColumn(
                        "Fi",
                        width=60,
                        format="%d",
                        help="Suma acumulada de las frecuencias.",
                    ),
                    "Frecuencia relativa (hi)": st.column_config.NumberColumn(
                        "hi",
                        width=70,
                        format="%.4f",
                        help="Proporción de datos en el intervalo.",
                    ),
                    "Porcentaje (%)": st.column_config.NumberColumn(
                        "%",
                        width=65,
                        format="%.2f%%",
                        help="Frecuencia relativa expresada como porcentaje.",
                    ),
                },
                alt="Tabla colorida con intervalos y frecuencias estadísticas",
            )
            csv = display_df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "Descargar CSV",
                data=csv,
                file_name="quantyx_86_datos.csv",
                mime="text/csv",
                width="stretch",
            )

    with bottom_grid.cell():
        with st.container(border=True, key="summary-card"):
            st.subheader("Resumen estadístico", icon=":material/star:")
            summary_stats = (
                ("media", "Media", f"{result['mean']:,.2f}", ":material/calculate:"),
                ("mediana", "Mediana", f"{result['median']:,.2f}", ":material/bar_chart:"),
                (
                    "desviacion",
                    "Desviación estándar",
                    f"{result['std_dev']:,.2f}",
                    ":material/functions:",
                ),
                (
                    "moda",
                    "Moda",
                    f"{result['mode']:g}" if result["mode_count"] > 1 else "Sin moda",
                    ":material/trending_up:",
                ),
            )
            summary_grid = st.grid(2, min_column_width=160, gap="small")
            for key, label, value, icon in summary_stats:
                with summary_grid.cell():
                    with st.container(border=True, key=f"summary-stat-{key}"):
                        icon_column, value_column = st.columns(
                            [0.3, 0.7],
                            gap="small",
                            vertical_alignment="center",
                        )
                        with icon_column:
                            st.markdown(icon)
                        with value_column:
                            st.caption(label)
                            st.markdown(
                                f'<div class="summary-value summary-value-{key}">{value}</div>',
                                unsafe_allow_html=True,
                            )
            st.markdown(
                f'<div class="insight-strip"><span class="insight-icon">💡</span>'
                f'<span><strong>Un dato curioso:</strong> {insight}</span></div>',
                unsafe_allow_html=True,
            )

st.markdown(
    '<div class="quantyx-about">Quantyx 86 · El lenguaje de los datos.</div>',
    unsafe_allow_html=True,
)