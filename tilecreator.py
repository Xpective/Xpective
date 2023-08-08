from PIL import Image, ImageDraw, ImageFilter
import random

def generate_rock_tile(width, height):
    # Erstellen Sie ein neues Bild mit den angegebenen Abmessungen
    img = Image.new('RGB', (width, height), color="#3b2f2f")
    draw = ImageDraw.Draw(img)
    
    # Bestimmen Sie die Anzahl und Größe der Felsen
    for _ in range(random.randint(3, 7)):
        rock_width = random.randint(10, width // 3)
        rock_height = random.randint(10, height // 3)
        
        # Bestimmen Sie die Position des Felsens
        x = random.randint(0, width - rock_width)
        y = random.randint(0, height - rock_height)
        
        # Wählen Sie zufällig zwischen verschiedenen Felsformen
        shape_type = random.choice(['ellipse', 'rectangle'])
        
        if shape_type == 'ellipse':
            draw.ellipse((x, y, x + rock_width, y + rock_height), fill="#5a463d")
        elif shape_type == 'rectangle':
            draw.rectangle((x, y, x + rock_width, y + rock_height), fill="#5a463d")
        
        # Füge kleinere Details wie Risse oder kleinere Steine hinzu
        for _ in range(random.randint(2, 5)):
            small_rock_x = random.randint(x, x + rock_width - 5)
            small_rock_y = random.randint(y, y + rock_height - 5)
            draw.ellipse((small_rock_x, small_rock_y, small_rock_x + 5, small_rock_y + 5), fill="#3b2f2f")
        
    # Füge Schattierungen hinzu, um den Felsen Tiefe zu verleihen
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    draw = ImageDraw.Draw(img)
    for _ in range(random.randint(3, 7)):
        shadow_x = random.randint(0, width - 20)
        shadow_y = random.randint(0, height - 20)
        draw.ellipse((shadow_x, shadow_y, shadow_x + 20, shadow_y + 20), fill="#2c2c2c")
    
    return img

# Generieren Sie eine Rock-Tile
tile = generate_rock_tile(64, 64)
tile.show()
