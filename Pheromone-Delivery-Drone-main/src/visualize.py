import matplotlib.pyplot as plt
import math

def visualization(filename, coords, route, distance):

    route_coords = [coords[i - 1] for i in route]
    x = [p[0] for p in route_coords]
    y = [p[1] for p in route_coords]

    # ensures the smaller side = 1920 pixels
    width, height = 16, 12 
    dpi = 1920 / min(width, height) 
    plt.figure(figsize=(width, height), dpi=dpi)

    plt.plot(x, y, 'o-') # plots each point with a dot
    plt.plot(x[0], y[0], 'ro')  # to mark charger location in red
    plt.axis('off')

    img_file = f"{filename}_SOLUTION_{distance}.jpeg"
    plt.savefig(img_file)
    plt.close()

    print(f"==> Visualization saved as {img_file}")
