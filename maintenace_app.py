import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="RM E&I Automation", page_icon="🛠️")
st.title("🛠️ RM E&I Maintenance Automation")

# Connection banana
conn = st.connection("gsheets", type=GSheetsConnection)

# Data parhna (Read)
df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1MjbmnCfZYf7V1SWOxoryfIAy9pL_25IpanU0qTzRwCw/edit?usp=sharing")

# --- FORM INTERFACE ---
with st.form("maintenance_form"):
    inspector_name = st.text_input("Inspector Name")
    asset_list = ["1. HMD", "2. Loop Scanner", "3. Pyrometer"]
    selected_asset = st.selectbox("Select Asset", asset_list)
    remarks = st.text_area("Remarks")
    
    submit = st.form_submit_button("Submit")

    if submit:
        if inspector_name:
            # Naya data purane data mein add karna
            new_data = pd.DataFrame([{
                "Inspector Name": inspector_name,
                "Asset": selected_asset,
                "Remarks": remarks
            }])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            
            # Wapas Sheet mein likhna (Update)
            conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1MjbmnCfZYf7V1SWOxoryfIAy9pL_25IpanU0qTzRwCw/edit?usp=sharing", data=updated_df)
            st.success("Data Submitted!")
        else:
            st.error("Please enter Inspector Name")

st.dataframe(df)
