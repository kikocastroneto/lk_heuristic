import logging
from lk_heuristic.models.node import Node2D, Node3D

# create a logger object
logger = logging.getLogger(__name__)


def import_tsp_file(tsp_file):
    """
    Import a .tsp file containing tsp definition and parse tsp header to a dictionary and tsp nodes to a list. Returns both objects in a tuple.

    *This function only works for .tsp instances of "TYPE" = TSP (symmetric tsp) and for "EDGE_WEIGH_TYPE" = EUC_2D or EUC_3D, which are the tsp problems that solver can handle currently.

    :param tsp_file: the .tsp file path
    :type tsp_file: str
    :return: a tuple with the header dict definition and a list of nodes
    :rtype: tuple
    """

    # set the allowed type and edge weight for tsp
    allowed_types = ["TSP"]
    allowed_edge_weights = ["EUC_2D", "EUC_3D"]

    # return objects
    tsp_header = {}  # the .tsp header dict to be returned by the function
    nodes = []  # the list of nodes to be parsed from node coord section

    is_node_section = False

    try:

        with open(tsp_file, "r+") as f:

            tsp_lines = f.readlines()

            for line in tsp_lines:

                # coordinates section
                if is_node_section:

                    if tsp_header["TYPE"] in allowed_types and tsp_header["EDGE_WEIGHT_TYPE"] in allowed_edge_weights:

                        if line.strip() != "EOF":

                            coords = line.replace("\n", "").split()

                            if tsp_header["EDGE_WEIGHT_TYPE"] == "EUC_2D":
                                nodes.append(Node2D(float(coords[1]), float(coords[2])))
                            elif tsp_header["EDGE_WEIGHT_TYPE"] == "EUC_3D":
                                nodes.append(Node3D(float(coords[1]), float(coords[2]), float(coords[3])))

                # header section
                else:

                    if line.strip() == "NODE_COORD_SECTION":
                        is_node_section = True

                    # split the line using ":" to get header attributes
                    line_split = line.split(":")

                    if len(line_split) == 2:

                        tsp_header[line_split[0].strip()] = line_split[1].strip()

    except Exception as e:
        logger.error(f"Error during import of .tsp file: '{e}'")

    # return the .tsp dict and node values as a tuple
    return tsp_header, nodes


def export_tsp_file(tsp_file_path, tsp_header, nodes, tour_type="cycle"):
    """
    Export a .tsp file using tsp_header header elements and list of nodes. Nodes are parsed into "NODES_COORD_SECTION" format.

    :param tsp_file_path: the name of tsp file to be exported
    :type tsp_file_path: str
    :param tsp_header: a dictionary containing header values for the .tsp file
    :type tsp_header: dict
    :param nodes: a list containing nodes to be parsed into tsp file
    :type nodes: list
    :param tour_type: the type of the tour (either 'path' or 'cycle')
    :type tour_type: str
    """

    try:

        with open(tsp_file_path, "w+") as f:

            # loop through each header value and write it to file
            for k, v in tsp_header.items():
                f.write(f"{k} : {v}\n")

            # write the node section declaration
            f.write("NODE_COORD_SECTION\n")

            # removes pivot node when using hamiltonian path tour type
            # pivot node shall be the first node (from get_nodes function of Tour class)
            if tour_type == "path":
                nodes.pop(0)

            for i, node in enumerate(nodes):
                if type(node) == Node2D:
                    f.write(f"{i} {node.x} {node.y}\n")
                elif type(node) == Node3D:
                    f.write(f"{i} {node.x} {node.y} {node.z}\n")

            # write end of file declaration
            f.write("EOF\n")

    except Exception as e:
        logger.error(f"Error during export of .tsp file: '{e}'")
