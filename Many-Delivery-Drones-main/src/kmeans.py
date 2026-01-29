import numpy as np
from nearestNeighbor import NearestNeighborDistance as nn 

def objectiveFunction(points, labels, centers):
    return float(np.sum((points - centers[labels]) ** 2))

def kmeans(points, k):
    points = np.array(points)
    n = len(points)

    # Step 2
    centers = points[np.random.choice(n, k, replace=False)]

    for j in range(100):

        # Step 3
        expandedPoints = points[:, np.newaxis]
        distances = np.linalg.norm(expandedPoints - centers, axis=2)
        labels = np.argmin(distances, axis=1)

        # Step 4
        newCenters = np.array([
            points[labels == i].mean(axis=0) if np.any(labels == i) else centers[i]
            for i in range(k)
        ])

        # Step 5
        if np.allclose(newCenters, centers):
            break
        centers = newCenters

    clusters = []

    for i in range(k):
        landingPad = centers[i]
        clusterPoints = points[labels == i]
        
        if len(clusterPoints) == 0:
            continue

        routing_data = np.vstack([landingPad, clusterPoints])
        route_indices, dist = nn(clusterPoints, landingPad)
        route_coords = routing_data[route_indices]
        clusters.append({
            "center": landingPad,
            "route": route_coords,
            "distance": dist
        })

    kmeansObj = objectiveFunction(points, labels, centers)
    totalDistance = sum(c["distance"] for c in clusters)

    return {"totalDistance": totalDistance, "objective": kmeansObj, "clusters": clusters}