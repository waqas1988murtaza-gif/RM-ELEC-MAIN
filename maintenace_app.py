import streamlit as st
import requests
from datetime import datetime

# Page Settings
st.set_page_config(page_title="Naveena Steel - RM E&I", page_icon="🏗️", layout="centered")

# Custom Styling for Naveena Steel Theme
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #1d3557; color: white; border-radius: 8px; font-weight: bold; }
    .main { background-color: #f8f9fa; }
    .header-style { color: #1d3557; text-align: center; font-size: 30px; font-weight: bold; margin-bottom: 0px; }
    .checklist-box { background-color: #f1f4f9; padding: 15px; border-radius: 10px; border-left: 5px solid #1d3557; }
    </style>
    """, unsafe_allow_html=True)

# 1. Naveena Steel Logo (Using your uploaded file)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
   st.image("download.png", width=250)
st.markdown('<p class="header-style">RM Electrical & Automation Maintenance Log</p>', unsafe_allow_html=True)
st.write(f"<center>📅 {datetime.now().strftime('%d-%b-%Y')} | 🕒 {datetime.now().strftime('%I:%M %p')}</center>", unsafe_allow_html=True)
st.write("---")

# URL (Make sure this is your latest Web App URL)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwyObsneunsz5XCcdQBxXGP3dN585OHApUCH4ylrOLgFE86FUvG01jXWtC57QI8KKbIjw/exec"

# Form
with st.container():
    col_a, col_b = st.columns(2)
    with col_a:
        inspector = st.text_input("👤 Inspector Name", placeholder="e.g. Anwar")
    with col_b:
        shift = st.radio("🕒 Select Shift", ["Shift A", "Shift B"], horizontal=True)

    asset = st.selectbox("🏗️ Select Equipment / Area", [
        "HMD (Hot Metal Detector)", 
        "Loop Scanner", 
        "Pyrometer", 
        "Solenoid Valve", 
        "Limit Switch",
        "Binding Machines"
    ])

    # --- Dynamic Checklist Logic ---
    st.markdown(f'<div class="checklist-box">🔍 <b>Maintenance Checklist: {asset}</b>', unsafe_allow_html=True)
    checks = []
    
    c1, c2 = st.columns(2)
    if "HMD" in asset:
        with c1:
            if st.checkbox("Glass Cleaned"): checks.append("Glass Clean")
            if st.checkbox("Air Blowing Check"): checks.append("Air OK")
        with c2:
            if st.checkbox("Water Circulation"): checks.append("Water OK")
            if st.checkbox("Sensing Check"): checks.append("Sensing OK")
            
    elif "Loop Scanner" in asset:
        with c1:
            if st.checkbox("Lens Cleaning"): checks.append("Lens Clean")
            if st.checkbox("Mounting Tightness"): checks.append("Mounting OK")
        with c2:
            if st.checkbox("Signal Strength Check"): checks.append("Signal OK")
            
    elif "Pyrometer" in asset:
        with c1:
            if st.checkbox("Lens Cleaning"): checks.append("Lens Clean")
            if st.checkbox("Focus Alignment"): checks.append("Focus OK")
        with c2:
            if st.checkbox("Cable Inspection"): checks.append("Cable OK")
    
    else: # General for others
        with c1:
            if st.checkbox("General Cleaning"): checks.append("Cleaning Done")
            if st.checkbox("Visual Inspection"): checks.append("Visual OK")
        with c2:
            if st.checkbox("Wiring Check"): checks.append("Wiring OK")
            if st.checkbox("Operational Test"): checks.append("Ops OK")
    st.markdown('</div>', unsafe_allow_html=True)

    remarks_found = st.text_area("📝 Additional Remarks / Issues Found")

    if st.button("🚀 SUBMIT MAINTENANCE DATA"):
        if inspector:
            with st.spinner("Saving to Cloud..."):
                final_remarks = f"[{shift}] Checks: {', '.join(checks)}. Notes: {remarks_found}"
                payload = {
                    "inspector": inspector,
                    "asset": asset,
                    "remarks": final_remarks
                }
                try:
                    response = requests.post(SCRIPT_URL, json=payload, timeout=10)
                    if "Success" in response.text:
                        st.success(f"✅ Data Saved! Shukriya {inspector}.")
                        st.balloons()
                    else:
                        st.error("❌ Failed to Save. Check Apps Script.")
                except Exception as e:
                    st.error(f"❌ Connection Error: {e}")
        else:
            st.warning("⚠️ Name likhna zaroori hai!")

st.write("---")
st.caption("Developed for RM E&I Team | Naveena Steel")
