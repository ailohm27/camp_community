import os
import streamlit as st
from diagrams import Diagram
from diagrams.programming.flowchart import InputOutput, Action, Document, ManualInput

# Streamlit UI
st.title("IRE Process Flow Diagram")
st.markdown("This diagram describes what processes are in place to support the creation of an IRE.")

# Define the output path for the diagram
diagram_path = "process_flow"
png_path = f"{diagram_path}.png"

# Remove junk output by disabling return values from `diagrams`
with st.spinner("Generating diagram..."):
    with Diagram("", filename=diagram_path, show=False, direction="TB", graph_attr={"ranksep": "1", "nodesep": "1"}):
        # Define nodes
        excel_files = InputOutput("Excel Files")

        python_scripting_1 = Action("Python Scripting")
        data_outputs = [
            Document("RACI"),
            Document("Backup Data Flow"),
            Document("IRE Network Architecture"),
            Document("Cloud Environment")
        ]

        python_scripting_2 = Action("Python Scripting")
        draft_report = Document("Draft IRE Report")
        review_step = ManualInput("Human in the Loop")
        final_report = Document("Finalized IRE Report")
        api_call = Action("Prompt Engineering API")
        final_sow = Document("SOW")

        # Fix the arrow logic to avoid displaying junk output
        _ = excel_files >> python_scripting_1  # Suppress return value

        for doc in data_outputs:
            _ = python_scripting_1 >> doc  # Suppress return value
            _ = doc >> python_scripting_2  # Suppress return value

        _ = python_scripting_2 >> draft_report
        _ = draft_report >> review_step
        _ = review_step >> final_report
        _ = final_report >> api_call
        _ = api_call >> final_sow

# Ensure the PNG file exists before displaying it
if os.path.exists(png_path):
    st.image(png_path, caption="This diagram illustrates the IRE process flow.", use_container_width=True)
else:
    st.error("❌ Diagram was not generated! Check for errors.")
