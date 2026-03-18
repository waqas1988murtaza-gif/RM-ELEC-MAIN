import streamlit as st
import requests

st.set_page_config(page_title="RM E&I Automation", page_icon="⚙️")

# Custom Styling
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #007bff; color: white; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚙️ RM E&I Log System")
st.write("Enter maintenance details below:")

# --- NAYA URL YAHAN DAALEIN ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwyObsneunsz5XCcdQBxXGP3dN585OHApUCH4ylrOLgFE86FUvG01jXWtC57QI8KKbIjw/exec"

with st.container():
    name = st.text_input("👤 Inspector Name")
    asset = st.selectbox("🏗️ Select Asset", ["HMD", "Loop Scanner", "Pyrometer", "Solenoid Valve", "Limit Switch"])
    obs = st.text_area("📝 Remarks")

    if st.button("🚀 Submit Data"):
        if name:
            with st.spinner("Processing..."):
                payload = {"inspector": name, "asset": asset, "remarks": obs}
                try:
                    res = requests.post(SCRIPT_URL, json=payload, timeout=10)
                    if "Success" in res.text:
                        st.success(f"✅ Saved: {name}")
                        st.balloons()
                    else:
                        st.error("Server Issue!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter name.")
