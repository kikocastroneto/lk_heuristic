# Lin-Kernighan Heuristic in Python

This package contains the implementation of *Lin-Kernighan Heuristic* as the main solver for Travelling Salesman Problem (**TSP**) instances. 

## Implementation Remarks

### LK and LKH

LK Heuristic was first reported in an [1973 article][lk_article], where the core basis of the algorithm is well explained and detailed. A few decades later, in an [1998 article][lkh_article], Keld Helsgaun reported some enhancements to the original LK Heuristic (the famous [LKH heuristic][lkh]) with additional technical details for implementing the LK heuristic.

Both of these articles were the foundation for the implementation of the algorithm included in this package, with additional inspiration from [Arthur Mahéo post][arthur] / python implementation (which I strongly recommend the reading!).

### Node Structure

Nodes are implemented as Doubly-Linked Lists, one of the structures mentioned by Helsgaun to speed up edge swap operations. More advanced structures can be implemented for faster swaps, but are not included in this package.

### Refinements

There are 4 refinements proposed in the 1973 article aiming to improve the algorithm performance. Items 1 and 2 in the list below were implemented in this package, while items 3 and 4 are still open for implementation.

 1. Avoid checkout time (by skipping repeated 'bad' tours).
 2. Lookahead (by selecting 'good' edges for swaps)
 3. Reduction (by keeping 'good' edges from being broken)
 4. Non-Sequential exchanges (by allowing exchanges that does not form a tour)
 
## How-to-use

### TSPLIB

The use of this package is based on [.tsp files][tsplib] as the input to the improve procedure and also as the output (with the difference that nodes will be sorted at output file). Currently the .tsp files supported are *"TYPE: TSP"* (i.e, symmetric problem) and *"EDGE_WEIGHT_TYPE: EUC_2D / EUC_3D"* (euclidean distance in 2D or 3D), with no "special" sections in .tsp file. 

### Solvers

The package contains 3 possible solvers for the TSP problem, which can be selected during interactive mode or silent mode:

  1. **Brute-Force**: test all tour possibilities (this should be used for very small problems)
  2. **Nearest-Neighbor**: collect nearest nodes starting from a random node (fast, but non-optimal)
  3. **Lin-Kernighan**: The main algorithm of the package 

Methods 1 and 2 were implemented mostly for testing reasons and some performance comparisons, so the recommended solver is Lin-Kernighan.

### Interactive Mode

To run the solver in interactive mode, follow these steps:

  1. Add the desired .tsp file in 'samples' folder.
  2. Run tsp_interactive_solver.py file (`python tsp_interactive_solver.py`).
  3. Enter the number of the tsp file to be used
  4. Enter the number of the solution method to be used
  5. A single improve run is executed
  6. After improve has finished, a .tsp file is exported at 'solutions' folder

### Silent Mode

To run the solver in silent mode, follow these steps:

  1. Run tsp_silent_solver.py file with the following args:
   - --tsp_file: the path to .tsp file 
   - --solution_method: one of the possible solvers ('bf_improve', 'nn_improve', 'lk_improve')
   - --runs: the number of improve cycles to run
   - --logging_level: the level of progress details
  2. After improve has finished, a .tsp file is exported at 'solutions' folder with best solution found of all runs

Example: 
  `python tsp_silent_solver.py --tsp_file "C:/temp/test.tsp" --solution_method "lk_improve" --runs 50 --logging_level 20`

### Example of an interactive run 

```
# Step 1 - TSP Instance Selection #
*TSP instances avaliable in 'samples' directory:
[0] - a280.tsp
[1] - hexagon_2d.tsp
[2] - hexagon_3d.tsp
--> Select one of the instances: 1

# Step 2 - TSP Solution Methods #
*TSP solution methods avaliable in tsp.py:
[0] - bf_improve
[1] - nn_improve
[2] - lk_improve
--> Select one of the solution methods: 2

2022-02-06 12:01:19,781 [INFO] utils.solver_funcs: Importing .tsp file 'hexagon_2d.tsp'
2022-02-06 12:01:19,785 [INFO] utils.solver_funcs: Using 'cost_func_2d' for edge type 'EUC_2D'
2022-02-06 12:01:19,786 [DEBUG] utils.solver_funcs: Creating TSP instance
2022-02-06 12:01:19,788 [DEBUG] utils.solver_funcs: Starting improve method
2022-02-06 12:01:19,789 [DEBUG] models.tsp: delta gain error
2022-02-06 12:01:19,789 [DEBUG] models.tsp: Current tour '1' cost: 22.597
2022-02-06 12:01:19,790 [DEBUG] models.tsp: Current tour '2' cost: 22.419
2022-02-06 12:01:19,790 [DEBUG] models.tsp: Current tour '3' cost: 20.597
2022-02-06 12:01:19,791 [DEBUG] models.tsp: Current tour '4' cost: 19.597
2022-02-06 12:01:19,792 [DEBUG] models.tsp: Current tour '5' cost: 19.189
2022-02-06 12:01:19,792 [DEBUG] models.tsp: Current tour '6' cost: 15.153
2022-02-06 12:01:19,795 [DEBUG] models.tsp: Current tour '7' cost: 15.121
2022-02-06 12:01:19,799 [DEBUG] models.tsp: Current tour '8' cost: 11.531
2022-02-06 12:01:19,801 [DEBUG] models.tsp: Current tour '9' cost: 10.945
2022-02-06 12:01:19,803 [DEBUG] models.tsp: Current tour '10' cost: 9.657
2022-02-06 12:01:19,805 [DEBUG] models.tsp: Current tour '11' cost: 9.657
2022-02-06 12:01:19,810 [INFO] utils.solver_funcs: [Run:1] --> Cost: 9.657 / Best: 9.657 / Mean: 9.657 (0.018s)
2022-02-06 12:01:19,811 [INFO] utils.solver_funcs: Exporting 'hexagon_2d_9.657.tsp' file to solutions folder
```

### Example of a silent run 

```
2022-02-06 12:04:19,830 [INFO] utils.solver_funcs: Importing .tsp file 'a280.tsp'
2022-02-06 12:04:19,840 [INFO] utils.solver_funcs: Using 'cost_func_2d' for edge type 'EUC_2D'
2022-02-06 12:04:22,707 [INFO] utils.solver_funcs: [Run:1] --> Cost: 2823.337 / Best: 2823.337 / Mean: 2823.337 (2.709s)
2022-02-06 12:04:25,009 [INFO] utils.solver_funcs: [Run:2] --> Cost: 2821.078 / Best: 2821.078 / Mean: 2822.207 (2.289s)
2022-02-06 12:04:27,422 [INFO] utils.solver_funcs: [Run:3] --> Cost: 2702.677 / Best: 2702.677 / Mean: 2782.364 (2.403s)
2022-02-06 12:04:29,818 [INFO] utils.solver_funcs: [Run:4] --> Cost: 2673.830 / Best: 2673.830 / Mean: 2755.230 (2.391s)
2022-02-06 12:04:32,355 [INFO] utils.solver_funcs: [Run:5] --> Cost: 2984.470 / Best: 2673.830 / Mean: 2801.078 (2.522s)
2022-02-06 12:04:35,237 [INFO] utils.solver_funcs: [Run:6] --> Cost: 2781.378 / Best: 2673.830 / Mean: 2797.795 (2.876s)
2022-02-06 12:04:37,571 [INFO] utils.solver_funcs: [Run:7] --> Cost: 2743.860 / Best: 2673.830 / Mean: 2790.090 (2.325s)
2022-02-06 12:04:40,421 [INFO] utils.solver_funcs: [Run:8] --> Cost: 2724.558 / Best: 2673.830 / Mean: 2781.898 (2.843s)
2022-02-06 12:04:43,899 [INFO] utils.solver_funcs: [Run:9] --> Cost: 2639.497 / Best: 2639.497 / Mean: 2766.076 (3.473s)
2022-02-06 12:04:47,032 [INFO] utils.solver_funcs: [Run:10] --> Cost: 2943.038 / Best: 2639.497 / Mean: 2783.772 (3.125s)
2022-02-06 12:04:47,032 [INFO] utils.solver_funcs: Exporting 'a280_2639.497.tsp' file to solutions folder
```


## Plotting

The main output from the improvement process is the .tsp file with nodes sorted as in the optimal tour found at improvement procedure. User can use this file and parse it to his preferred visualization tool. Although, a simple tool was designed to display 2D and 3D plots using [Plotly][plotly].

In plot_funcs.py, there are two functions to plot either 2D or 3D graphs using as input the .tsp file. After running those functions, a html file is exported at 'plots' folder, which can be viewed using the browser.

Example of the plot result using a280.tsp instance
![plot_sample.png](plot_sample.png)

## Packages and Versions

- OS: Windows 10
- Python: 3.7.0 64bit
- Additional Packages: plotly==5.5.0 

[lk_article]: https://doi.org/10.1287%2Fopre.21.2.498
[lkh_article]: https://doi.org/10.1016%2FS0377-2217%2899%2900284-2
[lkh]: http://webhotel4.ruc.dk/~keld/research/LKH/
[arthur]: https://arthur.maheo.net/implementing-lin-kernighan-in-python/
[tsplib]: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
[plotly]: https://plotly.com/python/