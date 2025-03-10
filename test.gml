graph G directed
node A in G
node B in G
edge A -> B weight 10 in G
node C in G
edge B -> C weight 5 in G
visualize G


graph G
node A in G
node B in G
edge A -> B weight 10 in G
save graph G to "graph1.gml"

load graph H from "graph1.gml"
visualize H