import os
import json
import streamlit as st
import pandas as pd
import graphviz
from faker import Faker
from faker.providers import BaseProvider

#################################
# 1) DATA GENERATION FUNCTION
#################################
def generate_sample_data(num_profiles=100, parameters_file="./data/parametersBackupData.json", output_file="./data/sampleDataTest2.json"):
    """
    Generates random backup data using Faker.
    Each field is a single value.
    Writes the generated data to a JSON file and returns the data.
    
    Expected keys in the parameters file (example):
      - "Current Backup Products"
      - "IRE Backup Products"
      - "# of Backup Environment"  <-- note: singular "Environment"
      - "Technologies to Be Placed in Vault"
      - "Traffic Allowed"
      - "Traffic Blocked"
    """
    fake = Faker('en_US')
    with open(parameters_file, 'r') as f:
        file_data = json.load(f)

    class BackupProvider(BaseProvider):
        def current_backup_products(self):
            return fake.random_element(file_data["Current Backup Products"])
        def ire_backup_products(self):
            return fake.random_element(file_data["IRE Backup Products"])
        def num_of_backup_environments(self):
            # Use the key as it appears in your file (singular)
            return fake.random_element(file_data["# of Backup Environment"])
        def technologies_to_be_placed_in_vault(self):
            return fake.random_element(file_data["Technologies to Be Placed in Vault"])
        def traffic_allowed(self):
            return fake.random_element(file_data["Traffic Allowed"])
        def traffic_blocked(self):
            return fake.random_element(file_data["Traffic Blocked"])

    fake.add_provider(BackupProvider)

    st.markdown('<p style="color: green; font-weight: bold;">SAMPLE DATA GENERATOR</p>', unsafe_allow_html=True)
    st.write(f"Generating {num_profiles} backup profiles...")

    data = []
    for _ in range(num_profiles):
        profile = {
            "Current Backup Products": fake.current_backup_products(),
            "IRE Backup Products": fake.ire_backup_products(),
            "# of Backup Environment": fake.num_of_backup_environments(),
            "Technologies to Be Placed in Vault": fake.technologies_to_be_placed_in_vault(),
            "Traffic Allowed": fake.traffic_allowed(),
            "Traffic Blocked": fake.traffic_blocked(),
        }
        data.append(profile)

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
    
    st.success(f"Data generated and saved to {output_file}")
    return data

#################################
# 2) TRANSFORM FOR TABLE
#################################
def transform_data_for_table(data):
    """
    For backup data (single values), returns the data unchanged.
    """
    return data

#################################
# 3) CLASSIFY & BUILD DIAGRAM
#################################
def classify_resource(key):
    """
    Classify a resource key into a group.
    For backup data:
      - If the key contains "backup", "vault", or "blocked" → "Backup"
      - If it contains "firewall", "router", "dns", or "traffic allowed" → "Secondary"
      - Otherwise → "Primary"
    """
    lower_key = key.lower()
    if "backup" in lower_key or "vault" in lower_key or "blocked" in lower_key:
        return "Backup"
    elif "firewall" in lower_key or "router" in lower_key or "dns" in lower_key or "traffic allowed" in lower_key:
        return "Secondary"
    else:
        return "Primary"

def build_cloud_tenant_diagram(profile):
    """
    Creates a cloud-agnostic landing zone–style diagram using the first backup profile.
    
    Diagram structure:
      - Root tenant: "Cloud Tenant (Root)"
         • Under this, a Platform Group containing:
             - "Subscription: Primary" (for resources classified as Primary)
             - "Subscription: Secondary" (for resources classified as Secondary)
         • Also, a Backup Group containing:
             - "Subscription: Backup Services" (for resources classified as Backup)
    
    Resources from 'profile' are added to the appropriate subgraph.
    """
    g = graphviz.Digraph(format="png", engine="dot")
    g.attr(rankdir="LR", splines="true", nodesep="1.5", ranksep="2.0")

    # Dictionary to hold subgraph references
    subgraphs = {}

    # Root tenant subgraph
    with g.subgraph(name="cluster_root") as root:
        root.attr(label="Cloud Tenant (Root)", style="dashed", color="gray")
        
        # Platform Group
        with root.subgraph(name="cluster_platform") as platform:
            platform.attr(label="Platform Group", style="filled", fillcolor="#E8F4FA")
            with platform.subgraph(name="cluster_primary") as primary:
                primary.attr(label="Subscription: Primary", style="filled", fillcolor="#F0F8FF")
                subgraphs["Primary"] = primary
            with platform.subgraph(name="cluster_secondary") as secondary:
                secondary.attr(label="Subscription: Secondary", style="filled", fillcolor="#F0F8FF")
                subgraphs["Secondary"] = secondary

        # Backup Group
        with root.subgraph(name="cluster_backup") as backup:
            backup.attr(label="Backup Group", style="filled", fillcolor="#FFE5E5")
            with backup.subgraph(name="cluster_backup_sub") as backup_sub:
                backup_sub.attr(label="Subscription: Backup Services", style="filled", fillcolor="#FFE5E5")
                subgraphs["Backup"] = backup_sub

    # Add resource nodes into the appropriate subgraph
    for key, val in profile.items():
        # Create a label with the key and value
        label = f"{key}\n({val})"
        group = classify_resource(key)  # "Primary", "Secondary", or "Backup"
        node_id = f"{group}_{key}"
        if group in subgraphs:
            subgraphs[group].node(
                node_id,
                label=label,
                shape="box",
                style="filled",
                fillcolor="white",
                color="black",
                fontcolor="black"
            )

    # Example edges (update these based on your real relationships)
    g.edge("Primary_Firewall_Management", "Secondary_Firewalls", label="Manages")
    g.edge("Primary_Storage_Devices", "Backup_Backup_Products", label="Backups")
    g.edge("Secondary_Routers", "Primary_Default_Gateway", label="Routing")

    return g

#################################
# 4) STREAMLIT APP
#################################
def main():
    st.title("Cloud-Agnostic Backup Data Flow Generator & Diagram")
    st.markdown("""
This app generates sample backup data and builds a cloud-agnostic landing zone–style diagram.
Data fields are single values.
    """)

    # Use session state for data persistence
    if "data" not in st.session_state:
        st.session_state["data"] = None

    st.markdown("### 1) Generate or Load Data")
    generate_new = st.checkbox("Generate new data?", value=True)
    num_profiles = st.number_input("Number of Backup Profiles", min_value=1, value=100)
    parameters_file = st.text_input("Parameters File Path", "./data/parametersBackupData.json")
    output_file = st.text_input("Output File Path", "./data/sampleDataTest2.json")

    if generate_new:
        if st.button("Generate Data Now"):
            data = generate_sample_data(num_profiles, parameters_file, output_file)
            st.session_state["data"] = data
    else:
        st.write("Using existing data if available.")

    if st.button("Load Data from File"):
        if not os.path.exists(output_file):
            st.error(f"No data file found at {output_file}")
        else:
            with open(output_file, "r") as f:
                loaded_data = json.load(f)
            if not loaded_data:
                st.error("Data file is empty!")
            else:
                st.session_state["data"] = loaded_data
                st.success(f"Loaded {len(loaded_data)} profiles from {output_file}")

    if st.session_state["data"]:
        st.subheader("Sample Data Table")
        transformed = transform_data_for_table(st.session_state["data"])
        df = pd.DataFrame(transformed)
        st.dataframe(df)
    else:
        st.info("No data to display yet. Generate or load data first.")
        return

    st.markdown("### 2) Build Cloud Tenant Diagram")
    if st.button("Build Diagram"):
        profile = st.session_state["data"][0]
        diagram = build_cloud_tenant_diagram(profile)
        st.graphviz_chart(diagram)
        diagram.render("cloud_tenant_diagram", cleanup=True)
        png_file = "cloud_tenant_diagram.png"
        if os.path.exists(png_file):
            with open(png_file, "rb") as f:
                st.download_button(
                    label="💾 Download Diagram (PNG)",
                    data=f,
                    file_name="cloud_tenant_diagram.png",
                    mime="image/png"
                )
            st.success(f"Diagram generated and saved as {png_file}")
        else:
            st.error("Could not find the diagram file!")

if __name__ == "__main__":
    main()