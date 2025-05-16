import streamlit as st
import database as db
from datetime import datetime, timedelta
import time

def init_session_state():
    """Initialize session state variables for authentication"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'login_time' not in st.session_state:
        st.session_state.login_time = None

def login_user(username, password):
    """Log in a user"""
    user_id = db.validate_login(username, password)
    if user_id:
        st.session_state.logged_in = True
        st.session_state.user_id = user_id
        st.session_state.username = username
        st.session_state.login_time = datetime.now()
        return True
    return False

def logout_user():
    """Log out a user"""
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.login_time = None

def register_user(username, email, password, full_name=None, bio=None):
    """Register a new user"""
    user_id = db.create_user(username, email, password, full_name, bio)
    if user_id:
        st.session_state.logged_in = True
        st.session_state.user_id = user_id
        st.session_state.username = username
        st.session_state.login_time = datetime.now()
        return True
    return False

def is_logged_in():
    """Check if a user is logged in"""
    return st.session_state.logged_in

def get_current_user_id():
    """Get the current user ID"""
    return st.session_state.user_id if is_logged_in() else None

def get_current_username():
    """Get the current username"""
    return st.session_state.username if is_logged_in() else None

def require_login():
    """Require user to be logged in, redirect to login page if not"""
    if not is_logged_in():
        st.warning("⚠️ You need to login to access this page.")
        time.sleep(2)  # Give time for the warning to be visible
        st.switch_page("app.py")
        return False
    return True

def check_session_expiry(expiry_hours=24):
    """Check if the session has expired and log out if it has"""
    if is_logged_in() and st.session_state.login_time:
        expiry_time = st.session_state.login_time + timedelta(hours=expiry_hours)
        if datetime.now() > expiry_time:
            logout_user()
            st.warning("Your session has expired. Please log in again.")
            time.sleep(2)
            st.rerun()