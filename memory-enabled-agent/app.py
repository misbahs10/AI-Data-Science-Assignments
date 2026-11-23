
import streamlit as st

from agent.llm import GroqLLM
from memory.manager import MemoryManager
from memory.database import (
    initialize_database,
    create_conversation,
    get_conversations,
    get_messages,
    delete_conversation,
)


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Memory AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- DATABASE INITIALIZATION ----------------

initialize_database()


# ---------------- LOAD SERVICES ----------------

@st.cache_resource
def load_services():
    """Load AI and memory services once."""

    manager = MemoryManager()
    llm = GroqLLM()

    return manager, llm


try:
    manager, llm = load_services()

except Exception as error:
    st.error(f"Application initialization failed: {error}")
    st.stop()


# ---------------- SESSION STATE ----------------

if "active_conversation_id" not in st.session_state:
    st.session_state.active_conversation_id = None


# Load conversations from database.
conversations = get_conversations()

# Create first conversation if database is empty.
if not conversations:

    new_id = create_conversation()

    st.session_state.active_conversation_id = new_id

    conversations = get_conversations()


# Validate active conversation.
valid_ids = [
    conversation["id"]
    for conversation in conversations
]

if st.session_state.active_conversation_id not in valid_ids:

    st.session_state.active_conversation_id = valid_ids[0]


# Initialize or synchronize conversation selector.
if (
    "conversation_selector" not in st.session_state
    or st.session_state.conversation_selector not in valid_ids
):

    st.session_state.conversation_selector = (
        st.session_state.active_conversation_id
    )


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🧠 Memory AI")

    st.caption("Your personal AI assistant")

    st.divider()

    # NEW CONVERSATION
    if st.button(
        "＋ New Conversation",
        use_container_width=True
    ):

        new_id = create_conversation()

        # Update active conversation.
        st.session_state.active_conversation_id = new_id

        # Update selectbox state BEFORE rerun.
        st.session_state.conversation_selector = new_id

        st.rerun()


    # CONVERSATION HISTORY
    st.subheader("Your Conversations")

    conversations = get_conversations()

    conversation_ids = [
        conversation["id"]
        for conversation in conversations
    ]

    if conversations:

        selected_id = st.selectbox(
            "Select conversation",
            options=conversation_ids,
            format_func=lambda conversation_id: next(
                (
                    conversation["title"]
                    for conversation in conversations
                    if conversation["id"] == conversation_id
                ),
                "Conversation"
            ),
            key="conversation_selector",
            label_visibility="collapsed"
        )

        st.session_state.active_conversation_id = selected_id


    st.divider()


    # ---------------- LONG-TERM MEMORY ----------------

    st.subheader("💾 Long-Term Memories")

    memories = manager.get_all_memories()

    st.metric(
        "Saved Memories",
        len(memories)
    )

    with st.expander("View saved memories"):

        if memories:

            for memory in memories:

                st.markdown(
                    f"**{memory['category'].title()}**"
                )

                st.write(memory["memory"])

                st.divider()

        else:

            st.info("No memories saved yet.")


    # ---------------- ADD MEMORY ----------------

    with st.expander("＋ Add a Memory"):

        with st.form("add_memory_form"):

            memory_text = st.text_area(
                "What should AI remember?"
            )

            category = st.selectbox(
                "Category",
                [
                    "general",
                    "education",
                    "skills",
                    "preferences",
                    "interests",
                    "career"
                ]
            )

            submitted = st.form_submit_button(
                "Save Memory",
                use_container_width=True
            )

            if submitted:

                if memory_text.strip():

                    manager.save_memory(
                        memory_text,
                        category
                    )

                    st.success(
                        "Memory saved successfully!"
                    )

                    st.rerun()

                else:

                    st.warning(
                        "Please enter a memory."
                    )


    st.divider()

    st.caption(
        "Powered by Groq + SQLite + FastEmbed"
    )


# ---------------- MAIN CHAT INTERFACE ----------------

st.title("🧠 Memory AI Assistant")

st.caption(
    "An AI assistant that remembers your conversations "
    "and retrieves relevant long-term memories."
)

st.divider()


# Get currently selected conversation.
conversation_id = st.session_state.active_conversation_id


# ---------------- DISPLAY CHAT HISTORY ----------------

messages = get_messages(conversation_id)

for message in messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------- USER INPUT ----------------

user_prompt = st.chat_input(
    "Ask me anything..."
)


if user_prompt:

    try:

        # Display user message.
        with st.chat_message("user"):

            st.markdown(user_prompt)


        # Retrieve context BEFORE saving current message.
        context = manager.get_agent_context(
            conversation_id,
            user_prompt
        )


        # Save user message.
        manager.add_message(
            conversation_id,
            "user",
            user_prompt
        )


        # Generate AI response.
        with st.chat_message("assistant"):

            with st.spinner(
                "Thinking and retrieving memories..."
            ):

                response = llm.generate_response(
                    user_message=user_prompt,
                    conversation_history=context[
                        "conversation_history"
                    ],
                    relevant_memories=context[
                        "relevant_memories"
                    ]
                )

            st.markdown(response)


        # Save assistant response.
        manager.add_message(
            conversation_id,
            "assistant",
            response
        )


    except Exception as error:

        st.error(
            f"Something went wrong: {error}"
        )
