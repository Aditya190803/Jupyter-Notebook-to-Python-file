import streamlit as st
from nbconvert import PythonExporter
import nbformat
from io import StringIO
import os

def convert_ipynb_to_py(notebook_content):
    # Load the notebook
    notebook = nbformat.reads(notebook_content, as_version=4)
    
    # Create a PythonExporter instance
    python_exporter = PythonExporter()
    
    # Convert the notebook to Python script
    body, _ = python_exporter.from_notebook_node(notebook)
    return body

def filter_code_cells(notebook_content):
    # Load the notebook
    notebook = nbformat.reads(notebook_content, as_version=4)
    
    # Initialize an empty list for code cells
    code_cells = []
    
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            code_cells.append(cell.source)
    
    # Join code cells into a single string
    return "\n\n".join(code_cells)

# Streamlit UI
st.title('Jupyter Notebook to Python Script Converter')

st.write("Upload a Jupyter Notebook (.ipynb) file to convert it to a Python (.py) file:")

# File uploader
uploaded_file = st.file_uploader("Choose a notebook file", type="ipynb")

if uploaded_file is not None:
    # Extract the filename without the extension
    file_name, _ = os.path.splitext(uploaded_file.name)
    
    # Read the file content
    notebook_content = uploaded_file.read().decode("utf-8")
    
    # Filter code cells
    python_script = filter_code_cells(notebook_content)
    
    # Display the converted script
    st.text_area("Python Script:", python_script, height=500)
    
    # Provide download link for the Python script with the same base name
    st.download_button(
        label="Download Python Script",
        data=python_script,
        file_name=f"{file_name}.py",
        mime="text/x-python-script"
    )
