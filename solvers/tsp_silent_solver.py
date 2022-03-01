# add project path to sys.path so that imports can be made
# remove this after setting the package as a module
import sys
import os
import argparse
sys.path.append(os.path.abspath(os.path.join(__file__, "../../")))
from utils.solver_funcs import solve_tsp

# set parser options (for silent execution) and get the args from execution
parser = argparse.ArgumentParser(description="Parse the tsp file and the solution method")
parser.add_argument("--tsp_file", type=str, required=False, help="the tsp file path")
parser.add_argument("--solution_method", type=str, required=False, help="the solution method to solve the tsp")
parser.add_argument("--runs", type=int, required=False, help="the number of improve cycles to run")
parser.add_argument("--logging_level", type=int, required=False, help="the logging level for more or less details of the execution")
args = parser.parse_args()

# init the tsp_file and solution_method from parser
tsp_file = args.tsp_file  # the path to .tsp file
solution_method = args.solution_method  # the solution method (as a string)
runs = args.runs  # the number of runs
logging_level = args.logging_level  # the logging level

# execute the solver using inputs
solve_tsp(tsp_file, solution_method, runs, logging_level)
