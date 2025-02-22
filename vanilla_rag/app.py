import requests
import streamlit as st

# Title
st.title("🔎 Vanilla RAG")

# Upload Document
uploaded_file = st.file_uploader("Upload a PDF or text document", type=["txt", "pdf"])

# Search Button
if uploaded_file and st.button("🔍 Search"):
    st.write("Extracting text and retrieving relevant documents...")

    # Stream the file to FastAPI
    with st.spinner("Sending file..."):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post("http://127.0.0.1:8000/upload", files=files)

    # Show Retrieval Results
    if response.status_code == 200:
        st.subheader("🔍 Retrieval Results")
        st.write(response.json().get("result", "No results found."))
    else:
        st.error("Failed to retrieve data.")

# Retrieval Settings (Displayed in Main UI)
st.subheader("⚙️ Retrieval Settings")
top_k = st.slider("Top K Results", 1, 10, 5)
similarity_metric = st.radio(
    "Similarity Metric", ["Cosine", "Dot Product", "Euclidean"]
)

# Display Selected Settings
st.write(f"📌 Selected Top K: {top_k}")
st.write(f"📌 Selected Similarity Metric: {similarity_metric}")
