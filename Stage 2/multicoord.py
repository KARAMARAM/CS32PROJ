import math

# Preset destinations (name -> (lat, lon))
PRESETS = {
    "mecca": (21.4225, 39.8262),
    "jerusalem": (31.7683, 35.2137),
    # add more as you like
}

def calculate_bearing(lat, lon, dest_lat, dest_lon):
    """
    Calculate the bearing in degrees from North from (lat, lon) to (dest_lat, dest_lon).
    """
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    dest_lat_rad = math.radians(dest_lat)
    dest_lon_rad = math.radians(dest_lon)

    delta_lon = dest_lon_rad - lon_rad
    x = math.sin(delta_lon) * math.cos(dest_lat_rad)
    y = math.cos(lat_rad) * math.sin(dest_lat_rad) - math.sin(lat_rad) * math.cos(dest_lat_rad) * math.cos(delta_lon)
    bearing_rad = math.atan2(x, y)
    bearing_deg = (math.degrees(bearing_rad) + 360) % 360
    return bearing_deg

def get_cardinal_direction(angle):
    """
    Map an angle (in degrees) to the nearest cardinal or intercardinal direction.
    """
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = round(angle / 45) % 8
    return directions[idx]

def display_compass(angle):
    """
    Display a simple text-based compass showing the bearing arrow.
    """
    cardinal = get_cardinal_direction(angle)
    arrows = {
        "N": "↑", "NE": "↗", "E": "→", "SE": "↘",
        "S": "↓", "SW": "↙", "W": "←", "NW": "↖"
    }
    arrow_sym = arrows[cardinal]

    print("\n   Compass:")
    print("       N")
    print("       |")
    print("   W --+-- E")
    print("       |")
    print("       S")
    print(f"\nBearing: {angle:.2f}° from North")
    print(f"Closest cardinal: {cardinal} {arrow_sym}\n")

def choose_destination():
    """
    Let the user pick a preset or enter custom coordinates.
    Returns (dest_lat, dest_lon).
    """
    print("Choose a destination:")
    for i, name in enumerate(PRESETS, 1):
        print(f"  {i}. {name.title()}")
    print(f"  {len(PRESETS)+1}. Enter custom coordinates")

    choice = input(f"Select 1–{len(PRESETS)+1}: ").strip()
    try:
        idx = int(choice)
        if 1 <= idx <= len(PRESETS):
            key = list(PRESETS.keys())[idx-1]
            return PRESETS[key]
        elif idx == len(PRESETS) + 1:
            lat = float(input("Enter target latitude  (decimal °): "))
            lon = float(input("Enter target longitude (decimal °): "))
            return lat, lon
    except (ValueError, IndexError):
        pass

    print("Invalid choice, please try again.")
    return choose_destination()

def main():
    try:
        lat = float(input("Enter your latitude  (decimal °): "))
        lon = float(input("Enter your longitude (decimal °): "))
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return

    dest_lat, dest_lon = choose_destination()
    bearing = calculate_bearing(lat, lon, dest_lat, dest_lon)
    display_compass(bearing)

if __name__ == "__main__":
    main()
