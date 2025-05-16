import streamlit as st
import database as db
import auth
import time
from datetime import datetime

# Initialize session state
auth.init_session_state()

# Check if user is logged in
if not auth.require_login():
    st.stop()

# Set page configuration
st.set_page_config(
    page_title="Feed | FreelanceHub",
    page_icon="📱",
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
    .post-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: white;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
        margin-bottom: 1.5rem;
        border: 1px solid #e0e0e0;
    }
    .post-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }
    .post-author {
        font-weight: bold;
        color: #1E88E5;
    }
    .post-date {
        color: #757575;
        font-size: 0.875rem;
    }
    .post-content {
        margin-bottom: 1.25rem;
    }
    .post-actions {
        display: flex;
        gap: 1rem;
    }
    .like-button {
        color: #F44336;
        cursor: pointer;
    }
    .comment-button {
        color: #1E88E5;
        cursor: pointer;
    }
    .like-count {
        color: #F44336;
        font-weight: bold;
    }
    .comment-count {
        color: #1E88E5;
        font-weight: bold;
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
    .section-header {
        font-size: 1.5rem;
        color: #1E88E5;
        margin-bottom: 1rem;
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

# Initialize or get session state variables
if "show_comments" not in st.session_state:
    st.session_state.show_comments = {}

if "new_comment" not in st.session_state:
    st.session_state.new_comment = {}


# Main content
def main():
    st.markdown('<p class="main-header">Feed</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Share and engage with other freelancers</p>', unsafe_allow_html=True)

    # Get user data
    user_id = auth.get_current_user_id()

    # Create columns layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Post creation form
        with st.form(key="create_post_form"):
            st.subheader("Create a Post")
            post_content = st.text_area(
                "Share what's on your mind...",
                placeholder="Share a tip, ask a question, or update the community on your latest project...",
                height=100
            )

            # For future implementation: image upload
            # post_image = st.file_uploader("Add an image (optional)", type=["jpg", "jpeg", "png"])

            submit_post = st.form_submit_button("Post")

            if submit_post and post_content:
                # Create the post in the database
                post_id = db.create_post(user_id, post_content)

                if post_id:
                    st.success("Post created successfully!")
                    # Short delay to show success message
                    time.sleep(1)
                    # Rerun to refresh the feed
                    st.rerun()
                else:
                    st.error("An error occurred while creating your post. Please try again.")

        # Display feed posts
        st.markdown('<p class="section-header">Recent Posts</p>', unsafe_allow_html=True)

        # Get all posts
        all_posts = db.get_posts(limit=20)

        if all_posts:
            # Display each post
            for post in all_posts:
                display_post(post, user_id)
        else:
            st.info("No posts yet. Be the first to share something with the community!")

    with col2:
        st.markdown('<p class="section-header">Community Updates</p>', unsafe_allow_html=True)

        # Display some static community announcements
        st.markdown("""
        <div class="post-card">
            <div class="post-header">
                <span class="post-author">FreelanceHub Team</span>
                <span class="post-date">Today</span>
            </div>
            <div class="post-content">
                <p>Welcome to our community feed! Share your experiences, ask questions, and connect with other freelancers. Stay tuned for upcoming features!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="post-card">
            <div class="post-header">
                <span class="post-author">Freelancer Tip of the Day</span>
                <span class="post-date">Today</span>
            </div>
            <div class="post-content">
                <p>Always ensure your contract includes a clear scope of work and revision policy to avoid scope creep. This protects both you and your client!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # # Display trending topics or popular posts
        # st.markdown('<p class="section-header">Trending Topics</p>', unsafe_allow_html=True)
        #
        # trending_topics = [
        #     "Remote Work Tips",
        #     "Pricing Strategies",
        #     "Client Communication",
        #     "Portfolio Building",
        #     "Work-Life Balance"
        # ]
        #
        # for topic in trending_topics:
        #     st.markdown(f"""
        #     <div style="padding: 0.5rem 1rem; background-color: #e3f2fd; border-radius: 0.5rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
        #         <span>#{topic.replace(' ', '')}</span>
        #         <span style="color: #757575; font-size: 0.875rem;">trending</span>
        #     </div>
        #     """, unsafe_allow_html=True)


def display_post(post, current_user_id):
    """Display a single post with like and comment functionality"""
    post_id = post['id']
    post_date = datetime.strptime(post['created_at'], "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")

    # Check if the current user has liked this post
    has_liked = db.has_user_liked_post(current_user_id, post_id)
    like_count = post['like_count']
    comments = post['comments']

    # Initialize session state for this post if needed
    if post_id not in st.session_state.show_comments:
        st.session_state.show_comments[post_id] = False

    if post_id not in st.session_state.new_comment:
        st.session_state.new_comment[post_id] = ""

    with st.container():
        # Post card
        st.markdown(f"""
        <div class="post-card">
            <div class="post-header">
                <span class="post-author">{post['username']}</span>
                <span class="post-date">{post_date}</span>
            </div>
            <div class="post-content">
                <p>{post['content']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Like and comment buttons
        col1, col2, col3 = st.columns([1, 1, 4])

        with col1:
            # Like button
            if has_liked:
                if st.button(f"❤️ {like_count}", key=f"unlike_{post_id}"):
                    # Unlike the post
                    if db.unlike_post(current_user_id, post_id):
                        st.rerun()
            else:
                if st.button(f"🤍 {like_count}", key=f"like_{post_id}"):
                    # Like the post
                    if db.like_post(current_user_id, post_id):
                        st.rerun()

        with col2:
            # Comment button
            if st.button(f"💬 {len(comments)}", key=f"comment_{post_id}"):
                # Toggle show comments
                st.session_state.show_comments[post_id] = not st.session_state.show_comments[post_id]
                st.rerun()

        # Display comments
        if st.session_state.show_comments[post_id]:
            with st.container():
                # Display existing comments
                if comments:
                    for comment in comments:
                        comment_date = datetime.strptime(comment['created_at'], "%Y-%m-%d %H:%M:%S").strftime(
                            "%b %d, %Y")

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

                # Add new comment
                with st.form(key=f"add_comment_form_{post_id}"):
                    st.text_area(
                        "Add a comment",
                        value=st.session_state.new_comment[post_id],
                        key=f"comment_text_{post_id}"
                    )

                    if st.form_submit_button("Submit"):
                        comment_text = st.session_state[f"comment_text_{post_id}"]

                        if comment_text:
                            # Add the comment to the database
                            comment_id = db.add_comment(current_user_id, post_id, comment_text)

                            if comment_id:
                                # Clear the comment text
                                st.session_state.new_comment[post_id] = ""
                                st.rerun()
                            else:
                                st.error("An error occurred while adding your comment. Please try again.")


if __name__ == "__main__":
    main()