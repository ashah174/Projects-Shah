import numpy as np
import math, time

#basic KNN algorithm - used geeksforgeeks for algorithm reference
def euclideanDistance(x, y):
    total = 0
    for i in range(len(x)):
        total += ((x[i]-y[i])**2)
    return math.sqrt(total)

def NearestNeighborDistance (dataPts, landingPad): 

    routing_data = np.vstack([landingPad, dataPts])
    n_total = len(routing_data)
    visited = [False] * n_total 
    
    route = [0]
    visited[0] = True
    totalDistance = 0.0
    currIndex = 0

    for step in range(n_total - 1): 
        nearestIndex = -1
        nearestDistance = float("inf")

        for j in range(n_total): 
            if not visited[j]:
                d = euclideanDistance(routing_data[currIndex], routing_data[j])
                if d < nearestDistance:
                    nearestDistance = d
                    nearestIndex = j
        
        if nearestIndex == -1:
             break 
                
        route.append(nearestIndex)
        visited[nearestIndex] = True
        totalDistance += nearestDistance
        currIndex = nearestIndex

    backToPad = euclideanDistance(routing_data[currIndex], routing_data[0])
    totalDistance += backToPad
    route.append(0)

    return route, totalDistance