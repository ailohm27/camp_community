import os
import streamlit as st
import graphviz

# Set output format (choose "png" or "pdf")
output_format = "png"

# Streamlit UI Header
st.title("🛠 POC IRE Architecture Diagram")
st.markdown("""
The solutions architecture diagram displays the flow of information and 
technologies used in supporting the POC.
""")

architecture_data = [
    {
        "component": "Deliverables Template",
        "type": "Template",
        "dependencies": ["Excel Data, Diagrams", "Excel Data, RACI"],
        "data_flows": ["Generation of Fake Data", "Generation of Fake Data"]
    },
    {
        "component": "Excel Data, Diagrams",
        "type": "Excel",
        "dependencies": ["Diagram Python Script"],
        "data_flows": ["Transfer of Data"]
    },
    {
        "component": "Excel Data, RACI",
        "type": "Excel",
        "dependencies": ["RACI Python Script"],
        "data_flows": ["Transfer of Data"]
    },
    {
        "component": "Diagram Python Script",
        "type": "Python Script",
        "dependencies": ["Diagrams"],
        "data_flows": ["Publish"]
    },
    {
        "component": "RACI Python Script",
        "type": "Python Script",
        "dependencies": ["RACI"],
        "data_flows": ["Publish"]
    },
    {
        "component": "Diagrams",
        "type": "Visualizations",
        "dependencies": ["SOW"],
        "data_flows": ["Script Python"]
    },
    {
        "component": "RACI",
        "type": "Table",
        "dependencies": ["SOW"],
        "data_flows": ["Script Python"]
    },
    {
        "component": "SOW",
        "type": "SOW",
        "dependencies": [],
        "data_flows": []
    }
]

# Create a Graphviz Digraph using the DOT engine (top-to-bottom layout)
g = graphviz.Digraph(format=output_format, engine="dot")
g.attr(
    compound="true",
    rankdir="TB",       # Top-to-bottom layout
    overlap="false",    # Reduce node overlap
    splines="true",     # Smoother edges
    style="filled",
    color="lightgray",
    fillcolor="white",
    nodesep="1",
    ranksep="1"
)

# Define node shapes for each component type
component_shapes = {
    "Template": "octagon",
    "Report": "box",
    "Excel": "oval",
    "Python Script": "octagon",
    "Visualizations": "oval",
    "RACI": "box",
    "SOW": "box"
}

# Define edge colors for each data flow type
data_flow_colors = {
    "Generation of Fake Data": "blue",
    "Python Query": "red",
    "Transfer of Data": "green",
    "Publish": "purple",
    "Python Script": "brown"
}

# Add nodes directly to the main graph (each component appears only once)
added_nodes = {}
for item in architecture_data:
    comp = item["component"]
    if comp not in added_nodes:
        g.node(
            comp,
            label=f"{comp}\n({item['type']})",
            shape=component_shapes.get(item["type"], "rectangle"),
            color="black",
            style="filled",
            fillcolor="white",
            fontcolor="black"
        )
        added_nodes[comp] = True

# Add edges between components (color edges based on data flow)
for item in architecture_data:
    comp = item["component"]
    for i, dependency in enumerate(item["dependencies"]):
        data_flow = item["data_flows"][i] if i < len(item["data_flows"]) else "Unknown Flow"
        edge_color = data_flow_colors.get(data_flow, "black")
        g.edge(
            comp,
            dependency,
            label=data_flow,
            color=edge_color,
            style="solid"
        )

# Render diagram to a file and provide a download button
output_filename = "architecture_diagram"
g.render(output_filename, cleanup=True)
diagram_file = f"{output_filename}.{output_format}"

# st.subheader("📊 Architecture Diagram")
st.graphviz_chart(g)

if os.path.exists(diagram_file):
    with open(diagram_file, "rb") as f:
        st.download_button(
            label=f"💾 Download Diagram as {output_format.upper()}",
            data=f,
            file_name=os.path.basename(diagram_file),
            mime="image/png" if output_format == "png" else "application/pdf"
        )
    st.success(f"Diagram generated and saved as {diagram_file}")
else:
    st.error("Could not find the generated diagram file!")