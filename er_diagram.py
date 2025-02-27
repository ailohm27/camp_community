import json
import argparse

from faker import Faker
from faker.providers import BaseProvider, DynamicProvider
from rich.console import Console


if __name__ == "__main__":
    console = Console()
    

    console.print(f"""
SAMPLE DATA GENERATOR
        """, style="bold green")
    
   
    kval = 8
    
    console.print(f"Generating {kval} consultant profiles", style="green")

    fake = Faker('en_US')

    with open("./data/base_skills.json", 'r') as f:
        file_data = json.load(f)

    
    class SkillsProvider(BaseProvider):
        def mechanism(self, lengthSet):
            return self.random_elements(file_data["mechanism"], length=lengthSet)
        
        def directionality(self, lengthSet):
            return self.random_elements(file_data["directionality"], length=lengthSet)
        
    fake.add_provider(SkillsProvider)
    
    output = []
    for _ in range(5):
        appRelations = fake.random_int(min=1,max=8)
        appNameList = []
        topicList = []
        for _ in range(appRelations):
            appNameList.append("AppName-" + str(fake.random_int(min=0, max=100))+ "")
            topicList.append(fake.unique.word())
        obj = {
            "appName1": "AppName-" + str(fake.random_int(min=0, max=100))+ "",
            "appName2": appNameList,
            "directionality": fake.directionality(appRelations),
            "mechanism": fake.mechanism(appRelations),
            "topic" : topicList,
        }
        output.append(obj)

    console.print(f"Consultant profiles generated. Writing to consultant_profiles", style="green")
    json.dump(output, open("./data/consultant_profiles.json", "w"), indent=4)

import pandas as pd
import numpy as np
import os
import json

if __name__ == "__main__":
    # Load the data
    with open("./data/consultant_profiles.json", 'r') as f:
        data = json.load(f)
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    dfToFill = pd.DataFrame(columns=['appName1', 'appName2', 'directionality', 'mechanism','topic'])
    incrementer = 0
    for i, row in df.iterrows():
        for j in range(len(row['appName2'])):
            dfToFill.at[incrementer, 'appName1'] = row['appName1']
            dfToFill.at[incrementer, 'appName2'] = row['appName2'][j]
            dfToFill.at[incrementer, 'directionality'] = row['directionality'][j]
            dfToFill.at[incrementer, 'mechanism'] = row['mechanism'][j]
            dfToFill.at[incrementer, 'topic'] = row['topic'][j]
            incrementer += 1
    
    print(dfToFill)
 
 #
from graphviz import Digraph



# Prompt user for application to map
app_to_map = "all"

# Initialize a directed graph with additional attributes
graph_format = 'svg' 
g = Digraph(format=graph_format, engine='circo', strict=True) # dot, neato, fdp, sfdp, circo, twopi, nop, nop2, osage, patchwork
g.attr(compound='true', style='filled', color='deepskyblue', fillcolor='lightskyblue')

# Filter the data to include only relevant rows or "all" for all applications
if app_to_map == "all":
    filtered_df = dfToFill
    app_shape = 'circle'
else:
    filtered_df = df[(df['App-1'] == app_to_map) | (df['App-2'] == app_to_map)]
    app_shape = 'box'
    g.node(app_to_map, label=app_to_map, shape=f'{app_shape}', color='deepskyblue', fillcolor='lightskyblue')

def get_label(row):
    #Generate label for edges using the topic, or blank if NaN.
    return f"{row['topic']}" if pd.notna(row['topic']) else ""

# Define colors for mechanisms
mechanism_colors = {
    "fileShare": "blue",
    "ftp": "red",
    "api": "green",
    "emails": "grey",
    "autosys": "orange",
    "service bus": "purple",
    "batch updates": "brown"
}

mechanism_arrow = {
    "fileShare":"odot",
    "ftp":"box",
    "api":"diamond",
    "emails":"vee",
    "autosys":"tee",
    "service bus":"crow",
    "batch updates":"normal"
}

# Add edges within a subgraph for better organization
with g.subgraph(name="cluster00") as relationships:
    relationships.attr(label="Application Relationships", style="dashed")
    for _, row in filtered_df.iterrows():
        style = "solid"
        arrowhead = "normal"
        arrowtail = "normal"
        direction = "forward"
        
        direction_type = str(row['directionality']).strip().lower() if pd.notna(row['directionality']) else ""
        mechanism_type = str(row['mechanism']).strip().lower() if pd.notna(row['mechanism']) else ""
        
        color = mechanism_colors.get(mechanism_type, "black")  # Default to black if no match
        arrowhead = mechanism_arrow.get(mechanism_type, "normal")  # Default to black if no match

                
        if direction_type == "bi-directional":
            style = "bold"
            direction = "both"
            arrowtail=arrowhead
        elif direction_type == "depends on":
            style = "dashed"
            
        relationships.edge(row['appName1'], row['appName2'], label=get_label(row), style=style, arrowhead=arrowhead, arrowtail=arrowtail, dir=direction, color=color)

# Add a properly structured subgraph for Legend and Mechanism at the bottom

'''
with g.subgraph(name="cluster01") as legend:
    legend.attr(label="Legend", style="dashed")
    legend.node("Legend", shape="box")
    legend.edge("Legend", "Bi-Directional", label="Double Arrow", style="bold", dir="both")
    legend.edge("Legend", "Depends On", label="Dashed Line", style="dashed")
    legend.edge("Legend", "Normal Flow", label="Solid Line", style="solid")
'''
# with g.subgraph(name="cluster02") as invi:
#     invi.attr(color=invis, style=invis)
#     invi.node("Invisible", shape="point", color=invis, style=invis)
   
with g.subgraph(name="cluster03") as mechan:
    mechan.attr(label="Mechanism", style="dashed")
    mechan.node("Mechanism", shape="box")
    mechan.edge("Mechanism", "API", label="Green Diamond", arrowhead="diamond", color="green")
    mechan.edge("Mechanism", "FTP", label="Red Box", arrowhead="box", color="red", shape="box")
    mechan.edge("Mechanism", "Fileshare", label="Blue Circle", arrowhead="odot", color="blue")
    mechan.edge("Mechanism", "Emails", label="Grey Vee", arrowhead="vee", color="grey")
    mechan.edge("Mechanism", "Autosys", label="Orange Tee", arrowhead="tee", color="orange")
    mechan.edge("Mechanism", "Service Bus", label="Purple Crow", arrowhead="crow", color="purple")
    mechan.edge("Mechanism", "Batch Updates", label="Brown Normal", arrowhead="normal", color="brown")

# Save and render the graph
g.render("relationship_map")

print(f"Graph generated as relationship_map.{graph_format}")