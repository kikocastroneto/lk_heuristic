import random
import time
import math
import logging
from itertools import permutations
from models.edge import Edge
from models.tour import Tour
from utils.timer_funcs import improve_timer_decorator

# create the logger for the module
logger = logging.getLogger(__name__)


class Tsp:
    """
    The TSP class represents the travelling salesman problem inputs and helper methods for the problem.
    """

    # set the precision of the gain
    # this is required when computing the gain in "simmetric" tours, to avoid incorrect calculations when using just "> 0 "
    gain_precision = 0.01

    def __init__(self, nodes, cost_function, shuffle=False):
        """
        The TSP input is a list of nodes which will be used as input to build a tour. Tour nodes can be randomized using shuffle parameter. The cost function is the function used to compute the cost matrix. 

        :param nodes: the list of nodes for the tsp
        :type nodes: list
        :param cost_function: the function used to compute the cost between two nodes
        :type cost_function: function
        :param shuffle: a boolean value indicating if nodes shall be shuffled before building the tour
        :type shuffle: boolean
        """

        # initialize nodes
        self.nodes = nodes

        # shuffle the nodes
        if shuffle:
            random.shuffle(self.nodes)

        # initialize the tour using the nodes
        self.tour = Tour(self.nodes)

        # initialize the cost matrix after having the nodes initialized into the tour object using the defined cost_function
        self.cost_matrix = {}
        self.set_cost_matrix(cost_function)

        # initialize tour cost after having the cost matrix initialized
        self.tour.set_cost(self.cost_matrix)

        # solution methods avaliable to solve the problem
        self.methods = {
            "bf_improve": self.bf_improve,
            "nn_improve": self.nn_improve,
            "lk_improve": self.lk_improve
        }

        # init the swap stack
        # the swap stack is the "memory" of swap_nodes function of the tour objects, so that if an invalid sequence of swap are made it is possible to "undo" the swap by executing the swaps in reversed order using the stack of swaps
        self.swap_stack = []

        # init the set of solutions
        # the set of solutions will help to avoid repeated tours analysis
        # it is a hash of a tuple of node sequences
        self.solutions = set()

    def set_cost_matrix(self, cost_func):
        """
        Compute the cost matrix using tsp nodes and a predefined cost function. The matrix is in the form of a dictionary with (row,column) values as keys of the dict

        :param cost_func: the cost function to be used to compute the cost matrix
        :type cost_func: function
        """

        # index is used to avoid repeated computation
        index = 0
        for i in range(len(self.nodes)):
            for j in range(index, len(self.nodes)):
                # get node 1 and node2
                n1 = self.nodes[i]
                n2 = self.nodes[j]

                # compute the cost between nodes
                cost = cost_func(n1, n2)

                # update cost matrix
                self.cost_matrix[(n1.id, n2.id)] = cost
                self.cost_matrix[(n2.id, n1.id)] = cost  # simmetric value

            # update index for next iteration
            index += 1

    def restore_tour(self):
        """
        Restore an initial tour that passed through some 2-opt swaps. The swaps are undone until no more swaps can be made, from last swap to initial one. The reversed operation of a swap_nodes(t1,t2,t3,t4) is swap_nodes(t3,t2,t1,t4)
        """

        # loop until no more swap stacks
        while (self.swap_stack):

            # get last stack
            curr_stack = self.swap_stack[-1]

            # collect node values
            t1 = curr_stack[0]
            t2 = curr_stack[1]
            t3 = curr_stack[2]
            t4 = curr_stack[3]

            # execute the reversed swap
            self.tour.swap_nodes(t3, t2, t1, t4)

            # remove last stack
            self.swap_stack.pop()

    def get_closest_neighboors(self, t1, t2, max_neighboors=5):
        """
        Get the closest neighbors of t2 by computing the gain = c(x2) - c(y1) (the difference between the cost of the broken edge x2 and joined edge y1). x2 = (t3,t4) and y1 = (t2,t3). The use of t1 is required to check if the future swap to be made is valid, so that only valid swaps are considered and returned by the function. The procedure of this function is the refinement "Lookahead" defined at 1973 LK paper.

        The return will be a list of tuple in the format: ((t3,t4), gain), where the first element is a tuple with nodes of broken edge and gain is the computed gain value (c(x2) - c(y1)). The amount of values to be returned is defined by the max_neighboors variable, which at LK paper, is suggested to be 5.

        :param t1: the tail node of the edge to be broken 
        :type t1: Node2D
        :param t2: the head node of the edge to be broken
        :type t2: Node2D
        :param max_neighboors: the maximum number of closest neighbors to collect
        :type max_neighboors: int
        :return: returns a list of tuple with nodes (t3,t4) and the gain value
        :rtype: list
        """
        # create a dictionary mapping (t3,t4) with respective gain relative to t2
        # gain = c(t3,t4) - c(t2,t3)
        closest_neighboors = {}

        # loop through each possible t3
        for t3 in self.tour.nodes:

            # t3 can't be t2 for a valid swap
            if t3 != t2:

                # compute the gain for the valid swap
                # in a valid swap t4 is either t3.pred or t3.succ, but not both, which is checked by the is_swap_valid function
                if (self.tour.is_swap_valid(t1, t2, t3, t3.pred)):
                    closest_neighboors[(t3, t3.pred)] = self.cost_matrix[(t3.id, t3.pred.id)] - self.cost_matrix[(t2.id, t3.id)]
                if (self.tour.is_swap_valid(t1, t2, t3, t3.succ)):
                    closest_neighboors[(t3, t3.succ)] = self.cost_matrix[(t3.id, t3.succ.id)] - self.cost_matrix[(t2.id, t3.id)]

        # returns a list of (key,value) pairs of the max values of gain.
        return sorted(closest_neighboors.items(), key=lambda x: x[1], reverse=True)[:max_neighboors]

    def lk_select_broken_edge(self, gain, t1, t2, t3, t4, broken_edges, joined_edges):
        """
        This function is used to select the next edge to be broken at current configuration of the LK optimization procedure. After that, the function will swap the tour nodes (t1,t2,t3,t4) and return a boolean value indicating if the swap resulted in a valid better tour.

        If the swap results in a valid worse tour, the call to select a new joined edge will be made to continue the exploration of new edges. This new exploration will try to swap the closed edge (t4,t1) with a new potencial better edge.

        The nodes t1, t2, t3 and t4 represents the swap in current configuration. When having sequence of swaps in the same tour, LK paper will mention those nodes based on the swap number, like (t2i, t2i+1, t2i+2...), where "i" is the swap number.

        :param gain: the current gain from last LK step
        :type gain: float
        :param t1: the tail node of the first broken edge in the 2-opt swap
        :type t1: Node2D
        :param t2: the head node of the first broken edge in the 2-opt swap
        :type t2: Node2D
        :param t3: the tail node of the second broken edge in the 2-opt swap
        :type t3: Node2D
        :param t4: the head node of the second broken edge in the 2-opt swap
        :type t4: Node2D
        :param broken_edges: the set of broken edges
        :type broken_edges: set
        :param joined_edges: the set of joined edges
        :type joined_edges: set
        :return: a boolean indicating if improvement was found
        :rtype: boolean
        """

        # get the edge to be broken and its cost
        broken_edge = Edge(t3, t4)
        broken_cost = self.cost_matrix[(t3.id, t4.id)]

        # the neighboor can't be t1 (this results in an invalid tour)
        # disjoint criteria (broken edge can't be previouslly at joined edges)
        # check if broken_edge is not already inside broken_edges set, because an edge can't be broken two times, this would lead to incorrect calculation
        if t1 != t4 and broken_edge not in joined_edges and broken_edge not in broken_edges:

            # try to do the 2-opt swap
            if (self.tour.swap_nodes(t1, t2, t3, t4)):

                # include the swap nodes into the swap stack
                self.swap_stack.append((t1, t2, t3, t4))

                # add the broken edge to the set of broken edges
                broken_edges.add(broken_edge)

                # build the join edge from neighboor to last node (closing the tour)
                joined_edge = Edge(t4, t1)
                joined_cost = self.cost_matrix[(t4.id, t1.id)]

                # compute the current gain value
                curr_gain = gain + (broken_cost - joined_cost)

                # check for repeated tours (one of LK refinements is to remove repeated tours that already were tested and checked that can't be improved). O(n) complexity like the one done below could be improved with hashingtables, as done by Helsgaum.
                if (hash(tuple([node.succ.id for node in self.tour.nodes])) in self.solutions):
                    return False

                # if gain is positive, restart the search with new tour
                # this is a simplification of LK from Helsgaun paper. LK suggest to continue the search, while Helsgaun suggest to simplify the algorithm
                if curr_gain > self.gain_precision:

                    # add joined edge
                    joined_edges.add(joined_edge)

                    # a sanity check here
                    old_tour_cost = self.tour.cost
                    self.tour.set_cost(self.cost_matrix)  # this shall not be erased in the future!
                    delta_tour_cost = abs(old_tour_cost - self.tour.cost)
                    delta_gain = abs(delta_tour_cost - curr_gain)

                    if (delta_gain > self.gain_precision):
                        logger.error("delta gain error")

                    if (old_tour_cost < self.tour.cost):
                        logger.error("cost error")

                    # return true value meaning an improvement was found
                    return True

                # if gain is negative, try to find a new best edge to add to form a new best tour
                else:

                    # try to find new joined edge
                    return self.lk_select_joined_edge(curr_gain, t1, t4, broken_edges, joined_edges)

        # boolean value indicating no improvement was found
        return False

    def lk_select_joined_edge(self, gain, t1, t4, broken_edges, joined_edges):
        """
        This function is used to select the next edge to be joined at current configuration of the LK optimization procedure. A false boolean is returned if a new joined edge was not found. If a replacement is found, the call for the selection of a new broken edge is made. 

        The selection function will "undo" the last joined edge (t4,t1) from previous "select_broken_edge" procedure, which closed the tour, by selecting a new potencial "node" so that (t1,t4) is broken and a new joined edge (t4,node) will be tested.

        :param gain: the current gain from last LK step
        :type gain: float
        :param t1: the head node of the last joined edge
        :type t1: Node2D
        :param t4: the tail node of the last joined edge
        :type t4: Node2D
        :param broken_edges: the set of broken edges
        :type broken_edges: set
        :param joined_edges: the set of joined edges
        :type joined_edges: set
        :return: a boolean indicating if improvement was found
        :rtype: boolean
        """

        # get the cost of the last joined edge (t4,t1)
        broken_cost = self.cost_matrix[(t4.id, t1.id)]

        # loop through the closest possible node from t4 instead of looping through all nodes
        for (node, neighbor_node), _ in self.get_closest_neighboors(t1, t4):

            # node must be different from t4 (since t4 is the tail of the new edge)
            if (node != t4):

                # create the edge and get the edge cost
                joined_edge = Edge(t4, node)
                joined_cost = self.cost_matrix[(t4.id, node.id)]

                # compute the new gain value
                curr_gain = gain + (broken_cost - joined_cost)

                # check if edge to be added is not in broken edges (disjoint criteria)
                # check if edge to be added is not already inside the tour
                # check if gain is positive
                if joined_edge not in broken_edges and joined_edge not in self.tour.edges and curr_gain > self.gain_precision:

                    # add the edge to joined edges
                    joined_edges.add(joined_edge)

                    # try to select an edge to be broken
                    return self.lk_select_broken_edge(curr_gain, t1, t4, node, neighbor_node, broken_edges, joined_edges)

        # boolean value indicating no improvement was found
        return False

    def lk_main(self):
        """
        Execute the main loop of LK Heuristic to optimize the tour. This is a single run of LK loop, which tries to find a better tour considering current tour being analyzed.
        """

        # loop through each node in the tour, to apply the optimization
        # LK Heuristic will loop over all tour nodes as initial nodes (first node is explored in total)
        for t1 in self.tour.nodes:

            # loop through each neighboorhood node from initial node (second node is also explored as total, so at least 2-opt is always tested for all nodes)
            for t2 in (t1.pred, t1.succ):

                # get the break edge and the cost
                broken_edge = Edge(t1, t2)
                broken_cost = self.cost_matrix[(t1.id, t2.id)]

                # loop through the closest possible node t3 from t2 instead of looping through all nodes
                for (t3, t4), _ in self.get_closest_neighboors(t1, t2):

                    # get the joined edge and its cost
                    joined_edge = Edge(t3, t2)
                    joined_cost = self.cost_matrix[(t3.id, t2.id)]

                    # compute the gain
                    gain = broken_cost - joined_cost

                    # check if joined edge is not inside the existing tour
                    # check if gain is positive
                    if joined_edge not in self.tour.edges and gain > self.gain_precision:

                        # append the edges to each edges set
                        broken_edges = set([broken_edge])
                        joined_edges = set([joined_edge])

                        # try to select the next break edge and get a possibly new tour
                        if self.lk_select_broken_edge(gain, t1, t2, t3, t4, broken_edges, joined_edges):

                            # reset the swap stack
                            self.swap_stack.clear()

                            # add the solution string to the set
                            self.solutions.add(hash(tuple([node.succ.id for node in self.tour.nodes])))

                            # return true value
                            return True
                        else:
                            # if new best tour was not found, restore the initial tour to continue the loop (if tour was not swapped, it will remain the same)
                            self.restore_tour()

        # if no improvement is found, return false
        return False

    @improve_timer_decorator
    def lk_improve(self):
        """
        The improve loop using Lin-Kernighan Heuristic. The loop calls main LK optimizer everytime a better tour is found (which will try to optimize the new best tour using the same optimizer). The loop ends when no improvement is found, such that current tour will be the local optimal
        """

        # number of tours tested
        tour_count = 1

        # boolean checking if a improved tour was found
        improved = True

        # loop until no improvement is found at TSP tour
        while improved:

            # compute the improvement
            improved = self.lk_main()

            # log the current tour cost
            logger.info(f"Current tour '{tour_count}' cost: {self.tour.cost:.3f}")

            # update tour count
            tour_count += 1

    @improve_timer_decorator
    def bf_improve(self):
        """
        The improve loop using Brute-Force computation, which converges for the global optimal tour. All permutations for nodes will be tested. It is recommended only for very small tours (< 10 nodes).
        """

        # assign values for the minimum cost and tour found
        min_cost = math.inf
        min_tour = None

        # create all possible permutations for the tour
        perms = permutations(self.nodes)

        # get the start node (to avoid repeated tours)
        start_node = self.nodes[0]

        # count number of tested tours
        tour_count = 0

        # loop through each permutation
        for perm in perms:

            # only permutation starting with the starting node is considered (so that repeated tours starting at a different node are not considered)
            if perm[0] == start_node:

                # loop through each node (starting from the last one)
                for i in range(-1, len(perm) - 1):

                    # get current and next nodes
                    curr_node = perm[i]
                    next_node = perm[i + 1]

                    # assign predecessor and successor nodes
                    curr_node.succ = next_node
                    next_node.pred = curr_node

                # update the cost value
                self.tour.set_cost(self.cost_matrix)

                # check if a best tour was found
                if self.tour.cost < min_cost:

                    # update best values
                    min_cost = self.tour.cost
                    min_tour = perm

                    # log the current  tour cost
                    logger.info(f"Current tour '{tour_count}'cost: {self.tour.cost:.3f}")

                # update and log count
                tour_count += 1
                if tour_count % 1000 == 0:
                    logger.info(f"Current tour '{tour_count}' cost: {min_cost:.3f}")

        # loop through each node of the best tour
        for i in range(-1, len(min_tour) - 1):

            # get current and next nodes
            curr_node = min_tour[i]
            next_node = min_tour[i + 1]

            # assign predecessor and successor nodes
            curr_node.succ = next_node
            next_node.pred = curr_node

        # update the cost value
        self.tour.set_cost(self.cost_matrix)

    @improve_timer_decorator
    def nn_improve(self):
        """
        The improve loop using Nearest-Neighbor computation.
        """

        # get the starting time
        start_time = time.time()

        # create a set of all tsp nodes
        nodes = set(self.nodes)

        # get the starting node
        curr_node = self.nodes[0]

        # start the set of visited nodes
        visited_nodes = set()
        visited_nodes.add(curr_node)

        # loop until all nodes are visited
        while (len(visited_nodes) < len(self.nodes)):

           # loop to find the nearest neighbor of current node
            cost = math.inf
            # loop through each node that were not visited yet
            for node in nodes - visited_nodes:
                if self.cost_matrix[(node.id, curr_node.id)] < cost:
                    cost = self.cost_matrix[(node.id, curr_node.id)]
                    next_node = node

            # update succ and pred for current and next nodes
            next_node.pred = curr_node
            curr_node.succ = next_node

            # add new node to visited nodes set
            visited_nodes.add(next_node)

            # update current node for next iteration
            curr_node = next_node

        # update the starting and ending nodes
        self.nodes[0].pred = curr_node
        curr_node.succ = self.nodes[0]

        # update the cost value
        self.tour.set_cost(self.cost_matrix)

    @classmethod
    def get_solution_methods(cls):
        """
        Get the list of solution methods for the tsp

        :return: list of solution method
        :rtype: list
        """
        return [cls.bf_improve, cls.nn_improve, cls.lk_improve]
