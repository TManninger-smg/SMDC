"""
Author Data form for collecting  essential information about the dataset's author.
"""
from pydantic import BaseModel , Field, EmailStr
import streamlit_pydantic as sp
import streamlit as st
import  datetime
class AuthorData(BaseModel):
    title: str = Field( description="Title of the dataset", min_length=1)
    keywords_comma_sperated: str = Field(description="Keywords related to the dataset", min_length=1)
    description: str = Field( description="Description of the dataset", min_length=1)
    uploaded_by: str= Field(description="Name of the person who uploaded the dataset")    
    email: EmailStr = Field(description="Email of the person who uploaded the dataset")
    date: datetime.date = Field(description="Date of data creation")
    identifier: str = Field(description="Unique identifier for the dataset",min_length=1)
    contributors: str = Field(default="", description="Contributors to the dataset")

def AuthorDataPage(display_stored_data: bool = False):
    """
    Author Data Page for collecting metadata about the dataset.
    Author data is stored in session state variable `author_data`.
    """
    st.title("Author Information")
    data = sp.pydantic_form(key="Author Information", model=AuthorData, clear_on_submit=True)
    if data:
        st.session_state.author_data = data.model_dump()
        st.success("Data submitted successfully!")
    else:
        st.error("Please fill in all required fields.")

    # Display stored data (optional, for verification)
    if display_stored_data and 'author_data' in st.session_state:
        st.subheader("Stored Author Data:")
        st.json(st.session_state.author_data) 

    
if __name__=="__main__":
        AuthorDataPage(display_stored_data=True)
    