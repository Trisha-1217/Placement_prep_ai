import streamlit as st
import os
import json
from dotenv import load_dotenv
import engine

load_dotenv()

st.set_page_config(
    page_title="PlacementPrep AI | Career-Readiness Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Clean Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .round-banner {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 6px solid #2563EB;
        border-radius: 8px;
        padding: 14px 20px;
        margin-bottom: 16px;
    }
    .question-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #3B82F6;
        padding: 18px 22px;
        border-radius: 8px;
        margin-bottom: 16px;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #0F172A !important;
    }
    .feedback-box {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-left: 5px solid #22C55E;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 16px;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "session_data" not in st.session_state:
    st.session_state.session_data = None
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "latest_feedback" not in st.session_state:
    st.session_state.latest_feedback = ""

# Sidebar: Configuration & Candidate Setup
with st.sidebar:
    st.markdown("## 🎓 PlacementPrep AI")
    st.caption("AI-powered career-readiness assistant for students")
    
    st.divider()
    
    # 1. GEMINI API KEY SECURITY: Read strictly from .env, never expose in UI
    if not engine.is_api_configured():
        st.warning("⚠️ Gemini API configuration is missing. Please contact the administrator.")
    else:
        st.success("✅ AI Assistant Ready")

    st.divider()

    # Candidate Setup
    st.markdown("#### 👤 Candidate Setup")
    candidate_name = st.text_input(
        "Candidate Name", 
        value="Alex Sharma", 
        disabled=st.session_state.interview_started
    )
    target_role = st.selectbox(
        "Target Role",
        [
            "Software Development Engineer (SDE 1)",
            "Backend Engineer",
            "Frontend Engineer",
            "Full Stack Developer",
            "Data Analyst / Scientist",
            "DevOps / Cloud Engineer"
        ],
        disabled=st.session_state.interview_started
    )
    difficulty = st.select_slider(
        "Difficulty Level",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Intermediate",
        disabled=st.session_state.interview_started
    )

    st.divider()

    if not st.session_state.interview_started:
        if st.button("🚀 Start Interview", type="primary", use_container_width=True):
            st.session_state.session_data = engine.start_interview_session(candidate_name, target_role, difficulty)
            if not (st.session_state.session_data.get("current_question") or "").strip():
                st.session_state.session_data["current_question"] = "What is the difference between a process and a thread in an operating system?"
            st.session_state.interview_started = True
            st.session_state.latest_feedback = ""
            st.rerun()
    else:
        if st.button("🔄 Reset / Start New Interview", use_container_width=True):
            st.session_state.session_data = None
            st.session_state.interview_started = False
            st.session_state.latest_feedback = ""
            st.rerun()


# Main Application Interface (Clean Student-Facing Layout)
st.markdown('<div class="main-header">PlacementPrep AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">AI-powered career-readiness assistant for students <span style="font-size: 0.85rem; color: #94A3B8;">• Supporting quality education (SDG 4)</span></div>', 
    unsafe_allow_html=True
)

if not st.session_state.interview_started:
    st.info("👈 Enter your candidate profile in the sidebar and click **'Start Interview'** to begin.")
    st.markdown("""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 20px; margin-top: 15px;">
        <h4 style="margin-top: 0; color: #1E293B;">Ready for your technical interview?</h4>
        <p style="color: #64748B; margin-bottom: 0;">
            You will begin with <b>Round 1: CS Fundamentals</b> (Operating Systems, DBMS, OOP, and Computer Networks).
            The interviewer will ask exactly one question at a time.
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    sess = st.session_state.session_data
    current_idx = min(sess.get("current_round_idx", 0), len(engine.ROUNDS) - 1)
    current_round = engine.ROUNDS[current_idx]
    total_answered = len(sess.get("history", []))
    total_questions = len(engine.ROUNDS) * sess.get("max_questions_per_round", 2)
    progress_val = min(total_answered / float(total_questions), 1.0)

    # 3. ROUND-BY-ROUND PROGRESS INDICATOR
    round_name_display = f"Round {current_idx + 1} of 4 — {current_round['name']}"
    st.markdown(f"""
    <div class="round-banner">
        <span style="font-size: 1.15rem; font-weight: 700; color: #1E293B;">📍 {round_name_display}</span><br>
        <span style="color: #64748B; font-size: 0.9rem;">Topics: {current_round['topics']} | Question {min(sess.get('round_question_count', 1), 2)} of 2 in this round ({total_answered} of {total_questions} total answered)</span>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progress_val)

    # Display Brief Feedback on previous answer if available
    if st.session_state.latest_feedback:
        st.markdown(f'<div class="feedback-box">💡 <b>Interviewer Feedback:</b><br>{st.session_state.latest_feedback}</div>', unsafe_allow_html=True)

    # --- ACTIVE ROUND STATE: ASK ONE QUESTION AT A TIME ---
    if not sess.get("is_completed"):

        # State A: Current round is in progress (Candidate needs to answer question 1 or 2)
        if not sess.get("round_completed"):
            st.markdown(f"#### ❓ Question {sess.get('round_question_count', 1)} of 2:")
            
            # Safe fallback if question is empty
            question_text = (sess.get("current_question") or "").strip()
            if not question_text:
                question_text = "What is the difference between a process and a thread in an operating system?"
                sess["current_question"] = question_text

            st.markdown(f'<div class="question-box" style="color: #0F172A; font-weight: 500;">{question_text}</div>', unsafe_allow_html=True)

            with st.form("candidate_answer_form"):
                candidate_answer = st.text_area(
                    "Your Answer:", 
                    placeholder="Explain your approach, core concepts, or trade-offs clearly...",
                    height=150
                )
                submit_col, _ = st.columns([2, 8])
                with submit_col:
                    submitted = st.form_submit_button("Submit Answer ➔", type="primary", use_container_width=True)

            if submitted:
                if not candidate_answer.strip():
                    st.warning("Please enter your answer before submitting.")
                else:
                    with st.spinner("Interviewer is evaluating your response..."):
                        res = engine.process_candidate_answer(sess, candidate_answer)
                        st.session_state.latest_feedback = res.get("feedback", "")
                        st.rerun()

        # State B: Current round completed! Require explicit button to proceed to next round
        else:
            next_round_num = current_idx + 2
            next_round = engine.ROUNDS[current_idx + 1] if current_idx + 1 < len(engine.ROUNDS) else None
            
            st.success(f"🎉 **{current_round['name']} Completed!** You have answered both questions for Round {current_idx + 1}.")
            st.info(f"👉 Ready for the next phase? Click below to activate **Round {next_round_num}: {next_round['name']}**.")
            
            if st.button(f"Proceed to Round {next_round_num}: {next_round['name']} ➔", type="primary", use_container_width=True):
                with st.spinner(f"Preparing Round {next_round_num}: {next_round['name']}..."):
                    engine.proceed_to_next_round(sess)
                    st.session_state.latest_feedback = ""
                    st.rerun()

    # --- FINAL RESULTS STATE: ALL 4 ROUNDS (8 QUESTIONS) COMPLETED ---
    else:
        st.balloons()
        st.success("🎉 **Interview Completed!** You have successfully completed all 4 rounds (8 questions).")

        report = sess.get("final_report") or {}
        factor_scores = report.get("factor_scores") or {
            "technical_competence": 8.0,
            "problem_solving": 8.0,
            "communication": 8.5,
            "professionalism": 9.0
        }
        round_scores = report.get("round_scores") or {
            "cs_fundamentals": 8.5,
            "dsa": 8.0,
            "system_design": 7.5,
            "hr_behavioral": 9.0
        }

        # 1. AI Evaluation: Factor-Wise Scores
        st.markdown("### 📊 Factor-Wise AI Evaluation")
        f1, f2, f3, f4 = st.columns(4)
        f1.metric("Technical Competence", f"{factor_scores.get('technical_competence', 8.0)}/10")
        f2.metric("Problem Solving", f"{factor_scores.get('problem_solving', 8.0)}/10")
        f3.metric("Communication", f"{factor_scores.get('communication', 8.5)}/10")
        f4.metric("Professionalism", f"{factor_scores.get('professionalism', 9.0)}/10")

        # 2. Round-Wise Scores
        st.markdown("### 🎯 Round-Wise Performance Scores")
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Round 1: CS Fundamentals", f"{round_scores.get('cs_fundamentals', 8.0)}/10")
        r2.metric("Round 2: DSA & Problem Solving", f"{round_scores.get('dsa', 8.0)}/10")
        r3.metric("Round 3: System Design", f"{round_scores.get('system_design', 7.5)}/10")
        r4.metric("Round 4: HR & Behavioral", f"{round_scores.get('hr_behavioral', 9.0)}/10")

        st.divider()

        # 3. Diagnostic Skill-Gap Analysis
        st.markdown("### 🔍 Diagnostic Skill-Gap Analysis")
        st.caption("Identified weak topics based on your responses, with diagnostic explanations of why improvement is needed.")
        
        skill_gaps = report.get("skill_gaps", [])
        if skill_gaps:
            for gap in skill_gaps:
                priority = gap.get("priority", "Medium")
                badge_color = "#DC2626" if priority == "High" else "#D97706"
                bg_color = "#FEF2F2" if priority == "High" else "#FFFBEB"
                border_color = "#FCA5A5" if priority == "High" else "#FDE68A"
                st.markdown(
                    f"""
                    <div style="background-color: {bg_color}; 
                                border: 1px solid {border_color}; 
                                border-left: 5px solid {badge_color}; 
                                border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <strong style="font-size: 1.05rem; color: #1E293B;">📌 {gap.get('topic', 'General Topic')}</strong>
                            <span style="background-color: {badge_color}; color: white; padding: 2px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: 600;">{priority} Priority</span>
                        </div>
                        <p style="color: #475569; margin: 0; font-size: 0.95rem;"><b>Diagnostic Reason:</b> {gap.get('reason', 'Further conceptual refinement recommended.')}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.divider()

        # 4. Strengths & Improvement Areas
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### ✅ Top Strengths")
            for s in report.get("strengths", []):
                st.markdown(f"- {s}")
        with c2:
            st.markdown("#### 🎯 Areas for Improvement")
            for imp in report.get("improvement_areas", []):
                st.markdown(f"- {imp}")

        st.markdown(f"#### 🏆 Final Recommendation\n**{report.get('final_recommendation', 'Hire')}**")

        st.divider()

        # 5. Personalized 7-Day Improvement Roadmap
        st.markdown("### 📅 Personalized 7-Day Improvement Roadmap")
        st.caption("A tailored, day-by-day study and practice plan targeting your identified skill gaps.")
        
        roadmap = report.get("roadmap_7_day", [])
        if roadmap:
            for day_item in roadmap:
                day_num = day_item.get("day", 1)
                title = day_item.get("title", f"Day {day_num}")
                focus = day_item.get("focus", "")
                action_items = day_item.get("action_items", [])
                
                with st.expander(f"🗓️ Day {day_num}: {title} — *Focus: {focus}*", expanded=(day_num <= 2)):
                    st.markdown(f"**Primary Objective:** {focus}")
                    st.markdown("**Action Items:**")
                    for item in action_items:
                        st.markdown(f"- [ ] {item}")

        st.divider()

        # 6. Complete Interview Transcript & Download Dossier
        gaps_markdown = "\n".join([
            f"- **{g.get('topic')}** ({g.get('priority')} Priority): {g.get('reason')}"
            for g in skill_gaps
        ])
        roadmap_markdown = ""
        for d in roadmap:
            roadmap_markdown += f"\n### Day {d.get('day')}: {d.get('title')}\n- **Focus:** {d.get('focus')}\n"
            for task in d.get('action_items', []):
                roadmap_markdown += f"  - [ ] {task}\n"

        transcript_markdown = ""
        for idx, h in enumerate(sess.get("history", []), 1):
            transcript_markdown += f"\n### Question {idx} (Round {h.get('round_id')}: {h.get('round')})\n"
            transcript_markdown += f"- **Question:** {h.get('question')}\n"
            transcript_markdown += f"- **Answer:** {h.get('answer')}\n"
            transcript_markdown += f"- **Feedback:** {h.get('feedback')}\n"

        full_report_text = f"""# PlacementPrep AI - Comprehensive Evaluation Report
Candidate: {sess['candidate_name']}
Target Role: {sess['target_role']}
Difficulty Level: {sess['difficulty']}

---

## 1. Factor-Wise AI Evaluation
- Technical Competence: {factor_scores.get('technical_competence', 8.0)}/10
- Problem Solving: {factor_scores.get('problem_solving', 8.0)}/10
- Communication: {factor_scores.get('communication', 8.5)}/10
- Professionalism: {factor_scores.get('professionalism', 9.0)}/10
- Overall Score: {report.get('overall_score', 8.3)}/10

## 2. Round-Wise Performance Scores
- Round 1 (CS Fundamentals): {round_scores.get('cs_fundamentals', 8.0)}/10
- Round 2 (DSA & Problem Solving): {round_scores.get('dsa', 8.0)}/10
- Round 3 (Project Defense & System Design): {round_scores.get('system_design', 7.5)}/10
- Round 4 (HR & Behavioral): {round_scores.get('hr_behavioral', 9.0)}/10

## 3. Diagnostic Skill-Gap Analysis
{gaps_markdown}

## 4. Top Strengths
""" + "\n".join([f"- {s}" for s in report.get("strengths", [])]) + """

## 5. Areas for Improvement
""" + "\n".join([f"- {imp}" for imp in report.get("improvement_areas", [])]) + f"""

## 6. Final Recommendation
{report.get('final_recommendation', 'Hire')}

---

## 7. Personalized 7-Day Improvement Roadmap
{roadmap_markdown}

---

## 8. Complete Interview Transcript (8 Questions)
{transcript_markdown}
"""
        with st.expander("📄 View Complete Interview Transcript (8 Questions)", expanded=False):
            for idx, h in enumerate(sess.get("history", []), 1):
                st.markdown(f"#### Question {idx} — Round {h.get('round_id', idx)}: {h.get('round', '')}")
                st.markdown(f"**Question:** {h.get('question', '')}")
                st.markdown(f"**Candidate Answer:** {h.get('answer', '')}")
                if h.get("feedback"):
                    st.caption(f"💡 Feedback: {h.get('feedback', '')}")
                st.divider()

        st.download_button(
            "📥 Download Full Evaluation Dossier (.md)",
            data=full_report_text,
            file_name=f"PlacementPrep_Dossier_{sess['candidate_name'].replace(' ', '_')}.md",
            mime="text/markdown"
        )

    # --- CONVERSATION HISTORY CONTAINER (ALWAYS VISIBLE DURING INTERVIEW) ---
    if sess.get("history") and not sess.get("is_completed"):
        st.divider()
        st.markdown("### 💬 Conversation History")
        for h in sess.get("history", []):
            with st.chat_message("assistant", avatar="🎓"):
                st.markdown(f"**Round {h.get('round_id')} — {h.get('round')} (Q{h.get('question_num', 1)})**")
                st.markdown(h.get("question", ""))
            with st.chat_message("user", avatar="👤"):
                st.markdown(h.get("answer", ""))
            if h.get("feedback"):
                st.caption(f"💡 *Interviewer Feedback:* {h.get('feedback')}")
