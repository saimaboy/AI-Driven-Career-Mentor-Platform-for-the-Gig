import streamlit as st
import database as db
import auth
from recommenders import recommend_courses, get_skill_gap_courses
import textwrap

# Initialize session state
auth.init_session_state()
if not auth.require_login():
    st.stop()

# Page config
st.set_page_config(
    page_title="Courses | FreelanceHub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS (including .view-button)
st.markdown(
    """
    <style>
    .main-header { font-size:2.5rem; color:#1E88E5; margin-bottom:0; }
    .sub-header  { font-size:1.2rem; color:#757575; margin-top:0; }
    .course-card {
      border:1px solid #e0e0e0; border-radius:.5rem;
      padding:1rem; margin-bottom:1rem; background:#fff;
    }
    .course-title {
      font-size:1.25rem; font-weight:bold;
      color:#1E88E5; margin-bottom:.5rem;
    }
    .course-provider { font-style:italic; color:#757575; }
    .course-price    { font-weight:bold; color:#4CAF50; }
    .course-skill {
      display:inline-block; background:#e3f2fd;
      color:#1E88E5; padding:.25rem .5rem; border-radius:1rem;
      font-size:.8rem; margin:.25rem .5rem .5rem 0;
    }
    .difficulty-badge {
      display:inline-block; padding:.25rem .5rem;
      border-radius:.25rem; font-size:.8rem; font-weight:bold;
      margin-left:.5rem;
    }
    .difficulty-beginner    { background:#C8E6C9; color:#2E7D32; }
    .difficulty-intermediate{ background:#FFECB3; color:#FF8F00; }
    .difficulty-advanced    { background:#FFCDD2; color:#C62828; }
    .recommended-badge {
      background:#FFC107; color:#212121; padding:.25rem .5rem;
      border-radius:.25rem; font-size:.8rem; font-weight:bold;
      margin-left:.5rem;
    }
    .skill-gap-badge {
      background:#E1BEE7; color:#6A1B9A; padding:.25rem .5rem;
      border-radius:.25rem; font-size:.8rem; font-weight:bold;
      margin-left:.5rem;
    }
    .view-button {
      border:1px solid #e0e0e0; background:transparent;
      color:#1E88E5; padding:.5rem 1rem; border-radius:.25rem;
      cursor:pointer;
    }
    .view-button:hover { background:#f1f1f1; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
def render_sidebar():
    with st.sidebar:
        st.image("https://freesvg.org/img/1538298822.png", width=100)
        st.title("FreelanceHub")
        st.success(f"Logged in as: {auth.get_current_username()}")
        # st.markdown("### Navigation")
        # st.page_link("app.py",              "📊 Dashboard",        icon="🏠")
        # st.page_link("pages/profile.py",    "👤 Profile & Skills", icon="👤")
        # st.page_link("pages/gigs.py",       "💼 Gigs",             icon="💼")
        # st.page_link("pages/courses.py",    "🎓 Courses",          icon="🎓")
        # st.page_link("pages/feed.py",       "📱 Feed",             icon="📱")
        # st.page_link("pages/support.py",    "🤖 Chatbot Support",  icon="🤖")
        if st.button("Logout"):
            auth.logout_user()
            st.rerun()

render_sidebar()

# Main
def main():
    st.markdown('<p class="main-header">Courses</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Discover courses to enhance your skills</p>', unsafe_allow_html=True)

    user_id     = auth.get_current_user_id()
    user_skills = db.get_user_skills(user_id)

    tab1, tab2, tab3 = st.tabs(["Recommended Courses", "Skill Gap Courses", "Browse All Courses"])
    with tab1: display_recommended_courses_tab(user_id, user_skills)
    with tab2: display_skill_gap_courses_tab(user_id, user_skills)
    with tab3: display_all_courses_tab(user_id)


def display_recommended_courses_tab(user_id, user_skills):
    st.subheader("Courses Recommended for You")
    if not user_skills:
        st.warning("Add skills to your profile to get personalized recommendations.")
        if st.button("Add Skills Now", key="add_skills_recommended"):
            st.switch_page("pages/profile.py")
        return

    recs = recommend_courses(user_id, limit=10)
    if recs:
        st.write("Based on your skill profile, we recommend these:")
        for c in recs:
            display_course_card(c, is_recommended=True)
    else:
        st.info("No recommended courses—try updating your skills.")


def display_skill_gap_courses_tab(user_id, user_skills):
    st.subheader("Courses to Fill Your Skill Gaps")
    if not user_skills:
        st.warning("Add skills to your profile to get skill gap recommendations.")
        if st.button("Add Skills Now", key="add_skills_skillgap"):
            st.switch_page("pages/profile.py")
        return

    gaps = get_skill_gap_courses(user_id, limit=10)
    if gaps:
        st.write("Based on market demand, these can fill your gaps:")
        for c in gaps:
            display_course_card(c, is_skill_gap=True)
    else:
        st.info("No skill-gap courses found; you may already be well-rounded!")


def display_all_courses_tab(user_id):
    st.subheader("Browse All Courses")

    # 1) get only the skills that have ≥1 course
    conn   = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT s.id, s.name, s.category
        FROM skills s
        JOIN course_skills cs ON s.id = cs.skill_id
    """)
    all_skills = [dict(row) for row in cursor.fetchall()]
    conn.close()

    # Filters UI
    with st.expander("Filters", expanded=False):
        cat_list = sorted({s["category"] for s in all_skills})
        col1, col2, col3 = st.columns(3)

        with col1:
            selected_category = st.selectbox("Filter by Category", ["All Categories"] + cat_list)

        with col2:
            skills_in_cat = [s for s in all_skills
                             if selected_category=="All Categories" or s["category"]==selected_category]
            skill_opts = [f"{s['name']} ({s['category']})" for s in skills_in_cat]
            selected_skill = st.selectbox("Filter by Skill", ["All Skills"] + skill_opts)

        with col3:
            levels = ["All Levels", "Beginner", "Intermediate", "Advanced"]
            selected_difficulty = st.selectbox("Filter by Difficulty", levels)

    # Build SQL query
    query_parts = ["SELECT c.id FROM courses c"]
    params = []

    if selected_skill != "All Skills":
        skill_name = selected_skill.split(" (")[0]
        skill_id   = next(s["id"] for s in all_skills if s["name"]==skill_name)
        query_parts.append("JOIN course_skills cs ON c.id = cs.course_id")
        query_parts.append("WHERE cs.skill_id = ?")
        params.append(skill_id)
    elif selected_category != "All Categories":
        ids = [s["id"] for s in all_skills if s["category"]==selected_category]
        placeholders = ",".join("?"*len(ids))
        query_parts.append("JOIN course_skills cs ON c.id = cs.course_id")
        query_parts.append(f"WHERE cs.skill_id IN ({placeholders})")
        params += ids

    if selected_difficulty!="All Levels":
        clause = "AND" if "WHERE" in " ".join(query_parts) else "WHERE"
        query_parts.append(f"{clause} c.difficulty_level = ?")
        params.append(selected_difficulty)

    query_parts.append("GROUP BY c.id")
    query = " ".join(query_parts)

    # Execute & fetch
    conn   = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    course_ids = [r[0] for r in cursor.fetchall()]

    # Load full course objects
    courses = []
    for cid in course_ids:
        cursor.execute("""
            SELECT id, title, description, provider, url, difficulty_level, duration, price
            FROM courses WHERE id=?
        """, (cid,))
        c = dict(cursor.fetchone())

        cursor.execute("""
            SELECT s.id, s.name, s.category
            FROM skills s JOIN course_skills cs ON s.id=cs.skill_id
            WHERE cs.course_id=?
        """, (cid,))
        c["skills"] = [dict(r) for r in cursor.fetchall()]
        courses.append(c)

    conn.close()

    if courses:
        for c in courses:
            display_course_card(c)
    else:
        st.info("No courses match your filters.")


def display_course_card(course, is_recommended=False, is_skill_gap=False):
    # build outer HTML with zero indent
    raw = f"""\
<div class="course-card">
  <div class="course-title">
    {course['title']}
    {'<span class="recommended-badge">Recommended</span>' if is_recommended else ''}
    {'<span class="skill-gap-badge">Skill Gap</span>' if is_skill_gap else ''}
    <span class="difficulty-badge difficulty-{course['difficulty_level'].lower()}">
      {course['difficulty_level']}
    </span>
  </div>
  <p class="course-provider">
    {course['provider']} | {course['duration']}
  </p>
  <p>{course['description'][:200]}{'...' if len(course['description'])>200 else ''}</p>
  <p class="course-price">
    {'Free' if course['price']==0 else f'${course["price"]:.2f}'}
  </p>
  <div>
    {"".join(f'<span class="course-skill">{s["name"]}</span>' for s in course['skills'])}
  </div>
  <div style="text-align:right; margin-top:.5rem;">
    <a href="{course['url']}" target="_blank">
      <button class="view-button">View Course</button>
    </a>
  </div>
</div>
"""
    # remove any lingering indentation & render
    html = textwrap.dedent(raw)
    html = "\n".join(line.lstrip() for line in html.splitlines())
    st.markdown(html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
