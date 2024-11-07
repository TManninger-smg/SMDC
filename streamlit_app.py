import streamlit as st
import pandas as pd

# Define data storage
investigations = []

# Investigation Data Entry Form
st.header("Investigation Data Entry")
name = st.text_input("Investigation Name")
investigators = st.text_area("Investigators (comma-separated)")
corresponding_author = st.text_input("Corresponding Author")
dataset_list = st.text_area("Datasets (comma-separated)")
materials = st.text_area("Materials or Composites (comma-separated)")
publications = st.text_area("Publications (comma-separated)")

if st.button("Add Investigation"):
    investigation = {
        "Name": name,
        "Investigators": investigators.split(","),
        "Corresponding_Author": corresponding_author,
        "Datasets": dataset_list.split(","),
        "Materials": materials.split(","),
        "Publications": publications.split(",")
    }
    investigations.append(investigation)
    st.success("Investigation added!")

# Display and Download Data
st.header("Current Investigations")
if investigations:
    df = pd.DataFrame(investigations)
    st.dataframe(df)
    
    # Provide option to download as CSV
    csv = df.to_csv(index=False)
    st.download_button("Download Investigations as CSV", data=csv, file_name="investigations.csv")
else:
    st.write("No investigations added yet.")
