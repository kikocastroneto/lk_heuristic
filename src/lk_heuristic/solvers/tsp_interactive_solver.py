import logging
from lk_heuristic.utils.solver_funcs import get_interactive_inputs, solve_tsp

# start interactive shell to collect tsp file and solution method
tsp_file, solution_method = get_interactive_inputs()

# execute the solver using inputs
solve_tsp(tsp_file, solution_method, 1, logging.DEBUG)
