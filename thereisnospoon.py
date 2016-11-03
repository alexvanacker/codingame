import sys
import time


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
        assert width == len(cell_matrix[0])
        assert height == len(cell_matrix)
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

    def add_two_links(self, node1, node2):
        self.add_link(node1, node2)
        self.add_link(node1, node2)

    def add_link(self, node1, node2):
        # print >> sys.stderr, 'Adding link between '+str(node1)+' and ' + str(node2)
        if len(self.adj_list[node1]) >= node1.value:
            print >> sys.stderr, 'Cannot add a link between {} and {}: {} is filled.'.format(str(node1), str(node2), str(node1))
            return False
        if len(self.adj_list[node2]) >= node2.value:
            print >> sys.stderr, 'Cannot add a link between {} and {}: {} is filled with {}'.format(str(node1), str(node2), str(node2), str(self.adj_list[node2]))
            return False

        if self.adj_list[node1].count(node2) == 2:
            print >> sys.stderr, 'Already two links, cannot add more between {} and {}'.format(str(node1), str(node2))
            return False

        # if self.is_link_crossing_other_links(node1, node2):
        #     print >> sys.stderr, 'Link would cross another one, cannot add it.'
        #     return False

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

        for node, nodelist in self.adj_list.iteritems():
            for linked in nodelist:
                if self.is_link_crossing_other_links(node, linked):
                    return False
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

    def is_vertical_link_crossing(self, node1, node2):
        y_high = max(node1.y, node2.y)
        y_low = min(node1.y, node2.y)
        other_nodes = {k: v for (k, v) in self.adj_list.iteritems() if k is not node1 and k is not node2}
        # Remove those that are on the same axes: their links cannot cross
        # We do not check node2.x since it is assumed equal in this method.
        potential_crosses = {k: v for (k, v) in other_nodes.iteritems() if k.x != node1.x and k.y != node1.y and k.y != node2.y}
        for node, linked_nodes in potential_crosses.iteritems():
            # Check only horizontal links
            for linked_node in [l for l in linked_nodes if l.y == node.y]:
                y_link = node.y
                x_low = min(node.x, linked_node.x)
                x_max = max(node.x, linked_node.x)
                if y_link > y_low and y_link < y_high and node1.x > x_low and node1.x < x_max:
                    return True
        return False

    def is_horizontal_link_crossing(self, node1, node2):
        x_high = max(node1.x, node2.x)
        x_low = min(node1.x, node2.x)
        other_nodes = {k: v for (k, v) in self.adj_list.iteritems() if k is not node1 and k is not node2}
        # Remove those that are on the same axes: their links cannot cross
        # We do not check node2.y since it is assumed equal in this method.
        potential_crosses = {k: v for (k, v) in other_nodes.iteritems() if k.y != node1.y and k.x != node1.x and k.x != node2.x}
        for node, linked_nodes in potential_crosses.iteritems():
            # Check only vertical links
            for linked_node in [l for l in linked_nodes if l.x == node.x]:
                x_link = node.x
                y_low = min(node.y, linked_node.y)
                y_max = max(node.y, linked_node.y)
                if x_link > x_low and x_link < x_high and node1.y > y_low and node1.y < y_max:
                    return True
        return False

    def is_link_crossing_other_links(self, node1, node2):
        """ returns True if the link between two nodes
        crosses any other existing link in the graph.
        """
        if node1.x == node2.x:
            return self.is_vertical_link_crossing(node1, node2)
        else:
            return self.is_horizontal_link_crossing(node1, node2)

    def __repr__(self):
        return str(self.adj_list)

    def is_on_edge(self, node):
        """ Returns true if the noe is on an edge, false otherwise. """
        x = node.x
        y = node.y
        return x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1

    def link_will_not_create_an_island(self, node1, node2):
        """ Returns True of the link will not cut off part of the graph. """
        # Add the link in the graph
        self.add_link(node1, node2)
        result = False
        linked_to_node1_dict = self.depth_first_search(node1)
        linked_to_node1 = {k for (k, v) in linked_to_node1_dict.iteritems() if v}
        # If all nodes are connected, the island is the graph, so we're ok
        if len(linked_to_node1) == len(self.adj_list):
            result = True
        else:
            # Check that all the linked are not filled
            all_linked_are_filled = True
            for node in linked_to_node1:
                if self.get_nb_links_node(node) < node.value:
                    all_linked_are_filled = False
                    break
            result = not all_linked_are_filled

        # Remove the link for now
        self.remove_link(node1, node2)
        return result


def add_obvious_links(graph):
    """ Returns list of links which are obvious. If an error occurs, returns None.
    If there are no obvious links to add, returns an empty list.

    """
    solutions = []
    original_graph = graph
    has_mod = True
    while has_mod:
        has_mod = False
        for node in [n for n in graph.adj_list if graph.get_nb_links_node(n) < n.value]:

            # Number of links to set
            nb_links_to_set = node.value - graph.get_nb_links_node(node)
            if nb_links_to_set != 0:

                # Number of possible neighbors
                possible_neighbors = [neighbor for neighbor in node.neighbors if graph.get_nb_links_node(neighbor) < neighbor.value and
                                      graph.nb_links(node, neighbor) < 2]

                if len(possible_neighbors) == 1:
                    neighbor = possible_neighbors[0]
                    # Only one possible neighbor, let's add as many links as we can. If there is an error, return False
                    print >> sys.stderr, 'Obvious link to set between {} and {}, with {} links'.format(str(node), str(neighbor), str(nb_links_to_set))
                    for i in xrange(nb_links_to_set):
                        if graph.add_link(node, neighbor):
                            has_mod = True
                            solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")
                        else:
                            # There was en error, when only one possible neighbor is remaining.
                            # The graph is not a possible solution.
                            graph = original_graph
                            return None

                else:
                    if nb_links_to_set == 1:
                        # Check neighbors which, if we add the link, do not create an island
                        possible_neighbors = [n for n in possible_neighbors if graph.link_will_not_create_an_island(node, n)]
                        if len(possible_neighbors) == 1:
                            neighbor = possible_neighbors[0]
                            # Only one possible neighbor, let's add as many links as we can. If there is an error, return False
                            print >> sys.stderr, 'Obvious link to set between {} and {} as only possibility without island creation.'.format(str(node), str(neighbor))
                            for i in xrange(nb_links_to_set):
                                if graph.add_link(node, neighbor):
                                    has_mod = True
                                    solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")
                                else:
                                    # There was en error, when only one possible neighbor is remaining.
                                    # The graph is not a possible solution.
                                    graph = original_graph
                                    return None

    return solutions


def remove_obvious_solutions(graph, solutions):
    print >> sys.stderr, 'Optimization phase: removing obvious solutions.'
    # First easy step: set the obivous ones:
    # 3s and 4s that are in corners
    # 5s and 6s that are on edges
    # 7s and 8s anywhere else
    corners = [(0, 0), (0, graph.height - 1), (graph.width - 1, 0), (graph.width - 1, graph.height - 1)]
    for x, y in corners:
        node = graph.get_point(x, y)
        if node is not None and node.value == 4:
            for neighbor in node.neighbors:
                nb_links = graph.nb_links(node, neighbor)
                if nb_links == 0:
                    graph.add_two_links(node, neighbor)
                    solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")
                    solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")
                elif nb_links == 1:
                    graph.add_link(node, neighbor)
                    solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")

        # If a 3 is in a corner, it will at least have 1 link going in the two possible directions.
        if node is not None and node.value == 3:
            for neighbor in node.neighbors:
                nb_links = graph.nb_links(node, neighbor)
                if nb_links == 0:
                    if graph.add_link(node, neighbor):
                        solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")

    for node in graph.adj_list:
        if node.value == 1:
            # Check if there is only one neighbor with value > 1
            neighbors_possible = [n for n in node.neighbors if n.value > 1]
            if len(neighbors_possible) == 1:
                neighbor = neighbors_possible[0]
                if graph.nb_links(node, neighbor) == 0:
                    if graph.add_link(node, neighbor):
                        solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")
                # print node.to_solution_string()+" "+neighbor.to_solution_string() + " 1"

        if node.value == 5 and graph.is_on_edge(node):
            # A 5 on an edge will have at least one link going from each direction.
            for neighbor in node.neighbors:
                if graph.nb_links(neighbor, node) == 0:
                    if graph.add_link(node, neighbor):
                        solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")

        if node.value == 6 and graph.is_on_edge(node):
                for neighbor in node.neighbors:
                    nb_links_between_the_two = graph.nb_links(neighbor, node)
                    if nb_links_between_the_two == 0:
                        graph.add_two_links(node, neighbor)
                        solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")
                        solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")

                    elif nb_links_between_the_two == 1:
                        # Only one link can be placed
                        graph.add_link(node, neighbor)
                        solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")

        if node.value == 7:
            # Any node with a 7 will have at least one link going in each direction.
            for neighbor in node.neighbors:
                nb_links_between_the_two = graph.nb_links(neighbor, node)
                if nb_links_between_the_two == 0:
                    if graph.add_link(node, neighbor):
                        solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")

        if node.value == 8:
            # add all the links
            for neighbor in node.neighbors:
                nb_links_between_the_two = graph.nb_links(neighbor, node)
                if nb_links_between_the_two == 0:
                    graph.add_two_links(node, neighbor)
                    solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")
                    solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")

                elif nb_links_between_the_two == 1:
                    # Only one link can be placed
                    if graph.add_link(node, neighbor):
                        solutions.append(node.to_solution_string() + " " + neighbor.to_solution_string() + " 1")

    print >> sys.stderr, 'Current graph: ' + str(graph)
    # now check all nodes that only have one possibility (i.e. nb_links = value - 1)

    solutions.extend(add_obvious_links(graph))

    print >> sys.stderr, 'End of optimizations.'


def find_sol_main(graph):
    solutions = []
    start_optim = time.clock()
    remove_obvious_solutions(graph, solutions)
    time_optim = time.clock() - start_optim
    print >> sys.stderr, 'Time for optimization: ' + str(time_optim)
    print >> sys.stderr, 'Graph: ' + str(graph)
    print >> sys.stderr, 'Launching recursive search...'

    start_rec = time.clock()
    rec_solutions = find_sol(graph)
    assert rec_solutions is not None
    solutions.extend(rec_solutions)
    time_rec = time.clock() - start_rec
    print >> sys.stderr, 'Time for recursive search: ' + str(time_rec)

    # Final graph adj list debug
    print >> sys.stderr, 'Final graph: ' + str(graph)
    return solutions


def choose_node_to_process(graph):
    """ Returns the node on which we will try to add a link.
    If all nodes are filled, returns None.
    """
    unfilled = [n for n in graph.adj_list if not graph.is_filled(n)]
    if len(unfilled) > 0:
        # sort by number of possible links
        # to place ascending
        unfilled.sort(key=lambda x: x.value - len(graph.adj_list[x]))
        return unfilled[0]

    else:
        return None


def find_sol(graph, depth=0):
    solution = []
    """ Returns the list of strings to print
    which are the links to create. """
    obvious_sols = add_obvious_links(graph)
    if obvious_sols is not None:
        solution.extend(obvious_sols)
    else:
        print >> sys.stderr, 'Failure to add obvious links, current graph is incorrent'
        print >> sys.stderr, str(graph)
        return None

    node = choose_node_to_process(graph)
    if node is not None:
        # Get one of its unfilled neighbors that has less than
        # 2 links from node
        unfilled_neighbors = [m for m in node.neighbors
                              if not graph.is_filled(m)]

        unfilled_neighbors_linkable = [l for l in unfilled_neighbors
                                       if graph.nb_links(node, l) < 2 and graph.link_will_not_create_an_island(node, l)]

        if len(unfilled_neighbors_linkable) > 0:
            # Sort neighbors by value, take the lowest one
            unfilled_neighbors_linkable.sort(key=lambda x: x.value - len(graph.adj_list[x]))

            for neighbor in unfilled_neighbors_linkable:
                if graph.add_link(node, neighbor):
                    print >> sys.stderr, 'Recursive step: added link from ' + str(node) + ' to ' + str(neighbor)
                    solution_string = node.to_solution_string() + " " +\
                        neighbor.to_solution_string() + " 1"
                    solution.append(solution_string)
                    rec_sol = find_sol(graph, depth=depth + 1)
                    if rec_sol is not None:
                        solution.extend(rec_sol)
                        return solution

                    else:
                        # remove the link, we don't have a solution there
                        graph.remove_link(node, neighbor)
                        print >> sys.stderr, 'Recursive step: removing link from ' + str(node) + ' to ' + str(neighbor)
                        del solution[-1]

            # If we iterated on all neighbors but None could bring a solution,
            # it means there was a problem before, so return None.
            # print >> sys.stderr, 'No neighbors possible to link, solution is incorrect.'
            return None
        else:
            # The current node being processed has unfilled links,
            # but no available neighbors: this is not a suitable
            # solution.
            # print >> sys.stderr, 'No neighbors possible to link, solution is incorrect.'
            return None
    else:
        if graph.check_if_solution_ok():
            return solution
        else:
            # print >> sys.stderr, 'Solution was not correct, backtracking'
            return None


def main():
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


if __name__ == '__main__':
    main()
