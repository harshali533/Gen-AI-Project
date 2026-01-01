# app_ui.py
import streamlit as st
from agent_router import agent_router
from chatbot import get_answer
from voice_input import listen

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Sunbeam Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ------------------ Session State Init ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "threads" not in st.session_state:
    st.session_state.threads = {
        "About Sunbeam": [],
        "Internship": [],
        "Courses": [],
        "Contact": []
    }
if "active_thread" not in st.session_state:
    st.session_state.active_thread = "About Sunbeam"

# ------------------ LOGIN PAGE ------------------
if not st.session_state.logged_in:
    st.title("🔐 Login to Sunbeam AI Chatbot")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username.strip() != "" and password.strip() != "":
            # ✅ Accept any username/password
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.success(f"✅ Welcome {st.session_state.username} 🌷")
            # No need for st.experimental_rerun()
        else:
            st.error("❌ Please enter username and password")

# ------------------ CHATBOT UI ------------------
else:
    st.title("✨🤖 Sunbeam AI Chatbot")
    st.caption(f"Logged in as **{st.session_state.username}** 🌷")

    # ------------------ Logout Button ------------------
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun = lambda: None  # just disable old calls
        st.experimental_rerun()  # Safe dummy for backward compatibility

    # ------------------ Sidebar Threads ------------------
    st.sidebar.title("📂 Chat History")
    st.session_state.active_thread = st.sidebar.radio(
        "Select Topic",
        list(st.session_state.threads.keys())
    )

    # Clear chat button
    if st.sidebar.button("🗑 Clear Current Thread"):
        st.session_state.threads[st.session_state.active_thread] = []

    # ------------------ Display Chat History ------------------
    for msg in st.session_state.threads[st.session_state.active_thread]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ------------------ Chat Input ------------------
    col_text, col_voice = st.columns([10, 1])
    with col_text:
        user_input = st.chat_input(f"Ask something about {st.session_state.active_thread}...")
    with col_voice:
        voice_clicked = st.button("🎤")

    # ------------------ Handle Text Input ------------------
    if user_input:
        # Save user message
        st.session_state.threads[st.session_state.active_thread].append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = get_answer(user_input)
            st.markdown(answer)
        # Save bot response
        st.session_state.threads[st.session_state.active_thread].append(
            {"role": "assistant", "content": answer}
        )

    # ------------------ Handle Voice Input ------------------
    if voice_clicked:
        with st.spinner("Listening..."):
            voice_query = listen()
        if voice_query:
            # Save user message
            st.session_state.threads[st.session_state.active_thread].append(
                {"role": "user", "content": voice_query}
            )
            with st.chat_message("user"):
                st.markdown(voice_query)

            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = agent_router(voice_query)
                st.markdown(answer)

            # Save bot response
            st.session_state.threads[st.session_state.active_thread].append(
                {"role": "assistant", "content": answer}
            )
        else:
            st.warning("Could not hear properly")
