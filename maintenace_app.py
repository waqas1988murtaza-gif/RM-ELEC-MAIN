import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(page_title="RM E&I Automation", page_icon="🛠️", layout="wide")

# Sidebar for Stats & Info
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942503.png", width=100)
    st.title("Admin Panel")
    st.info("System is Online ✅")
    st.markdown("---")
    st.write("🛠️ **Asset Categories:** 5")
    st.write("📅 **Date:** " + pd.Timestamp.now().strftime("%d-%b-%Y"))

# Main Interface
st.title("🛠️ RM E&I Maintenance Automation")
st.markdown("Fill the form below to log inspection data directly into the system.")

# --- APNA URL YAHAN PASTE KAREIN ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzkhwqUc2fYB-9O1dV1LoB6kBA18E-ZG_xffr5upYf8FKi9xvlt0vVX0a4K30sJMGK4/exec"

# Form and View Tabs
tab1, tab2 = st.tabs(["📝 Inspection Form", "📊 Recent Logs"])

with tab1:
    with st.form("maintenance_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            inspector = st.text_input("👤 Inspector Name", placeholder="Enter your full name")
            asset = st.selectbox("🏗️ Select Asset", [
                "HMD (Hot Metal Detector)", 
                "Loop Scanner", 
                "Pyrometer", 
                "Solenoid Valve", 
                "Limit Switch",
                "Control Panel",
                "Motor Terminal Box"
            ])

        with col2:
            status = st.select_slider("⚡ Condition Status", options=["Critical", "Needs Repair", "Normal", "Good", "Excellent"], value="Normal")
            location = st.text_input("📍 Location / Line", placeholder="e.g. Roughing Mill, Stand 1")

        remarks = st.text_area("📝 Detailed Remarks / Observations", placeholder="Explain any issues or work done...")
        
        submit = st.form_submit_button("🚀 Submit Entry to Cloud")

        if submit:
            if inspector and location:
                with st.spinner("Uploading data..."):
                    # Ab hum extra details bhi bhej rahe hain
                    payload = {
                        "inspector": inspector,
                        "asset": asset,
                        "remarks": f"[{status}] at {location}: {remarks}"
                    }
                    try:
                        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
                        if "Success" in response.text:
                            st.success(f"Shukriya {inspector}! Data save ho gaya.")
                            st.balloons()
                        else:
                            st.error("Server Error!")
                    except Exception as e:
                        st.error(f"Connection Fail: {e}")
            else:
                st.warning("⚠️ Inspector Name aur Location likhna lazmi hai!")

with tab2:
    st.subheader("View Sheet Directly")
    st.write("Pichla data dekhne ke liye aap niche wala button daba kar sheet khol sakte hain:")
    st.link_button("📂 Open Google Sheet", "https://docs.google.com/spreadsheets/d/1NilFTCm_6L9yhjVeqkr6tBC9EwU32vOmS8AkY_syPKk/edit")

st.markdown("---")
st.caption("Developed for RM Electrical & Instrumentation Team")
