import streamlit as st
from html import escape

from agent import analyze_incident, learn_from_incident


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OpsMind | Incident Command Center",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "page": "Dashboard",
    "analysis_result": None,
    "current_incident": "",
    "resolved": False,
    "resolution": "",
    "outcome": "",
    "incident_count": 0,
    "last_status": "Ready",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# PREMIUM COMMAND-CENTER CSS
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--bg:#f7f8fc;--surface:#fff;--surface-soft:#f9faff;--ink:#151827;--muted:#687085;--line:#e7e9f0;--purple:#6d4df2;--purple2:#8b6cf6;--purple-soft:#f1edff;--blue:#3b82f6;--cyan:#16a7c8;--green:#16a36a;--green-soft:#eaf8f1;--red:#dc4d5a;--amber:#d48a16}
*{box-sizing:border-box}.stApp{background:linear-gradient(180deg,#fbfbfd 0%,#f5f7fb 100%)!important;color:var(--ink)!important;font-family:Inter,ui-sans-serif,system-ui,sans-serif!important}.main .block-container{max-width:1440px!important;padding:30px 46px 56px!important}
/* LIGHT SIDEBAR */
section[data-testid="stSidebar"]{
        background:#EEE8FF !important;
        border-right:1px solid #263247 !important;
    }section[data-testid="stSidebar"] .block-container{padding:24px 16px!important;background:#eef0f7!important}section[data-testid="stSidebar"] *{font-family:Inter,ui-sans-serif,sans-serif!important}section[data-testid="stSidebar"] .stButton>button{background:transparent!important;color:#5e6678!important;border:1px solid transparent!important;border-radius:10px!important;min-height:42px!important;padding:8px 12px!important;font-size:12px!important;font-weight:600!important;text-align:left!important;box-shadow:none!important;transition:.16s ease!important}section[data-testid="stSidebar"] .stButton>button:hover{background:#f5f2ff!important;color:#5035c7!important;border-color:#e7defe!important;transform:translateX(2px)!important}section[data-testid="stSidebar"] button[kind="header"],section[data-testid="stSidebar"] button[aria-label="Collapse sidebar"],section[data-testid="stSidebar"] button[aria-label="Expand sidebar"],section[data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"]{display:none!important}
.brand{display:flex;align-items:center;gap:10px;margin:3px 5px 2px}.brand-mark{width:36px;height:36px;display:flex;align-items:center;justify-content:center;border-radius:10px;background:linear-gradient(135deg,#704cf2,#9a7cff);color:#fff;font-size:18px;box-shadow:0 8px 20px rgba(109,77,242,.2)}.brand-name{color:#171a27;font-family:'Space Grotesk',Inter,sans-serif!important;font-size:21px;font-weight:700;letter-spacing:-.7px}.brand-sub{color:#9097a8;font-size:9px;margin:5px 5px 22px;letter-spacing:.25px}.side-status{padding:13px;margin:0 2px 22px;border:1px solid #dfe2ea;border-radius:12px;background:#f4f6fb}.side-status-label,.side-section{color:#9aa1b0;font-size:8px;font-weight:800;letter-spacing:1.5px}.side-status-value{color:#159765;font-size:11px;font-weight:700;margin-top:5px}.side-section{text-transform:uppercase;margin:20px 4px 7px}.side-footer{margin:22px 2px 0;padding:12px;border:1px solid #dfe2ea;border-radius:12px;background:#e7e9f1;color:#737b8d;font-size:8px;line-height:1.5}.side-footer b{color:#454c5d}
/* TYPOGRAPHY */
.page-kicker{color:#7358d8;font-size:9px;font-weight:800;letter-spacing:1.7px;text-transform:uppercase;margin-bottom:7px}.page-title{color:#151827;font-family:'Space Grotesk',Inter,sans-serif!important;font-size:32px;line-height:1.08;font-weight:700;letter-spacing:-1.2px;margin-bottom:6px}.page-desc{color:#70788a;font-size:12px;line-height:1.65;margin-bottom:22px}.section-label{color:#8b93a4;font-size:8px;font-weight:800;letter-spacing:1.7px;text-transform:uppercase;margin:28px 0 10px}.footer{text-align:center;color:#a0a6b4;font-size:9px;padding:28px 0 4px}
/* HERO */
.hero{position:relative;overflow:hidden;min-height:300px;padding:34px 38px;border-radius:20px;background:linear-gradient(135deg,#ffffff 0%,#f6f2ff 58%,#eef7ff 100%);border:1px solid #e4e5ef;box-shadow:0 18px 50px rgba(35,29,75,.07)}.hero:before{content:'';position:absolute;width:470px;height:470px;right:-230px;top:-280px;border-radius:50%;border:1px solid rgba(109,77,242,.12);box-shadow:0 0 0 55px rgba(109,77,242,.035),0 0 0 110px rgba(109,77,242,.018)}.hero-grid{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1.35fr) minmax(310px,.65fr);gap:35px;align-items:center}.hero-eyebrow{display:inline-flex;align-items:center;gap:7px;padding:6px 10px;border-radius:999px;background:#fff;border:1px solid #e5e1f5;color:#655d7b;font-size:8px;font-weight:800;letter-spacing:1px;text-transform:uppercase;margin-bottom:15px}.live-dot{color:#18aa6c}.hero-title{color:#171927;font-family:'Space Grotesk',Inter,sans-serif!important;font-size:48px;font-weight:700;letter-spacing:-2.4px;line-height:1;margin-bottom:11px}.hero-title span{color:#7351ee}.hero-sub{color:#303548;font-size:17px;font-weight:650;margin-bottom:9px}.hero-desc{max-width:700px;color:#687185;font-size:12px;line-height:1.75}.hero-actions{margin-top:20px}.hero-action{display:inline-block;padding:9px 12px;margin-right:7px;border-radius:8px;background:#fff;border:1px solid #e4e6ed;color:#596175;font-size:9px;font-weight:700}.hero-visual{border:1px solid #e3e5ee;background:rgba(255,255,255,.78);border-radius:15px;padding:18px;box-shadow:0 10px 25px rgba(28,31,50,.04)}.hero-visual-title{color:#9299a8;font-size:8px;font-weight:800;letter-spacing:1.3px;text-transform:uppercase;margin-bottom:13px}.signal{display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid #eceef3}.signal:last-child{border-bottom:0}.signal-icon{width:29px;height:29px;display:flex;align-items:center;justify-content:center;border-radius:8px;background:#f0ecff;color:#6b4ee8;font-size:11px}.signal strong{display:block;color:#252b3b;font-size:10px}.signal small{color:#8991a2;font-size:8px}
/* COMPACT DASHBOARD */
.dashboard-hero{margin-top:18px!important;background:#fff;border:1px solid #e2e5ec;border-radius:18px;padding:24px 26px;box-shadow:0 8px 28px rgba(25,29,45,.035)}
.dashboard-hero-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(300px,.85fr);gap:22px;align-items:center}
.dashboard-kicker{color:#765be0;font-size:8px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px}
.dashboard-title{color:#171b29;font-family:'Space Grotesk',Inter,sans-serif!important;font-size:38px;font-weight:700;letter-spacing:-1.4px;line-height:1.05}
.dashboard-title span{color:#7351ee}
.dashboard-desc{color:#6f7789;font-size:13px;line-height:1.65;margin-top:8px;max-width:620px}
.dashboard-status{display:flex;justify-content:space-between;align-items:center;padding:12px 14px;background:#f4f6fb;border:1px solid #e5e7ee;border-radius:10px;margin-top:16px}
.dashboard-status b{color:#17895c;font-size:9px}
.dashboard-status span{color:#8a92a2;font-size:8px}
.dashboard-memory{border:1px solid #ddd5ff;background:#faf8ff;border-radius:13px;padding:16px}
.dashboard-memory-label{color:#7b67bd;font-size:8px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase}
.dashboard-memory-number{font-family:'Space Grotesk';font-size:30px;font-weight:700;color:#694fe0;margin-top:8px}
.dashboard-memory-note{font-size:9px;color:#81899b;margin-top:2px}
.dashboard-memory-line{height:1px;background:#e9e3ff;margin:12px 0}
.dashboard-memory-item{font-size:10px;color:#596276;padding:6px 0;border-bottom:1px solid #eeeaff}
.dashboard-memory-item:last-child{border-bottom:0}
.dashboard-incident{background:#fff;border:1px solid #e2e5ec;border-radius:15px;padding:17px}
.dashboard-incident-head{display:flex;justify-content:space-between;align-items:center;gap:10px}
.dashboard-incident-title{font-size:12px;font-weight:700;color:#202637}
.dashboard-incident-badge{padding:5px 8px;border-radius:999px;background:#fff2f2;border:1px solid #ffdfe1;color:#c84a55;font-size:7px;font-weight:800}
.dashboard-incident-text{font-size:11px;line-height:1.65;color:#6c7587;margin-top:8px}
.dashboard-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.dashboard-tag{padding:4px 7px;border-radius:5px;background:#f6f7fa;border:1px solid #e3e6ed;color:#727b8d;font-size:7px}
.dashboard-empty{padding:18px;background:#f8f9fc;border:1px dashed #dfe3eb;border-radius:10px;color:#7d8697;font-size:9px;line-height:1.5}
.dashboard-loop{background:#fff;border:1px solid #e2e5ec;border-radius:15px;padding:17px}
.dashboard-loop-title{font-size:12px;font-weight:700;color:#202637}
.dashboard-loop-sub{font-size:10px;color:#838b9c;margin-top:3px}
.dashboard-loop-steps{display:grid;grid-template-columns:repeat(5,1fr);gap:7px;margin-top:13px}
.dashboard-loop-step{padding:10px;background:#f8f9fc;border:1px solid #e4e7ee;border-radius:9px}
.dashboard-loop-step.memory{background:#f6f2ff;border-color:#d9cffd}
.dashboard-loop-step small{font-size:7px;color:#9098a8}
.dashboard-loop-step b{display:block;font-size:10px;color:#465064;margin-top:4px}
.dashboard-loop-step.memory b{color:#654bc8}
@media(max-width:1000px){.dashboard-hero-grid{grid-template-columns:1fr}.dashboard-loop-steps{grid-template-columns:repeat(2,1fr)}}
/* KPI */
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.kpi{position:relative;padding:16px 17px;background:#fff;border:1px solid #e5e7ee;border-radius:13px;box-shadow:0 6px 20px rgba(25,29,45,.035)}.kpi-accent{position:absolute;left:0;top:12px;bottom:12px;width:3px;border-radius:0 3px 3px 0;background:#7357e8}.kpi.green .kpi-accent{background:#19a66e}.kpi.cyan .kpi-accent{background:#199fbe}.kpi.amber .kpi-accent{background:#d49120}.kpi-label{color:#8a92a2;font-size:8px;font-weight:800;letter-spacing:1.1px;text-transform:uppercase}.kpi-value{color:#171c2b;font-family:'Space Grotesk',Inter,sans-serif!important;font-size:22px;font-weight:700;margin-top:7px}.kpi-note{color:#9aa1af;font-size:8px;margin-top:3px}
/* PANELS */
.panel{background:#fff;border:1px solid #e5e7ee;border-radius:15px;padding:18px;box-shadow:0 7px 24px rgba(25,29,45,.03)}.panel-dark{background:#fff;border:1px solid #e5e7ee;color:var(--ink)}.panel-title{color:#202637;font-size:13px;font-weight:700}.panel-dark .panel-title{color:#202637}.panel-sub,.panel-dark .panel-sub{color:#7a8395;font-size:11px;line-height:1.65;margin-top:4px}
/* LOOP */
.loop-panel{background:#fff;border:1px solid #e1e3eb;border-radius:17px;padding:19px;box-shadow:0 10px 30px rgba(25,29,45,.035)}.loop-head{display:flex;justify-content:space-between;gap:20px;align-items:flex-start}.loop-title{color:#202637;font-size:14px;font-weight:700}.loop-sub{color:#7f8798;font-size:9px;margin-top:4px}.loop-badge{padding:6px 9px;border-radius:999px;color:#16865a;background:#ecf9f2;border:1px solid #d4efdf;font-size:8px;font-weight:800}.loop-line{height:1px;background:#e8eaf0;margin:16px 0}.loop-steps{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}.loop-step{padding:12px;border:1px solid #e4e7ee;background:#fafbfe;border-radius:10px}.loop-step.memory{border-color:#cfc1ff;background:#f7f3ff}.loop-num{color:#8e96a6;font-size:7px;font-weight:800;letter-spacing:1px}.loop-step.memory .loop-num{color:#7658dc}.loop-name{color:#394154;font-size:9px;font-weight:700;margin-top:5px}.loop-step.memory .loop-name{color:#5e43c2}
/* INVESTIGATION */
.incident-shell{background:#fff;border:1px solid #e4e6ed;border-radius:17px;overflow:hidden;box-shadow:0 8px 26px rgba(25,29,45,.03)}.incident-head{display:flex;justify-content:space-between;align-items:center;padding:16px 18px;border-bottom:1px solid #e9ebf0;background:#fbfcfe}.incident-label{color:#687286;font-size:8px;font-weight:800;letter-spacing:1.4px;text-transform:uppercase}.status-chip{padding:5px 8px;border-radius:999px;background:#fff6e7;color:#a96e09;font-size:8px;font-weight:800}.status-chip.ready{background:#edf8f2;color:#278053}.status-chip.learned{background:#f1edff;color:#6952c5}.memory-signal{display:flex;align-items:center;gap:8px;padding:11px 13px;background:#f7f4ff;border:1px solid #e5dcff;border-radius:10px;color:#6553a8;font-size:9px;line-height:1.5}.analysis-wrap{background:#fff;border:1px solid #e3e5ec;border-radius:16px;padding:19px 21px}.analysis-head{display:flex;justify-content:space-between;align-items:center;gap:15px;margin-bottom:14px}.analysis-kicker{color:#7861d5;font-size:8px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase}.analysis-title{color:#172033;font-family:'Space Grotesk',Inter,sans-serif!important;font-size:17px;font-weight:700;margin-top:3px}.analysis-tag{padding:6px 8px;border-radius:7px;color:#2b7e59;background:#edf8f2;font-size:8px;font-weight:800;white-space:nowrap}.analysis-wrap .stMarkdown{color:#30394a!important}.analysis-wrap .stMarkdown h1,.analysis-wrap .stMarkdown h2,.analysis-wrap .stMarkdown h3{color:#172033!important;font-family:'Space Grotesk',Inter,sans-serif!important}.analysis-wrap .stMarkdown h2{font-size:16px!important;margin-top:20px!important}.analysis-wrap .stMarkdown h3{font-size:13px!important}.analysis-wrap .stMarkdown p,.analysis-wrap .stMarkdown li{font-size:11px!important;line-height:1.7!important;color:#4c5668!important}.analysis-wrap .stMarkdown strong{color:#222b3c!important}.analysis-wrap table{font-size:10px!important}
/* MEMORY */
.memory-card{background:#fff;border:1px solid #e4e6ed;border-left:3px solid #8068df;border-radius:11px;padding:13px 14px;margin-bottom:8px;box-shadow:0 5px 17px rgba(15,23,42,.025)}.memory-meta{color:#8c95a5;font-size:7px;font-weight:800;letter-spacing:1.1px;text-transform:uppercase;margin-bottom:6px}.memory-text{color:#465064;font-size:10px;line-height:1.6}
/* LEARN */
.learning-hero{padding:20px;border-radius:15px;background:linear-gradient(135deg,#f4f1ff,#fff);border:1px solid #e4ddfa}.learning-hero-title{color:#292341;font-family:'Space Grotesk',Inter,sans-serif!important;font-size:18px;font-weight:700}.learning-hero-text{color:#77718a;font-size:10px;line-height:1.6;margin-top:5px}.learn-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.learn-card{padding:14px;border:1px solid #e4e6ed;border-radius:11px;background:#fff}.learn-num{color:#8068df;font-size:8px;font-weight:800;letter-spacing:1px}.learn-title{color:#253044;font-size:10px;font-weight:700;margin-top:6px}.learn-text{color:#7d8798;font-size:9px;line-height:1.55;margin-top:4px}
/* INPUTS */
div[data-baseweb="textarea"]>div{background:#fff!important;border:1px solid #dfe3eb!important;border-radius:11px!important;box-shadow:none!important}div[data-baseweb="textarea"]>div:focus-within{border-color:#8068df!important;box-shadow:0 0 0 3px rgba(128,104,223,.09)!important}label{color:#5d687b!important;font-size:10px!important;font-weight:700!important}.stButton>button{min-height:40px!important;border-radius:9px!important;font-size:10px!important;font-weight:700!important;border:1px solid #dfe3eb!important;box-shadow:none!important;transition:.18s ease!important}.stButton>button:hover{transform:translateY(-1px)!important;box-shadow:0 8px 20px rgba(15,23,42,.06)!important}button[kind="primary"]{background:linear-gradient(135deg,#684de0,#8067e9)!important;color:#fff!important;border:0!important;box-shadow:0 8px 20px rgba(104,77,224,.20)!important}.stAlert{border-radius:10px!important;font-size:10px!important}hr{border-color:#e7eaf0!important}
@media(max-width:1000px){.hero-grid{grid-template-columns:1fr}.kpi-grid{grid-template-columns:repeat(2,1fr)}.loop-steps{grid-template-columns:repeat(2,1fr)}}

/* FINAL SIDEBAR + TYPOGRAPHY OVERRIDES */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background: #EEE8FF !important;
}
section[data-testid="stSidebar"] * {
    color: #3B2A68;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #5A4A82 !important;
    font-size: 14px !important;
}
section[data-testid="stSidebar"] button {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #D7DEEA !important;
}
section[data-testid="stSidebar"] button:hover {
    background: #DED1FF !important;
}
section[data-testid="stSidebar"] .stButton > button {
    color: #3B2A68 !important;
    background: transparent !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    color: #FFFFFF !important;
}


/* FINAL READABILITY */
.dashboard-title { font-size: 42px !important; line-height: 1.08 !important; }
.dashboard-desc { font-size: 15px !important; line-height: 1.65 !important; }
.dashboard-kicker, .section-label { font-size: 10px !important; letter-spacing: 1.8px !important; }
.kpi-label { font-size: 10px !important; letter-spacing: 1.4px !important; }
.kpi-value { font-size: 22px !important; }
.kpi-note { font-size: 10px !important; }
.dashboard-memory-label { font-size: 10px !important; letter-spacing: 1.6px !important; }
.dashboard-memory-number { font-size: 28px !important; }
.dashboard-memory-note,
.dashboard-memory-item { font-size: 11px !important; }
.learn-title { font-size: 15px !important; }
.learn-desc { font-size: 12px !important; line-height: 1.55 !important; }
.learn-num { font-size: 10px !important; }
.learn-name { font-size: 13px !important; }
.stButton > button { font-size: 14px !important; font-weight: 600 !important; }



/* FINAL SIDEBAR — PREMIUM LAVENDER */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background: #E7DEFA !important;
    border-right: 1px solid #D4C7EF !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #51446F !important;
}

section[data-testid="stSidebar"] .brand {
    margin-bottom: 4px !important;
}

section[data-testid="stSidebar"] .brand-name {
    color: #21163D !important;
    font-size: 20px !important;
    font-weight: 750 !important;
}

section[data-testid="stSidebar"] .brand-sub {
    color: #776A96 !important;
    font-size: 9px !important;
    letter-spacing: .8px !important;
}

section[data-testid="stSidebar"] .side-section {
    color: #75698E !important;
    font-size: 9px !important;
    letter-spacing: 1.6px !important;
    font-weight: 700 !important;
    margin-top: 24px !important;
    margin-bottom: 8px !important;
}

section[data-testid="stSidebar"] .side-status {
    background: #F0EAFE !important;
    border: 1px solid #D6C9F0 !important;
    border-radius: 12px !important;
    padding: 13px 14px !important;
    margin-top: 18px !important;
}

section[data-testid="stSidebar"] .side-status-label {
    color: #8579A0 !important;
    font-size: 9px !important;
    letter-spacing: 1.2px !important;
}

section[data-testid="stSidebar"] .side-status-value {
    color: #168A52 !important;
    font-size: 12px !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] .stButton {
    margin: 2px 0 !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 9px !important;
    color: #4D3D70 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    min-height: 40px !important;
    padding: 8px 12px !important;
    text-align: left !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: #DCD0F3 !important;
    color: #2D1B55 !important;
    border-color: #D1C2EC !important;
}

section[data-testid="stSidebar"] .nav-active {
    width: 100% !important;
    box-sizing: border-box !important;
    min-height: 40px !important;
    padding: 9px 12px !important;
    margin: 2px 0 !important;
    border-radius: 9px !important;
    background: #7048E8 !important;
    color: #FFFFFF !important;
    font-size: 14px !important;
    font-weight: 650 !important;
    line-height: 1.4 !important;
    box-shadow: 0 4px 10px rgba(112,72,232,.16) !important;
}

section[data-testid="stSidebar"] .nav-active * {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] .brand-mark {
    background: #7048E8 !important;
    color: #FFFFFF !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] .side-section + div {
    margin-top: 0 !important;
}


/* ============================================================
   HIDE STREAMLIT PLATFORM UI — OPSMIND ONLY
   ============================================================ */

/* Remove Streamlit top header / toolbar */
header[data-testid="stHeader"] {
    display: none !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stAppDeployButton"] {
    display: none !important;
}

/* Remove top-right Streamlit menu */
#MainMenu {
    display: none !important;
}

button[title="View app menu"] {
    display: none !important;
}

/* Remove Streamlit footer */
footer {
    display: none !important;
}

/* Remove empty top spacing created by the hidden header */
.block-container {
    padding-top: 2.2rem !important;
}

/* Hide Streamlit's sidebar collapse/expand controls */
section[data-testid="stSidebar"] button[kind="header"],
section[data-testid="stSidebar"] button[aria-label="Collapse sidebar"],
section[data-testid="stSidebar"] button[aria-label="Expand sidebar"],
section[data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"] {
    display: none !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def go_to(page):
    st.session_state.page = page
    st.rerun()


def reset_incident():
    st.session_state.analysis_result = None
    st.session_state.current_incident = ""
    st.session_state.resolved = False
    st.session_state.resolution = ""
    st.session_state.outcome = ""
    st.session_state.last_status = "Ready"


def get_memories():
    if not st.session_state.analysis_result:
        return []
    memories = st.session_state.analysis_result.get("memories", [])
    unique = []
    for memory in memories:
        if memory and memory not in unique:
            unique.append(memory)
    return unique


def topbar(title, description, kicker="OPS MIND"):
    st.markdown(
        f"""
        <div class="page-kicker">{escape(kicker)}</div>
        <div class="page-title">{escape(title)}</div>
        <div class="page-desc">{escape(description)}</div>
        """,
        unsafe_allow_html=True,
    )


def memory_cards(memories, limit=None):
    items = memories if limit is None else memories[:limit]
    for i, memory in enumerate(items, 1):
        st.markdown(
            f"""
            <div class="memory-card">
                <div class="memory-meta">HINDSIGHT MEMORY · {i:02d}</div>
                <div class="memory-text">{escape(str(memory))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">✦</div>
            <div class="brand-name">OpsMind</div>
        </div>
        <div class="brand-sub">AI INCIDENT COMMAND CENTER</div>

        <div class="side-status">
            <div class="side-status-label">MEMORY INFRASTRUCTURE</div>
            <div class="side-status-value">● Hindsight Connected</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-section">Command Center</div>', unsafe_allow_html=True)
    # Active page is rendered as a filled purple navigation item.
    # Other pages remain normal clickable sidebar buttons.
    if st.session_state.page == "Dashboard":
        st.markdown('<div class="nav-active">◈ &nbsp; Overview</div>', unsafe_allow_html=True)
    elif st.button("◈   Overview", width="stretch"):
        go_to("Dashboard")

    if st.session_state.page == "Investigate":
        st.markdown('<div class="nav-active">⌁ &nbsp; Investigate Incident</div>', unsafe_allow_html=True)
    elif st.button("⌁   Investigate Incident", width="stretch"):
        go_to("Investigate")

    if st.session_state.page == "Memory":
        st.markdown('<div class="nav-active">◉ &nbsp; Hindsight Memory</div>', unsafe_allow_html=True)
    elif st.button("◉   Hindsight Memory", width="stretch"):
        go_to("Memory")

    if st.session_state.page == "Learn":
        st.markdown('<div class="nav-active">↗ &nbsp; Learn & Improve</div>', unsafe_allow_html=True)
    elif st.button("↗   Learn & Improve", width="stretch"):
        go_to("Learn")

    st.markdown('<div class="side-section">Actions</div>', unsafe_allow_html=True)
    if st.button("＋   Start New Incident", width="stretch"):
        reset_incident()
        go_to("Investigate")



# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    memories = get_memories()
    current_status = "Learned" if st.session_state.resolved else ("Analyzed" if st.session_state.analysis_result else "Ready")

    # ========================================================
    # CLEAN LIGHT DASHBOARD
    # ========================================================

    st.markdown(
        f"""
        <div class="dashboard-hero"><div class="dashboard-hero-grid"><div><div class="dashboard-kicker">AI INCIDENT COMMAND CENTER</div><div class="dashboard-title">Operational intelligence,<br><span>with memory.</span></div><div class="dashboard-desc">Investigate production incidents using what your team has already learned.</div><div class="dashboard-status"><span>Hindsight memory infrastructure</span><b>● Connected</b></div></div><div class="dashboard-memory"><div class="dashboard-memory-label">HINDSIGHT RECALL</div><div class="dashboard-memory-number">{len(memories)}</div><div class="dashboard-memory-note">relevant experiences recalled</div><div class="dashboard-memory-line"></div><div class="dashboard-memory-item">Previous incidents</div><div class="dashboard-memory-item">Previous resolutions</div><div class="dashboard-memory-item">Previous outcomes</div></div></div></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">Command status</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi green">
                <div class="kpi-accent"></div>
                <div class="kpi-label">Hindsight</div>
                <div class="kpi-value">Connected</div>
                <div class="kpi-note">Memory layer</div>
            </div>
            <div class="kpi cyan">
                <div class="kpi-accent"></div>
                <div class="kpi-label">Memories recalled</div>
                <div class="kpi-value">{len(memories)}</div>
                <div class="kpi-note">Latest investigation</div>
            </div>
            <div class="kpi">
                <div class="kpi-accent"></div>
                <div class="kpi-label">Incident state</div>
                <div class="kpi-value">{escape(current_status)}</div>
                <div class="kpi-note">Current session</div>
            </div>
            <div class="kpi amber">
                <div class="kpi-accent"></div>
                <div class="kpi-label">AI engine</div>
                <div class="kpi-value">Groq</div>
                <div class="kpi-note">Reasoning layer</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">Current incident</div>', unsafe_allow_html=True)

    if st.session_state.current_incident:
        incident_text = escape(st.session_state.current_incident)
        incident_badge = "LEARNED" if st.session_state.resolved else ("ANALYZED" if st.session_state.analysis_result else "READY")
        st.markdown(
            f"""
            <div class="dashboard-incident">
                <div class="dashboard-incident-head">
                    <div class="dashboard-incident-title">Production incident</div>
                    <div class="dashboard-incident-badge">{incident_badge}</div>
                </div>
                <div class="dashboard-incident-text">{incident_text}</div>
                <div class="dashboard-tags">
                    <span class="dashboard-tag">PRODUCTION</span>
                    <span class="dashboard-tag">INCIDENT</span>
                    <span class="dashboard-tag">HINDSIGHT</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="dashboard-empty">
                No active incident. Start an investigation to bring a production issue into the command center.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("Open Investigation  →", type="primary", width="stretch"):
        go_to("Investigate")

    st.markdown('<div class="section-label">How OpsMind learns</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="dashboard-loop">
            <div class="dashboard-loop-title">One continuous memory loop</div>
            <div class="dashboard-loop-sub">Every confirmed resolution becomes useful context for the next incident.</div>
            <div class="dashboard-loop-steps">
                <div class="dashboard-loop-step"><small>01</small><b>Detect</b></div>
                <div class="dashboard-loop-step memory"><small>02</small><b>Recall</b></div>
                <div class="dashboard-loop-step"><small>03</small><b>Analyze</b></div>
                <div class="dashboard-loop-step"><small>04</small><b>Resolve</b></div>
                <div class="dashboard-loop-step memory"><small>05</small><b>Remember ↻</b></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="footer">OpsMind · Hindsight + Groq</div>', unsafe_allow_html=True)

# ============================================================
# INVESTIGATE
# ============================================================

elif st.session_state.page == "Investigate":

    topbar(
        "Incident Investigation",
        "Turn a production symptom into a memory-enhanced investigation.",
        "INCIDENT COMMAND",
    )

    current_state = "Learned" if st.session_state.resolved else ("Analyzed" if st.session_state.analysis_result else "Ready")
    chip_class = "learned" if st.session_state.resolved else ("ready" if current_state == "Ready" else "")

    st.markdown(
        f"""
        <div class="incident-shell">
            <div class="incident-head">
                <div class="incident-label">NEW PRODUCTION INCIDENT</div>
                <div class="status-chip {chip_class}">● {escape(current_state)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    incident = st.text_area(
        "Incident description",
        value=st.session_state.current_incident,
        height=145,
        placeholder=(
            "Example:\n\nProduction checkout API is returning HTTP 503 errors after today's deployment. "
            "Customers cannot complete payments. PostgreSQL connections are timing out."
        ),
    )

    b1, b2 = st.columns([3.2, 1])
    with b1:
        if st.button("🧠  Analyze with OpsMind", type="primary", width="stretch"):
            if not incident.strip():
                st.warning("Describe the production incident first.")
            else:
                st.session_state.current_incident = incident
                st.session_state.resolved = False
                st.session_state.last_status = "Analyzing"
                with st.spinner("Recalling Hindsight experience and generating the investigation..."):
                    try:
                        result = analyze_incident(incident)
                        st.session_state.analysis_result = result
                        st.session_state.incident_count += 1
                        st.session_state.last_status = "Analysis Complete"
                        st.success("Incident analyzed successfully.")
                    except Exception as e:
                        st.error("Unable to analyze the incident.")
                        st.exception(e)
    with b2:
        if st.button("＋  New Incident", width="stretch"):
            reset_incident()
            st.rerun()

    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        analysis = result.get("analysis", "")
        memories = get_memories()

        st.markdown('<div class="section-label">Investigation signal</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="memory-signal">
                <span>🧠</span>
                <span><b>{len(memories)} relevant experiences recalled</b> from Hindsight before the AI generated this response.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="section-label">AI investigation</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="analysis-wrap">
                <div class="analysis-head">
                    <div>
                        <div class="analysis-kicker">AI INCIDENT INTELLIGENCE</div>
                        <div class="analysis-title">Memory-enhanced investigation complete</div>
                    </div>
                    <div class="analysis-tag">● HINDSIGHT ACTIVE</div>
                </div>
            """
            , unsafe_allow_html=True,
        )
        st.markdown(analysis)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-label">Evidence used</div>', unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Memories recalled", len(memories))
        with m2:
            st.metric("Memory system", "Hindsight")
        with m3:
            st.metric("Reasoning engine", "Groq")

        st.markdown('<div class="section-label">Recalled operational experience</div>', unsafe_allow_html=True)
        if memories:
            memory_cards(memories)
        else:
            st.info("No relevant previous incidents were found for this investigation.")

        st.markdown('<div class="section-label">Next action</div>', unsafe_allow_html=True)
        if st.button("Record confirmed resolution →", type="primary", width="stretch"):
            go_to("Learn")

    st.markdown('<div class="footer">OpsMind · Investigate with context, not from zero</div>', unsafe_allow_html=True)


# ============================================================
# MEMORY
# ============================================================

elif st.session_state.page == "Memory":

    topbar(
        "Hindsight Memory",
        "Inspect the operational experience retrieved for the current incident.",
        "MEMORY INTELLIGENCE",
    )

    memories = get_memories()

    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi cyan"><div class="kpi-accent"></div><div class="kpi-label">Relevant memories</div><div class="kpi-value">{len(memories)}</div><div class="kpi-note">Retrieved for this incident</div></div>
            <div class="kpi"><div class="kpi-accent"></div><div class="kpi-label">Memory engine</div><div class="kpi-value">Hindsight</div><div class="kpi-note">Persistent experience layer</div></div>
            <div class="kpi green"><div class="kpi-accent"></div><div class="kpi-label">Connection</div><div class="kpi-value">Live</div><div class="kpi-note">Ready for recall + retain</div></div>
            <div class="kpi amber"><div class="kpi-accent"></div><div class="kpi-label">AI reasoning</div><div class="kpi-value">Groq</div><div class="kpi-note">Memory-grounded analysis</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">Why memory matters</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-dark panel">
            <div class="panel-title">A normal AI starts with the incident. OpsMind starts with the incident <i>and</i> experience.</div>
            <div class="panel-sub">Hindsight retrieves relevant historical knowledge, while the confirmed outcome of today's incident can become context for tomorrow's investigation. This makes memory part of the response loop rather than a passive archive.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.current_incident:
        st.markdown('<div class="section-label">Current incident</div>', unsafe_allow_html=True)
        st.info(st.session_state.current_incident)

    st.markdown('<div class="section-label">Retrieved experience</div>', unsafe_allow_html=True)
    if memories:
        memory_cards(memories)
    else:
        st.info("No recalled memories yet. Analyze an incident first.")

    st.markdown('<div class="section-label">Demo moment</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="learning-hero">
            <div class="learning-hero-title">Show the judge the memory loop.</div>
            <div class="learning-hero-text">Resolve one incident → save its outcome → submit a similar incident → show the retrieved experience → compare the resulting recommendation.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="footer">OpsMind · Persistent operational experience powered by Hindsight</div>', unsafe_allow_html=True)


# ============================================================
# LEARN
# ============================================================

elif st.session_state.page == "Learn":

    topbar(
        "Learn & Improve",
        "Turn a confirmed resolution into future incident knowledge.",
        "CONTINUOUS LEARNING",
    )

    if not st.session_state.current_incident:
        st.markdown(
            """
            <div class="learning-hero">
                <div class="learning-hero-title">No active incident yet.</div>
                <div class="learning-hero-text">Analyze an incident first, then record what actually fixed it and what happened afterwards.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Start Investigation →", type="primary"):
            go_to("Investigate")
    else:
        st.markdown(
            """
            <div class="learning-hero">
                <div class="learning-hero-title">🧠 Teach OpsMind what really happened.</div>
                <div class="learning-hero-text">The AI recommendation is only a hypothesis. The confirmed human resolution and outcome are what turn this incident into durable operational experience.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="section-label">Incident being learned</div>', unsafe_allow_html=True)
        st.info(st.session_state.current_incident)

        st.markdown('<div class="section-label">What fixed it?</div>', unsafe_allow_html=True)
        resolution = st.text_area(
            "Resolution",
            value=st.session_state.resolution,
            height=125,
            placeholder=(
                "Example: Rolled back the deployment, restored the previous database connection-pool configuration, and restarted the API service."
            ),
        )

        st.markdown('<div class="section-label">What happened afterwards?</div>', unsafe_allow_html=True)
        outcome = st.text_area(
            "Outcome",
            value=st.session_state.outcome,
            height=105,
            placeholder="Example: HTTP 503 errors stopped and customers were able to complete payments successfully.",
        )

        if st.button("💾  Save confirmed learning to Hindsight", type="primary", width="stretch"):
            if not resolution.strip():
                st.warning("Enter the resolution.")
            elif not outcome.strip():
                st.warning("Enter the outcome.")
            else:
                st.session_state.resolution = resolution
                st.session_state.outcome = outcome
                with st.spinner("Storing confirmed incident experience in Hindsight..."):
                    try:
                        learn_from_incident(
                            incident=st.session_state.current_incident,
                            resolution=resolution,
                            outcome=outcome,
                        )
                        st.session_state.resolved = True
                        st.session_state.last_status = "Learned"
                        st.success("Resolution saved to Hindsight.")
                    except Exception as e:
                        st.error("The resolution could not be saved.")
                        st.exception(e)

        if st.session_state.resolved:
            st.markdown('<div class="section-label">Learning recorded</div>', unsafe_allow_html=True)
            st.success("OpsMind learned from this incident — the incident, resolution and outcome are now stored as future operational knowledge.")

            st.markdown('<div class="section-label">The loop is now closed</div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="learn-grid">
                    <div class="learn-card"><div class="learn-num">01 · REMEMBER</div><div class="learn-title">Store experience</div><div class="learn-text">The incident and confirmed resolution are retained in Hindsight.</div></div>
                    <div class="learn-card"><div class="learn-num">02 · RECALL</div><div class="learn-title">Retrieve next time</div><div class="learn-text">A similar future incident can retrieve this operational experience.</div></div>
                    <div class="learn-card"><div class="learn-num">03 · IMPROVE</div><div class="learn-title">Respond with context</div><div class="learn-text">Future AI investigations begin with more relevant evidence.</div></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            if st.button("↻  Test another similar incident", type="primary", width="stretch"):
                reset_incident()
                go_to("Investigate")

    st.markdown('<div class="footer">OpsMind · Detect · Recall · Analyze · Resolve · Learn</div>', unsafe_allow_html=True)
