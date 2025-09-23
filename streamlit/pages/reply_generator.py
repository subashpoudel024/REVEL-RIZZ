import streamlit as st
import requests
import base64

# FastAPI endpoint
API_URL = "http://localhost:8000/api/reply-generator"  # Change if deployed elsewhere

st.set_page_config(page_title="Reply Generator", page_icon="💬", layout="centered")

st.title("💬 Reply Generator")
st.write("Upload an image, ask a question, and get AI-powered replies.")

# Upload image
uploaded_file = st.file_uploader("Upload an image (JPG/PNG)", type=["jpg", "jpeg", "png"])

# User query input
user_query = st.text_area("Enter your query", placeholder="Type your question here...")

# Tones (multi-select)
available_tones = ["formal", "casual", "friendly", "professional", "humorous"]
tones = st.multiselect("Select tones (optional)", available_tones)

# Button to trigger API
if st.button("Generate Reply"):
    if uploaded_file is None:
        st.error("⚠️ Please upload an image first.")
    elif not user_query.strip():
        st.error("⚠️ Please enter a query.")
    else:
        try:
            # Convert image to base64
            image_bytes = uploaded_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            payload = {
                "image_base64": image_base64,
                "user_query": user_query,
                "tones": tones if tones else None,
            }

            with st.spinner("⏳ Generating reply..."):
                response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                data = response.json()
                st.success("✅ Reply generated successfully!")
                st.write("### Response:")
                st.json(response.json())
   
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"🚨 An error occurred: {str(e)}")
