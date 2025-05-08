import json
import pandas as pd
from enum import Enum
import streamlit as st
import datetime
# Custom JSON encoder to handle sets
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
    

# Function to create Enum from Excel
def create_material_enum_from_excel(excel_path: str, column_name: str) -> type:
    df = pd.read_csv(excel_path)
    material_names = df[column_name].dropna().unique()
    enum_members = {str(name).replace(" ", "_").lower(): str(name) for name in material_names if str(name)}
    return Enum('MaterialType', enum_members) if enum_members else Enum('MaterialType', {'default': 'default'})
