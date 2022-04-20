import unittest
from models.node import Node2D
from models.tour import Tour


class TestTour(unittest.TestCase):
    """
    A class to perform testing on TSP tours
    """

    def setUp(self):

        # create hexagon 2D nodes (sequenced at best cost)
        self.hexagon_nodes = [Node2D(1, 3), Node2D(1.5, 2.5), Node2D(2, 2), Node2D(2, 1), Node2D(2, 0), Node2D(1.5, -0.5), Node2D(1, -1), Node2D(0.5, -0.5), Node2D(0, 0), Node2D(0, 1), Node2D(0, 2), Node2D(0.5, 2.5)]

        # create the tour using the nodes
        self.tour = Tour(self.hexagon_nodes)

    def test_total_nodes(self):
        """
        Test the number of nodes created in the tour, making sure all nodes were added to nodes list
        """

        self.assertEqual(len(self.tour.nodes), 12)

    def test_total_edges(self):
        """
        Test the number of edges created in the tour, making sure all edges were added to the edges set
        """

        self.assertEqual(len(self.tour.edges), 12)

    def test_swap_feasibility(self):
        """
        Test the feasibility validation procedure (before the swap itself). Feasible swap is a valid swap executed in a feasible tour that results in another feasible tour. Invalid swaps will make either an unfeasible tour (two separated segments) or an impossible tour (when repeated nodes are used at swap operation)
        """

        # all checks are done in both directions (i.e, t2 == t1.succ or t2 == t1.pred)
        # a feasible swap must be t1-t2-t4-t3
        self.assertTrue(self.tour.is_swap_feasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[6], self.tour.nodes[5]))
        self.assertTrue(self.tour.is_swap_feasible(self.tour.nodes[0], self.tour.nodes[11], self.tour.nodes[5], self.tour.nodes[6]))

        # a swap t1-t2-t3-t4 is unfeasible because it creates two separated tours
        self.assertFalse(self.tour.is_swap_feasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[5], self.tour.nodes[6]))
        self.assertFalse(self.tour.is_swap_feasible(self.tour.nodes[0], self.tour.nodes[11], self.tour.nodes[6], self.tour.nodes[5]))

        # a swap is impossible if any node is equal to other node in the swap operation
        self.assertFalse(self.tour.is_swap_feasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[1], self.tour.nodes[2]))
        self.assertFalse(self.tour.is_swap_feasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[-1], self.tour.nodes[0]))

    def test_swap_unfeasibility(self):
        """
        Test the unfeasibility validation procedure (before the swap itself). Unfeasible swap is valid swap executed in a feasible tour that results in an unfeasible tour (two separated tours).
        """

        # all checks are done in both directions (i.e, t2 == t1.succ or t2 == t1.pred)
        # an unfeasible swap must be t1-t2-t3-t4
        self.assertTrue(self.tour.is_swap_unfeasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[5], self.tour.nodes[6]))
        self.assertTrue(self.tour.is_swap_unfeasible(self.tour.nodes[0], self.tour.nodes[11], self.tour.nodes[6], self.tour.nodes[5]))

        # a swap t1-t2-t4-t3 is feasible because it creates a valid tour
        self.assertFalse(self.tour.is_swap_unfeasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[6], self.tour.nodes[5]))
        self.assertFalse(self.tour.is_swap_unfeasible(self.tour.nodes[0], self.tour.nodes[11], self.tour.nodes[5], self.tour.nodes[6]))

        # a swap is impossible if any node is equal to other node in the swap operation
        self.assertFalse(self.tour.is_swap_unfeasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[1], self.tour.nodes[2]))
        self.assertFalse(self.tour.is_swap_unfeasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[-1], self.tour.nodes[0]))

    def test_swap_feasible(self):
        """
        Test the 2-Opt feasible swap from an feasible tour to another feasible one. Checking is done so that a swap is made and unmade to return in the original state.
        """

        # execute swap
        # initial tour = 0-1-2-3-4-5-6-7-8-9-10-11
        # swap tour = 0-11-10-9-8-1-2-3-4-5-6-7 (the segment between 0 and 8 is reversed)
        self.tour.swap_feasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[8], self.tour.nodes[7])

        # checking all nodes pos values
        self.assertEqual(self.tour.nodes[0].pos, -4)
        self.assertEqual(self.tour.nodes[1].pos, 1)
        self.assertEqual(self.tour.nodes[2].pos, 2)
        self.assertEqual(self.tour.nodes[3].pos, 3)
        self.assertEqual(self.tour.nodes[4].pos, 4)
        self.assertEqual(self.tour.nodes[5].pos, 5)
        self.assertEqual(self.tour.nodes[6].pos, 6)
        self.assertEqual(self.tour.nodes[7].pos, 7)
        self.assertEqual(self.tour.nodes[8].pos, 0)
        self.assertEqual(self.tour.nodes[9].pos, -1)
        self.assertEqual(self.tour.nodes[10].pos, -2)
        self.assertEqual(self.tour.nodes[11].pos, -3)

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[10])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[0])

        # undo the swap
        # this also test the condition where "pos" attribute assumes negative values
        # initial tour = 0-11-10-9-8-1-2-3-4-5-6-7
        # swap tour =  0-1-2-3-4-5-6-7-8-9-10-11 (the segment between 0 and 1 is reversed)
        self.tour.swap_feasible(self.tour.nodes[7], self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[8])

        # checking all nodes pos values
        # the pos attribute don't reset to original values, but they match the node sequence
        self.assertEqual(self.tour.nodes[0].pos, 0)
        self.assertEqual(self.tour.nodes[1].pos, 1)
        self.assertEqual(self.tour.nodes[2].pos, 2)
        self.assertEqual(self.tour.nodes[3].pos, 3)
        self.assertEqual(self.tour.nodes[4].pos, 4)
        self.assertEqual(self.tour.nodes[5].pos, 5)
        self.assertEqual(self.tour.nodes[6].pos, 6)
        self.assertEqual(self.tour.nodes[7].pos, 7)
        self.assertEqual(self.tour.nodes[8].pos, -4)
        self.assertEqual(self.tour.nodes[9].pos, -3)
        self.assertEqual(self.tour.nodes[10].pos, -2)
        self.assertEqual(self.tour.nodes[11].pos, -1)

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # execute a new swap where t1-t2-t4-t3 are all neighbor nodes
        # initial tour =  0-1-2-3-4-5-6-7-8-9-10-11
        # swap tour =  0-2-1-3-4-5-6-7-8-9-10-11 (the segment between 1 and 2 is reversed)
        self.tour.swap_feasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[3], self.tour.nodes[2])

        # checking all nodes pos values
        self.assertEqual(self.tour.nodes[0].pos, 0)
        self.assertEqual(self.tour.nodes[1].pos, 2)
        self.assertEqual(self.tour.nodes[2].pos, 1)
        self.assertEqual(self.tour.nodes[3].pos, 3)
        self.assertEqual(self.tour.nodes[4].pos, 4)
        self.assertEqual(self.tour.nodes[5].pos, 5)
        self.assertEqual(self.tour.nodes[6].pos, 6)
        self.assertEqual(self.tour.nodes[7].pos, 7)
        self.assertEqual(self.tour.nodes[8].pos, -4)
        self.assertEqual(self.tour.nodes[9].pos, -3)
        self.assertEqual(self.tour.nodes[10].pos, -2)
        self.assertEqual(self.tour.nodes[11].pos, -1)

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # execute a new swap where t2 is the predecessor of t1
        # initial tour =  0-2-1-3-4-5-6-7-8-9-10-11
        # swap tour =  0-2-1-3-4-5-6-11-10-9-8-7 (the segment between 11 and 7 is reversed)
        self.tour.swap_feasible(self.tour.nodes[0], self.tour.nodes[11], self.tour.nodes[6], self.tour.nodes[7])

        # checking all nodes pos values
        self.assertEqual(self.tour.nodes[0].pos, 0)
        self.assertEqual(self.tour.nodes[1].pos, 2)
        self.assertEqual(self.tour.nodes[2].pos, 1)
        self.assertEqual(self.tour.nodes[3].pos, 3)
        self.assertEqual(self.tour.nodes[4].pos, 4)
        self.assertEqual(self.tour.nodes[5].pos, 5)
        self.assertEqual(self.tour.nodes[6].pos, 6)
        self.assertEqual(self.tour.nodes[7].pos, -1)
        self.assertEqual(self.tour.nodes[8].pos, -2)
        self.assertEqual(self.tour.nodes[9].pos, -3)
        self.assertEqual(self.tour.nodes[10].pos, -4)
        self.assertEqual(self.tour.nodes[11].pos, -5)

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[10])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[6])

    def test_swap_unfeasible(self):
        """
        Test the unfeasible 2-Opt swap where 2 disconnected tours are created. Checking is done so that a swap is made and unmade to return in the original state.
        """

        # execute swap
        # initial tour = 0-1-2-3-4-5-6-7-8-9-10-11
        # swap tour = two disconnected tours: 0-1-2-3-4-5 / 6-7-8-9-10-11
        # unfeasible swap does not change pos attribute, so this is not checked (like in feasible swap)
        self.tour.swap_unfeasible(self.tour.nodes[11], self.tour.nodes[0], self.tour.nodes[5], self.tour.nodes[6])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[6])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # undo the swap
        # initial tour = two disconnected tours: 0-1-2-3-4-5 / 6-7-8-9-10-11
        # swap tour = 0-1-2-3-4-5-6-7-8-9-10-11
        self.tour.swap_unfeasible(self.tour.nodes[6], self.tour.nodes[11], self.tour.nodes[0], self.tour.nodes[5])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # execute swap (with t2 = t1.pred to check reversed order)
        # initial tour = 0-1-2-3-4-5-6-7-8-9-10-11
        # swap tour = two disconnected tours: 0-1-2-3-4-5 / 6-7-8-9-10-11
        # unfeasible swap does not change pos attribute, so this is not checked (like in feasible swap)
        self.tour.swap_unfeasible(self.tour.nodes[0], self.tour.nodes[11], self.tour.nodes[6], self.tour.nodes[5])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[6])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # undo the swap
        # initial tour = two disconnected tours: 0-1-2-3-4-5 / 6-7-8-9-10-11
        # swap tour = 0-1-2-3-4-5-6-7-8-9-10-11
        self.tour.swap_unfeasible(self.tour.nodes[6], self.tour.nodes[11], self.tour.nodes[0], self.tour.nodes[5])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

    def test_swap_node_between_t2_t3(self):
        """
        Test the node swap between t2-t3, from an unfeasible tour to a feasible one. Checking is done so that a swap is made and unmade to return in the original state.
        """

        # execute initial unfeasible swap
        # initial tour = 0-1-2-3-4-5-6-7-8-9-10-11
        # swap tour = two disconnected tours: 1-2-3-4-5 / 0-6-7-8-9-10-11
        self.tour.swap_unfeasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[5], self.tour.nodes[6])

        # swap is executed to a feasible tour (t4 after t1 / t6 after t5)
        # initial tour = 1-2-3-4-5 / 0-6-7-8-9-10-11
        # swap tour: 0-4-5-1-2-3-6-7-8-9-10-11
        self.tour.swap_node_between_t2_t3(self.tour.nodes[0], self.tour.nodes[6], self.tour.nodes[3], self.tour.nodes[4])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # # undo the swap returning to an unfeasible tour
        # initial tour: 0-4-5-1-2-3-6-7-8-9-10-11
        # swap tour = 1-2-3-4-5 / 0-6-7-8-9-10-11
        self.tour.swap_node_between_t2_t3(self.tour.nodes[0], self.tour.nodes[4], self.tour.nodes[3], self.tour.nodes[6])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # undo the swap returning to a feasible tour
        # initial tour = 0-1-2-3-4-5 / 6-7-8-9-10-11
        # swap tour: 0-1-2-3-4-5-6-7-8-9-10-11
        self.tour.swap_unfeasible(self.tour.nodes[5], self.tour.nodes[1], self.tour.nodes[0], self.tour.nodes[6])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # execute initial unfeasible swap
        # initial tour = 0-1-2-3-4-5-6-7-8-9-10-11
        # swap tour = two disconnected tours: 1-2-3-4-5 / 0-6-7-8-9-10-11
        self.tour.swap_unfeasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[5], self.tour.nodes[6])

        # swap is executed to a feasible tour (t4 after t1 / t5 after t6)
        # initial tour = 1-2-3-4-5 / 0-6-7-8-9-10-11
        # swap tour: 0-3-2-1-5-4-6-7-8-9-10-11
        self.tour.swap_node_between_t2_t3(self.tour.nodes[0], self.tour.nodes[6], self.tour.nodes[4], self.tour.nodes[3])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # swap is executed to an unfeasible tour
        # initial tour: 0-3-2-1-5-4-6-7-8-9-10-11
        # swap tour = 1-2-3-4-5 / 0-6-7-8-9-10-11
        self.tour.swap_node_between_t2_t3(self.tour.nodes[0], self.tour.nodes[3], self.tour.nodes[4], self.tour.nodes[6])

        # swap is executed to a feasible tour (t1 after t4 / t5 after t6)
        # initial tour = 1-2-3-4-5 / 0-6-7-8-9-10-11
        # swap tour: 0-4-5-1-2-3-6-7-8-9-10-11
        self.tour.swap_node_between_t2_t3(self.tour.nodes[6], self.tour.nodes[0], self.tour.nodes[4], self.tour.nodes[3])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # swap is executed to an ufeasible tour
        # initial tour: 0-4-5-1-2-3-6-7-8-9-10-11
        # swap tour = 1-2-3-4-5 / 0-6-7-8-9-10-11
        self.tour.swap_node_between_t2_t3(self.tour.nodes[6], self.tour.nodes[3], self.tour.nodes[4], self.tour.nodes[0])

        # swap is executed to a feasible tour (t1 after t4 / t6 after t5)
        # initial tour = 1-2-3-4-5 / 0-6-7-8-9-10-11
        # swap tour: 0-3-2-1-5-4-6-7-8-9-10-11
        self.tour.swap_node_between_t2_t3(self.tour.nodes[6], self.tour.nodes[0], self.tour.nodes[3], self.tour.nodes[4])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

    def test_swap_node_between_t1_t4(self):
        """
        Test the node swap between t1 and t4, from an unfeasible tour to another unfeasible one. Checking is done so that a swap is made and unmade to return in the original state.
        """

        # execute initial unfeasible swap
        # initial tour = 0-1-2-3-4-5-6-7-8-9-10-11
        # swap tour = two disconnected tours: 1-2-3-4-5 / 0-6-7-8-9-10-11
        self.tour.swap_unfeasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[5], self.tour.nodes[6])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # execute t5 swap (t4 after t1 and t5 after t6)
        # initial tour = two disconnected tours: 1-2-3-4-5 / 0-6-7-8-9-10-11
        # swap tour = two disconnected tours: 1-2-3-4-5 / 0-8-7-6-9-10-11
        # self.tour.swap_node_between_t1_t4(self.tour.nodes[0], self.tour.nodes[6], self.tour.nodes[9], self.tour.nodes[8])
        self.tour.swap_feasible(self.tour.nodes[0], self.tour.nodes[6], self.tour.nodes[9], self.tour.nodes[8])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # undo the swap
        # initial tour = two disconnected tours: 1-2-3-4-5 / 0-8-7-6-9-10-11
        # swap tour = two disconnected tours: 1-2-3-4-5 / 0-6-7-8-9-10-11
        self.tour.swap_feasible(self.tour.nodes[0], self.tour.nodes[8], self.tour.nodes[9], self.tour.nodes[6])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # execute t5 swap (t1 after t4 and t6 after t5)
        # initial tour = two disconnected tours: 1-2-3-4-5 / 0-6-7-8-9-10-11
        # swap tour = two disconnected tours: 1-2-3-4-5 / 0-8-7-6-9-10-11
        self.tour.swap_feasible(self.tour.nodes[6], self.tour.nodes[0], self.tour.nodes[8], self.tour.nodes[9])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

        # undo the swap
        # initial tour = two disconnected tours: 1-2-3-4-5 / 0-8-7-6-9-10-11
        # swap tour = two disconnected tours: 1-2-3-4-5 / 0-6-7-8-9-10-11
        self.tour.swap_feasible(self.tour.nodes[6], self.tour.nodes[9], self.tour.nodes[8], self.tour.nodes[0])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[0])

        # checking all nodes predecessor
        self.assertEqual(self.tour.nodes[0].pred, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[1].pred, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[2].pred, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[3].pred, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[4].pred, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[5].pred, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[6].pred, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[7].pred, self.tour.nodes[6])
        self.assertEqual(self.tour.nodes[8].pred, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[9].pred, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[10].pred, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[11].pred, self.tour.nodes[10])

    def test_restore_tour(self):
        """
        Test the function to restore the tour that passed through some 2-Opt swaps by undoing a certain amount of executed swaps
        """

        # get initial condition
        initial_succs = [node.succ for node in self.tour.nodes]
        initial_preds = [node.pred for node in self.tour.nodes]

        # execute a feasible swap and restore the tour
        self.tour.swap_feasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[8], self.tour.nodes[7])
        self.tour.restore()

        # compare the current nodes with initial nodes
        self.assertEqual(initial_preds, [node.pred for node in self.tour.nodes])
        self.assertEqual(initial_succs, [node.succ for node in self.tour.nodes])

        # execute 2 feasible swaps and restore the tour
        self.tour.swap_feasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[8], self.tour.nodes[7])
        self.tour.swap_feasible(self.tour.nodes[11], self.tour.nodes[10], self.tour.nodes[3], self.tour.nodes[2])
        self.tour.restore()

        # compare the current nodes with initial nodes
        self.assertEqual(initial_preds, [node.pred for node in self.tour.nodes])
        self.assertEqual(initial_succs, [node.succ for node in self.tour.nodes])

        # execute one unfeasible swap and restore tour
        self.tour.swap_unfeasible(self.tour.nodes[11], self.tour.nodes[0], self.tour.nodes[5], self.tour.nodes[6])
        self.tour.restore()

        # compare the current nodes with initial nodes
        self.assertEqual(initial_preds, [node.pred for node in self.tour.nodes])
        self.assertEqual(initial_succs, [node.succ for node in self.tour.nodes])

        # execute one feasible and one unfeasible swap and restore tour
        self.tour.swap_feasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[8], self.tour.nodes[7])
        self.tour.swap_unfeasible(self.tour.nodes[0], self.tour.nodes[11], self.tour.nodes[5], self.tour.nodes[6])
        self.tour.restore()

        # compare the current nodes with initial nodes
        self.assertEqual(initial_preds, [node.pred for node in self.tour.nodes])
        self.assertEqual(initial_succs, [node.succ for node in self.tour.nodes])

        # execute one unfeasible and one of the special swaps
        self.tour.swap_unfeasible(self.tour.nodes[0], self.tour.nodes[1], self.tour.nodes[5], self.tour.nodes[6])
        self.tour.swap_node_between_t2_t3(self.tour.nodes[0], self.tour.nodes[6], self.tour.nodes[3], self.tour.nodes[4])
        self.tour.restore()

        # compare the current nodes with initial nodes
        self.assertEqual(initial_preds, [node.pred for node in self.tour.nodes])
        self.assertEqual(initial_succs, [node.succ for node in self.tour.nodes])

    def test_swap_double_bridge_normal(self):
        """
        Test the double bridge swap when all nodes are ordered exactly as needed to perform the operation
        """

        # execute the double bridge move
        self.tour.swap_double_bridge(self.tour.nodes[5], self.tour.nodes[6], self.tour.nodes[11], self.tour.nodes[0], self.tour.nodes[2], self.tour.nodes[3], self.tour.nodes[9], self.tour.nodes[10])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[6])

    def test_swap_double_bridge_reversed(self):
        """
        Test the double bridge swap when nodes to perform the move are reversed
        """

        # execute the double bridge move
        self.tour.swap_double_bridge(self.tour.nodes[6], self.tour.nodes[5], self.tour.nodes[0], self.tour.nodes[11], self.tour.nodes[10], self.tour.nodes[9], self.tour.nodes[3], self.tour.nodes[2])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[6])

    def test_swap_double_bridge_semi_normal(self):
        """
        Test the double bridge swap when nodes are in correct sequence but the second unfeasible swap is not correctly positioned (t5 is not between t4-t1 segment)
        """

        # execute the double bridge move
        self.tour.swap_double_bridge(self.tour.nodes[5], self.tour.nodes[6], self.tour.nodes[11], self.tour.nodes[0], self.tour.nodes[9], self.tour.nodes[10], self.tour.nodes[2], self.tour.nodes[3])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[6])

    def test_swap_double_bridge_inverted(self):
        """
        Test the double bridge swap when nodes are in incorrect sequence, needing to reverse the nodes before applying the swap
        """

        # execute the double bridge move
        self.tour.swap_double_bridge(self.tour.nodes[6], self.tour.nodes[5], self.tour.nodes[0], self.tour.nodes[11], self.tour.nodes[2], self.tour.nodes[3], self.tour.nodes[9], self.tour.nodes[10])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[6])

    def test_swap_double_bridge_fully_inverted(self):
        """
        Test the double bridge swap when nodes are in incorrect sequence, needing to reverse the nodes before applying the swap.
        """

        # execute the double bridge move
        self.tour.swap_double_bridge(self.tour.nodes[6], self.tour.nodes[5], self.tour.nodes[0], self.tour.nodes[11], self.tour.nodes[9], self.tour.nodes[10], self.tour.nodes[2], self.tour.nodes[3])

        # checking all nodes successor
        self.assertEqual(self.tour.nodes[0].succ, self.tour.nodes[1])
        self.assertEqual(self.tour.nodes[1].succ, self.tour.nodes[2])
        self.assertEqual(self.tour.nodes[2].succ, self.tour.nodes[10])
        self.assertEqual(self.tour.nodes[3].succ, self.tour.nodes[4])
        self.assertEqual(self.tour.nodes[4].succ, self.tour.nodes[5])
        self.assertEqual(self.tour.nodes[5].succ, self.tour.nodes[0])
        self.assertEqual(self.tour.nodes[6].succ, self.tour.nodes[7])
        self.assertEqual(self.tour.nodes[7].succ, self.tour.nodes[8])
        self.assertEqual(self.tour.nodes[8].succ, self.tour.nodes[9])
        self.assertEqual(self.tour.nodes[9].succ, self.tour.nodes[3])
        self.assertEqual(self.tour.nodes[10].succ, self.tour.nodes[11])
        self.assertEqual(self.tour.nodes[11].succ, self.tour.nodes[6])
