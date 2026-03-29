import streamlit as st
import requests
import json

# --- CONFIG ---
# Apna Google Script URL yahan lazmi dalein
SCRIPT_URL = "https://script.google.com/macros/s/XXXXX/exec" 

st.set_page_config(page_title="Naveena Maintenance", page_icon="⚙️")

# Logo Load karein (Aapki repo se)
st.image("https://raw.githubusercontent.com/waqas1988murtaza/Naveena-Steel/main/download.png", width=150)
st.title("RM E&I Maintenance Log")

# 1. Google Sheet se Dynamic List mangwana
@st.cache_data(ttl=10)
def get_dynamic_assets():
    try:
        # Hum Google Script ko 'getSettings' action bhejenge
        resp = requests.get(f"{SCRIPT_URL}?action=getSettings")
        return resp.json()
    except:
        # Agar error aaye to ye default list dikhaye ga
        return {"1. HMD": ["Model-500", "Model-600"], "2. Loop Scanner": ["Standard"]}

assets = get_dynamic_assets()

# --- ADMIN: FRONT-END SE UPGRADE KAREIN ---
with st.expander("🛠️ Admin: Add New Equipment/Models"):
    st.write("Yahan se aap nayi categories ya HMD ke naye models add kar sakte hain.")
    
    col1, col2 = st.columns(2)
    with col1:
        new_cat = st.text_input("New Category Name")
        if st.button("Add Category"):
            requests.post(SCRIPT_URL, json={"type": "ADD_SETTING", "category": new_cat, "item": "Default"})
            st.cache_data.clear()
            st.rerun()
            
    with col2:
        target_cat = st.selectbox("Select Parent", list(assets.keys()))
        new_model = st.text_input(f"New Model for {target_cat}")
        if st.button("Add Model/Item"):
            requests.post(SCRIPT_URL, json={"type": "ADD_SETTING", "category": target_cat, "item": new_model})
            st.cache_data.clear()
            st.rerun()

st.divider()

# --- MAIN LOGGING FORM ---
name = st.text_input("Inspector Name", placeholder="Enter your name")
shift = st.radio("Shift", ["Shift A", "Shift B"], horizontal=True)

# Parent Selection (HMD, Loop Scanner etc.)
parent_selection = st.selectbox("Select Equipment Group", list(assets.keys()))

# Child Selection (HMD ke andar models - AUTOMATIC UPDATE)
child_options = assets.get(parent_selection, [])
child_selection = st.selectbox(f"Select Specific {parent_selection}", child_options)

# Checklist (Dynamic Checklist bhi bana saktay hain)
st.info("📝 Maintenance Checklist:")
c1 = st.checkbox("Clean lens/glass")
c2 = st.checkbox("Check alignment")
c3 = st.checkbox("Verify power LED status")

remarks = st.text_area("Remarks / Issues Found", value="Ok")

if st.button("🚀 SUBMIT TO EXCEL"):
    payload = {
        "type": "LOG_ENTRY",
        "inspector": name,
        "shift": shift,
        "parent": parent_selection,
        "child": child_selection,
        "remarks": remarks
    }
    
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        if "Success" in response.text:
            st.success(f"✅ Data for {child_selection} saved successfully!")
        else:
            st.error("❌ Connection error! Google Script check karein.")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
