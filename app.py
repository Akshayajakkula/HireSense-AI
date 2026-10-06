import re
from pathlib import Path

import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="HireSense AI", page_icon="🧠", layout="wide")

# Skills the app can recognise. Add more of your own!
SKILLS = [
    "Python", "Java", "C", "C++", "JavaScript", "TypeScript", "SQL", "R",
    "HTML", "CSS", "React", "Node.js", "Django", "Flask", "FastAPI", "Streamlit",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Data Analysis",
    "Data Science", "Data Visualization", "Statistics", "Pandas", "NumPy",
    "Scikit-learn", "TensorFlow", "PyTorch", "Keras", "OpenCV", "Transformers",
    "LangChain", "RAG", "ChromaDB", "LLM", "Generative AI", "Prompt Engineering",
    "Gemini", "OpenAI", "Hugging Face", "Power BI", "Tableau", "Excel",
    "MySQL", "MongoDB", "PostgreSQL", "Git", "GitHub", "Docker", "Kubernetes",
    "AWS", "Azure", "GCP", "Linux", "REST API", "Data Structures", "Algorithms",
    "OOP", "Problem Solving", "Communication", "Teamwork", "Leadership",
]


def load_css(path):
    css = Path(path).read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def html(block):
    """Render an HTML block (joins lines so Streamlit does not misread indentation)."""
    st.markdown("".join(line.strip() for line in block.splitlines()), unsafe_allow_html=True)


def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text, len(reader.pages)


def find_skills(text):
    lowered = text.lower()
    found = []
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, lowered):
            found.append(skill)
    return found


def text_similarity(a, b):
    vectors = TfidfVectorizer(stop_words="english").fit_transform([a, b])
    return float(cosine_similarity(vectors[0], vectors[1])[0][0])


def chips(items, kind=""):
    if not items:
        return '<span class="none">None found</span>'
    return "".join(f'<span class="chip {kind}">{s}</span>' for s in items)


load_css("assets/style.css")

# ---------------- HERO ----------------
html("""
<div class="hero">
<span class="orb o1"></span><span class="orb o2"></span>
<span class="badge">✨ AI-powered resume screening</span>
<div class="hero-title">HireSense <span class="grad">AI</span></div>
<div class="hero-sub">Upload a resume, paste a job description, and get an instant match score, skill gaps and improvement tips.</div>
<div class="chips">
<span class="chip">🐍 Python</span><span class="chip">⚡ Streamlit</span><span class="chip">🧮 scikit-learn</span><span class="chip">🧠 NLP</span><span class="chip">📄 PDF Parsing</span>
</div>
</div>
""")

# ---------------- FEATURES ----------------
html("""
<div class="cards">
<div class="card"><div class="icon">📄</div><div class="card-title">Resume Parsing</div><div class="card-text">Reads PDF resumes and pulls out clean text and key details in seconds.</div></div>
<div class="card"><div class="icon">🎯</div><div class="card-title">Smart Matching</div><div class="card-text">Compares a resume with the job description using skills and text similarity.</div></div>
<div class="card"><div class="icon">💡</div><div class="card-title">Skill Insights</div><div class="card-text">Shows matched skills, missing skills and tips to improve the resume.</div></div>
</div>
""")

html("""
<div class="section-title">How it works</div>
<div class="section-sub">Three simple steps</div>
<div class="steps">
<div class="step"><div class="num">1</div><div><div class="step-title">Upload</div><div class="step-text">Add a resume in PDF format.</div></div></div>
<div class="step"><div class="num">2</div><div><div class="step-title">Paste</div><div class="step-text">Paste the job description.</div></div></div>
<div class="step"><div class="num">3</div><div><div class="step-title">Analyze</div><div class="step-text">Get your score and insights.</div></div></div>
</div>
""")

# ---------------- INPUTS ----------------
html("""
<div class="section-title">Screen a resume</div>
<div class="section-sub">Add both inputs, then press Analyze</div>
""")

left, right = st.columns(2, gap="large")
with left:
    uploaded = st.file_uploader("Upload resume (PDF)", type=["pdf"])
with right:
    jd = st.text_area(
        "Paste the job description",
        height=200,
        placeholder="Example: We need an AI/ML intern with Python, Machine Learning, NLP, SQL and Git...",
    )

blind = st.checkbox("🕶️ Blind screening mode (hide personal contact details for fair screening)")
analyze = st.button("🚀 Analyze resume")

# ---------------- RESULTS ----------------
if analyze:
    if uploaded is None or not jd.strip():
        st.warning("Please upload a resume and paste a job description first.")
    else:
        text, pages = read_pdf(uploaded)
        if not text.strip():
            st.error("No text found. This may be a scanned PDF (image). OCR support can be added later.")
            st.stop()

        resume_skills = find_skills(text)
        jd_skills = find_skills(jd)
        matched = [s for s in jd_skills if s in resume_skills]
        missing = [s for s in jd_skills if s not in resume_skills]
        extra = [s for s in resume_skills if s not in jd_skills]

        # Text similarity (scaled x2 because TF-IDF scores are naturally low)
        text_pct = min(100, round(text_similarity(text, jd) * 100 * 2))

        if jd_skills:
            skill_pct = round(len(matched) / len(jd_skills) * 100)
            score = round(0.6 * skill_pct + 0.4 * text_pct)
            skill_label = f"{len(matched)} of {len(jd_skills)} skills"
        else:
            skill_pct = 0
            score = text_pct
            skill_label = "No known skills in job description"

        if score >= 75:
            cls, verdict = "good", "🌟 Excellent match"
        elif score >= 55:
            cls, verdict = "ok", "👍 Good match"
        elif score >= 35:
            cls, verdict = "warn", "⚠️ Partial match"
        else:
            cls, verdict = "bad", "❌ Low match"

        words = len(text.split())

        html("""<div class="section-title">Results</div>""")

        html(f"""
<div class="stats">
<div class="stat"><div class="stat-num">{pages}</div><div class="stat-label">Pages</div></div>
<div class="stat"><div class="stat-num">{words}</div><div class="stat-label">Words</div></div>
<div class="stat"><div class="stat-num">{len(resume_skills)}</div><div class="stat-label">Skills found in resume</div></div>
<div class="stat"><div class="stat-num">{len(matched)}</div><div class="stat-label">Skills matched</div></div>
</div>
""")

        html(f"""
<div class="result">
<div>
<div class="ring {cls}" style="--p:{score}"><span>{score}<small>%</small></span></div>
<div class="verdict">{verdict}</div>
</div>
<div>
<div class="rt">Score breakdown</div>
<div class="bar-row"><div class="bar-label"><span>Skill match (60% weight)</span><span>{skill_label}</span></div><div class="bar"><i style="--w:{skill_pct}%"></i></div></div>
<div class="bar-row"><div class="bar-label"><span>Text similarity (40% weight)</span><span>{text_pct}%</span></div><div class="bar"><i style="--w:{text_pct}%"></i></div></div>
<div class="bar-row"><div class="bar-label"><span>Overall score</span><span>{score}%</span></div><div class="bar"><i style="--w:{score}%"></i></div></div>
</div>
</div>
""")

        html(f"""
<div class="panels">
<div class="panel"><div class="rt">✅ Matched skills ({len(matched)})</div><div class="chips left">{chips(matched, "good")}</div></div>
<div class="panel"><div class="rt">❌ Missing skills ({len(missing)})</div><div class="chips left">{chips(missing, "bad")}</div></div>
</div>
<div class="panel" style="margin-top:20px"><div class="rt">➕ Extra skills in the resume</div><div class="chips left">{chips(extra, "extra")}</div></div>
""")

        if missing:
            tip = "💡 <b>Tip:</b> To improve this resume, add projects, certifications or experience showing: " + ", ".join(missing[:6]) + "."
        else:
            tip = "💡 <b>Tip:</b> This resume covers every skill found in the job description. Great job!"
        html(f'<div class="tip">{tip}</div>')

        # Contact details (hidden in blind mode)
        if blind:
            html('<div class="tip">🕶️ Blind screening is ON: name, email and phone are hidden, so the decision is based only on skills.</div>')
        else:
            emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text)
            phones = re.findall(r"\+?\d[\d\s\-]{8,14}\d", text)
            html(f"""
<div class="panel" style="margin-top:20px"><div class="rt">📇 Contact details found</div>
<div class="chips left">{chips(emails[:2], "extra")}{chips(phones[:1], "extra")}</div></div>
""")
            with st.expander("📄 View extracted resume text"):
                st.text_area("Resume text", text, height=300)

html('<div class="footer">Built with using · Python · Streamlit · scikit-learn</div>')