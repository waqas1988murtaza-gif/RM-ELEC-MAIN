import streamlit as st
import requests
from datetime import datetime
import google.generativeai as genai  # AI library add ki hai

st.set_page_config(page_title="Naveena Steel - RM Maintenance", page_icon="🏗️", layout="centered")

# --- 1. AI SETUP (Free Google AI Studio) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("⚠️ AI Key missing! Streamlit Secrets mein add karein.")

# --- Custom CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #1d3557; color: white; border-radius: 8px; font-weight: bold; height: 3em; }
    .checklist-box { background-color: #f1f4f9; padding: 20px; border-radius: 10px; border-left: 10px solid #1d3557; margin-bottom: 10px; }
    .ai-box { background-color: #e8f0fe; padding: 15px; border-radius: 10px; border: 1px dashed #4285f4; }
    </style>
    """, unsafe_allow_html=True)

# Logo aur Title
st.title("🏗️ RM E&I Maintenance Log")
st.write(f"📅 {datetime.now().strftime('%d-%b-%Y')} | 🕒 {datetime.now().strftime('%I:%M %p')}")

# Google Script URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyZf9a8rIJSUJ0BCGIJLXO0bIiLvZCujELboKVt__GSn1crsYJuPbsy1MwDhOyIjdpKKg/exec"

assets_data = {
    "1. HMD": ["Clean lens/glass", "Check alignment", "Verify power LED status", "Air purging flow"],
    "2. Pyrometer": ["Check display reading", "Verify sighting window clean", "4-20mA output check"],
    "3. Loop Scanner": ["Verify loop height on HMI", "Check sensor status LEDs", "Clean sensor face"],
    "4. Mill Stand Motors": ["Monitor sound/vibration", "Check VFD fault logs", "Verify cooling airflow"],
    "14. Atlas Copco Compressors": ["Check oil/temp logs", "Check for abnormal alarms", "Take motor load"],
    "17. Transformers": ["Check Winding Temp", "Check Oil Temp", "Verify Terminals"]
} # (Baqi items aap yahan add kar sakte hain...)

# Form Section
with st.container():
    col_name, col_shift = st.columns(2)
    with col_name:
        inspector = st.text_input("👤 Inspector Name")
    with col_shift:
        shift = st.radio("🕒 Shift", ["Shift A", "Shift B"], horizontal=True)

    asset_choice = st.selectbox("🏗️ Select Equipment", list(assets_data.keys()))
    
    # Checklist
    st.markdown('<div class="checklist-box">🔍 <b>Maintenance Checklist:</b>', unsafe_allow_html=True)
    selected_checks = []
    for point in assets_data[asset_choice]:
        if st.checkbox(point):
            selected_checks.append(point)
    st.markdown('</div>', unsafe_allow_html=True)

    remarks = st.text_area("📝 Remarks / Issues Found")

    # --- 2. AI ASSISTANT SECTION ---
    if remarks:
        if st.button("🤖 Ask AI for Fix?"):
            with st.spinner('Gemini AI solution dhoond raha hai...'):
                prompt = f"I am a maintenance engineer at a steel mill. I found this issue: '{remarks}' in '{asset_choice}'. Give me 3 quick technical points to fix it in Urdu/Hindi (Roman)."
                try:
                    response = model.generate_content(prompt)
                    st.markdown(f'<div class="ai-box"><b>AI Suggestion:</b><br>{response.text}</div>', unsafe_allow_html=True)
                except:
                    st.error("AI not responding. Check API Key.")

    # Submit to Excel
    if st.button("🚀 SUBMIT TO EXCEL"):
        if inspector:
            payload = {
                "inspector": inspector, "shift": shift, "asset": asset_choice,
                "checks": ", ".join(selected_checks), "remarks": remarks
            }
            try:
                res = requests.post(SCRIPT_URL, json=payload, timeout=10)
                st.success("✅ Data saved in Excel!")
                st.balloons()
            except:
                st.error("Connection error!")
