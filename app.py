import streamlit as st
import pandas as pd

st.set_page_config(page_title="Maintenance System", page_icon="🛠️", layout="wide")
st.title("🛠️ Maintenance Management System")

# Aapki Sheet ka link (Jo maine check kiya hai)
sheet_url = "https://docs.google.com/spreadsheets/d/1MjbmnCfZYf7V1SWOxoryfIAy9pL_25IpanU0qTzRwCw/edit?usp=sharing"

def get_csv_url(url):
    return url.split("/edit")[0] + "/export?format=csv"

try:
    csv_url = get_csv_url(sheet_url)
    df = pd.read_csv(csv_url)
    
    if df.empty:
        st.info("📢 Sheet khali hai! Please Sheet mein data enter karein.")
    else:
        st.success(f"✅ Data loaded! Total Records: {len(df)}")
        st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error("❌ Connection Error")
    st.write("Please make sure your Google Sheet has at least one row of data and is shared as 'Anyone with the link'.")
