import streamlit as st
from graph import create_debate_graph  
st.set_page_config(page_title="AI Debate Arena", layout="wide")

st.markdown("""
<style>
    /* Pro Agent Styling (Blue) */
    .pro-box {
        background-color: #e0f2fe;
        border-left: 5px solid #0284c7;
        padding: 20px;
        border-radius: 8px;
        color: #0c4a6e;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Con Agent Styling (Yellow) */
    .con-box {
        background-color: #fef9c3;
        border-right: 5px solid #ca8a04;
        padding: 20px;
        border-radius: 8px;
        color: #713f12;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Judge Agent Styling (Purple) */
    .judge-box {
        background-color: #f3e8ff;
        border-top: 5px solid #9333ea;
        padding: 25px;
        border-radius: 8px;
        color: #4c1d95;
        margin-top: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Round Header Styling */
    .round-header {
        text-align: center;
        color: #5E3A8FFF;
        padding-top: 15px;
        padding-bottom: 5px;
        border-bottom: 2px solid #ddd;
        margin-bottom: 20px;
        font-family: sans-serif;
    }
</style>
""", unsafe_allow_html=True)


def reset_debate():
    st.session_state.is_running = False
    st.session_state.debate_finished = False
    st.session_state.messages = []
    st.session_state.final_pro_history = []
    st.session_state.final_con_history = []
    st.session_state.verdict = ""

if "is_running" not in st.session_state:
    reset_debate()


def render_debate_ui(show_tabs=False):
    """Renders the debate UI from the current session state history."""
    current_round_rendered = 0
    cols = None
    
    
    for msg in st.session_state.messages:
        
        if msg["round"] != current_round_rendered:
            current_round_rendered = msg["round"]
            st.markdown(f"<div class='round-header'><h2>Round {current_round_rendered}</h2></div>", unsafe_allow_html=True)
            cols = st.columns(2)
        
        
        if msg["role"] == "pro" and cols:
            with cols[0]:
                st.markdown(f"<div class='pro-box'><h3>🟦 Pro Agent</h3>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "con" and cols:
            with cols[1]:
                st.markdown(f"<div class='con-box'><h3>🟨 Con Agent</h3>{msg['content']}</div>", unsafe_allow_html=True)
                
    
    if st.session_state.verdict:
        st.markdown(f"<div class='judge-box'><h2>⚖️ The Judge's Verdict</h2>{st.session_state.verdict}</div>", unsafe_allow_html=True)
        
    
    if show_tabs and st.session_state.verdict:
        st.markdown("---")
        st.markdown("### 📜 Complete Transcripts")
        tab_pro, tab_con, tab_judge = st.tabs(["🟦 Pro Transcript", "🟨 Con Transcript", "⚖️ Judge Verdict"])
        
        with tab_pro:
            for i, text in enumerate(st.session_state.final_pro_history):
                st.markdown(f"**Round {i+1}:**\n\n{text}")
                st.divider()
        with tab_con:
            for i, text in enumerate(st.session_state.final_con_history):
                st.markdown(f"**Round {i+1}:**\n\n{text}")
                st.divider()
        with tab_judge:
            st.markdown(st.session_state.verdict)


st.title("⚖️ AI Debate Arena")
st.write("Watch two AI agents debate a topic over 3 rounds, followed by a final judgment.")


col1, col2, col3 = st.columns([6, 2, 2])
with col1:
    topic = st.text_input("Enter the Debate Topic:", placeholder="e.g., Remote work is more productive than office work")
with col2:
    st.write("") 
    if st.button("🚀 Start Debate", use_container_width=True, type="primary"):
        if topic:
            reset_debate()
            st.session_state.is_running = True
        else:
            st.warning("Please enter a topic first.")
with col3:
    st.write("") 
    if st.button("🔄 Clear / Reset", use_container_width=True):
        reset_debate()
        st.rerun()

st.markdown("---")


if st.session_state.is_running and not st.session_state.debate_finished:
    
    app = create_debate_graph()
    initial_state = {
        "topic": topic,
        "current_round": "Round 1",
        "round_count": 1,
        "pro_history": [],
        "con_history": [],
        "verdict": ""
    }
    
    
    ui_container = st.empty()
    
    current_round_tracker = 1
    
    
    with st.spinner("The debate is live..."):
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
  
    render_debate_ui(show_tabs=True)
