import unittest

import easygraph as eg
import easygraph.functions.graph_embedding as fn
import numpy as np


class Test_Nobe(unittest.TestCase):
    def setUp(self):
        self.ds = eg.datasets.get_graph_karateclub()
        self.edges = [(1, 4), (2, 4), (4, 1), (0, 4), (4, 3)]
        self.test_directed_graphs = [eg.DiGraph()]
        self.test_undirected_graphs = [eg.Graph(self.edges)]
        self.test_directed_graphs.append(eg.classes.DiGraph(self.edges))
        self.shs = eg.common_greedy(self.ds, int(len(self.ds.nodes) / 3))

    def test_NOBE(self):
        fn.NOBE(self.test_undirected_graphs[0], 1)

    def test_NOBE_GA(self):
        """
        for i in self.test_graphs:
            eg.functions.NOBE_GA(i, K=1)
            print(i)
        """
        fn.NOBE_GA(self.test_directed_graphs[1], 1)


if __name__ == "__main__":
    unittest.main()
