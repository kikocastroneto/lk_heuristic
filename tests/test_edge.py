import unittest
from lk_heuristic.models.node import Node2D, Node3D
from lk_heuristic.models.edge import Edge


class TestEdge(unittest.TestCase):
    """
    A class to perform testing on TSP edges
    """

    def setUp(self):
        """
        The method to be performed before every test. Used to setup some edges
        """

        # initialize 2D test nodes
        node_2d_1 = Node2D(0, 1)
        node_2d_1.id = 0
        node_2d_2 = Node2D(1, 0)
        node_2d_2.id = 1
        node_2d_3 = Node2D(0, 1)
        node_2d_3.id = 2

        #  a test edge
        self.edge_2d_1 = Edge(node_2d_1, node_2d_2)

        # an equal edge
        self.edge_2d_equal_1 = Edge(node_2d_1, node_2d_2)

        # the reversed edge
        self.edge_2d_reversed_1 = Edge(node_2d_2, node_2d_1)

        # edge with different node id
        self.edge_2d_almost_equal_1 = Edge(node_2d_1, node_2d_3)

        # initialize 3D test nodes
        node_3d_1 = Node3D(0, 1, 0)
        node_3d_1.id = 0
        node_3d_2 = Node3D(1, 0, 0)
        node_3d_2.id = 1
        node_3d_3 = Node3D(0, 1, 0)
        node_3d_3.id = 2

        #  a test edge
        self.edge_3d_1 = Edge(node_3d_1, node_3d_2)

        # an equal edge
        self.edge_3d_equal_1 = Edge(node_3d_1, node_3d_2)

        # the reversed edge
        self.edge_3d_reversed_1 = Edge(node_3d_2, node_3d_1)

        # edge with different node id
        self.edge_3d_almost_equal_1 = Edge(node_3d_1, node_3d_3)

    def test_edge_2d_equality(self):
        """
        Testing edge equality.
        """

        # equal edges
        self.assertEqual(self.edge_2d_1, self.edge_2d_equal_1)

        # edge (n1,n2) must be equal to edge (n2,n1) if ids are the same
        self.assertEqual(self.edge_2d_1, self.edge_2d_reversed_1)

        # edge (n1,n2) not equal to edge (n2,n1) if ids are not the same
        self.assertNotEqual(self.edge_2d_1, self.edge_2d_almost_equal_1)

    def test_edge_2d_valid(self):
        """
        Testing if edge is valid
        """

        # an edge isn't valid if both nodes are equal (it must connect different nodes)
        node = Node2D(1, 0)
        self.assertRaises(AssertionError, Edge, node, node)

    def test_edge_3d_equality(self):
        """
        Testing edge equality.
        """

        # equal edges
        self.assertEqual(self.edge_3d_1, self.edge_3d_equal_1)

        # edge (n1,n2) must be equal to edge (n2,n1) if ids are the same
        self.assertEqual(self.edge_3d_1, self.edge_3d_reversed_1)

        # edge (n1,n2) not equal to edge (n2,n1) if ids are not the same
        self.assertNotEqual(self.edge_3d_1, self.edge_3d_almost_equal_1)

    def test_edge_3d_valid(self):
        """
        Testing if edge is valid
        """

        # an edge isn't valid if both nodes are equal (it must connect different nodes)
        node = Node3D(1, 0, 0)
        self.assertRaises(AssertionError, Edge, node, node)
