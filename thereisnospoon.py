import sys


class Node:
    """ A node with its coordinates
    """
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.neighbors = []

    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ',' +\
               str(self.value) + ')'

    def to_solution_string(self):
        return str(self.x) + " " + str(self.y)

    def coords(self):
        return (self.x, self.y)

    def get_value(self):
        return self.value

    def equals(self, node):
        return self.x == node.x and self.y == node.y

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(tuple([self.x, self.y]))


class Graph:
    """ Representation of the graph"""

    def __init__(self, cell_matrix, width, height):
        self.width = width
        self.height = height
        self.adj_list = {}
        # Map x, y to a Node
        self.matrix = {}
        for y, line in enumerate(cell_matrix):
            for x, char in enumerate(line):
                if char == '.':
                    pass
                else:
                    value = int(char)
                    n = Node(x, y, value)
                    self.adj_list[n] = []
                    if x not in self.matrix:
                        self.matrix[x] = {}
                    self.matrix[x][y] = n

        # Set all the possible neighbors
        for node in self.adj_list:
            # print >> sys.stderr, 'Searching neighbors of '+str(node)
            current_x = node.x
            current_y = node.y
            # Up
            while(current_y > 0):
                current_y = current_y - 1
                # Is there a node?
                possible_neighbor = self.get_point(current_x, current_y)
                if possible_neighbor is not None:
                    # print >> sys.stderr, 'Found a neighbor '+str(possible_neighbor)
                    node.neighbors.append(possible_neighbor)
                    break

            current_y = node.y
            # Down
            while(current_y < self.height):
                current_y = current_y + 1
                # Is there a node?
                possible_neighbor = self.get_point(current_x, current_y)
                if possible_neighbor is not None:
                    # print >> sys.stderr, 'Found a neighbor '+str(possible_neighbor)
                    node.neighbors.append(possible_neighbor)
                    break

            current_y = node.y
            # Left
            while(current_x > 0):
                current_x = current_x - 1
                # Is there a node?
                possible_neighbor = self.get_point(current_x, current_y)
                if possible_neighbor is not None:
                    # print >> sys.stderr, 'Found a neighbor '+str(possible_neighbor)
                    node.neighbors.append(possible_neighbor)
                    break

            current_x = node.x

            # Right
            while(current_x < self.width):
                current_x = current_x + 1
                # Is there a node?
                possible_neighbor = self.get_point(current_x, current_y)
                if possible_neighbor is not None:
                    # print >> sys.stderr, 'Found a neighbor '+str(possible_neighbor)
                    node.neighbors.append(possible_neighbor)
                    break

            current_x = node.x

    def get_point(self, x, y):
        if x in self.matrix:
            if y in self.matrix[x]:
                return self.matrix[x][y]
        return None

    def debug_neighbors(self):
        for node in self.adj_list:
            print >> sys.stderr, "Neighbors of " + str(node) + ": " + str(node.neighbors)

    def add_link(self, node1, node2):
        # print >> sys.stderr, 'Adding link between '+str(node1)+' and ' + str(node2)
        if len(self.adj_list[node1]) >= node1.value:
            print >> sys.stderr, 'Cannot add a link to ' + str(node1)
            return False
        if len(self.adj_list[node2]) >= node2.value:
            print >> sys.stderr, 'Cannot add a link to ' + str(node2)
            return False

        if self.adj_list[node1].count(node2) == 2:
            print >> sys.stderr, 'Already two links, cannot add more between the nodes.'
            return False

        for n, links in self.adj_list.iteritems():
            if n.equals(node1):
                links.append(node2)
            if n.equals(node2):
                links.append(node1)
        return True

    def remove_link(self, node1, node2):
        # print >> sys.stderr, 'Removing a link between '+str(node1)+' and ' + str(node2)
        for n, links in self.adj_list.iteritems():
            if n.equals(node1):
                links.remove(node2)
            if n.equals(node2):
                links.remove(node1)

    def check_if_solution_ok(self):
        """ Method to call on a graph in which
        all nodes have their number of links met.
        Checks that all nodes are connected.
        """
        is_ok_dict = {}
        # Init all at false
        for node in self.adj_list:
            is_ok_dict[node] = False

        # Recursively go through the links
        first = self.adj_list.keys()[0]
        self.rec_is_sol_ok(first, is_ok_dict)

        for n, is_ok in is_ok_dict.iteritems():
            if not is_ok:
                # print >> sys.stderr, "A node was not linked! " + str(n)
                return False

        # Check for crossed links
        for node, links in self.adj_list.iteritems():
            pass

        return True

    def get_nb_links_node(self, node):
        return len(self.adj_list[node])

    def depth_first_search(self, node):
        visited = {node: False for node in self.adj_list}
        self.depth_first_search_rec(node, visited)
        return visited

    def depth_first_search_rec(self, node, visited):
        visited[node] = True
        for linked in self.adj_list[node]:
            if not visited[linked]:
                self.depth_first_search_rec(linked, visited)

    def find_connected_components(self):
        islands = []
        for node in self.adj_list:
            # Check that we haven't already seen the node
            already_processed = False
            for island in islands:
                if node in island:
                    already_processed = True
                    break

            if not already_processed:
                visited = self.depth_first_search(node)
                connected = []
                for node, status in visited.iteritems():
                    if status:
                        connected.append(node)

                islands.append(connected)

        print >> sys.stderr, 'Islands found: ' + str(islands)
        return islands

    def has_unlinkable_islands(self):
        """ Checks if there are any islands that cannot be
        connected to the rest of thhe graph."""
        islands = self.find_connected_components()
        if len(islands) > 1:
            for island in islands:
                has_a_linkable_node = False
                for node in island:
                    if not self.is_filled(node):
                        has_a_linkable_node = True
                        break

                if not has_a_linkable_node:
                    print >> sys.stderr, 'Found an island that cannot be linked back: ' + str(island)
                    return True
        else:
            return False

    def rec_is_sol_ok(self, node, is_ok_dict):
        if not is_ok_dict[node]:
            is_ok_dict[node] = True
            for linked in self.adj_list[node]:
                # print >> sys.stderr, 'Found linked nodes: '+str(node)+ ' '  + str(linked)
                self.rec_is_sol_ok(linked, is_ok_dict)
        else:
            # We already processed this node before
            pass

    def nb_links(self, node1, node2):
        """ Returns the number of links between the two nodes. """
        linked_nodes = self.adj_list[node1]
        return linked_nodes.count(node2)

    def is_filled(self, node):
        nb_links = len(self.adj_list[node])
        return nb_links >= node.value

    def __repr__(self):
        return str(self.adj_list)

    def is_on_edge(self, node):
        """ Returns true if the noe is on an edge, false otherwise. """
        x = node.x
        y = node.y
        return x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1


def remove_obvious_solutions(graph, solutions):
    # First easy step: set the obivous ones:
    # 4s that are in corners
    # 6s that are on edges
    # 8s anywhere else
    corners = [(0, 0), (0, graph.height - 1), (width - 1, 0), (width - 1, height - 1)]
    for x, y in corners:
        node = graph.get_point(x, y)
        if node is not None and node.value == 4:
            for neighbor in node.neighbors:
                graph.add_link(node, neighbor)
                graph.add_link(node, neighbor)
                solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 2")
                # print node.to_solution_string()+" "+neighbor.to_solution_string() + " 2"

    # 8s and 6s
    for node in graph.adj_list:
        if node.value == 1:
            # Check if there is only one neighbor with value > 1
            neighbors_possible = [n for n in node.neighbors if n.value > 1]
            if len(neighbors_possible) == 1:
                neighbor = neighbors_possible[0]
                graph.add_link(node, neighbor)
                solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")
                # print node.to_solution_string()+" "+neighbor.to_solution_string() + " 1"

        if node.value == 6:
            if graph.is_on_edge(node):
                print >> sys.stderr, 'Linking node on edge with value 6: ' + str(node)
                for neighbor in node.neighbors:
                    if graph.nb_links(neighbor, node) == 0:
                        graph.add_link(node, neighbor)
                        graph.add_link(node, neighbor)
                        solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 2")
                        # print node.to_solution_string()+" "+neighbor.to_solution_string() + " 2"

        if node.value == 8:
            # add all the links
            for neighbor in node.neighbors:
                if graph.nb_links(neighbor, node) == 0:
                    print >> sys.stderr, 'Linking node with value 8: ' + str(node) + ' ' + str(neighbor)
                    graph.add_link(node, neighbor)
                    graph.add_link(node, neighbor)
                    # print node.to_solution_string()+" "+neighbor.to_solution_string() + " 2"
                    solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 2")

    print >> sys.stderr, 'Current graph: ' + str(graph)
    # now check all nodes that only have one possibility (i.e. nb_links = value - 1)
    print >> sys.stderr, 'Optimization phase: removing obvious solutions.'

    for x in xrange(2, 8):
        # Check the nodes which value is x ...
        node_x_values = [n for n in graph.adj_list if n.value == x]
        # ... and which has x - 1 links already. For example: Nodes with value 2 with 1 link already set.
        to_inspect = [m for m in node_x_values if graph.get_nb_links_node(m) == x - 1]
        had_mod = True
        while(had_mod):
            had_mod = False
            print >> sys.stderr, 'Value ' + str(x) + ': inspect list: ' + str(to_inspect)
            for node in to_inspect:
                unfilled_neighbors = [m for m in node.neighbors if not graph.is_filled(m)]
                unfilled_neighbors_linkable = [l for l in unfilled_neighbors if graph.nb_links(node, l) < 2]

                print >> sys.stderr, str(node) + ': Unfilled neighbors linkable: ' + str(unfilled_neighbors_linkable)
                if len(unfilled_neighbors_linkable) == 1:
                    had_mod = True
                    neighbor = unfilled_neighbors_linkable[0]
                    print >> sys.stderr, 'Found an optimization between ' + str(node) + ' and ' + str(neighbor)
                    graph.add_link(node, neighbor)
                    solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")
                    # print node.to_solution_string()+" "+neighbor.to_solution_string() + " 1"
                    to_inspect = [nd for nd in node_x_values if graph.get_nb_links_node(nd) == x - 1]
                else:

                    unfilled_neighbors_linkable = [t for t in unfilled_neighbors_linkable if graph.get_nb_links_node(t) != t.value - 1]
                    print >> sys.stderr, str(node) + ': Neighbors which have a 1 link possibility: ' + str(unfilled_neighbors_linkable)
                    if len(unfilled_neighbors_linkable) == 1:
                        had_mod = True
                        neighbor = unfilled_neighbors_linkable[0]
                        print >> sys.stderr, 'Found an optimization between ' + str(node) + ' and ' + str(neighbor)
                        graph.add_link(node, neighbor)
                        solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")
                        # print node.to_solution_string()+" "+neighbor.to_solution_string() + " 1"
                        to_inspect = [nd for nd in node_x_values if graph.get_nb_links_node(nd) == x - 1]
                    else:
                        # Filter those which value is not the current number
                        unfilled_neighbors_linkable = [t for t in unfilled_neighbors_linkable if t.value == x]
                        print >> sys.stderr, str(node) + ': Possible neighbors with value set to ' + str(x) + ': ' + str(unfilled_neighbors_linkable)
                        if len(unfilled_neighbors_linkable) == 1:
                            had_mod = True
                            neighbor = unfilled_neighbors_linkable[0]
                            print >> sys.stderr, 'Found an optimization between ' + str(node) + ' and ' + str(neighbor)
                            graph.add_link(node, neighbor)
                            # print node.to_solution_string()+" "+neighbor.to_solution_string() + " 1"
                            solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")
                            to_inspect = [nd for nd in node_x_values if graph.get_nb_links_node(nd) == x - 1]


def find_sol_main(graph):
    solutions = []
    remove_obvious_solutions(graph, solutions)
    print >> sys.stderr, 'Graph: ' + str(graph)
    print >> sys.stderr, 'Launching recursive search...'
    solutions.extend(find_sol(graph))

    # Final graph adj list debug
    print >> sys.stderr, 'Final graph: ' + str(graph)
    return solutions


def find_sol(graph):
    solution = []
    """ Returns the list of strings to print
    which are the links to create. """

    # List of all nodes which need links
    unfilled = [n for n in graph.adj_list if not graph.is_filled(n)]
    if len(unfilled) > 0:
        # Take node of lowest value: sort by value (ascending)
        # then take the first one.
        unfilled.sort(key=lambda x: x.value)
        node = unfilled[0]

        # Get one of its unfilled neighbors that has less than
        # 2 links from node
        unfilled_neighbors = [m for m in node.neighbors
                              if not graph.is_filled(m)]

        unfilled_neighbors_linkable = [l for l in unfilled_neighbors
                                       if graph.nb_links(node, l) < 2]
        # TODO check if link would cross another

        if len(unfilled_neighbors) > 0:
            # Sort neighbors by value, take the lowest one
            unfilled_neighbors.sort(key=lambda x: x.value)
            for neighbor in unfilled_neighbors_linkable:
                if graph.add_link(node, neighbor):
                    solution_string = node.to_solution_string() + " " +\
                        neighbor.to_solution_string() + " 1"
                    solution.append(solution_string)
                    rec_sol = find_sol(graph)
                    if rec_sol is not None:
                        solution.extend(rec_sol)
                        return solution

                    else:
                        # remove the link, we don't have a solution there
                        graph.remove_link(node, neighbor)
                        del solution[-1]
        else:
            return None
    else:
        if graph.check_if_solution_ok():
            return solution
        else:
            return None


width = int(raw_input())  # the number of cells on the X axis
height = int(raw_input())  # the number of cells on the Y axis
cell_matrix = []
for i in xrange(height):
    line = raw_input()  # width characters, each either a number or a '.'
    cell_matrix.append(line)

graph = Graph(cell_matrix, width, height)

print >> sys.stderr, str(graph)

solutions = find_sol_main(graph)

for s in solutions:
    print s
