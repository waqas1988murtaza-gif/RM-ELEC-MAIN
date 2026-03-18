import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Page Configuration for Wide Layout
st.set_page_config(page_title="Naveena Steel - RM Maintenance Automation", page_icon="🏗️", layout="wide")

# Custom CSS for Colorful Professional Theme
st.markdown("""
    <style>
    .main { background-color: #e9ecef; }
    .stSidebar { background-color: #1d3557; color: white; }
    h1 { color: #1d3557; text-align: center; }
    .status-card { padding: 15px; border-radius: 8px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;}
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #007bff; color: white; font-weight: bold;}
    .stTab { background-color: #f8f9fa; border-radius: 8px;}
    </style>
    """, unsafe_allow_html=True)

# sidebar structure
with st.sidebar:
    st.image("https://naveenasteel.com/wp-content/uploads/2020/06/Naveena-Steel-Logo.png", width=200)
    st.title("Admin Panel")
    st.info("⚡ System is Online ✅")
    st.markdown("---")
    st.write("🛠️ **Asset Categories:** 5")
    st.write("📅 **Date:** " + pd.Timestamp.now().strftime("%d-%b-%Y"))
    st.write("Shift: main")

# Main Header
st.title("🏗️ RM E&I Maintenance Automation")
st.markdown("Enter maintenance details below to log data to Google Sheets.")
st.write(f"📅 **Date:** {datetime.now().strftime('%d-%b-%Y')} | 🕒 **Time:** {datetime.now().strftime('%I:%M %p')}")
st.write("---")

# --- NAYA URL YAHAN DAALEIN ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwyObsneunsz5XCcdQBxXGP3dN585OHApUCH4ylrOLgFE86FUvG01jXWtC57QI8KKbIjw/exec"

# Tabs for organize the view
tab1, tab2 = st.tabs(["📝 Inspection Form", "📂 Recent Logs"])

with tab1:
    with st.container():
        inspector = st.text_input("👤 Inspector Name", placeholder="Enter your full name")
        
        asset_list = [
            "HMD (Hot Metal Detector)", 
            "Loop Scanner", 
            "Pyrometer", 
            "Solenoid Valve", 
            "Limit Switch"
        ]
        asset = st.selectbox("🏗️ Select Asset", asset_list)
        
        # --- Specific Condition Checkboxes for HMD ---
        hmd_checks = []
        if asset == "HMD (Hot Metal Detector)":
            st.write("🔍 **HMD Checklist:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                glass_clean = st.checkbox("Glass Cleaned?", value=False)
                if glass_clean: hmd_checks.append("Glass Cleaned")
            with col2:
                air_check = st.checkbox("Air Pressure OK?", value=False)
                if air_check: hmd_checks.append("Air OK")
            with col3:
                water_circulation = st.checkbox("Water Circulation OK?", value=False)
                if water_circulation: hmd_checks.append("Water OK")
                sensing_check = st.checkbox("Sensing Working?", value=False)
                if sensing_check: hmd_checks.append("Sensing OK")

        # Combining specific checks into remarks
        checks_text = ", ".join(hmd_checks)
        if checks_text:
            final_remarks = f"Checks: {checks_text}. "
        else:
            final_remarks = ""

        raw_remarks = st.text_area("📝 Additional Remarks", placeholder="Write any extra observations here...")
        remarks = final_remarks + raw_remarks

        # Colorful Submit Button
        if st.button("🚀 Submit Data to Cloud"):
            if inspector and asset:
                with st.spinner("Processing..."):
                    payload = {
                        "inspector": inspector,
                        "asset": asset,
                        "remarks": remarks
                    }
                    try:
                        # Adding timeout to prevent hanging
                        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
                        if "Success" in response.text:
                            st.success(f"✅ Data for {inspector} regarding {asset} saved successfully!")
                            st.balloons()
                        else:
                            st.error(f"❌ Server Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Connection Fail: {e}")
            else:
                st.warning("⚠️ Please enter Inspector Name.")

with tab2:
    st.subheader("Sheet Logs")
    st.write("Recent entries from Google Sheet will appear here. Press to open full sheet.")
    st.link_button("📂 Open Google Sheet", "https://docs.google.com/spreadsheets/d/1NilFTCm_6L9yhjVeqkr6tBC9EwU32vOmS8AkY_syPKk/edit")

st.markdown("---")
st.caption("Developed for RM Electrical & Instrumentation | Naveena Steel")
