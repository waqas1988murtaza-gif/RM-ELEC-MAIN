import streamlit as st
import requests

st.set_page_config(page_title="RM E&I Automation", page_icon="🛠️")
st.title("🛠️ RM E&I Maintenance Automation")

# Naya URL yahan paste karein
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzkhwqUc2fYB-9O1dV1LoB6kBAl8E-ZG_xffr5upYf8FKi9xvlt0vVXOa4K30sJMGK4mg/exec"

with st.form("maintenance_form", clear_on_submit=True):
    st.subheader("Inspection Details")
    inspector = st.text_input("Inspector Name")
    asset = st.selectbox("Select Asset", ["HMD", "Loop Scanner", "Pyrometer", "Solenoid Valve", "Limit Switch"])
    remarks = st.text_area("Remarks")
    submit = st.form_submit_button("Submit Data")

    if submit:
        if inspector:
            payload = {"inspector": inspector, "asset": asset, "remarks": remarks}
            try:
                # Timeout add kiya hai taake app hang na ho
                response = requests.post(SCRIPT_URL, json=payload, timeout=10)
                if "Success" in response.text:
                    st.success(f"✅ Shukriya {inspector}! Data save ho gaya.")
                    st.balloons()
                else:
                    st.error(f"❌ Server Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Connection Fail: {e}")
        else:
            st.warning("⚠️ Name likhna zaroori hai.")
