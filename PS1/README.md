# COMS BC 3997 - F22
# PS1: Grid, Informed, and Random Search Algorithms
* Due: 5pm, Friday September 30th

In this assignment, you will implement the random search algorithm RRT and implement (informed) search algorithms to help Pacman find paths in a maze. Note: We will use the Pacman framework developed at Berkeley. This framework is used worldwide to teach AI, therefore it is very important that you DO NOT publish your solutions online.

## Written Assignment (16 points)

Please go to the PDF in the written folder for the written instructions.

Question 1 (4 points)

Question 2 (2 points)

Question 3 (2 points)

Question 4 (3 points)

Question 5 (2 points)

Question 6 (3 points)

## RRT Algorithm (8 points + 1 bonus)

<img src="https://upload.wikimedia.org/wikipedia/en/thumb/f/f5/RRT_graph1.png/300px-RRT_graph1.png">

**Files you'll edit (and thus submit to Gradescope for Autograding):**

`util.py` 	Where all of your RRT helper functions will go.

In this section, you'll be implementing the RRT robotic planning algorithm. All code can be found in the `rrt` folder. Your goal will be to implement several functions in `util.py` to successfully find a path from a source point to the goal using RRT. This path should avoid collisions with obstacles.

**NOTE: You need to install pygame for this to run: `pip3 install pygame`**

Functions that should be filled in for full credit are:
* `winCondition`    - 1 point
* `nearestNode`     - 1 point
* `getNewPoint`     - 1 point
* `extend`          - 2 points
* `isCollisionFree` - 3 points

To test your implementation, there are three maps that increase in difficulty:
* `python3 runNoObs.py` -- no obstacles (you can test your other functions with this before implementing `isCollisionFree` -- just make sure `isCollisionFree` returns True always -- should take 500ish iterations)
* `python3 runBasicObs.py` -- some basic obstacles that you can test with that will still finish quickly (again around 500ish iterations)
* `python3 runBugtrap.py` -- start in a bugtrap (should take a couple thousand iterations)
* `python3 runDoubleBugtrap.py` -- start and end in a bugtrap (a very hard problem for RRT, this could take some time)

Note: Sometimes the graphics will make it appear that a vaild solution is just barely crossing the tip of a diagonal line and that is ok!

Note2: By construction our tests will never take a step that is bigger than an obstacle so you do not need to worry about collisions in the middle of your extensions. [You're welcome :-)](https://www.youtube.com/watch?v=79DijItQXMM)

#### Bi-Directional RRT - 1 Bonus Point
For one bonus point implement a new file called ```bi-rrt.py``` which implements the bi-directional RRT algorithm as we discussed in class. As a reminder, this algorithm builds two trees, one starting from the start state, and another form the goal. At each iteration the first tree grows as a standard RRT tree while the second tree grows towards the new state added to the first tree. The algorithm exits when the trees meeet. As a hint, it likely makes sense to copy the ``rrt.py`` file and simply make a few modificaitons. **Note: this file will need to be manually graded and so make sure to push your solution to GitHub and make a note on your written assignment that you did the bonus question!**


## Pacman (16 points + 1 bonus)

![Pacman](https://upload.wikimedia.org/wikipedia/en/5/59/Pac-man.png)

**Files you'll edit (and thus submit to Gradescope for Autograding):**

`search.py` 		Where all of your search algorithms will reside.

`searchAgents.py` 	Where all of your search-based agents will reside.

Welcome to the first Pacman problem set of the semester. In this project, your Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. You will build general search algorithms and apply them to Pacman scenarios. For those of you who aren't familiar with Pacman, he is a character from an old video game that runs around a maze trying to capture all the dots without getting eaten by the ghosts. Pacman can also eat the special large dots to powerup into ghost eating mode. Throughout the semester we will code up more and more sophisticated Pacman agents based on the algorithms we are learning about in class.

**While these problem sets follow the Berkely material closely we wil sometimes provide additional hints in our instructions and will sometimes NOT do part of the Berkeley assignment. Therefore please always follow the instructions given in these README files.**

**These projects will be graded with the autograder which is run using `python3 autograder.py`. Make sure your code passes all tests before the deadline!**

Files you might want to look at:

`pacman.py` 	The main file that runs Pacman games. This file describes a Pacman GameState type, which you use in this project.

`game.py` 		The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.

`util.py` 		Useful data structures for implementing search algorithms.

The rest of the files are simply supporting files for graphics and scaffolding for various game play and grading operations.

### Introduction

Welcome to Pacman

After downloading the code you should be able to play a game of Pacman by typing the following at the command line:

`python3 pacman.py`

Pacman lives in a shiny blue world of twisting corridors and tasty round treats. Navigating this world efficiently will be Pacman's first step in mastering his domain.

The simplest agent in `searchAgents.py` is called the `GoWestAgent`, which always goes West (a trivial reflex agent). This agent can occasionally win:

`python3 pacman.py --layout testMaze --pacman GoWestAgent`

But, things get ugly for this agent when turning is required:

`python3 pacman.py --layout tinyMaze --pacman GoWestAgent`

If Pacman gets stuck, you can exit the game by typing `CTRL-c` into your terminal.

Soon, your agent will solve not only `tinyMaze`, but any maze you want.

Note that `pacman.py` supports a number of options that can each be expressed in a long way (e.g., `--layout`) or a short way (e.g., `-l`). You can see the list of all options and their default values via:

`python3 pacman.py -h`

Also, all of the commands that appear in this project also appear in `commands.txt`, for easy copying and pasting. In UNIX/Mac OS X, you can even run all these commands in order with `bash commands.txt`.

Note: if you get error messages regarding Tkinter, see <a href="http://tkinter.unpythonic.net/wiki/How_to_install_Tkinter">this page</a>.

### Question 1 (3 points): Finding a Fixed Food Dot using Depth First Search

In `searchAgents.py`, you'll find a fully implemented `SearchAgent`, which plans out a path through Pacman's world and then executes that path step-by-step. The search algorithms for formulating a plan are not implemented -- that's your job.

First, test that the `SearchAgent` is working correctly by running:

`python3 pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch`

The command above tells the `SearchAgent` to use `tinyMazeSearch` as its search algorithm, which is implemented in `search.py`. Pacman should navigate the maze successfully.

Now it's time to write full-fledged generic search functions to help Pacman plan routes! Remember that a search node must contain not only a state but also the information necessary to reconstruct the path (plan) which gets to that state.

Important note: All of your search functions need to return a list of actions that will lead the agent from the start to the goal. These actions all have to be legal moves (valid directions, no moving through walls).

Important note: Make sure to use the `Stack`, `Queue` and `PriorityQueue` data structures provided to you in `util.py`! These data structure implementations have particular properties which are required for compatibility with the autograder.

Hint: Each algorithm is very similar. Algorithms for DFS, BFS, UCS, and A* differ only in the details of how the fringe is managed. So, concentrate on getting DFS right and the rest should be relatively straightforward. **Indeed, one possible implementation requires only a single generic search method which is configured with an algorithm-specific queuing strategy. (Your implementation need not be of this form to receive full credit but you may find it very helpful).**

Implement the depth-first search (DFS) algorithm in the depthFirstSearch function in search.py. To make your algorithm complete, write the graph search version of DFS, which avoids expanding any already visited states.

Your code should quickly find a solution for:

`python3 pacman.py -l tinyMaze -p SearchAgent`

`python3 pacman.py -l mediumMaze -p SearchAgent`

`python3 pacman.py -l bigMaze -z .5 -p SearchAgent`

The Pacman board will show an overlay of the states explored, and the order in which they were explored (brighter red means earlier exploration). Is the exploration order what you would have expected? Does Pacman actually go to all the explored squares on his way to the goal?

Hint: If you use a `Stack` as your data structure, the solution found by your DFS algorithm for `mediumMaze` should have a length of 130 (provided you push successors onto the fringe in the order provided by `getSuccessors`; you might get 246 if you push them in the reverse order). Is this a least cost solution? If not, think about what depth-first search is doing wrong.

**REMEMBER TO RUN `python3 autograder.py -q q1` to make sure you pass all the grading tests for q1!**

### Question 2 (3 points): Breadth First Search

Implement the breadth-first search (BFS) algorithm in the `breadthFirstSearch` function in `search.py`. Again, write a graph search algorithm that avoids expanding any already visited states. Test your code the same way you did for depth-first search.

`python3 pacman.py -l mediumMaze -p SearchAgent -a fn=bfs`

`python3 pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5`

Does BFS find a least cost solution? If not, check your implementation.

Hint: If Pacman moves too slowly for you, try the option `--frameTime 0`.

Note: If you've written your search code generically, your code should work equally well for the eight-puzzle search problem without any changes.

`python3 eightpuzzle.py`

As always remember to run `python3 autograder.py -q q2` to make sure you pass all the grading tests for q2!

### Question 3 (3 points): Varying the Cost Function

While BFS will find a fewest-actions path to the goal, we might want to find paths that are "best" in other senses. Consider `mediumDottedMaze` and `mediumScaryMaze`.

By changing the cost function, we can encourage Pacman to find different paths. For example, we can charge more for dangerous steps in ghost-ridden areas or less for steps in food-rich areas, and a rational Pacman agent should adjust its behavior in response.

Implement the uniform-cost graph search algorithm in the `uniformCostSearch` function in `search.py`. We encourage you to look through `util.py` for some data structures that may be useful in your implementation. You should now observe successful behavior in all three of the following layouts, where the agents below are all UCS agents that differ only in the cost function they use (the agents and cost functions are written for you):

`python3 pacman.py -l mediumMaze -p SearchAgent -a fn=ucs`

`python3 pacman.py -l mediumDottedMaze -p StayEastSearchAgent`

`python3 pacman.py -l mediumScaryMaze -p StayWestSearchAgent`

Note: You should get very low and very high path costs for the `StayEastSearchAgent` and `StayWestSearchAgent` respectively, due to their exponential cost functions (see `searchAgents.py` for details).

As always remember to run `python3 autograder.py -q q3` to make sure you pass all the grading tests for q3!

### Question 4 (3 points): A* search

Implement A* graph search in the empty function `aStarSearch` in `search.py`. A* takes a heuristic function as an argument. Heuristics take two arguments: a state in the search problem (the main argument), and the problem itself (for reference information). The `nullHeuristic` heuristic function in `search.py` is a trivial example.

You can test your A* implementation on the original problem of finding a path through a maze to a fixed position using the Manhattan distance heuristic (implemented already as `manhattanHeuristic` in `searchAgents.py`).

`python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic`

You should see that A* finds the optimal solution slightly faster than uniform cost search (about 549 vs. 620 search nodes expanded in our implementation, but ties in priority may make your numbers differ slightly). What happens on openMaze for the various search strategies?

As always remember to run `python3 autograder.py -q q4` to make sure you pass all the grading tests for q4!

### Question 5 (4 points + 1 bonus): Eating All The Dots

**Note: Make sure to complete Question 4 before working on Question 5, because Question 5 builds upon your answer for Question 4.**

Now we'll solve a hard search problem: eating all the Pacman food in as few steps as possible. For this, we'll need a new search problem definition which formalizes the food-clearing problem: `FoodSearchProblem` in `searchAgents.py` (implemented for you). A solution is defined to be a path that collects all of the food in the Pacman world. For the present project, solutions do not take into account any ghosts or power pellets; solutions only depend on the placement of walls, regular food and Pacman. (Of course ghosts can ruin the execution of a solution and we'll need different algorithms to consider those scenarios!) If you have written your general search methods correctly, A* with a null heuristic (equivalent to uniform-cost search) should quickly find an optimal solution to testSearch with no code change on your part (total cost of 7).

`python3 pacman.py -l testSearch -p AStarFoodSearchAgent`

Note: `AStarFoodSearchAgent` is a shortcut for `-p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristic`.

You should find that UCS starts to slow down even for the seemingly simple tinySearch. As a reference, our implementation takes 2.5 seconds to find a path of length 27 after expanding 5057 search nodes.

Fill in `foodHeuristic` in `searchAgents.py` with a consistent heuristic for the `FoodSearchProblem`. Try your agent on the `trickySearch` board:

`python3 pacman.py -l trickySearch -p AStarFoodSearchAgent`

Our UCS agent finds the optimal solution in about 13 seconds, exploring over 16,000 nodes.

Any non-trivial non-negative consistent heuristic will receive 1 point. Make sure that your heuristic returns 0 at every goal state and never returns a negative value. Depending on how few nodes your heuristic expands, you'll get additional points.

Remember: If your heuristic is inconsistent, you will receive no credit, so be careful! Can you solve mediumSearch in a short time? If so, we're either very, very impressed, or your heuristic is inconsistent.

|Number of nodes expanded |	Grade |
| ------ | --------|
|more than 15000 |	1/4|
|at most 15000 |	2/4|
|at most 12000 |	3/4|
|at most 9000 |	4/4 (full credit; medium)|
|at most 7000 |	5/4 (optional extra credit; hard)|

As always remember to run `python3 autograder.py -q q7` to make sure you pass all the grading tests for q7!

**This one may take a little while to run depending on your heuristic but it shouldn't take more than a minute (unless you are printing out a ton of things)!**

**Hint: what is an UNDERESTIMATE of the distance you will have to travel!**

### Important Note:

The autograder is king so make sure that your implementation follows the spec asked for by the instructions. If you are running into errors maybe you are avoiding pushing valid paths to the frontier because you are making an optimization that is valid in the BFS case but not in the A* case. If the spec did not ask for this optimization it may cause the autograder to fail. This is another reason why we suggest using a general search! There will be less things to debug and less areas to do a weird quirk if you are trying to be generic! Also you should not have to modify the stack, queue, or priority queue data structures at all to accomplish this homework!

Finally you can run the autograder as many times as you'd like before submitting and can submit multiple times as well just make sure the final code passes all of the tests via `python autograder.py`!

**You must submit to gradescope to get credit for the assignment --- make sure you submit the required files before the deadline!**

### Want more practice with Informed Search and Heuristics?

There are additional problems as part of the Berkeley Pset that you can explore. Check out the instructions for their [project1 from Spring 2022](https://inst.eecs.berkeley.edu/~cs188/sp22/project1/). As we have modified their files to remove some of those extra problems you will want to download the zip from their website and then copy over your modified `search.py` and `searchAgents.py` files.