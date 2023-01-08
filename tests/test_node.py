import unittest
from lk_heuristic.models.node import Node2D, Node3D


class TestNode(unittest.TestCase):
    """
    A class to perform testing on TSP nodes
    """

    def setUp(self):
        """
        The method to be performed before every test. Used to setup some nodes
        """

        # initialize for 2D nodes
        # a test node
        self.node_2d_1 = Node2D(0, 1)
        self.node_2d_1.id = 0

        # same node 1 creation
        self.node_2d_equal_1 = Node2D(0, 1)
        self.node_2d_equal_1.id = 0

        # a different node coordinates
        self.node_2d_2 = Node2D(2, 3)
        self.node_2d_2.id = 1

        # create same node coords, but change the id
        self.node_2d_almost_equal_1 = Node2D(0, 1)
        self.node_2d_almost_equal_1.id = 2

        # an empty node
        self.node_2d_empty = None

        # a reversed coordinate node
        self.node_2d_reversed_1 = Node2D(1, 0)
        self.node_2d_reversed_1.id = 3

        # initialize for 3D nodes
        # a test node
        self.node_3d_1 = Node3D(0, 1, 2)
        self.node_3d_1.id = 0

        # same node 1 creation
        self.node_3d_equal_1 = Node3D(0, 1, 2)
        self.node_3d_equal_1.id = 0

        # a different node coordinates
        self.node_3d_2 = Node3D(1, 1, 2)
        self.node_3d_2.id = 1

        # create same node coords, but change the id
        self.node_3d_almost_equal_1 = Node3D(0, 1, 2)
        self.node_3d_almost_equal_1.id = 2

        # an empty node
        self.node_3d_empty = None

        # a reversed coordinate node
        self.node_3d_reversed_1 = Node3D(2, 1, 0)
        self.node_3d_reversed_1.id = 3

        # almost similar nodes
        self.node_3d_same_x_y_1 = Node3D(0, 1, 3)
        self.node_3d_same_x_y_1.id = 4
        self.node_3d_same_y_z_1 = Node3D(3, 1, 2)
        self.node_3d_same_y_z_1.id = 5
        self.node_3d_same_x_z_1 = Node3D(0, 3, 2)
        self.node_3d_same_x_z_1.id = 6

    def test_node_2d_equality(self):
        """
        Testing node equality.
        """

        # similar node coords and ids, but different instances
        self.assertEqual(self.node_2d_1, self.node_2d_equal_1)

        # different node coords, but same id
        self.assertNotEqual(self.node_2d_1, self.node_2d_2)

        # same node coords, but different id
        self.assertNotEqual(self.node_2d_1, self.node_2d_almost_equal_1)

        # equality with an empty node
        self.assertNotEqual(self.node_2d_1, self.node_2d_empty)

        # reversed (x,y) coord values
        self.assertNotEqual(self.node_2d_1, self.node_2d_reversed_1)

    def test_node_2d_gt(self):
        """
        Testing node size comparison (greater than).
        """

        # different node coords
        self.assertLess(self.node_2d_1, self.node_2d_2)

        # reversed node coords
        self.assertLess(self.node_2d_1, self.node_2d_reversed_1)

    def test_node_3d_equality(self):
        """
        Testing node equality.
        """

        # similar node coords and ids, but different instances
        self.assertEqual(self.node_3d_1, self.node_3d_equal_1)

        # different node coords, but same id
        self.assertNotEqual(self.node_3d_1, self.node_3d_2)

        # same node coords, but different id
        self.assertNotEqual(self.node_3d_1, self.node_3d_almost_equal_1)

        # equality with an empty node
        self.assertNotEqual(self.node_3d_1, self.node_3d_empty)

        # reversed (x,y,z) coord values
        self.assertNotEqual(self.node_3d_1, self.node_3d_reversed_1)

        # 2 coords equal but one is different
        self.assertNotEqual(self.node_3d_1, self.node_3d_same_x_y_1)
        self.assertNotEqual(self.node_3d_1, self.node_3d_same_y_z_1)
        self.assertNotEqual(self.node_3d_1, self.node_3d_same_x_z_1)

    def test_node_3d_gt(self):
        """
        Testing node size comparison (greater than).
        """

        # different node coords
        self.assertLess(self.node_3d_1, self.node_3d_2)

        # reversed node coords
        self.assertLess(self.node_3d_1, self.node_3d_reversed_1)
