import streamlit as st
from ai_researcher_2 import INITIAL_PROMPT, graph, config
from pathlib import Path
import logging
from langchain_core.messages import AIMessage
import json
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Advanced 3D Streamlit Config with Sidebar
st.set_page_config(
    page_title="Research AI Agent", 
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium 3D Styling with Sidebar
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(-45deg, #0a0a0a, #1a1a2e, #16213e, #0f3460);
        background-size: 400% 400%;
        animation: gradientAnimation 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gradientAnimation {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    section[data-testid="stSidebar"] {
        background: rgba(10, 10, 20, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(0, 255, 255, 0.2) !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .research-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 3rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.2);
    }
    
    .research-title {
        font-size: 3.5rem !important;
        font-weight: 800;
        background: linear-gradient(135deg, #00ffff 0%, #ff00ff 50%, #ffff00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem !important;
    }
    
    .research-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        font-weight: 500;
    }
    
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 18px !important;
        margin: 1rem 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 1rem !important;
    }
    
    [data-testid="stChatMessageContent"] {
        color: #e0e0e0 !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        padding: 1rem !important;
    }
    
    .stChatInput textarea {
        background: rgba(255, 255, 255, 1) !important;
        border: 2px solid rgba(0, 255, 255, 0.5) !important;
        border-radius: 16px !important;
        color: #1a1a2e !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
    .stChatInput textarea::placeholder {
        color: rgba(0, 100, 150, 0.6) !important;
        opacity: 1 !important;
    }
    
    .stChatInput textarea:focus {
        border-color: rgba(255, 0, 255, 0.6) !important;
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.4) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #00ffff !important;
        font-size: 1.5rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(255, 0, 255, 0.2)) !important;
        color: white !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(255, 0, 255, 0.3)) !important;
        border-color: rgba(0, 255, 255, 0.6) !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.4) !important;
    }
    
    .thinking-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 0.5rem 1rem;
        background: rgba(0, 255, 255, 0.15);
        border-radius: 12px;
        border: 1px solid rgba(0, 255, 255, 0.4);
        color: #00ffff;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .thinking-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00ffff;
        animation: thinking 1.4s infinite ease-in-out;
    }
    
    .thinking-dot:nth-child(1) { animation-delay: -0.32s; }
    .thinking-dot:nth-child(2) { animation-delay: -0.16s; }
    .thinking-dot:nth-child(3) { animation-delay: 0s; }
    
    @keyframes thinking {
        0%, 80%, 100% { transform: scale(0); opacity: 0.3; }
        40% { transform: scale(1); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized chat history")

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "default"

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {
        "default": {
            "name": "Current Research",
            "history": [],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    }

# SIDEBAR
with st.sidebar:
    st.markdown("### 💬 Chat Sessions")
    st.markdown("---")
    
    if st.button("🆕 New Chat Session", use_container_width=True):
        new_session_id = f"session_{len(st.session_state.chat_sessions)}"
        st.session_state.chat_sessions[new_session_id] = {
            "name": f"Research {len(st.session_state.chat_sessions) + 1}",
            "history": [],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.current_chat = new_session_id
        st.session_state.chat_history = []
        st.rerun()
    
    if st.button("🗑️ Clear Current Chat", use_container_width=True, type="secondary"):
        if st.session_state.current_chat in st.session_state.chat_sessions:
            st.session_state.chat_sessions[st.session_state.current_chat]["history"] = []
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Session Info")
    current_session = st.session_state.chat_sessions[st.session_state.current_chat]
    st.info(f"**Active:** {current_session['name']}")
    st.info(f"**Messages:** {len(st.session_state.chat_history)}")
    
    if st.button("📤 Export Chat", use_container_width=True):
        chat_data = {
            "session_name": current_session['name'],
            "exported_at": datetime.now().isoformat(),
            "messages": st.session_state.chat_history
        }
        st.download_button(
            label="Download JSON",
            data=json.dumps(chat_data, indent=2),
            file_name=f"research_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

# MAIN CONTENT
st.markdown('''
<div class="research-header">
    <h1 class="research-title">🔬 Research AI Agent</h1>
    <p class="research-subtitle">Advanced AI-powered research assistant with real-time data analysis</p>
</div>
''', unsafe_allow_html=True)

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Session", current_session['name'])
with col2:
    st.metric("Total", len(st.session_state.chat_history))
with col3:
    st.metric("User", len([m for m in st.session_state.chat_history if m['role'] == 'user']))
with col4:
    st.metric("AI", len([m for m in st.session_state.chat_history if m['role'] == 'assistant']))

st.markdown("### 💬 Conversation")

# Display chat history
current_history = st.session_state.chat_sessions[st.session_state.current_chat]["history"]
for message in current_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("🔍 What research topic would you like to explore?")

if user_input:
    # Add user message
    st.session_state.chat_sessions[st.session_state.current_chat]["history"].append(
        {"role": "user", "content": user_input}
    )
    st.session_state.chat_history = st.session_state.chat_sessions[st.session_state.current_chat]["history"]
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Process and display AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown('<span class="thinking-indicator">🤖 AI is researching<span class="thinking-dot"></span><span class="thinking-dot"></span><span class="thinking-dot"></span></span>', unsafe_allow_html=True)
        
        # Prepare input
        chat_input = {
            "messages": [{"role": "system", "content": INITIAL_PROMPT}] + st.session_state.chat_history
        }
        logger.info("Starting agent processing...")
        
        # Stream response
        full_response = ""
        tool_calls_log = []
        
        try:
            for s in graph.stream(chat_input, config, stream_mode="values"):
                message = s["messages"][-1]
                
                # Log tool calls
                if getattr(message, "tool_calls", None):
                    for tool_call in message.tool_calls:
                        tool_info = f"🔧 {tool_call['name']}"
                        tool_calls_log.append(tool_info)
                        logger.info(f"Tool call: {tool_call['name']}")
                
                # Handle assistant response
                if isinstance(message, AIMessage) and message.content:
                    text_content = message.content if isinstance(message.content, str) else str(message.content)
                    full_response += text_content + " "
            
            # Add tool calls to response
            if tool_calls_log:
                full_response = "🛠️ **Tools Used:** " + " | ".join(tool_calls_log) + "\n\n" + full_response
            
            # Display final response
            message_placeholder.markdown(full_response)
            
            # Save to history
            if full_response:
                st.session_state.chat_sessions[st.session_state.current_chat]["history"].append(
                    {"role": "assistant", "content": full_response}
                )
                st.session_state.chat_history = st.session_state.chat_sessions[st.session_state.current_chat]["history"]
        
        except Exception as e:
            logger.error(f"Error during agent processing: {e}")
            message_placeholder.markdown(f"❌ **Error:** {str(e)}")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; color: rgba(255, 255, 255, 0.5);">
    🚀 Powered by Advanced AI Research Agent
</div>
""", unsafe_allow_html=True)
