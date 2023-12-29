import math
from PIL import Image
import os
# Function to calculate the bearing between two points given their latitude and longitude
def calculate_bearing(lat1, lon1, lat2, lon2):
    # Convert angles to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Calculate the difference in longitudes
    delta_lon = lon2 - lon1

    # Calculate the bearing
    y = math.sin(delta_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    bearing = math.atan2(y, x)

    # Convert the angle from radians to degrees
    bearing = math.degrees(bearing)

    # Ensure the angle is within the range of 0-360 degrees
    bearing = (bearing + 360) % 360

    return bearing

# Example: Calculate the bearing between two coordinates
lat1 = 38.44933  # Harrisonburg, Virginia
lon1 = -78.8689
lat2 = 35.75  # Blue Ridge Mountain, USA
lon2 = -82.25

result_bearing = calculate_bearing(lat1, lon1, lat2, lon2)
print(f"The bearing between the two points is: {result_bearing} degrees")

# Get all image files in the folder
image_files = [file for file in os.listdir(".") if file.endswith(".png")]  # or update according to the file extension

# Cropping from the left side (for example, 400 pixels width)
crop_width = 400

for filename in image_files:
    # Open each image
    image = Image.open(filename)

    # Crop from the specified width on the left side
    cropped_image = image.crop((crop_width, 0, image.width, image.height))

    # Save the updated image
    updated_filename = "updated_" + filename  # You can create a new file name
    cropped_image.save(updated_filename)

    # Clear memory
    image.close()
"""
# İki görüntüyü aynı boyutlara getirme (örneğin, 800x600)
new_width = 1500
new_height = 897
image_1 = image_1.resize((new_width, new_height), Image.BILINEAR)
image_2 = image_2.resize((new_width, new_height), Image.BILINEAR)

image_1.save("resized_image_1.png")
image_2.save("resized_image_2.png")
"""