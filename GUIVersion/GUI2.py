import math
import tkinter as tk
from tkinter import ttk, messagebox

# Preset destinations (name -> (lat, lon))
PRESETS = {
    "Mecca": (21.4225, 39.8262),
    "Jerusalem": (31.7683, 35.2137),
}

def calculate_bearing(lat, lon, dest_lat, dest_lon):
    lat_r = math.radians(lat)
    lon_r = math.radians(lon)
    dst_lat_r = math.radians(dest_lat)
    dst_lon_r = math.radians(dest_lon)

    dlon = dst_lon_r - lon_r
    x = math.sin(dlon) * math.cos(dst_lat_r)
    y = (math.cos(lat_r) * math.sin(dst_lat_r) -
         math.sin(lat_r) * math.cos(dst_lat_r) * math.cos(dlon))
    return (math.degrees(math.atan2(x, y)) + 360) % 360

class CompassApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rotating Compass")
        self.minsize(300, 450)

        # === Canvas ===
        self.size = 300
        self.radius = self.size // 2 - 20
        self.cx = self.cy = self.size // 2

        self.canvas = tk.Canvas(self, width=self.size, height=self.size, bg="white")
        self.canvas.pack(padx=10, pady=10)

        self._draw_background()
        self.arrow_handle = None
        self._draw_arrow(0)

        # === Controls Frame ===
        controls = tk.Frame(self)
        controls.pack(pady=10, fill="x")

        # Latitude
        tk.Label(controls, text="Latitude:", width=12, anchor="e")\
            .pack(side="left", padx=(0,5))
        self.lat_entry = tk.Entry(controls)
        self.lat_entry.pack(side="left", expand=True, fill="x")

        # Longitude
        tk.Label(controls, text="Longitude:", width=12, anchor="e")\
            .pack(side="left", padx=(15,5))
        self.lon_entry = tk.Entry(controls)
        self.lon_entry.pack(side="left", expand=True, fill="x")

        # Destination dropdown
        dest_frame = tk.Frame(self)
        dest_frame.pack(pady=(5,10), fill="x")
        tk.Label(dest_frame, text="Destination:", width=12, anchor="e")\
            .pack(side="left", padx=(0,5))
        self.dest_var = tk.StringVar(value="Mecca")
        ttk.Combobox(dest_frame, textvariable=self.dest_var,
                     values=list(PRESETS.keys()),
                     state="readonly")\
            .pack(side="left", expand=True, fill="x")

        # Button
        tk.Button(self, text="Point Compass", command=self._on_click)\
            .pack(pady=10)

    def _draw_background(self):
        # big circle
        self.canvas.create_oval(
            self.cx - self.radius, self.cy - self.radius,
            self.cx + self.radius, self.cy + self.radius
        )
        # N/E/S/W
        for dx, dy, lbl in [(0,-self.radius,"N"), (self.radius,0,"E"),
                            (0,self.radius,"S"), (-self.radius,0,"W")]:
            self.canvas.create_text(self.cx+dx, self.cy+dy,
                                    text=lbl, font=("Arial",12,"bold"))
        # ticks
        for angle in range(0, 360, 30):
            r = math.radians(angle)
            x1 = self.cx + (self.radius-5) * math.sin(r)
            y1 = self.cy - (self.radius-5) * math.cos(r)
            x2 = self.cx + self.radius * math.sin(r)
            y2 = self.cy - self.radius * math.cos(r)
            self.canvas.create_line(x1, y1, x2, y2)

    def _draw_arrow(self, angle_deg):
        if self.arrow_handle:
            self.canvas.delete(self.arrow_handle)
        r = math.radians(angle_deg)
        x2 = self.cx + (self.radius-10)*math.sin(r)
        y2 = self.cy - (self.radius-10)*math.cos(r)
        self.arrow_handle = self.canvas.create_line(
            self.cx, self.cy, x2, y2,
            arrow=tk.LAST, width=3
        )

    def _on_click(self):
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
        except ValueError:
            return messagebox.showerror(
                "Invalid input",
                "Please enter valid decimal numbers for latitude and longitude."
            )
        dst = self.dest_var.get()
        bearing = calculate_bearing(lat, lon, *PRESETS[dst])
        self._draw_arrow(bearing)
        self.title(f"Compass → {dst} ({bearing:.1f}°)")

if __name__ == "__main__":
    CompassApp().mainloop()
