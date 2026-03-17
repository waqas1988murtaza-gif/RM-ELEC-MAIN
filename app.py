import streamlit as st
import pandas as pd

st.set_page_config(page_title="Maintenance App", layout="wide")
st.title("📋 RM Maintenance Checklist")

# Aapka Sheet Link (Maine fix kar diya hai)
sheet_url = "https://docs.google.com/spreadsheets/d/1MjbmnCfZYf7V1SWOxoryfIAy9pL_25IpanU0qTzRwCw/edit?usp=drivesdk"

def load_data(url):
    csv_url = url.split("/edit")[0] + "/export?format=csv"
    return pd.read_csv(csv_url)

try:
    df = load_data(sheet_url)
    
    if df.empty:
        st.warning("⚠️ Sheet khali hai! Please Row 1 mein headings likhein.")
    else:
        st.success("✅ Data Loaded Successfully!")
        # Search Bar
        search = st.text_input("🔍 Search here...", "")
        if search:
            df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error("❌ Error: Sheet mein data nahi mila.")
    st.info("💡 Solution: Google Sheet mein kam az kam Row 1 mein headings (ID, Date, Task) likhein.")
