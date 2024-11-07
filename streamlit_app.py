import streamlit as st
import pandas as pd

# Initialize data storage for each entity
investigations = []
materials = []
samples = []
experiments = []
datafiles = []

st.title("Research Data Entry Application")

### Investigation Data Entry ###
st.header("Investigation Data Entry")
name = st.text_input("Investigation Name")
investigators = st.text_area("Investigators (comma-separated)")
corresponding_author = st.text_input("Corresponding Author")
dataset_list = st.text_area("Datasets (comma-separated)")
materials_list = st.text_area("Materials or Composites (comma-separated)")
publications = st.text_area("Publications (comma-separated)")

if st.button("Add Investigation"):
    investigation = {
        "Name": name,
        "Investigators": investigators.split(","),
        "Corresponding_Author": corresponding_author,
        "Datasets": dataset_list.split(","),
        "Materials": materials_list.split(","),
        "Publications": publications.split(",")
    }
    investigations.append(investigation)
    st.success("Investigation added!")

### Material Data Entry ###
st.header("Material Data Entry")
material_name = st.text_input("Material Name")
material_type = st.selectbox("Material Type", ["Composite", "Single Material"])
material_samples = st.text_area("Samples (comma-separated)")
material_parameters = st.text_area("Parameters (comma-separated)")

if st.button("Add Material"):
    material = {
        "Name": material_name,
        "Type": material_type,
        "Samples": material_samples.split(","),
        "Parameters": material_parameters.split(",")
    }
    materials.append(material)
    st.success("Material added!")

### Sample Data Entry ###
st.header("Sample Data Entry")
sample_name = st.text_input("Sample Name")
sample_geometry = st.text_input("Geometry")
sample_date = st.date_input("Sample Date")
sample_parameters = st.text_area("Sample Parameters (comma-separated)")
sample_experiments = st.text_area("Experiments (comma-separated)")
from_sample = st.text_input("Derived from Sample")
preparation_protocol = st.text_area("Preparation Protocol")

if st.button("Add Sample"):
    sample = {
        "Name": sample_name,
        "Geometry": sample_geometry,
        "Date": sample_date,
        "Parameters": sample_parameters.split(","),
        "Experiments": sample_experiments.split(","),
        "From Sample": from_sample,
        "Preparation Protocol": preparation_protocol
    }
    samples.append(sample)
    st.success("Sample added!")

### Experiment Data Entry ###
st.header("Experiment Data Entry")
experiment_name = st.text_input("Experiment Name")
experiment_type = st.text_input("Experiment Technique")
experiment_parameters = st.text_area("Experimental Parameters (comma-separated)")

if st.button("Add Experiment"):
    experiment = {
        "Name": experiment_name,
        "Technique": experiment_type,
        "Parameters": experiment_parameters.split(",")
    }
    experiments.append(experiment)
    st.success("Experiment added!")

### Datafile Data Entry ###
st.header("Datafile Data Entry")
datafile_name = st.text_input("Datafile Name")
storage_type = st.selectbox("Storage Type", ["Local", "Remote"])
storage_value = st.text_input("Storage Location/Value")
storage_format = st.text_input("Format Type")
storage_parameters = st.text_area("Storage Parameters (comma-separated)")

if st.button("Add Datafile"):
    datafile = {
        "Name": datafile_name,
        "Storage Type": storage_type,
        "Storage Value": storage_value,
        "Format Type": storage_format,
        "Parameters": storage_parameters.split(",")
    }
    datafiles.append(datafile)
    st.success("Datafile added!")

### Display and Download Section ###
st.header("Data Overview and Export")

# Function to download CSV
def download_csv(data, filename):
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    st.download_button(f"Download {filename}", data=csv, file_name=f"{filename}.csv")

# Display and download options for each entity
if investigations:
    st.subheader("Investigations")
    st.dataframe(pd.DataFrame(investigations))
    download_csv(investigations, "investigations.csv")

if materials:
    st.subheader("Materials")
    st.dataframe(pd.DataFrame(materials))
    download_csv(materials, "materials.csv")

if samples:
    st.subheader("Samples")
    st.dataframe(pd.DataFrame(samples))
    download_csv(samples, "samples.csv")

if experiments:
    st.subheader("Experiments")
    st.dataframe(pd.DataFrame(experiments))
    download_csv(experiments, "experiments.csv")

if datafiles:
    st.subheader("Datafiles")
    st.dataframe(pd.DataFrame(datafiles))
    download_csv(datafiles, "datafiles.csv")
