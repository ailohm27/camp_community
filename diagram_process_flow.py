from diagrams import Diagram
from diagrams.programming.flowchart import InputOutput, Action, Document, ManualInput
import streamlit as st
import pandas as pd
import graphviz

diagram_path = "process_flow"

with Diagram("", filename=diagram_path, show=False, direction="TB", graph_attr={"ranksep": "2.5", "nodesep": "1.5"}):
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

    # Add labels to arrows
    excel_files >> python_scripting_1 >> data_outputs
    data_outputs >> python_scripting_2 >> draft_report
    draft_report >> review_step >> final_report
    final_report >> api_call >> final_sow

# print(Diagram) # test for ensuring Diagram is running properly in the environment

# st.write("Process Flow Diagram")
# with Diagram(show=False, direction="LB"):
#     InputOutput("Excel Files") >> Action("Python Scripting") >> [
#         Document("RACI"),
#         Document("Backup Data Flow"),
#         Document("IRE Network Architecture"),
#         Document("Cloud Environment")
#     ] >> Action("Python Scripting") >> Document("Draft IRE Report") >> ManualInput("Human in the Loop") >> Document("Finalized IRE Report") >> Action("Prompt Engineering API") >> Document("SOW")

# Check if the diagram was generated
import os
if os.path.exists(diagram_path + ".png"):
    st.image(diagram_path + ".png", caption="Describes what processes are in place to support the creation of an IRE.", use_container_width=True)
else:
    st.error("Diagram was not generated! Check for errors.")