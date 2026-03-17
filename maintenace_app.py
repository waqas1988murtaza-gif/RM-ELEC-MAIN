import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="RM Maintenance System", page_icon="🛠️", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .status-card { padding: 20px; border-radius: 10px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ RM Maintenance Dashboard")

# Sheet Link
sheet_url = "https://docs.google.com/spreadsheets/d/1MjbmnCfZYf7V1SWOxoryfIAy9pL_25IpanU0qTzRwCw/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
    
    # --- Top Stats Row ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tasks", len(df))
    with col2:
        pending = len(df[df['Status'].str.contains('Pending', case=False, na=False)])
        st.metric("Pending", pending, delta_color="inverse")
    with col3:
        completed = len(df[df['Status'].str.contains('Completed|Done', case=False, na=False)])
        st.metric("Completed", completed)
    with col4:
        st.write("**Quick Actions**")
        st.link_button("➕ Add New Entry", "https://docs.google.com/spreadsheets/d/1MjbmnCfZYf7V1SWOxoryfIAy9pL_25IpanU0qTzRwCw/edit")

    st.divider()

    # --- Main Interface ---
    tab1, tab2 = st.tabs(["📋 View Checklist", "🔍 Search & Filter"])

    with tab1:
        st.subheader("Current Maintenance Schedule")
        # Displaying with better colors
        def color_status(val):
            color = '#e1f5fe' if val == 'Pending' else '#e8f5e9'
            return f'background-color: {color}'
        
        st.dataframe(df.style.applymap(color_status, subset=['Status']), use_container_width=True)

    with tab2:
        search_query = st.text_input("Enter Equipment Name or Location")
        if search_query:
            filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
            st.write(filtered_df)

except Exception as e:
    st.error("Data Load Error. Please check your Google Sheet.")
