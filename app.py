import streamlit as st
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent Pipeline",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Mono', monospace; }

.stApp { background: #0a0a0f; color: #e8e4d9; }

[data-testid="stSidebar"] { background: #0f0f18 !important; border-right: 1px solid #1e1e2e; }
[data-testid="stSidebar"] * { color: #e8e4d9 !important; }

.hero-wrap {
    padding: 2.2rem 0 2rem 0;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #1e1e2e;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #7c6af7;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 3.2rem;
    letter-spacing: -0.04em;
    line-height: 1.0;
    margin-bottom: 0.6rem;
    background: linear-gradient(110deg, #f0ebe0 30%, #7c6af7 70%, #3ecf8e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #6b6b7e;
    letter-spacing: 0.08em;
}

.step-card { background: #111119; border: 1px solid #1e1e2e; border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 0.7rem; display: flex; align-items: center; gap: 0.8rem; transition: border-color 0.3s; }
.step-card.active  { border-color: #7c6af7; background: #13131f; }
.step-card.done    { border-color: #3ecf8e; background: #0f1a15; }
.step-card.pending { opacity: 0.45; }
.step-icon { font-size: 1.3rem; }
.step-label { font-family: 'DM Mono', monospace; font-size: 0.82rem; letter-spacing: 0.05em; }
.step-status { margin-left: auto; font-size: 0.72rem; color: #6b6b7e; text-transform: uppercase; letter-spacing: 0.1em; }
.step-card.active  .step-status { color: #7c6af7; }
.step-card.done    .step-status { color: #3ecf8e; }

.output-panel { background: #111119; border: 1px solid #1e1e2e; border-radius: 8px; padding: 1.4rem 1.6rem; margin-top: 1rem; }
.output-panel h4 { font-family: 'Syne', sans-serif; font-size: 0.85rem; letter-spacing: 0.12em; text-transform: uppercase; color: #7c6af7; margin-bottom: 0.8rem; }

.stButton > button { background: #7c6af7 !important; color: #fff !important; border: none !important; border-radius: 6px !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; font-size: 0.95rem !important; letter-spacing: 0.06em !important; padding: 0.65rem 2.2rem !important; transition: background 0.2s, transform 0.15s !important; width: 100% !important; }
.stButton > button:hover { background: #9b8cff !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0px) !important; }

.stTextInput > div > div > input, .stTextArea > div > div > textarea { background: #111119 !important; border: 1px solid #1e1e2e !important; border-radius: 6px !important; color: #e8e4d9 !important; font-family: 'DM Mono', monospace !important; font-size: 0.9rem !important; }
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color: #7c6af7 !important; box-shadow: 0 0 0 2px rgba(124,106,247,0.2) !important; }

.stSelectbox > div > div { background: #111119 !important; border: 1px solid #1e1e2e !important; border-radius: 6px !important; color: #e8e4d9 !important; }

label, .stTextInput label, .stTextArea label, .stSelectbox label { font-family: 'DM Mono', monospace !important; font-size: 0.78rem !important; color: #6b6b7e !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; }

hr { border-color: #1e1e2e !important; }

.score-badge { display: inline-block; background: #1a1a2e; border: 1px solid #7c6af7; border-radius: 4px; padding: 0.3rem 0.8rem; font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800; color: #7c6af7; margin-bottom: 1rem; }

.err-box { background: #1a0f0f; border: 1px solid #cf3e3e; border-radius: 8px; padding: 1rem 1.2rem; color: #ff6b6b; font-size: 0.85rem; }

.scroll-box { max-height: 340px; overflow-y: auto; padding-right: 0.4rem; }
.scroll-box::-webkit-scrollbar { width: 4px; }
.scroll-box::-webkit-scrollbar-track { background: #0a0a0f; }
.scroll-box::-webkit-scrollbar-thumb { background: #2a2a3e; border-radius: 2px; }

[data-testid="stToolbar"] { display: none !important; }
</style>
""",
    unsafe_allow_html=True,
)


# ── Session state defaults ─────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "pipeline_run": False,
        "current_step": None,
        "search_results": None,
        "scraped_content": None,
        "report": None,
        "critic_review": None,
        "error": None,
        "last_topic": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init_state()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📋 Pipeline Steps")

    STEPS = [
        ("🔍", "Search Agent", "search"),
        ("📄", "Reader Agent", "reader"),
        ("✍️", "Writer Chain", "writer"),
        ("🧐", "Critic Agent", "critic"),
    ]

    cs = st.session_state.current_step
    for icon, label, key in STEPS:
        if cs == key + "_start":
            state_cls, status = "active", "running…"
        elif (
            cs
            and cs != "done"
            and cs.split("_")[0] in [s[2] for s in STEPS]
            and STEPS.index((icon, label, key))
            < [s[2] for s in STEPS].index(cs.split("_")[0])
        ):
            state_cls, status = "done", "done"
        else:
            step_end_reached = st.session_state.get(key + "_done", False)
            if step_end_reached:
                state_cls, status = "done", "done"
            else:
                state_cls, status = "pending", "waiting"

        st.markdown(
            f"""
        <div class="step-card {state_cls}">
            <span class="step-icon">{icon}</span>
            <span class="step-label">{label}</span>
            <span class="step-status">{status}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    if st.session_state.pipeline_run:
        if st.button("🔄 Reset Pipeline"):
            for k in [
                "pipeline_run",
                "current_step",
                "search_results",
                "scraped_content",
                "report",
                "critic_review",
                "error",
                "last_topic",
                "search_done",
                "reader_done",
                "writer_done",
                "critic_done",
            ]:
                st.session_state[k] = None if k != "pipeline_run" else False
            st.rerun()


# ── Main area ──────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero-wrap">
    <div class="hero-eyebrow">🔬 Multi-Agent Research System</div>
    <div class="hero-title">ResearchMind</div>
    <div class="hero-sub">Search &nbsp;·&nbsp; Read &nbsp;·&nbsp; Write &nbsp;·&nbsp; Critique — fully autonomous</div>
</div>
""",
    unsafe_allow_html=True,
)

topic = st.text_input(
    "Research Topic",
    placeholder="e.g. Quantum computing breakthroughs in 2025",
    value=st.session_state.last_topic,
)

run_col, _ = st.columns([1, 3])
with run_col:
    run_btn = st.button(
        "▶  Run Pipeline",
        disabled=st.session_state.pipeline_run
        and st.session_state.current_step is not None,
    )


# ── Pipeline execution ─────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.markdown(
            '<div class="err-box">⚠️ Please enter a research topic before running.</div>',
            unsafe_allow_html=True,
        )
    else:
        for k in [
            "search_results",
            "scraped_content",
            "report",
            "critic_review",
            "error",
            "search_done",
            "reader_done",
            "writer_done",
            "critic_done",
        ]:
            st.session_state[k] = None
        st.session_state.pipeline_run = True
        st.session_state.last_topic = topic
        st.session_state.current_step = "search_start"

        try:
            from pipeline import run_research_pipeline

            status_placeholder = st.empty()

            for progress in run_research_pipeline(topic):
                step = progress.get("step", "")
                state = progress.get("state", {})
                st.session_state.current_step = step

                if step == "search_start":
                    status_placeholder.info("🔍 Search Agent is gathering information…")
                elif step == "search_end":
                    st.session_state.search_results = state.get("search_results")
                    st.session_state.search_done = True
                    status_placeholder.info(
                        "📄 Reader Agent is extracting content from URLs…"
                    )
                elif step == "reader_end":
                    st.session_state.scraped_content = state.get("scraped_content")
                    st.session_state.reader_done = True
                    status_placeholder.info("✍️ Writer Chain is generating the report…")
                elif step == "writer_end":
                    st.session_state.report = state.get("report")
                    st.session_state.writer_done = True
                    status_placeholder.info("🧐 Critic Agent is reviewing the report…")
                elif step == "critic_end":
                    st.session_state.critic_review = state.get("critic_review")
                    st.session_state.critic_done = True
                    status_placeholder.success("✅ Pipeline complete!")

            st.session_state.current_step = "done"

        except ImportError as e:
            st.session_state.error = f"Import error — make sure pipeline.py and agent.py are in the same directory.\n\nDetails: {e}"
            st.session_state.pipeline_run = False
        except Exception as e:
            st.session_state.error = f"Pipeline error: {e}"
            st.session_state.pipeline_run = False

        st.rerun()


# ── Error display ──────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(
        f'<div class="err-box">❌ {st.session_state.error}</div>',
        unsafe_allow_html=True,
    )


# ── Results display ────────────────────────────────────────────────────────────
if (
    st.session_state.search_results
    or st.session_state.report
    or st.session_state.critic_review
):
    st.markdown("---")
    st.markdown("### 📊 Pipeline Output")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🔍 Search Results", "📄 Scraped Content", "📝 Report", "🧐 Critic Review"]
    )

    with tab1:
        if st.session_state.search_results:
            st.markdown(
                '<div class="output-panel"><h4>Search Results</h4>',
                unsafe_allow_html=True,
            )
            st.markdown('<div class="scroll-box">', unsafe_allow_html=True)
            st.markdown(st.session_state.search_results)
            st.markdown("</div></div>", unsafe_allow_html=True)
        else:
            st.caption("Waiting for search results…")

    with tab2:
        if st.session_state.scraped_content:
            st.markdown(
                '<div class="output-panel"><h4>Scraped Web Content</h4>',
                unsafe_allow_html=True,
            )
            st.markdown('<div class="scroll-box">', unsafe_allow_html=True)
            st.markdown(st.session_state.scraped_content)
            st.markdown("</div></div>", unsafe_allow_html=True)
        else:
            st.caption("Waiting for scraped content…")

    with tab3:
        if st.session_state.report:
            st.markdown(
                '<div class="output-panel"><h4>Generated Research Report</h4>',
                unsafe_allow_html=True,
            )
            st.markdown(st.session_state.report)
            st.markdown("</div>", unsafe_allow_html=True)
            st.download_button(
                label="⬇️ Download Report (.md)",
                data=st.session_state.report,
                file_name=f"report_{st.session_state.last_topic[:30].replace(' ','_')}.md",
                mime="text/markdown",
            )
        else:
            st.caption("Report will appear here after the writer step…")

    with tab4:
        if st.session_state.critic_review:
            review_text = str(st.session_state.critic_review)
            import re

            score_match = re.search(r"Score:\s*(\d+)/10", review_text)
            if score_match:
                score = score_match.group(1)
                st.markdown(
                    f'<div class="score-badge">Score: {score}/10</div>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                '<div class="output-panel"><h4>Critic Review</h4>',
                unsafe_allow_html=True,
            )
            st.markdown(review_text)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.caption("Critic review will appear here after the final step…")


# ── Welcome state ──────────────────────────────────────────────────────────────
elif not st.session_state.pipeline_run:
    st.markdown(
        """
    <div style="margin-top:2rem; padding: 2rem; background:#111119; border:1px solid #1e1e2e; border-radius:10px; color:#6b6b7e; font-size:0.85rem; line-height:1.8;">
        <strong style="color:#e8e4d9; font-family:'Syne',sans-serif; font-size:1rem;">How it works</strong><br><br>
        1. &nbsp;Enter your <strong style="color:#7c6af7;">research topic</strong> in the field above<br>
        2. &nbsp;Click <strong style="color:#7c6af7;">Run Pipeline</strong> to kick off the multi-agent flow<br>
        3. &nbsp;Watch as the <strong style="color:#3ecf8e;">Search → Reader → Writer → Critic</strong> agents work in sequence<br>
        4. &nbsp;Download your polished research report when done
    </div>
    """,
        unsafe_allow_html=True,
    )
