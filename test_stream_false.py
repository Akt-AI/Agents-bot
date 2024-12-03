from ollama import chat
import ollama
from IPython import get_ipython

# Check if we're in an IPython environment
ipython = get_ipython()

# If we're not in an IPython environment, fall back to normal Python execution
if ipython is None:
    print("Not in an IPython environment. Executing code normally.")
else:
    print("In IPython environment. Preparing to execute code.")

# Execute the code in the IPython environment
stream = chat(
    model='llama3.2',
    messages=[{'role': 'tool', 'content': 'Write a python script to plot lorenz attractors'}],
    stream=False,  # If False, get the full response immediately
)

# Assuming the entire content (Python code) is in stream['message']['content']
code = stream['message']['content']

# Print the code for debugging (optional)
print("Generated code:\n", code)

# Only run the code in IPython if available
if ipython:
    ipython.run_cell(code)
else:
    # Execute the code normally in the regular Python environment
    exec(code)

