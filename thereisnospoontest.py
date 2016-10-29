import unittest
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


if __name__ == '__main__':
    unittest.main()
