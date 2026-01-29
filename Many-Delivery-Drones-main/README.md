# Pheromone-Delivery-Drone
## CS 179M Fall 2025 - Dr. Eamonn Keogh

## Overview
A pest known as the naval orangeworm has been causing significant damage to the almonds on Mr. Keogh’s farm. Crop losses have been rising, so finding a more efficient way to protect the orchard has become important.

The farm already uses insect surveillance sensors to track pest activity, but most traditional methods of eliminating the insects are costly. A more practical and environmentally friendly solution is Pheromone-Based Mating Disruption. This involves using a drone to apply pheromone paste across the orchard so male insects become confused and struggle to locate females. This reduces the overall infestation and helps protect crop yield.

The main problem we’re tackling is the drone’s limited flight time. The current routes are too long, which drains the battery and reduces how much ground the drone can cover. Our goal is to minimize the total distance the drone needs to travel while still making all required stops. The program builds an efficient path that lets the drone complete all deliveries and return to its starting point as quickly as possible. We also explore routes using one to four drones by applying K-means clustering and solving each cluster with a TSP approach based on the nearest neighbor method.

## Execution

1. Run the code by using this command in the terminal &rarr; python main.py
2. When prompted for a file, enter the name of a file of your choice. 
3. The output will list the landing pad locations, nodes visited, and routes for all possible numbers of drones
4. Then, when prompted, please enter the desired number of drones to be used.
5. The output will be a set of route files and a visualization that shows the exact paths taken by the drones.

Each route file contains the order in which the delivery points are visited and the distance of the whole trip. The program will also save a combined plot that displays all clusters and their routes together. This makes it easy to verify that each drone is covering a separate region and that the routes are as efficient as possible. Once the program finishes, you can open the solutions folder to view all route files and the final overall plot. 
