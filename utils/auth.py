"""
Authentication utility for AgriSensa Streamlit
Session-based authentication (works without API)
"""

import streamlit as st
from datetime import datetime

# ========== DEFAULT USERS ==========
DEFAULT_USERS = {
    'yandri': {
        'password': 'yandri2025',
        'role': 'superadmin',
        'name': 'Yandri - Owner',
        'email': 'yandri@agrisensa.com'
    },
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


def get_users():
    """Get users from session state."""
    if 'registered_users' not in st.session_state:
        st.session_state.registered_users = DEFAULT_USERS.copy()
    return st.session_state.registered_users


def get_activity_log():
    """Get user activity log."""
    if 'user_activity_log' not in st.session_state:
        st.session_state.user_activity_log = []
    return st.session_state.user_activity_log


def log_user_activity(username: str, action: str, details: str = ""):
    """Log user activity."""
    log = get_activity_log()
    log.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'username': username,
        'action': action,
        'details': details
    })


def init_auth_state():
    """Initialize authentication state."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    get_users()
    get_activity_log()


def login(username: str, password: str) -> tuple:
    """Authenticate user."""
    init_auth_state()
    users = get_users()
    
    if not username or not password:
        return False, "Username dan password harus diisi"
    
    username = username.strip().lower()
    
    if username not in users:
        log_user_activity(username, 'LOGIN_FAILED', 'User tidak ditemukan')
        return False, "Username tidak ditemukan"
    
    user_data = users[username]
    
    if user_data['password'] != password:
        log_user_activity(username, 'LOGIN_FAILED', 'Password salah')
        return False, "Password salah"
    
    st.session_state.authenticated = True
    st.session_state.user = {
        'username': username,
        'name': user_data['name'],
        'role': user_data['role'],
        'email': user_data['email']
    }
    
    log_user_activity(username, 'LOGIN', f"Login sebagai {user_data['role']}")
    return True, f"Selamat datang, {user_data['name']}!"


def logout():
    """Logout current user."""
    if st.session_state.get('user'):
        log_user_activity(st.session_state.user['username'], 'LOGOUT', 'User logout')
    st.session_state.authenticated = False
    st.session_state.user = None


def register(username: str, password: str, name: str, email: str) -> tuple:
    """Register a new user."""
    init_auth_state()
    users = get_users()
    
    if not username or not password or not name:
        return False, "Username, password, dan nama harus diisi"
    
    if len(username) < 3:
        return False, "Username minimal 3 karakter"
    
    if len(password) < 6:
        return False, "Password minimal 6 karakter"
    
    username = username.strip().lower()
    
    if username in users:
        return False, "Username sudah digunakan"
    
    users[username] = {
        'password': password,
        'role': 'user',
        'name': name,
        'email': email or f"{username}@agrisensa.com"
    }
    
    st.session_state.authenticated = True
    st.session_state.user = {
        'username': username,
        'name': name,
        'role': 'user',
        'email': email or f"{username}@agrisensa.com"
    }
    
    log_user_activity(username, 'REGISTER', 'User baru mendaftar')
    return True, f"Selamat datang, {name}! Akun berhasil dibuat."


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    init_auth_state()
    return st.session_state.authenticated


def get_current_user() -> dict:
    """Get current logged in user info."""
    init_auth_state()
    return st.session_state.user


def require_auth():
    """Require authentication to access page."""
    init_auth_state()
    
    if not st.session_state.authenticated:
        show_login_required()
        st.stop()
    
    return st.session_state.user


def show_login_required():
    """Show login required message."""
    st.warning("🔐 **Login Diperlukan** - Silakan login untuk mengakses fitur ini")
    
    with st.form("quick_login"):
        st.markdown("### 🔑 Quick Login")
        username = st.text_input("Username", placeholder="admin / demo / petani")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login", use_container_width=True, type="primary"):
            success, message = login(username, password)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    st.caption("Demo: admin/admin123, demo/demo123, petani/petani123")


def show_user_info_sidebar():
    """Show current user info in sidebar."""
    if is_authenticated():
        user = get_current_user()
        role_icon = '👑' if user['role'] == 'superadmin' else ('🛡️' if user['role'] == 'admin' else '👤')
        st.sidebar.success(f"{role_icon} **{user['name']}** ({user['role']})")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
