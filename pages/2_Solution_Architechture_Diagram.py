import os
import streamlit as st
import graphviz

# Set output format (choose "png" or "pdf")
output_format = "png"

# Streamlit UI Header
st.title("🛠 Solution Architecture Diagram")
st.markdown("""
The solutions architecture diagram displays the flow of information and 
technologies used in supporting the POC.
""")
# -----------------------------------------------------------------------------
# Static architecture data (adjust as needed)
# Each dictionary represents a component with:
# - "component": unique component name
# - "type": the type (for shape lookup)
# - "domain": the technology domain (used for clustering)
# - "dependencies": list of component names it connects to
# - "data_flows": list of labels (one per dependency)
# -----------------------------------------------------------------------------
architecture_data = [
    {
        "component": "Data Template for Deliverables",
        "type": "Template",
        "domain": "Frontend",
        "dependencies": ["Excel Data for Diagrams", "Excel Data for RACI"],
        "data_flows": ["Generation of Fake Data", "Generation of Fake Data"]
    },
    {
        "component": "Excel Data for Diagrams",
        "type": "Excel",
        "domain": "Backend Services",
        "dependencies": ["Python Script(s) for Diagrams"],
        "data_flows": ["Message Publish"]
    },
    {
        "component": "Excel Data for RACI",
        "type": "Excel",
        "domain": "Backend Services",
        "dependencies": ["Python Script for RACI"],
        "data_flows": []
    },
    {
        "component": "Python Script(s) for Diagrams",
        "type": "Python Script",
        "domain": "DevOps & CI/CD",
        "dependencies": ["Diagram Visualizations"],
        "data_flows": []
    },
    {
        "component": "Python Script for RACI",
        "type": "Python Script",
        "domain": "DevOps & CI/CD",
        "dependencies": ["Populated RACI"],
        "data_flows": []
    },
    {
        "component": "Diagram Visualizations",
        "type": "Visualizations",
        "domain": "Monitoring & Logging",
        "dependencies": ["SOW"],
        "data_flows": []
    },
    {
        "component": "Populated RACI",
        "type": "RACI",
        "domain": "Security & IAM",
        "dependencies": ["SOW"],
        "data_flows": []
    },
    {
        "component": "SOW",
        "type": "SOW",
        "domain": "Collaboration & Integration",
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
    "Template": "diamond",
    "Report": "box",
    "Excel": "ellipse",
    "Python Script": "diamond",
    "Visualizations": "ellipse",
    "RACI": "box",
    "SOW": "box"
}

# Define edge colors for each data flow type
data_flow_colors = {
    "Transfer of Data": "blue",
    "SQL Query": "red",
    "Message Publish": "green",
    "Authentication Check": "purple",
    "Data Cache": "brown"
}

# Build clusters based on domain
# Get unique domains from static data.
domains = list({item["domain"] for item in architecture_data})
clusters = {}
for domain in domains:
    cluster_name = f"cluster_{domain.lower().replace(' ', '_')}"
    with g.subgraph(name=cluster_name) as sub:
        sub.attr(label=domain, color="black", style="dashed")
        clusters[domain] = sub

# Add nodes to clusters (each component appears only once)
added_nodes = {}
for item in architecture_data:
    comp = item["component"]
    domain = item["domain"]
    if comp not in added_nodes:
        clusters[domain].node(
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

st.subheader("📊 Architecture Diagram")
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