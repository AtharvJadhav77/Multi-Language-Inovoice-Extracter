# from dotenv import load_dotenv
# import os
# import streamlit as st
# from PIL import Image
# import google.generativeai as genai

# # -------------------- LOAD ENV --------------------
# load_dotenv()

# # -------------------- CONFIGURE GEMINI --------------------
# genai.configure(api_key=os.getenv("GENAI_API_KEY"))

# # -------------------- LOAD MODEL --------------------
# # Gemini 1.5 Pro supports text + image
# model = genai.GenerativeModel("gemini-1.5-flash")

# # -------------------- GEMINI RESPONSE FUNCTION --------------------
# def get_gemini_response(user_query, image, system_prompt):
#     response = model.generate_content(
#         [
#             system_prompt,
#             user_query,
#             image
#         ]
#     )
#     return response.text

# # -------------------- STREAMLIT UI --------------------
# st.set_page_config(
#     page_title="Multi-Language Invoice Extractor",
#     layout="centered"
# )

# st.title("📄 Multi-Language Invoice Extractor")
# st.write("Upload an invoice image and ask questions about it.")

# # -------------------- USER INPUT --------------------
# user_query = st.text_input(
#     "Ask a question about the invoice:",
#     placeholder="e.g. What is the total amount and invoice number?"
# )

# uploaded_file = st.file_uploader(
#     "Upload Invoice Image",
#     type=["png", "jpg", "jpeg"]
# )

# image = None
# if uploaded_file:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Invoice", use_column_width=True)

# submit = st.button("Analyze Invoice")

# # -------------------- SYSTEM PROMPT --------------------
# system_prompt = """
# You are an expert invoice analyzer.
# Extract and analyze information from invoice images.
# Answer accurately based only on the invoice content.
# If the invoice language is not English, translate when needed.
# """

# # -------------------- EXECUTION --------------------
# if submit:
#     if not uploaded_file:
#         st.error("❌ Please upload an invoice image.")
#     elif not user_query:
#         st.error("❌ Please enter a question.")
#     else:
#         with st.spinner("Analyzing invoice..."):
#             try:
#                 response = get_gemini_response(user_query, image, system_prompt)
#                 st.subheader("✅ Response")
#                 st.write(response)
#             except Exception as e:
#                 st.error(f"Error: {e}")
from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- GEMINI CLIENT ----------------
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(
    page_title="Multi-Language Invoice Extractor",
    layout="centered"
)

st.title("📄 Multi-Language Invoice Extractor (Gemini 2.5 Flash)")
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

image_bytes = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice", use_column_width=True)
    image_bytes = uploaded_file.getvalue()

submit = st.button("Analyze Invoice")

# ---------------- SYSTEM PROMPT ----------------
system_prompt = """
You are an expert invoice analyzer.
Extract accurate information from invoice images.
Translate the invoice to English if it is not in English.
Answer strictly based on the invoice content.
"""

# ---------------- GEMINI RESPONSE ----------------
def get_gemini_response(user_query, image_bytes, system_prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            system_prompt,
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg",
            ),
            user_query,
        ],
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
                    image_bytes,
                    system_prompt
                )
                st.subheader("✅ Response")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
