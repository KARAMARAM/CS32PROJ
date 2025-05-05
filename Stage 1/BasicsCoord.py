import math

# Coordinates of the Kaaba in Mecca.
KAABA_LAT = 21.4225
KAABA_LON = 39.8262

def calculate_qibla_direction(lat, lon):
    """
    Calculate the Qibla direction in degrees from North for a given
    latitude and longitude.
    
    The formula uses differences in longitude and the trigonometric functions:
      angle = arctan2( sin(delta_longitude),
                       cos(user_latitude) * tan(kaaba_latitude) - sin(user_latitude)*cos(delta_longitude) )
    
    Angles are converted to/from radians as needed.
    """
    # Convert degrees to radians.
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    kaaba_lat_rad = math.radians(KAABA_LAT)
    kaaba_lon_rad = math.radians(KAABA_LON)
    
    # Compute the difference in longitude.
    delta_lon = kaaba_lon_rad - lon_rad
    # Calculate the angle using the arctan2 function.
    angle_rad = math.atan2(math.sin(delta_lon),
                           math.cos(lat_rad) * math.tan(kaaba_lat_rad) - math.sin(lat_rad) * math.cos(delta_lon))
    
    # Convert the angle from radians to degrees, normalize to [0, 360)
    angle_deg = math.degrees(angle_rad)
    qibla_direction = (angle_deg + 360) % 360
    return qibla_direction

def get_cardinal_direction(angle):
    """
    Map an angle (in degrees) to the nearest cardinal or intercardinal direction.
    """
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    # Divide the full circle into 8 segments of 45 degrees each.
    index = round(angle / 45) % 8
    return directions[index]

def display_compass(qibla_angle):
    """
    Display a simple text-based representation of a compass along with the Qibla direction.
    """
    cardinal = get_cardinal_direction(qibla_angle)
    
    # Choose an arrow symbol according to the cardinal direction.
    arrows = {
        "N": "↑",
        "NE": "↗",
        "E": "→",
        "SE": "↘",
        "S": "↓",
        "SW": "↙",
        "W": "←",
        "NW": "↖"
    }
    arrow_symbol = arrows.get(cardinal, "?")
    
    # Basic compass display.
    print("\nCompass View:")
    print("      N")
    print("      |")
    print("W ----+---- E")
    print("      |")
    print("      S")
    print(f"\n Your Qibla direction is approximately: {qibla_angle:.2f}° from North")
    print(f"That is closest to: {cardinal} {arrow_symbol}\n")

def main():
    """
    Main function that prompts the user for latitude and longitude,
    calculates the Qibla direction, and displays it.
    """
    try:
        lat = float(input("Enter your latitude (in decimal degrees): "))
        lon = float(input("Enter your longitude (in decimal degrees): "))
    except ValueError:
        print("Invalid input. Please enter numerical values for coordinates.")
        return

    # Calculate Qibla direction.
    qibla_angle = calculate_qibla_direction(lat, lon)
    # Show the result in a text-based "compass" view.
    display_compass(qibla_angle)

if __name__ == '__main__':
    main()
