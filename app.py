import streamlit as st
import google.generativeai as genai
from PIL import Image
import pytesseract
import cv2
import numpy as np

# ---------------- CONFIG ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

st.set_page_config(
    page_title="Multi-Language Invoice Extractor",
    layout="centered"
)

st.title("📄 Multi-Language Invoice Extractor")

# ---------------- USER INPUT ----------------
uploaded_file = st.file_uploader(
    "Upload Invoice Image",
    type=["png", "jpg", "jpeg"]
)

user_query = st.text_input(
    "Ask a question about the invoice",
    placeholder="e.g. What is the invoice number and total amount?"
)

# ---------------- OCR FUNCTION ----------------
def extract_text(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray)

# ---------------- EXECUTION ----------------
if st.button("Analyze Invoice"):
    if not uploaded_file or not user_query:
        st.error("Please upload an image and enter a question.")
    else:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Invoice", use_column_width=True)

        with st.spinner("Extracting text from invoice..."):
            text = extract_text(image)

        with st.spinner("Analyzing invoice..."):
            prompt = f"""
            Invoice Text:
            {text}

            Question:
            {user_query}

            Answer clearly and accurately.
            """
            response = model.generate_content(prompt)
            st.subheader("✅ Response")
            st.write(response.text)
