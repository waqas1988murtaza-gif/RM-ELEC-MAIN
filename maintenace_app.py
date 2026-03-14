import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# --- Google Sheets Setup ---
def save_to_google_sheet(data_dict):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Secrets se credentials uthana
        creds_info = st.secrets.get("gcp_service_account", st.secrets)
        creds_dict = dict(creds_info)
        
        # Private key formatting fix
        if "private_key" in creds_dict:
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # Sheet open karein
        sheet = client.open("Maintenance_Data_Logs").sheet1
        sheet.append_row(list(data_dict.values()))
        return True
    except Exception as e:
        return f"Error: {e}"

# --- UI Design ---
st.set_page_config(page_title="RM Maintenance", layout="wide")
st.title("🛠️ RM E&I Maintenance Automation")

maintenance_db = {
    "1. HMD (Hot Metal Detector)": ["Clean lens/glass", "Check alignment", "Verify power LED", "Inspect mounting brackets"],
    "4. Mill Stand Motors": ["Monitor sound/vibration", "Check VFD logs", "Clean cooling fans/filters"],
    "5. Shear Motors": ["Check brake operation", "Verify encoder feedback", "Inspect power cables"],
    "14. Atlas Copco Compressors": ["Check oil/temp logs", "Clean air intake filters"],
    "17. Transformers": ["Winding/Oil Temp check", "Silica Gel color", "Oil level"]
}

c1, c2, c3 = st.columns(3)
with c1:
    date_val = st.date_input("Date", datetime.now())
with c2:
    shift = st.selectbox("Shift", ["Shift A (12H)", "Shift B (12H)"])
with c3:
    user = st.text_input("Inspector Name")

category = st.selectbox("Select Asset Category", list(maintenance_db.keys()))
st.divider()

st.subheader(f"✅ Checklist: {category}")
tasks = maintenance_db.get(category, [])
check_status = {}

col_a, col_b = st.columns(2)
for i, t in enumerate(tasks):
    target_col = col_a if i % 2 == 0 else col_b
    check_status[t] = target_col.checkbox(t, key=f"{category}_{t}")

remarks = st.text_area("Observations / Remarks")

if st.button("Submit Maintenance Record"):
    if not user:
        st.error("Please enter Inspector Name!")
    else:
        results = [f"{t}: {'OK' if v else 'Pending'}" for t, v in check_status.items()]
        entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Date": str(date_val),
            "Shift": shift,
            "Category": category,
            "User": user,
            "Status": " | ".join(results),
            "Remarks": remarks
        }

        with st.spinner('Saving to Google Sheet...'):
            res = save_to_google_sheet(entry)
            if res == True:
                st.success("Success! Data saved to Google Sheet.")
                st.balloons()
            else:
                st.error(f"Failed to connect: {res}")
                # Fallback backup
                pd.DataFrame([entry]).to_csv("backup.csv", mode='a', index=False, header=not os.path.exists("backup.csv"))
