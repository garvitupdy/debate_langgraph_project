import streamlit as st
from graph import create_debate_graph

st.set_page_config(
    page_title="AI Debate Arena",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

    /* ── Global Reset & Base ── */
    html, body, [data-testid="stAppViewContainer"] {
        background: #0d0d14 !important;
    }
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(ellipse at 20% 10%, #1a1035 0%, #0d0d14 45%, #0d1420 100%) !important;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    
    * { box-sizing: border-box; }

    /* Animated noise grain overlay */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
        opacity: 0.5;
    }

    /* ── Typography ── */
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', Georgia, serif !important;
    }
    p, span, div, label, button {
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Hero Title ── */
    .arena-hero {
        text-align: center;
        padding: 60px 20px 20px;
        position: relative;
    }
    .arena-hero .eyebrow {
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #8b7cf6;
        margin-bottom: 16px;
        display: block;
    }
    .arena-hero h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: clamp(42px, 7vw, 80px);
        font-weight: 900;
        font-style: italic;
        line-height: 1.05;
        margin: 0 0 20px;
        background: linear-gradient(135deg, #e8e0ff 0%, #c4b5fd 30%, #f0abfc 65%, #fbbf24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 0 40px rgba(139, 92, 246, 0.3));
    }
    .arena-hero .subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 16px;
        font-weight: 300;
        color: #6b7280;
        letter-spacing: 0.5px;
        max-width: 480px;
        margin: 0 auto;
        line-height: 1.7;
    }

    /* ── Glowing Divider ── */
    .glow-divider {
        width: 100%;
        height: 1px;
        background: linear-gradient(90deg, transparent, #7c3aed44, #7c3aed99, #7c3aed44, transparent);
        margin: 32px 0;
        position: relative;
    }
    .glow-divider::after {
        content: '⚔';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #0d0d14;
        color: #7c3aed;
        font-size: 14px;
        padding: 0 12px;
    }

    /* ── Input Section ── */
    .input-section {
        background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 32px 36px;
        margin-bottom: 32px;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    .input-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139,92,246,0.6), transparent);
    }

    /* ── Streamlit Input Override ── */
    [data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(139,92,246,0.3) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 15px !important;
        padding: 14px 18px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 0 0 rgba(139,92,246,0) !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: rgba(139,92,246,0.7) !important;
        box-shadow: 0 0 0 3px rgba(139,92,246,0.15) !important;
        background: rgba(255,255,255,0.06) !important;
    }
    [data-testid="stTextInput"] input::placeholder {
        color: #4b5563 !important;
    }
    [data-testid="stTextInput"] label {
        color: #9ca3af !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        font-family: 'DM Mono', monospace !important;
    }

    /* ── Buttons ── */
    [data-testid="stButton"] button {
        border-radius: 12px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        letter-spacing: 0.5px !important;
        padding: 12px 24px !important;
        transition: all 0.25s ease !important;
        border: none !important;
        cursor: pointer !important;
    }
    [data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed, #9333ea, #a855f7) !important;
        color: #fff !important;
        box-shadow: 0 4px 24px rgba(124, 58, 237, 0.45), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    }
    [data-testid="stButton"] button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(124, 58, 237, 0.6), inset 0 1px 0 rgba(255,255,255,0.2) !important;
    }
    [data-testid="stButton"] button[kind="primary"]:active {
        transform: translateY(0px) !important;
    }
    [data-testid="stButton"] button:not([kind="primary"]) {
        background: rgba(255,255,255,0.05) !important;
        color: #9ca3af !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    [data-testid="stButton"] button:not([kind="primary"]):hover {
        background: rgba(255,255,255,0.08) !important;
        color: #e2e8f0 !important;
        transform: translateY(-1px) !important;
    }

    /* ── Spinner ── */
    [data-testid="stSpinner"] {
        color: #8b5cf6 !important;
    }
    [data-testid="stSpinner"] > div {
        border-color: #8b5cf6 transparent transparent transparent !important;
    }

    /* ── Round Badge ── */
    .round-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        margin: 40px 0 28px;
    }
    .round-badge .line {
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1));
    }
    .round-badge .line.right {
        background: linear-gradient(90deg, rgba(255,255,255,0.1), transparent);
    }
    .round-badge .label {
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #6d28d9;
        background: rgba(109,40,217,0.12);
        border: 1px solid rgba(109,40,217,0.3);
        padding: 6px 20px;
        border-radius: 100px;
    }

    /* ── Debate Cards ── */
    .debate-card {
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        animation: cardReveal 0.5s ease forwards;
    }
    @keyframes cardReveal {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .debate-card:hover {
        transform: translateY(-2px);
    }

    /* Pro Card (Blue) */
    .pro-card {
        background: linear-gradient(145deg, #0c1e3d 0%, #0a1628 100%);
        border: 1px solid rgba(2, 132, 199, 0.35);
        box-shadow: 0 8px 32px rgba(2, 132, 199, 0.1), inset 0 1px 0 rgba(2,132,199,0.15);
    }
    .pro-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #0284c7, #38bdf8, #7dd3fc, #0284c7);
        background-size: 200%;
        animation: shimmer 3s linear infinite;
    }
    .pro-card .card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 18px;
    }
    .pro-card .agent-badge {
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #38bdf8;
        background: rgba(56,189,248,0.1);
        border: 1px solid rgba(56,189,248,0.25);
        padding: 4px 12px;
        border-radius: 100px;
    }
    .pro-card .card-body {
        font-family: 'DM Sans', sans-serif;
        font-size: 15px;
        line-height: 1.8;
        color: #bae6fd;
        font-weight: 300;
    }
    .pro-card .icon-dot {
        width: 8px; height: 8px;
        background: #38bdf8;
        border-radius: 50%;
        box-shadow: 0 0 8px #38bdf8;
        flex-shrink: 0;
    }

    /* Con Card (Amber) */
    .con-card {
        background: linear-gradient(145deg, #1f1500 0%, #1a1200 100%);
        border: 1px solid rgba(202, 138, 4, 0.35);
        box-shadow: 0 8px 32px rgba(202, 138, 4, 0.1), inset 0 1px 0 rgba(202,138,4,0.15);
    }
    .con-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #ca8a04, #fbbf24, #fde68a, #ca8a04);
        background-size: 200%;
        animation: shimmer 3s linear infinite;
    }
    .con-card .card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 18px;
    }
    .con-card .agent-badge {
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #fbbf24;
        background: rgba(251,191,36,0.1);
        border: 1px solid rgba(251,191,36,0.25);
        padding: 4px 12px;
        border-radius: 100px;
    }
    .con-card .card-body {
        font-family: 'DM Sans', sans-serif;
        font-size: 15px;
        line-height: 1.8;
        color: #fde68a;
        font-weight: 300;
    }
    .con-card .icon-dot {
        width: 8px; height: 8px;
        background: #fbbf24;
        border-radius: 50%;
        box-shadow: 0 0 8px #fbbf24;
        flex-shrink: 0;
    }

    @keyframes shimmer {
        0%   { background-position: 0% 0%; }
        100% { background-position: 200% 0%; }
    }

    /* ── Judge Verdict ── */
    .verdict-wrapper {
        margin: 48px 0 32px;
        position: relative;
    }
    .verdict-eyebrow {
        text-align: center;
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #a855f7;
        margin-bottom: 20px;
    }
    .judge-card {
        background: linear-gradient(145deg, #160d2e 0%, #110826 100%);
        border: 1px solid rgba(147,51,234,0.4);
        border-radius: 20px;
        padding: 40px 44px;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 0 0 1px rgba(147,51,234,0.1),
            0 20px 60px rgba(147,51,234,0.15),
            inset 0 1px 0 rgba(147,51,234,0.2);
    }
    .judge-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #7c3aed, #a855f7, #c084fc, #f0abfc, #a855f7, #7c3aed);
        background-size: 300%;
        animation: shimmer 4s linear infinite;
    }
    .judge-card::after {
        content: '';
        position: absolute;
        top: -80px; right: -80px;
        width: 260px; height: 260px;
        background: radial-gradient(circle, rgba(147,51,234,0.12) 0%, transparent 70%);
        pointer-events: none;
    }
    .judge-card .judge-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 28px;
    }
    .judge-card .judge-icon {
        font-size: 28px;
        filter: drop-shadow(0 0 12px rgba(168,85,247,0.7));
    }
    .judge-card .judge-title {
        font-family: 'Playfair Display', serif;
        font-size: 22px;
        font-style: italic;
        color: #e9d5ff;
        margin: 0;
    }
    .judge-card .judge-badge {
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #a855f7;
        background: rgba(168,85,247,0.1);
        border: 1px solid rgba(168,85,247,0.3);
        padding: 4px 12px;
        border-radius: 100px;
        margin-left: auto;
    }
    .judge-card .judge-body {
        font-family: 'DM Sans', sans-serif;
        font-size: 16px;
        line-height: 1.9;
        color: #d8b4fe;
        font-weight: 300;
    }

    /* ── Stats Bar ── */
    .stats-bar {
        display: flex;
        gap: 12px;
        justify-content: center;
        margin: 32px 0;
        flex-wrap: wrap;
    }
    .stat-pill {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 100px;
        padding: 8px 20px;
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        color: #6b7280;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .stat-pill .dot {
        width: 6px; height: 6px;
        border-radius: 50%;
    }
    .stat-pill.pro .dot  { background: #38bdf8; box-shadow: 0 0 6px #38bdf8; }
    .stat-pill.con .dot  { background: #fbbf24; box-shadow: 0 0 6px #fbbf24; }
    .stat-pill.judge .dot { background: #a855f7; box-shadow: 0 0 6px #a855f7; }

    /* ── Tabs ── */
    [data-testid="stTabs"] [data-testid="stTab"] {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
        color: #6b7280 !important;
        font-weight: 500 !important;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        color: #a855f7 !important;
        border-bottom-color: #a855f7 !important;
    }
    [data-testid="stTabsContent"] {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 12px !important;
        padding: 24px !important;
    }

    /* ── Transcript Items ── */
    .transcript-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    .transcript-round {
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #4b5563;
        margin-bottom: 10px;
    }
    .transcript-text {
        font-family: 'DM Sans', sans-serif;
        font-size: 14px;
        line-height: 1.75;
        color: #9ca3af;
        font-weight: 300;
    }

    /* ── Live indicator ── */
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #ef4444;
        margin-bottom: 24px;
    }
    .live-dot {
        width: 7px; height: 7px;
        background: #ef4444;
        border-radius: 50%;
        animation: pulse 1.2s ease-in-out infinite;
        box-shadow: 0 0 8px #ef4444;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.8); }
    }

    /* ── Warning / Info ── */
    [data-testid="stAlert"] {
        background: rgba(239,68,68,0.08) !important;
        border: 1px solid rgba(239,68,68,0.2) !important;
        border-radius: 12px !important;
        color: #fca5a5 !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #3f3f5f; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #6d6d9f; }

    /* ── Sidebar (if used) ── */
    [data-testid="stSidebar"] {
        background: #0a0a12 !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }

    /* ── Main container padding ── */
    .main .block-container {
        padding-top: 0 !important;
        max-width: 1200px !important;
    }

    /* ── Section labels ── */
    .section-label {
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #374151;
        margin-bottom: 24px;
        margin-top: 8px;
        text-align: center;
    }

    /* ── Topic display pill ── */
    .topic-pill {
        display: inline-block;
        background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(168,85,247,0.1));
        border: 1px solid rgba(124,58,237,0.3);
        border-radius: 100px;
        padding: 10px 28px;
        font-family: 'Playfair Display', serif;
        font-size: 18px;
        font-style: italic;
        color: #c4b5fd;
        text-align: center;
        margin: 0 auto 32px;
        display: block;
        width: fit-content;
        max-width: 90%;
    }
    
    /* Hide streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)




def reset_debate():
    st.session_state.is_running = False
    st.session_state.debate_finished = False
    st.session_state.messages = []
    st.session_state.final_pro_history = []
    st.session_state.final_con_history = []
    st.session_state.verdict = ""
    st.session_state.debate_topic = ""

if "is_running" not in st.session_state:
    reset_debate()




def render_debate_ui(show_tabs=False):
    """Renders the full debate UI from session state."""
    current_round_rendered = 0
    cols = None

    for msg in st.session_state.messages:
        if msg["round"] != current_round_rendered:
            current_round_rendered = msg["round"]
            st.markdown(
                f"""<div class="round-badge">
                        <div class="line"></div>
                        <div class="label">Round {current_round_rendered}</div>
                        <div class="line right"></div>
                    </div>""",
                unsafe_allow_html=True
            )
            cols = st.columns(2, gap="large")

        if msg["role"] == "pro" and cols:
            with cols[0]:
                
                st.markdown(
                    """<div class="pro-card">
                            <div class="card-header">
                                <div class="icon-dot"></div>
                                <span class="agent-badge">Pro · Affirmative</span>
                            </div>
                            <div class="card-body">""", 
                    unsafe_allow_html=True
                )
                
                st.markdown(msg['content'])
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
        elif msg["role"] == "con" and cols:
            with cols[1]:
                st.markdown(
                    """<div class="con-card">
                            <div class="card-header">
                                <div class="icon-dot"></div>
                                <span class="agent-badge">Con · Opposition</span>
                            </div>
                            <div class="card-body">""", 
                    unsafe_allow_html=True
                )
                st.markdown(msg['content'])
                st.markdown("</div></div>", unsafe_allow_html=True)

    if st.session_state.verdict:
        st.markdown(
            """<div class="verdict-wrapper">
                    <div class="verdict-eyebrow">⚖&nbsp;&nbsp;Final Judgment</div>
                    <div class="judge-card">
                        <div class="judge-header">
                            <span class="judge-icon">⚖️</span>
                            <h3 class="judge-title">The Judge's Verdict</h3>
                            <span class="judge-badge">Final Decision</span>
                        </div>
                        <div class="judge-body">""",
            unsafe_allow_html=True
        )
        st.markdown(st.session_state.verdict)
        st.markdown("</div></div></div>", unsafe_allow_html=True)

    if show_tabs and st.session_state.verdict:
        st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-label">📜 &nbsp; Complete Transcripts</p>', unsafe_allow_html=True)

        tab_pro, tab_con, tab_judge = st.tabs(["🟦 &nbsp;Pro Transcript", "🟨 &nbsp;Con Transcript", "⚖️ &nbsp;Judge Verdict"])

        with tab_pro:
            for i, text in enumerate(st.session_state.final_pro_history):
                st.markdown(
                    f"""<div class="transcript-item">
                            <div class="transcript-round">Round {i+1}</div>
                            <div class="transcript-text">""",
                    unsafe_allow_html=True
                )
                st.markdown(text)
                st.markdown("</div></div>", unsafe_allow_html=True)
                
        with tab_con:
            for i, text in enumerate(st.session_state.final_con_history):
                st.markdown(
                    f"""<div class="transcript-item">
                            <div class="transcript-round">Round {i+1}</div>
                            <div class="transcript-text">""",
                    unsafe_allow_html=True
                )
                st.markdown(text)
                st.markdown("</div></div>", unsafe_allow_html=True)
                
        with tab_judge:
            st.markdown(
                """<div class="transcript-item"><div class="transcript-text">""",
                unsafe_allow_html=True
            )
            st.markdown(st.session_state.verdict)
            st.markdown("</div></div>", unsafe_allow_html=True)




st.markdown("""
<div class="arena-hero">
    <span class="eyebrow">Powered by AI Agents</span>
    <h1>Debate Arena</h1>
    <p class="subtitle">Two AI agents clash across three rounds of structured argument. One judge. One verdict.</p>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="stats-bar">
    <div class="stat-pill pro"><div class="dot"></div>Pro &nbsp;·&nbsp; Affirmative</div>
    <div class="stat-pill">VS</div>
    <div class="stat-pill con"><div class="dot"></div>Con &nbsp;·&nbsp; Opposition</div>
    <div class="stat-pill" style="margin-left:12px;">3 Rounds</div>
    <div class="stat-pill judge"><div class="dot"></div>AI Judge</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)




st.markdown('<div class="input-section">', unsafe_allow_html=True)

col_input, col_start, col_reset = st.columns([5, 1.4, 1.2])

with col_input:
    topic = st.text_input(
        "Debate Topic",
        placeholder="e.g., Remote work is more productive than office work",
        label_visibility="visible"
    )

with col_start:
    st.write("")
    if st.button("🚀 &nbsp;Start Debate", use_container_width=True, type="primary"):
        if topic:
            reset_debate()
            st.session_state.is_running = True
            st.session_state.debate_topic = topic
        else:
            st.warning("Please enter a topic to begin.")

with col_reset:
    st.write("")
    if st.button("↺ &nbsp;Reset", use_container_width=True):
        reset_debate()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)




if st.session_state.is_running and not st.session_state.debate_finished:

    
    active_topic = topic or st.session_state.debate_topic
    st.markdown(f'<div class="topic-pill">"{active_topic}"</div>', unsafe_allow_html=True)
    st.markdown('<div class="live-indicator"><div class="live-dot"></div>Live Debate</div>', unsafe_allow_html=True)

    app = create_debate_graph()
    initial_state = {
        "topic": active_topic,
        "current_round": "Round 1",
        "round_count": 1,
        "pro_history": [],
        "con_history": [],
        "verdict": ""
    }

    ui_container = st.empty()
    current_round_tracker = 1

    with st.spinner("The debate is in session…"):
        for output in app.stream(initial_state):
            for node_name, update_data in output.items():
                if node_name == "pro":
                    response = update_data["pro_history"][0]
                    st.session_state.messages.append({"round": current_round_tracker, "role": "pro", "content": response})
                    st.session_state.final_pro_history.append(response)

                elif node_name == "con":
                    response = update_data["con_history"][0]
                    st.session_state.messages.append({"round": current_round_tracker, "role": "con", "content": response})
                    st.session_state.final_con_history.append(response)
                    current_round_tracker += 1

                elif node_name == "judge":
                    st.session_state.verdict = update_data["verdict"]

                with ui_container.container():
                    render_debate_ui(show_tabs=False)

    st.session_state.debate_finished = True
    st.rerun()


elif st.session_state.debate_finished:
    
    if st.session_state.debate_topic:
        st.markdown(f'<div class="topic-pill">"{st.session_state.debate_topic}"</div>', unsafe_allow_html=True)
    render_debate_ui(show_tabs=True)
