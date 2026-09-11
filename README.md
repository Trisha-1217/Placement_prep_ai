# 🎓 PlacementPrep AI
### AI-Powered Campus Placement Mock Interview Platform for UN SDG 4: Quality Education

[![UN SDG 4](https://img.shields.io/badge/UN%20SDG-4%20Quality%20Education-C5192D?style=for-the-badge)](https://sdgs.un.org/goals/goal4)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Gemini 3.6 Flash](https://img.shields.io/badge/Google%20Gemini-3.6%20Flash-8E75B2?style=for-the-badge&logo=google)](https://aistudio.google.com)

---

## 🌍 Problem Statement & UN SDG 4 Alignment

In universities and colleges globally, millions of students prepare for competitive technical campus placements. However, high-quality interview preparation remains largely inaccessible:
- **Mentorship Inequality**: Mock interview coaching from senior industry professionals is expensive and scarce.
- **Generic Practice**: Standard question banks lack dynamic, personalized, role-specific follow-ups.
- **Lack of Diagnostic Guidance**: Students often receive rejection emails with zero feedback on why their answers fell short.

**PlacementPrep AI** directly advances **UN SDG 4: Quality Education** by democratizing personalized placement training. It gives every student access to a 24/7 technical interviewer and placement mentor that conducts structured mock interviews, evaluates technical competence, diagnoses specific skill gaps, and generates a personalized 7-day recovery roadmap.

---

## ✨ Key Features

1. **Candidate Profile Setup**:
   - Customizable Candidate Name, Target Role (*SDE 1, Backend Engineer, Frontend Engineer, Full Stack Developer, Data Analyst / Scientist, DevOps / Cloud Engineer*), and Difficulty Level (*Beginner, Intermediate, Advanced*).

2. **Four-Round Mock Interview (8 Questions Total)**:
   - **Round 1: CS Fundamentals** (Operating Systems, DBMS, OOP, Computer Networks).
   - **Round 2: DSA & Problem Solving** (Data Structures, Algorithms, Time & Space Complexity).
   - **Round 3: Project Defense & System Design** (Practical Architecture, Caching, Scalability Bottlenecks).
   - **Round 4: HR & Behavioral** (Communication, STAR Methodology, Conflict Resolution).
   - **Strict Turn Pacing**: Exactly one question at a time, exactly 2 questions per round, with immediate 1–2 sentence constructive pedagogical feedback after each response.

3. **Multi-Factor AI Evaluation**:
   - Quantitative scoring (1.0–10.0) across 4 core competencies:
     - **Technical Competence**
     - **Problem Solving**
     - **Communication**
     - **Professionalism**

4. **Diagnostic Skill-Gap Analysis**:
   - Pinpoints specific weak topics based on the candidate's answers with clear diagnostic reasoning explaining *why* improvement is needed.
   - Categorized by priority (*High Priority* / *Medium Priority*).

5. **Comprehensive Performance Report**:
   - Round-wise scores and factor-wise scores.
   - Key validated strengths and targeted improvement areas.
   - Final recommendation verdict (*Strong Hire, Hire, Leaning Hire, Needs More Preparation*).

6. **Personalized 7-Day Improvement Roadmap**:
   - Day-by-day actionable curriculum (Day 1 through Day 7) directly targeting identified skill gaps.
   - Downloadable evaluation dossier in Markdown format.

7. **Standardized Next Gen Chatbot Arena API**:
   - Compliant `POST /chat` and `GET /health` endpoints for automated evaluation.

---

## 🛠️ Technology Stack

- **Frontend & Web UI**: Streamlit (Python)
- **Evaluation API Server**: FastAPI, Uvicorn, Pydantic
- **AI / LLM Foundation**: Google Gemini API (`gemini-3.6-flash` via official `google-genai` SDK)
- **Environment & Security**: `python-dotenv`, Streamlit Secrets, environment variable isolation
- **QR Code Utility**: `qrcode[pil]`

---

## 🚀 How to Run Locally

### 1. Clone & Navigate to Workspace
```bash
cd Placement_prep
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# Windows (cmd/powershell)
copy .env.example .env

# macOS / Linux
cp .env.example .env
```
Edit `.env` and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
> **Security Note**: Never commit `.env`. It is ignored by `.gitignore`.

### 5. Run the Streamlit Web Application
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

### 6. Run the FastAPI Evaluation Endpoint
In a separate terminal:
```bash
python api.py
```
Or directly with Uvicorn:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```
- API Endpoint: **`http://localhost:8000/chat`**
- Interactive Swagger Docs: **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 📡 API Endpoints

### 1. `GET /health`
Verifies server health and Gemini API connectivity.
- **Request:** `GET http://localhost:8000/health`
- **Response:**
  ```json
  {
    "status": "healthy",
    "service": "PlacementPrep AI API",
    "gemini_configured": true
  }
  ```

### 2. `POST /chat`
Mandatory Arena Evaluation endpoint.
- **Request:** `POST http://localhost:8000/chat`
- **Payload:**
  ```json
  {
    "message": "Teach me the basics of linear regression as if I am a beginner, then give me three practice questions."
  }
  ```
- **Response:**
  ```json
  {
    "response": "### Understanding Linear Regression (SDG 4: Quality Education)\n\nLinear Regression is a foundational supervised machine learning algorithm...\n\n### Practice Questions:\n1. ..."
  }
  ```

---

## ☁️ Deployment Instructions

### Deploying the Web UI (Streamlit Community Cloud)
1. Push your repository to GitHub (ensure `.env` is NOT included).
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a **New App**.
3. Select your repository, branch (`main`), and set the main file path to `app.py`.
4. In **Advanced Settings** ➔ **Secrets**, paste your Gemini key:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key_here"
   ```
5. Click **Deploy**. The app will read `GEMINI_API_KEY` seamlessly from Streamlit Secrets.

### Deploying the FastAPI Endpoint (Render / Railway)
1. Connect your GitHub repository to [Render](https://render.com) or [Railway](https://railway.app).
2. Create a **Web Service**.
3. Configure the build and start commands:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
4. In Environment Variables, add:
   - `GEMINI_API_KEY`: `your_actual_gemini_api_key_here`
5. Deploy the service. Your evaluation endpoint will be live at `https://<your-service>.onrender.com/chat`.

---

## 📄 License
MIT License - Built for the Next Gen Chatbot Arena (UN SDG 4: Quality Education).
