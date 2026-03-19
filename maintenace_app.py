import streamlit as st
import requests
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Naveena Steel - RM E&I", page_icon="🏗️", layout="wide")

# Custom CSS for Naveena Steel Theme
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #1d3557; color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    h1 { color: #1d3557; text-align: center; font-weight: 800; }
    .stCheckbox { font-size: 16px; }
    .category-header { background-color: #1d3557; color: white; padding: 10px; border-radius: 5px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 1. Header & Branding
col_logo, col_head = st.columns([1, 4])
with col_logo:
    st.image("https://naveenasteel.com/wp-content/uploads/2020/06/Naveena-Steel-Logo.png", width=180)
with col_head:
    st.title("RM Electrical & Automation Maintenance Log")
    st.write(f"📅 {datetime.now().strftime('%d-%b-%Y')} | 🕒 {datetime.now().strftime('%I:%M %p')} | **Shift A & B (12 Hours)**")

st.write("---")

# --- SCRIPT URL (Don't forget to update this if needed) ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwyObsneunsz5XCcdQBxXGP3dN585OHApUCH4ylrOLgFE86FUvG01jXWtC57QI8KKbIjw/exec"

# 2. User & Equipment Selection
with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        inspector = st.text_input("👤 Inspector Name", placeholder="Enter Name")
    with c2:
        shift = st.radio("🕒 Select Shift", ["Shift A", "Shift B"], horizontal=True)
    with c3:
        # Saare 19 items aapki list ke mutabiq
        equipment_list = [
            "1. HMD (Hot Metal Detector)", "2. Pyrometer", "3. Loop Scanner",
            "4. Mill Stand Motors", "5. Shear Motors", "6. Pinch Roll Motor",
            "7. Roller Table Motors", "8. Cooling Bed BLVs", "9. BLS",
            "10. Binding Machines", "11. TS Panels", "12. ET IH (Panels & Coils)",
            "13. EOT Cranes", "14. Atlas Copco Compressors", "15. Pump House & Scale Filtration",
            "16. Lathe & CNC Machines", "17. Transformers", "18. RHF (Panel & Motors)",
            "19. MV Panel Room"
        ]
        selected_equipment = st.selectbox("🏗️ Select Equipment / Area", equipment_list)

st.markdown(f"<div class='category-header'>🔍 Maintenance Checklist: {selected_equipment}</div>", unsafe_allow_html=True)

# 3. Dynamic Checkboxes according to your Excel Sheet
checks = []
col_a, col_b = st.columns(2)

with st.container():
    # Automation & Sensors
    if "HMD" in selected_equipment:
        with col_a:
            if st.checkbox("Lens/Glass Cleaning"): checks.append("Lens Clean")
            if st.checkbox("Alignment Check"): checks.append("Alignment OK")
        with col_b:
            if st.checkbox("Air Purging Flow"): checks.append("Air OK")
            if st.checkbox("Power/Signal LED Status"): checks.append("LED OK")

    elif "Pyrometer" in selected_equipment:
        with col_a:
            if st.checkbox("Optical Lens Cleaning"): checks.append("Lens Clean")
            if st.checkbox("Sighting Window Check"): checks.append("Window OK")
        with col_b:
            if st.checkbox("Display Reading vs Reference"): checks.append("Reading OK")
            if st.checkbox("Cable/Connector Inspection"): checks.append("Cable OK")

    elif "Loop Scanner" in selected_equipment:
        with col_a:
            if st.checkbox("Sensor Face Cleaning"): checks.append("Face Clean")
            if st.checkbox("HMI Reading Verification"): checks.append("HMI OK")
        with col_b:
            if st.checkbox("Mounting Bracket Stability"): checks.append("Mounting OK")
            if st.checkbox("Cooling/Air Check"): checks.append("Cooling OK")

    # Motors & Power
    elif "Motor" in selected_equipment or "Shear" in selected_equipment:
        with col_a:
            if st.checkbox("Sound & Vibration Check"): checks.append("Vibration OK")
            if st.checkbox("Cooling Blower/Fan Status"): checks.append("Blower OK")
        with col_b:
            if st.checkbox("VFD/Drive Fault Log Check"): checks.append("No Faults")
            if st.checkbox("Terminal Box Inspection"): checks.append("Terminals OK")

    elif "Transformers" in selected_equipment:
        with col_a:
            if st.checkbox("Oil Level Check"): checks.append("Oil OK")
            if st.checkbox("Winding/Oil Temperature"): checks.append("Temp OK")
        with col_b:
            if st.checkbox("Silica Gel Condition"): checks.append("Silica Gel OK")
            if st.checkbox("Terminal/Bushings Inspection"): checks.append("Terminals OK")

    elif "MV Panel" in selected_equipment or "TS Panels" in selected_equipment:
        with col_a:
            if st.checkbox("Panel Cleaning & Inspection"): checks.append("Cleaned")
            if st.checkbox("Indication Lamps Check"): checks.append("Indications OK")
        with col_b:
            if st.checkbox("KWh/Reading Recording"): checks.append("Reading Taken")
            if st.checkbox("Relay/VCB Status Check"): checks.append("VCB OK")

    else:
        with col_a:
            if st.checkbox("General Cleaning Done"): checks.append("Cleaned")
            if st.checkbox("Visual Inspection OK"): checks.append("Visual OK")
        with col_b:
            if st.checkbox("Operational Test Successful"): checks.append("Operational OK")
            if st.checkbox("Wiring/Connection Check"): checks.append("Wiring OK")

st.markdown("---")

# 4. Remarks and Submission
remarks_text = st.text_area("📝 Remarks / Issues Found", placeholder="Detail any faults, abnormal sounds, or repairs done...")

if st.button("🚀 SUBMIT LOG TO NAVEENA CLOUD"):
    if inspector:
        with st.spinner("Logging data..."):
            # Sab kuch ek line mein merge karna sheet ke liye
            formatted_remarks = f"[{shift}] " + (", ".join(checks) if checks else "Routine Check") + f" | Remarks: {remarks_text}"
            
            payload = {
                "inspector": inspector,
                "asset": selected_equipment,
                "remarks": formatted_remarks
            }
            try:
                response = requests.post(SCRIPT_URL, json=payload, timeout=12)
                if "Success" in response.text:
                    st.success(f"✅ Successful! Thank you {inspector} for the update.")
                    st.balloons()
                else:
                    st.error("❌ Submission Failed. Check Google Script URL.")
            except Exception as e:
                st.error(f"❌ Connection Error: {e}")
    else:
        st.warning("⚠️ Please enter your name before submitting.")

st.write("---")
st.caption("Developed for RM Electrical & Automation Department | Naveena Steel Mills")
