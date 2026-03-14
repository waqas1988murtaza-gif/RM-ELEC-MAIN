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
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        
        # Check karein ke Sheet ka naam exact yahi ho
        sheet = client.open("Maintenance_Data_Logs").sheet1
        sheet.append_row(list(data_dict.values()))
        return True
    except Exception as e:
        # Sidebar mein error dikhayega agar sheet connect na hui
        st.sidebar.error(f"Google Sheet Error: {e}")
        return False

# --- Page Setup ---
st.set_page_config(page_title="RM Maintenance", layout="wide")
st.title("🛠️ RM E&I Maintenance Automation")

# --- DATABASE (Ismein aap apni marzi se mazeed points add kar sakte hain) ---
maintenance_db = {
    "1. HMD (Hot Metal Detector)": ["Clean lens/glass", "Check alignment", "Verify power LED", "Inspect mounting brackets"],
    "4. Mill Stand Motors": ["Monitor sound/vibration", "Check VFD logs", "Clean cooling fans/filters", "Check cable terminals"],
    "5. Shear Motors": ["Check brake operation", "Verify encoder feedback", "Inspect power cables"],
    "14. Atlas Copco Compressors": ["Check oil/temp logs", "Clean air intake filters"],
    "17. Transformers": ["Winding/Oil Temp check", "Silica Gel color", "Oil level"],
    # Yahan baqi 19 categories isi tarah add kar lein
}

# --- FORM ---
# Form ke bahar Selectbox rakhne se UI foran update hota hai
c1, c2, c3 = st.columns(3)
with c1:
    date_val = st.date_input("Date", datetime.now())
with c2:
    # Shift sirf A aur B
    shift = st.selectbox("Shift (12 Hours)", ["Shift A", "Shift B"])
with c3:
    user = st.text_input("Inspector Name / ID")

category = st.selectbox("Select Asset Category", list(maintenance_db.keys()))

st.divider()

# Checklist wala hissa
st.subheader(f"✅ Checklist: {category}")
tasks = maintenance_db.get(category, [])
check_status = {}

# Column wise checkboxes taake jagah kam gheray
col_a, col_b = st.columns(2)
for i, t in enumerate(tasks):
    target_col = col_a if i % 2 == 0 else col_b
    # Unique key dena zaroori hai (category + task)
    check_status[t] = target_col.checkbox(t, key=f"{category}_{t}")

remarks = st.text_area("Observations / Remarks")

if st.button("Submit Maintenance Record"):
    if not user:
        st.error("Bhai, Inspector Name likhna zaroori hai!")
    else:
        # Data tayyar karna
        task_results = [f"{t}: {'OK' if val else 'Pending'}" for t, val in check_status.items()]
        
        entry_data = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Date": str(date_val),
            "Shift": shift,
            "Category": category,
            "User": user,
            "Status": " | ".join(task_results),
            "Remarks": remarks
        }

        # Google Sheet mein save karna
        if save_to_google_sheet(entry_data):
            st.success(f"Mubarak ho! {category} ka data Google Sheet mein save ho gaya.")
            st.balloons()
        else:
            # Agar sheet connect na ho to computer mein save kar lo
            pd.DataFrame([entry_data]).to_csv("local_backup.csv", mode='a', index=False, header=not os.path.exists("local_backup.csv"))
            st.warning("⚠️ Google Sheet se connect nahi ho saka. Data computer mein (local_backup.csv) save kar diya hai.")