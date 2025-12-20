"""
Authentication utility for AgriSensa Streamlit
Provides session-based authentication for all pages
"""

import streamlit as st
import hashlib

# ========== USER DATABASE (Simple - can be extended to use real DB) ==========
# Format: username: (password_hash, role, display_name)
USERS = {
    'admin': {
        'password': 'admin123',
        'role': 'admin',
        'name': 'Administrator',
        'email': 'admin@agrisensa.com'
    },
    'demo': {
        'password': 'demo123',
        'role': 'user',
        'name': 'Demo User',
        'email': 'demo@agrisensa.com'
    },
    'petani': {
        'password': 'petani123',
        'role': 'user',
        'name': 'Petani Indonesia',
        'email': 'petani@agrisensa.com'
    }
}


def init_auth_state():
    """Initialize authentication state."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None


def login(username: str, password: str) -> tuple[bool, str]:
    """
    Authenticate user with username and password.
    Returns (success, message)
    """
    init_auth_state()
    
    if not username or not password:
        return False, "Username dan password harus diisi"
    
    # Check if user exists
    if username.lower() not in USERS:
        return False, "Username tidak ditemukan"
    
    user_data = USERS[username.lower()]
    
    # Verify password
    if user_data['password'] != password:
        return False, "Password salah"
    
    # Set session state
    st.session_state.authenticated = True
    st.session_state.user = {
        'username': username.lower(),
        'name': user_data['name'],
        'role': user_data['role'],
        'email': user_data['email']
    }
    
    return True, f"Selamat datang, {user_data['name']}!"


def logout():
    """Logout current user."""
    st.session_state.authenticated = False
    st.session_state.user = None


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    init_auth_state()
    return st.session_state.authenticated


def get_current_user() -> dict:
    """Get current logged in user info."""
    init_auth_state()
    return st.session_state.user


def require_auth():
    """
    Require authentication to access page.
    Call this at the start of every protected page.
    If not authenticated, shows login prompt and stops execution.
    """
    init_auth_state()
    
    if not st.session_state.authenticated:
        show_login_required()
        st.stop()
    
    return st.session_state.user


def show_login_required():
    """Show login required message with redirect."""
    st.markdown("""
    <style>
        .login-required {
            text-align: center;
            padding: 3rem;
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-radius: 16px;
            margin: 2rem auto;
            max-width: 500px;
        }
        .login-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        .login-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #92400e;
            margin-bottom: 0.5rem;
        }
        .login-message {
            color: #a16207;
            margin-bottom: 1.5rem;
        }
    </style>
    <div class="login-required">
        <div class="login-icon">🔐</div>
        <div class="login-title">Login Diperlukan</div>
        <div class="login-message">Silakan login untuk mengakses fitur ini</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick login form
    st.markdown("---")
    with st.form("quick_login"):
        st.markdown("### 🔑 Quick Login")
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username", placeholder="admin / demo / petani")
        with col2:
            password = st.text_input("Password", type="password", placeholder="••••••••")
        
        if st.form_submit_button("Login", use_container_width=True, type="primary"):
            success, message = login(username, password)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    st.caption("**Demo accounts:** admin/admin123, demo/demo123, petani/petani123")


def show_user_info_sidebar():
    """Show current user info in sidebar."""
    if is_authenticated():
        user = get_current_user()
        st.sidebar.markdown(f"""
        <div style="padding: 1rem; background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                    border-radius: 12px; margin-bottom: 1rem; border: 1px solid #10b981;">
            <div style="font-weight: 700; color: #065f46;">👤 {user['name']}</div>
            <div style="font-size: 0.8rem; color: #047857;">{user['role'].upper()}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
