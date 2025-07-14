# Backwards Dijkstra Algorithm for Shortest Path

This Python project implements the **backwards Dijkstra algorithm** to find the **lowest cost walk** between two vertices in a directed graph with **positive edge costs**. Instead of starting from the source, this algorithm starts from the destination and works backwards.

---

The backwards Dijkstra algorithm functions as follows:

1. Start from the **destination** vertex.
2. Use a **priority queue (min-heap)** to explore **inbound** edges.
3. Keep track of the **shortest known distances** from each vertex to the destination.
4. Reconstruct the shortest path once the source vertex is reached.

---
