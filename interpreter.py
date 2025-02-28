import networkx as nx
import matplotlib.pyplot as plt
from parser import parser
import plotly.graph_objects as go

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
        node1 = ast[1]
        node2 = ast[2]
        graph_name = ast[3]
        if graph_name in graph_store:
            graph_store[graph_name].add_edge(node1, node2)
            print(f"Added edge {node1} -> {node2} in graph {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")

    elif command == 'color_node':
        node_name = ast[1]
        color = ast[2].strip('"')

        for graph_name, graph in graph_store.items():
            if node_name in graph:
                if graph_name not in node_colors:
                    node_colors[graph_name] = {}
                node_colors[graph_name][node_name] = color
                print(f"Colored node {node_name} with {color}")
                break
        else:
            print(f"Error: Node {node_name} not found in any graph")

    elif command == 'color_edge':
        node1 = ast[1]
        node2 = ast[2]
        color = ast[3].strip('"')

        for graph_name, graph in graph_store.items():
            if graph.has_edge(node1, node2):
                if graph_name not in edge_colors:
                    edge_colors[graph_name] = {}
                edge_colors[graph_name][(node1, node2)] = color
                print(f"Colored edge {node1} -> {node2} with {color}")
                break
        else:
            print(f"Error: Edge {node1} -> {node2} not found in any graph")

    elif command == 'find_cycle':
        graph_name = ast[1]
        if graph_name in graph_store:
            try:
                cycle = list(nx.find_cycle(graph_store[graph_name], orientation='ignore'))
                print(f"Cycle found in {graph_name}: {cycle}")
            except nx.NetworkXNoCycle:
                print(f"No cycle found in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")

    elif command == 'shortest_path':
        node1 = ast[1]
        node2 = ast[2]
        graph_name = ast[3]

        if graph_name in graph_store:
            graph = graph_store[graph_name]

            if node1 in graph and node2 in graph:
                try:
                    path = nx.shortest_path(graph, source=node1, target=node2, method="dijkstra")
                    print(f"Shortest path from {node1} to {node2} in {graph_name}: {path}")
                except nx.NetworkXNoPath:
                    print(f"No path found between {node1} and {node2} in {graph_name}")
            else:
                print(f"Error: One or both nodes do not exist in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")
    
    elif command == 'visualize':
        graph_name = ast[1]
        visualize_animated(graph_name)

    
    if graph_name in graph_store:
        graph = graph_store[graph_name]

        # Vælg et layout
        layout_choice = 'spring'  # Muligheder: 'spring', 'circular', 'kamada_kawai'

        if layout_choice == 'spring':
            pos = nx.spring_layout(graph, seed=42)  
        elif layout_choice == 'circular':
            pos = nx.circular_layout(graph)  
        elif layout_choice == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(graph)

        # Brug gemte farver eller standardfarver
        node_color_list = [node_colors.get(graph_name, {}).get(node, 'lightblue') for node in graph.nodes()]
        edge_color_list = [edge_colors.get(graph_name, {}).get((u, v), 'gray') for u, v in graph.edges()]
        
        # Find vægte på kanter (hvis de findes)
        edge_labels = {(u, v): graph[u][v].get('weight', '') for u, v in graph.edges()}

        # Bestem kanttykkelse baseret på vægt (standard = 1)
        edge_widths = [graph[u][v].get('weight', 1) for u, v in graph.edges()]

        # Opret figuren
        plt.figure(figsize=(10, 8))

        # Tegn grafen med dynamiske farver og tykkelse
        nx.draw(
            graph, pos, 
            with_labels=True, 
            node_color=node_color_list, 
            edge_color=edge_color_list,
            node_size=1500,  
            font_size=12,  
            width=edge_widths,  
            edge_cmap=plt.cm.Blues
        )

        # Tilføj vægt-labels på kanterne
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')

        plt.title(f"Visualization of Graph: {graph_name}")
        plt.show()
    
    else:
        print(f"Error: Graph {graph_name} does not exist")
    
import time
import matplotlib.animation as animation

def visualize_animated(graph_name):
    if graph_name not in graph_store:
        print(f"Error: Graph {graph_name} does not exist")
        return

    graph = graph_store[graph_name]
    pos = nx.spring_layout(graph, seed=42)
    edges = list(graph.edges())

    fig, ax = plt.subplots(figsize=(10, 8))

    def update(i):
        ax.clear()
        subgraph = graph.edge_subgraph(edges[:i+1])
        nx.draw(subgraph, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=1000, ax=ax)
        ax.set_title(f"Step {i+1}: Adding edge {edges[i][0]} -> {edges[i][1]}")

    ani = animation.FuncAnimation(fig, update, frames=len(edges), interval=100, repeat=False)
    plt.show()  # Nu kører animationen uden blokering


    plt.ioff()  # 🔥 Slå interaktiv tilstand fra, når animationen er færdig
    #plt.show()  # Afslut med en endelig visualisering


def run_gml(code):
    lines = code.strip().split("\n")
    for line in lines:
        ast = parser.parse(line)
        execute(ast)