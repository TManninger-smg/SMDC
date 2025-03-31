import streamlit as st
import pandas as pd
import os

st.cache_data.clear()

def main():
    st.title("Fill Out Form")

    # Load Experiments Data
    @st.cache_data
    def load_experiments():
        file_path = os.path.join(os.getcwd(), "Experiments.CSV")
        if not os.path.exists(file_path):
            st.error(f"Error: The file '{file_path}' was not found.")
            return []
        df = pd.read_csv(file_path)
        df["Combined"] = df["Experiment_Type"] + " - " + df["Experiment_Description"] + " - " + df["Common_Experiment"]
        return df["Combined"].tolist()

    experiment_options = load_experiments()

    # Load Materials Data
    @st.cache_data
    def load_materials():
        file_path = os.path.join(os.getcwd(), "Materials.CSV")
        if not os.path.exists(file_path):
            st.error(f"Error: The file '{file_path}' was not found.")
            return []
        df = pd.read_csv(file_path)
        if "Material" not in df.columns or "Description" not in df.columns:
            st.error("Error: Expected columns 'Material' and 'Description' not found in Materials.CSV")
            return []
        df["Combined"] = df["Material"] + " - " + df["Description"]
        return df["Combined"].tolist()

    material_options = load_materials()

    # Load Data Categories (UTF-16 support)
    @st.cache_data
    def load_data_categories():
        file_path = os.path.join(os.getcwd(), "Data_Categories.CSV")
        if not os.path.exists(file_path):
            st.error(f"Error: The file '{file_path}' was not found.")
            return []
        df = pd.read_csv(file_path, encoding="utf-16")
        return df["Data_Category"].tolist()

    data_categories_options = load_data_categories()

    # Main Form Section
    st.header("Main Form")
    title = st.text_input("Title*")
    keywords = st.text_area("Keywords (up to 10)*")
    description = st.text_area("Description - for human readers")
    uploader = st.text_input("Uploader/Datahost/First author*")
    email = st.text_input("E-mail contact*")
    contributors = st.text_area("Contributor(s) - optional place for Co-Authors etc")
    date = st.text_input("Date - choose a year*")
    identifier = st.text_input("Identifier* (e.g., DOI or repository link)")

    # Dataset Sections
    if "dataset_count" not in st.session_state:
        st.session_state.dataset_count = 1

    for i in range(1, st.session_state.dataset_count + 1):
        st.subheader(f"Dataset{i} in my repository")

        dataset_type = st.selectbox(
            f"Pick one for Dataset{i}",
            ["picture/graph/audio/video", "table", "folder with pictures/graphs/audios/videos"],
            key=f"dataset_type_{i}"
        )
        filename = st.text_input(f"Filename.ext for Dataset{i}", key=f"filename_{i}")

        if dataset_type == "table":
            num_entries = st.text_input(f"Number of entries (lines) for Dataset{i}", key=f"num_entries_{i}")
            num_columns = st.number_input(f"Number of Columns for Dataset{i}", min_value=1, step=1, key=f"num_columns_{i}")

            if f"table_data_{i}" not in st.session_state:
                st.session_state[f"table_data_{i}"] = pd.DataFrame(
                    [["", "", "Factor"] for _ in range(num_columns)],
                    columns=["Column Description", "Entity Description", "Role"]
                )
            edited_table = st.data_editor(
                st.session_state[f"table_data_{i}"],
                key=f"editable_table_{i}"
            )
            edited_table["Role"] = edited_table["Role"].apply(lambda x: x if x in ["Factor", "Response"] else "Factor")
            st.session_state[f"table_data_{i}"] = edited_table
        else:
            num_files = st.text_input(f"Number of files for Dataset{i}", key=f"num_files_{i}")
            file_description = st.text_area(f"Description of files for Dataset{i}", key=f"file_description_{i}")

        # Show Data Categories only for picture/graph/audio/video
        if dataset_type == "picture/graph/audio/video":
            data_categories = st.multiselect(
                f"Select Data Categories for Dataset{i}",
                options=data_categories_options,
                key=f"data_categories_{i}"
            )

        experiments = st.multiselect(f"Which experiments were done for Dataset{i}", experiment_options, key=f"experiments_{i}")
        materials = st.multiselect(f"Which materials were used for Dataset{i}", material_options, key=f"materials_{i}")

    if st.button("+ Add Another Dataset"):
        st.session_state.dataset_count += 1

    # Additional Information Section
    st.header("Additional Information")
    temperature = st.selectbox("Temperature", ["Room Temperature", "<10 °C", ">30 °C", "In the Data Table", "User-defined Temperature"])
    user_defined = st.text_input("User-defined Temperature") if temperature == "User-defined Temperature" else ""
    location = st.selectbox("Add Location", ["lab", "in the Data Table", "Coordinates"])
    coordinates = st.text_input("Coordinates") if location == "Coordinates" else ""

    # Submit Button
    if st.button("Submit"):
        st.success("Form Submitted Successfully!")

if __name__ == "__main__":
    main()
