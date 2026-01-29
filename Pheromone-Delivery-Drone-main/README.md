# Pheromone-Delivery-Drone
## CS 179M Fall 2025 - Dr. Eamonn Keogh

## Overview
A pest, the naval orangeworm, is infesting almonds on an almond farm owned by Mr. Keogh. We want to find a way to mitigate pest damage, as crop losses have increased rapidly.

There are insect surveillance sensors in place to collect information about the insects, but the methods to eliminate them are expensive. The solution found was to use Pheromone-Based Mating Distribution (PBMD), which involves applying pheromone paste with a drone to confuse male insects from finding females. This approach is safer for the environment and more effective.

The problem we are trying to solve is that the drone's current flight time is too high, resulting in wasted battery. Therefore, our goal is to minimize the flight path length, given the list of locations the drone carrying the pheromone paste must visit. We will determine the shortest route that the drone needs to take to complete its task and return to its starting/charging point.

## Execution

1. Run the code by using this command in the terminal &rarr; python main.py
2. When prompted for a file, enter the name of a file of your choice. 
3. Then, when prompted for an algorithm, please choose one of the three algorithms we implemented by selecting 1, 2, or 3: Random Search, Nearest Neighbor, or Augmented Nearest Neighbor. 
4. Press ENTER to stop the algorithm from running for choices 1 and 3.
5. The output will be the best distance output to the command line, a .txt file containing the best route, and a .jpeg file containing a visualization of the route. 
