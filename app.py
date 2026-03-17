import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.title("Maintenance Checklist")

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)
    sheet = client.open("Maintenance").sheet1

    st.success("Connected to Google Sheet ✅")

except Exception as e:
    st.error("Google Sheet connection failed ❌")
    st.stop()

st.header("Checklist: HMD (Hot Metal Detector)")

clean_lens = st.checkbox("Clean lens/glass")
power_led = st.checkbox("Verify power LED")
alignment = st.checkbox("Check alignment")
mounting = st.checkbox("Inspect mounting brackets")

remarks = st.text_area("Observations / Remarks")

if st.button("Submit Maintenance Record"):

    data = [
        str(datetime.now()),
        "HMD",
        clean_lens,
        power_led,
        alignment,
        mounting,
        remarks
    ]

    sheet.append_row(data)

    st.success("Record submitted successfully ✅")
