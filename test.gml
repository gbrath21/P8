graph G directed
node A in G
node B in G
node C in G
edge A -> B weight 10 in G
edge B -> C weight 5 in G
edge A -> C weight 5 in G
visualize G

graph G directed
node A in G
node B in G
node C in G
edge A -> B weight 10 in G
edge B -> C weight 5 in G
edge A -> C weight 5 in G
find path A to B in G
visualize G

graph G
node A in G
node B in G
node C in G
if node A in G then delete1 node A from G
visualize G

graph G directed
node A in G
node B in G
edge A -> B weight 10 in G
node C in G
edge B -> C weight 5 in G
edge C -> A weight 5 in G
find path A to B in G
visualize G

graph G directed 
node A in G
node B in G 
node C in G
edge A -> B weight 10 in G 
edge B -> C weight 5 in G 
edge A -> C weight 5 in G
find cycle in G
visualize G

graph G directed
node A in G
node B in G
node C in G
edge A -> B in G
edge B -> C in G
closure transitive in G
visualize G

graph G
node A in G
node B in G
node C in G
edge A -> B weight 3 in G
edge B -> C weight 1 in G
edge A -> C weight 2 in G
find mst in G
visualize G

graph H directed 
node A in H
node B in H
delete1 node B from H
edge A -> B in H
visualize H

graph G
node A in G
node B in G
edge A -> B weight 10 in G
save graph G to "graph1.gml"

load graph H from "graph1.gml"
visualize H

graph G directed
node A in G
node B in G 
node C in G 
node D in G 
node E in G 
edge A -> B in G
edge B -> C in G 
edge C -> D in G
edge D -> E in G 
edge E -> A in G 
visualize G