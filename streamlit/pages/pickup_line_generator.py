import streamlit as st
import requests

# FastAPI endpoint
API_URL = "https://dvorakinnovationai-revel-rizz-api.hf.space/api/pickup-line-generator"
# API_URL = "http://127.0.0.1:8000//api/pickup-line-generator"


st.set_page_config(page_title="Pickup Line Generator", page_icon="💘", layout="centered")

st.title("Pickup Line Generator")
st.write("Generate fun and creative pickup lines with customizable tones and attributes.")

# User query input
user_query = st.text_area("Your some Qureies? (optional)", placeholder="e.g., I have to impress her by tomorrow.")

# Tones (multi-select)
available_tones = ["romantic", "funny", "cheesy", "flirty", "sarcastic", "friendly"]
tones = st.multiselect("Select tones (optional)", available_tones)

# Attributes (must provide at least one)
attributes = st.text_area(
    "Enter attributes of that person (comma-separated, required)", 
    placeholder="e.g., coffee lover, programmer, bookworm"
)

# Button to trigger API
if st.button("Generate Pickup Line"):
    if not attributes.strip():
        st.error("⚠️ Please enter at least one attribute.")
    else:
        try:
            # Process attributes into list
            attributes_list = [attr.strip() for attr in attributes.split(",") if attr.strip()]

            payload = {
                "user_query": user_query if user_query.strip() else '',
                "tones": tones if tones else None,
                "attributes": attributes_list,
            }

            with st.spinner("💫 Generating pickup lines..."):
                response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                data = response.json()
                st.success("✅ Pickup lines generated successfully!")
                st.write("### Your Pickup Lines:")
                st.json(response.json())

            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"🚨 An error occurred: {str(e)}")
