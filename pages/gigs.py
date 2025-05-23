import streamlit as st
import database as db
import database_gig as db_gig
import auth
import time
from datetime import datetime
from recommenders import recommend_gigs


# Initialize session state
auth.init_session_state()

# Check if user is logged in
if not auth.require_login():
    st.stop()

# Prep our custom tab index + suggestion state
if "active_gig_tab" not in st.session_state:
    st.session_state.active_gig_tab = 0    # 0=Explore,1=My,2=Create,3=Picked
if "dismissed_gigs" not in st.session_state:
    st.session_state.dismissed_gigs = set()
if "prefill_gig" not in st.session_state:
    st.session_state.prefill_gig = {}

# Page config
st.set_page_config(
    page_title="Gigs | FreelanceHub",
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
    .gig-card {
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: white;
    }
    .gig-title {
        font-size: 1.25rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .gig-price {
        font-weight: bold;
        color: #4CAF50;
    }
    .gig-skill {
        display: inline-block;
        background-color: #e3f2fd;
        color: #1E88E5;
        padding: 0.25rem 0.5rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .recommended-badge {
        background-color: #FFC107;
        color: #212121;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
    .picked-badge {
        background-color: #4CAF50;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
    .comment-card {
        padding: 0.75rem;
        background-color: #f5f5f5;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .comment-author {
        font-weight: bold;
        color: #1E88E5;
    }
    .comment-date {
        color: #757575;
        font-size: 0.8rem;
    }
    .file-card {
        border: 1px solid #e0e0e0;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin-bottom: 0.5rem;
        background-color: #f9f9f9;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .file-name {
        color: #1E88E5;
        font-weight: bold;
    }
    .file-size {
        color: #757575;
        font-size: 0.8rem;
    }
    .recommended-badge {
        background: #FFC107;
        color: #212121;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
      }
      .picked-badge {
        background: #4CAF50;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
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
    st.markdown('<p class="main-header">Gigs</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Create and explore freelance gigs</p>', unsafe_allow_html=True)

    # Get user data
    user_id = auth.get_current_user_id()
    user_skills = db.get_user_skills(user_id)

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Explore Gigs", "My Gigs", "Create New Gig", "Picked Gigs"])

    with tab1:
        display_explore_gigs_tab(user_id, user_skills)

    with tab2:
        display_my_gigs_tab(user_id)

    with tab3:
        display_create_gig_tab(user_id, user_skills)

    with tab4:
        display_picked_gigs_tab(user_id)


def display_explore_gigs_tab(user_id, user_skills):
    st.subheader("Explore Gigs")

    # Filters
    with st.expander("Filters", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            # Get skill categories
            all_skills = db.get_skills()
            categories = list(set([skill['category'] for skill in all_skills]))
            categories.sort()

            selected_category = st.selectbox("Filter by Category", ["All Categories"] + categories)

        with col2:
            # Get skills based on selected category
            if selected_category != "All Categories":
                category_skills = [skill for skill in all_skills if skill['category'] == selected_category]
            else:
                category_skills = all_skills

            skill_options = [f"{skill['name']} ({skill['category']})" for skill in category_skills]
            selected_skill_option = st.selectbox("Filter by Skill", ["All Skills"] + skill_options)

    # Recommended Gigs Section
    st.markdown("### Recommended for You")
    if user_skills:
        from recommenders import recommend_gigs
        recommended_gigs = recommend_gigs(user_id, 5)

        if recommended_gigs:
            for gig in recommended_gigs:
                display_gig_card(gig, user_id)
        else:
            st.info("No recommended gigs yet. Try updating your skills or check back later.")
    else:
        st.warning("Add skills to your profile to get personalized recommendations.")
        if st.button("Add Skills"):
            st.switch_page("pages/profile.py")

    # All Gigs Section
    st.markdown("### All Gigs")

    # Prepare filters
    filters = {}
    if selected_category != "All Categories":
        # Get skill IDs for the selected category
        category_skill_ids = [skill['id'] for skill in all_skills if skill['category'] == selected_category]
        filters['skill_ids'] = category_skill_ids

    if selected_skill_option != "All Skills":
        # Extract skill name from the option
        selected_skill_name = selected_skill_option.split(" (")[0]
        # Find the skill ID
        selected_skill_id = next((skill['id'] for skill in all_skills if skill['name'] == selected_skill_name), None)
        if selected_skill_id:
            filters['skill_ids'] = [selected_skill_id]

    # Get gigs based on filters
    all_gigs = db.get_gigs(limit=50, **filters)

    if all_gigs:
        # Remove gigs that are already in recommended section
        if 'recommended_gigs' in locals() and recommended_gigs:
            recommended_gig_ids = [gig['id'] for gig in recommended_gigs]
            all_gigs = [gig for gig in all_gigs if gig['id'] not in recommended_gig_ids]

        for gig in all_gigs:
            display_gig_card(gig, user_id)
    else:
        st.info("No gigs found with the selected filters.")


def display_my_gigs_tab(user_id):
    st.subheader("My Gigs")

    # Get user's gigs
    user_gigs = db.get_gigs(user_id=user_id)

    if user_gigs:
        # Loop through gigs with an index for unique keys
        for index, gig in enumerate(user_gigs):
            with st.container():
                st.markdown(f"""
                <div class="gig-card">
                    <div class="gig-title">{gig['title']}</div>
                    <p>{gig['description']}</p>
                    <p class="gig-price">Price: ${gig['price_min']} - ${gig['price_max']}</p>
                    <p>Duration: {gig['duration']}</p>
                    <p>Created: {gig['created_at']}</p>
                    <p>Skills: {', '.join([skill['name'] for skill in gig['skills']])}</p>
                    <p>Status: {gig['status'].capitalize()}</p>
                </div>
                """, unsafe_allow_html=True)

                # Display the number of users who picked this gig
                picked_count = db_gig.get_gig_picks_count(gig['id'])
                if picked_count > 0:
                    st.write(f"**{picked_count}** user{'s' if picked_count != 1 else ''} picked this gig")

                # Show gig comments with unique context based on index
                with st.expander("Comments", expanded=False):
                    display_gig_comments(gig['id'], user_id, context=f"my_gigs_{index}")

                # Show file uploads with unique context based on index
                with st.expander("Files", expanded=False):
                    display_gig_files(gig['id'], user_id, context=f"my_gigs_{index}", is_owner=True)
    else:
        st.info("You haven't created any gigs yet.")

        with st.expander("Tips for Creating Successful Gigs", expanded=True):
            st.markdown("""
            ### Tips for Creating Successful Gigs

            1. **Write a clear, specific title** that includes your main skill and deliverable
            2. **Break down your services** into different packages or tiers
            3. **Be specific about what's included** and what costs extra
            4. **Add eye-catching visuals** that showcase your work
            5. **Highlight your unique selling point** - what makes your service special
            """)

    # Button to create new gig
    if st.button("Create New Gig"):
        # Switch to create gig tab
        st.session_state.tabs_default = 2
        st.rerun()


def display_create_gig_tab(user_id, user_skills):
    st.subheader("Create a New Gig")

    # Ensure session state variables are initialized
    if "dismissed_gigs" not in st.session_state:
        st.session_state.dismissed_gigs = set()
    if "prefill_gig" not in st.session_state:
        st.session_state.prefill_gig = {}

    if not user_skills:
        st.warning("You need to add skills to your profile before creating a gig.")
        if st.button("Add Skills Now"):
            st.switch_page("pages/profile.py")
        return

    # 2) Build raw suggestions
    raw = recommend_gigs(user_id, limit=10) or []
    existing = {g["id"] for g in db.get_gigs(user_id=user_id)}
    suggestions = [
        g for g in raw
        if g["id"] not in existing
           and g["id"] not in st.session_state.dismissed_gigs
    ]

    # 3) Fallback (filtered)
    if not suggestions:
        fallback = []
        for skill in user_skills[:5]:
            tpl_id = f"tpl_{skill['id']}"
            if tpl_id in st.session_state.dismissed_gigs:
                continue
            fallback.append({
                "id": tpl_id,
                "title": f"I will provide professional {skill['name']} services",
                "description": "...",
                "price_min": 50.0,  # Use float for consistency
                "price_max": 150.0,  # Use float for consistency
                "duration": "3-5 days",
                "skills": [skill["id"]],
            })
        suggestions = fallback

    # --- 4) Render the panel if we have ANY suggestions ---
    if suggestions:
        st.subheader("✏️ Gig Ideas for You")
        for gig in suggestions[:5]:
            st.markdown(f"**{gig['title']}**  \n{gig['description'][:150]}…")
            c1, c2 = st.columns(2)

            # Callback to prefill, normalizing skills → always a list of ints
            def _use_template(gig=gig):
                raw_skills = gig.get("skills", [])
                skill_ids = [
                    s["id"] if isinstance(s, dict) else s
                    for s in raw_skills
                ]
                st.session_state.prefill_gig = {
                    "title": gig["title"],
                    "description": gig["description"],
                    "price_min": gig["price_min"],
                    "price_max": gig["price_max"],
                    "duration": gig["duration"],
                    "skills": skill_ids,
                }

            c1.button("Use as Template", key=f"use_{gig['id']}", on_click=_use_template)

            def _dismiss(gig_id=gig["id"]):
                st.session_state.dismissed_gigs.add(gig_id)

            c2.button("Dismiss", key=f"dismiss_{gig['id']}", on_click=_dismiss)

    # 2) Prefill values
    pre = st.session_state.prefill_gig
    default_title       = pre.get("title", "")
    default_description = pre.get("description", "")
    default_price_min   = pre.get("price_min", 50.0)  # Ensure float
    default_price_max   = pre.get("price_max", 100.0)  # Ensure float
    default_duration    = pre.get("duration", "1 week")
    default_skills      = set(pre.get("skills", []))

    # 3) Creation form
    with st.form("create_gig_form"):
        title = st.text_input("Gig Title", value=default_title, placeholder="I will...")
        description = st.text_area(
            "Description",
            value=default_description,
            height=200,
            placeholder="Describe your services in detail…"
        )

        col1, col2 = st.columns(2)

        with col1:
            price_min = st.number_input(
                "Minimum Price ($)", min_value=1.0, max_value=10000.0,  # Use float
                value=default_price_min
            )
        with col2:
            price_max = st.number_input(
                "Maximum Price ($)", min_value=1.0, max_value=10000.0,  # Use float
                value=default_price_max
            )

        durations = ["1 day", "2-3 days", "3-5 days", "1 week", "2 weeks", "1 month", "Custom"]
        idx = durations.index(default_duration) if default_duration in durations else len(durations)-1
        duration = st.selectbox("Delivery Time", durations, index=idx)
        if duration == "Custom":
            custom = st.text_input("Specify Custom Duration", value=default_duration)
            duration = custom or default_duration

        # Skills selection
        st.subheader("Select Related Skills")
        skills_by_cat = {}
        for s in user_skills:
            skills_by_cat.setdefault(s["category"], []).append(s)

        selected_skill_ids = []
        for cat, skills in skills_by_cat.items():
            st.markdown(f"**{cat}**")
            cols = st.columns(3)
            for i, skill in enumerate(skills):
                checked = skill["id"] in default_skills
                if cols[i % 3].checkbox(skill["name"], value=checked, key=f"gig_skill_{skill['id']}"):
                    selected_skill_ids.append(skill["id"])

        submit = st.form_submit_button("Create Gig")
        if submit:
            if not title or not description:
                st.error("Please provide both title and description.")
            elif price_min > price_max:
                st.error("Minimum price cannot exceed maximum price.")
            elif not selected_skill_ids:
                st.error("Please select at least one skill.")
            else:
                new_id = db.create_gig(
                    user_id, title, description,
                    price_min, price_max, duration,
                    selected_skill_ids
                )
                if new_id:
                    st.success("Gig created successfully!")
                    # Clear prefill and jump back to My Gigs
                    st.session_state.prefill_gig = {}
                    st.session_state.active_gig_tab = 1
                    time.sleep(1)
                    # Switch to "My Gigs" tab
                    st.session_state.tabs_default = 1
                    st.rerun()
                else:
                    st.error("An error occurred while creating the gig. Please try again.")

def display_picked_gigs_tab(user_id):
    st.subheader("Gigs You've Picked")

    # Get gigs picked by the user
    picked_gigs = db_gig.get_user_picked_gigs(user_id)

    if picked_gigs:
        # Loop through picked gigs with an index for unique keys
        for index, gig in enumerate(picked_gigs):
            with st.container():
                # Display the gig
                st.markdown(f"""
                <div class="gig-card">
                    <div class="gig-title">
                        {gig['title']}
                        <span class="picked-badge">Picked</span>
                    </div>
                    <p><strong>By:</strong> {gig['username']}</p>
                    <p>{gig['description'][:200]}{'...' if len(gig['description']) > 200 else ''}</p>
                    <p class="gig-price">Price: ${gig['price_min']} - ${gig['price_max']}</p>
                    <p>Duration: {gig['duration']}</p>
                    <div>
                        {''.join([f'<span class="gig-skill">{skill["name"]}</span>' for skill in gig['skills']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Unpick button with unique key
                if st.button("Unpick This Gig", key=f"unpick_{gig['id']}_{index}"):
                    db_gig.unpick_gig(user_id, gig['id'])
                    st.success("Gig unpicked successfully!")
                    time.sleep(1)
                    st.rerun()

                # Show gig comments with unique context based on index
                with st.expander("Comments", expanded=True):
                    display_gig_comments(gig['id'], user_id, context=f"picked_gigs_{index}")

                # Show file uploads with unique context based on index
                with st.expander("Files", expanded=True):
                    display_gig_files(gig['id'], user_id, context=f"picked_gigs_{index}")
    else:
        st.info("You haven't picked any gigs yet. Browse the 'Explore Gigs' tab to find gigs you're interested in.")


def display_gig_card(gig, user_id):
    """
    Render one gig card.
    Only the gig-owner or a user who picked the gig will see the comments & files.
    """
    gig_id   = gig['id']
    owner_id = gig['user_id']

    is_picked = db_gig.has_user_picked_gig(user_id, gig_id)
    is_recommended = gig.get('is_recommended', False)
    recommended_badge = (
        '<span class="recommended-badge">Recommended</span>'
        if is_recommended else
        ""
    )
    picked_badge = (
        '<span class="picked-badge">Picked</span>'
        if is_picked else
        ""
    )

    # --- 1) Basic gig info ---
    st.markdown(f"""
    <div style="border:1px solid #e0e0e0; border-radius:.5rem; padding:1rem; background:#fff; margin-bottom:1rem;">
      <div style="font-size:1.25rem; font-weight:bold; color:#1E88E5;">
        {gig['title']}
        {recommended_badge}
    {picked_badge}
      </div>
      <p><strong>By:</strong> {gig['username']}</p>
      <p>{gig['description'][:200]}{'...' if len(gig['description'])>200 else ''}</p>
      <p style="font-weight:bold; color:#4CAF50;">Price: ${gig['price_min']} - ${gig['price_max']}</p>
      <p>Duration: {gig['duration']}</p>
      <div>
        {''.join(f'<span style="display:inline-block;background:#e3f2fd;color:#1E88E5;padding:.25rem .5rem;border-radius:1rem;font-size:.8rem;margin:.25rem .5rem .5rem 0;">{s["name"]}</span>' for s in gig['skills'])}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 2) Pick / Unpick button ---

    if is_picked:
        if st.button("Unpick This Gig", key=f"unpick_{gig_id}"):
            db_gig.unpick_gig(user_id, gig_id)
            st.success("Gig unpicked.")
            st.rerun()
    else:
        if st.button("Pick This Gig", key=f"pick_{gig_id}"):
            db_gig.pick_gig(user_id, gig_id)
            st.success("Gig picked! You can now see comments & files.")
            st.rerun()

    # --- 3) Only show comments & files if owner or picker ---
    is_owner   = (owner_id == user_id)
    has_access = is_owner or is_picked

    if has_access:
        with st.expander("View Comments & Files", expanded=False):
            st.subheader("Comments")
            display_gig_comments(gig_id, user_id, context=f"explore_{gig_id}")

            st.subheader("Files")
            display_gig_files(gig_id, user_id, context=f"explore_{gig_id}", is_owner=is_owner)
    # if no access, we simply do nothing here (no expander, no info)


def display_gig_comments(gig_id, user_id, context="default"):
    """Display and add comments for a gig

    Args:
        gig_id (int): The ID of the gig
        user_id (int): The ID of the current user
        context (str): A context identifier to create unique form keys
    """
    # Get existing comments
    comments = db_gig.get_gig_comments(gig_id)

    if comments:
        for comment in comments:
            comment_date = datetime.strptime(comment['created_at'], "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")

            st.markdown(f"""
            <div class="comment-card">
                <div style="display: flex; justify-content: space-between;">
                    <span class="comment-author">{comment['username']}</span>
                    <span class="comment-date">{comment_date}</span>
                </div>
                <p>{comment['content']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No comments yet. Be the first to comment!")

    # Add new comment form with a unique key based on gig_id and context
    form_key = f"comment_form_{gig_id}_{context}"
    with st.form(key=form_key, clear_on_submit=True):
        comment_text = st.text_area("Add a comment", height=100,
                                    placeholder="Ask questions, discuss details, or provide feedback...")
        submit_comment = st.form_submit_button("Post Comment")

        if submit_comment and comment_text:
            # Add comment to database
            comment_id = db_gig.add_gig_comment(user_id, gig_id, comment_text)

            if comment_id:
                st.success("Comment added successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("An error occurred while adding your comment. Please try again.")


def display_gig_files(gig_id, user_id, context="default", is_owner=False):
    """Display and upload files for a gig

    Args:
        gig_id (int): The ID of the gig
        user_id (int): The ID of the current user
        context (str): A context identifier to create unique form keys
        is_owner (bool, optional): Whether the current user is the owner of the gig
    """
    # Get existing files
    files = db_gig.get_gig_files(gig_id)

    if files:
        st.subheader("Uploaded Files")
        for file in files:
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"""
                <div class="file-card">
                    <span class="file-name">{file['filename']}</span>
                    <span class="file-size">Uploaded by: {file['username']} on {datetime.strptime(file['uploaded_at'], "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")}</span>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                # Download button with unique key
                download_key = f"download_{file['id']}_{context}"
                st.download_button(
                    label="Download",
                    data=file['file_data'],
                    file_name=file['filename'],
                    mime="application/octet-stream",
                    key=download_key
                )
    else:
        st.info("No files uploaded yet.")

    # File upload form with a unique key
    form_key = f"file_form_{gig_id}_{context}"
    st.subheader("Upload a File")
    with st.form(key=form_key, clear_on_submit=True):
        uploaded_file = st.file_uploader("Choose a file",
                                         type=["pdf", "doc", "docx", "jpg", "jpeg", "png", "zip"],
                                         key=f"uploader_{gig_id}_{context}")
        file_description = st.text_input("File description (optional)")
        submit_file = st.form_submit_button("Upload File")

        if submit_file and uploaded_file:
            # Process the uploaded file
            file_data = uploaded_file.read()
            filename = uploaded_file.name

            # Add file to database
            file_id = db_gig.add_gig_file(user_id, gig_id, filename, file_data, file_description)

            if file_id:
                st.success("File uploaded successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("An error occurred while uploading your file. Please try again.")


# Main function to run the app
if __name__ == "__main__":
    # db_gig.init_gig_tables()
    main()