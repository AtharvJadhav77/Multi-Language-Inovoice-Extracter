
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# ---------------- CONFIGURE GEMINI ----------------
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Gemini model (image + text supported)
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(
    page_title="Multi-Language Invoice Extractor",
    layout="centered"
)

st.title("📄 Multi-Language Invoice Extractor")
st.write("Upload an invoice image and ask questions about it.")

# ---------------- USER INPUT ----------------
user_query = st.text_input(
    "Ask a question about the invoice:",
    placeholder="e.g. What is the invoice number, date, and total amount?"
)

uploaded_file = st.file_uploader(
    "Upload Invoice Image",
    type=["png", "jpg", "jpeg"]
)

image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice", use_column_width=True)

submit = st.button("Analyze Invoice")

# ---------------- SYSTEM PROMPT ----------------
system_prompt = """
You are an expert invoice analyzer.
Extract accurate information from invoice images.
Translate the invoice to English if it is not in English.
Answer strictly based on the invoice content.
"""

# ---------------- GEMINI RESPONSE FUNCTION ----------------
def get_gemini_response(user_query, image, system_prompt):
    response = model.generate_content(
        [
            system_prompt,
            user_query,
            image
        ]
    )
    return response.text

# ---------------- EXECUTION ----------------
if submit:
    if not uploaded_file:
        st.error("❌ Please upload an invoice image.")
    elif not user_query:
        st.error("❌ Please enter a question.")
    else:
        with st.spinner("Analyzing invoice..."):
            try:
                result = get_gemini_response(
                    user_query,
                    image,
                    system_prompt
                )
                st.subheader("✅ Response")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
