import os
import pickle
import webbrowser
import networkx as nx
import plotly.graph_objects as go
import plotly.io as pio
from parser import parser
import numpy as np

# Gemmer alle grafer
graph_store = {}

visualize_called = False  # Global variabel til at tracke visualize

# Gemmer alle grafer
graph_store = {}

visualize_called = False  # Global variabel til at tracke visualize
pending_cycles = {}  # Holder cyklusser for grafer
pending_paths = {}   # Holder korteste stier for grafer
pending_msts = {} 
pending_closures = {}

def execute(ast):
    global visualize_called, pending_cycles, pending_paths, pending_msts, pending_closures
    
    if ast is None:
        return

    command = ast[0]
    
    if visualize_called:
        print("Warning: No commands should be executed after 'visualize'. Ignoring input.")
        return  # Stop al eksekvering efter visualize
    
    if command == 'visualize':
        visualize_called = True  # Marker at visualize er kaldt
        graph_names = ast[1] if isinstance(ast[1], list) else [ast[1]]
        
        for graph_name in graph_names:
            if graph_name in graph_store:
                cycle = pending_cycles.pop(graph_name, None)  # Hent og fjern cyklus fra pending
                path = pending_paths.pop(graph_name, None)  # Hent og fjern path fra pending
                mst = pending_msts.pop(graph_name, None)
                visualize_interactive(graph_name, path=path, cycle=cycle, mst=mst)
            else:
                print(f"Error: Graph {graph_name} does not exist")
                
    # Create graph
    elif command == 'graph':
        graph_name = ast[1]
        graph_store[graph_name] = nx.Graph()
        print(f"Created graph: {graph_name}")

    # Directed or undirected graph
    elif command == 'directed_graph':
        graph_name = ast[1]
        graph_store[graph_name] = nx.DiGraph()
        print(f"Created directed graph: {graph_name}")

    # Create node
    elif command == 'node':
        node_name, graph_name = ast[1], ast[2]
        if graph_name in graph_store:
            graph_store[graph_name].add_node(node_name)
            print(f"Added node {node_name} to graph {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")

    #Create edge
    elif command == 'edge':
        node1, node2, graph_name, weight = ast[1], ast[2], ast[3], int(ast[4]) if len(ast) > 4 else 0
        if graph_name in graph_store:
            graph = graph_store[graph_name]
            if node1 in graph and node2 in graph:
                graph.add_edge(node1, node2, weight=weight)
                print(f"Added edge {node1} -> {node2} (weight: {weight}) in graph {graph_name}")
            else: 
                print(f"Error: One or both nodes ({node1}, {node2}) do not exist in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")
    
    #Find cycle
    elif command == 'find_cycle':
        graph_name = ast[1]
        if graph_name in graph_store:
            try:
                cycle = list(nx.find_cycle(graph_store[graph_name], orientation='original'))
                pending_cycles[graph_name] = cycle  # Gem cyklus til visualize
                print(f"Cycle found in {graph_name}: {cycle}")
            except nx.NetworkXNoCycle:
                print(f"No cycle found in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")
    
    # Find shortest path
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
                    pending_paths[graph_name] = path  # Gem path til visualize
                    print(f"Shortest path from {node1} to {node2} in {graph_name}: {path}")
                except nx.NetworkXNoPath:
                    print(f"No path found between {node1} and {node2} in {graph_name}")
            else: 
                print(f"Error: One or both nodes do not exist in {graph_name}")
        else: 
            print(f"Error: Graph {graph_name} does not exist")
    
    #Find mst
    elif command == 'find_mst':
        graph_name = ast[1]
        if graph_name in graph_store:
            graph = graph_store[graph_name]
            if isinstance(graph, nx.DiGraph):
                print(f"Error: MST can only be found for undirected graphs (Graph {graph_name} is directed)")
            else:
                mst = nx.minimum_spanning_tree(graph, weight="weight")
                pending_msts[graph_name] = mst.edges(data=True)
                print(f"MST found for {graph_name}: {list(mst.edges(data=True))}")
        else:
            print(f"Error: Graph {graph_name} does not exist")

    # Delete a node in the graph
    elif command == 'delete1_node':
        node_name, graph_name = ast[1], ast[2]
    
        if graph_name in graph_store:
            graph = graph_store[graph_name]
        
            if node_name in graph:
                graph.remove_node(node_name)
                print(f"Node {node_name} deleted from {graph_name}.")
            else:
                print(f"Error: Node {node_name} does not exist in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")

    # If statements 
    elif command == 'if_node':
        node, graph_name, then_stmt = ast[1], ast[2], ast[3]
        if graph_name in graph_store and node in graph_store[graph_name]:
            execute(then_stmt)
            
    elif command == 'if_edge':
        node, graph_name, then_stmt = ast[1], ast[2], ast[3], ast[4]
        graph = graph_store.get(graph_name)
        if graph and graph.has_edge(node1, node2):
            exectute(then.stmt)
            
    elif command == 'if_path':
        node1, node2, graph_name, then_stmt = ast[1], ast[2], ast[3], ast[4]
        graph = graph_store.get(graph_name)
        if graph:
            try:
                nx.shortest_path(graph, source=node1, target=node2)
                executre(then.stmt)
            except nx.NetworkXNoPath:
                pass
    
    elif command == 'if_cycle':
        graph_name, then_stmt = ast[1], ast[2]
        graph = graph_store.get(graph_name)
        if graph:
            try:
                nx.find_cycle(graph, orientation='ignore')
                execure(then.stmt)
            except nx.NetworkXNoCycle:
                pass
            
    elif command == 'closure':
        closure_type, graph_name = ast[1], ast[2]
        if graph_name not in graph_store:
            print(f"Error: Graph {graph_name} does not exist")
            return
        
        graph = graph_store[graph_name]
        edges_to_add = []
    
        if closure_type == 'reflexive':
            for node in graph.nodes():
                if not graph.has_edge(node, node):
                    edges_to_add.append((node, node, {"weight": 0}))
        
        elif closure_type == 'symmetric':
            edges_to_add = []
            for u, v in graph.edges():
                if not graph.has_edge(v, u):
                    edges_to_add.append((v, u))
                                
        elif closure_type == 'transitive':
            closure_graph = nx.transitive_closure(graph)
            for u, v in closure_graph.edges():
                if not graph.has_edge(u, v):
                    edges_to_add.append((u, v))
                    
        graph.add_edges_from(edges_to_add)
        pending_closures[graph_name] = edges_to_add
        print(f"{closure_type.capitalize()} closure applied to {graph_name}. New edges added: {edges_to_add}")
            
# Visualize graph (we use Plotly)
def visualize_interactive(graph_name, path=None, cycle=None, mst=None, closure=None):
    if graph_name not in graph_store:
        print(f"Error: Graph {graph_name} does not exist")
        return

    graph = graph_store[graph_name]
    is_directed = isinstance(graph, nx.DiGraph)
    pos = nx.spring_layout(graph, seed=42)

    edge_x, edge_y, cycle_edge_x, cycle_edge_y, path_edge_x, path_edge_y = [], [], [], [], [], []
    closure_edge_x, closure_edge_y = [], []
    edge_labels = {}

    cycle_edges = set((u, v) for u, v, *_ in cycle) if cycle else set()
    path_edges = set(zip(path, path[1:])) if path else set()
    closure_edges = set(closure) if closure else set()
    mst_edge_x, mst_edge_y = [], []
    mst_edges = set((u, v) for u, v, _ in mst) if mst else set()

    for u, v, data in graph.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        weight = str(data.get("weight", 0))
        edge_labels[(u, v)] = weight

        if (u, v) in closure_edges or (v, u) in closure_edges:
            closure_edge_x.extend([x0, x1, None])
            closure_edge_y.extend([y0, y1, None])
        elif (u, v) in mst_edges or (v, u) in mst_edges:
            mst_edge_x.extend([x0, x1, None])
            mst_edge_y.extend([y0, y1, None])
        elif (u, v) in cycle_edges or (v, u) in cycle_edges:
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
            node_colors.append("#ADD8E6")

    # Scatter plots for edges and nodes
    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=2, color="gray"), hoverinfo='none')
    cycle_edge_trace = go.Scatter(x=cycle_edge_x, y=cycle_edge_y, mode='lines', line=dict(width=3, color="red"), hoverinfo='none')
    path_trace = go.Scatter(x=path_edge_x, y=path_edge_y, mode='lines', line=dict(width=4, color="green"), hoverinfo='none')
    closure_trace = go.Scatter(x=closure_edge_x, y=closure_edge_y, mode='lines', line=dict(width=3, color="purple"), hoverinfo='none')

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text',
        text=node_text, textposition="top center",
        marker=dict(size=20, color=node_colors, line=dict(width=0, color="black"))
    )

    mst_trace = go.Scatter(x=mst_edge_x, y=mst_edge_y, mode='lines',
                           line=dict(width=3, color="orange"), hoverinfo='none')
    

    fig = go.Figure(data=[edge_trace, cycle_edge_trace, path_trace, mst_trace, closure_trace, node_trace])

    # **Tilføj vægte på edges**
    for (u, v), weight in edge_labels.items():
        x_mid = (pos[u][0] + pos[v][0]) / 2
        y_mid = (pos[u][1] + pos[v][1]) / 2
        fig.add_annotation(x=x_mid, y=y_mid, text=weight, showarrow=False,
                           font=dict(color="black", size=20, family="Arial"))

    # **Hvis grafen er directed, tilføj pile**
    if is_directed:
        for u, v in graph.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            fig.add_annotation(
                ax=x0, ay=y0, x=x1, y=y1,
                xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=3, arrowsize=1.5, arrowcolor="black"
            )

    # **Tilføj forklaringsboks**
    existing_annotations = list(fig.layout.annotations) if fig.layout.annotations is not None else []
    legend_annotation = dict(
        text="<span style='color:#ADD8E6; font-weight:bold;'>Blue</span>: Normal nodes & edges &nbsp;&nbsp;"
             "<span style='color:green; font-weight:bold;'>Green</span>: Shortest path &nbsp;&nbsp;"
             "<span style='color:red; font-weight:bold;'>Red</span>: Cycles &nbsp;"
             "<span style='color:orange; font-weight:bold;'>Orange</span>: MST &nbsp;",
             #"<span style='color:purple; font-weight:bold;'>Purple</span>: Closure edges",
        showarrow=False,
        xref="paper", yref="paper",
        x=0.5, y=-0.05, yanchor="top",
        font=dict(family="Trebuchet MS", size=12, color="black"),
        align="center",
        bordercolor="black",
        borderwidth=1,
        bgcolor="white"
    )
    existing_annotations.append(legend_annotation)

    # **Gør akserne synlige igen (koordinatsystem)**
    fig.update_layout(
        title={"text": f"<span style='font-family:Trebuchet MS; color:black; font-size:22px;'>Visualization of Graph: {graph_name}</span>",
               "x": 0.5, "xanchor": "center"},
        showlegend=False,
        annotations=existing_annotations,
        xaxis=dict(
            showgrid=True,
            zeroline=True,
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=True,
            showticklabels=True
        ),
        plot_bgcolor="white"
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