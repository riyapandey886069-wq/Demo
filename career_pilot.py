import os
import json
import random
import streamlit as st
import pandas as pd

# Optional real AI support
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareerPilot - AI Career Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>



.st-emotion-cache-pgu27n{
color:black !important;
}


.stRadio label p, .stSelectbox label p{
background:#eafefd !important;
border:1px solid #eafefd !important;
}
.st-emotion-cache-1cv0o6g{
background:white !important;

}
/* =========================================================
   PALETTE (reference)
   --teal-deep:   #008080
   --teal-mid:    #40B5A0
   --turquoise:   #00CED1
   --cyan-light:  #E0FFFF
   --seagreen:    #2E8B57
   --cadet:       #5F9EA0
   --lightsea:    #20B2AA
   --aqua-bright: #8BFFFF
   --azure:       #F0FFFF
   --teal-ink:    #004D4D
========================================================= */

:root {
    --teal-deep:   #008080;
    --teal-mid:    #40B5A0;
    --turquoise:   #00CED1;
    --cyan-light:  #E0FFFF;
    --seagreen:    #2E8B57;
    --cadet:       #5F9EA0;
    --lightsea:    #20B2AA;
    --aqua-bright: #8BFFFF;
    --azure:       #F0FFFF;
    --teal-ink:    #004D4D;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

html { scroll-behavior: smooth; }

/* =========================================================
   GLOBAL — minimal, airy, slowly breathing gradient
========================================================= */

.stApp {
    background:
        radial-gradient(circle at 8% 8%, rgba(0,206,209,0.14), transparent 32%),
        radial-gradient(circle at 92% 15%, rgba(46,139,87,0.10), transparent 34%),
        radial-gradient(circle at 50% 100%, rgba(64,181,160,0.10), transparent 38%),
        linear-gradient(135deg, var(--azure) 0%, #eefffe 45%, var(--cyan-light) 100%);
    background-size: 200% 200%;
    animation: bgDrift 22s ease-in-out infinite;
    color: var(--teal-ink);
    font-family: "Inter", "Segoe UI", sans-serif;
}

@keyframes bgDrift {
    0%   { background-position: 0% 0%; }
    50%  { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}


/* =========================================================
   SIDEBAR — clean glass panel
========================================================= */

section[data-testid="stSidebar"] {
    background: rgba(240,255,255,0.75);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-right: 1px solid rgba(0,128,128,0.18);
    box-shadow: 6px 0 30px rgba(0,77,77,0.06);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--teal-ink) !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #0f3d3d !important;
    font-weight: 600;
}

section[data-testid="stSidebar"] .stRadio label {
    border-radius: 12px;
    padding: 9px 12px;
    position: relative;
    transition: all 0.3s cubic-bezier(.4,0,.2,1);
}

section[data-testid="stSidebar"] .stRadio label::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 12px;
    background: linear-gradient(90deg, var(--turquoise), var(--teal-mid));
    opacity: 0;
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.35s ease, opacity 0.35s ease;
    z-index: -1;
}

section[data-testid="stSidebar"] .stRadio label:hover::before {
    opacity: 0.14;
    transform: scaleX(1);
}

section[data-testid="stSidebar"] .stRadio label:hover {
    transform: translateX(5px);
    color: var(--teal-deep) !important;
}


/* =========================================================
   TEXT
========================================================= */

h1, h2, h3, h4 {
    color: var(--teal-ink) !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

p, label, .stMarkdown {
    color: #14514f;
}

.stRadio label p, .stSelectbox label p {
    color: var(--teal-ink) !important;
    font-weight: 600 !important;
}


/* =========================================================
   HERO — glass card, animated gradient title, floating orbs
========================================================= */

.hero {
    position: relative;
    padding: 44px;
    border-radius: 28px;
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(0,206,209,0.30);
    box-shadow:
        0 20px 55px rgba(0,128,128,0.14),
        inset 0 1px 0 rgba(255,255,255,0.6);
    margin-bottom: 28px;
    overflow: hidden;
    animation: fadeUp 0.7s ease;
}

.hero::before,
.hero::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    filter: blur(2px);
    pointer-events: none;
}

.hero::before {
    width: 260px;
    height: 260px;
    right: -80px;
    top: -100px;
    background: radial-gradient(circle, rgba(0,206,209,0.35), transparent 70%);
    animation: floatingGlow 7s ease-in-out infinite;
}

.hero::after {
    width: 180px;
    height: 180px;
    left: -60px;
    bottom: -80px;
    background: radial-gradient(circle, rgba(46,139,87,0.25), transparent 70%);
    animation: floatingGlow 9s ease-in-out infinite reverse;
}

.hero-title {
    font-size: 46px;
    font-weight: 850;
    letter-spacing: -1px;
    position: relative;
    background: linear-gradient(90deg, var(--teal-deep), var(--turquoise), var(--seagreen), var(--teal-deep));
    background-size: 300% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: shimmerText 6s linear infinite;
}

.hero-subtitle {
    font-size: 17px;
    color: #1a5c5a;
    font-weight: 600;
    margin-top: 10px;
    position: relative;
}

@keyframes shimmerText {
    0%   { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}


/* =========================================================
   DASHBOARD CARDS — minimal glass, animated gradient border
   on hover, gentle lift + glow
========================================================= */

.dashboard-card {
    position: relative;
    background: rgba(255,255,255,0.72);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0,128,128,0.16);
    border-radius: 20px;
    padding: 24px;
    min-height: 145px;
    box-shadow: 0 10px 26px rgba(0,77,77,0.08);
    overflow: hidden;
    transition: transform 0.4s cubic-bezier(.2,.8,.2,1), box-shadow 0.4s ease;
    animation: fadeUp 0.6s ease both;
}

.dashboard-card::before {
    content: "";
    position: absolute;
    inset: 0;
    padding: 1.5px;
    border-radius: 20px;
    background: linear-gradient(120deg, var(--turquoise), var(--teal-mid), var(--seagreen), var(--turquoise));
    background-size: 260% 260%;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: 0;
    transition: opacity 0.4s ease;
    animation: borderFlow 5s linear infinite;
}

.dashboard-card:hover::before { opacity: 1; }

.dashboard-card:hover {
    transform: translateY(-8px) scale(1.015);
    box-shadow: 0 24px 50px rgba(0,206,209,0.24);
}

@keyframes borderFlow {
    0%   { background-position: 0% 50%; }
    100% { background-position: 260% 50%; }
}

.card-title {
    color: #2f7d78;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

.card-value {
    color: var(--teal-ink);
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -1px;
    display: inline-block;
}

.card-subtitle {
    color: #5b8f8c;
    font-size: 13px;
    font-weight: 500;
    margin-top: 8px;
}

/* Stagger entrance so cards cascade in */
.dashboard-card:nth-of-type(1) { animation-delay: 0.05s; }
.dashboard-card:nth-of-type(2) { animation-delay: 0.15s; }
.dashboard-card:nth-of-type(3) { animation-delay: 0.25s; }
.dashboard-card:nth-of-type(4) { animation-delay: 0.35s; }


/* =========================================================
   SECTION BOX
========================================================= */

.section-box {
    background: rgba(255,255,255,0.70);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0,128,128,0.16);
    border-radius: 22px;
    padding: 26px;
    margin-top: 20px;
    box-shadow: 0 10px 30px rgba(0,77,77,0.07);
    transition: all 0.35s ease;
    animation: fadeUp 0.7s ease;
}

.section-box:hover {
    box-shadow: 0 20px 44px rgba(0,206,209,0.16);
    border-color: rgba(0,206,209,0.32);
}


/* =========================================================
   BUTTONS — animated gradient sweep + soft glow pulse
========================================================= */

.stButton > button {
    position: relative;
    border-radius: 12px;
    border: none;
    background: linear-gradient(90deg, var(--teal-deep), var(--turquoise), var(--seagreen), var(--teal-deep));
    background-size: 300% auto;
    color: white;
    font-weight: 700;
    padding: 11px 24px;
    box-shadow: 0 8px 22px rgba(0,128,128,0.30);
    overflow: hidden;
    transition: background-position 0.6s ease, transform 0.25s ease, box-shadow 0.25s ease;
}

.stButton > button::after {
    content: "";
    position: absolute;
    top: 0; left: -60%;
    width: 40%; height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255,255,255,0.55), transparent);
    transform: skewX(-20deg);
    transition: left 0.6s ease;
}

.stButton > button:hover {
    background-position: right center;
    transform: translateY(-3px);
    box-shadow: 0 14px 32px rgba(0,206,209,0.40);
}

.stButton > button:hover::after { left: 130%; }

.stButton > button:active { transform: scale(0.96); }


/* =========================================================
   PROGRESS BAR — animated shimmer fill
========================================================= */

.progress-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 7px;
    color: var(--teal-ink);
    font-size: 14px;
    font-weight: 700;
}

.progress-container {
    width: 100%;
    height: 12px;
    background: rgba(0,128,128,0.10);
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(0,128,128,0.14);
}

.progress-fill {
    position: relative;
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(90deg, var(--teal-deep), var(--turquoise), var(--lightsea));
    background-size: 200% auto;
    box-shadow: 0 3px 12px rgba(0,206,209,0.35);
    animation: progressAnimation 1.2s ease, gradientSlide 3s linear infinite;
}

.progress-fill::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.55), transparent);
    animation: shimmerSweep 1.8s ease-in-out infinite;
}

@keyframes shimmerSweep {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

@keyframes gradientSlide {
    0%   { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}


/* =========================================================
   BADGES — soft pop-in + hover lift
========================================================= */

.badge {
    display: inline-block;
    padding: 8px 14px;
    margin: 5px;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(0,206,209,0.14), rgba(46,139,87,0.10));
    border: 1px solid rgba(0,128,128,0.28);
    color: var(--teal-deep);
    font-weight: 700;
    font-size: 13px;
    transition: all 0.3s cubic-bezier(.34,1.56,.64,1);
}

.badge:hover {
    transform: translateY(-4px) scale(1.05);
    background: rgba(0,206,209,0.22);
    box-shadow: 0 8px 20px rgba(0,206,209,0.25);
}


/* =========================================================
   AI RESPONSE BOX — pulsing soft glow border
========================================================= */

.ai-box {
    position: relative;
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(0,206,209,0.30);
    padding: 24px;
    border-radius: 20px;
    margin-top: 16px;
    color: #0f3d3d;
    box-shadow: 0 10px 30px rgba(0,128,128,0.10);
    animation: fadeUp 0.6s ease, glowPulse 3.5s ease-in-out infinite;
}

@keyframes glowPulse {
    0%, 100% { box-shadow: 0 10px 30px rgba(0,128,128,0.10); }
    50%      { box-shadow: 0 10px 38px rgba(0,206,209,0.28); }
}


/* =========================================================
   INPUT BOXES
========================================================= */

.stTextInput input,
.stTextArea textarea,
.stSelectbox div,
.stNumberInput input {
    border-radius: 12px !important;
    border: 1.5px solid rgba(0,128,128,0.24) !important;
    background: #ffffff !important;
    color: var(--teal-ink) !important;
    font-weight: 500;
    transition: all 0.25s ease;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border: 1.5px solid var(--turquoise) !important;
    box-shadow: 0 0 0 4px rgba(0,206,209,0.16) !important;
}


/* =========================================================
   METRIC CARDS
========================================================= */

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.72);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(0,128,128,0.16);
    border-top: 3px solid var(--turquoise);
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 9px 24px rgba(0,77,77,0.07);
    transition: all 0.35s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(0,206,209,0.22);
}

[data-testid="stMetricValue"] {
    color: var(--teal-ink) !important;
    font-weight: 800 !important;
}

[data-testid="stMetricLabel"] {
    color: #2f7d78 !important;
    font-weight: 700 !important;
}


/* =========================================================
   TABS
========================================================= */

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(0,128,128,0.08);
    padding: 6px;
    border-radius: 14px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 9px 18px;
    color: #2f7d78;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: #ffffff;
    color: var(--teal-deep);
    font-weight: 800;
    box-shadow: 0 4px 14px rgba(0,77,77,0.10);
}


/* =========================================================
   EXPANDER
========================================================= */

.streamlit-expanderHeader {
    background: rgba(255,255,255,0.75) !important;
    border: 1px solid rgba(0,128,128,0.18) !important;
    border-radius: 14px !important;
    color: var(--teal-ink) !important;
    font-weight: 700 !important;
    transition: all 0.25s ease;
}

.streamlit-expanderHeader:hover {
    border-color: var(--turquoise) !important;
}


/* =========================================================
   DATAFRAME
========================================================= */

[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(0,128,128,0.18);
    box-shadow: 0 7px 24px rgba(0,77,77,0.08);
}


/* =========================================================
   FILE UPLOADER
========================================================= */

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.65);
    border: 2px dashed rgba(0,206,209,0.45);
    border-radius: 18px;
    padding: 10px;
    transition: all 0.3s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--turquoise);
    background: rgba(0,206,209,0.06);
}


/* =========================================================
   DIVIDERS
========================================================= */

hr {
    border: none;
    border-top: 1px solid rgba(0,128,128,0.16);
    margin: 25px 0;
}


/* =========================================================
   SMALL TEXT
========================================================= */

.small-muted {
    color: #5b8f8c;
    font-size: 13px;
    font-weight: 500;
}


/* =========================================================
   ANIMATIONS
========================================================= */

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes floatingGlow {
    0%   { transform: translate(0,0); }
    50%  { transform: translate(-18px,18px); }
    100% { transform: translate(0,0); }
}

@keyframes progressAnimation {
    from { width: 0%; }
}


/* =========================================================
   RESPONSIVE DESIGN
========================================================= */

@media (max-width: 768px) {
    .hero { padding: 26px; }
    .hero-title { font-size: 32px; }
    .hero-subtitle { font-size: 15px; }
    .dashboard-card { padding: 18px; }
    .card-value { font-size: 28px; }
}


/* =========================================================
   SCROLLBAR
========================================================= */

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--azure); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(var(--turquoise), var(--teal-deep));
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: var(--teal-ink); }


.stTextInput input, .stTextArea textarea, .stSelectbox div, .stNumberInput input{
border:none !important;
}


</style>
""", unsafe_allow_html=True)


# ============================================================
# OPTIONAL OPENAI CONFIGURATION
# ============================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = None

if OpenAI and OPENAI_API_KEY:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        openai_client = None


# ============================================================
# CAREER DATABASE
# ============================================================

career_data = {
    "Python Developer": {
        "skills": [
            "Python", "OOP", "SQL", "Git",
            "Django", "REST API", "Data Structures"
        ],
        "description": "Develops applications and backend systems using Python.",
        "salary": "₹3-6 LPA",
        "projects": [
            "Student Management System",
            "REST API with Django",
            "AI Chatbot"
        ]
    },

    "Data Scientist": {
        "skills": [
            "Python", "Statistics", "Pandas", "NumPy",
            "Machine Learning", "SQL", "Data Visualization"
        ],
        "description": "Analyzes data and builds machine learning models.",
        "salary": "₹5-9 LPA",
        "projects": [
            "House Price Prediction",
            "Customer Churn Analysis",
            "Student Performance Prediction"
        ]
    },

    "Machine Learning Engineer": {
        "skills": [
            "Python", "Machine Learning", "Deep Learning",
            "TensorFlow", "Scikit-learn", "SQL", "Statistics"
        ],
        "description": "Builds and deploys machine learning systems.",
        "salary": "₹5-10 LPA",
        "projects": [
            "ML Prediction API",
            "Recommendation System",
            "Image Classification System"
        ]
    },

    "AI Engineer": {
        "skills": [
            "Python", "Machine Learning", "Deep Learning",
            "NLP", "Computer Vision", "TensorFlow", "PyTorch"
        ],
        "description": "Develops artificial intelligence based applications.",
        "salary": "₹6-12 LPA",
        "projects": [
            "AI Career Advisor",
            "NLP Chatbot",
            "Computer Vision Application"
        ]
    },

    "Web Developer": {
        "skills": [
            "HTML", "CSS", "JavaScript", "Python",
            "SQL", "Git", "REST API"
        ],
        "description": "Creates and maintains modern web applications.",
        "salary": "₹3-7 LPA",
        "projects": [
            "Portfolio Website",
            "E-commerce Website",
            "Full Stack Student Portal"
        ]
    },

    "Data Analyst": {
        "skills": [
            "Python", "SQL", "Excel", "Statistics",
            "Pandas", "Data Visualization", "Power BI"
        ],
        "description": "Analyzes business data and creates useful insights.",
        "salary": "₹3-7 LPA",
        "projects": [
            "Sales Dashboard",
            "Student Analytics Dashboard",
            "Business KPI Analysis"
        ]
    },

    "Software Developer": {
        "skills": [
            "Python", "Java", "OOP",
            "Data Structures", "SQL", "Git", "Problem Solving"
        ],
        "description": "Designs and develops software applications.",
        "salary": "₹4-8 LPA",
        "projects": [
            "Banking Application",
            "Library Management System",
            "Desktop Productivity App"
        ]
    }
}


all_skills = sorted(set(
    skill
    for career in career_data.values()
    for skill in career["skills"]
))


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "current_skills": [],
    "missing_skills": [],
    "skill_score": 0.0,
    "skill_gap": 100.0,
    "predictions": [],
    "predicted_career": "",
    "ai_advice": "",
    "chat_history": [],
    "quiz_score": None,
    "quiz_questions": [],
    "project_progress": 50,
    "learning_progress": 50,
    "assessment_progress": 50,
    "interview_progress": 50
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚀 CareerPilot")

candidate_name = st.sidebar.text_input(
    "Candidate Name",
    placeholder="Enter your name"
)

education = st.sidebar.selectbox(
    "Education Level",
    ["BCA", "B.Tech", "MCA", "M.Tech", "B.Sc", "M.Sc", "Other"]
)

experience = st.sidebar.selectbox(
    "Experience Level",
    ["Fresher", "1-2 Years", "3-5 Years", "5+ Years"]
)

career_goal = st.sidebar.selectbox(
    "Target Career",
    list(career_data.keys())
)

st.sidebar.divider()

st.sidebar.subheader("📈 Progress Controls")

st.session_state.project_progress = st.sidebar.slider(
    "💻 Project Progress",
    0, 100, st.session_state.project_progress
)

st.session_state.learning_progress = st.sidebar.slider(
    "📚 Learning Progress",
    0, 100, st.session_state.learning_progress
)

st.session_state.assessment_progress = st.sidebar.slider(
    "🧪 Assessment Progress",
    0, 100, st.session_state.assessment_progress
)

st.session_state.interview_progress = st.sidebar.slider(
    "🎤 Interview Preparation",
    0, 100, st.session_state.interview_progress
)

st.sidebar.divider()

# if openai_client:
#     st.sidebar.success("🤖 Real AI Advisor: Connected")
# else:
#     st.sidebar.info(
#         "🤖 AI Advisor: Local mode\n\n"
#         "Add OPENAI_API_KEY to enable real AI."
#     )


# ============================================================
# HEADER
# ============================================================

display_name = candidate_name if candidate_name else "Future Professional"

st.markdown(f"""
<div class="hero">
    <h1>🚀 CareerPilot</h1>
    <p>AI Career Intelligence Platform</p>
    <p>Welcome, <b>{display_name}</b> 👋 — discover your best career path,
    understand your skill gaps and become job-ready.</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# FUNCTIONS
# ============================================================

def calculate_skill_gap(current_skills, target_career):
    required = career_data[target_career]["skills"]

    matched = [
        skill for skill in required
        if skill in current_skills
    ]

    missing = [
        skill for skill in required
        if skill not in current_skills
    ]

    score = (
        len(matched) / len(required) * 100
        if required else 0
    )

    gap = 100 - score

    return (
        required,
        matched,
        missing,
        round(score, 1),
        round(gap, 1)
    )


def predict_career(current_skills):
    results = []

    for career, info in career_data.items():
        required = info["skills"]

        matched = [
            skill for skill in required
            if skill in current_skills
        ]

        score = len(matched) / len(required) * 100

        results.append({
            "career": career,
            "score": round(score, 1),
            "matched": len(matched),
            "total": len(required)
        })

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )


def get_career_level(score):
    if score >= 85:
        return "Excellent Match"
    elif score >= 70:
        return "Strong Match"
    elif score >= 50:
        return "Moderate Match"
    return "Needs Development"


def generate_roadmap(missing_skills):
    roadmap = []

    for index, skill in enumerate(missing_skills):
        if index == 0:
            priority = "Priority 1 - Start Now"
        elif index == 1:
            priority = "Priority 2"
        elif index == 2:
            priority = "Priority 3"
        else:
            priority = "Later"

        roadmap.append({
            "skill": skill,
            "priority": priority
        })

    return roadmap


def calculate_readiness(skill_score):
    return round(
        skill_score * 0.50
        + st.session_state.project_progress * 0.20
        + st.session_state.assessment_progress * 0.15
        + st.session_state.interview_progress * 0.15,
        1
    )


def generate_local_advice(
    current_skills,
    missing_skills,
    career,
    skill_score
):
    strengths = ", ".join(current_skills[:5]) if current_skills else "Build your first skills"

    if missing_skills:
        gaps = ", ".join(missing_skills)
    else:
        gaps = "No major skill gaps"

    projects = ", ".join(career_data[career]["projects"][:2])

    return f"""
### 🤖 CareerPilot Local Advisor

**Career suitability:**  
Your current profile shows a **{skill_score}% match** for **{career}**.

**💪 Your strengths:**  
{strengths}

**🔍 Priority skill gaps:**  
{gaps}

**🚀 Recommended projects:**  
{projects}

**📚 What to do next:**
1. Focus on the highest-priority missing skill.
2. Build a small practical project.
3. Add the project to your GitHub portfolio.
4. Take the skill assessment.
5. Practice interview questions with Interview Pilot.

**🎯 Goal:**  
Move your career readiness score above 80% by improving skills,
projects and interview preparation.
"""


def generate_ai_advice():
    current_skills = st.session_state.current_skills
    missing_skills = st.session_state.missing_skills
    skill_score = st.session_state.skill_score

    if not current_skills:
        return "Please select your current skills first."

    if not openai_client:
        return generate_local_advice(
            current_skills,
            missing_skills,
            career_goal,
            skill_score
        )

    prompt = f"""
You are CareerPilot, a professional AI career advisor.

Candidate:
Name: {candidate_name or "Student"}
Education: {education}
Experience: {experience}

Current skills:
{", ".join(current_skills)}

Target career:
{career_goal}

Missing skills:
{", ".join(missing_skills) if missing_skills else "None"}

Skill match score:
{skill_score}%

Give practical advice suitable for a BCA student.

Use these sections:
### Career Suitability
### Your Strengths
### Skill Gaps
### 30-Day Action Plan
### Recommended Projects
### Interview Preparation
### Final Advice

Be realistic, concise and encouraging.
"""

    try:
        response = openai_client.responses.create(
            model="gpt-5.5",
            instructions=(
                "You are an expert career advisor. "
                "Give actionable and realistic career guidance."
            ),
            input=prompt
        )
        return response.output_text
    except Exception:
        return generate_local_advice(
        current_skills,
        missing_skills,
        career_goal,
        skill_score
    )


def ask_ai(question):
    current_skills = st.session_state.current_skills
    missing_skills = st.session_state.missing_skills
    skill_score = st.session_state.skill_score

    context = f"""
Candidate name: {candidate_name or "Student"}
Education: {education}
Experience: {experience}
Current skills: {", ".join(current_skills)}
Target career: {career_goal}
Missing skills: {", ".join(missing_skills)}
Skill match: {skill_score}%
"""

    if not openai_client:
        return (
            "🤖 Local CareerPilot:\n\n"
            f"Based on your profile, focus on {career_goal}. "
            f"Your current match is {skill_score}%. "
            f"Your next priority skills are "
            f"{', '.join(missing_skills[:3]) if missing_skills else 'advanced projects and interview practice'}."
        )

    try:
        response = openai_client.responses.create(
            model="gpt-5.5",
            instructions=(
                "You are CareerPilot, an expert AI career advisor. "
                "Answer the user's question using the supplied candidate profile. "
                "Keep answers practical for a college student."
            ),
            input=context + "\nUser question: " + question
        )

        return response.output_text

    except Exception:
     return (
        "🤖 **CareerPilot Local Advisor**\n\n"
        f"Your target career is **{career_goal}**.\n\n"
        f"Your current skill match is **{skill_score}%**.\n\n"
        f"Your next priority skills are: "
        f"**{', '.join(missing_skills[:3]) if missing_skills else 'advanced projects and interview practice'}**.\n\n"
        "💡 Keep practicing, build projects, and prepare interview questions regularly."
    )


def get_quiz_questions(skill):
    question_bank = {
        "Python": [
            {
                "q": "Which data type is mutable?",
                "options": ["Tuple", "List", "String", "Integer"],
                "answer": "List"
            },
            {
                "q": "Which keyword defines a function?",
                "options": ["func", "define", "def", "function"],
                "answer": "def"
            },
            {
                "q": "Which collection stores key-value pairs?",
                "options": ["List", "Tuple", "Dictionary", "Set"],
                "answer": "Dictionary"
            }
        ],

        "SQL": [
            {
                "q": "Which command retrieves data?",
                "options": ["SELECT", "INSERT", "DELETE", "UPDATE"],
                "answer": "SELECT"
            },
            {
                "q": "Which clause filters rows?",
                "options": ["ORDER BY", "WHERE", "GROUP BY", "JOIN"],
                "answer": "WHERE"
            },
            {
                "q": "Which keyword combines tables?",
                "options": ["MERGE", "JOIN", "UNION ALL ONLY", "CONNECT"],
                "answer": "JOIN"
            }
        ],

        "Machine Learning": [
            {
                "q": "Which is supervised learning?",
                "options": [
                    "Linear Regression",
                    "K-Means",
                    "PCA",
                    "Apriori"
                ],
                "answer": "Linear Regression"
            },
            {
                "q": "Which metric is common for classification?",
                "options": [
                    "Accuracy",
                    "RMSE only",
                    "R2 only",
                    "MAE only"
                ],
                "answer": "Accuracy"
            },
            {
                "q": "Which method helps prevent overfitting?",
                "options": [
                    "Regularization",
                    "Deleting labels",
                    "Removing validation",
                    "Increasing noise"
                ],
                "answer": "Regularization"
            }
        ]
    }

    return question_bank.get(skill, [])


# ============================================================
# TABS
# ============================================================

tabs = st.tabs([
    "🏠 Dashboard",
    "👤 Skill Profile",
    "🔍 Skill Gap",
    "💼 Career Prediction",
    "🗺️ Roadmap",
    "🧪 Skill Test",
    "ℹ️ System"
])

tab_dashboard, tab_profile, tab_gap, tab_career, tab_roadmap, tab_quiz, tab_system = tabs


# ============================================================
# TAB 1 - DASHBOARD
# ============================================================

with tab_dashboard:

    if st.session_state.current_skills:
        readiness = calculate_readiness(
            st.session_state.skill_score
        )
    else:
        readiness = 0

    st.header("📊 Career Intelligence Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">🎯 Skill Match</div>
                <div class="card-value">{st.session_state.skill_score}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">🔍 Skill Gap</div>
                <div class="card-value">{st.session_state.skill_gap}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">📚 Missing Skills</div>
                <div class="card-value">{len(st.session_state.missing_skills)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        career_text = (
            st.session_state.predicted_career
            if st.session_state.predicted_career
            else "Not analyzed"
        )

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">🏆 Best Career</div>
                <div class="card-value" style="font-size:20px;">
                    {career_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    col_left, col_right = st.columns([1, 1])

    with col_left:

        st.subheader("🚀 Overall Job Readiness")

        st.metric(
            "Career Readiness Score",
            f"{readiness}%"
        )

        st.progress(
            int(max(0, min(100, readiness)))
        )

        if readiness >= 85:
            st.success("🏆 Excellent — you are close to job-ready!")
        elif readiness >= 70:
            st.info("🔥 Strong progress — keep improving your gaps.")
        elif readiness >= 50:
            st.warning("📚 Moderate readiness — focus on your roadmap.")
        else:
            st.error("🚀 Start building your skills and projects.")

    with col_right:

        st.subheader("📈 My Progress")

        progress_data = {
            "Technical Skills": st.session_state.skill_score,
            "Learning": st.session_state.learning_progress,
            "Projects": st.session_state.project_progress,
            "Assessments": st.session_state.assessment_progress,
            "Interview": st.session_state.interview_progress
        }

        for label, value in progress_data.items():
            st.write(f"**{label} — {value}%**")
            st.progress(int(value))

    st.divider()

    st.subheader("💼 Top Career Matches")

    if st.session_state.predictions:

        for i, prediction in enumerate(
            st.session_state.predictions[:5]
        ):

            career = prediction["career"]
            score = prediction["score"]

            st.markdown(
                f"""
                <div class="career-card">
                    <b>{i + 1}. {career}</b>
                    <br>
                    <span class="small-note">
                        {prediction["matched"]}/{prediction["total"]} skills matched
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(int(score))

    else:
        st.info(
            "Select your skills and run Career Prediction "
            "to populate this dashboard."
        )

    st.divider()

    st.subheader("🏆 Achievements")

    achievements = []

    if st.session_state.current_skills:
        achievements.append("🏅 Skill Explorer")

    if st.session_state.skill_score >= 50:
        achievements.append("📈 Growing Professional")

    if st.session_state.skill_score >= 70:
        achievements.append("🥈 Strong Skill Profile")

    if st.session_state.skill_score >= 85:
        achievements.append("🥇 Career Ready")

    if st.session_state.assessment_progress >= 80:
        achievements.append("🧪 Assessment Champion")

    if st.session_state.project_progress >= 80:
        achievements.append("💻 Project Builder")

    if st.session_state.interview_progress >= 80:
        achievements.append("🎤 Interview Ready")

    if not achievements:
        achievements.append("🚀 Start your CareerPilot journey")

    for achievement in achievements:
        st.markdown(
            f'<span class="badge">{achievement}</span>',
            unsafe_allow_html=True
        )


# ============================================================
# TAB 2 - PROFILE
# ============================================================

with tab_profile:

    st.header("👤 Candidate Skill Profile")

    st.write(
        f"**Education:** {education}  |  "
        f"**Experience:** {experience}  |  "
        f"**Target:** {career_goal}"
    )

    st.subheader("🧠 Select Your Current Skills")

    current_skills = st.multiselect(
        "Choose the skills you already know:",
        all_skills,
        default=st.session_state.current_skills
    )

    st.session_state.current_skills = current_skills

    if current_skills:
        st.success(
            f"You selected {len(current_skills)} skills."
        )

        cols = st.columns(4)

        for i, skill in enumerate(current_skills):
            with cols[i % 4]:
                st.info(f"✅ {skill}")

        if st.button(
            "🔍 Analyze My Career Profile",
            use_container_width=True
        ):

            (
                required,
                matched,
                missing,
                score,
                gap
            ) = calculate_skill_gap(
                current_skills,
                career_goal
            )

            st.session_state.missing_skills = missing
            st.session_state.skill_score = score
            st.session_state.skill_gap = gap

            predictions = predict_career(current_skills)

            st.session_state.predictions = predictions
            st.session_state.predicted_career = predictions[0]["career"]

            st.success(
                "Profile analyzed successfully! "
                "Open the Dashboard to see your results."
            )

    else:
        st.warning(
            "Please select at least one current skill."
        )


# ============================================================
# TAB 3 - SKILL GAP
# ============================================================

with tab_gap:

    st.header("🔍 AI Skill Gap Analysis")

    if not st.session_state.current_skills:

        st.info(
            "Select your skills in Skill Profile first."
        )

    else:

        (
            required,
            matched,
            missing,
            score,
            gap
        ) = calculate_skill_gap(
            st.session_state.current_skills,
            career_goal
        )

        st.subheader(
            f"🎯 Analysis for {career_goal}"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Required Skills", len(required))

        with c2:
            st.metric("Skills You Have", len(matched))

        with c3:
            st.metric("Missing Skills", len(missing))

        st.divider()

        st.metric(
            "Skill Match Score",
            f"{score}%"
        )

        st.progress(int(score))

        st.write(
            f"**Skill Gap:** {gap}%"
        )

        level = get_career_level(score)

        if score >= 85:
            st.success(f"🌟 {level}")
        elif score >= 70:
            st.info(f"👍 {level}")
        elif score >= 50:
            st.warning(f"⚠️ {level}")
        else:
            st.error(f"❌ {level}")

        st.divider()

        left, right = st.columns(2)

        with left:
            st.subheader("✅ Skills You Have")

            for skill in matched:
                st.write(f"✅ {skill}")

        with right:
            st.subheader("❌ Skills You Need")

            if missing:
                for skill in missing:
                    st.write(f"🔴 {skill}")
            else:
                st.success("You have all required skills!")

        st.session_state.missing_skills = missing
        st.session_state.skill_score = score
        st.session_state.skill_gap = gap


# ============================================================
# TAB 4 - CAREER PREDICTION
# ============================================================

with tab_career:

    st.header("💼 Career Prediction & Recommendation")

    current_skills = st.session_state.current_skills

    if not current_skills:

        st.info(
            "Select your skills first."
        )

    else:

        predictions = predict_career(current_skills)

        st.session_state.predictions = predictions
        st.session_state.predicted_career = predictions[0]["career"]

        st.subheader("🎯 Recommended Career Paths")

        for i, prediction in enumerate(predictions):

            career = prediction["career"]
            score = prediction["score"]

            st.markdown(
                f"""
                <div class="career-card">
                    <h3>{i + 1}. {career}</h3>
                    <p>{career_data[career]["description"]}</p>
                    <p>💰 Entry Level: {career_data[career]["salary"]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(
                f"**Career Match: {score}%**"
            )

            st.progress(int(score))

            st.write(
                f"Matched Skills: "
                f"{prediction['matched']}/"
                f"{prediction['total']}"
            )

        best = predictions[0]

        st.success(
            f"🏆 Recommended Career: "
            f"{best['career']} "
            f"({best['score']}% match)"
        )

        st.subheader("💡 Why this career?")

        matched_best = [
            skill
            for skill in career_data[best["career"]]["skills"]
            if skill in current_skills
        ]

        st.write(
            f"You match {len(matched_best)} of "
            f"{len(career_data[best['career']]['skills'])} "
            f"important skills for this career."
        )

        st.subheader("💻 Suggested Projects")

        for project in career_data[best["career"]]["projects"]:
            st.write(f"🚀 {project}")


# ============================================================
# TAB 5 - ROADMAP
# ============================================================

with tab_roadmap:

    st.header("🗺️ Personalized Learning Roadmap")

    missing_skills = st.session_state.missing_skills

    selected_career = (
        st.session_state.predicted_career
        or career_goal
    )

    if not missing_skills:

        st.success(
            "No major skill gaps found. "
            "Focus on advanced projects and interview preparation."
        )

    else:

        st.subheader(
            f"🚀 Roadmap for {selected_career}"
        )

        roadmap = generate_roadmap(missing_skills)

        for i, item in enumerate(roadmap):

            skill = item["skill"]
            priority = item["priority"]

            st.markdown(
                f"### {i + 1}. {skill}"
            )

            st.info(f"📌 {priority}")

            if skill == "Python":
                st.write(
                    "Learn syntax, functions, OOP, file handling "
                    "and important Python libraries."
                )

            elif skill == "Machine Learning":
                st.write(
                    "Learn supervised learning, unsupervised learning, "
                    "preprocessing, feature engineering and evaluation."
                )

            elif skill == "Deep Learning":
                st.write(
                    "Learn ANN, CNN, activation functions, "
                    "loss functions and backpropagation."
                )

            elif skill == "SQL":
                st.write(
                    "Learn SELECT, JOIN, GROUP BY, subqueries, "
                    "normalization and database design."
                )

            elif skill == "Statistics":
                st.write(
                    "Learn probability, mean, median, variance, "
                    "correlation and distributions."
                )

            elif skill == "Pandas":
                st.write(
                    "Learn DataFrames, cleaning, filtering, grouping "
                    "and data analysis."
                )

            elif skill == "NumPy":
                st.write(
                    "Learn arrays, indexing, vectorized operations "
                    "and numerical computing."
                )

            elif skill == "TensorFlow":
                st.write(
                    "Learn model building, training, evaluation "
                    "and neural network implementation."
                )

            elif skill == "PyTorch":
                st.write(
                    "Learn tensors, neural networks and training loops."
                )

            elif skill == "NLP":
                st.write(
                    "Learn tokenization, preprocessing, embeddings "
                    "and text classification."
                )

            elif skill == "Computer Vision":
                st.write(
                    "Learn image processing, CNNs, OpenCV "
                    "and image classification."
                )

            else:
                st.write(
                    f"Build practical knowledge of {skill} "
                    "through tutorials and projects."
                )

            st.divider()

        st.subheader("📅 Suggested 30-Day Strategy")

        st.write("""
        **Week 1:** Learn the highest-priority missing skill.

        **Week 2:** Practice through small coding exercises.

        **Week 3:** Build a practical mini-project.

        **Week 4:** Upload the project to GitHub and prepare for interviews.
        """)

        st.session_state.learning_progress = st.slider(
            "📚 Update Learning Progress",
            0, 100,
            st.session_state.learning_progress,
            key="roadmap_progress"
        )


# ============================================================
# TAB 6 - AI ADVISOR (temporarily disabled)
# ============================================================
#
# To re-enable: add "🤖 AI Advisor" back to the tabs list above,
# add tab_ai back to the unpacking line, and uncomment this block.
#
# with tab_ai:
#
#     st.header("🤖 AI Career Advisor")
#
#     st.write(
#         "Ask CareerPilot about your career, skills, roadmap and job readiness."
#     )
#
#     current_skills = st.session_state.current_skills
#
#     if not current_skills:
#
#         st.warning(
#             "Please select your current skills first."
#         )
#
#     else:
#
#         st.info(
#             "CareerPilot will use your education, experience, "
#             "skills, target career and skill gaps to generate "
#             "personalized advice."
#         )
#
#         if openai_client:
#             st.success(
#                 "🟢 Real AI mode is active."
#             )
#         else:
#             st.warning(
#                 "🟡 Local advisor mode is active. "
#                 "Set OPENAI_API_KEY to enable real AI."
#             )
#
#         if st.button(
#             "✨ Generate Personalized Career Advice",
#             use_container_width=True
#         ):
#
#             with st.spinner(
#                 "CareerPilot is analyzing your profile..."
#             ):
#
#                 st.session_state.ai_advice = generate_ai_advice()
#
#         if st.session_state.ai_advice:
#
#             st.markdown(
#                 '<div class="advisor-box">',
#                 unsafe_allow_html=True
#             )
#
#             st.markdown(
#                 st.session_state.ai_advice
#             )
#
#             st.markdown(
#                 '</div>',
#                 unsafe_allow_html=True
#             )
#
#         st.divider()
#
#         st.subheader("💬 Ask CareerPilot")
#
#         for message in st.session_state.chat_history:
#
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])
#
#         question = st.chat_input(
#             "Example: What should I learn in the next 30 days?"
#         )
#
#         if question:
#
#             st.session_state.chat_history.append({
#                 "role": "user",
#                 "content": question
#             })
#
#             with st.chat_message("user"):
#                 st.markdown(question)
#
#             answer = ask_ai(question)
#
#             st.session_state.chat_history.append({
#                 "role": "assistant",
#                 "content": answer
#             })
#
#             with st.chat_message("assistant"):
#                 st.markdown(answer)


# ============================================================
# TAB 7 - SKILL TEST
# ============================================================

with tab_quiz:

    st.header("🧪 Skill Assessment")

    st.write(
        "Test your knowledge instead of only claiming a skill."
    )

    quiz_skills = [
        skill for skill in
        ["Python", "SQL", "Machine Learning"]
        if skill in st.session_state.current_skills
    ]

    if not quiz_skills:

        st.info(
            "Select Python, SQL or Machine Learning "
            "to unlock the demo assessment."
        )

    else:

        quiz_skill = st.selectbox(
            "Choose a skill to test:",
            quiz_skills
        )

        questions = get_quiz_questions(quiz_skill)

        if questions:

            with st.form(
                f"quiz_form_{quiz_skill}"
            ):

                answers = []

                for i, item in enumerate(questions):

                    st.write(
                        f"**Q{i + 1}. {item['q']}**"
                    )

                    answer = st.radio(
                        "Choose your answer:",
                        item["options"],
                        key=f"{quiz_skill}_{i}"
                    )

                    answers.append(answer)

                submitted = st.form_submit_button(
                    "🧪 Submit Assessment"
                )

            if submitted:

                correct = sum(
                    answers[i] == questions[i]["answer"]
                    for i in range(len(questions))
                )

                score = round(
                    correct / len(questions) * 100
                )

                st.session_state.quiz_score = score
                st.session_state.assessment_progress = score

                if score >= 80:
                    st.success(
                        f"🏆 Excellent! Your {quiz_skill} score is {score}%."
                    )
                elif score >= 60:
                    st.info(
                        f"👍 Good job! Your {quiz_skill} score is {score}%."
                    )
                else:
                    st.warning(
                        f"📚 Your score is {score}%. "
                        "Review the basics and try again."
                    )


# ============================================================
# TAB 8 - SYSTEM INFORMATION
# ============================================================

with tab_system:

    st.header("ℹ️ System Information")

    st.subheader("⚙️ Candidate Configuration")

    st.write(
        f"**Candidate:** "
        f"{candidate_name if candidate_name else 'Not provided'}"
    )

    st.write(f"**Education:** {education}")
    st.write(f"**Experience:** {experience}")
    st.write(f"**Target Career:** {career_goal}")

    st.divider()

    st.subheader("🧠 Available Careers")

    for career in career_data:
        st.write(f"• {career}")

    st.divider()

    st.subheader("📊 Current Session")

    st.write(
        f"**Skill Match:** "
        f"{st.session_state.skill_score}%"
    )

    st.write(
        f"**Skill Gap:** "
        f"{st.session_state.skill_gap}%"
    )

    st.write(
        f"**Predicted Career:** "
        f"{st.session_state.predicted_career or 'Not analyzed'}"
    )

    if st.session_state.quiz_score is not None:
        st.write(
            f"**Latest Assessment Score:** "
            f"{st.session_state.quiz_score}%"
        )

    st.divider()

    st.subheader("🤖 AI Recommendation Status")

    if openai_client:
        st.success(
            "Real OpenAI Career Advisor is connected."
        )
    else:
        st.info(
            "Local CareerPilot recommendation engine is active."
        )

    st.write("""
    CareerPilot combines candidate profiling, skill-gap analysis,
    career matching, personalized roadmaps, progress tracking,
    skill assessment and an AI career-advisor layer.
    """)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🚀 CareerPilot | AI Career Intelligence Platform"
)

st.caption(
    "Career Discovery • Skill Gap Analysis • AI Advice • "
    "Learning Roadmap • Progress Tracking"
)