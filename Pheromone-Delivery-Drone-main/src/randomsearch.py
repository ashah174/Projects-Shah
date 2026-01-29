import random, time, math, threading

def randomSearch(coordinates):
    
    bestRoute = None
    bestDistance = math.inf
    stop = False

    def routeDistance(route):
        distance = 0

        for i in range(len(route) - 1):
            x1, y1 = coordinates[route[i] - 1]
            x2, y2 = coordinates[route[i + 1] - 1]
            distance += math.hypot(x1 - x2, y1 - y2)
        
        return distance

    def waitForEnter():
        nonlocal stop
        input("Press ENTER if you want to stop the search!\n")
        stop = True

    threading.Thread(target=waitForEnter, daemon=True).start()
    
    startTimer = time.time()
    print("Shortest Route Discovered So Far:\n")

    while not stop:

            route = [1] + random.sample(range(2, len(coordinates) + 1), len(coordinates) - 1) + [1]
            d = routeDistance(route)
            if d < bestDistance:
                bestDistance, bestRoute = d, route
                print(round(bestDistance, 1))

    endTimer = time.time()

    if round(bestDistance, 1) > 6000:
        print("Warning: Solution is ", round(bestDistance, 1), "greater than the 6000-meter constraint. ")

    # print("\nBest Distance =", round(bestDistance, 1), "meters")
    # print("Best Route =" , bestRoute)
    # print("Best Time =", round(endTimer - startTimer, 4), "seconds\n")

    return bestDistance, bestRoute, endTimer - startTimer