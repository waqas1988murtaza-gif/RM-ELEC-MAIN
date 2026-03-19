import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Naveena Steel - RM Maintenance", page_icon="🏗️", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #1d3557; color: white; border-radius: 8px; font-weight: bold; height: 3em; }
    .checklist-box { background-color: #f1f4f9; padding: 20px; border-radius: 10px; border-left: 10px solid #1d3557; }
    </style>
    """, unsafe_allow_html=True)

# Logo
st.image("download.png", width=200)
st.title("RM E&I Maintenance Log")
st.write(f"📅 {datetime.now().strftime('%d-%b-%Y')} | 🕒 {datetime.now().strftime('%I:%M %p')}")

# SCRIPT URL (Apna wala yahan daalein)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyZf9a8rIJSUJ0BCGIJLXO0bIiLvZCujELboKVt__GSn1crsYJuPbsy1MwDhOyIjdpKKg/exec"

# 19 Items Dictionary based on your Excel
assets_data = {
    "1. HMD": ["Clean lens/glass", "Check alignment", "Verify power LED status", "Air purging flow"],
    "2. Pyrometer": ["Check display reading", "Verify sighting window clean", "4-20mA output check"],
    "3. Loop Scanner": ["Verify loop height on HMI", "Check sensor status LEDs", "Clean sensor face"],
    "4. Mill Stand Motors": ["Monitor sound/vibration", "Check VFD fault logs", "Verify cooling airflow"],
    "5. Shear Motors": ["Monitor sound/vibration", "Check cooling fan airflow", "Inspect limit switches"],
    "6. Pinch Roll Motor & Blower": ["Check motor vibration", "Inspect blower belt/coupling"],
    "7. Roller Table Motors": ["Visual inspection of motors", "Check for abnormal heating"],
    "8. Cooling Bed BLVs": ["Check blower operation", "Inspect control panel indicators"],
    "9. BLS": ["Verify operational logic", "Check sensor feedback"],
    "10. Binding Machines": ["Check hydraulic/electrical sync", "Inspect limit switches"],
    "11. TS Panels": ["Check indicator lamps", "Verify selector switch positions"],
    "12. ET IH (Panels & Coils)": ["Check coil insulation", "Monitor panel temperature"],
    "13. EOT Cranes": ["Check hoist/long travel motors", "Inspect pendant/remote control"],
    "14. Atlas Copco Compressors": ["Check oil/temp logs", "Check for abnormal alarms", "Take motor load"],
    "15. Pump House & Filtration": ["Check pump motor temp", "Take load of motors", "Verify panel lamps"],
    "16. Lathe & CNC Machines": ["Check ACs/Motors/HMI", "Visual check of wiring"],
    "17. Transformers": ["Check Winding Temp", "Check Oil Temp", "Verify Terminals"],
    "18. RHF Panels/Motors": ["Check instrument readings", "Visual panel inspection"],
    "19. MV Panels": ["Take KWh Reading", "Check relay status", "Inspect VCB/Multimeter"]
}

with st.container():
    col_name, col_shift = st.columns(2)
    with col_name:
        inspector = st.text_input("👤 Inspector Name")
    with col_shift:
        shift = st.radio("🕒 Shift", ["Shift A", "Shift B"], horizontal=True)

    asset_choice = st.selectbox("🏗️ Select Equipment", list(assets_data.keys()))
    
    # Checklist Display
    st.markdown(f'<div class="checklist-box">🔍 <b>Daily Maintenance Checklist:</b>', unsafe_allow_html=True)
    selected_checks = []
    points = assets_data[asset_choice]
    
    for point in points:
        if st.checkbox(point):
            selected_checks.append(point)
    st.markdown('</div>', unsafe_allow_html=True)

    remarks = st.text_area("📝 Remarks / Issues Found")

    if st.button("🚀 SUBMIT TO EXCEL"):
        if inspector:
            payload = {
                "inspector": inspector,
                "shift": shift,
                "asset": asset_choice,
                "checks": ", ".join(selected_checks),
                "remarks": remarks
            }
            try:
                res = requests.post(SCRIPT_URL, json=payload, timeout=10)
                if "Success" in res.text:
                    st.success("✅ Data saved in Excel format!")
                    st.balloons()
            except:
                st.error("Connection error!")
