import numpy as np
from scipy.spatial import Delaunay
from PIL import Image, ImageDraw
import math

def generate_clustered_rock_tile_v3():
    img = Image.new("RGBA", (800, 800), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Define the color palette
    colors = {
        "black": "#000000",
        "dark_gray": "#2c2c2c",
        "dark_brown": "#3b2f2f",
        "contour_brown": "#2a1d1d",
        "contour_gray": "#1d1d1d"
    }

    # Generate a big irregular cluster using pi and phi
    cluster_center = (400, 400)
    cluster_points = []
    for i in range(10):
        angle = 2 * math.pi * i / 10
        distance = 300 + 100 * math.sin(3 * angle)  # To create variation
        x = cluster_center[0] + distance * math.cos(angle)
        y = cluster_center[1] + distance * math.sin(angle)
        cluster_points.append((x, y))

    draw.polygon(cluster_points, fill=colors["black"])

    # Generate random points within the cluster
    points = np.array([(x, y) for x in range(800) for y in range(800) if img.getpixel((x, y))[:3] == (0, 0, 0)])
    points = points[np.random.choice(points.shape[0], 1000, replace=False)]

    tri = Delaunay(points)

    for simplex in tri.simplices:
        triangle = [tuple(point) for point in tri.points[simplex]]
        avg_dist = sum([point[0]**2 + point[1]**2 for point in triangle]) / 3.0
        triangle_image = Image.new("L", img.size)
        ImageDraw.Draw(triangle_image).polygon(triangle, fill=1)
        triangle_area = np.array(triangle_image).sum()

        if avg_dist < (0.3 * 800**2):
            color = colors["dark_brown"]
            contour_color = colors["contour_brown"] if triangle_area > 2000 else None
        else:
            color = colors["dark_gray"]
            contour_color = colors["contour_gray"] if triangle_area > 2000 else None

        draw.polygon(triangle, fill=color, outline=contour_color)

    return img

if __name__ == "__main__":
    img = generate_clustered_rock_tile_v3()
    img.show()

