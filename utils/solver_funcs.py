import os
import logging
from models import Tsp
from utils.cost_funcs import cost_funcs
from utils.io_funcs import import_tsp_file, export_tsp_file

# setup the logging format and level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger(__name__)

# get the directory of this file and setup the "samples" and "solutions" dir
file_dir = os.path.dirname(os.path.realpath(__file__))
samples_dir = os.path.abspath(os.path.join(file_dir, "../", "samples"))
solutions_dir = os.path.abspath(os.path.join(file_dir, "../", "solutions"))


def get_interactive_inputs():
    """
    Execute the interactive shell with user inputs to get a selection for the tsp file (from 'samples' directory) and a selection of a solution method (a list of avaliable methods at Tsp class)

    :return: a tuple with the tsp file and the solution method selected by the user
    :rtype: tuple
    """

    ###################################
    # Step 1 - Select the TSP problem #
    ###################################

    # index of a file and collection of file paths
    tsp_files = []

    # loop to collect files in selected directory
    print("# Step 1 - TSP Instance Selection #")
    print(f"*TSP instances avaliable in '{os.path.basename(samples_dir)}' directory:")
    for i, f in enumerate(os.listdir(samples_dir)):
        tsp_files.append(os.path.join(samples_dir, f))
        print(f"[{i}] - {f}")

    # loop to get user selection
    tsp_selection = "-1"
    while (not tsp_selection.isnumeric() or int(tsp_selection) > len(tsp_files) - 1):
        tsp_selection = input("--> Select one of the instances: ")

    # get the tsp file
    tsp_file = tsp_files[int(tsp_selection)]

    # print separator
    print("")

    ###################################
    # Step 2 - Select solution method #
    ###################################

    # get the solution methods avaliable at Tsp class
    solution_methods = Tsp.get_solution_methods()

    # loop to display avaliable solution methods
    print("# Step 2 - TSP Solution Methods #")
    print("*TSP solution methods avaliable in tsp.py:")
    for i, solution_method in enumerate(solution_methods):
        print(f"[{i}] - {solution_method.__name__}")

    # loop to get user selection
    method_selection = "-1"
    while (not method_selection.isnumeric() or int(method_selection) > len(solution_methods) - 1):
        method_selection = input("--> Select one of the solution methods: ")

    # get the method name
    solution_method = solution_methods[int(method_selection)].__name__

    # print separator
    print("")

    # returns the tsp file and solution method
    return (tsp_file, solution_method)


def solve_tsp(tsp_file, solution_method):
    """
    Solve a specific tsp problem using the tsp_file input and the desired solution method. The solution is parsed to .tsp file and exported to solution folder

    :param tsp_file: the .tsp file to be solved
    :type tsp_file: str
    :param solution_method: the method to be used when solving the tsp
    :type solution_method: function
    """

    # parse the .tsp file
    logger.info(f"Importing .tsp file '{os.path.basename(tsp_file)}'")
    tsp_header, tsp_nodes = import_tsp_file(tsp_file)

    # get the cost function
    cost_function = cost_funcs[tsp_header["EDGE_WEIGHT_TYPE"]]
    logger.info(f"Using '{cost_function.__name__}' for edge type '{tsp_header['EDGE_WEIGHT_TYPE']}'")

    # create the initial tsp instance
    logger.info("Creating TSP instance")
    tsp = Tsp(tsp_nodes, cost_function, shuffle=True)

    # execute the improvement method
    logger.info("Starting improve method")
    tsp.methods[solution_method]()

    # setup export name as "tspname_cost.tsp"
    tsp_full_name = os.path.basename(tsp_file)
    tsp_name, tsp_ext = os.path.splitext(tsp_full_name)
    export_file = os.path.join(solutions_dir, f"{tsp_name}_{tsp.tour.cost:.3f}.tsp")

    # execute the export
    logger.info(f"Exporting '{os.path.basename(export_file)}' file to solutions folder")
    export_tsp_file(export_file, tsp_header, tsp.tour.get_tour_nodes())
