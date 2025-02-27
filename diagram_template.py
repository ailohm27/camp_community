import diagrams as Diagram
import streamlit as st
import pandas as pd
import graphviz

from diagrams.programming.flowchart import InputOutput, Action, Document, ManualInput

with Diagram("Process Flow", show=False, direction="TB"):
    InputOutput("Excel Files") >> Action("Python Scripting") >> [Document("RACI"),
                                                                Document("Backup Data Flow"),
                                                                Document("IRE Network Architecture"),
                                                                Document("Cloud Environment")] >> Action("Python Scripting") >> Document("Draft IRE Report") >> ManualInput("Human in the Loop") >> Document("Finalized IRE Report") >> Action("Prompt Engineering API") >> Document("SOW")