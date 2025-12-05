# AgriBot - Asisten Pertanian Cerdas AI
# Chatbot powered by Google Gemini API
# Version: 1.0.1 - Fixed Streamlit Cloud secrets support

import streamlit as st
import os
import sys
from datetime import datetime

# ========== API KEY SETUP ==========
# Try to get API key from Streamlit secrets first, then fall back to environment variable
API_KEY_STATUS = "❌ Not loaded"
try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
        API_KEY_STATUS = "✅ Loaded from Streamlit secrets"
    elif "GEMINI_API_KEY" in os.environ:
        API_KEY_STATUS = "✅ Loaded from environment variable"
    else:
        API_KEY_STATUS = "❌ Not found in secrets or environment"
except Exception as e:
    API_KEY_STATUS = f"❌ Error: {str(e)}"

# Add parent directory to path to import chatbot_service
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from app.services.chatbot_service import ChatbotService
    CHATBOT_AVAILABLE = True
except ImportError:
    CHATBOT_AVAILABLE = False
    print("Warning: ChatbotService not available")

st.set_page_config(page_title="AgriBot - Asisten Pertanian AI", page_icon="🤖", layout="wide")

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    /* Chat container */
    .stChatMessage {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    /* User message */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    /* Bot message */
    .stChatMessage[data-testid="assistant-message"] {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
    }
    
    /* Input box */
    .stChatInputContainer {
        border-top: 1px solid #e2e8f0;
        padding-top: 1rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    }
    
    /* Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== INITIALIZE CHATBOT ==========
@st.cache_resource
def get_chatbot():
    """Initialize chatbot service (cached)"""
    if not CHATBOT_AVAILABLE:
        return None, "ChatbotService not available (import failed)"
    try:
        # Get API key from Streamlit secrets or environment
        api_key = None
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        elif "GEMINI_API_KEY" in os.environ:
            api_key = os.environ["GEMINI_API_KEY"]
        else:
            return None, "API key not found in secrets or environment"
        
        # Pass API key directly to ChatbotService
        chatbot = ChatbotService(api_key=api_key)
        
        # Check if initialization was successful
        if chatbot.init_error:
            return None, f"Initialization error: {chatbot.init_error}"
        
        if not chatbot.chat:
            return None, "Chat session not initialized"
        
        return chatbot, None
    except Exception as e:
        return None, f"Exception: {str(e)}"

# ========== SESSION STATE ==========
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Halo! Saya **AgriBot**, asisten pertanian pintar Anda. 🌱\n\nAda yang bisa saya bantu mengenai:\n- 🌾 Budidaya tanaman\n- 🐛 Hama & penyakit\n- 💧 Irigasi & pemupukan\n- 🌿 Pestisida nabati\n- 📊 Harga pasar\n- Dan topik pertanian lainnya!\n\nSilakan tanya apa saja! 😊"
        }
    ]

if 'chat_session' not in st.session_state:
    chatbot, error = get_chatbot()
    if chatbot and chatbot.chat:
        st.session_state.chat_session = chatbot.chat
        st.session_state.chatbot_error = None
    else:
        st.session_state.chat_session = None
        st.session_state.chatbot_error = error or "Unknown error"
        st.session_state.chat_session = None

# ========== MAIN APP ==========

# Header
st.markdown('<h1 class="main-header">🤖 AgriBot</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">Asisten Pertanian Cerdas Berbasis AI</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🔑 API Key Status")
    if "✅" in API_KEY_STATUS:
        st.success(API_KEY_STATUS)
    else:
        st.error(API_KEY_STATUS)
    
    st.markdown("---")
    st.markdown("### 📊 Statistik Chat")
    st.metric("Total Pesan", len(st.session_state.messages))
    st.metric("Pesan Anda", len([m for m in st.session_state.messages if m["role"] == "user"]))
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("""
    **Contoh Pertanyaan:**
    - Bagaimana cara menanam cabai?
    - Hama apa yang menyerang tomat?
    - Cara membuat pestisida nabati dari mimba?
    - Berapa harga cabai hari ini?
    - Pupuk apa yang bagus untuk padi?
    """)
    
    st.markdown("---")
    st.markdown("### 🌿 Fitur Khusus")
    st.success("""
    AgriBot terintegrasi dengan:
    - 📖 Knowledge Base (60+ artikel)
    - 🌿 Database Pestisida Nabati (60+ tumbuhan)
    - 🥬 Panduan Budidaya Sayuran
    - 🌍 Data pH Tanah & Ketinggian
    """)
    
    st.markdown("---")
    if st.button("🗑️ Hapus Riwayat Chat", type="secondary", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]  # Keep welcome message
        # Reset chat session
        chatbot = get_chatbot()
        if chatbot and chatbot.chat:
            st.session_state.chat_session = chatbot.chat
        st.rerun()
    
    st.markdown("---")
    st.caption("Powered by Google Gemini AI")

# Check if chatbot is available
if not CHATBOT_AVAILABLE or st.session_state.chat_session is None:
    st.error("⚠️ **Chatbot tidak tersedia**")
    
    # Show specific error if available
    if hasattr(st.session_state, 'chatbot_error') and st.session_state.chatbot_error:
        st.error(f"**Error Detail:** {st.session_state.chatbot_error}")
    
    st.warning("""
    Chatbot memerlukan:
    1. **Google Gemini API Key** di environment variable `GEMINI_API_KEY`
    2. Package `google-generativeai` terinstall
    
    Untuk mengaktifkan chatbot:
    ```bash
    # Install package
    pip install google-generativeai
    
    # Set API key (Windows)
    set GEMINI_API_KEY=your_api_key_here
    
    # Set API key (Linux/Mac)
    export GEMINI_API_KEY=your_api_key_here
    ```
    
    Dapatkan API key gratis di: https://makersuite.google.com/app/apikey
    """)
    st.stop()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Tanya sesuatu tentang pertanian..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("AgriBot sedang berpikir..."):
            try:
                # Get response from Gemini
                response = st.session_state.chat_session.send_message(prompt)
                bot_response = response.text
                
                # Display response
                st.markdown(bot_response)
                
                # Add to chat history
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
            except Exception as e:
                error_msg = f"Maaf, terjadi kesalahan: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")
st.caption("""
🤖 **AgriBot v1.0** - Asisten Pertanian Cerdas

💡 **Catatan**: AgriBot menggunakan AI dan mungkin tidak selalu 100% akurat. 
Untuk keputusan penting, konsultasikan dengan penyuluh pertanian atau ahli.

🌱 **Prinsip**: Mendorong pertanian berkelanjutan dan ramah lingkungan
""")
