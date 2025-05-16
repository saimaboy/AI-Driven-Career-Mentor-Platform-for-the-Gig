import streamlit as st
import database as db
import auth
from chatbot.bot import FreelanceSupportBot

# Initialize session state
auth.init_session_state()

# Require login
if not auth.require_login():
    st.stop()

# Page config
st.set_page_config(
    page_title="Support | FreelanceHub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size:2.5rem; color:#1E88E5; margin-bottom:0; }
    .sub-header  { font-size:1.2rem; color:#757575; margin-top:0; }
    .chat-message { padding:1rem; border-radius:.5rem; margin-bottom:1rem;
                     display:flex; gap:.75rem; }
    .chat-message.user { background:#E3F2FD; border-left:5px solid #1E88E5; }
    .chat-message.bot  { background:#F5F5F5; border-left:5px solid #4CAF50; }
    .avatar { width:2.5rem; height:2.5rem; border-radius:50%; background:#ccc;
               display:flex; align-items:center; justify-content:center; font-size:1.25rem; }
    .message-content { flex:1; }
    .section-header { font-size:1.5rem; color:#1E88E5; margin-bottom:1rem; }
    .card { padding:1.5rem; border-radius:.5rem; background:#f8f9fa;
            box-shadow:0 .125rem .25rem rgba(0,0,0,.075); margin-bottom:1rem; }
    .topic-card { cursor:pointer; transition:all .2s ease; }
    .topic-card:hover { transform:translateY(-3px);
                        box-shadow:0 .25rem .5rem rgba(0,0,0,.15); }
</style>
""", unsafe_allow_html=True)

# Sidebar
def render_sidebar():
    with st.sidebar:
        st.image("https://freesvg.org/img/1538298822.png", width=100)
        st.title("FreelanceHub")
        st.success(f"Logged in as: {auth.get_current_username()}")
        if st.button("Logout"):
            auth.logout_user()
            st.rerun()

render_sidebar()

# Initialize chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "bot", "content": "Hello! I'm your freelance assistant. How can I help you today?"}
    ]

# Initialize our new support bot
if "support_bot" not in st.session_state:
    user_id = auth.get_current_user_id()
    st.session_state.support_bot = FreelanceSupportBot(user_id)

def display_message(role, content):
    """Render a single chat message."""
    if role == "user":
        cls = "user"; avatar = "👤"
    else:
        cls = "bot";  avatar = "🤖"
    st.markdown(f"""
    <div class="chat-message {cls}">
      <div class="avatar">{avatar}</div>
      <div class="message-content">{content.replace('\\n','<br>')}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.markdown('<p class="main-header">Freelancer Support</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Get answers and advice for your freelancing journey</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

    with col1:
        # Clear history
        if st.button("🗑️ Clear Chat History", key="clear_history"):
            st.session_state.chat_messages = [
                {"role": "bot", "content": "Hello! I'm your freelance assistant. How can I help you today?"}
            ]
            st.rerun()

        st.markdown('<p class="section-header">Chat with Support Assistant</p>', unsafe_allow_html=True)
        for msg in st.session_state.chat_messages:
            display_message(msg["role"], msg["content"])

        # Input form
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Type your message...", key="user_message")
            submitted = st.form_submit_button("Send")
            if submitted and user_input:
                # user message
                st.session_state.chat_messages.append({"role":"user","content":user_input})
                # bot response
                reply = st.session_state.support_bot.get_response(user_input)
                st.session_state.chat_messages.append({"role":"bot","content":reply})
                st.rerun()

    with col2:
        # Common Topics
        st.markdown('<p class="section-header">Common Topics</p>', unsafe_allow_html=True)
        topic_questions = [
            ("Finding Clients",       "How do I find my first client?"),
            ("Setting Rates",         "How should I price my services?"),
            ("Skill Development",     "What skills should I improve?"),
            ("Creating Gigs",         "Tips for effective gig listings"),
            ("Profile Analysis",      "Analyze my current skill profile"),
            ("Success Strategies",    "What are the best freelancing strategies?")
        ]
        for title, question in topic_questions:
            st.markdown(f"""
                <div class="card topic-card">
                  <h4>{title}</h4>
                  <p style="color:#757575;font-style:italic;">"{question}"</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Ask about {title}", key=f"topic_{title}", help=question):
                st.session_state.chat_messages.append({"role":"user","content":question})
                reply = st.session_state.support_bot.get_response(question)
                st.session_state.chat_messages.append({"role":"bot","content":reply})
                st.rerun()

        # Personalized Skill Analysis
        user_id = auth.get_current_user_id()
        user_skills = db.get_user_skills(user_id)
        if user_skills:
            with st.expander("Get Personalized Skill Analysis", expanded=True):
                st.write("Click below to analyze your skill profile:")
                if st.button("Analyze My Skills", key="analyze_skills"):
                    q = "analyze my skill profile"
                    st.session_state.chat_messages.append({"role":"user","content":q})
                    reply = st.session_state.support_bot.get_response(q)
                    st.session_state.chat_messages.append({"role":"bot","content":reply})
                    st.rerun()

        # More Questions
        st.markdown('<p class="section-header">More Questions</p>', unsafe_allow_html=True)
        guaranteed = [
            ("Payment Methods", "What are the best payment methods for freelancers?"),
            ("Contract Advice","What should I include in my freelance contract?"),
            ("Time Management","How can I manage my time better as a freelancer?"),
            ("Client Communication","Tips for communicating with clients"),
            ("Handling Feedback","How should I handle client feedback?"),
            ("Creating Gigs","Can you give me tips for creating effective gigs?")
        ]
        for title, question in guaranteed:
            colA, colB = st.columns([3,1])
            with colA:
                st.markdown(f"**{title}**")
            with colB:
                if st.button("Ask", key=f"ask_{title}", help=question):
                    st.session_state.chat_messages.append({"role":"user","content":question})
                    reply = st.session_state.support_bot.get_response(question)
                    st.session_state.chat_messages.append({"role":"bot","content":reply})
                    st.rerun()

if __name__ == "__main__":
    main()
