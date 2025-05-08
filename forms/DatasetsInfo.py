from pydantic import BaseModel
import streamlit_pydantic as sp
import streamlit as st
from .utils import create_material_enum_from_excel   
from enum import Enum
from typing import Set
import os

class Datatype(str,Enum):
    text = "text"
    image = "image"
    audio = "audio"
    video = "video"
# get the absolute path of the current file
current_file_path = os.path.abspath(__file__)
materials_path = os.path.join(os.path.dirname(current_file_path), "resources", "Materials.csv")
experiments_path = os.path.join(os.path.dirname(current_file_path), "resources", "Experiments.csv")
#create material and experiment enums from excel files
MaterialType = create_material_enum_from_excel(materials_path, "Material")
ExperimentType = create_material_enum_from_excel(experiments_path, "Experiment_Type")

class DataSet1(BaseModel):
    pick_dataset_type: Datatype
    extension_of_the_file: str 
    time_series:  bool
    number_of_files: int
    description: str
    Materials: MaterialType
    Experiments: Set[ExperimentType]

def DataSetForm(display_stored_data: bool = False):
    """
    Dataset Form for collecting metadata about the dataset.
    Dataset form data is stored in session state variable `dataset_form_data`.
    """
    # create dataset_form_data in session state if it doesn't exist
    if 'dataset_form_data' not in st.session_state:
        st.session_state.dataset_form_data = []
    
    #form 
    st.title("Dataset Information")
    dataset = sp.pydantic_form(key="Dataset", model=DataSet1, clear_on_submit=True)
    
    # Store submitted data in session state
    if dataset:
        st.session_state.dataset_form_data.append(dataset.model_dump())
        st.success("Data submitted successfully!")
    else:
        st.error("Please fill in all required fields.")
    
    # Display stored data (optional, for verification)
    if display_stored_data and 'dataset_form_data' in st.session_state:
        st.subheader("Stored Dataset Form Data:")
        st.json(st.session_state.dataset_form_data)

if __name__ == "__main__":
    DataSetForm(display_stored_data=True)