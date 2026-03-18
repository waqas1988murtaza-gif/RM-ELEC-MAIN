import streamlit as st
import requests
from datetime import datetime

# Page Settings
st.set_page_config(page_title="Naveena Steel - RM E&I", page_icon="🏗️", layout="centered")

# Custom Styling for Naveena Steel Theme
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #1d3557; color: white; border-radius: 8px; height: 3em; font-weight: bold; }
    .main { background-color: #f8f9fa; }
    h1 { color: #1d3557; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 1. Naveena Steel Logo aur Header
# Note: Agar aapke paas apna link hai to 'image_url' ki jagah wo daal dein
st.image("https://naveenasteel.com/wp-content/uploads/2020/06/Naveena-Steel-Logo.png", width=250)
st.title("RM E&I Maintenance Log")
st.write(f"📅 **Date:** {datetime.now().strftime('%d-%b-%Y')} | 🕒 **Time:** {datetime.now().strftime('%I:%M %p')}")
st.write("---")

# --- APNA UPDATED URL YAHAN DAALEIN ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwyObsneunsz5XCcdQBxXGP3dN585OHApUCH4ylrOLgFE86FUvG01jXWtC57QI8KKbIjw/exec"

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        inspector = st.text_input("👤 Inspector Name", placeholder="Enter Name")
        asset = st.selectbox("🏗️ Select Asset", [
            "HMD (Hot Metal Detector)", 
            "Loop Scanner", 
            "Pyrometer", 
            "Solenoid Valve", 
            "Limit Switch"
        ])
    
    with col2:
        # 2. Main Shift Option
        shift = st.radio("🕒 Select Shift", ["Shift A", "Shift B", "Shift C"], horizontal=True)
        location = st.text_input("📍 Location/Area", placeholder="e.g. Roughing Mill")

    remarks = st.text_area("📝 Remarks / Observations", placeholder="Details of work done...")

    if st.button("🚀 Submit to Cloud"):
        if inspector:
            with st.spinner("Recording to Naveena Steel Database..."):
                # Data pack kar rahe hain
                payload = {
                    "inspector": inspector,
                    "asset": asset,
                    "remarks": f"[{shift}] {location}: {remarks}"
                }
                try:
                    response = requests.post(SCRIPT_URL, json=payload, timeout=10)
                    if "Success" in response.text:
                        st.success(f"✅ Shukriya {inspector}! Shift {shift} ka data save ho gaya.")
                        st.balloons()
                    else:
                        st.error("❌ Connection Issue: Sheet did not respond.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Inspector Name likhna zaroori hai!")

st.write("---")
st.caption("Developed for RM Electrical & Instrumentation | Naveena Steel")
