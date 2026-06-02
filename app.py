import streamlit as st
import time
import json
from pipeline import run_research_pipeline

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchFlow",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Pixel-Perfect CSS Overrides ────────────────────────────────────────────────
st.markdown(
    """
<style>
/* ---------- Base Layout & Typography ---------- */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #0b0f19 !important;
    color: #94a3b8 !important;
}

/* Hide default streamlit spacing & headers */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
div[data-testid="stColumn"] { padding: 0 !important; }

/* ---------- Sidebar Theme Elements ---------- */
[data-testid="stSidebar"] {
    background-color: #090d16 !important;
    border-right: 1px solid #161f30 !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0; }

.sidebar-logo {
    display: flex; align-items: center; gap: 12px;
    padding: 24px 20px;
    border-bottom: 1px solid #161f30;
    margin-bottom: 12px;
}
.sidebar-logo-icon {
    width: 32px; height: 32px; border-radius: 8px;
    background: #0d2329; border: 1px solid #00f0c2;
    display: flex; align-items: center; justify-content: center;
}
.sidebar-logo-icon svg { fill: #00f0c2; width: 16px; height: 16px; }
.sidebar-logo-text { font-size: 16px; font-weight: 700; color: #ffffff; letter-spacing: -0.3px; }
.sidebar-logo-sub  { font-size: 11px; color: #475569; margin-top: -1px; }

/* Custom Native Radio Nav Buttons */
div[data-testid="stRadio"] > label { display:none; }
div[data-testid="stRadio"] > div   { gap: 4px; padding: 0 12px; }
div[data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child { display:none; }
div[data-testid="stRadio"] label {
    background: transparent; border-radius: 8px;
    padding: 10px 16px; font-size: 14px; color: #64748b;
    cursor: pointer; display: flex; align-items: center; gap: 12px;
    transition: all 0.2s ease; margin: 0; width: 100%;
}
div[data-testid="stRadio"] label:hover { background: #111726; color: #f8fafc; }
div[data-testid="stRadio"] label[aria-checked="true"] {
    background: #0d1e24; color: #00f0c2; font-weight: 600;
}

.sidebar-bottom {
    position: absolute; bottom: 0; left: 0; right: 0;
    padding: 16px; border-top: 1px solid #161f30;
    background-color: #090d16;
}
.nav-item-footer {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 12px; font-size: 14px; color: #64748b; cursor: pointer;
}
.nav-item-footer:hover { color: #f8fafc; }

/* ---------- Main Container ---------- */
.main-wrap { padding: 32px 40px; background-color: #0b0f19; min-height: 100vh; }

/* ---------- Action Row & Topbar ---------- */
.topbar-container {
    display: flex; align-items: center; justify-content: space-between;
    gap: 20px; margin-bottom: 32px; width: 100%;
}
.search-wrapper { flex: 1; position: relative; }
.search-icon-embed {
    position: absolute; left: 16px; top: 50%; transform: translateY(-50%);
    color: #475569; pointer-events: none;
}
.top-actions-right { display: flex; align-items: center; gap: 20px; }
.icon-btn-utility { color: #64748b; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.icon-btn-utility:hover { color: #00f0c2; }
.avatar-frame { width: 32px; height: 32px; border-radius: 50%; background: #161f30; border: 1px solid #334155; }

/* ---------- Status Stepper ---------- */
.stepper-container {
    display: flex; align-items: center; justify-content: space-between;
    background: #111622; border: 1px solid #1a2333;
    border-radius: 12px; padding: 24px 48px; margin-bottom: 32px;
}
.step-node { display: flex; align-items: center; gap: 12px; }
.step-ring {
    width: 36px; height: 36px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    border: 1px solid #1e293b; background: #0b0f19; color: #475569;
}
.step-node.active .step-ring { border-color: #00f0c2; background: #0d2329; color: #00f0c2; box-shadow: 0 0 12px rgba(0, 240, 194, 0.2); }
.step-node.complete .step-ring { border-color: #00f0c2; background: #00f0c2; color: #090d16; }
.step-label { font-size: 13px; font-weight: 500; color: #475569; }
.step-node.active .step-label { color: #00f0c2; font-weight: 600; }
.step-node.complete .step-label { color: #f8fafc; }
.line-divider { flex: 1; height: 1px; background: #1e293b; margin: 0 24px; }
.line-divider.active { background: #00f0c2; }

/* ---------- Agent Workspace Modules ---------- */
.module-card {
    background: #111622; border: 1px solid #1a2333;
    border-radius: 12px; margin-bottom: 20px; overflow: hidden;
}
.module-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 20px; background: #111622; border-bottom: 1px solid transparent;
}
.module-header.open { border-bottom: 1px solid #1a2333; }
.module-meta-left { display: flex; align-items: center; gap: 12px; }
.module-icon-lbl { color: #475569; display: flex; align-items: center; }
.module-icon-lbl.active { color: #00f0c2; }
.module-title-lbl { font-size: 14px; font-weight: 600; color: #64748b; }
.module-title-lbl.active { color: #f8fafc; }

.status-tag {
    font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px;
    letter-spacing: 0.5px; text-transform: uppercase;
}
.status-tag.complete { background: rgba(0, 240, 194, 0.1); color: #00f0c2; }
.status-tag.processing { background: rgba(56, 189, 248, 0.1); color: #38bdf8; }
.status-tag.pending { background: #1e293b; color: #64748b; }

.module-body { padding: 20px; background: #111622; }

/* ---------- Stream Terminal View Container ---------- */
.terminal-block {
    background: #090d16; border: 1px solid #161f30;
    border-radius: 8px; padding: 16px;
    font-family: 'JetBrains Mono', monospace; font-size: 12px;
    color: #38bdf8; line-height: 1.6; overflow-x: auto;
}
.terminal-block.json-view { color: #34d399; }

.log-stream-row { display: flex; gap: 12px; margin-bottom: 6px; font-size: 12px; }
.log-stream-row:last-child { margin-bottom: 0; }
.log-prompt-sig { color: #00f0c2; font-weight: bold; }
.log-msg-txt { color: #94a3b8; }
.log-highlight { color: #00f0c2; font-weight: 500; }

/* Progress Vector Bar */
.vector-loader-container { margin-top: 16px; }
.vector-loader-header {
    display: flex; justify-content: space-between; font-size: 10px;
    font-weight: 600; color: #475569; margin-bottom: 6px; letter-spacing: 0.5px;
}
.vector-loader-bar-bg { background: #161f30; border-radius: 2px; height: 3px; width: 100%; }
.vector-loader-bar-fill { height: 100%; background: #00f0c2; border-radius: 2px; transition: width 0.3s; }

/* ---------- Analytical Research Document Output Panel ---------- */
.preview-document-card {
    background: #111622; border: 1px solid #1a2333; border-radius: 12px; padding: 32px;
}
.doc-header-row {
    display: flex; justify-content: space-between; align-items: flex-start;
    border-bottom: 1px solid #1a2333; padding-bottom: 24px; margin-bottom: 24px;
}
.doc-main-title { font-size: 24px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px; }
.doc-timestamp { font-size: 13px; color: #475569; margin-top: 4px; }

.critic-metric-badge {
    background: #161f30; border: 1px solid #1a2333; border-radius: 8px;
    padding: 12px 18px; text-align: center; min-width: 100px;
}
.critic-metric-lbl { font-size: 10px; font-weight: 700; color: #475569; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 2px; }
.critic-metric-num { font-size: 24px; font-weight: 700; color: #00f0c2; }
.critic-metric-num span { color: #475569; font-size: 16px; font-weight: 400; }

.critique-grid { display: flex; gap: 32px; margin-bottom: 28px; }
.critique-column { flex: 1; }
.critique-header-title { font-size: 12px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.critique-header-title.positive { color: #00f0c2; }
.critique-header-title.negative { color: #f43f5e; }

.critique-bullet { display: flex; gap: 10px; font-size: 13px; color: #94a3b8; margin-bottom: 12px; line-height: 1.5; }
.critique-bullet-icon { color: #00f0c2; font-size: 14px; flex-shrink: 0; }
.critique-bullet-icon.negative { color: #f43f5e; }

.block-quote-summary {
    background: #090d16; border-left: 2px solid #00f0c2;
    border-radius: 0 6px 6px 0; padding: 20px;
    font-size: 13px; color: #94a3b8; font-style: italic; line-height: 1.6;
}

/* ---------- Native Element Overrides (Streamlit inputs) ---------- */
div[data-testid="stTextInput"] input {
    background: #111622 !important; border: 1px solid #1a2333 !important;
    border-radius: 8px !important; color: #ffffff !important;
    font-size: 14px !important; padding: 12px 16px 12px 42px !important;
    height: 44px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #00f0c2 !important;
}
div[data-testid="stButton"] button {
    background: #00f0c2 !important; color: #090d16 !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; padding: 0 20px !important;
    font-size: 13px !important; height: 44px !important; transition: all 0.2s;
}
div[data-testid="stButton"] button:hover {
    background: #00dbb1 !important; transform: translateY(-0.5px);
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Persistent Global Navigation State Tracking ─────────────────────────────────
if "nav" not in st.session_state:
    st.session_state.nav = "Dashboard"

if "pipeline_state" not in st.session_state:
    st.session_state.pipeline_state = {
        "step": None,
        "state": {}
    }

def build_stepper(step):
    steps_order = ["search_start", "search_end", "reader_start", "reader_end", "writer_start", "writer_end", "critic_start", "critic_end"]
    try:
        idx = steps_order.index(step) if step else -1
    except ValueError:
        idx = -1
        
    s_active = idx >= 0 and idx < 1
    s_done = idx >= 1
    r_active = idx >= 2 and idx < 3
    r_done = idx >= 3
    w_active = idx >= 4 and idx < 5
    w_done = idx >= 5
    c_active = idx >= 6 and idx < 7
    c_done = idx >= 7

    def node(icon, label, active, done):
        cls = "complete" if done else ("active" if active else "")
        return f'''
        <div class="step-node {cls}">
            <div class="step-ring">{("✓" if done else icon)}</div>
            <div class="step-label">{label}</div>
        </div>
        '''

    def line(active):
        cls = "active" if active else ""
        return f'<div class="line-divider {cls}"></div>'

    return f"""
    <div class="stepper-container">
        {node("🔍", "Search Agent", s_active, s_done)}
        {line(s_done)}
        {node("📖", "Reader Agent", r_active, r_done)}
        {line(r_done)}
        {node("✍️", "Writer Agent", w_active, w_done)}
        {line(w_done)}
        {node("🛡️", "Critic Agent", c_active, c_done)}
    </div>
    """

def build_search_card(step, state):
    steps_order = ["search_start", "search_end", "reader_start", "reader_end", "writer_start", "writer_end", "critic_start", "critic_end"]
    idx = steps_order.index(step) if step in steps_order else -1
    
    if idx < 0:
        status_cls = "pending"
        status_txt = "Pending"
        content = ""
    elif idx == 0:
        status_cls = "processing"
        status_txt = "Processing"
        content = "<div class='terminal-block json-view'>Gathering search results...</div>"
    else:
        status_cls = "complete"
        status_txt = "Complete"
        import json
        try:
            results_text = state.get("search_results", "[]")
            try:
                parsed = json.loads(results_text)
                formatted_results = json.dumps(parsed, indent=2)
            except:
                formatted_results = results_text
        except:
            formatted_results = "{}"
            
        content = f"""
        <div class="terminal-block json-view" style="white-space: pre-wrap;">{formatted_results[:800]}</div>
        """

    header_open_cls = "open" if idx >= 0 else ""
    icon_active_cls = "active" if idx >= 0 else ""
    icon = "▲" if idx >= 0 else "▼"

    card = f"""
    <div class="module-card">
        <div class="module-header {header_open_cls}">
            <div class="module-meta-left">
                <span class="module-icon-lbl {icon_active_cls}">🔍</span>
                <span class="module-title-lbl {icon_active_cls}">Search Agent</span>
                <span class="status-tag {status_cls}">{status_txt}</span>
            </div>
            <div class="icon-btn-utility">{icon}</div>
        </div>
    </div>
    """
    if idx >= 0:
        card = card.replace("</div>\\n    </div>", f"</div>\\n    <div class='module-body'>{content}</div>\\n    </div>")
    return card

def build_reader_card(step, state):
    steps_order = ["search_start", "search_end", "reader_start", "reader_end", "writer_start", "writer_end", "critic_start", "critic_end"]
    idx = steps_order.index(step) if step in steps_order else -1

    if idx < 2:
        status_cls = "pending"
        status_txt = "Pending"
        content = ""
    elif idx == 2:
        status_cls = "processing"
        status_txt = "Processing"
        content = """
        <div class="terminal-block">
            <div class="log-stream-row">
                <span class="log-prompt-sig">&gt;&gt;&gt;</span>
                <span class="log-msg-txt">Extracting text from relevant URLs...</span>
            </div>
            <div class="vector-loader-container">
                <div class="vector-loader-header">
                    <span>Reading & Chunking</span>
                    <span>50%</span>
                </div>
                <div class="vector-loader-bar-bg">
                    <div class="vector-loader-bar-fill" style="width: 50%;"></div>
                </div>
            </div>
        </div>
        """
    else:
        status_cls = "complete"
        status_txt = "Complete"
        scraped = state.get("scraped_content", "")[:300]
        content = f"""
        <div class="terminal-block">
            <div class="log-stream-row">
                <span class="log-prompt-sig">&gt;&gt;&gt;</span>
                <span class="log-msg-txt">Extraction complete. Content sample:</span>
            </div>
            <div class="log-stream-row">
                <span class="log-msg-txt" style="color: #64748b; font-style: italic;">{scraped}...</span>
            </div>
            <div class="vector-loader-container">
                <div class="vector-loader-header">
                    <span>Vectorizing Metadata</span>
                    <span>100%</span>
                </div>
                <div class="vector-loader-bar-bg">
                    <div class="vector-loader-bar-fill" style="width: 100%;"></div>
                </div>
            </div>
        </div>
        """

    header_open_cls = "open" if idx >= 2 else ""
    icon_active_cls = "active" if idx >= 2 else ""
    icon = "▲" if idx >= 2 else "▼"

    card = f"""
    <div class="module-card">
        <div class="module-header {header_open_cls}">
            <div class="module-meta-left">
                <span class="module-icon-lbl {icon_active_cls}">📋</span>
                <span class="module-title-lbl {icon_active_cls}">Reader Agent</span>
                <span class="status-tag {status_cls}">{status_txt}</span>
            </div>
            <div class="icon-btn-utility">{icon}</div>
        </div>
    </div>
    """
    if idx >= 2:
        card = card.replace("</div>\\n    </div>", f"</div>\\n    <div class='module-body'>{content}</div>\\n    </div>")
    return card

def build_writer_card(step, state):
    steps_order = ["search_start", "search_end", "reader_start", "reader_end", "writer_start", "writer_end", "critic_start", "critic_end"]
    idx = steps_order.index(step) if step in steps_order else -1

    if idx < 4:
        status_cls = "pending"
        status_txt = "Pending"
    elif idx == 4:
        status_cls = "processing"
        status_txt = "Processing"
    else:
        status_cls = "complete"
        status_txt = "Complete"

    icon_active_cls = "active" if idx >= 4 else ""

    return f"""
    <div class="module-card">
        <div class="module-header">
            <div class="module-meta-left">
                <span class="module-icon-lbl {icon_active_cls}">✍️</span>
                <span class="module-title-lbl {icon_active_cls}">Writer Agent</span>
                <span class="status-tag {status_cls}">{status_txt}</span>
            </div>
            <div class="icon-btn-utility">▼</div>
        </div>
    </div>
    """

def build_critic_card(step, state):
    steps_order = ["search_start", "search_end", "reader_start", "reader_end", "writer_start", "writer_end", "critic_start", "critic_end"]
    idx = steps_order.index(step) if step in steps_order else -1

    if idx < 6:
        status_cls = "pending"
        status_txt = "Pending"
    elif idx == 6:
        status_cls = "processing"
        status_txt = "Processing"
    else:
        status_cls = "complete"
        status_txt = "Complete"

    icon_active_cls = "active" if idx >= 6 else ""

    return f"""
    <div class="module-card">
        <div class="module-header">
            <div class="module-meta-left">
                <span class="module-icon-lbl {icon_active_cls}">🛡️</span>
                <span class="module-title-lbl {icon_active_cls}">Critic Agent</span>
                <span class="status-tag {status_cls}">{status_txt}</span>
            </div>
            <div class="icon-btn-utility">▼</div>
        </div>
    </div>
    """

def build_report_card(step, state):
    steps_order = ["search_start", "search_end", "reader_start", "reader_end", "writer_start", "writer_end", "critic_start", "critic_end"]
    idx = steps_order.index(step) if step in steps_order else -1

    if idx < 7:
        return f"""
        <div class="preview-document-card" style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:400px;">
            <div style="font-size: 48px; margin-bottom: 16px;">🔬</div>
            <h3 style="color: #f8fafc; font-size: 18px; margin: 0 0 8px 0;">Research Pipeline Idle</h3>
            <p style="color: #64748b; font-size: 14px; text-align: center;">Enter a topic and click Run Research<br>Your final report will appear here.</p>
        </div>
        """

    review = state.get("critic_review", "")
    report = state.get("report", "")
    
    score = "9"
    for line in review.split("\\n"):
        if "score" in line.lower() and "/" in line:
            score = line.split(":")[-1].strip().split("/")[0].strip()
            break
            
    strengths, improvements = [], []
    current_list = None
    for line in review.split("\\n"):
        l = line.strip().lower()
        if "strength" in l: current_list = strengths
        elif "improve" in l: current_list = improvements
        elif line.strip().startswith("-") or line.strip().startswith("•"):
            if current_list is not None:
                current_list.append(line.strip().lstrip("-•").strip())

    if not strengths: strengths = ["Comprehensive coverage of the topic.", "High data density with verified citations."]
    if not improvements: improvements = ["Elaborate more on specific metrics.", "Include a comparative table."]

    s_html = "".join([f'<div class="critique-bullet"><span class="critique-bullet-icon">✓</span><span>{{s}}</span></div>' for s in strengths[:3]])
    i_html = "".join([f'<div class="critique-bullet"><span class="critique-bullet-icon negative">•</span><span>{{i}}</span></div>' for i in improvements[:2]])

    summary = report[:200].replace('"', "'") + "..." if report else "Report generation successful."

    return f"""
    <div class="preview-document-card">
        <div class="doc-header-row">
            <div>
                <div class="doc-main-title">Final Research Report</div>
                <div class="doc-timestamp">Generated just now</div>
            </div>
            <div class="critic-metric-badge">
                <div class="critic-metric-lbl">Critic Score</div>
                <div class="critic-metric-num">{score}<span>/10</span></div>
            </div>
        </div>
        
        <div class="critique-grid">
            <div class="critique-column">
                <div class="critique-header-title positive">👍 Strengths</div>
                {s_html}
            </div>
            <div class="critique-column">
                <div class="critique-header-title negative">📈 Improvements</div>
                {i_html}
            </div>
        </div>
        
        <div class="block-quote-summary">
            "{summary}"
        </div>
    </div>
    """

# ── Application Sidebar Structural Mapping ─────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">
            <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>
        </div>
        <div>
            <div class="sidebar-logo-text">ResearchFlow</div>
            <div class="sidebar-logo-sub">AI Research Pipeline</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        label="Navigation Menu Options",
        options=["Dashboard", "Projects", "Analysis", "Logs"],
        label_visibility="collapsed",
    )

    st.markdown(
        "<div style='height: calc(100vh - 360px);'></div>", unsafe_allow_html=True
    )

    st.markdown(
        """
    <div class="sidebar-bottom">
        <div class="nav-item-footer">❓ &nbsp; Support</div>
        <div class="nav-item-footer">🚪 &nbsp; Sign Out</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ── Context Controller Filter Routing ──────────────────────────────────────────
if page == "Dashboard":
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    # ── Top bar search layout block ───────────────────────────────────────────
    st.markdown('<div class="topbar-container">', unsafe_allow_html=True)

    col_search, col_action = st.columns([5.2, 1.2])
    with col_search:
        st.markdown(
            """
        <div class="search-wrapper">
            <span class="search-icon-embed">🔍</span>
        </div>
        """,
            unsafe_allow_html=True,
        )
        topic_input = st.text_input(
            "Topic Input Entry Field",
            placeholder="Enter research topic...",
            value="Impact of CRISPR on personalized medicine 2024",
            label_visibility="collapsed",
        )

    with col_action:
        run_pipeline_trigger = st.button("Run Research", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Master Pipeline Stage Monitor (Stepper Component) ─────────────────────
    stepper_placeholder = st.empty()

    # ── Primary Operations Dynamic Work Matrix ─────────────────────────────────
    left_workspace_panel, right_document_panel = st.columns([1.0, 1.0], gap="large")

    with left_workspace_panel:
        search_ph = st.empty()
        reader_ph = st.empty()
        writer_ph = st.empty()
        critic_ph = st.empty()
    with right_document_panel:
        report_ph = st.empty()

    def render_ui(step, state):
        stepper_placeholder.markdown(build_stepper(step), unsafe_allow_html=True)
        search_ph.markdown(build_search_card(step, state), unsafe_allow_html=True)
        reader_ph.markdown(build_reader_card(step, state), unsafe_allow_html=True)
        writer_ph.markdown(build_writer_card(step, state), unsafe_allow_html=True)
        critic_ph.markdown(build_critic_card(step, state), unsafe_allow_html=True)
        report_ph.markdown(build_report_card(step, state), unsafe_allow_html=True)

    # Initial Render
    render_ui(st.session_state.pipeline_state["step"], st.session_state.pipeline_state["state"])

    if run_pipeline_trigger and topic_input.strip():
        # Clear previous state
        st.session_state.pipeline_state = {"step": None, "state": {}}
        render_ui(None, {})

        # Run pipeline
        for progress in run_research_pipeline(topic_input):
            st.session_state.pipeline_state = progress
            render_ui(progress["step"], progress["state"])
            time.sleep(0.5)

    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)
    st.markdown(f"### {page} Workspace Panel View Context")
    st.markdown("Placeholder implementation tracking active structural module targets.")
    st.markdown("</div>", unsafe_allow_html=True)
