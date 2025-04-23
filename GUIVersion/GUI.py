import math
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Preset destinations
PRESETS = {
    "Mecca": (21.4225, 39.8262),
    "Jerusalem": (31.7683, 35.2137),
    # add more here...
}

def calculate_bearing(lat, lon, dest_lat, dest_lon):
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    dest_lat_rad = math.radians(dest_lat)
    dest_lon_rad = math.radians(dest_lon)

    delta_lon = dest_lon_rad - lon_rad
    x = math.sin(delta_lon) * math.cos(dest_lat_rad)
    y = math.cos(lat_rad) * math.sin(dest_lat_rad) - \
        math.sin(lat_rad) * math.cos(dest_lat_rad) * math.cos(delta_lon)
    bearing = (math.degrees(math.atan2(x, y)) + 360) % 360
    return bearing

class CompassApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rotating Compass")
        self.resizable(False, False)

        # build an absolute path to the GUIVersion folder
        script_dir = os.path.dirname(os.path.realpath(__file__))
        img_dir = os.path.join(script_dir, "GUIVersion")

        # Load images
        self.base_img  = Image.open(os.path.join(img_dir, "compass.png"))
        self.arrow_img = Image.open(os.path.join(img_dir, "arrow.png"))
        size = self.base_img.size

        # Canvas to hold both
        self.canvas = tk.Canvas(self, width=size[0], height=size[1])
        self.canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.base_tk = ImageTk.PhotoImage(self.base_img)
        self.canvas.create_image(size[0]//2, size[1]//2, image=self.base_tk)

        # Arrow canvas image handle (will update with rotate)
        self.arrow_handle = None
        self.draw_arrow(0)

        # User input fields
        tk.Label(self, text="Your Latitude:").grid(row=1, column=0, sticky="e")
        self.lat_entry = tk.Entry(self); self.lat_entry.grid(row=1, column=1)
        tk.Label(self, text="Your Longitude:").grid(row=2, column=0, sticky="e")
        self.lon_entry = tk.Entry(self); self.lon_entry.grid(row=2, column=1)

        # Destination dropdown
        tk.Label(self, text="Destination:").grid(row=3, column=0, sticky="e")
        self.dest_var = tk.StringVar(value="Mecca")
        self.dest_menu = ttk.Combobox(self, textvariable=self.dest_var,
                                      values=list(PRESETS.keys()),
                                      state="readonly")
        self.dest_menu.grid(row=3, column=1)

        # Calculate button
        calc_btn = tk.Button(self, text="Point Compass", command=self.update_compass)
        calc_btn.grid(row=4, column=0, columnspan=3, pady=10)

    def draw_arrow(self, angle):
        """Rotate the arrow image by `angle` and draw it."""
        rotated = self.arrow_img.rotate(angle, resample=Image.BICUBIC, expand=True)
        self.arrow_tk = ImageTk.PhotoImage(rotated)
        # Remove old arrow if exists
        if self.arrow_handle:
            self.canvas.delete(self.arrow_handle)
        # Center it
        w, h = rotated.size
        cx, cy = self.base_img.size[0]//2, self.base_img.size[1]//2
        self.arrow_handle = self.canvas.create_image(cx, cy, image=self.arrow_tk)

    def update_compass(self):
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
        except ValueError:
            return messagebox.showerror("Invalid input", "Enter valid numbers for lat/lon.")

        dest_name = self.dest_var.get()
        dest_lat, dest_lon = PRESETS[dest_name]
        bearing = calculate_bearing(lat, lon, dest_lat, dest_lon)

        # In PIL, positive rotation is counter-clockwise, so negate
        self.draw_arrow(-bearing)
        self.title(f"Compass → {dest_name} ({bearing:.1f}°)")

if __name__ == "__main__":
    app = CompassApp()
    app.mainloop()
 