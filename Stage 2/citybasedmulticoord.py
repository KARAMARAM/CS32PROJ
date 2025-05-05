import math
import csv
import os

# —————— Load your city dataset ——————
CITY_COORDS = {}
CSV_PATH = "data/worldcities.csv"  # path to your uploaded file

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"Could not find {CSV_PATH}; make sure it's uploaded.")

with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        city = row['city'].strip().lower()
        country = row.get('country', '').strip().lower()
        lat, lon = float(row['lat']), float(row['lng'])
        # key by "city, country"
        if country:
            CITY_COORDS[f"{city}, {country}"] = (lat, lon)
        # also key by city alone if unique
        if city not in CITY_COORDS:
            CITY_COORDS[city] = (lat, lon)

# —————— Bearing logic (unchanged) ——————

def calculate_bearing(lat, lon, dest_lat, dest_lon):
    lat_rad, lon_rad = math.radians(lat), math.radians(lon)
    dlat_rad, dlon_rad = math.radians(dest_lat), math.radians(dest_lon)
    delta_lon = dlon_rad - lon_rad
    x = math.sin(delta_lon) * math.cos(dlat_rad)
    y = (math.cos(lat_rad)*math.sin(dlat_rad)
         - math.sin(lat_rad)*math.cos(dlat_rad)*math.cos(delta_lon))
    bearing = math.degrees(math.atan2(x, y))
    return (bearing + 360) % 360

def get_cardinal_direction(angle):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return directions[round(angle/45) % 8]

def display_compass(angle):
    cardinal = get_cardinal_direction(angle)
    arrows = {
        "N":"↑","NE":"↗","E":"→","SE":"↘",
        "S":"↓","SW":"↙","W":"←","NW":"↖"
    }
    arrow = arrows[cardinal]
    print("\n   Compass:")
    print("       N\n       |   \n   W --+-- E\n       |   \n       S")
    print(f"\nBearing: {angle:.2f}° from North — {cardinal} {arrow}\n")

# —————— Prompting for a location ——————

def ask_for_location(prompt):
    """
    1) Ask for City or City, Country.
    2) If in CITY_COORDS, return its coords.
    3) Otherwise, fall back to manual lat/lon.
    """
    name = input(f"{prompt} (e.g. \"Yerevan\" or \"Paris, France\"): ").strip()
    key = name.lower()
    if key in CITY_COORDS:
        lat, lon = CITY_COORDS[key]
        print(f"→ Found {name.title()}: ({lat:.5f}, {lon:.5f})")
        return lat, lon
    else:
        print(f" “{name}” not found in city list.")
        while True:
            try:
                lat = float(input("Enter latitude  (decimal °): "))
                lon = float(input("Enter longitude (decimal °): "))
                return lat, lon
            except ValueError:
                print("Invalid numbers, please try again.")

# —————— Main flow ——————

def main():
    print("Where are you now?")
    orig_lat, orig_lon = ask_for_location("Your city")

    print("\nWhere do you want to go?")
    dest_lat, dest_lon = ask_for_location("Destination city")

    bearing = calculate_bearing(orig_lat, orig_lon, dest_lat, dest_lon)
    display_compass(bearing)

if __name__ == "__main__":
    main()
