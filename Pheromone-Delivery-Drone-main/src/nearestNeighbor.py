import numpy as np
import math, time

#basic KNN algorithm - used geeksforgeeks for algorithm reference
def euclideanDistance(x, y):
    total = 0
    for i in range(len(x)):
        total += ((x[i]-y[i])**2)
    return math.sqrt(total)

def NearestNeighborDistance (dataPts):

    startTimer = time.time()

    n = len(dataPts)
    visited = [False] * n
    route = [0]
    visited[0] = True
    totalDistance = 0.0
    currIndex = 0

    for step in range(n-1):
        nearestIndex = -1
        nearestDistance = float("inf")

        for j in range(n):
            if not visited[j]:
                d = euclideanDistance(dataPts[currIndex], dataPts[j])
                if d < nearestDistance:
                    nearestDistance = d
                    nearestIndex = j
        
        route.append(nearestIndex)
        visited[nearestIndex] = True
        totalDistance += nearestDistance
        currIndex = nearestIndex

    backToBase = euclideanDistance(dataPts[currIndex], dataPts[0])
    totalDistance += backToBase
    route.append(0)

    route = [x + 1 for x in route]

    endTimer = time.time()

    if totalDistance > 6000:
        print("Warning: Solution is ", totalDistance, "greater than the 6000-meter constraint. ")

    # print("\nBest Distance:", round(totalDistance, 1), "meters")
    # print("Best Route:", route)
    # print("Runtime:", round(endTimer - startTimer, 4), "seconds\n")

    return totalDistance, route, endTimer - startTimer


# #===============================================================

# #temporary test cases
# if __name__ == "__main__":
#     samplePoints = np.array([
#         [9.1113464e+00, 9.2960887e+01],
#         [5.7620938e+01, 6.9666720e+01],
#         [6.8336324e+01, 5.8279097e+01],
#         [5.4659311e+01, 8.1539721e+01],
#         [4.2572884e+01, 8.7901390e+01],
#         [6.4444278e+01, 9.8891162e+01],
#         [6.4761763e+01, 5.2237536e-02]
#     ])

#     startTimer = time.time()
#     route, distance = NearestNeighborDistance(samplePoints)
#     endTimer = time.time()

#     runTime = endTimer - startTimer
#     print("Route:", route)
#     print("Total Distance:", round(distance, 2))
#     print("Runtime:", round(runTime, 4), "s")