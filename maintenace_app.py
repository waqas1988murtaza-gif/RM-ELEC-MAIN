import streamlit as st
import requests

st.set_page_config(page_title="RM E&I Automation", page_icon="🛠️")

# Title and Logo look (as per your request)
st.title("🛠️ RM E&I Maintenance Automation")

# --- APNA URL YAHAN PASTE KAREIN ---
 "https://script.google.com/macros/s/AKfycbzkhwqUc2fYB-9O1dV1LoB6kBAl8E-ZG_xffr5upYf8FKi9xvlt0vVXOa4K30sJMGK4mg/exec "
SCRIPT_URL = "PASTE_YOUR_COPIED_LINK_HERE"

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
    
    submit = st.form_submit_button("Submit")

    if submit:
        if inspector:
            # Data pack kar ke bhejna
            payload = {
                "inspector": inspector, 
                "asset": asset, 
                "remarks": remarks
            }
            
            try:
                # Script ko request bhejna
                response = requests.post(SCRIPT_URL, json=payload)
                
                if "Success" in response.text:
                    st.success(f"✅ Shukriya {inspector}! Data save ho gaya.")
                    st.balloons()
                else:
                    st.error("❌ Kuch galti hui: " + response.text)
            except Exception as e:
                st.error(f"❌ Connection Fail: {e}")
        else:
            st.warning("⚠️ Name likhna zaroori hai.")

st.markdown("---")
st.caption("RM Maintenance System")
