
import streamlit as st

from src.ai.utils import get_initial_state
from src.ai.workflow import WriteflowManager, display_outputs, save_outputs, load_joined_outputs


st.secrets["OPENAI_API_KEY"]
session_state = st.session_state 
session_state.user_input = st.text_area("Write your story here:", height=300)

initial_state = get_initial_state(session_state.user_input )


writeflow = WriteflowManager()

writing = writeflow.invoke(initial_state)

display_outputs(writing)


