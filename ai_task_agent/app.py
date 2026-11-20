
import streamlit as st
import pandas as pd
import html

from agent.main import run_agent
from database.db import get_tasks, get_task_summary, initialize_database


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="NOVA | AI Task Manager",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_database()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_page" not in st.session_state:
    st.session_state.active_page = "Overview"



# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Main application */
.stApp {
    background: linear-gradient(135deg, #f8f7ff 0%, #f0f5ff 55%, #fdf7ff 100%);
    color: #30334d;
}

/* Hide Streamlit branding */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e8e5f5;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #454761;
}

/* Headings */
h1, h2, h3 {
    color: #30334d !important;
    font-weight: 750 !important;
}

p, label {
    color: #656982;
}

/* Hero section */
.hero {
    background: linear-gradient(115deg, #e8e5ff, #e6efff 60%, #f4eaff);
    border: 1px solid #ded9fa;
    border-radius: 24px;
    padding: 35px;
    margin-bottom: 28px;
    box-shadow: 0 8px 25px rgba(105, 91, 170, 0.08);
}

.hero-tag {
    display: inline-block;
    background: #ffffff;
    border: 1px solid #ddd7fa;
    padding: 7px 13px;
    border-radius: 30px;
    font-size: 12px;
    letter-spacing: 1px;
    color: #7561c7;
    font-weight: 700;
}

.hero h1 {
    font-size: 36px !important;
    margin: 18px 0 8px 0;
    color: #37345e !important;
}

.hero p {
    color: #626584;
    font-size: 15px;
}

/* Metric cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #e9e6f5;
    border-radius: 19px;
    padding: 23px;
    min-height: 135px;
    box-shadow: 0 5px 18px rgba(65, 58, 110, 0.06);
}

.metric-icon {
    font-size: 25px;
}

.metric-label {
    color: #8586a0;
    font-size: 13px;
    margin-top: 12px;
    font-weight: 600;
}

.metric-value {
    color: #51469b;
    font-size: 32px;
    font-weight: 750;
    margin-top: 3px;
}

/* Task cards */
.task-card {
    background: #ffffff;
    border: 1px solid #e9e6f5;
    border-radius: 17px;
    padding: 19px;
    margin-bottom: 13px;
    box-shadow: 0 4px 14px rgba(65, 58, 110, 0.04);
}

.task-title {
    color: #343650;
    font-size: 16px;
    font-weight: 700;
}

.task-meta {
    color: #85869e;
    font-size: 12px;
    margin-top: 9px;
}

/* Priority and status badges */
.pill {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    margin-right: 5px;
}

.high {
    background: #ffe8ed;
    color: #d84d70;
}

.medium {
    background: #fff3dc;
    color: #b98220;
}

.low {
    background: #e2f8ef;
    color: #238b65;
}

.pending {
    background: #e7f0ff;
    color: #477bc5;
}

.completed {
    background: #e2f8ef;
    color: #238b65;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(100deg, #8170dc, #6b9ce8);
    color: white !important;
    border: none;
    border-radius: 11px;
    padding: 9px 17px;
    font-weight: 650;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(100deg, #705ecb, #5788d6);
    box-shadow: 0 5px 15px rgba(110, 95, 200, 0.2);
}

/* Input fields */
.stTextInput input,
.stChatInput textarea,
.stSelectbox div[data-baseweb="select"] {
    background: #ffffff !important;
    color: #343650 !important;
    border: 1px solid #ddd9ef !important;
    border-radius: 12px !important;
}

/* Chat messages */
div[data-testid="stChatMessage"] {
    background: #ffffff;
    border: 1px solid #e9e6f5;
    border-radius: 17px;
    padding: 13px;
    margin-bottom: 12px;
}

/* Chat input */
div[data-testid="stChatInput"] {
    border-color: #c9c0f0 !important;
}

/* Agent status card */
.agent-status {
    display: flex;
    align-items: center;
    gap: 11px;
    background: #e8f8ef;
    border: 1px solid #bce8cc;
    border-radius: 13px;
    padding: 13px 12px;
    margin-top: 8px;
    margin-bottom: 10px;
}

.status-dot {
    width: 11px;
    height: 11px;
    min-width: 11px;
    background: #22a568;
    border-radius: 50%;
    box-shadow: 0 0 0 4px #c9f0d9;
}

.status-title {
    color: #18794e !important;
    font-size: 14px;
    font-weight: 750;
}

.status-subtitle {
    color: #56866d !important;
    font-size: 11px;
    margin-top: 3px;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 40px 15px;
    background: #ffffff;
    border: 1px dashed #d8d2ed;
    border-radius: 18px;
    color: #777993;
}

/* Divider */
hr {
    border-color: #e8e5f2;
}

</style>
""", unsafe_allow_html=True)



# ---------------- HELPER FUNCTIONS ----------------

def metric_card(icon, label, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def render_task(task):
    title = html.escape(str(task["title"]))
    due = html.escape(str(task["due_date"] or "Not set"))
    priority = str(task["priority"]).lower()
    status = str(task["status"]).lower()

    priority_class = (
        priority if priority in ["high", "medium", "low"] else "medium"
    )
    status_class = (
        status if status in ["pending", "completed"] else "pending"
    )

    st.markdown(f"""
    <div class="task-card">
        <div class="task-title">
            #{task['id']} &nbsp; {title}
        </div>
        <div style="margin-top:12px;">
            <span class="pill {priority_class}">
                {html.escape(str(task['priority']))} Priority
            </span>
            <span class="pill {status_class}">
                {html.escape(str(task['status']))}
            </span>
        </div>
        <div class="task-meta">📅 Due date: {due}</div>
    </div>
    """, unsafe_allow_html=True)


def render_hero(title, description):
    st.markdown(f"""
    <div class="hero">
        <span class="hero-tag">✦ INTELLIGENT TASK MANAGEMENT</span>
        <h1>{title}</h1>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)



# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("""
    <div style="padding:12px 5px 24px 5px;">
        <div style="font-size:30px;font-weight:800;color:#8170dc;">
            ✦ NOVA
        </div>
        <div style="font-size:12px;color:#85869e;letter-spacing:2px;">
            AI TASK MANAGER
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Navigation")

    page = st.radio(
        "Navigation",
        ["Overview", "AI Assistant", "My Tasks"],
        index=["Overview", "AI Assistant", "My Tasks"].index(
            st.session_state.active_page
        ),
        label_visibility="collapsed"
    )

    st.session_state.active_page = page

    st.divider()

    # Agent Status
    st.markdown("### Agent Status")

    st.markdown("""
    <div class="agent-status">
        <div class="status-dot"></div>
        <div>
            <div class="status-title">AI Agent Ready</div>
            <div class="status-subtitle">
                NOVA is online and ready to assist
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Powered by Groq · GPT OSS 20B")

    st.divider()

    if st.button("↻ Refresh Dashboard", use_container_width=True):
        st.rerun()

    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
    <div style="position:relative;margin-top:45px;color:#828aa9;font-size:11px;">
        NOVA AI · Version 1.0<br>
        Built with Python & Streamlit
    </div>
    """, unsafe_allow_html=True)


# ---------------- DATA ----------------

summary = get_task_summary()
all_tasks = get_tasks()

# ---------------- DATA ----------------

summary = get_task_summary()
all_tasks = get_tasks()


# ---------------- OVERVIEW PAGE ----------------

if page == "Overview":

    render_hero(
        "Your productivity, elevated.",
        "Welcome to your intelligent workspace. Plan smarter, work faster and stay organized with AI."
    )

    st.subheader("Your Workspace")

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card("✦", "TOTAL TASKS", summary["total"])

    with c2:
        metric_card("◷", "PENDING TASKS", summary["pending"])

    with c3:
        metric_card("✓", "COMPLETED TASKS", summary["completed"])

    st.write("")

    left, right = st.columns([1.4, 1])

    with left:
        st.subheader("Recent Tasks")

        if all_tasks:
            for task in all_tasks[:5]:
                render_task(task)
        else:
            st.markdown("""
            <div class="empty-state">
                <div style="font-size:35px;">✦</div>
                <h3>No tasks yet</h3>
                Start by asking your AI assistant to create a task.
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.subheader("Quick Actions")

        st.markdown("""
        <div class="task-card">
            <div class="task-title">✦ Meet your AI Assistant</div>
            <div class="task-meta">
                Create tasks using simple natural-language instructions.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open AI Assistant →", use_container_width=True):
            st.session_state.active_page = "AI Assistant"
            st.rerun()

        st.markdown("""
        <div class="task-card">
            <div class="task-title">▤ Manage your tasks</div>
            <div class="task-meta">
                View your tasks, priorities and completion status.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View All Tasks →", use_container_width=True):
            st.session_state.active_page = "My Tasks"
            st.rerun()


# ---------------- AI ASSISTANT PAGE ----------------

elif page == "AI Assistant":

    render_hero(
        "Meet your AI Assistant.",
        "Tell NOVA what you need. Your AI agent can create, view, complete and delete tasks."
    )

    st.subheader("AI Conversation")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if not st.session_state.messages:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:38px;">✦</div>
            <h3>How can I help you today?</h3>
            Try creating a task, checking your progress or calculating something.
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        examples = [
            "Create a high priority task for tomorrow.",
            "Show all my pending tasks.",
            "Give me a summary of my tasks."
        ]

        for example in examples:
            st.caption("✧ " + example)

    user_input = st.chat_input("Message NOVA...")

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.spinner("NOVA is thinking..."):

            try:
                response = run_agent(user_input)
            except Exception as error:
                response = f"Error: {error}"

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()


# ---------------- TASKS PAGE ----------------

elif page == "My Tasks":

    render_hero(
        "Your task center.",
        "Every task in one place. Stay focused and track your progress."
    )

    st.subheader("Task Management")

    selected_status = st.selectbox(
        "Filter by status",
        ["All", "Pending", "Completed"]
    )

    if selected_status == "All":
        filtered_tasks = get_tasks()
    else:
        filtered_tasks = get_tasks(selected_status)

    st.caption(f"{len(filtered_tasks)} task(s) found")

    if filtered_tasks:

        for task in filtered_tasks:
            render_task(task)

    else:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:35px;">▤</div>
            <h3>No matching tasks</h3>
            Try another filter or create a new task with NOVA.
        </div>
        """, unsafe_allow_html=True)

    if st.button("Open AI Assistant →"):
        st.session_state.active_page = "AI Assistant"
        st.rerun()


# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<div style="text-align:center;color:#858dab;font-size:12px;padding:10px;">
    ✦ NOVA AI Task Manager &nbsp; | &nbsp;
    Built with Streamlit, Python, SQLite and Groq
</div>
""", unsafe_allow_html=True)
