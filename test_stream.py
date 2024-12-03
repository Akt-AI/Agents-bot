from ollama import chat
import ollama
from IPython import get_ipython

ipython = get_ipython()

# Execute the code in the IPython environment
stream = chat(
    model='llama3.2',
    messages=[{'role': 'tool', 'content': 'Write a python script to plot lorenz attractors'}],
    stream=True,  # True to get the response in chunks
)

# Initialize an empty string to store the code
code = ""

# Loop through the stream chunks and accumulate the code
for chunk in stream:
    code += chunk['message']['content']  # Append the chunk to 'code'

# Print the accumulated code for debugging
print("Generated code:\n", code)

# Check if we're in an IPython environment
if ipython is not None:
    # Run the code in the IPython environment
    ipython.run_cell(code)
else:
    # If not in an IPython environment, execute normally using exec
    exec(code)
