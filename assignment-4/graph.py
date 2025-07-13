from collections import defaultdict, deque


class Graph:
    def __init__(self, vertices=None, incoming_edges=None, outgoing_edges=None, costs=None):
        """
        Constructor for the graph initializes
        :param vertices: either the number of vertices or a list of vertices
        :param incoming_edges: the incoming edges
        :param outgoing_edges: the outgoing edges
        :param costs: the costs of the edges
        """

        self._outgoing_edges = outgoing_edges if outgoing_edges is not None else {}
        self._incoming_edges = incoming_edges if incoming_edges is not None else {}
        self._costs = costs if costs is not None else {}

        if not (incoming_edges or outgoing_edges or costs):
            if vertices is None:
                vertices = []

            if isinstance(vertices, int):
                self._outgoing_edges = {i: [] for i in range(vertices)}
                self._incoming_edges = {i: [] for i in range(vertices)}
            elif isinstance(vertices, list):
                self._outgoing_edges = {v: [] for v in vertices}
                self._incoming_edges = {v: [] for v in vertices}


    def __str__(self):
        """
        Returns the string representation of the graph
        """
        graph = []

        graph.append("Outbound:")
        for x in self.parse_vertices():
            outbound_edges = " ".join(map(str, self.parse_outbound(x)))
            graph.append(f"{x}: {outbound_edges}")

        graph.append("Inbound:")
        for x in self.parse_vertices():
            inbound_edges = " ".join(map(str, self.parse_inbound(x)))
            graph.append(f"{x}: {inbound_edges}")

        return "\n".join(graph)

    # GETTERS AND SETTERS
    @property
    def number_of_vertices(self):
        return len(self._incoming_edges.keys())

    @property
    def incoming_edges(self):
        return self._incoming_edges

    @property
    def outgoing_edges(self):
        return self._outgoing_edges

    @property
    def costs(self):
        return self._costs

    def set_costs(self, new):
        self._costs = new

    def get_edges(self):
        """
        Returns the edges of the graph
        """
        return self._costs.keys()

    def get_cost_of_edge(self, x, y):
        """
        Returns the cost of an edge
        """
        if not self.valid_vertex(x):
            raise ValueError('The vertex {} not in graph!'.format(x))
        if not self.valid_vertex(y):
            raise ValueError('The vertex {} not in graph!'.format(y))
        if not self.edge_exists(x, y):
            raise ValueError(f'Edge ({x}, {y}) not in graph!')
        return self._costs[(x, y)]

    def change_cost(self, x, y, new_cost):
        """
        Changes the cost of the edge between x and y
        """
        if not self.valid_vertex(x):
            raise ValueError('The vertex {} not in graph!'.format(x))
        if not self.valid_vertex(y):
            raise ValueError('The vertex {} not in graph!'.format(y))
        if not self.edge_exists(x, y):
            raise ValueError(f'Edge ({x}, {y}) not in graph!')
        self._costs[(x, y)] = new_cost

    def valid_vertex(self, vertex):
        """
        Check if a vertex exists
        """
        return vertex in self._incoming_edges.keys()

    # PARSERS
    def parse_vertices(self):
        """
        Returns an iterator for the vertices
        """
        return self._outgoing_edges.keys()

    def parse_inbound(self, y):
        """
        Returns an iterator for the inbound edges of a vertex
        """
        if not self.valid_vertex(y):
            raise ValueError("The vertex {} doesn't exist!".format(y))
        for x in self._incoming_edges[y]:
            yield x

    def parse_outbound(self, x):
        """
        Returns an iterator for the outbound edges of a vertex
        """
        if not self.valid_vertex(x):
            raise ValueError("The vertex {} doesn't exist!".format(x))
        return list(self._outgoing_edges[x])

    # ADD & REMOVE VERTEX
    def add_vertex(self, new_vertex):
        """
        Adds the new vertex to the graph
        """
        if self.valid_vertex(new_vertex):
            raise ValueError("The vertex {} already exists!".format(new_vertex))
        self._outgoing_edges[new_vertex] = []
        self._incoming_edges[new_vertex] = []

    def remove_vertex(self, vertex_to_delete):
        """
        Removes a vertex
        """
        if not self.valid_vertex(vertex_to_delete):
            raise ValueError("The vertex {} doesn't exist!".format(vertex_to_delete))
        for e in list(self.parse_inbound(vertex_to_delete)):
            self.remove_edge(e, vertex_to_delete)
        for e in list(self.parse_outbound(vertex_to_delete)):
            self.remove_edge(vertex_to_delete, e)
        del self._incoming_edges[vertex_to_delete]
        del self._outgoing_edges[vertex_to_delete]

    # ADD & REMOVE EDGE
    def add_edge(self, x, y, c):
        """
        Add an edge between vertices x and y
        """
        if not self.valid_vertex(x):
            raise ValueError("The vertex {} doesn't exist!".format(x))
        if not self.valid_vertex(y):
            raise ValueError("The vertex {} doesn't exist!".format(y))
        if self.edge_exists(x, y):
            raise ValueError("The edge already exists!")
        self._outgoing_edges[x].append(y)
        self._incoming_edges[y].append(x)
        self._costs[(x, y)] = c
        return True

    def remove_edge(self, x, y):
        """
        Remove an edge between vertices x and y
        """
        if not self.valid_vertex(x):
            raise ValueError("Vertex {} doesn't exist.".format(x))
        if not self.valid_vertex(y):
            raise ValueError("Vertex {} doesn't exist.".format(y))
        if not self.edge_exists(x, y):
            raise ValueError("The edge doesn't exist!")
        self._costs.pop((x, y))
        self._outgoing_edges[x].remove(y)
        self._incoming_edges[y].remove(x)

    # # DEGREE
    def incoming_degree(self, vertex):
        """
        Returns the in degree of a vertex
        """
        if not self.valid_vertex(vertex):
            raise ValueError("The vertex {} doesn't exist!".format(vertex))
        return len(self._incoming_edges[vertex])

    def outgoing_degree(self, vertex):
        """
        Return the out degree of a vertex
        """
        if not self.valid_vertex(vertex):
            raise ValueError("The vertex {} doesn't exist!".format(vertex))
        return len(self._outgoing_edges[vertex])

    def edge_exists(self, x, y):
        """
        Check if there is an edge between two vertices
        """
        if not self.valid_vertex(x):
            raise ValueError("The vertex {} doesn't exist!".format(x))
        if not self.valid_vertex(y):
            raise ValueError("The vertex {} doesn't exist!".format(y))
        return y in self._outgoing_edges[x]

    def copy_graph(self):
        """
        Returns a copy of the graph
        """
        incoming_edges_copy = self._incoming_edges.copy()
        outgoing_edges_copy = self._outgoing_edges.copy()
        costs_copy = self._costs.copy()
        return Graph(None, incoming_edges_copy, outgoing_edges_copy, costs_copy)
