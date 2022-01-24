def cost_func_2d(n1, n2):
    """
    The cost function for 2D cartesian nodes, which is the euclidean distance between two nodes

    :param n1: first node
    :type n1: Node
    :param n2: second node
    :type n2: Node
    :return: the euclidean distance between first node and second node in 2D space
    :rtype: float
    """
    return ((n1.x - n2.x)**2 + (n1.y - n2.y)**2)**0.5


def cost_func_3d(n1, n2):
    """
    The cost function for 3D cartesian nodes, which is the euclidean distance between two nodes

    :param n1: first node
    :type n1: Node3D
    :param n2: second node
    :type n2: Node3D
    :return: the euclidean distance between first node and second node in 3D space
    :rtype: float
    """
    return ((n1.x - n2.x)**2 + (n1.y - n2.y)**2 + (n1.z - n2.z)**2)**0.5


# a dictionary mapping tsp lib edge weight type with respective cost function
cost_funcs = {"EUC_2D": cost_func_2d,
              "EUC_3D": cost_func_3d}
