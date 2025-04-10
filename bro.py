import math
# [Optional: import additional modules, e.g., tkinter for GUI display]

# Global constant for the Kaaba location in Mecca.
KAABA_LAT = 21.4225
KAABA_LON = 39.8262

def calculate_qibla_direction(user_lat, user_lon):
    """
    Calculate the Qibla direction (in degrees from North) given the user's latitude and longitude.
    
    [TODO: Convert the user and Kaaba coordinates to radians]
    [TODO: Compute the difference in longitude between the Kaaba and the user]
    [TODO: Apply the trigonometric formula using math.atan2]
    [TODO: Convert the resulting angle from radians to degrees and normalize it to a 0-360 range]
    """
    # Convert degrees to radians
    user_lat_rad = math.radians(user_lat)
    user_lon_rad = math.radians(user_lon)
    kaaba_lat_rad = math.radians(KAABA_LAT)
    kaaba_lon_rad = math.radians(KAABA_LON)
    
    # Calculate the difference in longitude
    delta_lon = kaaba_lon_rad - user_lon_rad
    
    # Compute the angle using the formula
    # [Note: This formula may need adjustments based on proper Qibla calculation methods]
    angle_rad = math.atan2(math.sin(delta_lon),
                           math.cos(user_lat_rad) * math.tan(kaaba_lat_rad) - math.sin(user_lat_rad) * math.cos(delta_lon))
    
    # Convert back to degrees and normalize the angle to the range [0, 360)
    qibla_direction = (math.degrees(angle_rad) + 360) % 360
    
    return qibla_direction

def display_compass(qibla_direction):
    """
    Display the Qibla direction on a compass.
    
    [TODO: Choose between a text-based output or a GUI representation]
    [If using a GUI]:
        - Initialize the window (e.g., with tkinter)
        - Draw a circle representing the compass
        - Place an arrow rotated by qibla_direction degrees (adjust for coordinate system)
    [If using text]:
        - Print a simple compass diagram and annotate the Qibla direction
    """
    # Example: Basic text-based display:
    print("\nCompass:")
    print("    N")
    print("    |")
    print("W --+-- E")
    print("    |")
    print("    S")
    print("\nQibla direction: {:.2f}° from North".format(qibla_direction))
    
    # [TODO: Add additional details or a graphical representation if desired]

def main():
    """
    Main entry point: prompt the user for coordinates, compute the Qibla direction, and display it.
    
    [TODO: Handle potential input errors with try/except]
    [TODO: Optionally, consider validating the coordinate range values]
    """
    # [Placeholder: Get user input; you can implement error handling as needed]
    user_lat = float(input("Enter your latitude (decimal degrees): "))  # [Input validation could be added]
    user_lon = float(input("Enter your longitude (decimal degrees): "))  # [Input validation could be added]
    
    # Calculate the Qibla direction using the provided user coordinates.
    qibla_direction = calculate_qibla_direction(user_lat, user_lon)
    
    # Display the computed Qibla direction.
    display_compass(qibla_direction)

if __name__ == '__main__':
    main()
