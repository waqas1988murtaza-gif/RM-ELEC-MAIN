import streamlit as st
import requests

# --- CONFIG ---
# Apna Google Script URL yahan paste karein
SCRIPT_URL = "https://script.google.com/macros/library/d/1rkg0F1-sn974tWCUfcE2AkfJcie4pHWK5v6VPRsf2NyLlm0cwTcP9DxQ/16" 
ADMIN_PWD = "NAVEENA_ADMIN"

st.set_page_config(page_title="Naveena RM Maintenance", layout="centered")

# --- AUTO-UPDATE DATA ---
# Bhai, maine yahan saari categories aur units khud daal diye hain
default_assets = {
    "HMD (Hot Metal Detectors)": [f"HMD-{i}" for i in range(1, 101)],
    "Pyrometers": ["Pyrometer-Entrance", "Pyrometer-Exit", "Pyrometer-Roughing", "Pyrometer-Finishing"],
    "Loop Scanners": [f"LS-{i}" for i in range(1, 15)],
    "Pulse Generators": ["PG-1", "PG-2", "PG-3", "PG-4"],
    "Pressure Switches": ["Oil Pressure", "Water Pressure", "Air Pressure"],
    "VFD Drives": ["Main Stand VFD", "Roughing VFD", "Pinch Roll VFD"],
    "Control Panels": ["Main PCC", "MCC-1", "MCC-2", "LCP-Automation"],
    "Emergency Switches": ["E-Stop Zone 1", "E-Stop Zone 2", "E-Stop Zone 3"]
}

st.image("https://raw.githubusercontent.com/waqas1988murtaza/Naveena-Steel/main/download.png", width=120)
st.title("⚡ RM E&I Maintenance Log")

# Admin Section (Password Protected) - Sirf extra cheezon ke liye
with st.expander("⚙️ Admin: Update Items"):
    pwd = st.text_input("Admin Password", type="password")
    if pwd == ADMIN_PWD:
        st.info("Bhai, yahan se aap mazeed nayi cheezain add kar sakte hain.")
        # (Yahan add category/item ka purana code hai)

st.divider()

# --- MAIN FORM ---
name = st.text_input("Inspector Name", placeholder="Apna naam likhein")
shift = st.radio("Shift Selection", ["Shift A", "Shift B"], horizontal=True)

# 1. Main Category Select karein
parent_selection = st.selectbox("Select Equipment Group", list(default_assets.keys()))

# 2. Sub-Category (HMD 1-100 wagera khud yahan ayenge)
child_options = default_assets.get(parent_selection, [])
child_selection = st.selectbox(f"Select Specific {parent_selection}", child_options)

st.info(f"📝 Checklist for {child_selection}")
col_c1, col_c2 = st.columns(2)
with col_c1:
    c1 = st.checkbox("Clean lens / Sensor Body")
    c2 = st.checkbox("Check Wiring / Mounting")
with col_c2:
    c3 = st.checkbox("Power/Signal Status OK")
    c4 = st.checkbox("Alignment Verified")

# Remarks (Khali box, user khud type karega)
remarks = st.text_area("Remarks / Maintenance Details", placeholder="Observation likhein (e.g. Lens cleaned, cable replaced)")

if st.button("🚀 SUBMIT TO GOOGLE SHEET", type="primary"):
    if not name:
        st.error("Bhai, pehle apna naam to likho!")
    else:
        payload = {
            "type": "LOG_ENTRY",
            "inspector": name,
            "shift": shift,
            "parent": parent_selection,
            "child": child_selection,
            "remarks": remarks
        }
        try:
            res = requests.post(SCRIPT_URL, json=payload, timeout=15)
            if "Success" in res.text:
                st.success(f"Mubarak ho! {child_selection} ka data save ho gaya.")
                st.balloons()
            else:
                st.error("Google Sheet error! Permission check karein.")
        except:
            st.error("Connection failed! Script URL sahi se paste karein.")
