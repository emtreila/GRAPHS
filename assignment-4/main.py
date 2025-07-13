from random import randint
from graph import Graph
from collections import defaultdict, deque


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
        print(" • Project schedule analysis")
        print("18. Analyze the project schedule.")

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
            graph.remove_edge(x, y)
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

    def ui_analyze_project_schedule(self):
        filename = input("Enter the project file name: ")  # gets the file name from the user
        try:
            analyze_project_schedule_from_file(filename)  # calls the function to analyze the project schedule
        except Exception as e:
            print(e)  # prints any errors that occur during the analysis

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
            if not (0 <= option <= 18):
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
            elif option == 18:
                self.ui_analyze_project_schedule()

        else:
            print("Invalid option!")


def analyze_project_schedule_from_file(filename):
    """
    for every directed edge u → v, vertex u comes before vertex v in the ordering.
    Analyzes the project schedule from a file.
    :param filename: The name of the file containing the project schedule.
    """

    durations = {} # dictionary to store activity durations
    prereq = defaultdict(list) # dictionary to store prerequisites
    successors = defaultdict(list) # dictionary to store successors
    vertices = set() # set to store all vertices

    # read the file and populate the dictionaries
    with open(filename) as f:
        for line in f:
            if line.strip() == "":
                continue
            parts = line.strip().split()
            activity = parts[0]
            duration = int(parts[1])
            prerequisites = [] if parts[2] == '-' else parts[2:]
            durations[activity] = duration
            vertices.add(activity)
            for p in prerequisites:
                prereq[activity].append(p)
                successors[p].append(activity)
                vertices.add(p)

    # compute in-degree for each vertex = number of prerequisites
    in_degree = {v: 0 for v in vertices}
    for act in prereq: # for each activity
        for p in prereq[act]: # for each prerequisite
            in_degree[act] += 1 # increment in-degree of the activity

    zero_in_degree_nodes = [] # create an empty list to hold nodes with in-degree 0
    for v in vertices: # loop through all vertices to check their in-degree
        if in_degree[v] == 0:
            zero_in_degree_nodes.append(v)
    queue = deque(zero_in_degree_nodes) # create a queue with nodes of in-degree 0

    # topological sort using in-degree
    topo = []  # list to store the sorted order
    while queue:
        u = queue.popleft()  # remove a node with in-degree 0
        topo.append(u)  # add it to the topological order

        for succ in successors[u]:  # go through all nodes that depend on 'u'
            in_degree[succ] -= 1  # we "remove" the edge u -> succ
            if in_degree[succ] == 0:
                queue.append(succ)  # if succ has no more dependencies, it's ready to be processed

    if len(topo) < len(vertices): # if the topological order doesn't include all vertices, there's a cycle
        print("The graph is not a DAG — cycle detected.")
        return

    print("\n Topological order of activities:")
    print(" → ".join(topo))

    # earliest start times
    earliest = {v: 0 for v in vertices} # initialize earliest start times to 0
    for u in topo: # for each vertex in topological order
        for v in successors[u]: # for each successor of u
            earliest[v] = max(earliest[v], earliest[u] + durations[u]) # update earliest start time of v
            # v can only start after all its prerequisites are completed
            # so it waits for the latest-finishing predecessor
            # this gives the earliest possible time v can start

    total_time = max(earliest[v] + durations[v] for v in vertices) # calculate total project time
    # its the maximum finish time of all activities

    # latest start times
    latest = {v: total_time - durations[v] for v in vertices} # initialize latest start times
    for u in reversed(topo): # process vertices in reverse topological order
        for v in successors[u]: # for each successor of u
            latest[u] = min(latest[u], latest[v] - durations[u]) # update latest start time of u
            # u must finish before its successors begin
            # so the latest it can start is the earliest its successors must start, minus its own duration
            # this gives the latest possible time u can start without delaying anything

    print("\n Project Schedule Analysis:")
    for v in topo:
        print(f"Activity '{v}' — duration: {durations[v]}, "
              f"earliest start: {earliest[v]}, "
              f"latest start: {latest[v]} ")

    print(f"\n Total project duration: {total_time} units")

    print("\n Critical activities:")
    # create an empty list to store critical activities
    critical = []
    for v in topo:
        # if earliest start time == latest start time -> the activity is critical
        if earliest[v] == latest[v]:
            critical.append(v)

    print(", ".join(critical))

    g = Graph()
    for v in vertices:
        g.add_vertex(v)
    for a in prereq:
        for p in prereq[a]:
            g.add_edge(p, a, durations[a])

    print("\n The graph structure:")
    print(g)


UI().main()
