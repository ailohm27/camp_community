import streamlit as st

st.set_page_config(
    page_title="Start Page",
    page_icon="👋",
)
st.write("# IRE Design Automation POC")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This is the work of Alexis Lohman, Kaz Kazarnoff and Shanay Martin. 

    Shanay presented the idea to the team to automate an IRE generation. For workstreams, she was focused on the creation of the RACI to be 
    templatized to support the automatic scirpting to populate it. 
    Kaz and Alexis support efforts in creating the python scripts, generating fake data and setting up the wireframe
    for Streamlit.

    Please flip through portions of the POC to understand the process flow and architecrtual diagram, in addition to the individual
    components making up the rought draft of the populated IRE.
"""
)