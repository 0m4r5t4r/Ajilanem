import base64
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

# ============================================================
# AJILANEM — Estadística fácil
# ============================================================

LOGO_PATH = Path(__file__).with_name("ajilanem_logo.svg")
LOGO_DATA_URI = f"data:image/svg+xml;base64,{base64.b64encode(LOGO_PATH.read_bytes()).decode('ascii')}"

st.set_page_config(
    page_title="Ajilanem | Estadística fácil",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state="collapsed",
)

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
    text-transform: uppercase;
}

.brand-mark {
    display: block;
    width: 1.65rem;
    height: 1.65rem;
    margin-right: .35rem;
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
    min-height: 82px !important;
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
</style>
""", unsafe_allow_html=True)

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

    if data_range == 0:
        k = 1
        width = 1.0
        edges = np.array([xmin, xmin + width], dtype=float)
    else:
        k = max(1, int(round(1 + 3.322 * math.log10(n))))
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
        left = "[" if i == 0 else "["
        right = "]" if i == len(fi) - 1 else ")"
        labels.append(f"{left}{edges[i]:g}, {edges[i+1]:g}{right}")

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
        "fi": fi, "xi": xi, "table": table,
        "mean": float(np.mean(data)), "median": float(np.median(data)),
        "mode": float(unique_values[mode_index]), "mode_count": int(value_counts[mode_index]),
    }

# -------------------- GRÁFICOS --------------------
CHART_COLORS = ["#A982E8", "#57BFAF", "#F28FB3", "#F1B84B", "#729BE8", "#79C98A", "#EB8D70", "#62BFD0"]

def chart_option(result: dict, chart_kind: str) -> dict:
    table = result["table"]
    intervals = table["Intervalo"].tolist()
    frequencies = [int(value) for value in table["Frecuencia absoluta (fi)"]]
    colors = [CHART_COLORS[index % len(CHART_COLORS)] for index in range(len(intervals))]

    base = {
        "animation": True,
        "animationDuration": 950,
        "animationDurationUpdate": 700,
        "animationEasing": "elasticOut",
        "animationEasingUpdate": "cubicOut",
        "color": colors,
        "backgroundColor": "transparent",
        "tooltip": {"trigger": "axis", "backgroundColor": "#fffaff", "borderColor": "#e6d9f3", "textStyle": {"color": "#3e3550"}},
        "grid": {"left": 38, "right": 22, "top": 30, "bottom": 62, "containLabel": True},
    }

    if chart_kind == "Barras":
        base.update({
            "xAxis": {
                "type": "category",
                "data": intervals,
                "axisLabel": {"color": "#645773", "rotate": 18, "fontSize": 11},
                "axisLine": {"lineStyle": {"color": "#d9cfe5"}},
                "axisTick": {"show": False},
            },
            "yAxis": {
                "type": "value",
                "minInterval": 1,
                "axisLabel": {"color": "#776b86"},
                "splitLine": {"lineStyle": {"color": "rgba(151, 129, 178, .16)", "type": "dashed"}},
            },
            "series": [{
                "name": "Frecuencia",
                "type": "bar",
                "data": [
                    {"value": value, "itemStyle": {"color": colors[index], "borderRadius": [10, 10, 3, 3]}}
                    for index, value in enumerate(frequencies)
                ],
                "barMaxWidth": 48,
                "showBackground": True,
                "backgroundStyle": {"color": "rgba(177, 158, 200, .08)", "borderRadius": [10, 10, 3, 3]},
                "label": {"show": True, "position": "top", "color": "#59496b", "fontWeight": 700},
                "emphasis": {"focus": "self", "itemStyle": {"shadowBlur": 16, "shadowColor": "rgba(88, 63, 128, .22)"}},
                "universalTransition": True,
            }],
        })
    elif chart_kind == "Proporción":
        base.update({
            "tooltip": {"trigger": "item", "backgroundColor": "#fffaff", "borderColor": "#e6d9f3", "textStyle": {"color": "#3e3550"}, "valueFormatter": "localized"},
            "legend": {"type": "scroll", "bottom": 2, "textStyle": {"color": "#645773"}},
            "title": {
                "text": str(result["n"]),
                "subtext": "datos",
                "left": "center",
                "top": "middle",
                "textStyle": {"fontSize": 28, "fontWeight": 800, "color": "#433553"},
                "subtextStyle": {"fontSize": 12, "color": "#857895"},
            },
            "series": [{
                "name": "Frecuencia",
                "type": "pie",
                "radius": ["48%", "72%"],
                "center": ["50%", "46%"],
                "startAngle": 90,
                "avoidLabelOverlap": True,
                "itemStyle": {"borderColor": "#fffaff", "borderWidth": 4, "borderRadius": 8},
                "label": {"color": "#544564", "formatter": "{b}\\n{d}%", "fontWeight": 600},
                "labelLine": {"lineStyle": {"color": "#b6a4c9"}},
                "emphasis": {"scale": True, "scaleSize": 10, "itemStyle": {"shadowBlur": 18, "shadowColor": "rgba(88, 63, 128, .24)"}},
                "data": [
                    {"name": label, "value": value, "itemStyle": {"color": colors[index]}}
                    for index, (label, value) in enumerate(zip(intervals, frequencies))
                ],
                "universalTransition": True,
            }],
        })
    else:
        base.update({
            "xAxis": {
                "type": "category",
                "data": intervals,
                "axisLabel": {"color": "#645773", "rotate": 18, "fontSize": 11, "interval": 0},
                "axisLine": {"lineStyle": {"color": "#d9cfe5"}},
                "axisTick": {"show": False},
            },
            "yAxis": {
                "type": "value",
                "min": 0,
                "minInterval": 1,
                "axisLabel": {"color": "#776b86"},
                "splitLine": {"lineStyle": {"color": "rgba(151, 129, 178, .16)", "type": "dashed"}},
            },
            "series": [{
                "name": "Frecuencia",
                "type": "bar",
                "data": [
                    {"value": value, "itemStyle": {"color": colors[index]}}
                    for index, value in enumerate(frequencies)
                ],
                "barWidth": "100%",
                "barCategoryGap": "0%",
                "barGap": "0%",
                "itemStyle": {"borderColor": "#fffaff", "borderWidth": 1},
                "label": {"show": True, "position": "top", "color": "#59496b", "fontWeight": 700},
                "emphasis": {"focus": "self", "itemStyle": {"shadowBlur": 16, "shadowColor": "rgba(88, 63, 128, .22)"}},
                "universalTransition": True,
            }],
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
intro, entry = st.columns([0.9, 1.1], gap="large", vertical_alignment="center")

with intro:
    heading_class = "hero-compact" if result is not None else ""
    heading = "Ajilanem"
    copy = (
        "Pega una lista de números y descubre su distribución en una tabla y gráficos fáciles de leer."
        if result is None
        else f"Resumen de {result['n']} datos. Edita la lista cuando quieras actualizar el análisis."
    )
    st.markdown(
        f"""
        <div class="{heading_class}">
            <div class="hero-kicker"><img class="brand-mark" src="{LOGO_DATA_URI}" alt="Símbolo inspirado en el cero maya">ESTADÍSTICA, SIN COMPLICACIONES</div>
            <h1 class="hero-heading">{heading}</h1>
            <p class="hero-copy">{copy}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with entry:
    with st.container(border=True, key="data-card"):
        st.markdown('<div class="section-eyebrow">Conjunto de datos</div>', unsafe_allow_html=True)
        st.caption("Escribe o pega tantos valores numéricos como necesites; se rechaza cualquier dato no numérico.")
        raw = st.text_area(
            "Conjunto de datos",
            key="raw_values",
            height=86,
            help="Separa los valores con comas, espacios, punto y coma o saltos de línea.",
            placeholder="Por ejemplo: 12, 15, 18, 22, 25",
            label_visibility="collapsed",
        )
        action, reset = st.columns([1.15, 1])
        with action:
            run = st.button("Actualizar análisis  →" if result is not None else "Ver mi análisis  →", type="primary", width="stretch")
        with reset:
            st.button("Cargar ejemplo", type="secondary", width="stretch", on_click=restore_example)
        if result is not None:
            st.button("Limpiar", type="tertiary", width="content", on_click=clear_data)

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
    st.markdown('<div class="section-eyebrow" style="margin:.4rem 0">RESUMEN &nbsp; / &nbsp; DISTRIBUCIÓN</div>', unsafe_allow_html=True)

    metrics = st.columns(4)
    for column, label, value in zip(
        metrics,
        ("Datos", "Mínimo", "Máximo", "Rango"),
        (f"{result['n']}", f"{result['min']:,.2f}", f"{result['max']:,.2f}", f"{result['range']:,.2f}"),
    ):
        column.metric(label, value)

    if result["mode_count"] > 1:
        insight = (
            f"El valor <strong>{result['mode']:g}</strong> es el más repetido "
            f"({result['mode_count']} veces). La mediana es <strong>{result['median']:,.2f}</strong>."
        )
    else:
        insight = (
            f"No hay valores repetidos: cada dato es único. "
            f"El promedio es <strong>{result['mean']:,.2f}</strong>."
        )
    st.markdown(
        f'<div class="insight-strip"><span class="insight-icon">💡</span><span><strong>Un dato curioso:</strong> {insight}</span></div>',
        unsafe_allow_html=True,
    )

    chart_column, table_column = st.columns([1.1, 1], gap="medium")
    with chart_column:
        with st.container(border=True, key="chart-card"):
            st.markdown("### Gráficos")
            st.caption(f"{result['k']} intervalos · amplitud {result['width']:.2f}")
            chart_kind = st.segmented_control(
                "Tipo de gráfico",
                options=["Barras", "Proporción", "Histograma"],
                default="Barras",
                key="chart-kind-v2",
                label_visibility="collapsed",
                width="stretch",
            )
            st.echarts_chart(
                chart_option(result, chart_kind or "Barras"),
                height=340,
                key="frequency-chart",
                alt=f"Frecuencias de datos agrupados en intervalos ({chart_kind or 'Barras'})",
            )

    with table_column:
        with st.container(border=True, key="table-card"):
            st.markdown("### Tabla de frecuencias")
            st.caption("Guarda o comparte tus resultados.")
            display_df = result["table"].copy()
            styled_df = (
                display_df.style
                .format({
                    "Marca de clase (Xi)": "{:.2f}",
                    "Frecuencia absoluta (fi)": "{:,.0f}",
                    "Frecuencia acumulada (Fi)": "{:,.0f}",
                    "Frecuencia relativa (hi)": "{:.4f}",
                    "Porcentaje (%)": "{:.2f}%",
                })
                .background_gradient(cmap="Purples", subset=["Frecuencia absoluta (fi)"])
                .background_gradient(cmap="YlGnBu", subset=["Marca de clase (Xi)"])
                .background_gradient(cmap="YlOrBr", subset=["Frecuencia acumulada (Fi)"])
                .background_gradient(cmap="BuGn", subset=["Frecuencia relativa (hi)"])
                .background_gradient(cmap="PuRd", subset=["Porcentaje (%)"])
                .set_table_styles([
                    {
                        "selector": "th",
                        "props": [
                            ("background-color", "#e7d9f6"),
                            ("color", "#433553"),
                            ("font-weight", "700"),
                            ("border-bottom", "2px solid #c9b3e1"),
                        ],
                    },
                    {
                        "selector": "tbody tr:nth-child(even) td",
                        "props": [("background-color", "rgba(246, 241, 252, .82)")],
                    },
                    {
                        "selector": "tbody tr:hover td",
                        "props": [("filter", "brightness(.96)")],
                    },
                ])
            )
            st.dataframe(
                styled_df,
                width="stretch",
                hide_index=True,
                height=250,
                alt="Tabla colorida con intervalos y frecuencias estadísticas",
            )
            csv = display_df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "Descargar CSV",
                data=csv,
                file_name="statia_datos.csv",
                mime="text/csv",
                width="stretch",
            )