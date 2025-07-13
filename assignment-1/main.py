from random import randint
from graph import Graph


# EXTERNAL FUNCTIONS

def create_random_graph(vertices, edges):
    """
    Creates a random graph with the specified number of vertices and edges
    """
    g = Graph(vertices)
    edges_added = set()
    while len(edges_added) < edges:
        x, y, c = randint(0, vertices - 1), randint(0, vertices - 1), randint(0, 100)
        if (x, y) not in edges_added:
            g.add_edge(x, y, c)
            edges_added.add((x, y))
    return g


def read_graph_from_file(filename):
    """
    Reads a graph from a file
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
        form = lines[0].strip()
        if form == 'format2':
            l = lines[1].strip().split()
            li = []
            for i in l:
                i = int(i)
                li.append(i)
            g = Graph(li)
            for line in lines[2:]:
                line = line.strip()
                if line == "":
                    continue
                arguments = line.split()
                x = int(arguments[0])
                y = int(arguments[1])
                cost = int(arguments[2])
                g.add_edge(x, y, cost)
        else:
            l = lines[0].strip().split()
            g = Graph(int(l[0]))
            for line in lines[1:]:
                line = line.strip()
                if line == "":
                    continue
                arguments = line.split()
                x = int(arguments[0])
                y = int(arguments[1])
                cost = int(arguments[2])
                g.add_edge(x, y, cost)
        return g


def write_graph_to_file(g, filename):
    """
    Writes a graph to a file
    """
    with open(filename, "w") as f:
        f.write("format2\n")
        isolated = []
        for v in g.parse_vertices():
            if g.incoming_degree(v) == 0 and g.outgoing_degree(v) == 0:
                isolated.append(v)
        f.write(str(g.number_of_vertices) + " ")
        no_edges = len(g.costs)
        f.write(str(no_edges) + "\n")
        vertices = ""
        for x in isolated:
            vertices = vertices + f"{x} "
        f.write(vertices + "\n")
        for x in g.parse_vertices():
            for y in g.parse_outbound(x):
                f.write(f"{x} {y} {g.get_cost_of_edge(x, y)}\n")


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
        print("6. Get the in degree of a vertex.")
        print("7. Get the out degree of a vertex.")
        print("8. Find if an edge between 2 vertices exists.")
        print("9. Retrieve the information (the integer) attached to a specified edge.")
        print("\t")
        print(" • Parse")
        print("10. Parse the set of vertices.")
        print(
            "11. Parse the set of outbound edges of a specified vertex. For each outbound edge, the iterator shall provide the target vertex.")
        print(
            "12. Parse the set of inbound edges of a specified vertex. For each inbound edge, the iterator shall provide the target vertex.")
        print("\t")
        print(" • Modify vertex, edge, cost")
        print("13. Add a vertex.")
        print("14. Remove vertex.")
        print("15. Add edge.")
        print("16. Remove edge.")
        print("17. Modify the information (the integer) attached to a specified edge.")
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
        if edges > (vertices * vertices):
            print("Too many edges!")
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

    def ui_in_degree(self, graph):
        vertex = input("Enter the vertex: ")
        try:
            vertex = int(vertex)
            degree = graph.incoming_degree(vertex)
            print(f"The in degree of the vertex {vertex} is {degree}.")
        except ValueError as e:
            print(e)


    def ui_out_degree(self, graph):
        vertex = input("Enter the vertex: ")
        try:
            vertex = int(vertex)
            degree = graph.outgoing_degree(vertex)
            print(f"The out degree of the vertex {vertex} is {degree}.")
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

    def ui_get_edge_information(self, graph):
        x = input("Enter the outgoing vertex: ")
        y = input("Enter the incoming vertex: ")
        try:
            x = int(x.strip())
            y = int(y.strip())
            print(f"The cost of the edge({x},{y}) is {graph.get_cost_of_edge(x, y)}")
        except ValueError as e:
            print(e)

    def ui_parse_vertices(self, graph):
        vertices = graph.parse_vertices()
        for vertex in vertices:
            print(vertex)

    def ui_parse_outbound_edges(self, graph):
        vertex = input("Enter the vertex: ")
        try:
            vertex = int(vertex)
            edges = graph.parse_outbound(vertex)
            for edge in edges:
                print(edge)
        except ValueError as e:
            print(e)

    def ui_parse_inbound_edges(self, graph):
        vertex = input("Enter the vertex: ")
        try:
            vertex = int(vertex)
            edges = graph.parse_inbound(vertex)
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
        x = input("Enter the outgoing vertex: ")
        y = input("Enter the incoming vertex: ")
        cost = input("Enter the cost: ")
        try:
            x = int(x.strip())
            y = int(y.strip())
            cost = int(cost.strip())
            graph.add_edge(x, y, cost)
        except ValueError as e:
            print(e)

    def ui_remove_edge(self, graph):
        x = input("Enter the outgoing vertex: ")
        y = input("Enter the incoming vertex: ")
        try:
            x = int(x.strip())
            y = int(y.strip())
            graph.remove_edge(x,y)
        except ValueError as e:
            print(e)

    def ui_modify_edge(self, graph):
        x = input("Enter the outgoing vertex: ")
        y = input("Enter the incoming vertex: ")
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
            if not (0 <= option <= 17):
                print("Invalid option!")
                return

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
                self.ui_in_degree(g)
            elif option == 7:
                self.ui_out_degree(g)
            elif option == 8:
                self.ui_edge_exists(g)
            elif option == 9:
                self.ui_get_edge_information(g)
            elif option == 10:
                self.ui_parse_vertices(g)
            elif option == 11:
                self.ui_parse_outbound_edges(g)
            elif option == 12:
                self.ui_parse_inbound_edges(g)
            elif option == 13:
                self.ui_add_vertex(g)
            elif option == 14:
                self.ui_remove_vertex(g)
            elif option == 15:
                self.ui_add_edge(g)
            elif option == 16:
                self.ui_remove_edge(g)
            elif option == 17:
                self.ui_modify_edge(g)
            else:
                print("Invalid option!")


UI().main()
