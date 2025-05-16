import streamlit as st
import database as db
import auth
import sqlite3
import os
from datetime import datetime
import textwrap

# Initialize the database
db.init_db()

# Initialize session state
auth.init_session_state()

# Set page configuration
st.set_page_config(
    page_title="FreelanceHub",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #757575;
        margin-top: 0;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .highlight-text {
        background-color: #e3f2fd;
        padding: 0.2rem 0.5rem;
        border-radius: 0.25rem;
    }
    .btn-primary {
        background-color: #1E88E5;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        text-decoration: none;
        display: inline-block;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
      /* hide header + built-in page nav */
      header {display: none;}
      nav[aria-label="page navigation"] {display: none;}
      /* optional: bump your sidebar up a bit */
      [data-testid="stSidebarNav"] { margin-top: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
def render_sidebar():
    with st.sidebar:
        st.image("https://freesvg.org/img/1538298822.png", width=100)
        st.title("FreelanceHub")

        if auth.is_logged_in():
            st.success(f"Logged in as: {auth.get_current_username()}")

            # st.markdown("### Navigation")
            # st.page_link("app.py", label="📊 Dashboard", icon="🏠")
            # st.page_link("pages/profile.py", label="👤 Profile & Skills", icon="👤")
            # st.page_link("pages/gigs.py", label="💼 Gigs", icon="💼")
            # st.page_link("pages/courses.py", label="🎓 Courses", icon="🎓")
            # st.page_link("pages/feed.py", label="📱 Feed", icon="📱")
            # st.page_link("pages/support.py", label="🤖 Chatbot Support", icon="🤖")

            if st.button("Logout"):
                auth.logout_user()
                st.rerun()
        else:
            st.info("Please login or create an account")


render_sidebar()


# Main content
def main():
    # Check if user is logged in
    if auth.is_logged_in():
        display_dashboard()
    else:
        display_login_page()


def display_login_page():
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<p class="main-header">FreelanceHub</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Your one-stop platform for freelancing success</p>', unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>📈 Grow Your Freelance Business</h3>
            <p>Create your profile, showcase your skills, and get personalized gig recommendations.</p>
        </div>
        <div class="card">
            <h3>🧠 Skill Up</h3>
            <p>Get course recommendations tailored to your skill profile and market demands.</p>
        </div>
        <div class="card">
            <h3>🤝 Connect</h3>
            <p>Share updates, like and comment on posts from other freelancers in the community.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            with st.form("login_form"):
                st.subheader("Login")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Login")

                if submit_login:
                    if username and password:
                        if auth.login_user(username, password):
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
                    else:
                        st.warning("Please enter both username and password")

        with tab2:
            with st.form("register_form"):
                st.subheader("Create an Account")
                new_username = st.text_input("Username", key="reg_username")
                new_email = st.text_input("Email", key="reg_email")
                new_password = st.text_input("Password", type="password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit_register = st.form_submit_button("Register")

                if submit_register:
                    if new_username and new_email and new_password:
                        if new_password != confirm_password:
                            st.error("Passwords do not match")
                        elif "@" not in new_email or "." not in new_email:
                            st.error("Please enter a valid email address")
                        else:
                            result = auth.register_user(new_username, new_email, new_password)
                            if result:
                                st.success("Registration successful! You are now logged in.")
                                st.rerun()
                            else:
                                st.error("Username or email already exists")
                    else:
                        st.warning("Please fill in all fields")


def display_dashboard():
    st.markdown('<p class="main-header">Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Welcome to your freelancing hub</p>', unsafe_allow_html=True)

    # Get user data
    user_id = auth.get_current_user_id()
    user = db.get_user_by_id(user_id)
    user_skills = db.get_user_skills(user_id)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if not user_skills:
            st.warning("Your profile is incomplete. Add your skills to get personalized recommendations.")
            if st.button("Complete Your Profile", use_container_width=True):
                st.switch_page("pages/profile.py")
        else:
            st.subheader("Your Skill Summary")

            # Group skills by category
            skills_by_category = {}
            for skill in user_skills:
                category = skill['category']
                if category not in skills_by_category:
                    skills_by_category[category] = []
                skills_by_category[category].append(skill)

            # Display skills by category with proficiency
            for category, skills in skills_by_category.items():
                with st.expander(f"{category} ({len(skills)})", expanded=True):
                    for skill in skills:
                        proficiency = skill.get('proficiency_level', 'Beginner')
                        years = skill.get('years_experience', 0)

                        # Determine color based on proficiency
                        if proficiency == 'Expert':
                            color = "#4CAF50"  # Green
                        elif proficiency == 'Advanced':
                            color = "#2196F3"  # Blue
                        elif proficiency == 'Intermediate':
                            color = "#FF9800"  # Orange
                        else:
                            color = "#9E9E9E"  # Grey

                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <div>{skill['name']}</div>
                            <div style="color: {color}; font-weight: bold;">{proficiency} ({years} yr{'s' if years != 1 else ''})</div>
                        </div>
                        """, unsafe_allow_html=True)

    with col2:
        st.subheader("Quick Actions")

        buttons = [
            ("Create New Gig", "pages/gigs.py"),
            ("Explore Courses", "pages/courses.py"),
            ("View Feed", "pages/feed.py"),
            ("Get Support", "pages/support.py")
        ]

        for label, page in buttons:
            button_col1, button_col2 = st.columns([4, 1])
            with button_col1:
                if st.button(label, use_container_width=True):
                    st.switch_page(page)

    with col3:
        st.subheader("Account Info")
        joined_date = datetime.strptime(user['join_date'], "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")

        st.markdown(f"""
        <div class="card" style="padding: 1rem;">
            <p><strong>Username:</strong> {user['username']}</p>
            <p><strong>Email:</strong> {user['email']}</p>
            <p><strong>Joined:</strong> {joined_date}</p>
        </div>
        """, unsafe_allow_html=True)

    # Recommendations section
    st.markdown('<p class="section-header">Personalized Recommendations</p>', unsafe_allow_html=True)

    if user_skills:
        from recommenders import recommend_gigs, recommend_courses

        # Get recommendations
        recommended_gigs = recommend_gigs(user_id, 3)
        recommended_courses = recommend_courses(user_id, 3)

        rec_col1, rec_col2 = st.columns(2)

        with rec_col1:
            st.subheader("Gig Recommendations")
            if recommended_gigs:
                for gig in recommended_gigs:
                    card = textwrap.dedent(f"""\
                    <a href="/gigs" style="text-decoration: none; color: inherit;">
                      <div class="card">
                        <h4>{gig['title']}</h4>
                        <p>{gig['description'][:100]}…</p>
                        <p><strong>Price Range:</strong> ${gig['price_min']} - ${gig['price_max']}</p>
                        <p><strong>Skills:</strong> {', '.join(s['name'] for s in gig['skills'])}</p>
                      </div>
                    </a>
                    """)
                    st.markdown(card, unsafe_allow_html=True)
            else:
                st.info("No gig recommendations yet. Try updating your skills or check back later.")

            if st.button("View All Gigs", use_container_width=True, key="dash_view_all_gigs"):
                st.switch_page("pages/gigs.py")

        with rec_col2:
            st.subheader("Course Recommendations")
            if recommended_courses:
                for course in recommended_courses:
                    card = textwrap.dedent(f"""\
                    <a href="/courses" style="text-decoration: none; color: inherit;">
                      <div class="card">
                        <h4>{course['title']}</h4>
                        <p>{course['description'][:100]}…</p>
                        <p><strong>Provider:</strong> {course['provider']}</p>
                        <p><strong>Level:</strong> {course['difficulty_level']}</p>
                        <p><strong>Skills:</strong> {', '.join(s['name'] for s in course['skills'])}</p>
                      </div>
                    </a>
                    """)
                    st.markdown(card, unsafe_allow_html=True)
            else:
                st.info("No course recommendations yet. Try updating your skills or check back later.")

            if st.button("View All Courses", use_container_width=True, key="dash_view_all_courses"):
                st.switch_page("pages/courses.py")
    else:
        st.info("Add skills to your profile to get personalized recommendations.")
        if st.button("Add Skills Now"):
            st.switch_page("pages/profile.py")

    # Recent activity from feed
    st.markdown('<p class="section-header">Recent Community Activity</p>', unsafe_allow_html=True)
    recent_posts = db.get_posts(limit=3)

    if recent_posts:
        for post in recent_posts:
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <p><strong>{post['username']}</strong> • {post['created_at']}</p>
                    <p>{post['content']}</p>
                    <p>❤️ {post['like_count']} likes • 💬 {len(post['comments'])} comments</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No posts yet. Be the first to share something with the community!")

    st.button("View Full Feed", on_click=lambda: st.switch_page("pages/feed.py"))


if __name__ == "__main__":
    main()