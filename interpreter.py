import networkx as nx
import matplotlib.pyplot as plt
from parser import parser
import plotly.graph_objects as go
import random
import time
import matplotlib.animation as animation
import plotly.io as pio
import webbrowser
import os 

# Gemmer alle grafer og farver
graph_store = {}
node_colors = {}
edge_colors = {}

def execute(ast):
    if ast is None:
        return
    
    command = ast[0]

    if command == 'graph':
        graph_name = ast[1]
        graph_store[graph_name] = nx.Graph()
        print(f"Created graph: {graph_name}")

    elif command == 'node':
        node_name = ast[1]
        graph_name = ast[2]
        if graph_name in graph_store:
            graph_store[graph_name].add_node(node_name)
            print(f"Added node {node_name} to graph {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")

    elif command == 'edge':
        node1, node2, graph_name, weight = ast[1], ast[2], ast[3], ast[4] if len(ast) > 4 else 1

        if graph_name in graph_store:
            graph_store[graph_name].add_edge(node1, node2, weight=int(weight))  # Sørger for at gemme vægten som int
            print(f"Added edge {node1} -> {node2} (weight: {weight}) in graph {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")

    elif command == 'find_mst':
        graph_name = ast[1]
        if graph_name in graph_store:
            mst = nx.minimum_spanning_tree(graph_store[graph_name])
            print(f"Minimum Spanning Tree for {graph_name}: {list(mst.edges())}")
        else:
            print(f"Error: Graph {graph_name} does not exist")

    elif command == 'delete_node':
        node_name, graph_name = ast[1], ast[2]
        if graph_name in graph_store and node_name in graph_store[graph_name]:
            graph_store[graph_name].remove_node(node_name)
            print(f"Deleted node {node_name} from graph {graph_name}")
            print(f"Remaining nodes after deletion: {list(graph_store[graph_name].nodes())}")
        else:
            print(f" Error: Node {node_name} does not exist in {graph_name}")

    elif command == 'delete_edge':
        node1, node2, graph_name = ast[1], ast[2], ast[3]
        if graph_name in graph_store and graph_store[graph_name].has_edge(node1, node2):
            graph_store[graph_name].remove_edge(node1, node2)
            print(f"Deleted edge {node1} -> {node2} from graph {graph_name}")
            print(f"Remaining edges after deletion: {list(graph_store[graph_name].edges())}")
        else:
            print(f"Error: Edge {node1} -> {node2} does not exist in {graph_name}")
            
    elif command == 'directed_graph':
        graph_name = ast[1]
        graph_store[graph_name] = nx.DiGraph()  # Brug en rettet graf
        print(f"Created directed graph: {graph_name}")

    elif command == 'visualize':
        graph_name = ast[1]
        visualize_interactive(graph_name)

import plotly.io as pio
import webbrowser
import os

def visualize_interactive(graph_name):
    """Vis den opdaterede graf interaktivt i Plotly."""
    if graph_name not in graph_store:
        print(f"Error: Graph {graph_name} does not exist")
        return

    graph = graph_store[graph_name]
    pos = nx.spring_layout(graph, seed=42)

    edge_x, edge_y = [], []
    edge_labels = {}
    for u, v, data in graph.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_labels[(u, v)] = str(data.get("weight", 1))  # Konverterer vægten til string for visning

    node_x, node_y, node_text = [], [], []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=2, color='gray'), hoverinfo='none')
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text, textposition="top center",
                            marker=dict(size=12, color='blue', line=dict(width=2)))

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title=f"Visualization of Graph: {graph_name}", showlegend=False)

    # Tilføj labels for kantvægtene
    for (u, v), weight in edge_labels.items():
        x_mid = (pos[u][0] + pos[v][0]) / 2
        y_mid = (pos[u][1] + pos[v][1]) / 2
        fig.add_annotation(x=x_mid, y=y_mid, text=weight, showarrow=False, font=dict(color="red", size=14))

    # Opret en filsti
    filename = os.path.abspath("graph_visualization.html")
    pio.write_html(fig, filename)

    # Åben browser
    try:
        webbrowser.open(f"file://{filename}", new=2)
        print(f"Graph visualization opened in browser: {filename}")
    except Exception as e:
        print(f"Could not open browser: {e}")

def run_gml(code):
    lines = code.strip().split("\n")
    for line in lines:
        ast = parser.parse(line)
        execute(ast)