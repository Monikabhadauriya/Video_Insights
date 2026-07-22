# import streamlit as st
# import time
# from dotenv import load_dotenv
# from utils.audio_processor import process_input
# from core.transcriber import transcribe_all
# from core.summarizer import summarize, generate_title
# from core.extractor import extract_action_items, extract_key_decisions, extract_questions
# from core.rag_engine import build_rag_chain, ask_question

# load_dotenv()

# # ─── Page Config ────────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="AI Video Assistant",
#     page_icon="🎬",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ─── Custom CSS ─────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

# /* ── Root Variables ── */
# :root {
#     --bg: #0a0a0f;
#     --surface: #111118;
#     --surface-2: #1a1a25;
#     --border: #2a2a3a;
#     --accent: #7c3aed;
#     --accent-glow: #9f67ff;
#     --accent-2: #06b6d4;
#     --text: #e8e8f0;
#     --text-muted: #7070a0;
#     --success: #10b981;
#     --warning: #f59e0b;
#     --danger: #ef4444;
# }

# /* ── Global Reset ── */
# html, body, [class*="css"] {
#     font-family: 'JetBrains Mono', monospace;
#     background-color: var(--bg) !important;
#     color: var(--text) !important;
# }

# .stApp {
#     background: var(--bg) !important;
# }

# /* Animated grid background */
# .stApp::before {
#     content: '';
#     position: fixed;
#     top: 0; left: 0;
#     width: 100%; height: 100%;
#     background-image:
#         linear-gradient(rgba(124, 58, 237, 0.03) 1px, transparent 1px),
#         linear-gradient(90deg, rgba(124, 58, 237, 0.03) 1px, transparent 1px);
#     background-size: 40px 40px;
#     pointer-events: none;
#     z-index: 0;
# }

# /* ── Sidebar ── */
# [data-testid="stSidebar"] {
#     background: var(--surface) !important;
#     border-right: 1px solid var(--border) !important;
# }

# [data-testid="stSidebar"] * {
#     color: var(--text) !important;
# }

# /* ── Headings ── */
# h1, h2, h3, h4, h5, h6 {
#     font-family: 'Syne', sans-serif !important;
#     color: var(--text) !important;
# }

# /* ── Hero Title ── */
# .hero-title {
#     font-family: 'Syne', sans-serif;
#     font-size: clamp(2rem, 5vw, 3.5rem);
#     font-weight: 800;
#     line-height: 1.1;
#     margin: 0;
#     background: linear-gradient(135deg, #ffffff 0%, var(--accent-glow) 50%, var(--accent-2) 100%);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
# }

# .hero-sub {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.8rem;
#     color: var(--text-muted);
#     letter-spacing: 0.2em;
#     text-transform: uppercase;
#     margin-top: 0.5rem;
# }

# /* ── Cards ── */
# .card {
#     background: var(--surface);
#     border: 1px solid var(--border);
#     border-radius: 12px;
#     padding: 1.5rem;
#     margin-bottom: 1rem;
#     position: relative;
#     overflow: hidden;
#     transition: border-color 0.2s;
# }

# .card:hover {
#     border-color: var(--accent);
# }

# .card::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 0;
#     width: 3px; height: 100%;
#     background: linear-gradient(180deg, var(--accent), var(--accent-2));
# }

# .card-title {
#     font-family: 'Syne', sans-serif;
#     font-size: 0.7rem;
#     font-weight: 700;
#     letter-spacing: 0.15em;
#     text-transform: uppercase;
#     color: var(--text-muted);
#     margin-bottom: 0.75rem;
#     display: flex;
#     align-items: center;
#     gap: 0.5rem;
# }

# .card-content {
#     font-size: 0.875rem;
#     line-height: 1.7;
#     color: var(--text);
# }

# /* ── Accent Badge ── */
# .badge {
#     display: inline-block;
#     padding: 0.2rem 0.6rem;
#     border-radius: 4px;
#     font-size: 0.65rem;
#     font-weight: 600;
#     letter-spacing: 0.1em;
#     text-transform: uppercase;
# }

# .badge-purple { background: rgba(124,58,237,0.2); color: var(--accent-glow); border: 1px solid rgba(124,58,237,0.3); }
# .badge-cyan   { background: rgba(6,182,212,0.15); color: var(--accent-2);    border: 1px solid rgba(6,182,212,0.3); }
# .badge-green  { background: rgba(16,185,129,0.15); color: var(--success);    border: 1px solid rgba(16,185,129,0.3); }

# /* ── Input & Buttons ── */
# .stTextInput > div > div > input,
# .stSelectbox > div > div {
#     background: var(--surface-2) !important;
#     border: 1px solid var(--border) !important;
#     border-radius: 8px !important;
#     color: var(--text) !important;
#     font-family: 'JetBrains Mono', monospace !important;
# }

# .stTextInput > div > div > input:focus {
#     border-color: var(--accent) !important;
#     box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
# }

# .stButton > button {
#     background: linear-gradient(135deg, var(--accent), #5b21b6) !important;
#     color: white !important;
#     border: none !important;
#     border-radius: 8px !important;
#     font-family: 'Syne', sans-serif !important;
#     font-weight: 700 !important;
#     font-size: 0.875rem !important;
#     letter-spacing: 0.05em !important;
#     padding: 0.6rem 1.5rem !important;
#     transition: all 0.2s !important;
#     text-transform: uppercase !important;
# }

# .stButton > button:hover {
#     transform: translateY(-1px) !important;
#     box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
# }

# /* Secondary button */
# .stButton > button[kind="secondary"] {
#     background: var(--surface-2) !important;
#     border: 1px solid var(--border) !important;
# }

# /* ── Progress / Status ── */
# .status-bar {
#     display: flex;
#     align-items: center;
#     gap: 0.75rem;
#     padding: 0.75rem 1rem;
#     background: var(--surface-2);
#     border-radius: 8px;
#     margin: 0.4rem 0;
#     border: 1px solid var(--border);
#     font-size: 0.8rem;
# }

# .status-dot {
#     width: 8px; height: 8px;
#     border-radius: 50%;
#     flex-shrink: 0;
# }

# .dot-active   { background: var(--accent-glow); box-shadow: 0 0 8px var(--accent-glow); animation: pulse 1.5s infinite; }
# .dot-done     { background: var(--success); }
# .dot-pending  { background: var(--border); }

# @keyframes pulse {
#     0%, 100% { opacity: 1; }
#     50%       { opacity: 0.4; }
# }

# /* ── Chat ── */
# .chat-container {
#     background: var(--surface);
#     border: 1px solid var(--border);
#     border-radius: 12px;
#     padding: 1.25rem;
#     max-height: 420px;
#     overflow-y: auto;
#     margin-bottom: 1rem;
# }

# .chat-msg {
#     margin-bottom: 1rem;
#     display: flex;
#     flex-direction: column;
#     gap: 0.2rem;
# }

# .chat-label {
#     font-size: 0.65rem;
#     font-weight: 700;
#     letter-spacing: 0.15em;
#     text-transform: uppercase;
# }

# .chat-bubble {
#     display: inline-block;
#     padding: 0.6rem 1rem;
#     border-radius: 10px;
#     font-size: 0.85rem;
#     line-height: 1.6;
#     max-width: 90%;
# }

# .user-label  { color: var(--accent-glow); }
# .bot-label   { color: var(--accent-2); }

# .user-bubble { background: rgba(124,58,237,0.15); border: 1px solid rgba(124,58,237,0.25); align-self: flex-end; }
# .bot-bubble  { background: rgba(6,182,212,0.1);  border: 1px solid rgba(6,182,212,0.2);   align-self: flex-start; }

# /* ── Divider ── */
# hr {
#     border: none !important;
#     border-top: 1px solid var(--border) !important;
#     margin: 1.5rem 0 !important;
# }

# /* ── Transcript box ── */
# .transcript-box {
#     background: var(--surface-2);
#     border: 1px solid var(--border);
#     border-radius: 8px;
#     padding: 1.25rem;
#     font-size: 0.82rem;
#     line-height: 1.8;
#     max-height: 300px;
#     overflow-y: auto;
#     color: var(--text-muted);
#     white-space: pre-wrap;
#     word-break: break-word;
# }

# /* ── Stale Streamlit elements ── */
# .stProgress > div > div > div { background: var(--accent) !important; }
# .stSpinner > div { border-top-color: var(--accent) !important; }
# [data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
# label { color: var(--text-muted) !important; font-size: 0.8rem !important; }

# /* scrollbar */
# ::-webkit-scrollbar { width: 5px; height: 5px; }
# ::-webkit-scrollbar-track { background: var(--bg); }
# ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
# ::-webkit-scrollbar-thumb:hover { background: var(--accent); }
# </style>
# """, unsafe_allow_html=True)

# # ─── Session State Init ──────────────────────────────────────────────────────────
# for key, default in {
#     "result": None,
#     "chat_history": [],
#     "processing": False,
#     "pipeline_done": False,
#     "pipeline_steps": {},
# }.items():
#     if key not in st.session_state:
#         st.session_state[key] = default

# # ─── Helpers ────────────────────────────────────────────────────────────────────
# def step_status(steps: dict, key: str) -> str:
#     s = steps.get(key, "pending")
#     if s == "active":  return "dot-active"
#     if s == "done":    return "dot-done"
#     return "dot-pending"

# def render_step_bar(label: str, key: str, icon: str):
#     css = step_status(st.session_state.pipeline_steps, key)
#     st.markdown(f"""
#     <div class="status-bar">
#         <div class="status-dot {css}"></div>
#         <span>{icon} {label}</span>
#     </div>""", unsafe_allow_html=True)

# # ─── Sidebar ────────────────────────────────────────────────────────────────────
# with st.sidebar:
#     st.markdown('<div class="hero-title" style="font-size:1.6rem">🎬 AI<br>Video</div>', unsafe_allow_html=True)
#     st.markdown('<div class="hero-sub">Meeting Intelligence</div>', unsafe_allow_html=True)
#     st.markdown("---")

#     st.markdown('<span class="badge badge-purple">Input</span>', unsafe_allow_html=True)
#     source = st.text_input("YouTube URL or File Path", placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4")

#     language = st.selectbox("Language", ["english", "hinglish"], index=0)

#     run_btn = st.button("⚡  Analyse", use_container_width=True)

#     if st.session_state.pipeline_done:
#         st.markdown("---")
#         st.markdown('<span class="badge badge-green">Pipeline Status</span>', unsafe_allow_html=True)
#         for step, icon, label in [
#             ("audio",      "🔊", "Audio Processing"),
#             ("transcript", "📝", "Transcription"),
#             ("title",      "🏷️", "Title Generation"),
#             ("summary",    "📋", "Summarisation"),
#             ("extract",    "🔍", "Extraction"),
#             ("rag",        "🧠", "RAG Engine"),
#         ]:
#             render_step_bar(label, step, icon)

# # ─── Main Area ──────────────────────────────────────────────────────────────────
# st.markdown('<div class="hero-title">AI Video Assistant</div>', unsafe_allow_html=True)
# st.markdown('<div class="hero-sub">Transcribe · Summarise · Chat with your meetings</div>', unsafe_allow_html=True)
# st.markdown("---")

# # ── Run Pipeline ────────────────────────────────────────────────────────────────
# if run_btn:
#     if not source.strip():
#         st.error("Please enter a YouTube URL or file path.")
#     else:
#         st.session_state.pipeline_done = False
#         st.session_state.result = None
#         st.session_state.chat_history = []
#         st.session_state.pipeline_steps = {}

#         progress_placeholder = st.empty()

#         def update_step(key, state):
#             st.session_state.pipeline_steps[key] = state

#         try:
#             with progress_placeholder.container():
#                 st.info("⚙️ Pipeline running — see sidebar for live status…")

#             update_step("audio", "active")
#             chunks = process_input(source)
#             update_step("audio", "done")

#             update_step("transcript", "active")
#             transcript = transcribe_all(chunks, language)
#             update_step("transcript", "done")

#             update_step("title", "active")
#             title = generate_title(transcript)
#             update_step("title", "done")

#             update_step("summary", "active")
#             summary = summarize(transcript)
#             update_step("summary", "done")

#             update_step("extract", "active")
#             action_items  = extract_action_items(transcript)
#             decisions     = extract_key_decisions(transcript)
#             questions     = extract_questions(transcript)
#             update_step("extract", "done")

#             update_step("rag", "active")
#             rag_chain = build_rag_chain(transcript)
#             update_step("rag", "done")

#             st.session_state.result = {
#                 "title": title,
#                 "transcript": transcript,
#                 "summary": summary,
#                 "action_items": action_items,
#                 "key_decisions": decisions,
#                 "open_questions": questions,
#                 "rag_chain": rag_chain,
#             }
#             st.session_state.pipeline_done = True
#             progress_placeholder.success("✅ Analysis complete!")
#             time.sleep(0.5)
#             progress_placeholder.empty()
#             st.rerun()

#         except Exception as e:
#             for k in ["audio","transcript","title","summary","extract","rag"]:
#                 if st.session_state.pipeline_steps.get(k) == "active":
#                     st.session_state.pipeline_steps[k] = "pending"
#             progress_placeholder.error(f"❌ Error: {e}")

# # ── Results ──────────────────────────────────────────────────────────────────────
# if st.session_state.result:
#     r = st.session_state.result

#     # Title banner
#     st.markdown(f"""
#     <div class="card">
#         <div class="card-title">📌 Session Title</div>
#         <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;color:var(--text)">
#             {r['title']}
#         </div>
#     </div>""", unsafe_allow_html=True)

#     # Top row: summary + transcript
#     col1, col2 = st.columns([3, 2], gap="medium")

#     with col1:
#         st.markdown(f"""
#         <div class="card">
#             <div class="card-title">📋 Summary</div>
#             <div class="card-content">{r['summary']}</div>
#         </div>""", unsafe_allow_html=True)

#     with col2:
#         with st.expander("📝 Full Transcript", expanded=False):
#             st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>', unsafe_allow_html=True)

#     # Second row: action items | decisions | questions
#     c1, c2, c3 = st.columns(3, gap="medium")

#     with c1:
#         st.markdown(f"""
#         <div class="card">
#             <div class="card-title">✅ Action Items</div>
#             <div class="card-content">{r['action_items']}</div>
#         </div>""", unsafe_allow_html=True)

#     with c2:
#         st.markdown(f"""
#         <div class="card">
#             <div class="card-title">🔑 Key Decisions</div>
#             <div class="card-content">{r['key_decisions']}</div>
#         </div>""", unsafe_allow_html=True)

#     with c3:
#         st.markdown(f"""
#         <div class="card">
#             <div class="card-title">❓ Open Questions</div>
#             <div class="card-content">{r['open_questions']}</div>
#         </div>""", unsafe_allow_html=True)

#     st.markdown("---")

#     # ── RAG Chat ──────────────────────────────────────────────────────────────
#     st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.2rem;font-weight:700;margin-bottom:1rem">💬 Chat with your Meeting</div>', unsafe_allow_html=True)

#     # Chat history display
#     if st.session_state.chat_history:
#         chat_html = '<div class="chat-container">'
#         for msg in st.session_state.chat_history:
#             if msg["role"] == "user":
#                 chat_html += f"""
#                 <div class="chat-msg" style="align-items:flex-end">
#                     <span class="chat-label user-label">You</span>
#                     <div class="chat-bubble user-bubble">{msg['content']}</div>
#                 </div>"""
#             else:
#                 chat_html += f"""
#                 <div class="chat-msg" style="align-items:flex-start">
#                     <span class="chat-label bot-label">🤖 Assistant</span>
#                     <div class="chat-bubble bot-bubble">{msg['content']}</div>
#                 </div>"""
#         chat_html += '</div>'
#         st.markdown(chat_html, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div class="card" style="text-align:center;padding:2rem">
#             <div style="font-size:2rem;margin-bottom:0.5rem">💬</div>
#             <div style="color:var(--text-muted);font-size:0.85rem">Ask anything about your meeting transcript</div>
#         </div>""", unsafe_allow_html=True)

#     # Chat input
#     chat_col1, chat_col2 = st.columns([5, 1], gap="small")
#     with chat_col1:
#         user_input = st.text_input("Your question", placeholder="What were the main decisions made?", label_visibility="collapsed")
#     with chat_col2:
#         send_btn = st.button("Send →", use_container_width=True)

#     if send_btn and user_input.strip():
#         with st.spinner("Thinking…"):
#             answer = ask_question(r["rag_chain"], user_input.strip())
#         st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
#         st.session_state.chat_history.append({"role": "assistant", "content": answer})
#         st.rerun()

#     if st.session_state.chat_history:
#         if st.button("🗑️ Clear Chat", type="secondary"):
#             st.session_state.chat_history = []
#             st.rerun()

# else:
#     # Empty state
#     st.markdown("""
#     <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:5rem 2rem;text-align:center">
#         <div style="font-size:4rem;margin-bottom:1rem">🎬</div>
#         <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:var(--text);margin-bottom:0.5rem">
#             Ready to Analyse
#         </div>
#         <div style="color:var(--text-muted);font-size:0.85rem;max-width:380px;line-height:1.7">
#             Paste a YouTube URL or local file path in the sidebar, choose your language, and hit <strong>Analyse</strong> to get started.
#         </div>
#         <div style="margin-top:2rem;display:flex;gap:1rem;flex-wrap:wrap;justify-content:center">
#             <span class="badge badge-purple">Transcription</span>
#             <span class="badge badge-cyan">Summarisation</span>
#             <span class="badge badge-green">RAG Chat</span>
#         </div>
#     </div>""", unsafe_allow_html=True)
import streamlit as st
import time
from dotenv import load_dotenv

load_dotenv()
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question



# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Video Insights",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg: #0a0a0f;
    --surface: #111118;
    --surface-2: #1a1a25;
    --border: #2a2a3a;
    --accent: #7c3aed;
    --accent-glow: #9f67ff;
    --accent-2: #06b6d4;
    --text: #e8e8f0;
    --text-muted: #7070a0;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background: var(--bg) !important;
}

/* Animated grid background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(124, 58, 237, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(124, 58, 237, 0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
    animation: drift 30s linear infinite;
}

@keyframes drift {
    0%   { background-position: 0 0; }
    100% { background-position: 40px 40px; }
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

/* ── Headings ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
}

/* ── Logo ── */
.logo-wrap {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 0.2rem;
}

.logo-mark {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
    box-shadow: 0 0 18px rgba(124,58,237,0.45);
    animation: float 3.5s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50%      { transform: translateY(-4px) rotate(4deg); }
}

.logo-text {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.25rem;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent-glow) 60%, var(--accent-2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Hero Title ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 800;
    line-height: 1.1;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent-glow) 50%, var(--accent-2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

/* ── Cards ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}

.card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.card-content {
    font-size: 0.875rem;
    line-height: 1.7;
    color: var(--text);
}

/* ── Metric chips ── */
.metric-row { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 1rem; }

.metric-chip {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    flex: 1;
    min-width: 120px;
    transition: border-color 0.2s, transform 0.2s;
}

.metric-chip:hover { border-color: var(--accent-2); transform: translateY(-2px); }

.metric-value {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.3rem;
    color: var(--text);
}

.metric-label {
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
}

/* ── Accent Badge ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.badge-purple { background: rgba(124,58,237,0.2); color: var(--accent-glow); border: 1px solid rgba(124,58,237,0.3); }
.badge-cyan   { background: rgba(6,182,212,0.15); color: var(--accent-2);    border: 1px solid rgba(6,182,212,0.3); }
.badge-green  { background: rgba(16,185,129,0.15); color: var(--success);    border: 1px solid rgba(16,185,129,0.3); }

/* ── Suggestion chips (clickable via st.button styled) ── */
div[data-testid="stHorizontalBlock"] .stButton > button.chip-btn {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 999px !important;
    font-size: 0.72rem !important;
    padding: 0.35rem 0.9rem !important;
    text-transform: none !important;
}

/* ── Input & Buttons ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent), #5b21b6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
}

/* Secondary button */
.stButton > button[kind="secondary"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 0.4rem; }

.stTabs [data-baseweb="tab"] {
    background: var(--surface-2) !important;
    border-radius: 8px 8px 0 0 !important;
    color: var(--text-muted) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1rem !important;
}

.stTabs [aria-selected="true"] {
    background: var(--surface) !important;
    color: var(--accent-glow) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* ── Progress / Status ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    background: var(--surface-2);
    border-radius: 8px;
    margin: 0.4rem 0;
    border: 1px solid var(--border);
    font-size: 0.8rem;
    transition: border-color 0.2s;
}

.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.dot-active   { background: var(--accent-glow); box-shadow: 0 0 8px var(--accent-glow); animation: pulse 1.5s infinite; }
.dot-done     { background: var(--success); }
.dot-pending  { background: var(--border); }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

/* ── Chat ── */
.chat-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
    max-height: 420px;
    overflow-y: auto;
    margin-bottom: 1rem;
}

.chat-msg {
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

.chat-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.chat-bubble {
    display: inline-block;
    padding: 0.6rem 1rem;
    border-radius: 10px;
    font-size: 0.85rem;
    line-height: 1.6;
    max-width: 90%;
}

.user-label  { color: var(--accent-glow); }
.bot-label   { color: var(--accent-2); }

.user-bubble { background: rgba(124,58,237,0.15); border: 1px solid rgba(124,58,237,0.25); align-self: flex-end; }
.bot-bubble  { background: rgba(6,182,212,0.1);  border: 1px solid rgba(6,182,212,0.2);   align-self: flex-start; }

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Transcript box ── */
.transcript-box {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem;
    font-size: 0.82rem;
    line-height: 1.8;
    max-height: 300px;
    overflow-y: auto;
    color: var(--text-muted);
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Stale Streamlit elements ── */
.stProgress > div > div > div { background: linear-gradient(90deg, var(--accent), var(--accent-2)) !important; }
.stSpinner > div { border-top-color: var(--accent) !important; }
[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
label { color: var(--text-muted) !important; font-size: 0.8rem !important; }

/* scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ──────────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "processing": False,
    "pipeline_done": False,
    "pipeline_steps": {},
    "pending_question": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

PIPELINE_STEPS = [
    ("audio",      "🔊", "Audio Processing"),
    ("transcript", "📝", "Transcription"),
    ("title",      "🏷️", "Title Generation"),
    ("summary",    "📋", "Summarisation"),
    ("extract",    "🔍", "Extraction"),
    ("rag",        "🧠", "RAG Engine"),
]

SUGGESTED_QUESTIONS = [
    "What were the main decisions made?",
    "Summarise this in 3 bullet points",
    "Who is responsible for the action items?",
    "What questions were left unanswered?",
]

# ─── Helpers ────────────────────────────────────────────────────────────────────
def step_status(steps: dict, key: str) -> str:
    s = steps.get(key, "pending")
    if s == "active":  return "dot-active"
    if s == "done":    return "dot-done"
    return "dot-pending"

def render_step_bar(label: str, key: str, icon: str):
    css = step_status(st.session_state.pipeline_steps, key)
    st.markdown(f"""
    <div class="status-bar">
        <div class="status-dot {css}"></div>
        <span>{icon} {label}</span>
    </div>""", unsafe_allow_html=True)

def pipeline_progress_fraction(steps: dict) -> float:
    done = sum(1 for k, _, _ in PIPELINE_STEPS if steps.get(k) == "done")
    return done / len(PIPELINE_STEPS)

def render_logo(size_title="1.6rem"):
    st.markdown(f"""
    <div class="logo-wrap">
        <div class="logo-mark">🔮</div>
        <div class="logo-text" style="font-size:{size_title}">Video<br>Insights</div>
    </div>""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    render_logo()
    st.markdown('<div class="hero-sub">Meeting Intelligence</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<span class="badge badge-purple">Input</span>', unsafe_allow_html=True)
    source = st.text_input("YouTube URL or File Path", placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4")

    language = st.selectbox("Language", ["english", "hinglish"], index=0)

    run_btn = st.button("⚡  Analyse", use_container_width=True)

    if st.session_state.result and not st.session_state.get("processing"):
        if st.button("🔄  New Session", use_container_width=True, type="secondary"):
            st.session_state.result = None
            st.session_state.chat_history = []
            st.session_state.pipeline_done = False
            st.session_state.pipeline_steps = {}
            st.rerun()

    if st.session_state.pipeline_steps and not st.session_state.pipeline_done:
        st.markdown("---")
        st.markdown('<span class="badge badge-cyan">Live Progress</span>', unsafe_allow_html=True)
        st.progress(pipeline_progress_fraction(st.session_state.pipeline_steps))
        for step, icon, label in PIPELINE_STEPS:
            render_step_bar(label, step, icon)

    if st.session_state.pipeline_done:
        st.markdown("---")
        st.markdown('<span class="badge badge-green">Pipeline Status</span>', unsafe_allow_html=True)
        st.progress(1.0)
        for step, icon, label in PIPELINE_STEPS:
            render_step_bar(label, step, icon)

# ─── Main Area ──────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Video Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Transcribe · Summarise · Chat with your meetings</div>', unsafe_allow_html=True)
st.markdown("---")

# ── Run Pipeline ────────────────────────────────────────────────────────────────
if run_btn:
    if not source.strip():
        st.error("Please enter a YouTube URL or file path.")
    else:
        st.session_state.pipeline_done = False
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_steps = {}
        st.session_state.processing = True

        progress_placeholder = st.empty()
        bar_placeholder = st.empty()

        def update_step(key, state):
            st.session_state.pipeline_steps[key] = state
            bar_placeholder.progress(pipeline_progress_fraction(st.session_state.pipeline_steps))

        try:
            with progress_placeholder.container():
                st.info("⚙️ Pipeline running — see sidebar for live status…")
            bar_placeholder.progress(0.0)

            update_step("audio", "active")
            chunks = process_input(source)
            update_step("audio", "done")

            update_step("transcript", "active")
            transcript = transcribe_all(chunks, language)
            update_step("transcript", "done")

            update_step("title", "active")
            title = generate_title(transcript)
            update_step("title", "done")

            update_step("summary", "active")
            summary = summarize(transcript)
            update_step("summary", "done")

            update_step("extract", "active")
            action_items  = extract_action_items(transcript)
            decisions     = extract_key_decisions(transcript)
            questions     = extract_questions(transcript)
            update_step("extract", "done")

            update_step("rag", "active")
            rag_chain = build_rag_chain(transcript)
            update_step("rag", "done")

            st.session_state.result = {
                "title": title,
                "transcript": transcript,
                "summary": summary,
                "action_items": action_items,
                "key_decisions": decisions,
                "open_questions": questions,
                "rag_chain": rag_chain,
            }
            st.session_state.pipeline_done = True
            st.session_state.processing = False
            progress_placeholder.success("✅ Analysis complete!")
            st.toast("Analysis complete!", icon="✅")
            time.sleep(0.5)
            progress_placeholder.empty()
            bar_placeholder.empty()
            st.rerun()

        except Exception as e:
            st.session_state.processing = False
            for k, _, _ in PIPELINE_STEPS:
                if st.session_state.pipeline_steps.get(k) == "active":
                    st.session_state.pipeline_steps[k] = "pending"
            progress_placeholder.error(f"❌ Error: {e}")

# ── Results ──────────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # Title banner
    st.markdown(f"""
    <div class="card">
        <div class="card-title">📌 Session Title</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;color:var(--text)">
            {r['title']}
        </div>
    </div>""", unsafe_allow_html=True)

    # Quick metrics
    word_count = len(r["transcript"].split())
    action_count = r["action_items"].count("\n") + 1 if r["action_items"] else 0
    question_count = r["open_questions"].count("\n") + 1 if r["open_questions"] else 0
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-chip"><div class="metric-value">{word_count}</div><div class="metric-label">Words Transcribed</div></div>
        <div class="metric-chip"><div class="metric-value">{action_count}</div><div class="metric-label">Action Items</div></div>
        <div class="metric-chip"><div class="metric-value">{question_count}</div><div class="metric-label">Open Questions</div></div>
        <div class="metric-chip"><div class="metric-value">{language.title()}</div><div class="metric-label">Language</div></div>
    </div>""", unsafe_allow_html=True)

    # Tabbed view instead of static stacked cards
    tab_overview, tab_transcript, tab_chat = st.tabs(["📋 Overview", "📝 Transcript", "💬 Chat"])

    with tab_overview:
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">📋 Summary</div>
                <div class="card-content">{r['summary']}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">✅ Action Items</div>
                <div class="card-content">{r['action_items']}</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">🔑 Key Decisions</div>
                <div class="card-content">{r['key_decisions']}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div class="card-title">❓ Open Questions</div>
            <div class="card-content">{r['open_questions']}</div>
        </div>""", unsafe_allow_html=True)

        st.download_button(
            "⬇️  Download Summary Report",
            data=f"Title: {r['title']}\n\nSummary:\n{r['summary']}\n\nAction Items:\n{r['action_items']}\n\nKey Decisions:\n{r['key_decisions']}\n\nOpen Questions:\n{r['open_questions']}",
            file_name="video_insights_report.txt",
            use_container_width=True,
        )

    with tab_transcript:
        st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>', unsafe_allow_html=True)
        st.download_button(
            "⬇️  Download Transcript",
            data=r["transcript"],
            file_name="transcript.txt",
            use_container_width=True,
        )

    with tab_chat:
        # Chat history display
        if st.session_state.chat_history:
            chat_html = '<div class="chat-container">'
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    chat_html += f"""
                    <div class="chat-msg" style="align-items:flex-end">
                        <span class="chat-label user-label">You</span>
                        <div class="chat-bubble user-bubble">{msg['content']}</div>
                    </div>"""
                else:
                    chat_html += f"""
                    <div class="chat-msg" style="align-items:flex-start">
                        <span class="chat-label bot-label">🤖 Assistant</span>
                        <div class="chat-bubble bot-bubble">{msg['content']}</div>
                    </div>"""
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card" style="text-align:center;padding:2rem">
                <div style="font-size:2rem;margin-bottom:0.5rem">💬</div>
                <div style="color:var(--text-muted);font-size:0.85rem">Ask anything about your meeting transcript</div>
            </div>""", unsafe_allow_html=True)

        # Suggested question chips
        st.markdown('<div style="font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:0.4rem">Try asking</div>', unsafe_allow_html=True)
        chip_cols = st.columns(len(SUGGESTED_QUESTIONS))
        for i, q in enumerate(SUGGESTED_QUESTIONS):
            with chip_cols[i]:
                if st.button(q, key=f"chip_{i}", use_container_width=True):
                    st.session_state.pending_question = q

        # Chat input
        chat_col1, chat_col2 = st.columns([5, 1], gap="small")
        with chat_col1:
            user_input = st.text_input(
                "Your question",
                value=st.session_state.pending_question,
                placeholder="What were the main decisions made?",
                label_visibility="collapsed",
                key="chat_input_box",
            )
        with chat_col2:
            send_btn = st.button("Send →", use_container_width=True)

        if send_btn and user_input.strip():
            with st.spinner("Thinking…"):
                answer = ask_question(r["rag_chain"], user_input.strip())
            st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.session_state.pending_question = ""
            st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat", type="secondary"):
                st.session_state.chat_history = []
                st.rerun()

else:
    # Empty state
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:5rem 2rem;text-align:center">
        <div class="logo-mark" style="width:72px;height:72px;font-size:2.2rem;margin-bottom:1rem">🔮</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:var(--text);margin-bottom:0.5rem">
            Ready to Analyse
        </div>
        <div style="color:var(--text-muted);font-size:0.85rem;max-width:380px;line-height:1.7">
            Paste a YouTube URL or local file path in the sidebar, choose your language, and hit <strong>Analyse</strong> to get started.
        </div>
        <div style="margin-top:2rem;display:flex;gap:1rem;flex-wrap:wrap;justify-content:center">
            <span class="badge badge-purple">Transcription</span>
            <span class="badge badge-cyan">Summarisation</span>
            <span class="badge badge-green">RAG Chat</span>
        </div>
    </div>""", unsafe_allow_html=True)