# Python Path Finding Visualizer

Welcome to Pathfinding Visualizer! I built this application because I was fascinated by pathfinding algorithms, and I wanted to visualize them in action. I hope that you enjoy playing around with this visualization tool just as much as I enjoyed building it.

## Meet the Path Finding Algorithms

This application supports the following algorithms:

**A\* Search** - Uses two heuristics to track the weight of each checked node with respect to the starting node and the distance to the end node; guarantees the shortest path.

**Bidirectional A\* Search** - Like traditional A*, but searches from both the start and end nodes simultaneously to find the end path faster; guarantees the shortest path.

**Genetic Path Algorithm** - Uses genetic populations and fitness calculations to progressively find a shorter and shorter path to the end node; does not guarantee finding any path.

**Depth-first Search** - Basic slow pathfinding algorithm that checks every node until the end node sequentially; does not guarantee the shortest path.

**Breadth-first Search** - Basic slow pathfinding algorithm that checks every node until the end node sequentially; guarantees the shortest path.

**Bidirectional Breadth-first Search** - Like traditional BFS, but searches from both the start and end nodes simultaneously to find the end path faster; guarantees the shortest path.

**Greedy Best-first Search** - A faster, more heuristic-heavy version of A* using only the distance to the end node as the sole heuristic; does not guarantee the shortest path

**Random Walk Search** - Progressively generates a path to the end node by randomly selecting from all node neighbor choices; does not guarantee finding any path.

On top of the pathfinding algorithms listed above, I implemented a **Recursive Division** Maze Generation algorithm.

Additional feature: After initial path generation of a specific algoreithm is complete, drag the start and end points of the final path around to see your path continually change. You can even add obstacles and drag around the start and end points to see your final path update in real time!

## More About the Genetic Path Algorithm

This algorithm is one I developed using existing genetic machine learning techniques. At its heart, it involves a population of several genetic players. Each genetic player has a "brain" that is basically a list of preset directions that forms a path. This path is intially comprised of random directions. In each "generation" each player in the genetic population can move until they hit the border of the grid or any obstacle, in which case it would die for this generation, or the end node, where it would be a "winner" for this generation. When all the genetic players have either "died" or "won". A fitness function is calculated for each player: if the player is a winner, then the fitness function is weighted by how few steps are taken to reach the end node (lower steps = higher fitness); if the player died, then the fitness function is weighted by the distance to the end node (lower distance = higher fitness). A winner will always have a higher fitness than a dead player. After the fitness is calculated, a "best player" is selected for this generation and is cloned into the next generation. All the other players are ordered by fitness in descending order, and have their brains randomly mutated (the preset list of directions that make up the "brain" is randomly changed), with the players with lower fitness being mutated more than the players with higher fitness. This process then continues until the path is not optimized between successive generations, or in the case where no path is found, until a generation limit is reached.


## More About the Random Walk Search

This is algorithm I researched online, but added a unique twist in how the current path is generated. At any given node in a Random Walk Search, the next node is randomly chosen from a list of possible neighboring nodes. This can include a node already in the current path (a backtracking feature if the path is stuck in a dead end). In this case, the path continuously deletes itself until the "next node" node is reached, or if the starting node is reached. This allows the Random Walk path to loop back on itself and start at a far-back previous node if it is moving in an opposite direction with respect to the end node. This process continuously repeats until the end node is reached or a path-step limit is reached, in which case no path would be found.

## Getting Started

First, install the necessary python modules.
```bash
pip3 install -r requirements.txt
```

Then, in the main directory, run the main python file to start up the visualizer.

```bash
python3 GameFramework.py
```
