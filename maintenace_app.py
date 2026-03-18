import streamlit as st
import requests
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Naveena Steel - RM E&I", page_icon="🏗️", layout="wide")

# Professional Industry Theme
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button { width: 100%; background-color: #1d3557; color: white; border-radius: 8px; font-weight: bold; height: 3.5em; border: none; }
    .stButton>button:hover { background-color: #457b9d; color: white; }
    h1 { color: #1d3557; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; }
    .stCheckbox { font-size: 18px; padding: 5px; }
    .css-1544g2n { padding: 2rem 1rem 1.5rem; }
    </style>
    """, unsafe_allow_html=True)

# 1. Header with Official Logo
col_logo, col_text = st.columns([1, 3])
with col_logo:
    st.image("https://naveenasteel.com/wp-content/uploads/2020/06/Naveena-Steel-Logo.png", width=200)
with col_text:
    st.title("RM E&I Maintenance Log System")
    st.write(f"📅 **Date:** {datetime.now().strftime('%d-%m-%Y')} | 🕒 **Time:** {datetime.now().strftime('%I:%M %p')}")

st.markdown("---")

# --- YOUR WORKING SCRIPT URL ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzkhwqUc2fYB-9O1dV1LoB6kBA18E-ZG_xffr5upYf8FKi9xvlt0vVX0a4K30sJMGK4/exec"

with st.container():
    # Top Section: User Info
    c1, c2, c3 = st.columns(3)
    with c1:
        inspector = st.text_input("👤 Inspector Name", placeholder="Type your name...")
    with c2:
        # Fixed 12-Hour Shifts: Only A and B
        shift = st.radio("🕒 Select 12-Hour Shift", ["Shift A", "Shift B"], horizontal=True)
    with c3:
        asset_list = ["HMD", "Loop Scanner", "Pyrometer", "Solenoid Valve", "Limit Switch", "Control Panel"]
        selected_asset = st.selectbox("🏗️ Select Equipment", asset_list)

    st.markdown("### 🔍 Technical Checklist")
    st.info(f"Please complete the mandatory checks for **{selected_asset}**")
    
    # Checklist Logic based on your requirement
    checks = []
    col_a, col_b = st.columns(2)

    if selected_asset == "HMD":
        with col_a:
            if st.checkbox("✅ Glass Cleaning Done"): checks.append("Glass Cleaned")
            if st.checkbox("✅ Air Purging Pressure OK"): checks.append("Air OK")
        with col_b:
            if st.checkbox("✅ Water Circulation Flow Check"): checks.append("Water OK")
            if st.checkbox("✅ Sensing/Signal Feedback Test"): checks.append("Sensing OK")

    elif selected_asset == "Loop Scanner":
        with col_a:
            if st.checkbox("✅ Lens Cleaning Done"): checks.append("Lens Cleaned")
            if st.checkbox("✅ Internal Cooling Fan Check"): checks.append("Cooling OK")
        with col_b:
            if st.checkbox("✅ Mounting & Alignment Check"): checks.append("Mounting OK")
            if st.checkbox("✅ Cable Insulation/Connection"): checks.append("Cable OK")

    elif selected_asset == "Pyrometer":
        with col_a:
            if st.checkbox("✅ Optical Lens Cleaning"): checks.append("Lens Cleaned")
            if st.checkbox("✅ Air Purging Line Check"): checks.append("Air OK")
        with col_b:
            if st.checkbox("✅ Temperature Accuracy Test"): checks.append("Temp OK")
            if st.checkbox("✅ Alignment with Hot Metal"): checks.append("Alignment OK")

    else:
        with col_a:
            if st.checkbox("✅ Physical Condition/Cleaning"): checks.append("Physical OK")
            if st.checkbox("✅ Terminal Tightness (Electrical)"): checks.append("Terminals OK")
        with col_b:
            if st.checkbox("✅ Operational Signal Check"): checks.append("Operation OK")

    st.markdown("---")

    # Final Remarks
    remarks_input = st.text_area("📝 Additional Remarks (Optional)", placeholder="Enter details of any fault or action taken...")
    
    # Formatting data for Sheet
    combined_remarks = f"[{shift}] " + (", ".join(checks) if checks else "Routine Check") + f" | Details: {remarks_input}"

    # Submit Button
    if st.button("🚀 SUBMIT TO NAVEENA CLOUD"):
        if inspector:
            with st.spinner("Synchronizing with Database..."):
                payload = {
                    "inspector": inspector,
                    "asset": selected_asset,
                    "remarks": combined_remarks
                }
                try:
                    response = requests.post(SCRIPT_URL, json=payload, timeout=12)
                    if "Success" in response.text:
                        st.success(f"✅ Data Logged! Excellent work, {inspector}.")
                        st.balloons()
                    else:
                        st.error("❌ Error: Sheet connection failed. Check Web App URL.")
                except Exception as e:
                    st.error(f"❌ Connection Error: {e}")
        else:
            st.warning("⚠️ Enter your name first!")

st.markdown("---")
st.caption("© 2026 Naveena Steel Mills | RM Electrical & Instrumentation Department")
