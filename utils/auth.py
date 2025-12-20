"""
Authentication utility for AgriSensa Streamlit
Provides database-backed authentication with session fallback
"""

import streamlit as st
import requests
from datetime import datetime
import os

# ========== API CONFIGURATION ==========
# Try to get API URL from environment or use default
API_BASE_URL = os.getenv('API_URL', 'https://agriisensa.vercel.app/api')

# ========== DEFAULT USERS (Fallback) ==========
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


def api_request(endpoint: str, method: str = 'GET', data: dict = None) -> dict:
    """Make API request with error handling."""
    try:
        url = f"{API_BASE_URL}/auth/{endpoint}"
        if method == 'GET':
            response = requests.get(url, params=data, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        return {'success': False, 'message': f'API Error: {str(e)}', 'api_error': True}


def get_users():
    """Get users from API or session state fallback."""
    if 'registered_users' not in st.session_state:
        st.session_state.registered_users = DEFAULT_USERS.copy()
    
    # Try to get from API
    result = api_request('users-list')
    if result.get('success') and result.get('users'):
        # Merge API users with session users
        for user in result['users']:
            username = user.get('username', '').lower()
            if username and username not in st.session_state.registered_users:
                st.session_state.registered_users[username] = {
                    'password': '***',  # Hidden
                    'role': user.get('role', 'user'),
                    'name': user.get('full_name') or user.get('username'),
                    'email': user.get('email', '')
                }
    
    return st.session_state.registered_users


def get_activity_log():
    """Get user activity log from API or session state."""
    if 'user_activity_log' not in st.session_state:
        st.session_state.user_activity_log = []
    
    # Try to get from API
    result = api_request('activities')
    if result.get('success') and result.get('activities'):
        return result['activities']
    
    return st.session_state.user_activity_log


def log_user_activity(username: str, action: str, details: str = ""):
    """Log user activity to API and session."""
    # Log to session
    log = st.session_state.get('user_activity_log', [])
    log.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'username': username,
        'action': action,
        'details': details
    })
    st.session_state.user_activity_log = log
    
    # Try to log to API
    api_request('log-activity', 'POST', {
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
    if 'user_activity_log' not in st.session_state:
        st.session_state.user_activity_log = []
    get_users()


def login(username: str, password: str) -> tuple[bool, str]:
    """
    Authenticate user with database API.
    Falls back to session if API unavailable.
    """
    init_auth_state()
    
    if not username or not password:
        return False, "Username dan password harus diisi"
    
    username = username.strip().lower()
    
    # Try API login first
    result = api_request('simple-login', 'POST', {
        'username': username,
        'password': password
    })
    
    if result.get('success'):
        user_data = result.get('user', {})
        st.session_state.authenticated = True
        st.session_state.user = {
            'username': user_data.get('username', username),
            'name': user_data.get('name', username),
            'role': user_data.get('role', 'user'),
            'email': user_data.get('email', '')
        }
        return True, result.get('message', 'Login berhasil!')
    
    # If API error (not auth failure), try fallback
    if result.get('api_error'):
        users = st.session_state.get('registered_users', DEFAULT_USERS)
        if username in users:
            if users[username]['password'] == password:
                st.session_state.authenticated = True
                st.session_state.user = {
                    'username': username,
                    'name': users[username]['name'],
                    'role': users[username]['role'],
                    'email': users[username]['email']
                }
                log_user_activity(username, 'LOGIN', 'Login via fallback')
                return True, f"Selamat datang, {users[username]['name']}!"
            else:
                return False, "Password salah"
        return False, "Username tidak ditemukan"
    
    return False, result.get('message', 'Login gagal')


def logout():
    """Logout current user."""
    if st.session_state.get('user'):
        log_user_activity(st.session_state.user['username'], 'LOGOUT', 'User logout')
    st.session_state.authenticated = False
    st.session_state.user = None


def register(username: str, password: str, name: str, email: str) -> tuple[bool, str]:
    """Register a new user via API with session fallback."""
    init_auth_state()
    
    if not username or not password or not name:
        return False, "Username, password, dan nama harus diisi"
    
    if len(username) < 3:
        return False, "Username minimal 3 karakter"
    
    if len(password) < 6:
        return False, "Password minimal 6 karakter"
    
    username = username.strip().lower()
    
    # Try API register first
    result = api_request('simple-register', 'POST', {
        'username': username,
        'password': password,
        'name': name,
        'email': email
    })
    
    if result.get('success'):
        user_data = result.get('user', {})
        st.session_state.authenticated = True
        st.session_state.user = {
            'username': user_data.get('username', username),
            'name': user_data.get('name', name),
            'role': user_data.get('role', 'user'),
            'email': user_data.get('email', email)
        }
        return True, result.get('message', 'Registrasi berhasil!')
    
    # If API error, try session fallback
    if result.get('api_error'):
        users = st.session_state.get('registered_users', {})
        if username in users:
            return False, "Username sudah digunakan"
        
        users[username] = {
            'password': password,
            'role': 'user',
            'name': name,
            'email': email or f"{username}@agrisensa.com"
        }
        st.session_state.registered_users = users
        st.session_state.authenticated = True
        st.session_state.user = {
            'username': username,
            'name': name,
            'role': 'user',
            'email': email or f"{username}@agrisensa.com"
        }
        log_user_activity(username, 'REGISTER', 'Register via fallback')
        return True, f"Selamat datang, {name}! Akun berhasil dibuat."
    
    return False, result.get('message', 'Registrasi gagal')


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
        .login-icon { font-size: 4rem; margin-bottom: 1rem; }
        .login-title { font-size: 1.5rem; font-weight: 700; color: #92400e; margin-bottom: 0.5rem; }
        .login-message { color: #a16207; margin-bottom: 1.5rem; }
    </style>
    <div class="login-required">
        <div class="login-icon">🔐</div>
        <div class="login-title">Login Diperlukan</div>
        <div class="login-message">Silakan login untuk mengakses fitur ini</div>
    </div>
    """, unsafe_allow_html=True)
    
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
        role_icon = '👑' if user['role'] == 'superadmin' else ('🛡️' if user['role'] == 'admin' else '👤')
        st.sidebar.markdown(f"""
        <div style="padding: 1rem; background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                    border-radius: 12px; margin-bottom: 1rem; border: 1px solid #10b981;">
            <div style="font-weight: 700; color: #065f46;">{role_icon} {user['name']}</div>
            <div style="font-size: 0.8rem; color: #047857;">{user['role'].upper()}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
