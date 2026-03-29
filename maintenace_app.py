import streamlit as st
import requests

# --- CONFIG ---
# Apna Naya Google Script URL yahan paste karein
SCRIPT_URL = "APNA_NEW_DEPLOYMENT_URL_YAHAN_DAALEIN"
ADMIN_PASSWORD = "NAVEENA_ADMIN" 

st.image("https://raw.githubusercontent.com/waqas1988murtaza/Naveena-Steel/main/download.png", width=150)
st.title("RM E&I Maintenance & Dynamic Log")

# 1. Google Sheet se Dynamic Data Load karna
@st.cache_data(ttl=10)
def get_assets():
    try:
        resp = requests.get(f"{SCRIPT_URL}?action=getSettings", timeout=10)
        return resp.json()
    except:
        # Default data agar connection fail ho jaye
        return {"HMD": ["HMD-1", "HMD-2"], "Loop Scanner": ["LS-1"]}

asset_dict = get_assets()

# --- ADMIN SECTION (Password Protected) ---
with st.expander("⚙️ Admin: Manage Categories & Sub-Items"):
    pwd = st.text_input("Enter Admin Password", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.success("Admin Access Granted!")
        tab1, tab2 = st.tabs(["Add New Category", "Add Sub-Items"])
        
        with tab1:
            new_cat = st.text_input("New Main Category (e.g., Motors)")
            if st.button("Create Category"):
                requests.post(SCRIPT_URL, json={"type": "ADD_SETTING", "category": new_cat, "item": "Default"})
                st.cache_data.clear()
                st.rerun()
        
        with tab2:
            target_cat = st.selectbox("Select Parent Category", list(asset_dict.keys()))
            st.write(f"Add items for {target_cat} (e.g., {target_cat}-1, {target_cat}-2...)")
            new_item = st.text_input(f"New Sub-Item Name")
            if st.button(f"Add to {target_cat}"):
                requests.post(SCRIPT_URL, json={"type": "ADD_SETTING", "category": target_cat, "item": new_item})
                st.cache_data.clear()
                st.rerun()
    elif pwd != "":
        st.error("Incorrect Password!")

st.divider()

# --- MAIN LOGGING FORM ---
name = st.text_input("Inspector Name")
shift = st.radio("Shift", ["Shift A", "Shift B"], horizontal=True)

# 1. Main Category Select karein (e.g., HMD)
parent_selection = st.selectbox("Select Equipment Group (Parent)", list(asset_dict.keys()))

# 2. Sub-Category Select karein (e.g., HMD-1, HMD-2...)
# Ye list 'parent_selection' ke mutabiq khud update hogi
child_options = asset_dict.get(parent_selection, [])
child_selection = st.selectbox(f"Select Specific {parent_selection} Unit", child_options if child_options else ["No items found"])

st.info(f"📝 Checklist for {child_selection}:")
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
        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
        if "Success" in response.text:
            st.success(f"✅ {child_selection} ka data save ho gaya!")
        else:
            st.error("❌ Google Script Error!")
    except Exception as e:
        st.error("⚠️ Connection Error! Script URL ya Internet check karein.")
