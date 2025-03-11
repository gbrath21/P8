import os
import pickle
import webbrowser
import networkx as nx
import plotly.graph_objects as go
import plotly.io as pio
from parser import parser

# Gemmer alle grafer
graph_store = {}

def execute(ast):
    if ast is None:
        return

    command = ast[0]

    if command == 'graph':
        graph_name = ast[1]
        graph_store[graph_name] = nx.Graph()
        print(f"Created graph: {graph_name}")

    elif command == 'directed_graph':
        graph_name = ast[1]
        graph_store[graph_name] = nx.DiGraph()
        print(f"Created directed graph: {graph_name}")

    elif command == 'node':
        node_name, graph_name = ast[1], ast[2]
        if graph_name in graph_store:
            graph_store[graph_name].add_node(node_name)
            print(f"Added node {node_name} to graph {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")

    elif command == 'edge':
        # ast: ('edge', node1, node2, graph_name, weight)
        node1, node2, graph_name, weight = ast[1], ast[2], ast[3], int(ast[4]) if len(ast) > 4 else 0
        if graph_name in graph_store:
            graph = graph_store[graph_name]
            print(f"Graph type: {type(graph)}")  # Debugging line
            if node1 in graph and node2 in graph:
                graph.add_edge(node1, node2, weight=weight)
                print(f"Added edge {node1} -> {node2} (weight: {weight}) in graph {graph_name}")
            else: 
                print(f"Error: One or both nodes ({node1}, {node2}) do not exist in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")

    elif command == 'find_cycle':
        graph_name = ast[1]
        if graph_name in graph_store:
            try:
                cycle = list(nx.find_cycle(graph_store[graph_name], orientation='ignore'))
                print(f"Cycle found in {graph_name}: {cycle}")
                visualize_interactive(graph_name, cycle=cycle)
            except nx.NetworkXNoCycle:
                print(f"No cycle found in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")

    elif command == 'shortest_path':
        node1, node2, graph_name = ast[1], ast[2], ast[3]
        if graph_name in graph_store:
            graph = graph_store[graph_name]
            if node1 in graph and node2 in graph:
                try:
                    if any("weight" in graph[u][v] for u, v in graph.edges()):
                        path = nx.shortest_path(graph, source=node1, target=node2, weight="weight", method="dijkstra")
                    else:
                        path = nx.shortest_path(graph, source=node1, target=node2, method="unweighted")
                    print(f"Shortest path from {node1} to {node2} in {graph_name}: {path}")
                    visualize_interactive(graph_name, path=path)
                except nx.NetworkXNoPath:
                    print(f"No path found between {node1} and {node2} in {graph_name}")
            else:
                print(f"Error: One or both nodes do not exist in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")
            
    elif command == 'delete1_node':
        node_name, graph_name = ast[1], ast[2]
    
        if graph_name in graph_store:
            graph = graph_store[graph_name]
        
            if node_name in graph:
                print(f"Deleting node {node_name} from {graph_name}...")  # Debugging
                graph.remove_node(node_name)
                print(f"Node {node_name} deleted from {graph_name}.")
                print(f"Remaining nodes: {list(graph.nodes())}")
                print(f"Remaining edges: {list(graph.edges())}")
            else:
                print(f"Error: Node {node_name} does not exist in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")

    elif command == 'visualize':
        graph_name = ast[1]
        if graph_name in graph_store:
            visualize_interactive(graph_name)
        else:
            print(f"Error: Graph {graph_name} does not exist")

def visualize_interactive(graph_name, path=None, cycle=None):
    """Vis den opdaterede graf i Plotly med mulighed for at fremhæve shortest path og cycles."""
    if graph_name not in graph_store:
        print(f"Error: Graph {graph_name} does not exist")
        return

    graph = graph_store[graph_name]
    pos = nx.spring_layout(graph, seed=42)

    edge_x, edge_y = [], []
    cycle_edge_x, cycle_edge_y = [], []
    path_edge_x, path_edge_y = [], []
    edge_labels = {}

    cycle_edges = set((u, v) for u, v, *_ in cycle) if cycle else set()
    path_edges = set(zip(path, path[1:])) if path else set()

    for u, v, data in graph.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        weight = str(data.get("weight", 1))
        edge_labels[(u, v)] = weight

        if (u, v) in cycle_edges or (v, u) in cycle_edges:
            cycle_edge_x.extend([x0, x1, None])
            cycle_edge_y.extend([y0, y1, None])
        elif (u, v) in path_edges or (v, u) in path_edges:
            path_edge_x.extend([x0, x1, None])
            path_edge_y.extend([y0, y1, None])
        else:
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

    node_x, node_y, node_text, node_colors = [], [], [], []
    cycle_nodes = {node for u, v in cycle_edges for node in (u, v)}
    path_nodes = set(path) if path else set()

    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        if node in cycle_nodes:
            node_colors.append("red")
        elif node in path_nodes:
            node_colors.append("green")
        else:
            node_colors.append("blue")

    is_directed = isinstance(graph, nx.DiGraph)

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines',
                            line=dict(width=2, color="gray"), hoverinfo='none')
    cycle_edge_trace = go.Scatter(x=cycle_edge_x, y=cycle_edge_y, mode='lines',
                                  line=dict(width=2, color="red"), hoverinfo='none')
    path_trace = go.Scatter(x=path_edge_x, y=path_edge_y, mode='lines',
                            line=dict(width=3, color="green"), hoverinfo='none')
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text,
                            textposition="top center",
                            marker=dict(size=12, color=node_colors, line=dict(width=2)))

    fig = go.Figure(data=[edge_trace, cycle_edge_trace, path_trace, node_trace])

    # Tilføj vægte på edges
    for (u, v), weight in edge_labels.items():
        x_mid = (pos[u][0] + pos[v][0]) / 2
        y_mid = (pos[u][1] + pos[v][1]) / 2
        fig.add_annotation(x=x_mid, y=y_mid, text=weight, showarrow=False,
                           font=dict(color="black", size=14))

    # Hvis grafen er directed, tilføj pile manuelt
    if is_directed:
        for u, v in graph.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            fig.add_annotation(
                ax=x0, ay=y0, x=x1, y=y1,
                xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=5, arrowsize=2, arrowcolor="black"
            )

    # Hent eksisterende annotations (pil- og vægt-annotations) og tilføj legend-annotation
    existing_annotations = list(fig.layout.annotations) if fig.layout.annotations is not None else []
    legend_annotation = dict(
        text="<span style='color:blue; font-weight:bold;'>Blue</span>: Standard nodes &nbsp;&nbsp;"
             "<span style='color:green; font-weight:bold;'>Green</span>: Shortest path &nbsp;&nbsp;"
             "<span style='color:red; font-weight:bold;'>Red</span>: Cycles",
        showarrow=False,
        xref="paper", yref="paper",
        x=0.5,
        y=-0.05,
        yanchor="top",
        font=dict(
            family="Trebuchet MS",
            size=12,
            color="black"
        ),
        align="center",
    )
    existing_annotations.append(legend_annotation)

    fig.update_layout(
        title={"text": f"<span style='font-family:Trebuchet MS; color:black; font-size:20px;'>Visualization of Graph: {graph_name}</span>"},
        showlegend=False,
        annotations=existing_annotations
    )

    filename = os.path.abspath("graph_visualization.html")
    pio.write_html(fig, filename)

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