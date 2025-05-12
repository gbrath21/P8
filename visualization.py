import os
import sys
import platform
import subprocess
import webbrowser
import base64
import plotly.graph_objects as go
import plotly.io as pio
import networkx as nx

def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)

def encode_image_base64(path):
    with open(resource_path(path), "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def insert_logo_in_html(filename, logo_path):
    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()

    logo_base64 = encode_image_base64(logo_path)
    logo_html = f"""
    <div style="position:fixed; top:10px; left:10px; z-index:1000;">
        <img src="data:image/png;base64,{logo_base64}" alt="GML Logo" style="height:70px;">
    </div>
    """
    html = html.replace("<body>", f"<body>\n{logo_html}")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

def visualize_interactive(graph, graph_name, path=None, cycle=None, mst=None, closure=None, bfs=None, dfs=None):
    is_directed = isinstance(graph, nx.DiGraph)
    pos = nx.spring_layout(graph, seed=42)

    edge_x, edge_y, cycle_edge_x, cycle_edge_y, path_edge_x, path_edge_y = [], [], [], [], [], []
    closure_edge_x, closure_edge_y, bfs_edge_x, bfs_edge_y, dfs_edge_x, dfs_edge_y = [], [], [], [], [], []
    edge_labels = {}

    cycle_edges = set((u, v) for u, v, *_ in cycle) if cycle else set()
    path_edges = set(zip(path, path[1:])) if path else set()
    closure_edges = set(closure) if closure else set()
    mst_edges = set((u, v) for u, v, _ in mst) if mst else set()
    bfs_edges = set(bfs) if bfs else set()
    dfs_edges = set(dfs) if dfs else set()

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
        elif (u, v) in bfs_edges or (v, u) in bfs_edges:
            bfs_edge_x.extend([x0, x1, None])
            bfs_edge_y.extend([y0, y1, None])
        elif (u, v) in dfs_edges or (v, u) in dfs_edges:
            dfs_edge_x.extend([x0, x1, None])
            dfs_edge_y.extend([y0, y1, None])
        else:
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

    node_x, node_y, node_text, node_colors = [], [], [], []
    cycle_nodes = {n for u, v in cycle_edges for n in (u, v)}
    path_nodes = set(path) if path else set()

    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        color = graph.nodes[node].get("color")
        if color:
            node_colors.append(color)
        elif node in cycle_nodes:
            node_colors.append("red")
        elif node in path_nodes:
            node_colors.append("green")
        else:
            node_colors.append("#4ad3ff")

    fig = go.Figure(data=[
        go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=2, color="gray"), hoverinfo='none'),
        go.Scatter(x=cycle_edge_x, y=cycle_edge_y, mode='lines', line=dict(width=3, color="red"), hoverinfo='none'),
        go.Scatter(x=path_edge_x, y=path_edge_y, mode='lines', line=dict(width=4, color="green"), hoverinfo='none'),
        go.Scatter(x=closure_edge_x, y=closure_edge_y, mode='lines', line=dict(width=3, color="purple"), hoverinfo='none'),
        go.Scatter(x=bfs_edge_x, y=bfs_edge_y, mode='lines', line=dict(width=3, color="blue"), hoverinfo='none'),
        go.Scatter(x=dfs_edge_x, y=dfs_edge_y, mode='lines', line=dict(width=3, color="magenta"), hoverinfo='none'),
        go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text, textposition="top center",
                   marker=dict(size=25, color=node_colors, line=dict(width=0, color="black")))
    ])

    for (u, v), weight in edge_labels.items():
        x_mid = (pos[u][0] + pos[v][0]) / 2
        y_mid = (pos[u][1] + pos[v][1]) / 2
        fig.add_annotation(x=x_mid, y=y_mid, text=weight, showarrow=False,
                           font=dict(family="Trebuchet MS", size=14, color="black"),
                           xanchor='center', yanchor='bottom', yshift=10)

    if is_directed:
        for u, v in graph.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            fig.add_annotation(ax=x0, ay=y0, x=x1, y=y1, xref="x", yref="y", axref="x", ayref="y",
                               showarrow=True, arrowhead=4, arrowsize=3, arrowcolor="black")

    fig.add_annotation(
        xref="paper", yref="paper", x=0.5, y=-0.05, yanchor="top",
        text=("<span style='color:#4ad3ff; font-weight:bold;'>Blue</span>: Normal nodes & edges &nbsp;&nbsp;"
              "<span style='color:green; font-weight:bold;'>Green</span>: Shortest path &nbsp;&nbsp;"
              "<span style='color:red; font-weight:bold;'>Red</span>: Cycles &nbsp;&nbsp;"
              "<span style='color:orange; font-weight:bold;'>Orange</span>: MST &nbsp;&nbsp;"
              "<span style='color:blue; font-weight:bold;'>Dark blue</span>: BFS &nbsp;&nbsp;"
              "<span style='color:magenta; font-weight:bold;'>Pink</span>: DFS"),
        showarrow=False, font=dict(size=12, color="black"), bgcolor="white", bordercolor="black", borderwidth=1
    )

    algorithm_text = ""
    if path is not None:
        algorithm_text += f"<b>Shortest path:</b> {path}<br>"
    if cycle is not None:
        algorithm_text += f"<b>Cycle:</b> {cycle}<br>"
    if mst is not None:
        algorithm_text += f"<b>MST:</b> {list(mst)}<br>"
    if bfs is not None:
        algorithm_text += f"<b>BFS:</b> {bfs}<br>"
    if dfs is not None:
        algorithm_text += f"<b>DFS:</b> {dfs}<br>"

    if algorithm_text:
        fig.add_annotation(
            xref="paper", yref="paper",
            x=0.98, y=0.98,
            xanchor="right", yanchor="top",
            text=algorithm_text,
            showarrow=False,
            bordercolor="#444",
            borderwidth=2,
            bgcolor="rgba(255,255,255,0.9)",
            font=dict(family="Trebuchet MS", size=13, color="#333")
        )

    fig.update_layout(title={"text": f"<span style='font-family:Trebuchet MS; font-size:22px;'>Visualization of Graph: {graph_name}</span>",
                              "x": 0.5, "xanchor": "center"},
                      showlegend=False, plot_bgcolor="white",
                      xaxis=dict(showgrid=True, zeroline=True),
                      yaxis=dict(showgrid=True, zeroline=True))

    filename = os.path.join(os.path.expanduser("~/Desktop"), "graph_visualization.html")
    pio.write_html(fig, filename)
    insert_logo_in_html(filename, resource_path("GMLlogo.png"))

    try:
        if platform.system() == "Darwin":
            subprocess.run(["/usr/bin/open", filename], check=True)
        else:
            webbrowser.open_new_tab(f"file://{filename}")
        print(f"Graph visualization opened: {filename}")
    except Exception as e:
        print(f"Could not open browser: {e}")