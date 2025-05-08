import streamlit as st
from Forms.DatasetsInfo import DataSetForm  # Changed SMDC.Forms to Forms
from Forms.AuthorData import AuthorDataPage  # Changed SMDC.Forms to Forms
from Forms.utils import SetEncoder  # Changed SMDC.Forms to Forms
import json

AuthorDataPage()
DataSetForm()
#download button for json file
combined_data_for_json = {}
if 'author_data' in st.session_state:
    combined_data_for_json['Author_Info'] = st.session_state.author_data
if 'dataset_form_data' in st.session_state:
    combined_data_for_json['Datasets'] = st.session_state.dataset_form_data
# Add JSON download button if there's data to download
if combined_data_for_json:
    try:
        # Use the custom encoder
        json_string = json.dumps(combined_data_for_json, indent=2, cls=SetEncoder)
        st.download_button(
            label="Download All Data as JSON",
            data=json_string,
            file_name="form_data.json",
            mime="application/json",
        )
    except Exception as e:
        st.error(f"Error generating JSON: {e}")
else:
    st.info("Submit forms to enable JSON download.")

#add a button to clear the session state
if st.button("Clear Data"):
    st.session_state.clear()
    st.success("Data cleared from the memory.")