import streamlit as st
import requests
import json
import os
import random

# API and Configuration
OLLAMA_API_URL = "http://localhost:11434"
GENERATION_MODEL = "qwen2.5:0.5b"

# Ensure chat history directory exists
HISTORY_DIR = "chat_history"
os.makedirs(HISTORY_DIR, exist_ok=True)

# Emoji list for random selection
EMOJI_LIST = ["😀", "🎉", "🤖", "🌟", "🧠", "📚", "💬", "🚀", "📝", "🎨", "✨"]

# In-memory user credentials for demo
USER_CREDENTIALS = {"test_user": "password123"}

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_chat_file" not in st.session_state:
    st.session_state.current_chat_file = None
if "session_emoji" not in st.session_state:
    st.session_state.session_emoji = random.choice(EMOJI_LIST)
if "stop_generation" not in st.session_state:
    st.session_state.stop_generation = False
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None


# Authentication functions
def login():
    """Login Screen."""
    st.title("🔒 Login")
    st.subheader("Access your personalized AI Assistant")
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    col1, col2, col3 = st.columns([0.4, 0.2, 0.4])
    with col2:
        login_button = st.button("Login", use_container_width=True)
    if login_button:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.is_logged_in = True
            st.session_state.current_user = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")


def register():
    """Registration Screen."""
    st.title("📝 Register")
    st.subheader("Create a new account for personalized access")
    username = st.text_input("Choose a Username", placeholder="Enter a username")
    password = st.text_input("Choose a Password", type="password", placeholder="Enter a password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
    col1, col2, col3 = st.columns([0.4, 0.2, 0.4])
    with col2:
        register_button = st.button("Register", use_container_width=True)
    if register_button:
        if username in USER_CREDENTIALS:
            st.error("Username already exists!")
        elif password != confirm_password:
            st.error("Passwords do not match!")
        elif not username or not password:
            st.error("Username and password cannot be empty!")
        else:
            USER_CREDENTIALS[username] = password
            st.success("Registration successful! Please log in.")


# Chat functions
def generate_response(prompt):
    """Generate a response using the Ollama API."""
    system = """You are a Physics book Writer, 
                given a topic you will 
                write a planned book."""

    response = requests.post(
        f"{OLLAMA_API_URL}/api/generate",
        json={"model": GENERATION_MODEL, "prompt": prompt, "system": system, "num_ctx": 100000},
        stream=True,
    )
    if response.status_code == 200:
        for chunk in response.iter_lines():
            if st.session_state.stop_generation:
                st.session_state.stop_generation = False
                break
            if chunk:
                try:
                    chunk_data = json.loads(chunk.decode("utf-8"))
                    if "response" in chunk_data:
                        yield chunk_data["response"]
                except json.JSONDecodeError:
                    st.error("Error parsing response chunk.")
    else:
        st.error(f"Error generating response: {response.text}")
        yield ""


def save_chat_history():
    """Save the current chat history."""
    if not st.session_state.chat_history:
        return
    if not st.session_state.current_chat_file:
        first_prompt = st.session_state.chat_history[0]["message"] if st.session_state.chat_history else "chat"
        sanitized_filename = "".join(c for c in first_prompt if c.isalnum() or c in (" ", "_", "-")).rstrip()
        st.session_state.current_chat_file = f"{st.session_state.session_emoji}_{sanitized_filename[:30].replace(' ', '_')}.md"

    file_path = os.path.join(HISTORY_DIR, st.session_state.current_chat_file)
    with open(file_path, "w") as file:
        file.write(f"# Chat Session {st.session_state.session_emoji}\n\n")
        for msg in st.session_state.chat_history:
            file.write(f"**{msg['role'].capitalize()}:** {msg['message']}\n\n")


def loop_chat(prompt):
    """Chat loop for processing prompts."""
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.chat_history.append({"role": "user", "message": prompt})

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            for chunk in generate_response(prompt):
                if st.session_state.stop_generation:
                    st.warning("Generation stopped by the user.")
                    break
                full_response += chunk
                response_placeholder.markdown(full_response)

            st.session_state.chat_history.append({"role": "assistant", "message": full_response})

        save_chat_history()


def main_chat():
    """Main Chat Interface."""
    st.title("💬 AI Chat Assistant")

    # Sidebar
    st.sidebar.header("📁 Chat History")
    st.sidebar.markdown(f"### Logged in as: {st.session_state.current_user}")
    if st.sidebar.button("➕ New Chat"):
        clear_chat()
    if st.sidebar.button("🗑️ Delete All History"):
        delete_all_history()

    # Display saved chat histories
    saved_histories = os.listdir(HISTORY_DIR)
    if saved_histories:
        for file_name in saved_histories:
            col1, col2 = st.sidebar.columns([0.8, 0.2])
            if col1.button(f"📄 {file_name}"):
                load_chat_history(file_name)
            if col2.button("❌", key=f"delete_{file_name}"):
                delete_file(file_name)

    # Chat Display
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["message"])

    # Chat Input
    prompt = st.chat_input("Type your message:")

    # Action Buttons Below Input
    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])
    with col2:
        stop_button = st.button("⏹️ Stop", use_container_width=True)
        regenerate_button = st.button("🔄 Regenerate", use_container_width=True)

    if stop_button:
        st.session_state.stop_generation = True

    if regenerate_button and st.session_state.chat_history:
        last_user_message = next(
            (msg["message"] for msg in reversed(st.session_state.chat_history) if msg["role"] == "user"), None
        )
        if last_user_message:
            loop_chat(last_user_message)

    if prompt:
        loop_chat(prompt)


def clear_chat():
    """Clear chat history."""
    st.session_state.chat_history = []
    st.session_state.current_chat_file = None
    st.session_state.session_emoji = random.choice(EMOJI_LIST)


def delete_file(file_name):
    """Delete a specific chat history file."""
    file_path = os.path.join(HISTORY_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)


def delete_all_history():
    """Delete all saved chat history files."""
    for file_name in os.listdir(HISTORY_DIR):
        delete_file(file_name)


if __name__ == "__main__":
    st.set_page_config(page_title="AI Chat Assistant", layout="wide")

    # Login/Registration Logic
    if not st.session_state.is_logged_in:
        st.sidebar.title("🔑 Authentication")
        page = st.sidebar.radio("Navigation", ["Login", "Register"])
        if page == "Login":
            login()
        elif page == "Register":
            register()
    else:
        main_chat()
