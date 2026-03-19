import streamlit as st
import requests
from datetime import datetime

# Page Config
st.set_page_config(page_title="Naveena Steel - RM E&I", page_icon="🏗️", layout="centered")

# Custom CSS for Naveena Theme
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #1d3557; color: white; border-radius: 8px; font-weight: bold; }
    .checklist-box { background-color: #f1f4f9; padding: 15px; border-radius: 10px; border-left: 5px solid #1d3557; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Logo aur Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("download.png", use_container_width=True)

st.markdown("<h2 style='text-align: center; color: #1d3557;'>RM E&I Maintenance Automation</h2>", unsafe_allow_html=True)
st.write(f"<center>📅 {datetime.now().strftime('%d-%b-%Y')} | 🕒 {datetime.now().strftime('%I:%M %p')}</center>", unsafe_allow_html=True)
st.write("---")

# Your Script URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwyObsneunsz5XCcdQBxXGP3dN585OHApUCH4ylrOLgFE86FUvG01jXWtC57QI8KKbIjw/exec"

# Form start
with st.container():
    c_a, c_b = st.columns(2)
    with c_a:
        inspector = st.text_input("👤 Inspector Name")
    with c_b:
        shift = st.radio("🕒 Shift", ["Shift A", "Shift B"], horizontal=True)

    # 19 Items from Excel
    asset_options = [
        "1. HMD (Hot Metal Detector)", "2. Pyrometer", "3. Loop Scanner", 
        "4. Mill Stand Motors", "5. Shear Motors", "6. Pinch Roll Motor & Blower",
        "7. Roller Table Motors", "8. Cooling Bed BLVs", "9. BLS", 
        "10. Binding Machines", "11. TS Panels", "12. ET IH (Panels & Coils)",
        "13. EOT Cranes", "14. Atlas Copco Compressors", "15. Pump House & Filtration",
        "16. Lathe & CNC Machines", "17. Transformers", "18. RHF Panels/Motors", "19. MV Panels"
    ]
    asset = st.selectbox("🏗️ Select Equipment (Excel Item)", asset_options)

    # Checklist Logic based on your Excel Sheet
    st.markdown(f'<div class="checklist-box"><b>🔍 Maintenance Checklist: {asset}</b>', unsafe_allow_html=True)
    checks = []
    
    col_v1, col_v2 = st.columns(2)
    
    if "HMD" in asset:
        with col_v1:
            if st.checkbox("Clean lens/glass"): checks.append("Lens Clean")
            if st.checkbox("Check alignment"): checks.append("Align OK")
        with col_v2:
            if st.checkbox("Verify power LED"): checks.append("LED OK")
            if st.checkbox("Air purging check"): checks.append("Air OK")
            
    elif "Pyrometer" in asset:
        with col_v1:
            if st.checkbox("Check display reading"): checks.append("Display OK")
        with col_v2:
            if st.checkbox("Sighting window clean"): checks.append("Window Clean")
            
    elif "Mill Stand Motors" in asset:
        with col_v1:
            if st.checkbox("Monitor sound/vibration"): checks.append("Vibration OK")
        with col_v2:
            if st.checkbox("Check VFD fault logs"): checks.append("VFD Logs OK")

    elif "Compressors" in asset:
        with col_v1:
            if st.checkbox("Check oil/temp logs"): checks.append("Logs OK")
        with col_v2:
            if st.checkbox("Abnormal alarm check"): checks.append("Alarms OK")
    
    else: # General for others
        with col_v1:
            if st.checkbox("Visual Inspection OK"): checks.append("Visual OK")
        with col_v2:
            if st.checkbox("Functional Test OK"): checks.append("Functional OK")

    st.markdown('</div>', unsafe_allow_html=True)
    remarks = st.text_area("📝 Additional Remarks")

    if st.button("🚀 SUBMIT TO SHEET"):
        if inspector:
            with st.spinner("Uploading..."):
                final_data = f"[{shift}] Checks: {', '.join(checks)}. {remarks}"
                payload = {"inspector": inspector, "asset": asset, "remarks": final_data}
                try:
                    res = requests.post(SCRIPT_URL, json=payload, timeout=10)
                    if "Success" in res.text:
                        st.success("✅ Excel Record Updated!")
                        st.balloons()
                except:
                    st.error("Connection Error!")
        else:
            st.warning("Please enter Inspector Name.")
