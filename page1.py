from dataclasses import dataclass, asdict
from pydantic import BaseModel, EmailStr, constr
from typing import Optional , Set
import streamlit_pydantic  as sp
import streamlit as st
import pydantic
from enum import Enum
import json # Add this import
import pandas as pd # Add pandas import

# Custom JSON encoder to handle sets
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

# Check pydantic version
class MainForm(BaseModel):
    title: str
    keywords: str
    description: str
    uploader: str
    email: str
    date: str
    identifier: str
    contributors: str = ""

data =sp.pydantic_form(key = "Main",model =MainForm)

class Datatype(str,Enum):
    text = "text"
    image = "image"
    audio = "audio"
    video = "video"

# Function to create Enum from Excel
def create_material_enum_from_excel(excel_path: str, column_name: str) -> type:
    try:
        df = pd.read_csv(excel_path)
        material_names = df[column_name].dropna().unique()
        enum_members = {str(name).replace(" ", "_").lower(): str(name) for name in material_names if str(name)}
        return Enum('MaterialType', enum_members) if enum_members else Enum('MaterialType', {'default': 'default'})
    except Exception as e:
        st.error(f"Error processing file '{excel_path}': {e}. Using default MaterialType.")
        return Enum('MaterialType', {'default': 'default'})

MaterialType = create_material_enum_from_excel("Materials.csv", "Material")
ExperimentType = create_material_enum_from_excel("Experiments.csv", "Experiment_Type")

class DataSet1(BaseModel):
    pick_dataset_type: Datatype
    extension_of_the_file: str 
    time_series:  bool
    number_of_files: int
    description: str
    Materials: MaterialType
    Experiments: Set[ExperimentType]
if 'dataset_form_data' not in st.session_state:
    st.session_state.dataset_form_data = []
dataset =sp.pydantic_form(key = "Dataset",model =DataSet1)

# Store submitted data in session state
if data:
    st.session_state.main_form_data = data.model_dump()

if dataset:
    st.session_state.dataset_form_data.append(dataset.model_dump())

# Display stored data (optional, for verification)
if 'main_form_data' in st.session_state:
    st.subheader("Stored Main Form Data:")
    st.json(st.session_state.main_form_data)

if 'dataset_form_data' in st.session_state:
    st.subheader("Stored Dataset Form Data:")
    for idx, dataset in enumerate(st.session_state.dataset_form_data):
        st.json({f"Dataset {idx + 1}": dataset})

# Prepare combined data for JSON download
combined_data_for_json = {}
if 'main_form_data' in st.session_state:
    combined_data_for_json['main_form'] = st.session_state.main_form_data
if 'dataset_form_data' in st.session_state:
    combined_data_for_json['dataset_form'] = st.session_state.dataset_form_data

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


