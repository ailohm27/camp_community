import streamlit as st
import graphviz

# Function to generate Graphviz table
def generate_table(features):
    dot = graphviz.Digraph()
    
    # Define table structure
    table_header = "<TABLE BORDER='1' CELLBORDER='1' CELLSPACING='0'>"
    table_header += "<TR><TD><B>Feature</B></TD></TR>"
    
    for feature in features:
        table_header += f"<TR><TD>{feature}</TD></TR>"
    
    table_header += "</TABLE>"

    # Add table as a node
    dot.node("table", label=f"<<{table_header}>>", shape="plaintext")

    return dot

# Streamlit UI
st.title("Modular Table Generator using Graphviz")

# Get user-defined features
features = st.text_area("Enter features (one per line)").split("\n")
features = [f.strip() for f in features if f.strip()]  # Remove empty lines

if features:
    st.graphviz_chart(generate_table(features))
