import os
import sys
import pickle
import networkx as nx
from parser import parser
import numpy as np
from visualization import visualize_interactive, resource_path

# Stores graphs etc.
graph_store = {}
visualize_called = False 
pending_cycles = {} 
pending_paths = {}   
pending_closures = {}
pending_msts = {}
pending_bfs = {}
pending_dfs = {}

def replace_identifier(ast, old, new):
    if isinstance(ast, tuple):
        return tuple(replace_identifier(elem, old, new) for elem in ast)
    elif isinstance(ast, list):
        return [replace_identifier(elem, old, new) for elem in ast]
    elif isinstance(ast, str):
        return new if ast == old else ast
    else:
        return ast  # fx int, float
    
def evaluate_condition(cond, sigma):
    if cond[0] == 'cond':
        sub = cond[1:]

        if sub[0] == 'node':
            _, n, _, G = sub
            return G in graph_store and n in graph_store[G]

        elif sub[0] == 'edge':
            _, u, _, v, _, G = sub
            return G in graph_store and graph_store[G].has_edge(u, v)

        elif sub[0] == 'path':
            _, n1, _, n2, _, G = sub
            if G in graph_store:
                try:
                    nx.shortest_path(graph_store[G], source=n1, target=n2)
                    return True
                except nx.NetworkXNoPath:
                    return False

        elif sub[0] == 'find':
            _, what, _, G = sub
            if what == 'cycle':
                if G in graph_store:
                    try:
                        nx.find_cycle(graph_store[G], orientation='ignore')
                        return True
                    except nx.NetworkXNoCycle:
                        return False

        elif sub[0] == 'not':
            rest = sub[1:]
            if rest[0] == 'node':
                _, n, _, G = rest
                return G in graph_store and n not in graph_store[G]
            elif rest[0] == 'edge':
                _, u, _, v, _, G = rest
                return G in graph_store and not graph_store[G].has_edge(u, v)
            elif rest[0] == 'path':
                _, n1, _, n2, _, G = rest
                if G in graph_store:
                    try:
                        nx.shortest_path(graph_store[G], source=n1, target=n2)
                        return False
                    except nx.NetworkXNoPath:
                        return True
            elif rest[0] == 'find':
                _, what, _, G = rest
                if what == 'cycle':
                    if G in graph_store:
                        try:
                            nx.find_cycle(graph_store[G], orientation='ignore')
                            return False
                        except nx.NetworkXNoCycle:
                            return True

    elif cond[0] == 'and':
        return evaluate_condition(cond[1], sigma) and evaluate_condition(cond[2], sigma)
    elif cond[0] == 'or':
        return evaluate_condition(cond[1], sigma) or evaluate_condition(cond[2], sigma)

    print(f"Unknown condition: {cond}")
    return False

def execute(ast):
    global visualize_called, pending_cycles, pending_paths, pending_msts, pending_closures, pending_bfs, pending_dfs
    
    if ast is None:
        return

    command = ast[0]
    
    # if visualize_called:
    #     print("Warning: No commands should be executed after 'visualize'. Ignoring input.")
    #     return  # Stop al eksekvering efter visualize
    
    if command == 'visualize':
        visualize_called = True  # Marker at visualize er kaldt
        graph_names = ast[1] if isinstance(ast[1], list) else [ast[1]]
        
        for graph_name in graph_names:
            if graph_name in graph_store:
                cycle = pending_cycles.pop(graph_name, None)  # Hent og fjern cyklus fra pending
                path = pending_paths.pop(graph_name, None)  # Hent og fjern path fra pending
                mst = pending_msts.pop(graph_name, None)
                bfs = pending_bfs.pop(graph_name, None)
                dfs = pending_dfs.pop(graph_name, None)
                graph = graph_store[graph_name]
                visualize_interactive(graph, graph_name, path=path, cycle=cycle, mst=mst, bfs=bfs, dfs=dfs)

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

    # Remove / delete a node in the graph
    elif command == 'remove_node':
        node_name, graph_name = ast[1], ast[2]
    
        if graph_name in graph_store:
            graph = graph_store[graph_name]
        
            if node_name in graph:
                graph.remove_node(node_name)
                print(f"Node {node_name} removed from {graph_name}.")
            else:
                print(f"Error: Node {node_name} does not exist in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")
            
    elif command == 'remove_edge':
        node1, node2, graph_name = ast[1], ast[2], ast[3]
        if graph_name in graph_store:
            graph = graph_store[graph_name]
            if graph.has_edge(node1, node2):
                graph.remove_edge(node1, node2)
                print(f"Edge {node1} -> {node2} removed from {graph_name}.")
            else:
                print(f"Error: Edge {node1} -> {node2} does not exist in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")
                
    elif command == 'color_node':
        node_name, color = ast[1], ast[2].strip('"')
        for graph in graph_store.values():
            if node_name in graph.nodes:
                graph.nodes[node_name]['color'] = color
                print(f"Colored node {node_name} with \"{color}\"")
        
    elif command == 'loop_node':
        var_name, graph_name, inner_statements = ast[1], ast[2], ast[3]
        graph = graph_store.get(graph_name)
        if graph:
            for node in graph.nodes():
                for stmt in inner_statements:
                    replaced_stmt = replace_identifier(stmt, var_name, node)
                    execute(replaced_stmt)
                    
    elif command == 'loop_edge':
        var1, var2, graph_name, inner_statements = ast[1], ast[2], ast[3], ast[4]
        graph = graph_store.get(graph_name)
        if graph:
            for u, v in graph.edges():
                for stmt in inner_statements:
                    replaced_stmt = replace_identifier(stmt, var1, u)
                    replaced_stmt = replace_identifier(replaced_stmt, var2, v)
                    print(f"Replacing U={u}, V={v}")
                    print("Before:", stmt)
                    print("After:", replaced_stmt)
                    execute(replaced_stmt)
    
    elif command == 'loop_graph_range':
        var, start, end, graph_name, block = ast[1], ast[2], ast[3], ast[4], ast[5]
        graph = graph_store.get(graph_name)
        if not graph:
            print(f"Error: Graph {graph_name} does not exist")
            return
        nodes = list(graph.nodes())
        for i in range(start - 1, min(end, len(nodes))):
            current_node = nodes[i]
            for stmt in block:
                replaced_stmt = replace_identifier(stmt, var, current_node)
                execute(replaced_stmt)
                
    elif command == 'loop_edge_range':
        u_var, v_var, start, end, graph_name, block = ast[1], ast[2], ast[3], ast[4], ast[5], ast[6]
        graph = graph_store.get(graph_name)
        if not graph:
            print(f"Error: Graph {graph_name} does not exist")
            return
        edges = list(graph.edges())
        for i in range(start - 1, min(end, len(edges))):
            u, v = edges[i]
            for stmt in block:
                stmt_replaced = replace_identifier(stmt, u_var, u)
                stmt_replaced = replace_identifier(stmt_replaced, v_var, v)
                execute(stmt_replaced)
                
    elif command == 'loop_times':
        start, end, block = ast[1], ast[2], ast[3]
        for _ in range(start, end + 1):
            for stmt in block:
                execute(stmt)
                
    elif command == 'add_weight':
        amount, node1, node2, graph_name = ast[1], ast[2], ast[3], ast[4]
        if graph_name in graph_store:
            graph = graph_store[graph_name]
            if graph.has_edge(node1, node2):
                current_weight = graph[node1][node2].get('weight', 0)
                new_weight = current_weight + amount
                graph[node1][node2]['weight'] = new_weight
                print(f"Updated weight of edge {node1} -> {node2} in {graph_name}: {current_weight} -> {new_weight}")
            else:
                print(f"Error: Edge {node1} -> {node2} does not exist in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")
                
    elif command == 'add_to_weight':
        amount, u, v = ast[1], ast[2], ast[3]
        for graph in graph_store.values():
            if graph.has_edge(u, v):
                current_weight = graph[u][v].get("weight", 0)
                graph[u][v]["weight"] = current_weight + amount
                print(f"Updated weight on edge {u} -> {v} to {current_weight + amount}")
            else:
                print(f"Edge {u} -> {v} not found")
    
    # If statements 
    elif command == 'if_expr':
        condition_ast, then_stmt = ast[1], ast[2]
        if evaluate_condition(condition_ast, sigma=None):  # sigma kan bruges senere til fx miljø
            execute(then_stmt)
    
    elif command == 'if_node':
        node, graph_name, then_stmt = ast[1], ast[2], ast[3]
        if graph_name in graph_store and node in graph_store[graph_name]:
            execute(then_stmt)
            
    elif command == 'if_edge':
        node1, node2, graph_name, then_stmt = ast[1], ast[2], ast[3], ast[4]
        graph = graph_store.get(graph_name)
        if graph and graph.has_edge(node1, node2):
            execute(then_stmt)
            
    elif command == 'if_path':
        node1, node2, graph_name, then_stmt = ast[1], ast[2], ast[3], ast[4]
        graph = graph_store.get(graph_name)
        if graph:
            try:
                nx.shortest_path(graph, source=node1, target=node2)
                execute(then_stmt)
            except nx.NetworkXNoPath:
                pass
    
    elif command == 'if_cycle':
        graph_name, then_stmt = ast[1], ast[2]
        graph = graph_store.get(graph_name)
        if graph:
            try:
                nx.find_cycle(graph, orientation='ignore')
                execute(then_stmt)
            except nx.NetworkXNoCycle:
                pass

    elif command == 'if_edge_weight':
        node1, node2, threshold, graph_name, then_stmt = ast[1], ast[2], ast[3], ast[4], ast[5]
        if graph_name in graph_store:
            graph = graph_store[graph_name]
            if graph.has_edge(node1, node2):
                current_weight = graph[node1][node2].get("weight", 0)
                if current_weight > threshold:
                    execute(then_stmt)
            else:
                print(f"Error: Edge {node1} -> {node2} does not exist in {graph_name}")
        else:
            print(f"Error: Graph {graph_name} does not exist")
    
    elif command == 'if_not_edge':
        node1, node2, graph_name, then_stmt = ast[1], ast[2], ast[3], ast[4]
        graph = graph_store.get(graph_name)
        if graph and not graph.has_edge(node1, node2):
            execute(then_stmt)
            
    elif command == 'if_not_node':
        node, graph_name, then_stmt = ast[1], ast[2], ast[3]
        if graph_name in graph_store and node not in graph_store[graph_name]:
            execute(then_stmt)
            
    elif command == 'if_not_path':
        node1, node2, graph_name, then_stmt = ast[1], ast[2], ast[3], ast[4]
        graph = graph_store.get(graph_name)
        if graph:
            try:
                nx.shortest_path(graph, source=node1, target=node2)
            except nx.NetworkXNoPath:
                execute(then_stmt)
    
    elif command == 'if_not_cycle':
        graph_name, then_stmt = ast[1], ast[2]
        graph = graph_store.get(graph_name)
        if graph:
            try:
                nx.find_cycle(graph, orientation='ignore')
            except nx.NetworkXNoCycle:
                execute(then_stmt)
    
    elif command == 'find_bfs':
        start_node, graph_name = ast[1], ast[2]
        graph = graph_store.get(graph_name)
        if graph and start_node in graph:
            bfs_nodes = list(nx.bfs_tree(graph, source=start_node).nodes())
            bfs_edges = list(nx.bfs_edges(graph, source=start_node))
            pending_bfs[graph_name] = bfs_edges
            print(f"BFS from {start_node} in {graph_name}: {bfs_nodes}")
        else:
            print(f"Error: Node or graph not found")
            
    elif command == 'find_dfs':
        start_node, graph_name = ast[1], ast[2]
        graph = graph_store.get(graph_name)
        if graph and start_node in graph:
            dfs_nodes = list(nx.dfs_tree(graph, source=start_node).nodes())
            dfs_edges = list(nx.dfs_edges(graph, source=start_node))
            pending_dfs[graph_name] = dfs_edges
            print(f"DFS from {start_node} in {graph_name}: {dfs_nodes}")
        else:
            print(f"Error: Node or graph not found")
            
    elif command == 'save_graph':
        graph_name, filename = ast[1], ast[2]
        if graph_name in graph_store:
            try:
                with open(filename, "wb") as f:
                    pickle.dump(graph_store[graph_name], f)
                    print(f"Graph {graph_name} saved to {filename}")
            except Exception as e:
                print(f"Error saving graph {graph_name} to {filename}: {e}")
        else:
            print(f"Error: Graph {graph_name} does not exist")
    
    elif command == 'load_graph':
        graph_name, filename = ast[1], ast[2]
        try:
            with open(filename, "rb") as f:
                loaded_graph = pickle.load(f)
                graph_store[graph_name] = loaded_graph
                print(f"Graph {graph_name} loaded from {filename}")
        except Exception as e:
            print(f"Error loading graph {graph_name} from {filename}: {e}")
            
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

def run_gml(code):
    lines = code.strip().split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        # Find alle typer af loops
        if line.strip().startswith("loop"):
            loop_header = line
            loop_indent = len(line) - len(line.lstrip())
            block_lines = []
            i += 1

            while i < len(lines):
                block_line = lines[i]
                indent = len(block_line) - len(block_line.lstrip())
                if not block_line.strip() or indent <= loop_indent:
                    break
                block_lines.append(block_line)
                i += 1

            full_block = loop_header + "\n" + "\n".join(block_lines)
            try:
                ast = parser.parse(full_block)
                execute(ast)
            except Exception as e:
                print(f"Parse error in loop block: {e}")
        else:
            try:
                ast = parser.parse(line.strip())
                execute(ast)
            except Exception as e:
                print(f"Parse error: {e}")
            i += 1