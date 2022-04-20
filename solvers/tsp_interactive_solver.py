# add project path to sys.path so that imports can be made
# remove this after setting the package as a module
import sys
import os
import logging
sys.path.append(os.path.abspath(os.path.join(__file__, "../../")))
from utils.solver_funcs import get_interactive_inputs, solve_tsp

# start interactive shell to collect tsp file and solution method
tsp_file, solution_method = get_interactive_inputs()

# execute the solver using inputs
solve_tsp(tsp_file, solution_method, 100, logging.INFO)
