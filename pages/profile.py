import streamlit as st
import database as db
import auth
import os
import time
from datetime import datetime

# Initialize session state
auth.init_session_state()

# Check if user is logged in
if not auth.require_login():
    st.stop()

# Set page configuration
st.set_page_config(
    page_title="Profile & Skills | FreelanceHub",
    page_icon="👤",
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
    .skill-chip {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        border-radius: 1rem;
        background-color: #e3f2fd;
        color: #1E88E5;
        font-size: 0.875rem;
    }
    .proficiency-beginner {
        background-color: #ECEFF1;
        border-left: 4px solid #9E9E9E;
    }
    .proficiency-intermediate {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    .proficiency-advanced {
        background-color: #E8F5E9;
        border-left: 4px solid #4CAF50;
    }
    .proficiency-expert {
        background-color: #FFF3E0;
        border-left: 4px solid #FF9800;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar
def render_sidebar():
    with st.sidebar:
        st.image("https://freesvg.org/img/1538298822.png", width=100)
        st.title("FreelanceHub")

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


render_sidebar()


# Main content
def main():
    st.markdown('<p class="main-header">Profile & Skills</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage your profile and skills</p>', unsafe_allow_html=True)

    # Get user data
    user_id = auth.get_current_user_id()
    user = db.get_user_by_id(user_id)
    user_skills = db.get_user_skills(user_id)

    # Create tabs
    tab1, tab2 = st.tabs(["Profile Information", "Skills Management"])

    with tab1:
        display_profile_tab(user)

    with tab2:
        display_skills_tab(user_id, user_skills)


def display_profile_tab(user):
    st.subheader("Personal Information")

    with st.form("profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            username = st.text_input("Username", value=user['username'], disabled=True)
            email = st.text_input("Email", value=user['email'])

        with col2:
            full_name = st.text_input("Full Name", value=user.get('full_name', ''))

        bio = st.text_area("Bio", value=user.get('bio', ''), height=150,
                           placeholder="Write a short bio about yourself, your experience, and what you specialize in...")

        submit_button = st.form_submit_button("Update Profile")

        if submit_button:
            # Update profile in the database
            conn = db.get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("""
                               UPDATE users
                               SET email     = ?,
                                   full_name = ?,
                                   bio       = ?
                               WHERE id = ?
                               """, (email, full_name, bio, user['id']))

                conn.commit()
                st.success("Profile updated successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                conn.close()

    st.subheader("Account Information")

    joined_date = datetime.strptime(user['join_date'], "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y")

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.markdown(f"""
        <div class="card">
            <p><strong>Member Since:</strong> {joined_date}</p>
            <p><strong>Account Type:</strong> Freelancer</p>
        </div>
        """, unsafe_allow_html=True)


def display_skills_tab(user_id, user_skills):
    st.subheader("Your Skills")

    # Create a dictionary of user skills for easy lookup
    user_skills_dict = {}
    for skill in user_skills:
        user_skills_dict[skill['id']] = {
            'proficiency_level': skill.get('proficiency_level', 'Beginner'),
            'years_experience': skill.get('years_experience', 0)
        }

    # Get all available skills by category
    skills_by_category = db.get_skills_by_category()

    # Create a form for skills management
    with st.form("skills_form"):
        st.markdown("Select your skills and set your proficiency level:")

        # Store selected skills in a list
        selected_skills = []

        # Create an expander for each skill category
        for category, skills in skills_by_category.items():
            with st.expander(f"{category} Skills",
                             expanded=category in [cat['category'] for cat in user_skills] if user_skills else False):
                for skill in skills:
                    skill_id = skill['id']
                    skill_name = skill['name']

                    # Check if user already has this skill
                    has_skill = skill_id in user_skills_dict

                    if has_skill:
                        default_proficiency = user_skills_dict[skill_id]['proficiency_level']
                        default_years = user_skills_dict[skill_id]['years_experience']
                    else:
                        default_proficiency = "Beginner"
                        default_years = 0

                    col1, col2, col3 = st.columns([3, 2, 1])

                    with col1:
                        has_this_skill = st.checkbox(skill_name, value=has_skill, key=f"skill_{skill_id}")

                    with col2:
                        # Changed: Remove the disabled parameter so it's always enabled
                        proficiency = st.selectbox(
                            "Level",
                            options=["Beginner", "Intermediate", "Advanced", "Expert"],
                            index=["Beginner", "Intermediate", "Advanced", "Expert"].index(default_proficiency),
                            key=f"prof_{skill_id}"
                        )

                    with col3:
                        # Changed: Remove the disabled parameter so it's always enabled
                        years = st.number_input(
                            "Years",
                            min_value=0,
                            max_value=30,
                            value=default_years,
                            step=1,
                            key=f"years_{skill_id}"
                        )

                    # Changed: Only add to selected_skills if the checkbox is checked
                    if has_this_skill:
                        selected_skills.append({
                            'skill_id': skill_id,
                            'proficiency_level': proficiency,
                            'years_experience': years
                        })

        submit_button = st.form_submit_button("Save Skills")

        if submit_button:
            # Update skills in the database
            try:
                db.update_user_skills(user_id, selected_skills)
                st.success("Skills updated successfully!")

                # Add a short delay and then rerun the app to refresh the display
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Display current skills summary
    if user_skills:
        st.subheader("Your Skills Summary")

        # Group skills by proficiency level
        skills_by_proficiency = {
            'Expert': [],
            'Advanced': [],
            'Intermediate': [],
            'Beginner': []
        }

        for skill in user_skills:
            proficiency = skill.get('proficiency_level', 'Beginner')
            skills_by_proficiency[proficiency].append(skill)

        # Display skills by proficiency
        for proficiency, skills in skills_by_proficiency.items():
            if skills:
                st.markdown(f"#### {proficiency} Level Skills")

                skill_html = "<div style='display: flex; flex-wrap: wrap;'>"
                for skill in skills:
                    skill_html += f"<div class='skill-chip proficiency-{proficiency.lower()}'>{skill['name']} ({skill.get('years_experience', 0)} yr{'s' if skill.get('years_experience', 0) != 1 else ''})</div>"
                skill_html += "</div>"

                st.markdown(skill_html, unsafe_allow_html=True)
    else:
        st.info("You haven't added any skills yet. Add skills to improve your profile and get better recommendations.")



if __name__ == "__main__":
    main()