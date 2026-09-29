# OpsMind — AI Incident Response Agent

OpsMind is an AI-powered incident response assistant that uses **Hindsight persistent memory** to help SRE and DevOps teams investigate production incidents using knowledge from previous incidents.

## 🚀 What OpsMind Does

OpsMind follows a continuous learning loop:

**Detect → Recall → Analyze → Resolve → Remember**

Instead of investigating every incident from zero, OpsMind recalls relevant previous incidents, resolutions, and outcomes before generating its investigation.

## 🧠 Hindsight Memory

Hindsight is the core memory layer of OpsMind.

It stores:

* Previous production incidents
* Root causes
* Resolutions
* Incident outcomes
* Operational experience

When a similar incident happens again, OpsMind recalls relevant experience and uses it to provide a more context-aware investigation.

## ⚙️ Technology Stack

* Python
* Streamlit
* Groq
* Hindsight by Vectorize
* hindsight-client
* python-dotenv

## 🏗️ Architecture

```text
User
  ↓
Streamlit UI
  ↓
OpsMind Incident Agent
  ↓
Hindsight Recall
  ↓
Groq AI Analysis
  ↓
Human Review
  ↓
Resolution + Outcome
  ↓
Hindsight Retain
  ↓
Future Incidents
```

## 🔄 Example Workflow

1. A production incident is reported.
2. OpsMind searches Hindsight for similar incidents.
3. Previous resolutions and outcomes are recalled.
4. Groq analyzes the current incident using that context.
5. A human confirms the resolution.
6. The incident, resolution, and outcome are stored in Hindsight.
7. Future similar incidents can benefit from the stored experience.

## 🎯 Problem

Traditional AI systems often respond only to the current incident. They do not automatically remember what previously happened, what fixed it, or what the outcome was.

OpsMind makes operational memory part of the incident-response loop.

## 💻 Run Locally

Clone the repository:

```bash
git clone https://github.com/kasamsrinidhi123/opsmind-ai-incident-response.git
cd opsmind-ai-incident-response
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file with your API credentials:

```text
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
GROQ_API_KEY=your_groq_api_key
```

Run the application:

```bash
streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

## 🔐 Security

API keys are stored in `.env` and are excluded from Git using `.gitignore`.

Never commit API keys or other secrets to the repository.

## 🏆 Hackathon

Built for **HackwithHyderabad 3.0 — AI Agents That Learn Using Hindsight**.

**Project:** OpsMind
**Focus:** AI Incident Response + Persistent Operational Memory
