import math
import csv
import os
import matplotlib.pyplot as plt

# —————— Load city → (lat, lon) lookup ——————
CITY_COORDS = {}
CSV_PATH = "data/worldcities.csv"

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"Could not find {CSV_PATH}")

with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        city  = row['city'].strip().lower()
        country = row.get('country', '').strip().lower()
        lat, lon = float(row['lat']), float(row['lng'])
        # key by "city, country"
        if country:
            CITY_COORDS[f"{city}, {country}"] = (lat, lon)
        # also allow bare city if not overridden
        if city not in CITY_COORDS:
            CITY_COORDS[city] = (lat, lon)

# —————— Bearing & plotting funcs ——————

def calculate_bearing(lat, lon, dest_lat, dest_lon):
    lat_rad      = math.radians(lat)
    dest_lat_rad = math.radians(dest_lat)
    delta_lon    = math.radians(dest_lon - lon)
    x = math.sin(delta_lon) * math.cos(dest_lat_rad)
    y = (math.cos(lat_rad)*math.sin(dest_lat_rad)
         - math.sin(lat_rad)*math.cos(dest_lat_rad)*math.cos(delta_lon))
    θ = math.atan2(x, y)
    return (math.degrees(θ) + 360) % 360

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in kilometers

    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    Δφ = math.radians(lat2 - lat1)
    Δλ = math.radians(lon2 - lon1)

    a = math.sin(Δφ / 2)**2 + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance  # distance in kilometers


def plot_compass(bearing_deg):
    fig, ax = plt.subplots(figsize=(5,5), subplot_kw={'projection':'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_xticks([])
    ax.set_yticks([])

    # tick marks every 30°
    for angle in range(0, 360, 30):
        θ = math.radians(angle)
        ax.plot([θ, θ], [0.9, 1.0], linewidth=2)

    # cardinal labels
    for angle, label in zip([0,90,180,270], ["N","E","S","W"]):
        ax.text(math.radians(angle), 1.08, label,
                ha='center', va='center', fontsize=16, fontweight='bold')

    # draw the arrow
    ax.arrow(math.radians(bearing_deg), 0,
             0, 0.8,
             width=0.02, length_includes_head=True)

    ax.set_ylim(0, 1.2)
    ax.set_title(f"Bearing: {bearing_deg:.2f}° from North", va='bottom')
    plt.show()


def validate_coordinates(lat, lon):
    if not (-90 <= lat <= 90):
        raise ValueError(f"Latitude {lat} out of bounds (must be between -90 and 90)")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Longitude {lon} out of bounds (must be between -180 and 180)")



def ask_for_location(prompt):
    """
    Prompt for "City" or "City, Country".
    If in CITY_COORDS, return that.
    Else, fall back to manual entry.
    """
    name = input(f"{prompt} (e.g. \"Yerevan\" or \"Paris, France\"): ").strip()
    key = name.lower()
    if key in CITY_COORDS:
        lat, lon = CITY_COORDS[key]
        print(f"→ Found {name.title()}: ({lat:.5f}, {lon:.5f})")
        validate_coordinates(lat, lon)
        return lat, lon

    print(f"✗ “{name}” not found. Please enter coordinates manually.")
    while True:
        try:
            lat = float(input("  latitude  (decimal °): "))
            lon = float(input("  longitude (decimal °): "))
            validate_coordinates(lat, lon)
            return lat, lon
        except ValueError:
            print("  Invalid numbers, try again.")

# —————— Main flow ——————

def main():
    print("Where are you now?")
    orig_lat, orig_lon = ask_for_location("Your city")

    print("\nWhere do you want to go?")
    dest_lat, dest_lon = ask_for_location("Destination city")

    distance = haversine_distance(orig_lat, orig_lon, dest_lat, dest_lon)
    print(f"Distance: {distance:.2f} km")

    bearing = calculate_bearing(orig_lat, orig_lon, dest_lat, dest_lon)
    plot_compass(bearing)

    


if __name__ == "__main__":
    main()
