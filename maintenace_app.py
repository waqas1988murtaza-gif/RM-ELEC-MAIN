import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Maintenance Checklist", layout="wide")
st.title("🛠️ Maintenance Checklist")

# Aapka Google Sheet Link
sheet_url = "https://docs.google.com/spreadsheets/d/1MjbmnCfZYf7V1SWOxoryfIAy9pL_25IpanU0qTzRwCw/edit?usp=drivesdk"

def get_csv_url(url):
    try:
        # Link ko CSV format mein convert karne ke liye
        if "/edit" in url:
            return url.split("/edit")[0] + "/export?format=csv"
        return url
    except:
        return url

try:
    csv_url = get_csv_url(sheet_url)
    df = pd.read_csv(csv_url)
    
    st.success("✅ Google Sheet connected successfully!")
    
    # Data table show karne ke liye
    st.write("### Current Records")
    st.dataframe(df, use_container_width=True)
    
except Exception as e:
    st.error("❌ Connection Failed")
    st.info("Make sure your Google Sheet is shared as 'Anyone with the link' (Viewer)")
    st.write(f"Debug Info: {e}")
