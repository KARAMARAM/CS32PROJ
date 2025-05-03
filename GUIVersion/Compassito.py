# if you’re on macOS / Linux

import math
import matplotlib.pyplot as plt

# Preset destinations (name -> (lat, lon))
PRESETS = {
    "Mecca":      (21.4225, 39.8262),
    "Jerusalem":  (31.7683, 35.2137),
    # add more as you like
}

def calculate_bearing(lat, lon, dest_lat, dest_lon):
    lat_rad      = math.radians(lat)
    dest_lat_rad = math.radians(dest_lat)
    delta_lon    = math.radians(dest_lon - lon)

    x = math.sin(delta_lon) * math.cos(dest_lat_rad)
    y = (math.cos(lat_rad) * math.sin(dest_lat_rad)
         - math.sin(lat_rad) * math.cos(dest_lat_rad) * math.cos(delta_lon))
    θ = math.atan2(x, y)
    return (math.degrees(θ) + 360) % 360

def choose_destination():
    print("Choose a destination:")
    for i, name in enumerate(PRESETS, 1):
        print(f"  {i}. {name}")
    print(f"  {len(PRESETS)+1}. Enter custom coordinates")
    choice = input(f"Select 1–{len(PRESETS)+1}: ").strip()

    try:
        idx = int(choice)
        if 1 <= idx <= len(PRESETS):
            key = list(PRESETS.keys())[idx-1]
            return PRESETS[key]
        elif idx == len(PRESETS)+1:
            lat = float(input("Enter target latitude  (decimal °): "))
            lon = float(input("Enter target longitude (decimal °): "))
            return lat, lon
    except (ValueError, IndexError):
        pass

    print("Invalid choice, try again.")
    return choose_destination()

def plot_compass(bearing_deg):
    """
    Draw a compass rose and an arrow pointing at bearing_deg from North.
    """
    fig, ax = plt.subplots(figsize=(5,5), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')    # zero at North
    ax.set_theta_direction(-1)         # clockwise positive

    # remove default grid/labels
    ax.set_xticks([])
    ax.set_yticks([])

    # draw tick marks every 30°
    for angle in range(0, 360, 30):
        θ = math.radians(angle)
        ax.plot([θ, θ], [0.9, 1.0], linewidth=2)

    # cardinal labels
    for angle, label in zip([0, 90, 180, 270], ["N", "E", "S", "W"]):
        ax.text(math.radians(angle), 1.08, label,
                ha='center', va='center', fontsize=16, fontweight='bold')

    # draw the bearing arrow
    ax.arrow(math.radians(bearing_deg), 0,
             0, 0.8,
             width=0.02,
             length_includes_head=True)

    ax.set_ylim(0, 1.2)
    ax.set_title(f"Bearing: {bearing_deg:.2f}° from North", va='bottom')
    plt.show()

def main():
    try:
        lat = float(input("Enter your latitude  (decimal °): "))
        lon = float(input("Enter your longitude (decimal °): "))
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return

    dest_lat, dest_lon = choose_destination()
    bearing = calculate_bearing(lat, lon, dest_lat, dest_lon)
    plot_compass(bearing)

if __name__ == "__main__":
    main()
