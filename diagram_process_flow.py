from diagrams import Diagram
from diagrams.programming.flowchart import InputOutput, Action, Document, ManualInput
import streamlit as st
import pandas as pd
import graphviz

diagram_path = "process_flow"

with Diagram("", filename=diagram_path, show=False, direction="TB", graph_attr={"ranksep": "20", "nodesep": "1"}):
    excel_files = InputOutput("Excel Files\n\n")

    python_scripting_1 = Action("Python Scripting\n\n")
    data_outputs = [
        Document("RACI\n\n"),
        Document("Backup Data Flow\n\n"),
        Document("IRE Network Architecture\n\n"),
        Document("Cloud Environment\n\n")
    ]

    python_scripting_2 = Action("Python Scripting\n\n")
    draft_report = Document("Draft IRE Report\n\n")

    review_step = ManualInput("Human in the Loop\n\n")
    final_report = Document("Finalized IRE Report\n\n")

    api_call = Action("Prompt Engineering API\n\n")
    final_sow = Document("SOW\n\n")

    # Add labels to arrows
    excel_files >> python_scripting_1 >> data_outputs
    data_outputs >> python_scripting_2 >> draft_report
    draft_report >> review_step >> final_report
    final_report >> api_call >> final_sow

# Check if the diagram was generated
import os
if os.path.exists(diagram_path + ".png"):
    st.image(diagram_path + ".png", caption="Describes what processes are in place to support the creation of an IRE.", use_container_width=True)
else:
    st.error("Diagram was not generated! Check for errors.")