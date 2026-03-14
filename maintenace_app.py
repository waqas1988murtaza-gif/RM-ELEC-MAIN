def save_to_google_sheet(data_dict):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Secrets ko dictionary mein badlein
        creds_dict = dict(st.secrets["gcp_service_account"])
        
        # Formatting ka masla hal karne ke liye
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open("Maintenance_Data_Logs").sheet1
        sheet.append_row(list(data_dict.values()))
        return True
    except Exception as e:
        return f"Error: {e}"
