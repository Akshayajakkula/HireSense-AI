import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="HireSense AI", page_icon="🧠")
st.title("HireSense AI")
st.write("Upload a resume (PDF) to get started.")

uploaded = st.file_uploader("Upload resume", type=["pdf"])

if uploaded is not None:
    reader = PdfReader(uploaded)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    st.success(f"Read {len(reader.pages)} page(s)")
    st.text_area("Extracted text", text, height=300)