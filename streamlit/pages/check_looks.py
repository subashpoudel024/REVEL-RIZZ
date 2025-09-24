import streamlit as st
import requests
import base64

# FastAPI endpoint
API_URL = "https://dvorakinnovationai-revel-rizz-api.hf.space/api/looks-analyzer"  # Change if deployed elsewhere

st.set_page_config(page_title="Looks Analyzer", page_icon="🧑‍🎨", layout="centered")

st.title("Looks Analyzer")
st.write("Upload your image and get style & looks suggestions!")

# Upload image
uploaded_file = st.file_uploader("Upload an image (JPG/PNG)", type=["jpg", "jpeg", "png"])

# User query input
user_query = st.text_area("Enter your query (optional)", placeholder="e.g., How do I look in this outfit?")

# Button to trigger API
if st.button("Analyze Looks"):
    if uploaded_file is None:
        st.error("⚠️ Please upload an image.")
    else:
        try:
            # Convert image to base64
            image_bytes = uploaded_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            payload = {
                "image_base64": image_base64,
                "user_query": user_query if user_query.strip() else None,
            }

            with st.spinner("✨ Analyzing your looks..."):
                response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                data = response.json()
                st.success("✅ Analysis complete!")
                st.write("### Suggestions:")
                st.json(data)
             
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"🚨 An error occurred: {str(e)}")
