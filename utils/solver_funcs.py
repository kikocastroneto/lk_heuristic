import os
import logging
import math
import time
from models import Tsp
from utils.cost_funcs import cost_funcs
from utils.io_funcs import import_tsp_file, export_tsp_file

# create the logger
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
    f_index = 0
    for f in os.listdir(samples_dir):
        if f.lower().endswith(".tsp"):
            tsp_files.append(os.path.join(samples_dir, f))
            print(f"[{f_index}] - {f}")
            f_index += 1

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


def solve_tsp(tsp_file, solution_method, runs, logging_level):
    """
    Solve a specific tsp problem a certain amount of times using the tsp_file input and the desired solution method. The best solution is parsed to .tsp file and exported to solution folder. 

    :param tsp_file: the .tsp file to be solved
    :type tsp_file: str
    :param solution_method: the method to be used when solving the tsp
    :type solution_method: function
    :param runs: the number of improve runs to be performed
    :type runs: int
    :param logging_level: the verbosity level for more or less details during execution
    :type logging_level: int
    """

    # setup the logger
    logging.basicConfig(level=logging_level, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # parse the .tsp file
    logger.info(f"Importing .tsp file '{os.path.basename(tsp_file)}'")
    tsp_header, tsp_nodes = import_tsp_file(tsp_file)

    # get the cost function
    cost_function = cost_funcs[tsp_header["EDGE_WEIGHT_TYPE"]]
    logger.info(f"Using '{cost_function.__name__}' for edge type '{tsp_header['EDGE_WEIGHT_TYPE']}'")

    # setup some information of the run
    best_tour = None  # the best tsp tour nodes found so far
    best_cost = math.inf  # the best cost found so fat
    mean_cost = 0  # the mean cost value of all runs

    # create the initial tsp instance
    logger.debug("Creating TSP instance")
    tsp = Tsp(tsp_nodes, cost_function, shuffle=False, max_neighbors=5)

    # looping through each run
    for run in range(1, runs + 1):

        # shuffle the tour nodes
        tsp.tour.shuffle()
        tsp.tour.set_cost(tsp.cost_matrix)

        # execute the improvement method and timeit
        logger.debug("Starting improve method")
        start_time = time.time()
        tsp.methods[solution_method]()
        end_time = time.time()

        # update best solution found so far (if current solution is the best)
        if tsp.tour.cost < best_cost:
            best_tour = tsp.tour.get_tour_nodes()
            best_cost = tsp.tour.cost

        # update mean cost value
        mean_cost += (tsp.tour.cost - mean_cost) / run

        # log the information of current run
        logger.info(f"[Run:{run}] --> Cost: {tsp.tour.cost:.3f} / Best: {best_cost:.3f} / Mean: {mean_cost:.3f} ({end_time - start_time:.3f}s)")

    # setup export name as "tspname_cost.tsp"
    tsp_full_name = os.path.basename(tsp_file)
    tsp_name, tsp_ext = os.path.splitext(tsp_full_name)
    export_file = os.path.join(solutions_dir, f"{tsp_name}_{best_cost:.3f}.tsp")

    # execute the export
    logger.info(f"Exporting '{os.path.basename(export_file)}' file to solutions folder")
    export_tsp_file(export_file, tsp_header, best_tour)
