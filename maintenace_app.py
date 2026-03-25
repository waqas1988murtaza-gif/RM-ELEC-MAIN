import streamlit as st
import requests
from datetime import datetime
from google import genai

# Page setup
st.set_page_config(page_title="Naveena Steel - RM Maintenance", page_icon="🏗️", layout="centered")

# --- AI SETUP (Direct Secrets Access) ---
# Hum check kar rahe hain ke key mil rahi hai ya nahi
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        # Agar key mil gayi to warning nahi dikhayenge
    except Exception as e:
        st.error(f"AI Connection Error: {e}")
else:
    st.warning("⚠️ AI Key missing! Streamlit Secrets mein GEMINI_API_KEY add karein.")

# Custom CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #1d3557; color: white; border-radius: 8px; font-weight: bold; height: 3em; }
    .checklist-box { background-color: #f1f4f9; padding: 20px; border-radius: 10px; border-left: 10px solid #1d3557; margin-bottom: 20px; }
    .ai-response { background-color: #e8f0fe; padding: 15px; border-radius: 10px; border: 1px solid #4285f4; color: #1d3557; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Logo aur Title
st.image("download.png", width=250)
st.title("RM E&I Maintenance Log")
st.write(f"📅 {datetime.now().strftime('%d-%b-%Y')} | 🕒 {datetime.now().strftime('%I:%M %p')}")

# SCRIPT URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyZf9a8rIJSUJ0BCGIJLXO0bIiLvZCujELboKVt__GSn1crsYJuPbsy1MwDhOyIjdpKKg/exec"

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
    
    st.markdown(f'<div class="checklist-box">🔍 <b>Maintenance Checklist:</b>', unsafe_allow_html=True)
    selected_checks = []
    for point in assets_data[asset_choice]:
        if st.checkbox(point):
            selected_checks.append(point)
    st.markdown('</div>', unsafe_allow_html=True)

    remarks = st.text_area("📝 Remarks / Issues Found")

    # AI Button
    if remarks and api_key:
        if st.button("🤖 Ask AI for Fix?"):
            with st.spinner('Gemini AI solution dhoond raha hai...'):
                try:
                    prompt = f"Technical issue in {asset_choice}: {remarks}. Give 3 quick fix points in Roman Urdu."
                    response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
                    st.markdown(f'<div class="ai-response"><b>AI Suggestion:</b><br>{response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"AI Error: {e}")

    # Submit to Excel
    if st.button("🚀 SUBMIT TO EXCEL"):
        if inspector:
            payload = {"inspector": inspector, "shift": shift, "asset": asset_choice, "checks": ", ".join(selected_checks), "remarks": remarks}
            try:
                res = requests.post(SCRIPT_URL, json=payload, timeout=10)
                st.success("✅ Data saved in Excel!")
                st.balloons()
            except:
                st.error("Connection error!")
