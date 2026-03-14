import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets Setup ---
def save_to_google_sheet(data_dict):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Secrets se data lena
        def save_to_google_sheet(data_dict):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Secrets se poori dictionary uthayen
        # Agar section name 'gcp_service_account' hai to wo uthayen, warna poora secrets
        creds_info = st.secrets.get("gcp_service_account", st.secrets)
        creds_dict = dict(creds_info)
        
        # Key ke formatting ka masla hal karein
        if "private_key" in creds_dict:
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open("Maintenance_Data_Logs").sheet1
        sheet.append_row(list(data_dict.values()))
        return True
    except Exception as e:
        return f"Error: {e}"
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # Sheet ka naam check karein
        sheet = client.open("Maintenance_Data_Logs").sheet1
        sheet.append_row(list(data_dict.values()))
        return True
    except Exception as e:
        return f"Error: {e}"

# --- Interface ---
st.title("🛠️ RM E&I Maintenance Automation")

maintenance_db = {
    "1. HMD (Hot Metal Detector)": ["Clean lens/glass", "Check alignment", "Verify power LED"],
    "4. Mill Stand Motors": ["Monitor sound/vibration", "Check VFD logs"],
    "17. Transformers": ["Winding/Oil Temp check", "Silica Gel color"]
}

user = st.text_input("Inspector Name")
category = st.selectbox("Select Asset", list(maintenance_db.keys()))

if st.button("Submit"):
    if user:
        entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Category": category,
            "User": user
        }
        res = save_to_google_sheet(entry)
        if res == True:
            st.success("Success! Data saved.")
            st.balloons()
        else:
            st.error(res)
    else:
        st.warning("Name likhen!")
