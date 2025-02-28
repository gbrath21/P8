import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# Graferne gemmes her
graph_store = {}

def create_graph():
    """Opretter en testgraf"""
    graph_name = "TestGraph"
    graph_store[graph_name] = nx.Graph()
    graph = graph_store[graph_name]

    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")
    graph.add_edge("D", "E")
    graph.add_edge("E", "A")

    return graph_name

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Visualization")

        # Indlæs graf
        self.graph_name = create_graph()
        self.graph = graph_store[self.graph_name]
        self.pos = nx.spring_layout(self.graph, seed=42)

        # Opsæt GUI layout
        self.canvas = None
        self.fig, self.ax = plt.subplots(figsize=(6, 5))

        self.start_button = ttk.Button(root, text="Start Animation", command=self.start_animation)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_animation)
        self.stop_button.pack(pady=5)

        self.speed_label = ttk.Label(root, text="Speed:")
        self.speed_label.pack()

        self.speed_scale = ttk.Scale(root, from_=0.1, to=2.0, orient=tk.HORIZONTAL)
        self.speed_scale.set(0.5)  # Standardhastighed
        self.speed_scale.pack()

        self.layout_label = ttk.Label(root, text="Layout:")
        self.layout_label.pack()

        self.layout_var = tk.StringVar(value="spring")
        self.layout_menu = ttk.Combobox(root, textvariable=self.layout_var, values=["spring", "circular", "kamada_kawai"])
        self.layout_menu.pack()

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        self.animation_running = False

    def update_graph(self, edges_to_draw):
        """Opdaterer grafen i GUI'en"""
        self.ax.clear()
        nx.draw(self.graph.edge_subgraph(edges_to_draw), self.pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=800, ax=self.ax)
        self.canvas.draw()

    def start_animation(self):
        """Starter animationen"""
        if self.animation_running:
            return
        
        self.animation_running = True
        edges = list(self.graph.edges())
        speed = self.speed_scale.get()

        for i in range(len(edges)):
            if not self.animation_running:
                break
            self.update_graph(edges[:i+1])
            self.root.update_idletasks()
            time.sleep(speed)

    def stop_animation(self):
        """Stopper animationen"""
        self.animation_running = False

# Start GUI
root = tk.Tk()
app = GraphApp(root)
root.mainloop()
