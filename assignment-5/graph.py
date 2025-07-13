class Graph:
    def __init__(self, vertices=None, edges=None):
        """
        Constructor for the graph initializes
        :param vertices: either the number of vertices or a list of vertices
        :param edges: the edges
        """
        self._edges = edges if edges is not None else {}

        if not vertices:
            self._vertices = set()
        else:
            if isinstance(vertices, int):
                self._vertices = set(range(vertices))
            elif isinstance(vertices, (list, set)):
                self._vertices = set(vertices)


    def __str__(self):
        """
        Returns the string representation of the undirected graph
        """
        graph = ["Undirected Graph Adjacency List:"]

        for vertex in self._vertices:
            neighbors = " ".join(map(str, self.get_neighbors(vertex)))
            graph.append(f"{vertex}: {neighbors}")

        return "\n".join(graph)

    # GETTERS AND SETTERS
    @property
    def vertices(self):
        return self._vertices

    @property
    def number_of_vertices(self):
        return len(self._vertices)

    @property
    def edges(self):
        return self._edges

    @property
    def number_of_edges(self):
        return len(self._edges)

    def get_cost_of_edge(self, x, y):
        """
        Returns the cost of an edge
        """
        if not self.vertex_exists(x):
            raise ValueError(f'The vertex {x} not in graph!')
        if not self.vertex_exists(y):
            raise ValueError(f'The vertex {y} not in graph!')
        if not self.edge_exists(x, y):
            raise ValueError(f'The edge ({x}, {y}) is not in the graph!')

        return self._edges[(x, y)]

    def change_cost(self, x, y, new_cost):
        """
        Changes the cost of the edge between x and y
        """
        if not self.vertex_exists(x):
            raise ValueError(f"The vertex {x} is not in the graph!")
        if not self.vertex_exists(y):
            raise ValueError(f"The vertex {y} is not in the graph!")

        if (x, y) in self._edges:
            self._edges[(x, y)] = new_cost
            self._edges[(y, x)] = new_cost
        else:
            raise ValueError(f"The edge ({x},{y})/({y},{x}) doesn't exist!")

    def vertex_exists(self, vertex):
        """
        Checks if a vertex exists in the graph

        :param vertex: The vertex to find
        :return: True if the vertex exists, False otherwise
        """
        return vertex in self._vertices

    def edge_exists(self, x, y):
        """
        Checks if an edge exists in the graph

        :param x: The first vertex of the edge
        :param y: The second vertex of the edge
        :return: True if the edge exists, False otherwise
        """
        return (x, y) in self._edges

    def get_neighbors(self, v):
        """
        Returns the list of neighbors of a vertex
        """
        if not self.vertex_exists(v):
            raise ValueError("The vertex {} doesn't exist!".format(v))
        neighbors = set()
        for edge in self._edges:
            if edge[0] == v:
                neighbors.add(edge[1])
            elif edge[1] == v:
                neighbors.add(edge[0])

        return neighbors

    # ADD & REMOVE VERTEX
    def add_vertex(self, new_vertex):
        """
        Adds the new vertex to the graph
        """
        if self.vertex_exists(new_vertex):
            raise ValueError(f"The vertex {new_vertex} already exists!")

        self._vertices.add(new_vertex)

    def remove_vertex(self, vertex_to_delete):
        """
        Removes a vertex from the graph, removing all edges
        associated with it

        :param vertex_to_delete: The vertex to delete
        :return: None
        """
        if not self.vertex_exists(vertex_to_delete):
            raise ValueError(f"The vertex {vertex_to_delete} doesn't exist!")

        edges_to_delete = []
        for edge in self._edges:
            if vertex_to_delete in edge:
                edges_to_delete.append(edge)

        for edge in edges_to_delete:
            del self._edges[edge]

        self._vertices.remove(vertex_to_delete)

    # ADD & REMOVE EDGE
    def add_edge(self, x, y, c):
        """
        Add an edge between vertices x and y with cost c

        If the edge already exists, update its cost

        :param x: The first vertex
        :param y: The second vertex
        :param c: The cost of the edge
        :return: None
        """
        if not self.vertex_exists(x):
            raise ValueError(f"The vertex {x} doesn't exist!")

        if not self.vertex_exists(y):
            raise ValueError(f"The vertex {y} doesn't exist!")


        self._edges[(x, y)] = c
        self._edges[(y, x)] = c

    def remove_edge(self, x, y):
        """
        Removes an edge between vertices x and y

        :param x: The first vertex
        :param y: The second vertex
        :return: None
        """
        if not self.vertex_exists(x):
            raise ValueError(f"The vertex {x} doesn't exist!")

        if not self.vertex_exists(y):
            raise ValueError(f"The vertex {y} doesn't exist!")

        if (x, y) in self._edges:
            del self._edges[(x, y)]
            del self._edges[(y, x)]
        else:
            raise ValueError(f"The edge ({x}, {y}) doesn't exist!")

    # DEGREE
    def degree(self, vertex) -> int:
        """
        Returns the degree of a vertex

        The degree is the number of edges that are connected to the
        vertex
        :param vertex: The vertex to get the degree of
        :return: The degree of the vertex
        """
        return len(self.get_neighbors(vertex))

    def isolated_vertices(self):
        """
        Returns a list of isolated vertices
        """
        return [v for v in self._vertices if self.degree(v) == 0]

    def copy_graph(self):
        """
        Returns a copy of the graph
        """
        vertices_copy = self._vertices.copy()
        edges_copy = self._edges.copy()
        return Graph(vertices_copy, edges_copy)
