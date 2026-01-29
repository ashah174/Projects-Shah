import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, math

from randomSearch import randomSearch as rs
from nearestNeighbor import NearestNeighborDistance as nn
from augmented import augmentedNearestNeighbor as ann
from visualize import visualization as vis

def main():
    
    coordinates = []
    
    while True:
        filename = input("Enter the name of the file: ")
        filepath = f"../data/{filename}"

        try:
            with open(filepath, "r") as file:
                for line in file:
                    if len(line.split()) != 2:
                         raise ValueError("Error in file formatting! Every line needs two numbers")
                    x, y = map(float, line.split())

                    if x < 0 or y < 0:
                        raise ValueError("Coordinate values can not be negative.")
                    
                    if (x,y) in coordinates:
                        raise ValueError("Duplicate coordinate found. Skipping over")
                        continue
                    coordinates.append((x, y))             
            break
        except FileNotFoundError:
            print(f"Error: The file '{filename}' does not exist. Please try again.\n")
        except ValueError as e:
            print(f"Value is not recognized: {e}. Please try again.\n")
    
    if len(coordinates) == 0:
        print("No coordinates found in file")
        sys.exit()

    print("\nThere are", len(coordinates), "nodes.")

    if len(coordinates) > 256:
        print("The number of nodes exceeds 256! Try again with fewer nodes.")
        sys.exit()

    alg_type = input("\nChoose an algorithm to solve the Pheromone Delivery Drone problem.\n1. Random Search\n2. Nearest Neighbor\n3. Augmented Nearest Neighbor\n\nEnter choice: ")

    while alg_type not in ('1', '2', '3'):
        print("Invalid input. Please enter '1', '2', or '3'.")
        alg_type = input("1. Random Search\n2. Nearest Neighbor\n3. Augmented Nearest Neighbor\n")

    if alg_type == '1':
        print("Running Random Search Algorithm...")
        distance, route, time = rs(coordinates)

    elif alg_type == '2':
        print("Running Nearest Neighbor Algorithm...")
        distance, route, time = nn(coordinates)
        
    else:
        print("Running Augmented Nearest Neighbor Algorithm...")
        distance, route, time = ann(coordinates)
    
    if filename.endswith(".txt"):
        filename = filename[:-4]

    distance = math.ceil(distance)
    
    outputfile = filename + "_SOLUTION_" + str(distance) + ".txt"

    print("\nBest Distance:", distance, "meters")
    print("Best Route:", route)
    print("Runtime:", round(time, 4), "seconds\n")


    # INCLUDE THIS CODE TO CREATE NEW SOLUTION FILE
    # =============================================
    with open(outputfile, 'w') as f:
        for node in route:
            f.write(str(node) + ' ')
    # =============================================

    print("==> Route written to disk as", outputfile)
    vis(filename, coordinates, route, distance)
    print("\n")

if __name__ == "__main__":
    main()