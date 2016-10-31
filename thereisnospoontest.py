import unittest
import sys
import thereisnospoon as tisn


class TestThereIsNoSpoon(unittest.TestCase):

    def test_detect_crossed_links(self):
        cell_matrix = ['..1..1',
                       '......',
                       '1...1.',
                       '......',
                       '..1..1']
        width = 6
        height = 5
        graph = tisn.Graph(cell_matrix, width, height)

        n1 = graph.get_point(2, 0)
        n2 = graph.get_point(2, 4)
        graph.add_link(n1, n2)
        n3 = graph.get_point(0, 2)
        n4 = graph.get_point(4, 2)
        graph.add_link(n3, n4)
        crosses = graph.is_link_crossing_other_links(n1, n2)
        self.assertTrue(crosses)
        same_cross = graph.is_link_crossing_other_links(n3, n4)
        self.assertTrue(same_cross)

    def test_no_cross(self):
        cell_matrix = ['..1..1',
                       '......',
                       '1...1.',
                       '......',
                       '..1..1']
        width = 6
        height = 5
        graph = tisn.Graph(cell_matrix, width, height)

        n1 = graph.get_point(0, 2)
        n2 = graph.get_point(4, 2)
        graph.add_link(n1, n2)
        n3 = graph.get_point(5, 0)
        n4 = graph.get_point(5, 4)
        graph.add_link(n3, n4)
        self.assertFalse(graph.is_link_crossing_other_links(n1, n2))

    def test_simple(self):
        cell_matrix = ['1.3',
                       '...',
                       '123']
        width = len(cell_matrix[0])
        height = len(cell_matrix)
        graph = tisn.Graph(cell_matrix, width, height)
        solutions = tisn.find_sol_main(graph)
        n1 = graph.get_point(0, 0)
        n2 = graph.get_point(2, 0)
        self.assertEquals(1, graph.nb_links(n1, n2), 'There should be only one link between ' + str(n1) + ' and ' + str(n2))
        self.assertEquals(5, len(solutions), 'There should be only 5 links to place, found ' + str(len(solutions)))

    def test_basic(self):
        cell_matrix = ['14.3',
                       '....',
                       '.4.4']
        width = 4
        height = 3
        graph = tisn.Graph(cell_matrix, width, height)
        solutions = tisn.find_sol_main(graph)
        n1 = graph.get_point(0, 3)
        n2 = graph.get_point(2, 3)
        self.assertEquals(8, len(solutions))

    def test_intermediate_three(self):
        print >> sys.stderr, 'Testing intermediate 3'
        cell_matrix = ['25.1',
                       '47.4',
                       '..1.',
                       '3344']
        width = 4
        height = 4
        graph = tisn.Graph(cell_matrix, width, height)
        solutions = tisn.find_sol_main(graph)
        self.assertTrue(solutions is not None)


if __name__ == '__main__':
    unittest.main()
