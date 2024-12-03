# LLM Code Generator Streamlit App

This Streamlit app allows users to interact with a Large Language Model (LLM) to generate Python code based on a given prompt, display the generated code, and execute the code within the app. It also features a file explorer in the sidebar to browse, view, and select files from the current directory.

![UI]("assets/ui.png")

## Features

1. **File Explorer in Sidebar**:
   - Browse through the current directory and subfolders.
   - Select and display the content of files in a container.

2. **Code Generation**:
   - Enter a prompt to generate Python code using an LLM (powered by Ollama).
   - The generated code is displayed in the app.

3. **Code Execution**:
   - Execute the generated Python code within the app.
   - Display the output of the executed code and any errors in the UI.

4. **Error Handling**:
   - If errors occur during code execution, they are displayed in the UI and saved in a log file.

## Installation

To run this app, you need to install the following Python packages:

1. **Streamlit** - For building the web app interface.
2. **Ollama** - To interact with the LLM model.
3. **Matplotlib** - For handling plots (if the generated code includes plotting).

You can install these dependencies using `pip`:

```bash
pip install streamlit ollama matplotlib numpy
```

## Usage

1. **Start the App**: 

   To run the app, execute the following command in the terminal:

   ```bash
   streamlit run app.py
   ```

2. **File Explorer**:
   - On the sidebar, you will see a file explorer.
   - You can browse and select files and folders from the current directory. The selected file’s content will be displayed in a container in the main app.

3. **Generate Code**:
   - Enter a prompt in the input box (e.g., "Write a python script to plot Lorenz attractors").
   - The app will generate Python code based on the prompt and display it in the app.

4. **Execute Code**:
   - After the code is generated, click on "Execute Code" to run the code.
   - The output and any errors will be shown below the generated code. If there are errors, they will also be saved in a `logs/error.txt` file.

5. **Error Handling**:
   - In case of an error during code execution, the app will attempt to debug the issue by modifying the code and re-running it.

## Code Structure

### 1. **`display_files_in_sidebar()`**:
   - Displays a file explorer in the sidebar, showing the files and folders in the current working directory.
   - Allows the user to select files and folders.

### 2. **`display_file_content()`**:
   - Opens and reads the selected file’s content.
   - Displays the content in a text area container in the app.

### 3. **`save_and_execute_code_with_subprocess()`**:
   - Saves the generated Python code to a file.
   - Executes the code using the `subprocess` module and captures the output (stdout) and error (stderr).

### 4. **`code_gen()`**:
   - Uses the Ollama LLM to generate Python code based on the user's prompt.
   - Displays the generated code in the app.

### 5. **`code_exec()`**:
   - Executes the generated Python code and captures the output.
   - Displays the output and any errors.

### 6. **`main()`**:
   - The main function that controls the flow of the app.
   - Handles file selection and code generation/execution.

## Example Workflow

1. **Enter Prompt**:
   - In the input field, type a prompt, such as "Write a Python script to plot Lorenz attractors."

2. **Generate Code**:
   - Click the "Generate Code" button, and the app will use the LLM to generate Python code based on the prompt.

3. **View and Execute Code**:
   - The generated Python code is displayed in the main window.
   - You can execute the code by clicking the "Execute Code" button.
   - The app will show the execution output and any errors.

4. **View Files**:
   - In the sidebar, you can navigate through your local files and select a file to display its contents in the main area.

## Example of Generated Code

Here's an example of the code the app might generate for the prompt "Write a Python script to plot Lorenz attractors":

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def lorenz_system(state, t, sigma=10.0, beta=8.0/3.0, rho=28.0):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Initial conditions
x0, y0, z0 = 1.0, 1.0, 1.0
state0 = [x0, y0, z0]

# Time grid
t = np.linspace(0, 2, 10000)

# Solve the Lorenz system
solution = odeint(lorenz_system, state0, t)

# Plot the results
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(solution[:, 0], solution[:, 1], solution[:, 2])
plt.show()
```

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit pull requests. Suggestions for improvements and bug fixes are always welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
https://docs.streamlit.io/develop/quick-reference/cheat-sheet
