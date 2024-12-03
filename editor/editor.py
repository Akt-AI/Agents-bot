import streamlit as st
from ollama import chat
import ollama
import subprocess
import io
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

st.title("LLM Code Generator")

# Function to display file and folder structure in the sidebar
def display_files_in_sidebar():
    # Get the current directory
    current_dir = os.getcwd()

    # Display the current directory and subfolders
    st.sidebar.title("File Explorer")

    # List directories in the current folder
    folders = [f for f in os.listdir(current_dir) if os.path.isdir(f)]
    files = [f for f in os.listdir(current_dir) if os.path.isfile(f)]

    # Display folder names in the sidebar
    folder_selection = st.sidebar.selectbox("Select a folder:", ["None"] + folders)
    
    # Display file names in the sidebar based on the folder selection
    if folder_selection != "None":
        folder_path = os.path.join(current_dir, folder_selection)
        files = os.listdir(folder_path)
        file_selection = st.sidebar.selectbox("Select a file:", files)
    else:
        file_selection = st.sidebar.selectbox("Select a file:", files)

    return folder_selection, file_selection

# Function to display file content in a container
def display_file_content(file_path):
    with open(file_path, "r") as file:
        file_content = file.read()
        st.text_area("File Content", file_content, height=300)


# Function to save the code to a file and execute it using subprocess
def save_and_execute_code_with_subprocess(code_filename):
    # Run the code using subprocess and capture output
    result = subprocess.run(
        ['python', code_filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Return the standard output and error output
    return result.stdout, result.stderr

def code_gen(user_input):
    # if st.button("Generate Code"):
    with st.spinner("Generating code..."):
        # Get the code from Ollama
        stream = chat(
            model='llama3.2',
            messages=[{'role': 'tool', 'content': user_input}],
            stream=True,  # True to get the response in chunks
        )

        # Initialize an empty string to store the code
        code = ""

        # Loop through the stream chunks and accumulate the code
        for chunk in stream:
            code += chunk['message']['content']  # Append the chunk to 'code'

        # Display the generated code
        st.subheader("Generated Python Code:")
        st.code(code, language='python')

        # Save the generated code to a file (optional for debugging)
        with open("template.py", "w") as f:
            f.write(code)
        
        return code

def code_exec(user_input):
    code = code_gen(user_input)
    # Button to execute the code
    if st.button("Execute Code"):
        with st.spinner("Executing code..."):
            # Execute the code using subprocess and capture the output
            output, error = save_and_execute_code_with_subprocess("template.py")
            # print(output)
            
            # Show the text-based output (stdout)
            st.subheader("Execution Output:")
            st.write(output)

            # Show any errors (stderr)
            if error:
                st.subheader("Error Output:")
                os.mkdir("logs")
                with open("logs/error.txt", "w") as f:
                    f.write(error)
                st.text(error)
                while True:
                    code_exec(user_input+ "Debug:"+ error)
                    output, error = save_and_execute_code_with_subprocess("template.py")
                    st.subheader("Execution Output:")
                    st.write(output)
            
                
def main():
    # Sidebar file explorer
    folder, selected_file = display_files_in_sidebar()

    # Show the selected file path in the main window
    if selected_file:
        file_path = os.path.join(folder if folder != "None" else "", selected_file)
        st.write(f"Selected file: {file_path}")
        display_file_content(file_path)
        
    user_input = st.chat_input("Enter a prompt for the LLM:")
    code = code_gen(user_input)
    code_exec(user_input)



if __name__=="__main__":
    main()




