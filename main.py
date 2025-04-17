import streamlit as st
from datetime import datetime
import random
import time
import base64

# Set page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better UI with dark theme
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Main container styling */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    /* Header styling */
    .header {
        background: linear-gradient(90deg, #3d5af1 0%, #7b2ff7 100%);
        padding: 1.5rem;
        border-radius: 0.8rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        margin-bottom: 1.5rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Chat container */
    .chat-container {
        background-color: #1a1c24;
        border-radius: 0.8rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        padding: 1.5rem;
        height: 65vh;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 10px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #1a1c24;
        border-radius: 5px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #3d5af1;
        border-radius: 5px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #7b2ff7;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1rem 1.5rem; 
        border-radius: 1rem; 
        margin-bottom: 1rem; 
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 0.75rem;
        max-width: 80%;
        animation: fadeIn 0.3s ease-in-out;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-message.user {
        background: linear-gradient(90deg, #3d5af1 0%, #2b3c8e 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 0.2rem;
        box-shadow: 0 4px 15px rgba(61, 90, 241, 0.2);
    }
    
    .chat-message.assistant {
        background: linear-gradient(90deg, #2c2f3c 0%, #1e2028 100%);
        color: white;
        margin-right: auto;
        border-bottom-left-radius: 0.2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .chat-message .avatar {
        min-width: 2.8rem;
        text-align: center;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        padding: 0.5rem;
        height: 2.8rem;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .chat-message.user .avatar {
        background: rgba(61, 90, 241, 0.3);
    }
    
    .chat-message.assistant .avatar {
        background: rgba(123, 47, 247, 0.3);
    }
    
    .chat-message .message {
        flex-grow: 1;
        line-height: 1.5;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 0.8rem 1.2rem;
        background: linear-gradient(90deg, #2c2f3c 0%, #1e2028 100%);
        border-radius: 1rem;
        margin-bottom: 1rem;
        width: fit-content;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background-color: #7b2ff7;
        border-radius: 50%;
        animation: typingAnimation 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typingAnimation {
        0%, 100% { transform: translateY(0); opacity: 0.5; }
        50% { transform: translateY(-5px); opacity: 1; }
    }
    
    /* Input area */
    .input-area {
        background-color: #1a1c24;
        border-radius: 0.8rem;
        padding: 1.2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        display: flex;
        gap: 0.8rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 1rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 1.5rem;
        padding: 0.75rem 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background-color: #2c2f3c;
        color: white;
        box-shadow: none !important;
        font-size: 1rem;
        width: 100%;
    }
    
    .stTextInput > div {
        flex-grow: 1;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3d5af1;
        box-shadow: 0 0 0 1px #3d5af1 !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5);
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #1a1c24;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .sidebar-title {
        background: linear-gradient(90deg, #3d5af1 0%, #7b2ff7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 10px rgba(123, 47, 247, 0.3);
    }
    
    .sidebar-section {
        background-color: #0e1117;
        padding: 1.2rem;
        border-radius: 0.8rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-section h3 {
        color: #e0e0e0;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        background: linear-gradient(90deg, #3d5af1 0%, #7b2ff7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #3d5af1 0%, #7b2ff7 100%);
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 10px rgba(123, 47, 247, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(123, 47, 247, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Model buttons */
    .model-button {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        border-radius: 0.5rem;
        color: white;
        font-weight: 500;
        font-size: 0.9rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .model-button:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }
    
    .model-button.active {
        background: linear-gradient(90deg, #3d5af1 0%, #7b2ff7 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 10px rgba(123, 47, 247, 0.3);
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #3d5af1 0%, #7b2ff7 100%);
    }
    
    .stSlider > div > div {
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Remove default footer */
    .reportview-container .main footer {
        visibility: hidden;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
    
    /* Chat features */
    .features-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.8rem;
        padding: 1rem;
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        opacity: 0.7;
    }
    
    /* Send button */
    .send-button {
        background: linear-gradient(90deg, #3d5af1 0%, #7b2ff7 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(123, 47, 247, 0.3);
    }
    
    .send-button:hover {
        transform: translateY(-2px) rotate(15deg);
        box-shadow: 0 6px 15px rgba(123, 47, 247, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Function to get a data URL for an image
def get_avatar_url(emoji):
    # This helper function creates an HTML image with the emoji
    return f'<div style="font-size: 1.5rem;">{emoji}</div>'

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thinking" not in st.session_state:
    st.session_state.thinking = False

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "GPT-3.5"

# Mock responses
mock_responses = [
    "I'm an AI assistant here to help! What would you like to know?",
    "That's an interesting question. Based on my knowledge, I would say that depends on several factors.",
    "Here's what I found: The latest research suggests multiple approaches to solve this problem.",
    "I don't have specific information about that, but I can suggest some resources that might help.",
    "Let me break this down into steps: First, you'll want to understand the fundamentals. Then, practice with some examples.",
    "Great question! This is a complex topic with many perspectives. Here's what I understand about it.",
    "I've analyzed your question, and I think we should approach it from these three angles...",
    "Thank you for sharing that. From what I understand, you're looking for guidance on this specific topic.",
    "Based on the information provided, here are some recommendations that might help you move forward.",
    "I appreciate your patience. This is a nuanced topic that requires careful consideration."
]

# Function to simulate AI typing with a thinking indicator
def simulate_typing():
    with st.container():
        typing_indicator = st.empty()
        typing_indicator.markdown("""
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Simulate thinking time
        time.sleep(random.uniform(1.0, 2.5))
        
        # Clear the typing indicator
        typing_indicator.empty()
        
        # Return a random response
        return random.choice(mock_responses)

# Create the main layout
with st.container():
    # Custom header
    st.markdown("""
    <div class="header">
        <h1>🤖 Neural Chat AI</h1>
        <p>Advanced AI Assistant - Ask me anything</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    st.markdown("""
    <div class="features-container">
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">Smart Responses</div>
            <div class="feature-desc">Intelligent AI-powered answers to any question</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Lightning Fast</div>
            <div class="feature-desc">Get answers in milliseconds</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure</div>
            <div class="feature-desc">Your conversations are private and protected</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns - chat area and sidebar
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat history
        for message in st.session_state.messages:
            avatar_html = get_avatar_url("🧑‍💻" if message["role"] == "user" else "🤖")
            st.markdown(f"""
            <div class="chat-message {message['role']}">
                <div class="avatar">{avatar_html}</div>
                <div class="message">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Add some space at the end of the chat container
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input area
        col1_input, col2_button = st.columns([6, 1])
        
        with col1_input:
            st.markdown('<div class="input-area">', unsafe_allow_html=True)
            # User input
            prompt = st.text_input("", placeholder="Ask anything... Type here", key="user_input", label_visibility="collapsed")
            # Send button
            st.markdown("""
            <div class="send-button">
                <span>➤</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle input
        if prompt:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Set thinking state
            st.session_state.thinking = True
            
            # Rerun to show the user message and start the thinking animation
            st.experimental_rerun()
        
    with col2:
        # Sidebar content
        st.markdown('<div class="sidebar-title">AI Control Panel</div>', unsafe_allow_html=True)
        
        # Model selection section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### AI Model")
        
        # Model selection with custom UI
        model_col1, model_col2 = st.columns(2)
        
        with model_col1:
            if st.button("GPT-3.5", key="gpt35"):
                st.session_state.selected_model = "GPT-3.5"
        
        with model_col2:
            if st.button("GPT-4", key="gpt4"):
                st.session_state.selected_model = "GPT-4"
        
        model_col3, model_col4 = st.columns(2)
        
        with model_col3:
            if st.button("Claude", key="claude"):
                st.session_state.selected_model = "Claude"
        
        with model_col4:
            if st.button("Custom", key="custom"):
                st.session_state.selected_model = "Custom"
        
        selected_text = "Selected model:"
        model_text = st.session_state.selected_model
        st.markdown(f"<div style='margin-top:10px;'>{selected_text} <span style='color:#7b2ff7;font-weight:bold;'>{model_text}</span></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Temperature control
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### Creativity Level")
        temperature = st.slider(
            "",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.1,
            label_visibility="collapsed"
        )
        st.markdown(f"<div>Value: <span style='color:#7b2ff7;font-weight:bold;'>{temperature}</span></div>", unsafe_allow_html=True)
        
        # Description based on temperature
        temp_description = ""
        if temperature <= 0.3:
            temp_description = "More factual, precise responses"
        elif temperature <= 0.7:
            temp_description = "Balanced creativity and accuracy"
        else:
            temp_description = "More creative, diverse responses"
        
        st.markdown(f"<div style='font-size:0.9rem;opacity:0.7;'>{temp_description}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat history control
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### Chat Options")
        if st.button("Clear Conversation", key="clear_history"):
            st.session_state.messages = []
            st.experimental_rerun()
        
        save_btn_col, export_btn_col = st.columns(2)
        with save_btn_col:
            st.button("Save Chat", key="save_chat")
        with export_btn_col:
            st.button("Export", key="export_chat")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # About section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### About")
        st.markdown("<div style='opacity:0.8;'>Neural Chat AI is a state-of-the-art AI assistant powered by advanced language models.</div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top:10px;opacity:0.8;'>Created: " + datetime.now().strftime("%Y-%m-%d") + "</div>", unsafe_allow_html=True)
        st.markdown("<div style='opacity:0.8;'>Version: 2.0.0</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Handle thinking state and generate response outside of the main container
if st.session_state.thinking:
    response = simulate_typing()
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.thinking = False
    st.experimental_rerun()
