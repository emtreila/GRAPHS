# 🔄 Hamiltonian Cycle Finder — Undirected Graph

---

This Python project finds a **Hamiltonian cycle** in an **undirected graph** using an **iterative backtracking algorithm**. A Hamiltonian cycle is a closed loop that visits each vertex **exactly once** and returns to the starting point.

The Hamiltonian cycle is found using an **iterative depth-first traversal** with backtracking:

1. Start from an arbitrary vertex
2. Explore all paths that visit every vertex exactly once
3. Return to the starting vertex to complete the cycle
4. If no valid cycle is found, return `None`

This approach avoids recursion by using a **stack** to track the path and visited state.

---
