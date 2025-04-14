import streamlit as st
import json
import os

def load_data(file_path="data.json"):
    """Load existing data from JSON file, or return an empty list if it doesn't exist or isn't a list."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    # If it's not a list, return empty list to avoid append errors
                    return []
            except json.JSONDecodeError:
                # If it's invalid JSON, return empty list
                return []
    else:
        return []

def save_data(data, file_path="data.json"):
    """Save the given data (which should be a list) to a JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def main():
    st.title("Streamlit Form to JSON (Append, Download & Reset)")

    # Use session state to hold form inputs so we can clear them after submission
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "age" not in st.session_state:
        st.session_state.age = 0
    if "city" not in st.session_state:
        st.session_state.city = ""

    # --- Form to add entries ---
    with st.form("my_form"):
        st.session_state.name = st.text_input("Name", value=st.session_state.name)
        st.session_state.age = st.number_input("Age", min_value=0, value=st.session_state.age)
        st.session_state.city = st.text_input("City", value=st.session_state.city)

        submitted = st.form_submit_button("Submit")
        if submitted:
            data = load_data()  # load existing entries
            new_entry = {
                "name": st.session_state.name,
                "age": st.session_state.age,
                "city": st.session_state.city
            }
            data.append(new_entry)
            save_data(data)

            # Reset form fields
            st.session_state.name = ""
            st.session_state.age = 0
            st.session_state.city = ""

            st.success("Entry added to data.json")

    # --- Print All JSON Entries ---
    if st.button("Print All JSON Entries"):
        data = load_data()
        if data:
            st.json(data)
        else:
            st.warning("No entries found. Please submit the form first.")

    st.write("---")

    # --- Download & Reset Data ---
    data = load_data()
    if data:
        # Convert data to JSON string for download
        data_json = json.dumps(data, indent=4)

        # Streamlit's download_button returns True when clicked
        download_clicked = st.download_button(
            label="Download & Reset All Entries",
            data=data_json,
            file_name="data.json",
            mime="application/json"
        )
        
        # Once downloaded, reset the file
        if download_clicked:
            save_data([])  # Reset file to an empty list
            st.success("All entries have been downloaded and reset.")
    else:
        st.info("No data available to download. Please add entries first.")

if __name__ == "__main__":
    main()
