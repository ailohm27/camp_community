import json
import streamlit as st
import pandas as pd
import graphviz
from faker import Faker
from rich.console import Console

# Streamlit UI Header
st.title("🛠 Architecture Diagram Generator")
st.markdown("Generate a random **architecture diagram** showcasing system components, dependencies, and data flow.")

# Initialize Faker & Console Logging
fake = Faker('en_US')
console = Console()

# Define system components
component_types = ["Web Server", "Database", "API Gateway", "Message Queue", "Auth Service", "Cache Layer"]
data_flow_types = ["HTTP Request", "SQL Query", "Message Publish", "Authentication Check", "Data Cache", "REST API Call"]

# Sidebar Controls
num_components = st.sidebar.slider("Number of Components", min_value=3, max_value=10, value=6, step=1)

# Generate system components
architecture_data = []
for _ in range(num_components):
    component_name = fake.company().replace(" ", "-")
    component_type = fake.random_element(component_types)
    dependencies = fake.random_elements(elements=component_types, length=fake.random_int(min=1, max=3), unique=True)
    data_flows = fake.random_elements(elements=data_flow_types, length=len(dependencies))

    architecture_data.append({
        "component": component_name,
        "type": component_type,
        "dependencies": dependencies,
        "data_flows": data_flows
    })

# Convert to DataFrame
df = pd.DataFrame(architecture_data)

# Display the generated architecture table
st.subheader("🔍 Generated System Components & Relationships")
st.dataframe(df)

# Define Graphviz Digraph
g = graphviz.Digraph(format="svg")
g.attr(compound="true", style="filled", color="lightgray", fillcolor="white")

# Define node shapes based on component type
component_shapes = {
    "Web Server": "rectangle",
    "Database": "cylinder",
    "API Gateway": "parallelogram",
    "Message Queue": "ellipse",
    "Auth Service": "diamond",
    "Cache Layer": "hexagon"
}

# Define node colors for better visualization
component_colors = {
    "Web Server": "blue",
    "Database": "orange",
    "API Gateway": "green",
    "Message Queue": "purple",
    "Auth Service": "red",
    "Cache Layer": "brown"
}

# Add nodes (system components)
for _, row in df.iterrows():
    g.node(
        row["component"], 
        label=f"{row['component']}\n({row['type']})",
        shape=component_shapes[row["type"]],
        color=component_colors[row["type"]],
        style="filled",
        fillcolor="white"
    )

# Add edges (connections between system components)
for _, row in df.iterrows():
    for i, dependency in enumerate(row["dependencies"]):
        data_flow = row["data_flows"][i] if i < len(row["data_flows"]) else "Unknown Flow"
        g.edge(row["component"], dependency, label=data_flow, color="black", style="solid")

# Display Architecture Diagram in Streamlit
st.subheader("📊 Architecture Diagram")
st.graphviz_chart(g)

st.success("Architecture Diagram Generated Successfully! 🎉")