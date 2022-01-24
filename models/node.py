class Node:
    """
    The node class represent a node in TSP problem. It is implemented as a doubly linked list, where each node has its predecessor and successor node defined.
    """

    def __init__(self):
        """
        Initialize a node
        """
        # the id of the node (this unique integer will help to distinguish between repeated coordinates nodes and also to build the distance matrix). It will be updated when initializing a tour
        self.id = -1

        # the position (index) of the node in a tour (to be update when initializing the tour)
        # the position can be either a positive or negative number, but is must be incremented by 1
        self.pos = -1

        # the predecessor and successor nodes at a tour (to be update when initializing the tour)
        self.pred = None
        self.succ = None

    def __eq__(self, other):
        """
        Equal comparison method between two nodes, which will be true when node ids are equal.

        :param other: other node of comparison
        :type other: Node
        :return: a boolean indicating if both nodes are equal
        :rtype: boolean
        """
        # check if other node is not None
        if (other):
            return (self.id == other.id)
        else:
            return False

    def __str__(self):
        """
        The display string when printing the object

        :return: the display string
        :rtype: str
        """
        return f"({self.id})"

    def __repr__(self):
        """
        The display string when printing the object

        :return: the display string
        :rtype: str
        """
        return f"({self.id})"


class Node2D(Node):
    """
    The node 2D class represent a node in 2D cartesian space.
    """

    def __init__(self, x, y):
        """
        Initialize a node with its cartesian values

        :param x: the "x" coordinate value
        :type x: float
        :param y: the "y" coordinate value
        :type y: float
        """

        # initialize the super class
        super().__init__()

        # initialize the node values
        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        Equal comparison method between two 2D nodes, which will be true when both node coordinates are equal and node id is equal (id comparison is done so that nodes with repeated coordinates are considered different. This may happen is some tsp instances)

        :param other: other node of comparison
        :type other: Node2D
        :return: a boolean indicating if both nodes are equal
        :rtype: boolean
        """
        # check if other node is not None
        if (other):
            return (self.x == other.x and self.y == other.y and self.id == other.id)
        else:
            return False

    def __gt__(self, other):
        """
        Greater than comparison method between two 2D nodes, which will be true when the tuple made of nodes are greater than the other tuple of nodes. This is relevant when building edges, to always keep same node ordering (for simmetric TSP).

        :param other: other node of comparison
        :type other: Node2D
        :return: a boolean indicating if node is greater than other node
        :rtype: boolean
        """
        return ((self.x, self.y) > (other.x, other.y))

    def __hash__(self):
        """
        Hashing Node2D object is required to allow comparison of Edge, which are elements made of Node2D. The hash is performed in the tuple of node x and y values
        """
        return hash((self.x, self.y))

    def __str__(self):
        """
        The display string when printing the object

        :return: the display string
        :rtype: str
        """
        return f"({self.x},{self.y})"

    def __repr__(self):
        """
        The display string when printing the object

        :return: the display string
        :rtype: str
        """
        return f"({self.x},{self.y})"


class Node3D(Node):
    """
    The node 3D class represent a node in 3D cartesian space.
    """

    def __init__(self, x, y, z):
        """
        Initialize a node with its cartesian values

        :param x: the "x" coordinate value
        :type x: float
        :param y: the "y" coordinate value
        :type y: float
        :param z: the "z" coordinate value
        :type z: float
        """

        # initialize the super class
        super().__init__()

        # initialize the node values
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        """
        Equal comparison method between two 3D nodes, which will be true when both node coordinates are equal and node id is equal (id comparison is done so that nodes with repeated coordinates are considered different. This may happen is some tsp instances)

        :param other: other node of comparison
        :type other: Node3D
        :return: a boolean indicating if both nodes are equal
        :rtype: boolean
        """
        # check if other node is not None
        if (other):
            return (self.x == other.x and self.y == other.y and self.z == other.z and self.id == other.id)
        else:
            return False

    def __gt__(self, other):
        """
        Greater than comparison method between two 3D nodes, which will be true when the tuple made of nodes are greater than the other tuple of nodes. This is relevant when building edges, to always keep same node ordering (for simmetric TSP).

        :param other: other node of comparison
        :type other: Node3D
        :return: a boolean indicating if node is greater than other node
        :rtype: boolean
        """
        return ((self.x, self.y, self.z) > (other.x, other.y, other.z))

    def __hash__(self):
        """
        Hashing Node3D object is required to allow comparison of Edge, which are elements made of Node3D. The hash is performed in the tuple of node x and y values
        """
        return hash((self.x, self.y, self.z))

    def __str__(self):
        """
        The display string when printing the object

        :return: the display string
        :rtype: str
        """
        return f"({self.x},{self.y},{self.z})"

    def __repr__(self):
        """
        The display string when printing the object

        :return: the display string
        :rtype: str
        """
        return f"({self.x},{self.y},{self.z})"
