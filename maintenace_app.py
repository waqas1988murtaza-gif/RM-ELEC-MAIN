import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Maintenance Checklist", layout="wide")
st.title("🛠️ Maintenance Checklist")

# --- YAHAN APNA COPY KIYA HUA LINK PASTE KAREIN ---
sheet_url = "APNA_SHEET_LINK_YAHAN_PASTE_KAREIN"

def get_csv_url(url):
    try:
        if "/edit" in url:
            return url.split("/edit")[0] + "/export?format=csv"
        return url
    except:
        return url

try:
    csv_url = get_csv_url(sheet_url)
    df = pd.read_csv(csv_url)
    
    st.success("✅ Google Sheet connected successfully!")
    
    # Data dikhanay ke liye
    st.write("### Current Records")
    st.dataframe(df, use_container_width=True)
    
except Exception as e:
    st.error("❌ Connection Failed")
    st.info("Check if your Google Sheet is shared as 'Anyone with the link'")
