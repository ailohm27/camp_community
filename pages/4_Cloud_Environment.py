import os
import json
import streamlit as st
import pandas as pd
import graphviz
from faker import Faker
from faker.providers import BaseProvider

#############################
# 1) DATA GENERATION FUNCTION
#############################
def generate_sample_data(num_profiles=20, parameters_file="./data/parameters.json", output_file="./data/sampleDataTest.json"):
    """
    Generates random cloud environment architecture data using Faker,
    writes to a JSON file, and returns the data as a list of dictionaries.
    Each field is a list of two items: [before, after].
    """
    fake = Faker('en_US')
    with open(parameters_file, 'r') as f:
        file_data = json.load(f)

    class SkillsProvider(BaseProvider):
        def Network_Model(self):
            return self.random_elements(file_data["Network Model"], length=2)
        def Cloud_Environment(self):
            return self.random_elements(file_data["Cloud Environment"], length=2)
        def Num_of_subscriptions(self):
            return self.random_elements(file_data["Num of subscriptions"], length=2)
        def Subscription_Names(self):
            return self.random_elements(file_data["Subscription Names"], length=2)
        def Firewalls(self):
            return self.random_elements(file_data["Firewalls"], length=2)
        def Archival_Storage_Accounts(self):
            return self.random_elements(file_data["Archival_Storage_Accounts"], length=2)
        def Firewall_Management(self):
            return self.random_elements(file_data["Firewall_Management"], length=2)
        def Platform_Services(self):
            return self.random_elements(file_data["Platform_Services"], length=2)
        def Critical_Systems(self):
            return self.random_elements(file_data["Critical_Systems"], length=2)
        def Compliance_Regulatory_Requirements(self):
            return self.random_elements(file_data["Compliance_Regulatory_Requirements"], length=2)
        def Networking_Requirements(self):
            return self.random_elements(file_data["Networking_Requirements"], length=2)
        def Num_of_Servers(self):
            return self.random_elements(file_data["# of Servers"], length=2)
        def Server_Type(self):
            return self.random_elements(file_data["Server_Type"], length=2)
        def Switches(self):
            return self.random_elements(file_data["Switches"], length=2)
        def Routers(self):
            return self.random_elements(file_data["Routers"], length=2)
        def Storage_Devices(self):
            return self.random_elements(file_data["Storage_Devices"], length=2)
        def DNS(self):
            return self.random_elements(file_data["DNS"], length=2)
        def DHCP(self):
            return self.random_elements(file_data["DHCP"], length=2)
        def Default_Gateway(self):
            return self.random_elements(file_data["Default_Gateway"], length=2)
        def DNS_Server(self):
            return self.random_elements(file_data["DNS_Server"], length=2)
        def Active_Directory(self):
            return self.random_elements(file_data["Active_Directory"], length=2)
        def AD_Domain_Controllers(self):
            return self.random_elements(file_data["AD_-_Domain_Controllers"], length=2)
        def AD_Organizational_Units(self):
            return self.random_elements(file_data["AD_-_Organizational_Units"], length=2)
        def Bandwidth(self):
            return self.random_elements(file_data["Bandwidth"], length=2)
        def Latency(self):
            return self.random_elements(file_data["Latency"], length=2)
        def Num_of_Users(self):
            return self.random_elements(file_data["# of Users"], length=2)
        def Num_of_Systems(self):
            return self.random_elements(file_data["# of Systems"], length=2)
        def Backup_Storage_Solution(self):
            return self.random_elements(file_data["Backup_Storage_Solution"], length=2)
        def User_Roles_with_IRE_Access(self):
            return self.random_elements(file_data["User_Roles_with_IRE_Access"], length=2)
        def User_Authentication(self):
            return self.random_elements(file_data["User_Authentication"], length=2)
        def User_Authorization(self):
            return self.random_elements(file_data["User_Authorization"], length=2)
        def Backup_Products(self):
            return self.random_elements(file_data["Backup_Products"], length=2)
        def Num_of_Backup_Environments(self):
            return self.random_elements(file_data["#_of_Backup_Environments"], length=2)
        def Technologies_to_Be_Placed_in_Vault(self):
            return self.random_elements(file_data["Technologies_to_Be_Placed_in_Vault"], length=2)
        def Azure_Blob(self):
            return self.random_elements(file_data["Azure_Blob?"], length=2)
        def Traffic_Allowed_Out(self):
            return self.random_elements(file_data["Traffic_Allowed_Out"], length=2)
        def SIEM_Tool(self):
            return self.random_elements(file_data["SIEM_Tool"], length=2)

    fake.add_provider(SkillsProvider)

    output = []
    for _ in range(num_profiles):
        profile = {
            "Network_Model": fake.Network_Model(),
            "Cloud_Environment": fake.Cloud_Environment(),
            "Num_of_subscriptions": fake.Num_of_subscriptions(),
            "Subscription_Names": fake.Subscription_Names(),
            "Firewalls": fake.Firewalls(),
            "Archival_Storage_Accounts": fake.Archival_Storage_Accounts(),
            "Firewall_Management": fake.Firewall_Management(),
            "Platform_Services": fake.Platform_Services(),
            "Critical_Systems": fake.Critical_Systems(),
            "Compliance_Regulatory_Requirements": fake.Compliance_Regulatory_Requirements(),
            "Networking_Requirements": fake.Networking_Requirements(),
            "Num_of_Servers": fake.Num_of_Servers(),
            "Server_Type": fake.Server_Type(),
            "Switches": fake.Switches(),
            "Routers": fake.Routers(),
            "Storage_Devices": fake.Storage_Devices(),
            "DNS": fake.DNS(),
            "DHCP": fake.DHCP(),
            "Default_Gateway": fake.Default_Gateway(),
            "DNS_Server": fake.DNS_Server(),
            "Active_Directory": fake.Active_Directory(),
            "AD_Domain_Controllers": fake.AD_Domain_Controllers(),
            "AD_Organizational_Units": fake.AD_Organizational_Units(),
            "Bandwidth": fake.Bandwidth(),
            "Latency": fake.Latency(),
            "Num_of_Users": fake.Num_of_Users(),
            "Num_of_Systems": fake.Num_of_Systems(),
            "Backup_Storage_Solution": fake.Backup_Storage_Solution(),
            "User_Roles_with_IRE_Access": fake.User_Roles_with_IRE_Access(),
            "User_Authentication": fake.User_Authentication(),
            "User_Authorization": fake.User_Authorization(),
            "Backup_Products": fake.Backup_Products(),
            "Num_of_Backup_Environments": fake.Num_of_Backup_Environments(),
            "Technologies_to_Be_Placed_in_Vault": fake.Technologies_to_Be_Placed_in_Vault(),
            "Azure_Blob": fake.Azure_Blob(),
            "Traffic_Allowed_Out": fake.Traffic_Allowed_Out(),
            "SIEM_Tool": fake.SIEM_Tool(),
        }
        output.append(profile)

    with open(output_file, "w") as f:
        json.dump(output, f, indent=4)
    
    return output

#############################
# 2) TRANSFORM FOR TABLE
#############################
def transform_data_for_table(data):
    """
    Splits each list of length 2 into two separate columns: <key>_before, <key>_after
    """
    new_data = []
    for row in data:
        transformed_row = {}
        for k, v in row.items():
            if isinstance(v, list) and len(v) == 2:
                transformed_row[f"{k}_before"] = v[0]
                transformed_row[f"{k}_after"] = v[1]
            else:
                transformed_row[k] = v
        new_data.append(transformed_row)
    return new_data

#############################
# 3) CLASSIFY + BUILD DIAGRAM
#############################
def classify_resource(key):
    """
    Classify resource key into a subscription/mgmt group.
    """
    lower_key = key.lower()
    if "firewall" in lower_key or "router" in lower_key or "dns" in lower_key:
        return "Connectivity"
    elif "backup" in lower_key or "recovery" in lower_key or "vault" in lower_key:
        return "AppRecovery"
    else:
        return "Foundation"

def build_landing_zone_diagram(profile):
    """
    Creates an Landing Zone–style diagram:
      - Root tenant with Platform Management and App Recovery management groups.
      - Platform MG has Foundation & Connectivity subscriptions.
      - App Recovery MG has an Application Recovery subscription.
    Places each resource from 'profile' into the appropriate subscription subgraph.
    """
    g = graphviz.Digraph(format="png", engine="dot")
    g.attr(rankdir="LR", splines="true", nodesep="1.5", ranksep="2.0")

    # Create subgraphs and capture references in a dictionary
    subgraphs = {}

    # Root tenant subgraph
    with g.subgraph(name="cluster_root_tenant") as root:
        root.attr(label="Tenant (Root)", style="dashed", color="gray")
        
        # Platform Management Group
        with root.subgraph(name="cluster_platform_mg") as mg_platform:
            mg_platform.attr(
                label="Platform Management Group",
                style="filled",
                color="black",
                fillcolor="#E8F4FA"
            )
            # Foundation subscription subgraph
            with mg_platform.subgraph(name="cluster_foundation_sub") as sub_foundation:
                sub_foundation.attr(
                    label="Subscription: Foundation",
                    style="filled",
                    color="blue",
                    fillcolor="#F0F8FF"
                )
                subgraphs["Foundation"] = sub_foundation  # store reference

            # Connectivity subscription subgraph
            with mg_platform.subgraph(name="cluster_connectivity_sub") as sub_connect:
                sub_connect.attr(
                    label="Subscription: Connectivity",
                    style="filled",
                    color="blue",
                    fillcolor="#F0F8FF"
                )
                subgraphs["Connectivity"] = sub_connect  # store reference

        # App Recovery Management Group
        with root.subgraph(name="cluster_apprecovery_mg") as mg_apprec:
            mg_apprec.attr(
                label="App Recovery Mgmt Group",
                style="filled",
                color="black",
                fillcolor="#FFE5E5"
            )
            # Application Recovery subscription subgraph
            with mg_apprec.subgraph(name="cluster_apprec_sub") as sub_apprec:
                sub_apprec.attr(
                    label="Subscription: Application Recovery",
                    style="filled",
                    color="red",
                    fillcolor="#FFE5E5"
                )
                subgraphs["AppRecovery"] = sub_apprec  # store reference

    # Add resources to appropriate subgraph based on classification.
    for key, val in profile.items():
        if isinstance(val, list) and len(val) == 2:
            label = f"{key}\n(before: {val[0]})\n(after: {val[1]})"
        else:
            label = f"{key}\n({val})"
        subscription = classify_resource(key)  # "Foundation", "Connectivity", or "AppRecovery"
        node_id = f"{subscription}_{key}"
        if subscription in subgraphs:
            subgraphs[subscription].node(
                node_id,
                label=label,
                shape="box",
                style="filled",
                fillcolor="white",
                color="black",
                fontcolor="black"
            )

    # Example edges (ensure node IDs match generated nodes)
    g.edge("Foundation_Firewall_Management", "Connectivity_Firewalls", label="Manages")
    g.edge("Foundation_Storage_Devices", "AppRecovery_Backup_Products", label="Backups")
    g.edge("Connectivity_Routers", "Foundation_Default_Gateway", label="Routing")

    return g

#############################
# 4) STREAMLIT APP
#############################
def main():
    st.title("Landing Zone–Style Generator & Diagram")

    # Use session state to store data
    if "data" not in st.session_state:
        st.session_state["data"] = None

    st.markdown("### 1) Generate or Load Data")
    generate_new = st.checkbox("Generate new data?", value=True)
    num_profiles = st.number_input("Number of Profiles", min_value=1, value=8)
    parameters_file = st.text_input("Parameters File Path", "./data/parameters.json")
    output_file = st.text_input("Output File Path", "./data/sampleDataTest.json")

    if generate_new:
        if st.button("Generate Data Now"):
            data = generate_sample_data(num_profiles, parameters_file, output_file)
            st.session_state["data"] = data
            st.success(f"{num_profiles} profiles generated and saved to {output_file}")
    else:
        st.write("Using existing data if available (uncheck to generate).")

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
        st.subheader("Sample Data Table (Before/After)")
        transformed = transform_data_for_table(st.session_state["data"])
        df = pd.DataFrame(transformed)
        st.dataframe(df)
    else:
        st.info("No data to display yet. Generate or load data first.")
        return

    st.markdown("### 2) Build Landing Zone Diagram")
    if st.button("Build Diagram"):
        # Use the first profile
        profile = st.session_state["data"][0]
        diagram = build_landing_zone_diagram(profile)
        st.graphviz_chart(diagram)
        diagram.render("landing_zone", cleanup=True)
        png_file = "landing_zone.png"
        if os.path.exists(png_file):
            with open(png_file, "rb") as f:
                st.download_button(
                    label="💾 Download Diagram (PNG)",
                    data=f,
                    file_name="landing_zone.png",
                    mime="image/png"
                )
            st.success(f"Diagram generated and saved as {png_file}")
        else:
            st.error("Could not find the diagram file!")

if __name__ == "__main__":
    main()