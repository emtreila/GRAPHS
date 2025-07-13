from random import randint
from graph import Graph


# EXTERNAL FUNCTIONS

def create_random_graph(vertices, edges):
    """
    Creates a random graph with the specified number of vertices and edges
    """
    g = Graph(vertices)
    edges_added = 0

    while edges_added < edges:
        x, y, c = randint(0, vertices - 1), randint(0, vertices - 1), randint(0, 100)
        if x == y:
            continue

        try:
            g.add_edge(x, y, c)
            edges_added += 1
        except Exception as e:
            print(e)

    return g


def read_graph_from_file(filename):
    """
    Reads an undirected graph from a file
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
        form = lines[0].strip()

        if form == "format2":
            vertices = list(map(int, lines[1].strip().split()))
            start_index = 2
        else:
            vertices = int(lines[0].strip().split()[0])
            start_index = 1

        g = Graph(vertices)
        for line in lines[start_index:]:
            line = line.strip()
            if not line:
                continue

            x, y, cost = map(int, line.split())
            if not g.edge_exists(x, y):
                g.add_edge(x, y, cost)

        return g


def write_graph_to_file(g, filename):
    """
    Writes an undirected graph to a file
    """
    with open(filename, "w") as f:
        f.write("format2\n")
        f.write(f"{g.number_of_vertices} {g.number_of_edges}\n")
        f.write(" ".join(map(str, g.isolated_vertices())) + "\n")

        for edge in g.edges:
            f.write(f"{edge[0]} {edge[1]} {g.edges[edge]}\n")


class UI:
    def __init__(self):
        self._graphs = []
        self._current = None

    def show_menu(self):
        print(" MENU ")
        print("\t")
        print("0. EXIT")
        print("\t")
        print(" • Graph configuration   ")
        print("1. Create a random graph with specified number of vertices and edges.")
        print("2. Read the graph from a text file.")
        print("3. Write the graph in a text file. ")
        print("4. Copy the graph. Save the copy in a text file.")
        print("\t")
        print(" • Graph Properties")
        print("5. Get the number of vertices.")
        print("6. Get the degree of a vertex.")
        print("7. Find if an edge between 2 vertices exists.")
        print("8. Retrieve the cost attached to a specified edge.")
        print("\t")
        print(" • Parse")
        print("9. Parse the set of vertices.")
        print("10. Parse the set of edges.")
        print("\t")
        print(" • Modify vertex, edge, cost")
        print("11. Add a vertex.")
        print("12. Remove vertex.")
        print("13. Add edge.")
        print("14. Remove edge.")
        print("15. Modify the information (the integer) attached to a specified edge.")
        print("\t")
        print(" • Find Hamiltonian Cycle")
        print("16. Find a Hamiltonian cycle in the graph.")
        print("\t")

    def ui_create_random_graph(self):
        print("\t")
        vertices = input(" Number of vertices: ")
        edges = input(" Number of edges: ")
        try:
            vertices = int(vertices)
            edges = int(edges)
        except:
            print("Invalid numbers!")
            return
        if edges > (vertices * (vertices - 1)) // 2:
            print("Too many edges for an undirected graph!")
            return
        else:
            return create_random_graph(vertices, edges)

    def ui_read_graph_from_file(self):
        filename = input("Enter the name of the file: ")
        try:
            new_graph = read_graph_from_file(filename)
            return new_graph
        except Exception as e:
            print(f"Error reading file: {e}")

    def ui_write_graph_to_file(self, graph):
        filename = input("Enter the name of the file: ")
        try:
            write_graph_to_file(graph, filename)
            print("Graph successfully written to file.")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def ui_copy_graph(self, graph):
        copy = graph.copy_graph()
        self.ui_write_graph_to_file(copy)

    def ui_number_vertices(self, graph):
        nr = graph.number_of_vertices
        print(f" The number of vertices is: {nr}.\t")

    def ui_degree(self, graph):
        vertex = input("Enter the vertex: ")
        try:
            vertex = int(vertex)
            deg = graph.degree(vertex)
            print(f"The in degree of the vertex {vertex} is {deg}.")
        except ValueError as e:
            print(e)

    def ui_edge_exists(self, graph):
        x = input("Enter the first vertex: ")
        y = input("Enter the second vertex: ")
        try:
            x = int(x.strip())
            y = int(y.strip())
            if graph.edge_exists(x, y):
                print(f"There is an edge between {x} and {y}.")
            else:
                print(f"There is no edge between {x} and {y}.")
        except ValueError as e:
            print(e)

    def ui_get_edge_cost(self, graph):
        x = input("Enter the first vertex: ")
        y = input("Enter the second vertex: ")
        try:
            x = int(x.strip())
            y = int(y.strip())
            print(f"The cost of the edge({x},{y}) is {graph.get_cost_of_edge(x, y)}")
        except ValueError as e:
            print(e)

    def ui_parse_vertices(self, graph):
        for vertex in graph.vertices:
            print(vertex)

    def ui_parse_edges(self, graph):
        vertex = input("Enter the vertex: ")
        try:
            vertex = int(vertex)
            edges = graph.get_neighbors(vertex)
            for edge in edges:
                print(edge)
        except ValueError as e:
            print(e)

    def ui_add_vertex(self, graph):
        vertex = input("Enter the vertex: ")
        try:
            vertex = int(vertex)
            graph.add_vertex(vertex)
        except ValueError as e:
            print(e)

    def ui_remove_vertex(self, graph):
        vertex = input("Enter the vertex: ")
        try:
            vertex = int(vertex)
            graph.remove_vertex(vertex)
        except ValueError as e:
            print(e)

    def ui_add_edge(self, graph):
        x = input("Enter the first vertex: ")
        y = input("Enter the second vertex: ")
        cost = input("Enter the cost: ")
        try:
            x = int(x.strip())
            y = int(y.strip())
            cost = int(cost.strip())
            graph.add_edge(x, y, cost)
        except ValueError as e:
            print(e)

    def ui_remove_edge(self, graph):
        x = input("Enter the first vertex: ")
        y = input("Enter the second vertex: ")
        try:
            x = int(x.strip())
            y = int(y.strip())
            graph.remove_edge(x, y)
        except ValueError as e:
            print(e)

    def ui_modify_edge(self, graph):
        x = input("Enter the first vertex: ")
        y = input("Enter the second vertex: ")
        cost = input("Enter the new cost: ")
        try:
            x = int(x.strip())
            y = int(y.strip())
            cost = int(cost.strip())
            graph.change_cost(x, y, cost)
        except ValueError as e:
            print(e)

    def main(self):
        g = Graph()
        self.show_menu()

        while True:

            option = input("\nPlease choose an option: ")
            if not option:
                print("Invalid option!")
                return
            try:
                option = int(option.strip())
            except:
                print("Invalid option!")
                return
            if not (0 <= option <= 16):
                print("Invalid option!")
                continue

            if option == 0:
                print("Bye, bye!")
                exit()
            elif option == 1:
                new_graph = self.ui_create_random_graph()
                if new_graph:
                    g = new_graph
            elif option == 2:
                new_graph = self.ui_read_graph_from_file()
                if new_graph:
                    g = new_graph
            elif option == 3:
                self.ui_write_graph_to_file(g)
            elif option == 4:
                self.ui_copy_graph(g)
            elif option == 5:
                self.ui_number_vertices(g)
            elif option == 6:
                self.ui_degree(g)
            elif option == 7:
                self.ui_edge_exists(g)
            elif option == 8:
                self.ui_get_edge_cost(g)
            elif option == 9:
                self.ui_parse_vertices(g)
            elif option == 10:
                self.ui_parse_edges(g)
            elif option == 11:
                self.ui_add_vertex(g)
            elif option == 12:
                self.ui_remove_vertex(g)
            elif option == 13:
                self.ui_add_edge(g)
            elif option == 14:
                self.ui_remove_edge(g)
            elif option == 15:
                self.ui_modify_edge(g)
            elif option == 16:
                cycle = find_hamiltonian_cycle_iterative(g)
                if cycle:
                    print("Hamiltonian cycle found:", " -> ".join(map(str, cycle)))
                else:
                    print("No Hamiltonian cycle found.")
            else:
                print("Invalid option!")
                continue


def find_hamiltonian_cycle_iterative(graph):
    """
    Find a Hamiltonian cycle in an undirected graph.
    Returns a list of vertices forming the cycle, or None if not found.
    """
    vertices = list(graph.vertices) # get the list of vertices in the graph
    n = len(vertices) # number of vertices in the graph
    if n == 0: # if there are no vertices in the graph
        return None

    start = vertices[0] # start from the first vertex
    stack = [(start, [start], set([start]))]  # (current_vertex, path_so_far, visited_set)

    while stack: # while there are still vertices to explore
        current, path, visited = stack.pop() # get the current vertex, path so far, and visited vertices

        if len(path) == n: # if the path includes all vertices
            if graph.edge_exists(path[-1], start): # check if there is an edge back to the start vertex
                return path + [start]  # complete cycle
            continue

        for neighbor in graph.get_neighbors(current): # get the neighbors of the current vertex
            if neighbor not in visited: # if the neighbor has not been visited
                new_path = path + [neighbor] # extend the path with the neighbor
                new_visited = visited | {neighbor} # mark the neighbor as visited
                stack.append((neighbor, new_path, new_visited)) # add the new state to the stack

    return None


UI().main()
