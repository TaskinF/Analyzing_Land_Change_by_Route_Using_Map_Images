from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd

def get_coordinates(address):
    geolocator = Nominatim(user_agent="taskin")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None

def generate_route_coordinates(start_address, end_address, interval_distance):
    start_coords = get_coordinates(start_address)
    end_coords = get_coordinates(end_address)

    if start_coords and end_coords:
        route = []
        distance = geodesic(start_coords, end_coords).kilometers
        num_intervals = int(distance / interval_distance)

        for i in range(num_intervals + 1):
            fraction = i / num_intervals
            coord = (
                start_coords[0] + fraction * (end_coords[0] - start_coords[0]),
                start_coords[1] + fraction * (end_coords[1] - start_coords[1]),
            )
            route.append(coord)

        return route
    else:
        return None

# Create a route between two points at regular intervals
start_point = "Harrisonburg, Virginia, USA"
end_point = "Appalachian Mountains, USA" # Blue Ridge Dağları
interval_distance_km = 0.5

route_coordinates = generate_route_coordinates(start_point, end_point, interval_distance_km)
if route_coordinates:
    data = {
        'Step': [f"Step {idx+1}" for idx in range(len(route_coordinates))],
        'Latitude': [coord[0] for coord in route_coordinates],
        'Longitude': [coord[1] for coord in route_coordinates]
    }

    df = pd.DataFrame(data)
    excel_file = 'route_coordinates.xlsx'
    df.to_excel(excel_file, index=False)

    print(f"The coordinates have been successfully saved in '{excel_file}' file.")
else:
    print("Coordinates not found.")
