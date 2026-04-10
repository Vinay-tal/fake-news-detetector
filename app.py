import streamlit as st
import requests
import os
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TruthLens – Fake News Detector",
    page_icon="🔍",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* Hide default Streamlit header */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Hero title */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #f0f0ff 30%, #7c6aff 70%, #ff6a9a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    line-height: 1.1;
}

.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: #555577;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a40, #7c6aff44, #2a2a40, transparent);
    margin: 2rem 0;
}

/* Text area override */
.stTextArea textarea {
    background: #12121e !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 1rem !important;
}
.stTextArea textarea:focus {
    border-color: #7c6aff !important;
    box-shadow: 0 0 0 2px #7c6aff22 !important;
}

/* Input field */
.stTextInput input {
    background: #12121e !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextInput input:focus {
    border-color: #7c6aff !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #7c6aff, #9d5cff) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px #7c6aff44 !important;
}

/* Result cards */
.result-card {
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-top: 1.5rem;
    border: 1px solid;
    animation: fadeUp 0.4s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.card-real {
    background: #0a1f12;
    border-color: #1a5c2a;
}
.card-fake {
    background: #1f0a0a;
    border-color: #5c1a1a;
}
.card-uncertain {
    background: #141410;
    border-color: #4a4a1a;
}

.verdict-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.verdict-text {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}
.verdict-real  { color: #4ade80; }
.verdict-fake  { color: #f87171; }
.verdict-uncertain { color: #facc15; }

.confidence-bar-wrap {
    background: #ffffff11;
    border-radius: 99px;
    height: 6px;
    margin-bottom: 1.2rem;
    overflow: hidden;
}
.confidence-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.6s ease;
}

.explanation-text {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.92rem;
    color: #aaaacc;
    line-height: 1.7;
    border-top: 1px solid #ffffff11;
    padding-top: 1rem;
    margin-top: 0.5rem;
}

.meta-pill {
    display: inline-block;
    background: #ffffff08;
    border: 1px solid #ffffff15;
    border-radius: 99px;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #7777aa;
    padding: 0.2rem 0.75rem;
    margin-right: 0.4rem;
    margin-bottom: 0.8rem;
}

.tip-box {
    background: #12121e;
    border: 1px solid #2a2a40;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #6666aa;
    font-family: 'DM Mono', monospace;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">TruthLens</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">// AI-powered fake news detector · powered by Groq</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── API Key input ─────────────────────────────────────────────────────────────
with st.expander("🔑 Enter your Groq API Key", expanded=not bool(os.environ.get("GROQ_API_KEY"))):
    st.markdown('<div class="tip-box">Get a free key at <strong>console.groq.com</strong> → API Keys. It\'s 100% free.</div>', unsafe_allow_html=True)
    st.markdown("")
    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        label_visibility="collapsed"
    )

# Resolve API key (env var takes priority)
api_key = os.environ.get("GROQ_API_KEY") or api_key_input

# ── Main Input ────────────────────────────────────────────────────────────────
st.markdown("#### Paste your article or claim below")
user_text = st.text_area(
    "Article / Headline / Claim",
    placeholder="e.g.  'Scientists confirm that drinking bleach cures the common cold...' \nor paste a full article text here.",
    height=220,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_btn = st.button("🔍 Analyze Now", use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Analysis ──────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert fact-checker and investigative journalist with deep knowledge of misinformation patterns, logical fallacies, and media literacy.

Analyze the given article/claim and respond ONLY in valid JSON with this exact structure:
{
  "verdict": "REAL" | "FAKE" | "UNCERTAIN",
  "confidence": <integer 0-100>,
  "headline_summary": "<one-sentence summary of the claim>",
  "red_flags": ["<flag1>", "<flag2>", ...],  // list of suspicious elements found (empty list if none)
  "credibility_signals": ["<signal1>", ...],  // list of credible elements found (empty list if none)
  "explanation": "<2-3 sentence plain-english explanation of your verdict>",
  "recommendation": "<one actionable tip for the reader>"
}

Verdict definitions:
- REAL: Content appears factual, well-sourced, consistent with known facts
- FAKE: Contains clear misinformation, fabricated claims, or manipulative language
- UNCERTAIN: Mixture of facts and speculation, unverifiable, or missing context

Be objective, thorough, and base your analysis on linguistic patterns, logical consistency, and known facts."""


def analyze(text: str, key: str) -> dict:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this:\n\n{text}"}
            ],
            "temperature": 0.2,
            "max_tokens": 900,
        }
    )
    response.raise_for_status()
    raw = response.json()["choices"][0]["message"]["content"].strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def render_result(data: dict):
    verdict = data.get("verdict", "UNCERTAIN").upper()
    confidence = data.get("confidence", 50)
    explanation = data.get("explanation", "")
    recommendation = data.get("recommendation", "")
    red_flags = data.get("red_flags", [])
    credibility_signals = data.get("credibility_signals", [])
    summary = data.get("headline_summary", "")

    card_class = {"REAL": "card-real", "FAKE": "card-fake"}.get(verdict, "card-uncertain")
    verdict_class = {"REAL": "verdict-real", "FAKE": "verdict-fake"}.get(verdict, "verdict-uncertain")
    verdict_emoji = {"REAL": "✅", "FAKE": "🚨"}.get(verdict, "⚠️")
    bar_color = {"REAL": "#4ade80", "FAKE": "#f87171"}.get(verdict, "#facc15")

    st.markdown(f"""
    <div class="result-card {card_class}">
        <div class="verdict-label">Verdict</div>
        <div class="verdict-text {verdict_class}">{verdict_emoji} {verdict}</div>
        <span class="meta-pill">Confidence: {confidence}%</span>
        <span class="meta-pill">Model: llama-3.3-70b-versatile</span>
        <div class="confidence-bar-wrap">
            <div class="confidence-bar-fill" style="width:{confidence}%; background:{bar_color};"></div>
        </div>
        <div class="explanation-text">
            <strong style="color:#e8e8f0; font-family:'Syne',sans-serif;">Summary:</strong><br>
            {summary}<br><br>
            <strong style="color:#e8e8f0; font-family:'Syne',sans-serif;">Analysis:</strong><br>
            {explanation}<br><br>
            <strong style="color:#e8e8f0; font-family:'Syne',sans-serif;">💡 What to do:</strong><br>
            {recommendation}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if red_flags or credibility_signals:
        col_a, col_b = st.columns(2)
        with col_a:
            if red_flags:
                st.markdown("**🚩 Red Flags**")
                for f in red_flags:
                    st.markdown(f"- {f}")
        with col_b:
            if credibility_signals:
                st.markdown("**✅ Credibility Signals**")
                for s in credibility_signals:
                    st.markdown(f"- {s}")


if analyze_btn:
    if not api_key:
        st.error("Please enter your Groq API key above.")
    elif len(user_text.strip()) < 30:
        st.warning("Please enter at least a sentence or headline to analyze.")
    else:
        with st.spinner("Analyzing with Groq LLaMA 3 70B..."):
            try:
                result = analyze(user_text.strip(), api_key)
                render_result(result)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ── Footer tips ───────────────────────────────────────────────────────────────
st.markdown("")
st.markdown("""
<div class="tip-box">
📌 <strong>Tips for best results:</strong><br>
• Paste full article text for deeper analysis &nbsp;·&nbsp; Headlines alone work too<br>
• Works for English text · supports news, social posts, WhatsApp forwards<br>
• Always cross-check with fact-checking sites like <em>snopes.com</em> or <em>factcheck.org</em>
</div>
""", unsafe_allow_html=True)
