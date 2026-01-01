import streamlit as st

# Dummy users
USERS = {
    "admin": "admin123",
    "sunbeam": "sunbeam123",
    "student": "student123"
}

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

# Login page
if not st.session_state.authenticated:
    st.title("🔐 Login to Sunbeam Chatbot")

    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Login"):
        username_clean = username_input.strip().lower()  # lowercase & strip spaces
        password_clean = password_input.strip()          # strip spaces

        # Check username and password
        if username_clean in USERS and USERS[username_clean] == password_clean:
            st.session_state.authenticated = True
            st.session_state.username = username_clean
            st.success(f"✅ Login successful! Welcome {username_clean} 🌷")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")

# Chatbot placeholder
else:
    st.success(f"Logged in as {st.session_state.username} 🌷")
    st.write("Chatbot UI goes here...")
