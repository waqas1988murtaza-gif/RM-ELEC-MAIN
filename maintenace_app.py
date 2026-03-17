import streamlit as st
import requests

st.set_page_config(page_title="RM E&I Automation", page_icon="🛠️")

st.title("🛠️ RM E&I Maintenance Automation")

# --- APNA URL YAHAN PASTE KAREIN ---
# Jo URL aapne Apps Script se copy kiya hai, usay niche wale quotes " " ke andar daalein
SCRIPT_URL = "https://script.google.com/macros/library/d/1rkg0F1-sn974tWCUfcE2AkfJcie4pHWK5v6VPRsf2NyLlm0cwTcP9DxQ/1"

with st.form("maintenance_form"):
    st.subheader("Inspection Details")
    
    inspector = st.text_input("Inspector Name")
    
    asset_list = [
        "1. HMD (Hot Metal Detector)",
        "2. Loop Scanner",
        "3. Pyrometer",
        "4. Solenoid Valve",
        "5. Limit Switch"
    ]
    asset = st.selectbox("Select Asset", asset_list)
    
    remarks = st.text_area("Remarks / Observations")
    
    submit = st.form_submit_button("Submit Data")

    if submit:
        if inspector:
            # Data taiyar karna
            payload = {
                "inspector": inspector, 
                "asset": asset, 
                "remarks": remarks
            }
            
            try:
                # Google Sheet ko data bhejna
                response = requests.post(SCRIPT_URL, json=payload)
                
                if response.text == "Success":
                    st.success(f"✅ Shukriya {inspector}! Data Sheet mein save ho gaya hai.")
                    st.balloons()
                else:
                    st.error("❌ Error: Sheet ne data qubool nahi kiya.")
            except Exception as e:
                st.error(f"❌ Connection Fail: {e}")
        else:
            st.warning("⚠️ Inspector Name likhna zaroori hai!")

st.markdown("---")
st.caption("RM Maintenance System - Powered by Streamlit")
