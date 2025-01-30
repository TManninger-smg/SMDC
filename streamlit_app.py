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
        st.write(f"Looking for file at: {file_path}")  # Debugging output
        
        if not os.path.exists(file_path):
            st.error(f"Error: The file '{file_path}' was not found. Please ensure it is in the correct directory.")
            return []
        df = pd.read_csv(file_path)
        df["Combined"] = df["Experiment_Type"] + " - " + df["Experiment_Description"] + " - " + df["Common_Experiment"]
        return df["Combined"].tolist()
    
    experiment_options = load_experiments()

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
        filename = st.text_input(
            f"Filename.ext for Dataset{i} (please write your filename and the extension)",
            key=f"filename_{i}"
        )

        if dataset_type == "table":
            st.write("Table Structure")

            # Number of Entries Input
            num_entries = st.text_input(
                f"Number of entries (lines) for Dataset{i}",
                key=f"num_entries_{i}"
            )
            
            # Number of Columns Input
            num_columns = st.number_input(
                f"Number of Columns for Dataset{i}",
                min_value=1, step=1, key=f"num_columns_{i}"
            )

            # Editable Table
            if f"table_data_{i}" not in st.session_state:
                st.session_state[f"table_data_{i}"] = pd.DataFrame(
                    [["", "", "Factor"] for _ in range(num_columns)],
                    columns=["Column Description", "Entity Description", "Role"]
                )
            else:
                # Update the number of rows in the table dynamically
                current_table = st.session_state[f"table_data_{i}"]
                if len(current_table) != num_columns:
                    st.session_state[f"table_data_{i}"] = pd.DataFrame(
                        [["", "", "Factor"] for _ in range(num_columns)],
                        columns=["Column Description", "Entity Description", "Role"]
                    )

            edited_table = st.data_editor(
                st.session_state[f"table_data_{i}"],
                key=f"editable_table_{i}"
            )

            # Ensure only "Factor" or "Response" are allowed in the "Role" column
            if "Role" in edited_table.columns:
                edited_table["Role"] = edited_table["Role"].apply(
                    lambda x: x if x in ["Factor", "Response"] else "Factor"
                )

            st.session_state[f"table_data_{i}"] = edited_table
        else:
            num_files = st.text_input(
                f"Number of files for Dataset{i}",
                key=f"num_files_{i}"
            )
            file_description = st.text_area(
                f"Description of files for Dataset{i}",
                key=f"file_description_{i}"
            )

        experiments = st.multiselect(
            f"Which experiments were done for Dataset{i} (to obtain that data)",
            options=experiment_options,
            key=f"experiments_{i}"
        )
        materials = st.text_area(
            f"Which materials were used for Dataset{i}",
            key=f"materials_{i}"
        )

    # Add More Datasets
    if st.button("+ Add Another Dataset"):
        st.session_state.dataset_count += 1

    # Additional Information Section
    st.header("Additional Information")
    temperature = st.selectbox(
        "Temperature",
        ["Room Temperature", "<10 °C", ">30 °C", "In the Data Table", "User-defined Temperature"]
    )

    # Only show the text input for user-defined temperature when selected
    if temperature == "User-defined Temperature":
        user_defined = st.text_input("User-defined Temperature")
    else:
        user_defined = ""

    location = st.selectbox("Add Location", ["lab", "in the Data Table", "Coordinates"])

    # Only show the text input for coordinates when "Coordinates" is selected
    if location == "Coordinates":
        coordinates = st.text_input("Coordinates")
    else:
        coordinates = ""

    # Submit Button
    if st.button("Submit"):
        datasets_data = []
        for i in range(1, st.session_state.dataset_count + 1):
            if st.session_state[f"dataset_type_{i}"] == "table":
                table_data = st.session_state[f"table_data_{i}"].to_dict(orient="records")
                num_entries = st.session_state[f"num_entries_{i}"]
            else:
                table_data = {
                    "num_files": st.session_state[f"num_files_{i}"],
                    "file_description": st.session_state[f"file_description_{i}"]
                }
                num_entries = None

            datasets_data.append({
                "type": st.session_state[f"dataset_type_{i}"],
                "filename": st.session_state[f"filename_{i}"],
                "num_entries": num_entries,
                "table": table_data,
                "experiments": st.session_state[f"experiments_{i}"],
                "materials": st.session_state[f"materials_{i}"]
            })

        submitted_data = {
            "title": title,
            "keywords": keywords,
            "description": description,
            "uploader": uploader,
            "email": email,
            "contributors": contributors,
            "date": date,
            "identifier": identifier,
            "datasets": datasets_data,
            "additional_info": {
                "temperature": temperature,
                "user_defined": user_defined,
                "location": location,
                "coordinates": coordinates,
            }
        }

        st.success("Form Submitted Successfully!")
        st.json(submitted_data)

if __name__ == "__main__":
    main()