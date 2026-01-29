import numpy as np
import time, random, threading

from nearestNeighbor import NearestNeighborDistance as nn
from nearestNeighbor import euclideanDistance as ed

def calculateDistance(dataPts, route):
    totalDistance = 0.0
    for i in range(len(route) - 1):
        a = route[i]
        b = route[i + 1]
        totalDistance += ed(dataPts[a - 1], dataPts[b - 1])
    return totalDistance

def augmentedNearestNeighbor(dataPts):
    stop = threading.Event()  

    def waitForEnter():
        input("Press ENTER if you want to stop the search!\n")
        stop.set()

    threading.Thread(target=waitForEnter, daemon=True).start()

    startTimer = time.time()
    bestDistance, bestRoute, timing = nn(dataPts)

    print("Running augmented nearest neighbor (press ENTER to stop)...\n")
    print("Shortest Distance So Far:\n")

    while not stop.is_set():
        
        newRoute = list(bestRoute)
        i, j = random.sample(range(2, len(newRoute) - 1), 2)
        newRoute[i], newRoute[j] = newRoute[j], newRoute[i]

        if random.random() < 0.1:
            inner = newRoute[1:-1]
            random.shuffle(inner)
            newRoute = [newRoute[0]] + inner + [newRoute[-1]]

        newDistance = calculateDistance(dataPts, newRoute)
        if newDistance < bestDistance: 
            bestDistance = newDistance
            bestRoute = list(newRoute)
            print(round(bestDistance, 2))

        time.sleep(0.001)

    endTimer = time.time()
    runTime = endTimer - startTimer

    if bestDistance > 6000:
        print(f"Warning: Solution is {round(bestDistance, 1)} greater than the 6000-meter constraint.")

    return bestDistance, bestRoute, runTime
