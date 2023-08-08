from PIL import Image, ImageDraw, ImageFilter
import random
import math
import numpy as np
from noise import pnoise2

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
    
    
def generate_perlin_texture(width, height):
    texture = Image.new('L', (width, height))  # L steht für Graustufen
    pixels = texture.load()

    # Parameter für das Perlin-Rauschen
    octaves = 6
    freq = 16.0 * octaves

    for y in range(height):
        for x in range(width):
            val = int(pnoise2(x/freq, y/freq, octaves=octaves, repeatx=1024, repeaty=1024, base=42) * 127.5 + 127.5)
            pixels[x, y] = val
            
    return texture

def apply_texture_to_shapes(base_image, texture):
    base_pixels = base_image.load()
    texture_pixels = texture.load()

    width, height = base_image.size

    # Erstellt ein neues Bild für das Ergebnis
    result_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    result_pixels = result_img.load()

    for y in range(height):
        for x in range(width):
            base_pixel = base_pixels[x, y]
            texture_pixel = texture_pixels[x, y]

            # Wenn der Alphakanal des Basisbildes nicht transparent ist
            if base_pixel[3] > 0:
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
    
    # Farben für Risse
    crack_colors = ["#1d1616", "#4c3c3c"]
    color = random.choice(crack_colors)
    
    # Berechnung des Endpunkts basierend auf Länge und goldenem Winkel
    points = [(start_x, start_y)]
    fib_lengths = fibonacci(6)
    
    current_angle = random.uniform(0, 2*math.pi)  # Startwinkel zufällig wählen
    for length in fib_lengths[2:]:
        segment_length = base_length * length / max(fib_lengths)
        end_x = start_x + segment_length * math.cos(current_angle)
        end_y = start_y + segment_length * math.sin(current_angle)
        points.append((end_x, end_y))
        
        # Update des Startpunkts für das nächste Segment und Drehen um den goldenen Winkel
        start_x, start_y = end_x, end_y
        current_angle += GOLDEN_ANGLE

    draw.line(points, fill=color, width=2)

def generate_platonic_shapes(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
def draw_platonic(draw, center, size, color, layer):
    
    choice = random.choice(["tetrahedron", "cube", "octahedron", "dodecahedron", "icosahedron"])
    
    if layer == 0:  # Heptagon für die erste Ebene
        angle = 2 * math.pi / 7
        points = [(center[0] + size * math.cos(n * angle), center[1] + size * math.sin(n * angle)) for n in range(7)]
        draw.polygon(points, fill=color)
    else:
        if choice == "tetrahedron":
            # Zeichnet ein Tetraeder
            draw.polygon([center, (center[0] + size, center[1]), (center[0] + size/2, center[1] - size)], fill=color)
        elif choice == "cube":
            # Zeichnet einen Würfel
            draw.rectangle([center, (center[0] + size, center[1] + size)], fill=color)
        elif choice == "octahedron":
            # Zeichnet ein Oktaeder
            draw.polygon([center, (center[0] + size, center[1]), (center[0] + size/2, center[1] + size)], fill=color)
            draw.polygon([center, (center[0] + size, center[1]), (center[0] + size/2, center[1] - size)], fill=color)
        elif choice == "dodecahedron":
            # Zeichnet ein Dodekaeder (vereinfachte Darstellung)
            draw.polygon([center, (center[0] + size, center[1]), (center[0] + size/2, center[1] - size)], fill=color)
            draw.polygon([center, (center[0], center[1] + size), (center[0] + size/2, center[1] + size/2)], fill=color)
        elif choice == "icosahedron":
            # Zeichnet ein Ikosaeder (vereinfachte Darstellung)
            draw.polygon([center, (center[0], center[1] + size), (center[0] + size/2, center[1] + size/2)], fill=color)
            draw.polygon([center, (center[0] + size, center[1]), (center[0] + size/2, center[1] - size/2)], fill=color)

def get_shade_of_brown(factor):
    # Basisfarben
    r_base = 90
    g_base = 70
    b_base = 61

    # Variationen zu den Basisfarben hinzufügen
    r_variation = int(r_base * factor) % 256
    g_variation = int(g_base * factor) % 256
    b_variation = int(b_base * factor) % 256

    # Farbe zusammenstellen
    color = "#{:02x}{:02x}{:02x}".format(r_variation, g_variation, b_variation)
    return color

def generate_rock_tile(width, height):
    img = Image.new('RGBA', (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    base_color = "#5a463d"
    num_layers = 9
    current_size = width / 2  # Größere Startgröße
    prev_center = (width/2, height/2)
    for layer in range(num_layers):
        dx = random.randint(20, 30) * random.choice([-1, 1])
        dy = random.randint(20, 30) * random.choice([-1, 1])
        # Farbe für diese Ebene
        factor = (0.9 ** (num_layers - layer)) + random.uniform(-0.1, 0.1)
        color = get_shade_of_brown(factor)

        center = (width/2, height/2)
        draw_platonic(draw, center, current_size, color, layer)
        
        form = [center, (current_size, current_size)]
        
        # Anzahl der Risse je nach Ebene
        num_cracks = 1
        if layer in [0, 1,5]:  # Die hintersten Ebenen
            num_cracks = random.randint(2, 4)

        for _ in range(num_cracks):
            add_crack(draw, form, current_size / 2)  # Risse nach innen
        
        # Die Größe für die nächste Ebene reduzieren
        scale_factor = random.uniform(1.4, 1.8)
        current_size /= scale_factor

    img = img.filter(ImageFilter.GaussianBlur(radius=2))

    texture = generate_perlin_texture(width, height)
    final_img = apply_texture_to_shapes(img, texture)

    return final_img

tile = generate_rock_tile(256, 256)
tile.show()
