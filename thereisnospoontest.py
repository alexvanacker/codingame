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


if __name__ == '__main__':
    unittest.main()
