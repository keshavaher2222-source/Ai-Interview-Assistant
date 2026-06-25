import streamlit as st
import random
import plotly.express as px
import plotly.graph_objects as go

from questions import questions
from evaluator import evaluate_answer
from database import create_table, save_result
from analytics import get_data
from pdf_generator import create_pdf
from resume_parser import extract_text

# -------------------------
# INIT DB
# -------------------------
create_table()

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="AI Interview Platform",
    page_icon="🤖",
    layout="wide"
)

# -------------------------
# GLOBAL CSS
# -------------------------
st.markdown("""
<style>

body {
    background-color: #f5f7fb;
}

.header {
    background: #0f172a;
    padding: 18px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size: 22px;
    font-weight: 600;
}

.card {
    background: #ffffff;
    padding: 24px;
    border-radius: 16px;
    border-left: 6px solid #2563eb;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.10);
    margin: 16px 0;
    transition: all 0.25s ease-in-out;
}

.card h3 {
    color: #0f172a;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
}

.card p {
    color: #111827;
    font-size: 20px;
    line-height: 1.7;
    font-weight: 600;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    background: #2563eb;
    color: white;
    font-weight: 600;
    height: 3em;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown("""
<div class="header">
🤖 AI Interview Assessment Platform (PRO)
</div>
""", unsafe_allow_html=True)

# -------------------------
# SESSION STATE
# -------------------------
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.questions = []
    st.session_state.saved = False

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.title("📊 Dashboard")

    if st.session_state.started:
        total = max(len(st.session_state.questions), 1)

        st.metric("Progress", f"{st.session_state.index}/{total}")
        st.metric("Score", round(st.session_state.score, 2))
        st.progress(st.session_state.index / total)

    st.markdown("---")
    st.caption("AI Interview System")

# -------------------------
# START SCREEN
# -------------------------
if not st.session_state.started:

    st.markdown("## 👤 Candidate Registration")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")

    with col2:
        domain = st.selectbox("Domain", list(questions.keys()))

    uploaded = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if uploaded:
        try:
            text = extract_text(uploaded)
            st.success("Resume loaded successfully")
        except Exception as e:
            st.error(f"Resume Error: {e}")

    if st.button("Start Interview"):

        if not name:
            st.warning("Please enter name")
            st.stop()

        st.session_state.name = name
        st.session_state.domain = domain

        st.session_state.questions = random.sample(
            questions[domain],
            min(10, len(questions[domain]))
        )

        st.session_state.started = True
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.saved = False

        st.rerun()

# -------------------------
# INTERVIEW SCREEN
# -------------------------
else:

    total = len(st.session_state.questions)

    # -------------------------
    # COMPLETED SCREEN (FIXED INDEX ERROR)
    # -------------------------
    if st.session_state.index >= total:

        st.balloons()

        final = round(st.session_state.score / total, 2)

        if not st.session_state.saved:
            save_result(
                st.session_state.name,
                st.session_state.domain,
                final
            )
            st.session_state.saved = True

        st.markdown("## 📊 Final Report")

        col1, col2, col3 = st.columns(3)
        col1.metric("Score", f"{final}/10")
        col2.metric("Questions", total)
        col3.metric("Domain", st.session_state.domain)

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=final,
            gauge={"axis": {"range": [0, 10]}}
        ))

        st.plotly_chart(fig, use_container_width=True)

        df = get_data()

        tab1, tab2 = st.tabs(["Analytics", "Leaderboard"])

        with tab1:
            if not df.empty:
                st.plotly_chart(px.bar(df, x="candidate_name", y="score"))

        with tab2:
            if not df.empty:
                st.dataframe(df.sort_values("score", ascending=False).head(10))

        if st.button("Restart Interview"):
            st.session_state.clear()
            st.rerun()

        st.stop()

    # -------------------------
    # QUESTION SCREEN (SAFE ACCESS)
    # -------------------------
    q = st.session_state.questions[st.session_state.index]

    st.progress(st.session_state.index / total)

    st.markdown(f"""
    <div class="card">
        <h3>🎯 Question {st.session_state.index+1}/{total}</h3>
        <p>{q['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    # FORM (FIXED INPUT RESET ISSUE)
    with st.form(key=f"form_{st.session_state.index}"):

        answer = st.text_area("✍ Your Answer", height=180)

        submit = st.form_submit_button("Submit Answer")

        if submit:

            score = evaluate_answer(answer, q["ideal_answer"])
            st.session_state.score += score
            st.session_state.index += 1

            st.rerun()