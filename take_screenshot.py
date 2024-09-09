import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--start-maximized")  # Start maximized
chrome_options.add_argument("--proxy-server=127.0.0.1:8889")  # Set proxy

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the webpage
url = "https://www.examprepper.co/exam/72/2"
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Adjust this value based on the page load time

# Get the full page dimensions
total_height = driver.execute_script("return document.body.scrollHeight")
total_width = driver.execute_script("return document.body.scrollWidth")

# Set the viewport size to the full page size
driver.set_window_size(total_width, total_height)

# Take a screenshot of the full page
screenshot = driver.get_screenshot_as_png()

# Save the screenshot as an image
with open("screenshot.png", "wb") as file:
    file.write(screenshot)

# Close the browser
driver.quit()

# Convert the image to PDF
image = Image.open("screenshot.png")
pdf_path = "webpage_screenshot.pdf"
image.save(pdf_path, "PDF", resolution=100.0)

print(f"Screenshot saved as {pdf_path}")
