from random import shuffle
from models.edge import Edge


class Tour:
    """
    The tour class represents a sequence of edges that starts at one node, visits all tour nodes and ends at same starting node. The nodes will be a list of nodes in the ordering of visit, while edges is a set of edges (so ordering is not considered).
    """

    def __init__(self, nodes):
        """
        A tour is made by a sequence of edges. Since edges are defined by sequence of nodes, the node sequence is used as input.

        :param nodes: the list of Nodes2D/Nodes3D that makes the tour
        :type nodes: list
        """

        # set the tour nodes and initialize tour node parameters
        self.nodes = nodes
        self.set_nodes()

        # set tour edges using defined tour nodes
        self.edges = set()
        self.set_edges()

        # Initialize the cost value, to be update when calling the function set_cost using a distance matrix.
        self.cost = 0

        # set the size of the tour
        self.size = len(nodes)

    def set_nodes(self):
        """
        Update tour nodes with specific related tour properties
        """

        # loop through each node and set the tour properties
        for i in range(len(self.nodes)):

            # set node's successor node
            if (i == len(self.nodes) - 1):
                self.nodes[i].succ = self.nodes[0]  # the successor of the last node is the first node
            else:
                self.nodes[i].succ = self.nodes[i + 1]

            # set node's predecessor node
            self.nodes[i].pred = self.nodes[i - 1]

            # set node position
            self.nodes[i].pos = i

            # set node id
            self.nodes[i].id = i

    def set_edges(self):
        """
        Generate the tour edges using current tour nodes
        """

        # initialize the set of edges
        tour_edges = set()

        # initialize the first node
        curr_node = self.nodes[0]

        # loop through each node and add the edge of current node and its neighbor
        while(curr_node.succ != self.nodes[0]):
            tour_edges.add(Edge(curr_node, curr_node.succ))
            curr_node = curr_node.succ

        # add the closing edge
        tour_edges.add(Edge(curr_node, curr_node.succ))

        # populate the edges
        self.edges = tour_edges

    def set_cost(self, cost_matrix):
        """
        Set the tour cost by summing all tour edge costs from a cost matrix

        :param cost_matrix: the matrix with cost(i,j) between node id "i" and node id "j"
        :type node: list

        """
        # initialize the cost
        tour_cost = 0

        # initialize the first node
        curr_node = self.nodes[0]

        # loop through each node and add the edge of current node and its neighbor
        while(curr_node.succ != self.nodes[0]):
            tour_cost += cost_matrix[(curr_node.id, curr_node.succ.id)]
            curr_node = curr_node.succ

        # add the cost of closing the loop (last node -> first node)
        tour_cost += cost_matrix[(curr_node.id, curr_node.succ.id)]

        # assign the cost value
        self.cost = tour_cost

    def shuffle(self):
        """
        Shuffle the tour nodes creating a random tour and re-initializing the tour edges 
        """

        # create random indexes between 1 and size-1
        indexes = [i for i in range(1, self.size)]
        shuffle(indexes)

        # add the 0 (first node) at the end of the indexes list
        indexes.append(0)

        # initilize the current node
        curr_node = self.nodes[0]

        # loop to change the predecessor, successor and position of each node
        for i in range(-1, self.size - 1):
            curr_node.succ = self.nodes[indexes[i + 1]]
            curr_node.pred = self.nodes[indexes[i - 1]]
            curr_node.pos = i + 1
            curr_node = curr_node.succ

        # rebuild the edges after shuffling the nodes
        self.set_edges()

    def get_tour_nodes(self):
        """
        Get the nodes inside the tour and add them sorted into a list of nodes. This is usefull to get the sequence of nodes inside the tour (without succ and pred properties, since this changes after improving a tour, for example) and use it for plot.

        :return: the list of node indexes
        :rtype: list
        """

        # start node indexes and get the starting node
        tour_nodes = []
        curr_node = self.nodes[0]

        # loop through each tour node
        while curr_node.succ != self.nodes[0]:

            # append the node index to list of indexes
            tour_nodes.append(curr_node)

            # update current node
            curr_node = curr_node.succ

        # append last index to close the tour
        tour_nodes.append(curr_node)

        #  return the list of indexes
        return tour_nodes

    def is_swap_valid(self, t1, t2, t3, t4):
        """
        Validate a 2Opt-Swap operation using reference nodes. Edge (t1,t2) and (t3,t4) are broken so that a relink of (t2,t3) and (t1,t4) is made, as shown below:

          t4  t3           t4   t3
          ()--()           ()   ()
         /      \         /  \ /  \
        ()      ()  -->  ()   X   ()
         \      /         \  / \  /
          ()--()           ()   ()
          t2  t1           t2   t1

        For a valid swap:
        *1: the order of the nodes in the tour must be (t1,t2,t4,t3) in any direction (clockwise or counter clockwise). Notice that in the scheme above, if we had (t1,t2,t3,t4), the relink would result in 2 closed loops, which are invalid. Notice that if we switch t1 with t2 and t3 with t4, it still valid, the change was only made in the direction;
        *2: t3 can't be a neighboor of t2. this would mean two sequential edges to be broken, which would lead to an invalid tour;

        :param t1: the tail node of the first broken edge
        :type t1: Node2D
        :param t2: the head node of the first broken edge
        :type t2: Node2D
        :param t3: the tail node of the second broken edge
        :type t3: Node2D
        :param t4: the head node of the second broken edge
        :type t4: Node2D
        :return: a boolean indicating if swap is valid
        :rtype: boolean
        """

        # t3 can't be a neighboor of t2, otherwise the swap operation will result in an invalid tour (rule 2)
        if (t3 == t2.pred or t3 == t2.succ):
            return False

        # check t4 based on the orientation of the edge (t1,t2)
        # for a valid swap, t4 can be validated using t1 and t2 orientation (rule 1)
        if t1.succ == t2:
            if t4 != t3.pred:
                return False
        elif t1.pred == t2:
            if t4 != t3.succ:
                return False

        # return true if no invalid swaps were found
        return True

    def swap_nodes(self, t1, t2, t3, t4):
        """
        Execute a 2Opt-Swap operation using reference nodes. Edge (t1,t2) and (t3,t4) are broken so that a relink of (t2,t3) and (t1,t4) is made, as shown below:

          t4  t3           t4   t3
          ()--()           ()   ()
         /      \         /  \ /  \
        ()      ()  -->  ()   X   ()
         \      /         \  / \  /
          ()--()           ()   ()
          t2  t1           t2   t1

        :param t1: the tail node of the first broken edge
        :type t1: Node2D
        :param t2: the head node of the first broken edge
        :type t2: Node2D
        :param t3: the tail node of the second broken edge
        :type t3: Node2D
        :param t4: the head node of the second broken edge
        :type t4: Node2D
        :return: a boolean indicating if swap was performed
        :rtype: boolean
        """

        # checking if swap configuration is valid
        if not self.is_swap_valid(t1, t2, t3, t4):
            return False

        # if t2 is not the successor of t1, invert t1 with t2 and t3 with t4
        # since the node reordering is always applied to t3 -> t1 segment, this is done so that the reordering loop will be done correctly.
        if (t1.succ != t2):
            temp = t1
            t1 = t2
            t2 = temp
            temp = t3
            t3 = t4
            t4 = temp

        # compute the segment size between t2 and t3 and compare it with the problem size
        # this validates if the segment between t2-t3 has more/less nodes than the segment t3-t1
        # if t2-t3 is shorter, we can switch t3 with t2 and t4 with t1 so that the swap result will be the same, but the amount of nodes to be reordered is smaller
        seg_size = t2.pos - t3.pos
        if seg_size < 0:
            seg_size += self.size  # the amount of nodes in t3-t1
        if (2 * seg_size > self.size):  # checking if there are more nodes in t3-t1 than t2-t3
            temp = t3
            t3 = t2
            t2 = temp
            temp = t4
            t4 = t1
            t1 = temp

        # initialize the position value from t1 (the value of t1 pos will be assigned to t3, since after the swap t3 is the predecessor of t2)
        pos = t1.pos

        # the starting node for the reversed segment is t3 (until t1)
        node = t3

        # the loop is broken at t1 successor, (since t1 is the last node)
        end_node = t1.succ

        # loop to reorder the nodes between t3-t1 segment (including t3 and t1)
        while (node != end_node):

            # invert the node ordering
            temp = node.succ
            node.succ = node.pred
            node.pred = temp

            # update node position
            node.pos = pos
            pos -= 1

            # update node for next loop with the last successor node
            node = temp

        # reassign the successor/predecessor values at each of the 4 reconnected nodes
        t3.succ = t2
        t2.pred = t3
        t1.pred = t4
        t4.succ = t1

        # returns a boolean indicating the swap was done
        return True

    def __str__(self):
        """
        The display string when printing the object

        :return: the display string
        :rtype: str
        """

        # get the starting node
        curr_node = self.nodes[0]

        # initialize the string
        node_seq = str(curr_node.id)

        # loop until tour is closed
        while curr_node.succ != self.nodes[0]:

            # get next node
            curr_node = curr_node.succ

            # update the string
            node_seq += f",{curr_node.id}"

        # return the string sequence
        return f"({node_seq})"
