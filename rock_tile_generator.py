
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

def generate_rock_tile():
    # Constants
    phi = (1 + np.sqrt(5)) / 2  # Golden ratio
    pi = np.pi

    # Generate random points
    num_points = 1000
    x_points = np.random.rand(num_points)
    y_points = np.random.rand(num_points)

    # Add more dense points in certain regions to create contrast
    for _ in range(200):
        x_points = np.append(x_points, 0.4 + 0.2 * np.random.rand())
        y_points = np.append(y_points, 0.4 + 0.2 * np.random.rand())

    # Perform triangulation
    triang = tri.Triangulation(x_points, y_points)

    # Create a colormap based on triangle area (smaller triangles are darker)
    tri_areas = np.array([0.5 * np.abs(np.cross(triang.x[triangle], triang.y[triangle]))
                          for triangle in triang.triangles])
    normed_areas = (tri_areas - tri_areas.min()) / (tri_areas.max() - tri_areas.min())
    colors = plt.cm.gray_r(normed_areas)

    # Plot the triangulated image
    plt.figure(figsize=(8, 8))
    for i, triangle in enumerate(triang.triangles):
        color = colors[i].mean(axis=0)  # Taking mean of the colors
        plt.fill(triang.x[triangle], triang.y[triangle], color=color, edgecolor='k', alpha=0.6)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    generate_rock_tile()

