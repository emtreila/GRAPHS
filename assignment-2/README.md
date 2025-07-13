#🔍 Connected Components in an Undirected Graph

This project implements a program to find the **connected components** of an **undirected graph** using **depth-first traversal (DFS)**. 

---

The connected components are found using an **iterative depth-first search (DFS)**:

1. For each unvisited vertex:
   - Start DFS traversal
   - Track all reachable vertices and edges
   - Form a subgraph for each connected component
2. Each connected component is returned as a separate `Graph` object.

This ensures that all vertices in the same component are grouped and isolated from others.

---
