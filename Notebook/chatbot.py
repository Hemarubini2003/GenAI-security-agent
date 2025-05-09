import streamlit as st
import nbformat
import os

# --- Function to read notebook content as plain text ---
def read_notebook(notebook_path):
    if not os.path.exists(notebook_path):
        return "Notebook file not found! Please check the path."
    nb = nbformat.read(notebook_path, as_version=4)
    content = []
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            content.append(cell.source)
        elif cell.cell_type == 'code':
            content.append(cell.source)
    return "\n\n".join(content)

# --- Simple retrieval function ---
def find_relevant_text(query, notebook_text):
    # For demonstration: return the first paragraph that contains any query word
    query_words = set(query.lower().split())
    for para in notebook_text.split('\n\n'):
        if any(qw in para.lower() for qw in query_words):
            return para
    return "Sorry, I couldn't find relevant information in the notebook."

# --- Streamlit UI ---
st.title("📓 Genie Security Agent Chatbot")

# Specify the path to your notebook file here:
NOTEBOOK_PATH = "Notebook/genie-security-agent.ipynb"

# Load notebook content once
if "notebook_text" not in st.session_state:
    st.session_state.notebook_text = read_notebook(NOTEBOOK_PATH)

# Display chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about the notebook..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # Retrieve relevant text from notebook
    answer = find_relevant_text(prompt, st.session_state.notebook_text)
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
