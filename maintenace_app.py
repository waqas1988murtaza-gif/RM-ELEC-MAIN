import streamlit as st
import requests

st.set_page_config(page_title="RM E&I Automation", page_icon="🛠️")
st.title("🛠️ RM E&I Maintenance Automation")

# --- Yahan apna Web App URL paste karein ---
SCRIPT_URL = "APNA_WEB_APP_URL_YAHAN_PASTE_KAREIN"

with st.form("maintenance_form"):
    inspector = st.text_input("Inspector Name")
    asset = st.selectbox("Select Asset", ["HMD", "Loop Scanner", "Pyrometer"])
    remarks = st.text_area("Remarks")
    submit = st.form_submit_button("Submit")

    if submit:
        if inspector:
            # Data bhejna
            payload = {"inspector": inspector, "asset": asset, "remarks": remarks}
            response = requests.post(SCRIPT_URL, json=payload)
            
            if response.text == "Success":
                st.success("✅ Data Sheet mein chala gaya!")
                st.balloons()
            else:
                st.error("❌ Kuch galti hui hai.")
        else:
            st.warning("Please enter Inspector Name")
