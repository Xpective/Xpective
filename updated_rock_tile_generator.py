
from PIL import Image, ImageDraw, ImageFilter
import random
import math
import numpy as np
import matplotlib.tri as tri

PHI = 1.61803398875
GOLDEN_ANGLE = 2 * math.pi / PHI

def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        seq = [0, 1]
        for i in range(2, n):
            seq.append(seq[i-1] + seq[i-2])
        return seq

def generate_simple_noise_texture(width, height):
    texture = Image.new('L', (width, height))
    pixels = texture.load()

    for y in range(height):
        for x in range(width):
            val = int(random.uniform(0, 255))
            pixels[x, y] = val

    return texture

def apply_texture_to_shapes(base_image, texture):
    base_pixels = base_image.load()
    texture_pixels = texture.load()

    width, height = base_image.size
    result_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    result_pixels = result_img.load()

    for y in range(height):
        for x in range(width):
            base_pixel = base_pixels[x, y]
            texture_pixel = texture_pixels[x, y]

            if base_pixel[3] > 0:  # Check if the pixel is not transparent
                combined_pixel = (
                    int(base_pixel[0] * texture_pixel / 255),
                    int(base_pixel[1] * texture_pixel / 255),
                    int(base_pixel[2] * texture_pixel / 255),
                    base_pixel[3]
                )
                result_pixels[x, y] = combined_pixel

    return result_img

def add_crack(draw, form, base_length):
    start_x, start_y = form[0]
    crack_colors = ["#1d1616", "#4c3c3c"]
    color = random.choice(crack_colors)
    
    points = [(start_x, start_y)]
    fib_lengths = fibonacci(6)
    
    current_angle = random.uniform(0, 2*math.pi)
    for length in fib_lengths[2:]:
        segment_length = base_length * length / max(fib_lengths)
        end_x = start_x + segment_length * math.cos(current_angle)
        end_y = start_y + segment_length * math.sin(current_angle)
        points.append((end_x, end_y))
        
        start_x, start_y = end_x, end_y
        current_angle += GOLDEN_ANGLE + random.uniform(-1, 1) * 0.5  # Variation hinzufügen

    draw.line(points, fill=color, width=2)

def get_shade_of_brown(factor):
    r_base = 90
    g_base = 70
    b_base = 61

    r_variation = int(r_base * factor) % 256
    g_variation = int(g_base * factor) % 256
    b_variation = int(b_base * factor) % 256

    color = "#{:02x}{:02x}{:02x}".format(r_variation, g_variation, b_variation)
    return color

def triangulate_polygon(points, color_factor):
    x_points = [point[0] for point in points]
    y_points = [point[1] for point in points]
    
    triang = tri.Triangulation(x_points, y_points)
    tri_areas = np.array([0.5 * np.abs(np.cross(triang.x[triangle], triang.y[triangle]))
                          for triangle in triang.triangles])
    normed_areas = (tri_areas - tri_areas.min()) / (tri_areas.max() - tri_areas.min())
    colors = plt.cm.gray_r(normed_areas * color_factor)
    
    triangles = []
    for i, triangle in enumerate(triang.triangles):
        color = colors[i].mean(axis=0)
        hex_color = "#{:02x}{:02x}{:02x}".format(int(color[0]*255), int(color[1]*255), int(color[2]*255))
        triangles.append((triang.x[triangle].tolist(), triang.y[triangle].tolist(), hex_color))
        
    return triangles

def generate_rock_tile_simplified(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    num_layers = 7
    current_size = width / 2
    for layer in range(num_layers):
        factor = (0.9 ** (num_layers - layer)) + random.uniform(-0.1, 0.1)
        color = get_shade_of_brown(factor)

        center = (width/2, height/2)
        angle = (2 * math.pi) / (layer + 7)  # Starting with a heptagon
        points = [(center[0] + current_size * math.cos(n * angle), center[1] + current_size * math.sin(n * angle)) for n in range(layer + 7)]
        
        triangles = triangulate_polygon(points, factor)
        for triangle in triangles:
            x_points, y_points, color = triangle
            draw.polygon(list(zip(x_points, y_points)), fill=color)

        if layer != 0:  # Risse nur ab dem zweiten Layer hinzufügen
            for point in points:
                if random.random() > 0.3:  # 70% chance to create a crack from each vertex
                    add_crack(draw, [point], current_size / 2)

        scale_factor = random.uniform(1.4, 1.8)
        current_size /= scale_factor

    img = img.filter(ImageFilter.GaussianBlur(radius=2))

    texture = generate_simple_noise_texture(width, height)
    final_img = apply_texture_to_shapes(img, texture)

    return final_img

if __name__ == '__main__':
    tile_simplified = generate_rock_tile_simplified(256, 256)
    tile_simplified.show()
