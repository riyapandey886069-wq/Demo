import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random
import re
from pypdf import PdfReader

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Interview Pilot - Career Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SESSION STATE
# ============================================================

if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = "Candidate"

if "interview_score" not in st.session_state:
    st.session_state.interview_score = 78

if "technical_score" not in st.session_state:
    st.session_state.technical_score = 82

if "communication_score" not in st.session_state:
    st.session_state.communication_score = 74

if "resume_score" not in st.session_state:
    st.session_state.resume_score = 85

if "questions_completed" not in st.session_state:
    st.session_state.questions_completed = 24

if "streak" not in st.session_state:
    st.session_state.streak = 7

if "career_result" not in st.session_state:
    st.session_state.career_result = None

if "skill_result" not in st.session_state:
    st.session_state.skill_result = None

if "resume_result" not in st.session_state:
    st.session_state.resume_result = None

if "communication_result" not in st.session_state:
    st.session_state.communication_result = None

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "target_role" not in st.session_state:
    st.session_state.target_role = "Python Developer"

if "skills" not in st.session_state:
    st.session_state.skills = ["Python", "SQL"]

if "experience_level" not in st.session_state:
    st.session_state.experience_level = "Fresher"

# ============================================================
# CUSTOM CSS - Teal / Turquoise color system
# ============================================================

st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* =========================================================
       PALETTE
       --teal-deep:   #008080
       --teal-mid:    #40B5A0
       --turquoise:   #00CED1
       --cyan-light:  #E0FFFF
       --seagreen:    #2E8B57
       --cadet:       #5F9EA0
       --lightsea:    #20B2AA
       --azure:       #F0FFFF
       --teal-ink:    #004D4D
       --muted-teal:  #5b8f8c
    ========================================================= */
    :root {
        --teal-deep:   #008080;
        --teal-mid:    #40B5A0;
        --turquoise:   #00CED1;
        --cyan-light:  #E0FFFF;
        --seagreen:    #2E8B57;
        --cadet:       #5F9EA0;
        --lightsea:    #20B2AA;
        --azure:       #F0FFFF;
        --teal-ink:    #004D4D;
        --muted-teal:  #5b8f8c;
        --bg-tint:     #eefffe;
        --border-soft: rgba(0,128,128,0.16);
        --border-strong: rgba(0,128,128,0.28);
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .st-emotion-cache-pgu27n {
        color: black !important;
    }

    .stRadio label p, .stSelectbox label p {
        background: var(--bg-tint) !important;
        border: 1px solid var(--bg-tint) !important;
    }

    .st-emotion-cache-1cv0o6g {
        background: white !important;
    }

    /* =========================================================
       MODERN HERO SECTION
    ========================================================= */
    .hero-modern {
        background: linear-gradient(135deg, var(--teal-deep) 0%, var(--turquoise) 100%);
        padding: 3rem 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0, 128, 128, 0.30);
    }

    .hero-modern::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
    }

    .hero-modern::after {
        content: '';
        position: absolute;
        bottom: -40%;
        left: -10%;
        width: 300px;
        height: 300px;
        background: rgba(46,139,87,0.15);
        border-radius: 50%;
    }

    .hero-title-modern {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }

    .hero-subtitle-modern {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        padding: 0.4rem 1.2rem;
        border-radius: 50px;
        color: white;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 1rem;
        border: 1px solid rgba(255,255,255,0.25);
        position: relative;
        z-index: 1;
    }

    /* =========================================================
       STAT CARDS - Dashboard
    ========================================================= */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid var(--border-soft);
        border-top: 3px solid var(--turquoise);
        box-shadow: 0 2px 10px rgba(0,77,77,0.06);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }

    .stat-card:hover {
        border-color: var(--turquoise);
        box-shadow: 0 10px 26px rgba(0,206,209,0.20);
        transform: translateY(-2px);
    }

    .stat-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--muted-teal);
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--teal-ink);
        margin: 0.3rem 0;
        background: linear-gradient(135deg, var(--teal-deep) 0%, var(--turquoise) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .stat-sub {
        font-size: 0.8rem;
        color: var(--muted-teal);
    }

    /* =========================================================
       MODERN BADGES
    ========================================================= */
    .badge-modern {
        display: inline-block;
        padding: 0.4rem 1rem;
        margin: 0.2rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, rgba(0,206,209,0.14) 0%, rgba(46,139,87,0.10) 100%);
        color: var(--teal-deep);
        border: 1px solid var(--border-strong);
        transition: all 0.3s ease;
        cursor: default;
    }

    .badge-modern:hover {
        background: linear-gradient(135deg, var(--teal-deep) 0%, var(--turquoise) 100%);
        color: white;
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(0,206,209,0.25);
    }

    .badge-success {
        background: linear-gradient(135deg, #10b98115 0%, #05966915 100%);
        color: #059669;
        border-color: rgba(16, 185, 129, 0.20);
    }

    .badge-warning {
        background: linear-gradient(135deg, #f59e0b15 0%, #d9770615 100%);
        color: #d97706;
        border-color: rgba(245, 158, 11, 0.20);
    }

    .badge-danger {
        background: linear-gradient(135deg, #ef444415 0%, #dc262615 100%);
        color: #dc2626;
        border-color: rgba(239, 68, 68, 0.20);
    }

    /* =========================================================
       MODERN PROGRESS BAR
    ========================================================= */
    .progress-label-modern {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--teal-ink);
        margin: 0.3rem 0;
    }

    .progress-modern {
        width: 100%;
        height: 8px;
        background: rgba(0,128,128,0.10);
        border-radius: 50px;
        overflow: hidden;
        margin: 0.5rem 0;
        border: 1px solid var(--border-soft);
    }

    .progress-modern-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--teal-deep) 0%, var(--turquoise) 50%, var(--lightsea) 100%);
        border-radius: 50px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }

    .progress-modern-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.35), transparent);
        animation: shimmer 2s infinite;
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    /* =========================================================
       SECTION BOXES
    ========================================================= */
    .section-box {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid var(--border-soft);
        box-shadow: 0 2px 10px rgba(0,77,77,0.06);
        margin-top: 1rem;
        transition: all 0.3s ease;
    }

    .section-box:hover {
        border-color: var(--turquoise);
        box-shadow: 0 10px 26px rgba(0,206,209,0.14);
    }

    .section-box h4 {
        color: var(--teal-ink);
        font-weight: 700;
        margin-bottom: 1rem;
        border-left: 4px solid var(--turquoise);
        padding-left: 0.6rem;
    }

    /* =========================================================
       AI RESPONSE BOX
    ========================================================= */
    .ai-box {
        background: linear-gradient(135deg, var(--bg-tint) 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid var(--border-strong);
        box-shadow: 0 8px 30px rgba(0,128,128,0.10);
        margin-top: 1rem;
        transition: all 0.3s ease;
    }

    .ai-box:hover {
        border-color: var(--turquoise);
        box-shadow: 0 12px 38px rgba(0,206,209,0.20);
    }

    /* =========================================================
       BUTTONS
    ========================================================= */
    .stButton > button {
        background: linear-gradient(135deg, var(--teal-deep) 0%, var(--turquoise) 100%);
        color: white;
        font-weight: 700;
        border: none;
        padding: 0.7rem 2rem;
        border-radius: 12px;
        transition: all 0.3s ease;
        width: 100%;
        font-size: 0.95rem;
        box-shadow: 0 4px 16px rgba(0,128,128,0.30);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(0,206,209,0.40);
    }

    .stButton > button:active {
        transform: scale(0.98);
    }

    /* =========================================================
       SIDEBAR
    ========================================================= */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-tint) 0%, #ffffff 100%);
        border-right: 1px solid var(--border-soft);
        padding: 2rem 1rem;
        box-shadow: 6px 0 24px rgba(0,77,77,0.05);
    }

    /* =========================================================
       INPUTS
    ========================================================= */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 12px !important;
        border: 2px solid rgba(0,128,128,0.20) !important;
        padding: 0.7rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        background: white !important;
        color: var(--teal-ink) !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--turquoise) !important;
        box-shadow: 0 0 0 4px rgba(0,206,209,0.16) !important;
    }

    /* =========================================================
       METRICS
    ========================================================= */
    [data-testid="stMetric"] {
        background: white;
        padding: 1.2rem;
        border-radius: 16px;
        border: 1px solid var(--border-soft);
        border-top: 3px solid var(--turquoise);
        box-shadow: 0 2px 10px rgba(0,77,77,0.06);
    }

    [data-testid="stMetricValue"] {
        font-weight: 800 !important;
        color: var(--teal-ink) !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted-teal) !important;
        font-weight: 600 !important;
    }

    /* =========================================================
       NAVIGATION TABS
    ========================================================= */
    .stRadio > div {
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .stRadio label {
        background: white;
        padding: 0.5rem 1.2rem;
        border-radius: 50px;
        border: 2px solid rgba(0,128,128,0.20);
        transition: all 0.3s ease;
        font-weight: 600;
        font-size: 0.85rem;
        color: var(--teal-ink);
    }

    .stRadio label:hover {
        border-color: var(--turquoise);
        background: var(--bg-tint);
    }

    .stRadio [aria-checked="true"] {
        background: linear-gradient(135deg, var(--teal-deep) 0%, var(--turquoise) 100%) !important;
        color: white !important;
        border-color: var(--teal-deep) !important;
        box-shadow: 0 4px 16px rgba(0,128,128,0.30);
    }

    /* =========================================================
       EXPANDERS
    ========================================================= */
    .streamlit-expanderHeader {
        background: white !important;
        border: 1px solid var(--border-soft) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        color: var(--teal-ink) !important;
        padding: 0.8rem 1.2rem !important;
    }

    .streamlit-expanderHeader:hover {
        border-color: var(--turquoise) !important;
    }

    /* =========================================================
       ALERTS
    ========================================================= */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }

    .stAlert > div {
        padding: 0.8rem 1.2rem !important;
    }

    /* =========================================================
       DATAFRAME
    ========================================================= */
    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid var(--border-soft);
        box-shadow: 0 2px 10px rgba(0,77,77,0.06);
    }

    /* =========================================================
       FILE UPLOADER
    ========================================================= */
    [data-testid="stFileUploader"] {
        background: var(--bg-tint);
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
        border-top: 2px solid var(--border-soft);
        margin: 2rem 0;
    }

    /* =========================================================
       FOOTER
    ========================================================= */
    .footer-modern {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: var(--muted-teal);
        font-size: 0.85rem;
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

    /* =========================================================
       RESPONSIVE
    ========================================================= */
    @media (max-width: 768px) {
        .hero-title-modern {
            font-size: 2.5rem;
        }
        .hero-subtitle-modern {
            font-size: 1rem;
        }
        .stat-value {
            font-size: 2rem;
        }
        .stRadio label {
            font-size: 0.75rem;
            padding: 0.3rem 0.8rem;
        }
        .hero-modern {
            padding: 2rem 1rem;
        }
    }


    .st-emotion-cache-7l0mdr{
    overflow:visible !Important;

    }

.st-emotion-cache-1nd20cx{
border:2px solid rgba(0,128,128,0.20) !important;
}
 .st-emotion-cache-1kzydod {
border:2px solid rgba(0,128,128,0.20) !important;
}   
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOCAL CAREER DATABASE
# ============================================================

CAREER_DB = {
    "Python Developer": {
        "skills": ["Python", "OOP", "SQL", "Git/GitHub", "Data Science"],
        "salary_note": "Entry-level Python Developer roles in India typically pay ₹3-6 LPA, rising quickly with backend and API experience.",
        "projects": ["Student Management System", "REST API Backend", "Task Automation Toolkit"],
        "description": "Python Developers build applications, APIs, and automation tools using Python."
    },
    "Data Scientist": {
        "skills": ["Python", "Machine Learning", "SQL", "Data Science", "Excel"],
        "salary_note": "Data Scientist roles typically start around ₹5-9 LPA.",
        "projects": ["House Price Prediction", "Customer Churn Analysis", "Student Performance Predictor"],
        "description": "Data Scientists analyze complex data to find patterns and build predictive models."
    },
    "Data Analyst": {
        "skills": ["Python", "SQL", "Excel", "Power BI", "Data Science"],
        "salary_note": "Data Analyst roles typically pay ₹3-7 LPA.",
        "projects": ["Sales Dashboard", "Student Analytics Dashboard", "Business KPI Report"],
        "description": "Data Analysts collect, process, and analyze data to help organizations make decisions."
    },
    "Machine Learning Engineer": {
        "skills": ["Python", "Machine Learning", "Deep Learning", "SQL", "Data Science"],
        "salary_note": "ML Engineer roles usually start ₹5-10 LPA.",
        "projects": ["ML Prediction API", "Recommendation Engine", "Image Classification System"],
        "description": "Machine Learning Engineers build, train, and deploy ML models into production."
    },
    "AI Engineer": {
        "skills": ["Python", "Machine Learning", "Deep Learning", "NLP", "Git/GitHub"],
        "salary_note": "AI Engineer roles typically pay ₹6-12 LPA.",
        "projects": ["AI Career Advisor Bot", "NLP Chatbot", "Computer Vision Classifier"],
        "description": "AI Engineers build intelligent systems that can reason, learn, and make decisions."
    },
    "Web Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "React", "Git/GitHub"],
        "salary_note": "Web Developer roles typically start ₹3-7 LPA.",
        "projects": ["Portfolio Website", "E-commerce Storefront", "Full-Stack Portal"],
        "description": "Web Developers build websites and web applications using modern frameworks."
    },
    "Software Developer": {
        "skills": ["Python", "Java", "C++", "SQL", "Git/GitHub"],
        "salary_note": "Software Developer roles typically pay ₹4-8 LPA.",
        "projects": ["Banking Application", "Library Management System", "Desktop App"],
        "description": "Software Developers design, build, and maintain software applications."
    },
    "Business Analyst": {
        "skills": ["Excel", "SQL", "Power BI", "Data Science", "Python"],
        "salary_note": "Business Analyst roles typically pay ₹4-8 LPA.",
        "projects": ["Business KPI Report", "Market Trend Analysis", "Stakeholder Dashboard"],
        "description": "Business Analysts bridge business needs with technology solutions."
    }
}

FILLER_WORDS = ["um", "uh", "like", "you know", "actually", "basically", "literally", "kind of", "sort of"]

QUESTION_BANK = {
    "Technical": {
        "Easy": [
            "Can you explain what {skill} is used for and where you've applied it?",
            "Walk me through how you would set up a simple project using {skill}.",
            "What data structure would you use to solve a basic search problem?"
        ],
        "Medium": [
            "How would you optimize a slow-running part of a project that uses {skill}?",
            "Describe a bug you fixed recently. How did you find the root cause?",
            "How would you design a simple API for a {role} use case?"
        ],
        "Hard": [
            "How would you scale a {skill}-based system to handle 10x the current load?",
            "Walk me through how you'd design an end-to-end data pipeline for a {role} project.",
            "How would you debug a system that fails intermittently in production?"
        ]
    },
    "HR": {
        "Easy": [
            "Tell me about yourself and why you're interested in a {role} role.",
            "What are your biggest strengths and weaknesses?",
            "Why do you want to work at our company?"
        ],
        "Medium": [
            "Where do you see yourself in 3 years as a {role}?",
            "How do you handle tight deadlines or pressure at work?",
            "What motivates you in your career?"
        ],
        "Hard": [
            "Tell me about a time you disagreed with a manager. How did you handle it?",
            "Why should we hire you over other candidates for this {role} position?",
            "Describe a professional failure and what you learned from it."
        ]
    },
    "Behavioral": {
        "Easy": [
            "Describe a time you worked in a team to complete a project.",
            "Tell me about a time you had to learn something new quickly.",
            "How do you prioritize tasks when you have multiple deadlines?"
        ],
        "Medium": [
            "Tell me about a time you made a mistake in a project. What did you do?",
            "Describe a situation where you had to convince someone of your idea.",
            "How do you handle receiving critical feedback?"
        ],
        "Hard": [
            "Tell me about the most challenging project you've worked on.",
            "Describe a time you had to make a decision with incomplete information.",
            "Tell me about a time you led others through a difficult situation."
        ]
    }
}

QUESTION_BANK["Mixed"] = {
    diff: QUESTION_BANK["Technical"][diff] + QUESTION_BANK["HR"][diff] + QUESTION_BANK["Behavioral"][diff]
    for diff in ["Easy", "Medium", "Hard"]
}

# ============================================================
# LOCAL RESPONSE ENGINE
# ============================================================

def match_skills(current_skills, required_skills):
    current_lower = {s.lower() for s in current_skills}
    matched = [s for s in required_skills if s.lower() in current_lower]
    missing = [s for s in required_skills if s.lower() not in current_lower]
    score = round(len(matched) / len(required_skills) * 100) if required_skills else 0
    return matched, missing, score

def build_roadmap(missing_skills):
    if not missing_skills:
        return [
            "You already cover the core skill set for this role — focus on advanced, portfolio-grade projects.",
            "Contribute to an open-source repository to show real-world collaboration.",
            "Prepare 3-4 strong project stories for interviews using the STAR method.",
            "Start scheduling mock interviews to sharpen your delivery."
        ]
    steps = [f"Spend the first 1-2 weeks on {missing_skills[0]} — complete a beginner course and write 3 small practice scripts."]
    if len(missing_skills) > 1:
        steps.append(f"Next, build a small hands-on exercise using {missing_skills[1]} to move it from theory to practice.")
    if len(missing_skills) > 2:
        steps.append(f"Once comfortable, combine {missing_skills[0]} and {missing_skills[2]} in one mini-project.")
    steps.append("Package everything into one portfolio project and publish it on GitHub with a clear README.")
    steps.append("Add the project to your resume and rehearse explaining it out loud.")
    return steps

def generate_reason(score, name, role, matched_count, total_count):
    if score >= 85:
        options = [
            f"{name}, your profile is an excellent fit for {role} — you already cover {matched_count}/{total_count} of the core skills.",
            f"This is a strong match. With {matched_count}/{total_count} key skills already in place, {role} is well within reach."
        ]
    elif score >= 65:
        options = [
            f"{name}, you're on solid ground for {role}, matching {matched_count}/{total_count} core skills.",
            f"Good alignment here: {matched_count}/{total_count} required skills are already covered for {role}."
        ]
    elif score >= 40:
        options = [
            f"{name}, {role} is a realistic goal — you currently match {matched_count}/{total_count} skills.",
            f"You're building the right foundation for {role} with {matched_count}/{total_count} skills covered."
        ]
    else:
        options = [
            f"{name}, {role} is achievable but will need consistent effort — right now {matched_count}/{total_count} core skills are in place.",
            f"There's real potential here for {role}. With {matched_count}/{total_count} skills matched today."
        ]
    idx = (matched_count + total_count + len(name)) % len(options)
    return options[idx]

def generate_next_action(missing_skills, role):
    if missing_skills:
        return f"This week, start learning {missing_skills[0]} and pair it with a 2-hour daily practice block."
    return f"You're ready — start applying to {role} roles and schedule 2 mock interviews this week."

def local_career_advice(candidate_name, skills_list, dream_job):
    role = dream_job if dream_job in CAREER_DB else None
    if not role:
        for key in CAREER_DB:
            if key.lower() in dream_job.lower() or dream_job.lower() in key.lower():
                role = key
                break
    if not role:
        best_role, best_score = None, -1
        for key, info in CAREER_DB.items():
            _, _, s = match_skills(skills_list, info["skills"])
            if s > best_score:
                best_role, best_score = key, s
        role = best_role
    if not role:
        role = "Python Developer"

    required = CAREER_DB[role]["skills"]
    matched, missing, score = match_skills(skills_list, required)

    return {
        "recommended_role": role,
        "match_score": score,
        "reason": generate_reason(score, candidate_name, role, len(matched), len(required)),
        "top_skills": matched if matched else skills_list[:3] if skills_list else ["Python"],
        "skill_gaps": missing,
        "roadmap": build_roadmap(missing),
        "salary_note": CAREER_DB[role]["salary_note"],
        "next_action": generate_next_action(missing, role),
        "role_description": CAREER_DB[role].get("description", ""),
        "project_suggestions": CAREER_DB[role].get("projects", [])
    }

def local_skill_gap(target, skill_input):
    current = [s.strip() for s in re.split(r"[,\n]", skill_input) if s.strip()]
    current_lower = {s.lower() for s in current}
    required = CAREER_DB.get(target, {}).get("skills", [])
    if not required:
        required = ["Python", "SQL", "Communication"]

    rows = []
    for skill in required:
        has = skill.lower() in current_lower
        current_val = 85 if has else 25
        gap = 100 - current_val
        priority = "High" if gap >= 60 else "Medium" if gap >= 30 else "Low"
        rows.append({
            "skill": skill,
            "current": current_val,
            "required": 100,
            "gap": gap,
            "priority": priority,
            "status": "✅ Covered" if has else "❌ Needs Work"
        })

    overall = round(sum(r["current"] for r in rows) / len(rows)) if rows else 0
    top_gaps = [r["skill"] for r in sorted(rows, key=lambda r: -r["gap"])[:3] if r["gap"] > 0]

    recommendations = [f"Spend a focused week on {skill} — one small daily exercise plus one applied mini-task." for skill in top_gaps]
    if not recommendations:
        recommendations = [
            "You're covering the full skill set — deepen expertise with an advanced project.",
            "Consider a certification to formally validate your existing skills.",
            "Start contributing to open-source projects in this domain."
        ]

    return {
        "overall_score": overall,
        "skills": rows,
        "top_gaps": top_gaps,
        "recommendations": recommendations
    }

def local_resume_analysis(resume_text, target_role):
    text_lower = resume_text.lower()
    word_count = len(resume_text.split())
    section_keywords = ["education", "experience", "project", "skill", "certificat", "internship", "summary"]
    sections_found = [k for k in section_keywords if k in text_lower]
    has_email = bool(re.search(r"[\w\.-]+@[\w\.-]+\.\w+", resume_text))
    has_phone = bool(re.search(r"\b\d{10}\b", resume_text))
    required_skills = CAREER_DB.get(target_role, {}).get("skills", ["Python", "SQL"])
    present_keywords = [s for s in required_skills if s.lower() in text_lower]
    missing_keywords = [s for s in required_skills if s not in present_keywords]
    keyword_coverage = len(present_keywords) / len(required_skills) if required_skills else 0

    score = 20
    score += min(len(sections_found), 6) * 6
    score += 10 if has_email else 0
    score += 5 if has_phone else 0
    score += round(keyword_coverage * 30)
    score += 10 if 200 <= word_count <= 900 else 0
    score = max(0, min(100, score))

    strengths = []
    if has_email:
        strengths.append("✓ Contact email is present")
    if has_phone:
        strengths.append("✓ Phone number is included")
    if "project" in sections_found:
        strengths.append("✓ Projects section included")
    if "experience" in sections_found or "internship" in sections_found:
        strengths.append("✓ Experience/Internship details present")
    if present_keywords:
        strengths.append(f"✓ Good keyword coverage: {', '.join(present_keywords[:4])}")
    if not strengths:
        strengths = ["✓ Resume has a clear starting structure"]

    weaknesses = []
    if not has_email:
        weaknesses.append("✗ No email address detected")
    if not has_phone:
        weaknesses.append("✗ No phone number detected")
    if "project" not in sections_found:
        weaknesses.append("✗ No dedicated projects section")
    if "skill" not in sections_found:
        weaknesses.append("✗ No clearly labeled skills section")
    if word_count < 200:
        weaknesses.append("✗ Resume is quite short")
    if word_count > 1000:
        weaknesses.append("✗ Resume is lengthy")
    if not weaknesses:
        weaknesses = ["No major structural issues found"]

    improvements = [
        "💡 Quantify achievements with numbers where possible",
        "💡 Lead each bullet point with a strong action verb",
        f"💡 Weave in missing keywords: {', '.join(missing_keywords[:4])}" if missing_keywords else "💡 Keep refreshing your project section",
        "💡 Keep formatting consistent throughout"
    ]

    if score >= 80:
        ats_advice = "✅ Your resume is in strong shape for ATS scanners"
    elif score >= 60:
        ats_advice = "⚠️ Reasonably ATS-friendly - add more role-specific keywords"
    else:
        ats_advice = "⚠️ Add a clearly labeled Skills section and role-specific keywords"

    summary = f"This resume covers {len(sections_found)} of {len(section_keywords)} expected sections and matches {len(present_keywords)}/{len(required_skills)} core {target_role} keywords."

    return {
        "score": score,
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "missing_keywords": missing_keywords,
        "improvements": improvements,
        "ats_advice": ats_advice
    }

def generate_interview_question(role, skills, difficulty, interview_type, question_number):
    pool = QUESTION_BANK.get(interview_type, QUESTION_BANK["Mixed"]).get(difficulty, [])
    if not pool:
        pool = ["Tell me about a project you're proud of and your role in it."]
    skill_choice = skills[question_number % len(skills)] if skills else "Python"
    idx = (question_number - 1) % len(pool)
    template = pool[idx]
    return template.format(skill=skill_choice, role=role)

def count_fillers(text):
    text_lower = text.lower()
    return sum(text_lower.count(f) for f in FILLER_WORDS)

def local_evaluate_answer(question, answer, role):
    words = answer.split()
    word_count = len(words)
    filler_count = count_fillers(answer)
    sentences = [s for s in re.split(r"[.!?]+", answer) if s.strip()]
    sentence_count = len(sentences)
    question_keywords = {w.lower().strip("?,.") for w in question.split() if len(w) > 4}
    answer_words = {w.lower().strip("?,.") for w in answer.split()}
    overlap = len(question_keywords & answer_words)
    relevance = min(100, 40 + overlap * 15)
    technical_accuracy = min(100, max(10, 30 + word_count * 1.1 - filler_count * 5))
    communication = max(10, 100 - filler_count * 10 - (0 if sentence_count >= 2 else 20))
    confidence = max(10, 100 - filler_count * 8 - (30 if word_count < 15 else 0))
    overall = round((technical_accuracy + communication + confidence + relevance) / 4)

    if overall >= 80:
        strength = "Excellent! Clear, confident and directly relevant."
        improvement = "Add one concrete metric or outcome to make it even more memorable."
    elif overall >= 60:
        strength = "Good! Solid structure and relevant content."
        improvement = f"Trim filler words ({filler_count} detected) and lead with your strongest point first."
    elif overall >= 40:
        strength = "You're touching the right topic, and the core idea is there."
        improvement = "Add more specific detail and a concrete example."
    else:
        strength = "You've made a start — the foundation is there to build on."
        improvement = "Expand the answer with a specific example, structured as situation, action, result."

    ideal_answer = f"A strong answer to \"{question}\" would briefly set context, describe the specific action you took (tying it to relevant {role} skills), and close with a measurable result."

    return {
        "technical_accuracy": round(technical_accuracy),
        "communication": round(communication),
        "confidence": round(confidence),
        "relevance": round(relevance),
        "overall_score": overall,
        "strength": strength,
        "improvement": improvement,
        "ideal_answer": ideal_answer
    }

def local_communication_analysis(question, answer):
    words = answer.split()
    word_count = len(words)
    filler_count = count_fillers(answer)
    sentences = [s for s in re.split(r"[.!?]+", answer) if s.strip()]
    sentence_count = max(1, len(sentences))
    avg_sentence_len = word_count / sentence_count

    clarity = max(10, 100 - filler_count * 8 - (20 if avg_sentence_len > 30 else 0))
    confidence = max(10, 100 - filler_count * 7 - (25 if word_count < 15 else 0))
    structure = 80 if sentence_count >= 3 else 55 if sentence_count == 2 else 35
    professionalism = max(20, 100 - filler_count * 6 - (15 if answer.isupper() else 0))
    conciseness = 90 if 40 <= word_count <= 150 else 65 if word_count < 40 else 50
    overall = round((clarity + confidence + structure + professionalism + conciseness) / 5)

    strengths = []
    if filler_count <= 1:
        strengths.append("✅ Very few filler words")
    if sentence_count >= 3:
        strengths.append("✅ Good structure with multiple developed points")
    if 40 <= word_count <= 150:
        strengths.append("✅ Length is well-balanced")
    if not strengths:
        strengths = ["✅ You've got the core idea across clearly"]

    improvements = []
    if filler_count > 1:
        improvements.append(f"💡 Cut filler words like 'um', 'like' — {filler_count} detected")
    if sentence_count < 2:
        improvements.append("💡 Break your answer into 2-3 clear points")
    if word_count < 40:
        improvements.append("💡 Expand with a specific example")
    if word_count > 150:
        improvements.append("💡 Tighten the answer — aim for 60-120 words")
    if not improvements:
        improvements = ["💡 Keep practicing at this pace — it's already interview-ready"]

    cleaned = answer
    for f in FILLER_WORDS:
        cleaned = re.sub(rf"\b{re.escape(f)}\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if cleaned and not cleaned[0].isupper():
        cleaned = cleaned[0].upper() + cleaned[1:]
    if cleaned and cleaned[-1] not in ".!?":
        cleaned += "."
    better_version = cleaned if cleaned else answer

    return {
        "clarity": round(clarity),
        "confidence": round(confidence),
        "structure": round(structure),
        "professionalism": round(professionalism),
        "conciseness": round(conciseness),
        "overall_score": overall,
        "filler_word_count": filler_count,
        "strengths": strengths,
        "improvements": improvements,
        "better_version": better_version
    }

def extract_resume_text(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"Could not read resume: {e}")
        return ""

def show_progress(label, value):
    value = max(0, min(100, int(value)))
    st.markdown(f"""
        <div class="progress-label-modern">
            <span>{label}</span>
            <span>{value}%</span>
        </div>
        <div class="progress-modern">
            <div class="progress-modern-fill" style="width:{value}%;"></div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
        <div style="text-align:center; margin-bottom:1.5rem;font-size:1.5rem;">
           🎯  <span style=" font-weight:800; background:linear-gradient(135deg, var(--teal-deep) 0%, var(--turquoise) 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
                Interview Pilot
            </span>
            <div style="color:var(--muted-teal); font-size:0.85rem;">Career & Interview Coach</div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    candidate_name = st.text_input("👤 Candidate Name", value=st.session_state.candidate_name)
    st.session_state.candidate_name = candidate_name if candidate_name else "Candidate"

    st.session_state.experience_level = st.selectbox(
        "💼 Experience Level",
        ["Fresher", "Student", "0-2 Years", "2-5 Years", "5+ Years"],
        index=0
    )

    st.session_state.target_role = st.selectbox(
        "🎯 Target Career",
        list(CAREER_DB.keys()),
        index=0
    )

    st.session_state.skills = st.multiselect(
        "🧠 Your Skills",
        ["Python", "Java", "C++", "SQL", "HTML", "CSS", "JavaScript", "React",
         "Machine Learning", "Deep Learning", "NLP", "Data Science", "Power BI",
         "Excel", "Git/GitHub", "Django", "Flask", "Docker", "AWS"],
        default=["Python", "SQL"]
    )

    st.divider()

    st.markdown(f"""
        <div style="background:white; padding:1.2rem; border-radius:16px; border:1px solid var(--border-soft); border-top:3px solid var(--turquoise); text-align:center;">
            <div style="font-size:0.7rem; color:var(--muted-teal); text-transform:uppercase; letter-spacing:0.5px;">Practice Streak</div>
            <div style="font-size:2.5rem; font-weight:800; color:var(--teal-ink);">🔥 {st.session_state.streak}</div>
            <div style="font-size:0.8rem; color:var(--muted-teal);">Days of continuous practice</div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.caption("🚀 v3.0 • Fully Self-Contained")

# ============================================================
# MAIN CONTENT - Hero Section
# ============================================================

st.markdown("""
    <div class="hero-modern">
        <div class="hero-title-modern">🎯 Interview Pilot</div>
        <div class="hero-subtitle-modern">AI-Powered Career & Interview Readiness Platform</div>
        <div class="hero-badge">⚡ Concept By Riya Pandey</div>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# NAVIGATION
# ============================================================

page = st.radio(
    "Navigation",
    ["🏠 Dashboard", "🤖 Career Advisor", "🧠 Skill Gap", "📄 Resume", "🎤 Interview", "🗣️ Communication", "🏆 Progress"],
    horizontal=True,
    label_visibility="collapsed"
)

# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":
    st.markdown(f"""
        <div style="margin-bottom:1.5rem;">
            <h2 style="color:var(--teal-ink); font-weight:700;">👋 Welcome back, {st.session_state.candidate_name}!</h2>
            <p style="color:var(--muted-teal);">Let's make you interview-ready for <strong style="color:var(--teal-deep);">{st.session_state.target_role}</strong> 🚀</p>
        </div>
    """, unsafe_allow_html=True)

    readiness = int((st.session_state.interview_score + st.session_state.technical_score +
                     st.session_state.communication_score + st.session_state.resume_score) / 4)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Overall Readiness</div>
                <div class="stat-value">{readiness}%</div>
                <div class="stat-sub">Preparation level</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Technical Skills</div>
                <div class="stat-value">{st.session_state.technical_score}%</div>
                <div class="stat-sub">Core competencies</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Communication</div>
                <div class="stat-value">{st.session_state.communication_score}%</div>
                <div class="stat-sub">Interview delivery</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Resume Score</div>
                <div class="stat-value">{st.session_state.resume_score}/100</div>
                <div class="stat-sub">ATS readiness</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        st.markdown("""
            <div class="section-box">
                <h4>📊 Skills Profile</h4>
        """, unsafe_allow_html=True)

        categories = ["Technical", "Communication", "Resume", "Interview"]
        values = [
            st.session_state.technical_score,
            st.session_state.communication_score,
            st.session_state.resume_score,
            st.session_state.interview_score
        ]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name="Your Score",
            line_color="#008080",
            fillcolor="rgba(0, 206, 209, 0.18)"
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color="#5b8f8c", gridcolor="rgba(0,128,128,0.16)"),
                angularaxis=dict(color="#004D4D", gridcolor="rgba(0,128,128,0.16)")
            ),
            showlegend=False,
            height=320,
            margin=dict(l=40, r=40, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("""
            <div class="section-box">
                <h4>🎯 Career Match</h4>
        """, unsafe_allow_html=True)

        _, _, base_match = match_skills(
            st.session_state.skills,
            CAREER_DB.get(st.session_state.target_role, {}).get("skills", [])
        )
        match_score = min(98, max(45, base_match + random.randint(-3, 8)))

        st.markdown(f"""
            <div style="text-align:center; padding:0.5rem;">
                <div style="font-size:4rem; font-weight:800; background:linear-gradient(135deg, var(--teal-deep) 0%, var(--turquoise) 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
                    {match_score}%
                </div>
                <div style="font-size:1.1rem; font-weight:600; color:var(--teal-ink);">{st.session_state.target_role}</div>
                <div style="color:var(--muted-teal); font-size:0.85rem;">Career compatibility</div>
            </div>
        """, unsafe_allow_html=True)

        show_progress("Match Score", match_score)
        st.info("💡 Complete the Career Advisor for detailed insights.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("🚀 Quick Actions")
    q_cols = st.columns(4)
    actions = [
        ("🤖", "Career Advisor", "Get personalized guidance"),
        ("🧠", "Skill Gap", "Analyze your skills"),
        ("📄", "Resume", "Upload & analyze"),
        ("🎤", "Interview", "Practice now")
    ]
    for col, (icon, title, desc) in zip(q_cols, actions):
        with col:
            st.markdown(f"""
                <div style="background:white; padding:1rem; border-radius:12px; border:1px solid var(--border-soft); border-top:3px solid var(--turquoise); text-align:center; transition:all 0.3s ease;">
                    <div style="font-size:2rem;">{icon}</div>
                    <div style="font-weight:700; color:var(--teal-ink);">{title}</div>
                    <div style="font-size:0.8rem; color:var(--muted-teal);">{desc}</div>
                </div>
            """, unsafe_allow_html=True)

# ============================================================
# CAREER ADVISOR
# ============================================================

elif page == "🤖 Career Advisor":
    st.markdown("""
        <h2 style="color:var(--teal-ink); font-weight:700;">🤖 Career Advisor</h2>
        <p style="color:var(--muted-teal);">Get personalized career recommendations based on your skills and interests.</p>
    """, unsafe_allow_html=True)

    with st.expander("📝 Tell us about yourself", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            education = st.text_input("🎓 Education", "BCA / Computer Applications")
            interests = st.text_area("❤️ Career Interests", "Artificial Intelligence, Python, Data Science", height=80)
        with col2:
            experience_text = st.text_area("💼 Experience / Projects", "I have worked on Python, Machine Learning and Streamlit projects.", height=80)
            dream_job = st.text_input("🎯 Dream Job", st.session_state.target_role)

    if st.button("🚀 Generate Career Plan", use_container_width=True):
        with st.spinner("Generating your personalized career plan..."):
            data = local_career_advice(
                st.session_state.candidate_name,
                st.session_state.skills,
                dream_job
            )
            st.session_state.career_result = data

    if st.session_state.career_result:
        data = st.session_state.career_result

        st.markdown("""
            <div class="ai-box">
        """, unsafe_allow_html=True)

        st.subheader(f"🎯 Recommended Career: {data.get('recommended_role', 'Career')}")

        score = data.get("match_score", 0)
        st.metric("Career Match Score", f"{score}%")
        st.write(data.get("reason", ""))

        st.markdown("### 💪 Your Strongest Skills")
        skill_html = "".join([f'<span class="badge-modern">{s}</span>' for s in data.get("top_skills", [])])
        st.markdown(skill_html, unsafe_allow_html=True)

        if data.get("skill_gaps"):
            st.markdown("### 🚨 Skill Gaps to Address")
            for gap in data.get("skill_gaps", []):
                st.warning(f"⚠️ {gap}")
        else:
            st.success("🎉 No major skill gaps for this role!")

        with st.expander("🗺️ View Career Roadmap"):
            for i, step in enumerate(data.get("roadmap", []), 1):
                st.markdown(f"**{i}.** {step}")

        st.markdown("### 💰 Salary Note")
        st.info(data.get("salary_note", ""))

        st.markdown("### 🚀 Recommended Next Action")
        st.success(data.get("next_action", ""))

        st.markdown("### 📝 Role Description")
        st.write(data.get("role_description", ""))

        st.markdown("### 🛠️ Project Suggestions")
        for project in data.get("project_suggestions", []):
            st.markdown(f"• {project}")

        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# SKILL GAP
# ============================================================

elif page == "🧠 Skill Gap":
    st.markdown("""
        <h2 style="color:var(--teal-ink); font-weight:700;">🧠 Skill Gap Analyzer</h2>
        <p style="color:var(--muted-teal);">Compare your current skills with the requirements for your target career.</p>
    """, unsafe_allow_html=True)

    target = st.selectbox("🎯 Select Target Job", list(CAREER_DB.keys()), index=0)
    skill_input = st.text_area("🧠 Enter Your Current Skills (comma separated)", ", ".join(st.session_state.skills), height=80)

    if st.button("🔍 Analyze Skill Gap", use_container_width=True):
        with st.spinner("Analyzing skill gaps..."):
            data = local_skill_gap(target, skill_input)
            st.session_state.skill_result = data

    if st.session_state.skill_result:
        data = st.session_state.skill_result

        st.markdown(f"""
            <div class="section-box">
                <h4>🎯 Overall Skill Readiness: {data.get('overall_score', 0)}%</h4>
        """, unsafe_allow_html=True)
        show_progress("Overall Readiness", data.get("overall_score", 0))
        st.markdown("</div>", unsafe_allow_html=True)

        skills_data = data.get("skills", [])
        if skills_data:
            df = pd.DataFrame(skills_data)

            st.markdown("""
                <div class="section-box">
                    <h4>📊 Skill Comparison</h4>
            """, unsafe_allow_html=True)

            fig = px.bar(df, x="skill", y=["current", "required"], barmode="group", height=350,
                         color_discrete_map={"current": "#008080", "required": "#00CED1"})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#004D4D"), legend_title_text="Level")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
                <div class="section-box">
                    <h4>📋 Detailed Skill Analysis</h4>
            """, unsafe_allow_html=True)
            st.dataframe(df[["skill", "status", "gap", "priority"]], use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
                <div class="section-box">
                    <h4>🚨 Priority Skill Gaps</h4>
            """, unsafe_allow_html=True)
            if data.get("top_gaps"):
                for gap in data.get("top_gaps", []):
                    st.error(f"🔴 {gap}")
            else:
                st.success("✅ No priority gaps — you're well covered!")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
                <div class="section-box">
                    <h4>💡 Learning Recommendations</h4>
            """, unsafe_allow_html=True)
            for i, rec in enumerate(data.get("recommendations", []), 1):
                st.info(f"{i}. {rec}")
            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# RESUME
# ============================================================

elif page == "📄 Resume":
    st.markdown("""
        <h2 style="color:var(--teal-ink); font-weight:700;">📄 Resume Analyzer</h2>
        <p style="color:var(--muted-teal);">Upload your resume for instant analysis of strengths, weaknesses, and ATS readiness.</p>
    """, unsafe_allow_html=True)

    uploaded_resume = st.file_uploader("📎 Upload Resume (PDF only)", type=["pdf"])

    if uploaded_resume:
        resume_text = extract_resume_text(uploaded_resume)
        if resume_text:
            st.success("✅ Resume successfully read and extracted.")
            with st.expander("👀 Preview Extracted Text"):
                st.text(resume_text[:3000] + ("..." if len(resume_text) > 3000 else ""))

            if st.button("🔍 Analyze Resume", use_container_width=True):
                with st.spinner("Analyzing your resume..."):
                    data = local_resume_analysis(resume_text, st.session_state.target_role)
                    st.session_state.resume_result = data
                    st.session_state.resume_score = int(data.get("score", 75))

    if st.session_state.resume_result:
        data = st.session_state.resume_result
        score = data.get("score", st.session_state.resume_score)

        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">📄 Resume Score</div>
                <div class="stat-value">{score}/100</div>
                <div class="stat-sub">ATS & career readiness</div>
            </div>
        """, unsafe_allow_html=True)

        show_progress("Resume Quality", score)

        st.markdown("""
            <div class="section-box">
                <h4>📝 Summary</h4>
        """, unsafe_allow_html=True)
        st.write(data.get("summary", ""))
        st.markdown("</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
                <div class="section-box">
                    <h4>✅ Strengths</h4>
            """, unsafe_allow_html=True)
            for item in data.get("strengths", []):
                st.success(item)
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("""
                <div class="section-box">
                    <h4>⚠️ Weaknesses</h4>
            """, unsafe_allow_html=True)
            for item in data.get("weaknesses", []):
                st.warning(item)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <div class="section-box">
                <h4>🔎 Missing Keywords</h4>
        """, unsafe_allow_html=True)
        if data.get("missing_keywords"):
            kw_html = "".join([f'<span class="badge-modern badge-warning">+ {k}</span>' for k in data.get("missing_keywords", [])])
            st.markdown(kw_html, unsafe_allow_html=True)
        else:
            st.success("✅ All core keywords for this role are present!")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <div class="section-box">
                <h4>🚀 Improvement Suggestions</h4>
        """, unsafe_allow_html=True)
        for item in data.get("improvements", []):
            st.info(item)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <div class="section-box">
                <h4>🎯 ATS Optimization Advice</h4>
        """, unsafe_allow_html=True)
        st.success(data.get("ats_advice", ""))
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# INTERVIEW
# ============================================================

elif page == "🎤 Interview":
    st.markdown(f"""
        <h2 style="color:var(--teal-ink); font-weight:700;">🎤 Mock Interview</h2>
        <p style="color:var(--muted-teal);">Practice interviewing for <strong style="color:var(--teal-deep);">{st.session_state.target_role}</strong> with AI-generated questions.</p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        difficulty = st.selectbox("📊 Difficulty", ["Easy", "Medium", "Hard"])
    with col2:
        interview_type = st.selectbox("📋 Interview Type", ["Technical", "HR", "Behavioral", "Mixed"])
    with col3:
        question_number = st.selectbox("🔢 Question #", list(range(1, 11)))

    if st.button("🎲 Generate Question", use_container_width=True):
        st.session_state.current_question = generate_interview_question(
            st.session_state.target_role,
            st.session_state.skills if st.session_state.skills else ["Python"],
            difficulty,
            interview_type,
            question_number
        )

    if st.session_state.current_question:
        st.markdown("""
            <div class="ai-box">
        """, unsafe_allow_html=True)

        st.subheader(f"🎯 Question {question_number}/10")
        st.markdown(f"### {st.session_state.current_question}")

        answer = st.text_area("✍️ Your Answer", height=150, placeholder="Type your answer here as if in a real interview...")

        if st.button("🔍 Evaluate Answer", use_container_width=True):
            if answer.strip():
                with st.spinner("Evaluating your answer..."):
                    data = local_evaluate_answer(st.session_state.current_question, answer, st.session_state.target_role)
                    st.session_state.interview_score = int(data.get("overall_score", 75))
                    st.session_state.questions_completed += 1

                    st.subheader("📊 Evaluation Results")
                    col_a, col_b, col_c, col_d = st.columns(4)
                    col_a.metric("Technical", f"{data.get('technical_accuracy', 0)}%")
                    col_b.metric("Communication", f"{data.get('communication', 0)}%")
                    col_c.metric("Confidence", f"{data.get('confidence', 0)}%")
                    col_d.metric("Overall", f"{data.get('overall_score', 0)}%")

                    st.success("💪 " + data.get("strength", ""))
                    st.warning("💡 " + data.get("improvement", ""))

                    with st.expander("👑 View Model Answer"):
                        st.write(data.get("ideal_answer", ""))

                    st.balloons()
            else:
                st.warning("Please type an answer before evaluating.")

        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# COMMUNICATION
# ============================================================

elif page == "🗣️ Communication":
    st.markdown("""
        <h2 style="color:var(--teal-ink); font-weight:700;">🗣️ Communication Analyzer</h2>
        <p style="color:var(--muted-teal);">Get detailed feedback on clarity, structure, confidence, and professionalism.</p>
    """, unsafe_allow_html=True)

    comm_question = st.text_input("🎤 Interview Question", "Tell me about yourself.")
    comm_answer = st.text_area("✍️ Your Answer", height=200, placeholder="Write your answer exactly as you would speak it...")

    if st.button("🧠 Analyze Communication", use_container_width=True):
        if not comm_answer.strip():
            st.warning("Please enter an answer to analyze.")
        else:
            with st.spinner("Analyzing your communication..."):
                data = local_communication_analysis(comm_question, comm_answer)
                st.session_state.communication_result = data
                st.session_state.communication_score = int(data.get("overall_score", 75))

    if st.session_state.communication_result:
        data = st.session_state.communication_result

        st.markdown("""
            <div class="section-box">
                <h4>📊 Communication Score</h4>
        """, unsafe_allow_html=True)
        show_progress("Overall Communication", data.get("overall_score", 0))
        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)
        metrics = [
            ("Clarity", data.get("clarity", 0)),
            ("Confidence", data.get("confidence", 0)),
            ("Structure", data.get("structure", 0)),
            ("Professionalism", data.get("professionalism", 0)),
            ("Conciseness", data.get("conciseness", 0))
        ]
        for col, (label, value) in zip([col1, col2, col3, col4, col5], metrics):
            with col:
                st.metric(label, f"{value}%")

        st.markdown("""
            <div class="section-box">
                <h4>🗣️ Communication Insights</h4>
        """, unsafe_allow_html=True)
        st.info(f"🔤 Filler words detected: {data.get('filler_word_count', 0)}")
        st.markdown("</div>", unsafe_allow_html=True)

        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("""
                <div class="section-box">
                    <h4>✅ What You Did Well</h4>
            """, unsafe_allow_html=True)
            for item in data.get("strengths", []):
                st.success(item)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown("""
                <div class="section-box">
                    <h4>🚀 How to Improve</h4>
            """, unsafe_allow_html=True)
            for item in data.get("improvements", []):
                st.warning(item)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <div class="section-box">
                <h4>✨ Improved Version</h4>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div style="background:linear-gradient(135deg, var(--bg-tint) 0%, #ffffff 100%); padding:1.2rem; border-radius:16px; border:1px solid var(--border-strong); margin-top:0.5rem; color:var(--teal-ink);">
                {data.get("better_version", "")}
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# PROGRESS
# ============================================================

elif page == "🏆 Progress":
    st.markdown("""
        <h2 style="color:var(--teal-ink); font-weight:700;">🏆 Your Progress & Achievements</h2>
    """, unsafe_allow_html=True)

    readiness = int((st.session_state.interview_score + st.session_state.technical_score +
                     st.session_state.communication_score + st.session_state.resume_score) / 4)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Overall Readiness", f"{readiness}%")
    with col2:
        st.metric("🎤 Questions Completed", st.session_state.questions_completed)
    with col3:
        st.metric("🔥 Practice Streak", f"{st.session_state.streak} days")

    st.markdown("""
        <div class="section-box">
            <h4>📈 Skill Progress Trends</h4>
    """, unsafe_allow_html=True)

    progress_df = pd.DataFrame({
        "Area": ["Technical", "Communication", "Resume", "Interview"],
        "Score": [
            st.session_state.technical_score,
            st.session_state.communication_score,
            st.session_state.resume_score,
            st.session_state.interview_score
        ]
    })

    fig = px.bar(progress_df, x="Area", y="Score", range_y=[0, 100], text="Score",
                 color="Area", color_discrete_sequence=["#008080", "#00CED1", "#2E8B57", "#20B2AA"])
    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#004D4D"), showlegend=False)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="section-box">
            <h4>🏅 Achievements</h4>
    """, unsafe_allow_html=True)

    achievements = []
    if st.session_state.questions_completed >= 1:
        achievements.append("🥇 First Interview")
    if st.session_state.questions_completed >= 5:
        achievements.append("🎤 Practice Makes Progress")
    if st.session_state.questions_completed >= 10:
        achievements.append("🎯 Interview Starter")
    if st.session_state.questions_completed >= 25:
        achievements.append("🔥 Interview Warrior")
    if st.session_state.streak >= 7:
        achievements.append("📅 7-Day Streak")
    if st.session_state.streak >= 30:
        achievements.append("🏆 30-Day Champion")
    if st.session_state.resume_score >= 80:
        achievements.append("📄 Resume Ready")
    if st.session_state.communication_score >= 80:
        achievements.append("🗣️ Communication Pro")
    if readiness >= 80:
        achievements.append("🎯 Interview Ready")

    if not achievements:
        achievements = ["🚀 Start practicing to unlock achievements!"]

    ach_html = "".join([f'<span class="badge-modern">{a}</span>' for a in achievements])
    st.markdown(ach_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="section-box">
            <h4>💡 Your Next Goal</h4>
    """, unsafe_allow_html=True)
    if readiness < 60:
        st.warning("🎯 Focus on building your technical foundation through daily practice.")
    elif readiness < 75:
        st.info("🎯 Practice more interviews and improve communication skills.")
    elif readiness < 90:
        st.success("🎯 Getting close! Focus on your skill gaps and keep practicing.")
    else:
        st.success("🏆 Excellent! You are highly interview-ready. Start applying!")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown("""
    <div class="footer-modern">
        <div style="font-size:1.2rem; font-weight:700; color:var(--teal-ink);">🎯 Interview Pilot</div>
        <div style="margin:0.3rem 0;">Career & Interview Readiness Platform</div>
        <div style="color:var(--muted-teal); font-size:0.8rem;">
            Built with Python • Streamlit • Rule-based Local Engine — No External AI Required
        </div>
        <div style="color:var(--muted-teal); font-size:0.8rem;">🚀 Fully Self-Contained • No API Keys Needed</div>
    </div>
""", unsafe_allow_html=True)