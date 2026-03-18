import streamlit as st
import requests

# Page settings for a cleaner look
st.set_page_config(page_title="RM E&I Automation", page_icon="⚙️", layout="centered")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    .stTextInput>div>div>input, .stSelectbox>div>div>select { border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Header with Logo
st.image("https://cdn-icons-png.flaticon.com/512/2942/2942503.png", width=70)
st.title("RM E&I Maintenance Log")
st.write("---")

# Your working Script URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzkhwqUc2fYB-9O1dV1LoB6kBA18E-ZG_xffr5upYf8FKi9xvlt0vVX0a4K30sJMGK4/exec"

# Simple Form
with st.container():
    inspector = st.text_input("👤 Inspector Name", placeholder="Enter Name")
    
    asset = st.selectbox("🏗️ Select Asset", [
        "HMD (Hot Metal Detector)", 
        "Loop Scanner", 
        "Pyrometer", 
        "Solenoid Valve", 
        "Limit Switch"
    ])
    
    remarks = st.text_area("📝 Remarks", placeholder="Write any observation here...")

    if st.button("🚀 Submit Data"):
        if inspector:
            with st.spinner("Saving..."):
                payload = {
                    "inspector": inspector,
                    "asset": asset,
                    "remarks": remarks
                }
                try:
                    response = requests.post(SCRIPT_URL, json=payload, timeout=10)
                    if "Success" in response.text:
                        st.success(f"✅ Data for {inspector} saved successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to save.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Please enter your name first.")

st.write("---")
st.caption("RM Electrical & Instrumentation Team | 2026")
