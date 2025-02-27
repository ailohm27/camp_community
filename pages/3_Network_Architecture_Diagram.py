# Code for IRE Network Architecture app

import streamlit as st
import pandas as pd
import graphviz
from faker import Faker
from rich.console import Console
import os

# Streamlit UI Header
st.title("🛠 Refined Architecture Diagram Generator")
st.markdown("""
Generate a random **architecture diagram** showcasing system components, 
dependencies, and data flow, **grouped by technology domains** in a left-to-right layout.
""")

# Initialize Faker & Console Logging
fake = Faker('en_US')
console = Console()

# Consolidated mapping: Technology domains with their component types.
domain_to_types = {
    "Frontend": ["Web Server"],
    "Backend Services": ["API Gateway"],
    "Security & IAM": ["Auth Service"],
    "Data & Storage": ["Database", "Cache Layer"],
    "Messaging & Events": ["Message Queue"],
    "Infrastructure & Networking": ["Load Balancer"],
    "DevOps & CI/CD": ["CI/CD Pipeline"],
    "Monitoring & Logging": ["Monitoring Service"],
    "Collaboration & Integration": ["Integration Hub"]
}

# Build a reverse mapping: component type -> domain
domain_mapping = {
    ctype: domain
    for domain, ctypes in domain_to_types.items()
    for ctype in ctypes
}

# List of all component types (the union of all values in domain_to_types)
component_types = [ctype for ctypes in domain_to_types.values() for ctype in ctypes]

# Expanded data flow types
data_flow_types = [
    "HTTP Request", "SQL Query", "Message Publish", "Authentication Check", 
    "Data Cache", "REST API Call", "Load Balancing", "Deployment Trigger", 
    "Alert Notification", "Data Sync"
]

# Sidebar Controls
num_components = st.sidebar.slider("Number of Components", min_value=5, max_value=500, value=25, step=5)
output_format = st.sidebar.selectbox("Diagram File Format", ["png", "pdf"])

# Generate system components
architecture_data = []
for _ in range(num_components):
    component_name = fake.company().replace(" ", "-")
    component_type = fake.random_element(component_types)
    dependencies = fake.random_elements(elements=component_types, length=fake.random_int(min=1, max=3), unique=True)
    data_flows = fake.random_elements(elements=data_flow_types, length=len(dependencies))
    domain = domain_mapping.get(component_type, "Other")
    
    architecture_data.append({
        "component": component_name,
        "type": component_type,
        "domain": domain,
        "dependencies": dependencies,
        "data_flows": data_flows
    })

# Convert generated data to DataFrame and display
df = pd.DataFrame(architecture_data)
st.subheader("🔍 Generated System Components & Relationships")
st.dataframe(df)

# Create a Graphviz Digraph using the DOT engine with left-to-right layout
g = graphviz.Digraph(format=output_format, engine="dot")
g.attr(
    compound="true",
    rankdir="LR",      # Left-to-right flow
    overlap="false",   # Tries to reduce node overlap
    splines="true",    # Smoother edges
    style="filled",
    color="lightgray",
    fillcolor="white",
    nodesep="1",
    ranksep="20"
)

# Define node shapes for each component type (default to rectangle)
component_shapes = {
    "Web Server": "rectangle",
    "Database": "cylinder",
    "API Gateway": "parallelogram",
    "Message Queue": "ellipse",
    "Auth Service": "diamond",
    "Cache Layer": "hexagon",
    "Load Balancer": "octagon",
    "CI/CD Pipeline": "box3d",
    "Monitoring Service": "note",
    "Integration Hub": "folder"
}

# Define line colors for each data flow type
data_flow_colors = {
    "HTTP Request": "blue",
    "SQL Query": "red",
    "Message Publish": "green",
    "Authentication Check": "purple",
    "Data Cache": "brown",
    "REST API Call": "orange",
    "Load Balancing": "teal",
    "Deployment Trigger": "magenta",
    "Alert Notification": "gold",
    "Data Sync": "cyan"
}

# Create clusters (subgraphs) for each technology domain
domains = df['domain'].unique()
clusters = {}
for domain in domains:
    cluster_name = f"cluster_{domain.lower().replace(' ', '_')}"
    with g.subgraph(name=cluster_name) as sub:
        sub.attr(label=domain, color="black", style="dashed")
        clusters[domain] = sub

# Add nodes to their corresponding domain clusters (nodes: black border, white fill)
added_nodes = {}
for _, row in df.iterrows():
    domain = row["domain"]
    if row["component"] not in added_nodes:
        clusters[domain].node(
            row["component"],
            label=f"{row['component']}\n({row['type']})",
            shape=component_shapes.get(row["type"], "rectangle"),
            color="black",
            style="filled",
            fillcolor="white",
            fontcolor="black"
        )
        added_nodes[row["component"]] = True

# Add edges (direct connections between system components), coloring by data flow
for _, row in df.iterrows():
    for i, dependency in enumerate(row["dependencies"]):
        data_flow = row["data_flows"][i] if i < len(row["data_flows"]) else "Unknown Flow"
        edge_color = data_flow_colors.get(data_flow, "black")
        # Draw an edge from the component to the dependency
        g.edge(
            row["component"],
            dependency,
            label=data_flow,
            color=edge_color,
            style="solid"
        )

# Render the diagram to a file (PNG or PDF)
output_filename = "architecture_diagram"
g.render(output_filename, cleanup=True)
diagram_file = f"{output_filename}.{output_format}"

# # Display the Architecture Diagram in Streamlit
# st.subheader("📊 Architecture Diagram (Preview)")
# st.graphviz_chart(g)

# Provide a download button to retrieve the static file for offline usage/printing
if os.path.exists(diagram_file):
    with open(diagram_file, "rb") as f:
        st.download_button(
            label=f"💾 Download Diagram as {output_format.upper()}",
            data=f,
            file_name=os.path.basename(diagram_file),
            mime=f"image/{output_format}" if output_format == "png" else "application/pdf"
        )
    st.success(f"Diagram generated and saved as {diagram_file}")
else:
    st.error("Could not find the generated diagram file!")

# -------------------------------
# Create a Meta Diagram for Domains
# -------------------------------

# Create a new Graphviz Digraph for the domain-level meta diagram
g_meta = graphviz.Digraph(format=output_format, engine="dot")
g_meta.attr(
    rankdir="LR",      # Left-to-right layout
    overlap="false",
    splines="true",
)
g_meta.attr(label="Domain Interdependencies", labelloc="t", fontsize="20")

# Get the set of all domains present in your data
domains_set = sorted(set(df['domain']))
# Add each domain as a node
for domain in domains_set:
    g_meta.node(domain,
                label=domain,
                shape="box",
                style="filled",
                fillcolor="lightblue",
                fontcolor="black")

# Count cross-domain dependencies.
meta_edges = {}
for comp in architecture_data:
    source_domain = comp["domain"]
    for dep in comp["dependencies"]:
        # Look up the domain of the dependency using our reverse mapping.
        target_domain = domain_mapping.get(dep, "Other")
        if source_domain != target_domain:
            key = (source_domain, target_domain)
            meta_edges[key] = meta_edges.get(key, 0) + 1

# Add edges to the meta diagram with counts as labels.
for (src, tgt), count in meta_edges.items():
    g_meta.edge(src, tgt, label=str(count), color="gray", style="bold")

# Render the diagram to a file (PNG or PDF)
output_filename = "domain_architecture_diagram"
g.render(output_filename, cleanup=True)
diagram_file = f"{output_filename}.{output_format}"

# Display the meta diagram in Streamlit.
st.subheader("📊 Domain Meta Diagram")
st.graphviz_chart(g_meta)

# Display the Architecture Diagram in Streamlit
st.subheader("📊 Architecture Diagram (Preview)")
st.graphviz_chart(g)

# Provide a download button to retrieve the static file for offline usage/printing
if os.path.exists(diagram_file):
    with open(diagram_file, "rb") as f:
        st.download_button(
            label=f"💾 Download Diagram as {output_format.upper()}",
            data=f,
            file_name=os.path.basename(diagram_file),
            mime=f"image/{output_format}" if output_format == "png" else "application/pdf"
        )
    st.success(f"Diagram generated and saved as {diagram_file}")
else:
    st.error("Could not find the generated diagram file!")