import numpy as np
from scipy.spatial import Delaunay
from PIL import Image, ImageDraw, ImageTk, ImageFilter
import math
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, colorchooser


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        
class RockGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Generator")

        self.scroll_frame = ScrollableFrame(root)
        self.scroll_frame.pack(fill="both", expand=True)

        self.frame = self.scroll_frame.scrollable_frame

        self.colors = {
            "background": "#FFFFFF",
            "rock1": "#B8B8B8",
            "rock2": "#A0A0A0",
            "rock3": "#888888",
            "rock4": "#707070",
            "rock5": "#585858",
        }

        self.rock_img = None
        self.rock_img_display = None

        
        self.triangle_size = tk.DoubleVar(value=20)  # Default value is 20
        self.shadow_angle = tk.DoubleVar(value=45)  # Default value is 45 degrees
        self.setup_gui()

    def setup_gui(self):
        # Color selectors
        for idx, (color_key, color_val) in enumerate(self.colors.items()):
            lbl = ttk.Label(self.frame, text=f"{color_key} color:")
            lbl.grid(row=idx, column=0, sticky="w", padx=10, pady=5)

            btn = ttk.Button(self.frame, text=f"Set {color_key} color", command=lambda key=color_key: self.change_color(key))
            btn.grid(row=idx, column=1, padx=10, pady=5)

            color_display = tk.Canvas(self.frame, width=50, height=20, bg=color_val)
            color_display.grid(row=idx, column=2, padx=10, pady=5)

        # Rock Image Display
        self.rock_img_display = tk.Label(self.frame)
        self.rock_img_display.grid(row=idx + 1, column=0, columnspan=3, padx=10, pady=10)

        # Generate Button
        gen_btn = ttk.Button(self.frame, text="Generate Rock", command=self.generate_rock)
        gen_btn.grid(row=idx + 2, column=0, columnspan=3, padx=10, pady=10)

    def change_color(self, color_key):
        color_code = colorchooser.askcolor(title=f"Choose a color for {color_key}")[1]
        if color_code:
            self.colors[color_key] = color_code
            self.generate_rock()

    def generate_rock(self):
        img = self.generate_clustered_rock_tile()
        
        # Apply shadow effects (Placeholder; needs further integration)
        triangles = generate_shadow_triangles(img.width, img.height, self.triangle_size.get())
        gradient = generate_shadow_gradient(img.width, img.height, self.shadow_angle.get())
        self.display_image(img)

    def display_image(self, img):
        img = img.resize((400, 400), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.rock_img_display.config(image=photo)
        self.rock_img_display.image = photo

    def generate_clustered_rock_tile(self):
        # Constants
        phi = (1 + np.sqrt(5)) / 2  # Golden ratio

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

        # Create an image using the triangulation
        img = Image.new("RGB", (800, 800), self.colors["background"])
        draw = ImageDraw.Draw(img)

        for triangle in triang.triangles:
            color_key = f"rock{np.random.randint(1, 6)}"
            draw.polygon([(triang.x[i] * 800, triang.y[i] * 800) for i in triangle], fill=self.colors[color_key])

        return img

# Create the main application window
root = tk.Tk()
root.geometry("500x700")
app = RockGeneratorGUI(root)
root.mainloop()
def generate_clustered_rock_tile(sides=10, distortion=0.0, noise=0.0, scale=1.0, shadow_angle=45, shadow_offset=10, colors=None):
    img = Image.new("RGBA", (800, 800), (255, 255, 255, 0))
    shadow_img = Image.new("RGBA", (800, 800), (255, 255, 255, 0))
    
    draw = ImageDraw.Draw(img)

    cluster_center = (400, 400)
    cluster_points = []
    for i in range(sides):
        angle = 2 * math.pi * i / sides
        distance = 300 * scale + distortion * 100 * math.sin(3 * angle)
        x = cluster_center[0] + distance * math.cos(angle) + np.random.uniform(-noise, noise)
        y = cluster_center[1] + distance * math.sin(angle) + np.random.uniform(-noise, noise)
        cluster_points.append((x, y))

    draw.polygon(cluster_points, fill=colors["black"])
    
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

    shadow = generate_shadow_offset_image(img, shadow_angle, shadow_offset)
    img.paste(shadow, (0, 0), shadow)

    return img

def generate_shadow_offset_image(img, angle, offset):
    angle_rad = math.radians(360 - angle)
    dx = offset * math.cos(angle_rad)
    dy = offset * math.sin(angle_rad)

    img = img.convert("L")
    img = img.point(lambda p: p * 0.7)
    img = img.filter(ImageFilter.GaussianBlur(3))
    
    # Ersetzen Sie die `.offset()` Methode durch `.crop()` und `.paste()`
    width, height = img.size
    img_cropped = img.crop((dx, dy, width, height))
    img.paste(img_cropped, (0, 0))

    return img

class RockGeneratorApp(tk.Tk):
    RESOLUTIONS = {
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "2K": (2560, 1440),
        "4K": (3840, 2160),
        "Custom": None
    }
    colors = {
        "black": "#000000",
        "dark_gray": "#2c2c2c",
        "dark_brown": "#3b2f2f",
        "contour_brown": "#2a1d1d",
        "contour_gray": "#1d1d1d",
        "shadow": "#000000"
    }

    def __init__(self):
        super().__init__()

        self.title("Rock Generator")
        self.geometry("1000x900")

        self.create_slider("Sides", "sides", 3, 20, 10)
        self.create_slider("Distortion", "distortion", 0, 1, 0.5, resolution=0.01)
        self.create_slider("Noise", "noise", 0, 50, 20)
        self.create_slider("Scale", "scale", 0.5, 1.5, 1.0, resolution=0.01)
        self.create_slider("Shadow Angle", "shadow_angle", 0, 360, 45)
        self.create_slider("Shadow Offset", "shadow_offset", 0, 50, 10)
        self.create_resolution_dropdown()
        self.create_color_buttons()
        
        self.generate_btn = ttk.Button(self, text="Generate Rock", command=self.generate_rock)
        self.generate_btn.pack(pady=20)

        self.save_btn = ttk.Button(self, text="Save As", command=self.save_image)
        self.save_btn.pack(pady=20)

        self.canvas = tk.Canvas(self, bg="white", width=800, height=800)
        self.canvas.pack(pady=20)

    def create_slider(self, label_text, attribute_name, min_val, max_val, default_val, resolution=1):
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        label = ttk.Label(frame, text=label_text)
        label.grid(row=0, column=0)

        slider = ttk.Scale(frame, from_=min_val, to=max_val, value=default_val, orient=tk.HORIZONTAL, length=250)
        slider.grid(row=0, column=1)
        slider.set(default_val)
        slider.bind("<Motion>", self.update_slider_value_label)
        slider.value_label = ttk.Label(frame, text=str(default_val))
        slider.value_label.grid(row=0, column=2)

        setattr(self, attribute_name, slider)

    def update_slider_value_label(self, event):
        slider = event.widget
        slider.value_label.config(text=str(round(float(slider.get()), 2)))

    def create_resolution_dropdown(self):
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        label = ttk.Label(frame, text="Resolution")
        label.grid(row=0, column=0)

        self.resolution_var = tk.StringVar()
        self.resolution_var.set("1080p")

        dropdown = ttk.Combobox(frame, textvariable=self.resolution_var)
        dropdown['values'] = list(self.RESOLUTIONS.keys())
        dropdown.grid(row=0, column=1)

    def generate_rock(self):
        width, height = self.RESOLUTIONS[self.resolution_var.get()]
        if width is None or height is None:
            width = simpledialog.askinteger("Custom Width", "Enter the width:")
            height = simpledialog.askinteger("Custom Height", "Enter the height:")
        
        img = generate_clustered_rock_tile(
            int(self.sides.get()), 
            self.distortion.get(), 
            self.noise.get(), 
            self.scale.get(), 
            self.shadow_angle.get(), 
            self.shadow_offset.get(), 
            self.colors
        )
        self.generated_img = img
        self.photo = ImageTk.PhotoImage(img.resize((800, 800)))
        self.canvas.create_image(400, 400, image=self.photo)
        
    def change_color(self, color_key):
        new_color = colorchooser.askcolor(title=f"Choose a color for {color_key}")[1]
        if new_color:
            self.colors[color_key] = new_color
            self.generate_rock()

    def create_color_buttons(self):
        """Create buttons to change colors."""
        frame = ttk.Frame(self)
        frame.pack(pady=10)
        for color_key in self.colors.keys():
            btn = ttk.Button(frame, text=f"Set {color_key} color", command=lambda key=color_key: self.change_color(key))
            btn.pack(side=tk.LEFT)

    def save_image(self):
        if hasattr(self, "generated_img"):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("PSD files", "*.psd"), ("All files", "*.*")])
            if file_path:
                if file_path.endswith(".psd"):
                    self.generated_img.save(file_path, "PSD")
                else:
                    self.generated_img.save(file_path, "PNG")

if __name__ == "__main__":
    app = RockGeneratorApp()
    app.mainloop()


def generate_shadow_triangles(width, height, triangle_size=20):
    """
    Generate shadow based on triangulation.
    
    Parameters:
    - width: Width of the image
    - height: Height of the image
    - triangle_size: Size of triangles for the triangulation
    
    Returns:
    - List of triangle coordinates
    """
    triangles = []
    
    # Create a grid of points
    x_points = np.arange(0, width, triangle_size)
    y_points = np.arange(0, height, triangle_size)
    
    for x in x_points:
        for y in y_points:
            # Create triangles based on the grid points
            p1 = (x, y)
            p2 = (x + triangle_size, y)
            p3 = (x + triangle_size, y + triangle_size)
            p4 = (x, y + triangle_size)
            
            # Split the square into two triangles
            triangles.append([p1, p2, p3])
            triangles.append([p1, p3, p4])
            
    return triangles


def generate_shadow_gradient(width, height, angle):
    """
    Generate a shadow gradient image based on the given angle.
    
    Parameters:
    - width: Width of the image
    - height: Height of the image
    - angle: Angle for the shadow gradient
    
    Returns:
    - An Image object with the shadow gradient
    """
    # Create a new image with transparent background
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate the start and end points of the gradient based on the angle
    x_start = width / 2 + math.cos(math.radians(angle)) * width
    y_start = height / 2 + math.sin(math.radians(angle)) * height
    x_end = width / 2 - math.cos(math.radians(angle)) * width
    y_end = height / 2 - math.sin(math.radians(angle)) * height
    
    # Draw the gradient
    for i in np.linspace(0, 1, width):
        color = (0, 0, 0, int(255 * i))
        draw.line([(x_start, y_start), (x_end, y_end)], fill=color, width=1)
        x_start -= math.cos(math.radians(angle))
        y_start -= math.sin(math.radians(angle))
        x_end -= math.cos(math.radians(angle))
        y_end -= math.sin(math.radians(angle))
    
    return img
