# 🔍 TruthLens – Fake News Detector

An AI-powered fake news detector built with **Streamlit + Groq (LLaMA 3 70B)**. Fully free to run.

---

## ⚡ Setup & Run (5 minutes)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a free Groq API Key
- Go to [console.groq.com](https://console.groq.com)
- Sign up (free) → API Keys → Create key
- Copy the key (starts with `gsk_...`)

### 3. Run the app
```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

### Optional: Set API key via environment variable
```bash
export GROQ_API_KEY=gsk_your_key_here   # Mac/Linux
set GROQ_API_KEY=gsk_your_key_here      # Windows
streamlit run app.py
```

---

## 🧠 How it works

1. User pastes a news article, headline, or claim
2. App sends it to **Groq's LLaMA 3 70B** with a custom fact-checking system prompt
3. Model returns a structured JSON verdict: `REAL`, `FAKE`, or `UNCERTAIN`
4. App displays confidence score, red flags, credibility signals, and recommendations

## 🛠 Tech Stack
| Component | Tool |
|-----------|------|
| UI | Streamlit |
| LLM | LLaMA 3 70B via Groq |
| Language | Python |
| Cost | 100% Free |

## 📁 Project Structure
```
fake_news_detector/
├── app.py            # Main Streamlit app
├── requirements.txt  # Dependencies
└── README.md         # This file
```

---

## 💡 For College Project Presentation

**Key talking points:**
- Uses **prompt engineering** to instruct LLM to act as a fact-checker
- Returns **structured JSON** output (not just text) for reliable parsing
- Detects red flags: emotional language, missing sources, logical fallacies
- Confidence score gives probabilistic output, not just binary classification
- Can be extended with RAG (Retrieval-Augmented Generation) for real-time web search
