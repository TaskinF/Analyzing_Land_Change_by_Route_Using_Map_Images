from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Path to Chromedriver
driver_path = r"C:\Users\furka\Downloads\chromedriver-win64\chromedriver.exe"

# Configure Chrome options
chrome_options = Options()

# Specify the Chromedriver executable path directly
chrome_options.binary_location = driver_path

# Start Chromedriver with specified options
driver = webdriver.Chrome(options=chrome_options)

# Setting the windows size
driver.set_window_size(1920, 1080)

# Read coordinates from Excel file
excel_file = r"C:\Users\furka\PycharmProjects\Automatic_Cross_Sectional_Surface_Analysis_from_Aerial_Photographs\Automatic-Cross-Sectional-Surface-Analysis-from-Aerial-Photographs\Source\route_coordinates.xlsx"
df = pd.read_excel(excel_file)

# Create route_steps list from Latitude and Longitude columns in the Excel file
route_steps = [(lat, lon) for lat, lon in zip(df['Latitude'], df['Longitude'])]

# Visit each coordinate in the route steps and take screenshots
for index, step in enumerate(route_steps, start=1):
    url = f"https://yandex.com.tr/harita/?l=sat&ll={step[1]},{step[0]}&z=18.5"
    driver.get(url)
    time.sleep(3)
    # Ekran görüntüsü al
    driver.save_screenshot(f'yandex_harita_goruntusu_{index}.png')

# Close the browser
driver.quit()
