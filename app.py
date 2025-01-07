
import streamlit as st

from src.ai.utils import get_initial_state
from src.ai.workflow import WriteflowManager, save_outputs, load_joined_outputs
from src.app.widgets import st_display_output


st.secrets["OPENAI_API_KEY"]
session_state = st.session_state 
session_state.user_input = st.text_area("Write your story here:", height=300)

initial_state = get_initial_state(session_state.user_input )
writeflow = WriteflowManager()

session_state.story = st.text_input("Enteryour story idea")
with st.spinner('Please wait...'):
    writing = writeflow.invoke(initial_state)

    st.session_state['stage'] =  st.selectbox(
        "Choose the stage of your story:",
        options=["Introduction", "Conflict", "Climax", "Resolution"],
        format_func=lambda x: {
            "Introduction": "Start of the Story",
            "Conflict": "Rising Action",
            "Climax": "Turning Point",
            "Resolution": "Conclusion"
        }[x]
    )

st_display_output(stage,writing)

if st.button("Next Page"):

    next_page = writeflow.next_page()

    display_outputs(next_page)


