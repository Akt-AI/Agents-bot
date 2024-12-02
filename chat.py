import streamlit as st
import requests
import json
import os
import random

model_api_list = []
OLLAMA_API_URL = "http://localhost:11434"

# Ensure chat history directory exists
HISTORY_DIR = "chat_history"
os.makedirs(HISTORY_DIR, exist_ok=True)

# Emoji list for random selection
EMOJI_LIST = ["😀", "🎉", "🤖", "🌟", "🧠", "📚", "💬", "🚀", "📝", "🎨", "✨"]

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_chat_file" not in st.session_state:
    st.session_state.current_chat_file = None
if "session_emoji" not in st.session_state:
    st.session_state.session_emoji = random.choice(EMOJI_LIST)
if "stop_generation" not in st.session_state:
    st.session_state.stop_generation = False


def generate_response(prompt):
    """
    Generate a response using the Ollama API.

    Parameters:
        prompt (str): The user input prompt.

    Yields:
        str: The generated response in chunks.
    """
    system = """You are a Physics book Writer, 
                given a topic you will 
                write a planned book."""

    response = requests.post(
        f"{OLLAMA_API_URL}/api/generate",
        json={"model": GENERATION_MODEL, 
              "prompt": prompt, 
              "system": system,
              "num_ctx": 100000},
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
    """Automatically save the current chat history."""
    if not st.session_state.chat_history:
        return

    # Generate filename from the first user prompt
    if not st.session_state.current_chat_file:
        first_prompt = st.session_state.chat_history[0]["message"] if st.session_state.chat_history else "chat"
        sanitized_filename = "".join(c for c in first_prompt if c.isalnum() or c in (" ", "_", "-")).rstrip()
        st.session_state.current_chat_file = f"{st.session_state.session_emoji}_{sanitized_filename[:30].replace(' ', '_')}.md"

    file_path = os.path.join(HISTORY_DIR, st.session_state.current_chat_file)
    with open(file_path, "w") as file:
        file.write(f"# Chat Session {st.session_state.session_emoji}\n\n")
        for msg in st.session_state.chat_history:
            file.write(f"**{msg['role'].capitalize()}:** {msg['message']}\n\n")


def load_chat_history(file_name):
    """Load a saved chat history from the chat_history folder."""
    file_path = os.path.join(HISTORY_DIR, file_name)
    with open(file_path, "r") as file:
        chat_lines = file.readlines()

    st.session_state.chat_history = []
    current_role = None
    current_message = ""

    for line in chat_lines:
        if line.startswith("**User:**"):
            if current_role and current_message:
                st.session_state.chat_history.append({"role": current_role, "message": current_message.strip()})
            current_role = "user"
            current_message = line.replace("**User:**", "").strip()
        elif line.startswith("**Assistant:**"):
            if current_role and current_message:
                st.session_state.chat_history.append({"role": current_role, "message": current_message.strip()})
            current_role = "assistant"
            current_message = line.replace("**Assistant:**", "").strip()
        else:
            current_message += line

    if current_role and current_message:
        st.session_state.chat_history.append({"role": current_role, "message": current_message.strip()})

    st.session_state.current_chat_file = file_name


def clear_chat():
    """Clear the chat history and reset session state."""
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


def loop_chat(prompt):
    if prompt:
        # Display the user's input
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user's message to chat history
        st.session_state.chat_history.append({"role": "user", "message": prompt})

        # Generate the AI's response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            for chunk in generate_response(prompt):
                if st.session_state.stop_generation:
                    st.warning("Generation stopped by the user.")
                    break
                full_response += chunk
                response_placeholder.markdown(full_response)

            # Add AI's response to chat history
            st.session_state.chat_history.append({"role": "assistant", "message": full_response})

        # Auto-save chat history
        save_chat_history()


def main_chat():
    st.title("💬 AI Chat Assistant")

    # Sidebar: Directory tree and new chat button
    st.sidebar.header("Chat History")
    if st.sidebar.button("➕ New Chat"):
        clear_chat()

    if st.sidebar.button("🗑️ Delete All History"):
        delete_all_history()

    # List saved chat histories as buttons with delete buttons
    saved_histories = os.listdir(HISTORY_DIR)
    if saved_histories:
        st.sidebar.markdown("### Saved Chats")
        for file_name in saved_histories:
            col1, col2 = st.sidebar.columns([0.8, 0.2])
            if col1.button(f"📄 {file_name}", key=f"load_{file_name}"):
                load_chat_history(file_name)
            if col2.button("❌", key=f"del_{file_name}"):
                delete_file(file_name)

    # Display chat messages from history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["message"])

    # Display current session emoji
    st.markdown(f"### Current Chat Emoji: {st.session_state.session_emoji}")

    # Chat input for new messages
    prompt = st.chat_input("Type your message:")

    # Place the stop button at the bottom
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        stop_button = st.button("⏹️")
        if stop_button:
            st.session_state.stop_generation = True

    while prompt:
        loop_chat(prompt)
        prompt = None  # Prevent looping on the same prompt


if __name__ == "__main__":
    st.set_page_config(page_title="AI Chat Assistant", layout="wide")
    main_chat()
