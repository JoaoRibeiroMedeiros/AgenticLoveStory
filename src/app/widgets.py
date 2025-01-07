
import streamlit as st

def st_display_output(title, workflow):
    st.markdown(f"### {title.replace('_', ' ').capitalize()}")
    st.markdown(workflow['outputs'][title])

