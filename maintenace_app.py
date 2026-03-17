import streamlit as st
import pandas as pd

st.set_page_config(page_title="Maintenance App", layout="wide")
st.title("🛠️ RM Maintenance System")

# Sheet Link
sheet_url = "https://docs.google.com/spreadsheets/d/1MjbmnCfZYf7V1SWOxoryfIAy9pL_25IpanU0qTzRwCw/export?format=csv"

try:
    # Data Load karna
    df = pd.read_csv(sheet_url)
    st.success("✅ Connection Active")
    
    # Search filter
    search = st.text_input("🔍 Search Equipment")
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("⚠️ Data Nahi Mila")
    st.info("Bhai, pehle Google Sheet mein ja kar pehli row mein 'Date, Equipment, Task, Status' likh dein.")

# Data Entry Form (Sirf dekhne ke liye, link open karne ka button)
st.sidebar.header("Add New Entry")
st.sidebar.write("Naya data daalne ke liye niche button dabayein:")
st.sidebar.link_button("Open Google Sheet", "https://docs.google.com/spreadsheets/d/1MjbmnCfZYf7V1SWOxoryfIAy9pL_25IpanU0qTzRwCw/edit")
