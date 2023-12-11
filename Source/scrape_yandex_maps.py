from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Path to Chromedriver
driver_path = r"C:\Users\furka\Downloads\chromedriver-win64\chromedriver.exe"

# Configure Chrome options
chrome_options = Options()
# Add any additional options if needed

# Specify the Chromedriver executable path directly
chrome_options.binary_location = driver_path

# Start Chromedriver with specified options
driver = webdriver.Chrome(options=chrome_options)

# Define your route steps here
route_steps = [
    (38.4251379, -80.1856578),  # Appalachian Mountains koordinatları
    (36.950932321950035, -81.08864802133368),
    (36.945826169037986, -80.94991110679278),
    # ... Diğer rota adımları ...
    (39.9512496, -76.7336521),  # York County koordinatları
]

# Visit each coordinate in the route steps and take screenshots
for index, step in enumerate(route_steps, start=1):
    url = f"https://yandex.com.tr/harita/?l=sat&ll={step[1]},{step[0]}&z=17"
    driver.get(url)
    time.sleep(5)  # Haritanın yüklenmesini beklemek için bir süre bekleme

    # Ekran görüntüsü al
    driver.save_screenshot(f'yandex_harita_goruntusu_{index}.png')

# Close the browser
driver.quit()
