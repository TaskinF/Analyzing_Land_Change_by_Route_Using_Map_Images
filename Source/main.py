import math
from PIL import Image
import os
import numpy as np
from skimage.feature import graycomatrix, graycoprops
from skimage import io, color
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.semi_supervised import SelfTrainingClassifier
import random

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

# Setting the haralick_features_list
haralick_features_list = []

for filename in image_files:
    # Open each image
    image = Image.open(filename)

    # Crop from the specified width on the left side
    cropped_image = image.crop((crop_width, 0, image.width, image.height))

    # Clear memory
    image.close()

    # Rotate the images based on the bearing
    rotated_image = cropped_image.rotate(result_bearing, expand=True)

    # Convert the image to RGB if it has an alpha channel (4th channel)
    if rotated_image.mode == 'RGBA':
        rotated_image = rotated_image.convert('RGB')

    rotated_filename = "rotated_" + filename  # New file name for rotated images
    rotated_image.save(rotated_filename)

    # Calculate Haralick features for the rotated image
    gray_image = color.rgb2gray(np.array(rotated_image))  # Convert rotated image to grayscale

    # Convert to unsigned integer type
    gray_image_uint8 = (gray_image * 255).astype(np.uint8)

    glcm = graycomatrix(gray_image_uint8, distances=[1, 2, 3], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], symmetric=True, normed=True)
    properties = ['contrast', 'homogeneity', 'energy', 'correlation']
    haralick_features = np.hstack([graycoprops(glcm, prop).ravel() for prop in properties])
    haralick_features_list.append(haralick_features)

    # Close image files
    rotated_image.close()

# All Haralick features for the images are stored in 'haralick_features_list'

print(len(haralick_features_list))

# Yarı gözetimli öğrenme için rastgele etiketler oluşturun
labels = [-1] * len(haralick_features_list)  # -1, etiketlenmemiş örnekleri temsil eder

# Belirli bir yüzde oranındaki örnekleri rastgele etiketleyin
labeled_percent = 0.2  # Örneklerin yüzde kaçının etiketleneceğini belirleyin
num_labeled = int(len(haralick_features_list) * labeled_percent)

# Rastgele seçilen örnekleri etiketle
labeled_indices = np.random.choice(len(haralick_features_list), size=num_labeled, replace=False)
for idx in labeled_indices:
    labels[idx] = np.random.randint(0, 2)  # 0 veya 1 olarak rastgele etiketle

X_labeled, X_unlabeled, y_labeled, y_unlabeled = train_test_split(
    haralick_features_list, labels, test_size=0.2, random_state=42
)


X_train, X_test, y_train, y_test = train_test_split(
    X_labeled, y_labeled, test_size=0.2, stratify=y_labeled, random_state=42
)

# Semi-Supervised SVM (Semi-SVM) Model
base_classifier = SVC(probability=True)
model = SelfTrainingClassifier(base_classifier, criterion="k_best", k_best=50)
model.fit(X_train, y_train)


predictions = model.predict(X_test)


accuracy = accuracy_score(y_test, predictions)
print(f"Model accuracy: {accuracy}")