import os
import math
import numpy as np
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from kmeans import kmeans
from visualize import visualization as vis

def main():
    filename = input("Enter the name of file: ").strip()
    filepath = f"../data/{filename}"

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    coords = np.loadtxt(filepath)
    numNodes = len(coords)

    ready_time = (datetime.now(ZoneInfo("America/Los_Angeles")) + timedelta(minutes=5)).strftime("%I:%M%p").lower()
    print(f"There are {numNodes} nodes: Solutions will be available by {ready_time}\n")

    if numNodes > 4096:
            print(f"Warning: There are more than 4096 nodes.")
            
    allSolutions = []

    # Running kmeans for 1–4 drones --> 10 times each
    for numDrones in range(1, 5):
        bestSolution = None
        bestDistance = float("inf")

        for i in range(10):
            result = kmeans(coords, numDrones)
            if result["totalDistance"] < bestDistance:
                bestDistance = result["totalDistance"]
                bestSolution = result

        allSolutions.append(bestSolution)

        print(f"{numDrones}) If you use {numDrones} drone(s), the total route will be {bestSolution['totalDistance']:.1f} meters")
        if bestSolution['totalDistance'] > 6000:
            print(f"Warning: Solution is {bestSolution['totalDistance']:.1f} meters, which is greater than the 6000-meter constraint. ")
        for i, c in enumerate(bestSolution["clusters"], 1):
            pad = c["center"]
            print(f"   {i}. Landing Pad {i} should be at [{int(pad[0])},{int(pad[1])}], "
                  f"serving {len(c['route'])} locations, route is {c['distance']:.1f} meters")
        print()

    # print("Objective Function Values (k-means: sum of squared distances):")
    # for i, sol in enumerate(allSolutions, 1):
    #     print(f"  {i} drone(s): {sol['objective']:.2f}")
    # print()

    choice = int(input("\nSelect number of drones (1–4): "))
    chosen = allSolutions[choice - 1]
    base = filename.replace(".txt", "").split("/")[-1]
    folder = "../solutions/"

    for i, cluster in enumerate(chosen["clusters"], 1):
        dist = int(cluster["distance"])
        outputPath = f"{folder}{base}_{i}_solution_{dist}.txt"
        np.savetxt(outputPath, cluster["route"], fmt="%.4f")
        print(f"  Saved {outputPath}")
    
    vis(f"{folder}{base}", chosen["clusters"])
    print("\nAll done. Routes saved in /solutions/ folder.")

if __name__ == "__main__":
    main()