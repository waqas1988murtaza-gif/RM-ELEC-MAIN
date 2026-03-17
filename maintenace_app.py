import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- PAGE SETUP ---
st.set_page_config(page_title="RM E&I Automation", page_icon="🛠️")

# --- GOOGLE SHEETS CONNECTION ---
# Yahan hum aapke Secrets se data uthayenge
try:
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    
    # Sheet open karein (Aapki sheet ka naam 'Sheet1' hona chahiye)
    sheet = client.open_by_key("1MjbmnCfZYf7V1SWOxoryfIAy9pL_25IpanU0qTzRwCw").sheet1
    st.success("✅ Connected to Google Sheets")
except Exception as e:
    st.error("❌ Connection Error: Make sure Secrets are set correctly.")
    st.stop()

# --- APP INTERFACE (WAISA HI LOOK) ---
st.title("🛠️ RM E&I Maintenance Automation")

with st.form("maintenance_form"):
    inspector_name = st.text_input("Inspector Name")
    
    asset_list = [
        "1. HMD (Hot Metal Detector)",
        "2. Loop Scanner",
        "3. Pyrometer",
        "4. Solenoid Valve",
        "5. Limit Switch"
    ]
    selected_asset = st.selectbox("Select Asset", asset_list)
    
    # Aap mazeed fields yahan add kar sakte hain
    remarks = st.text_area("Remarks (Optional)")
    
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        if inspector_name:
            # Data ko sheet mein bhejna
            new_row = [inspector_name, selected_asset, remarks]
            sheet.append_row(new_row)
            st.balloons()
            st.success(f"Data for {selected_asset} submitted successfully!")
        else:
            st.warning("Bhai, Inspector Name to likho!")

# --- VIEW DATA ---
if st.checkbox("Show Recent Entries"):
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    st.dataframe(df)
