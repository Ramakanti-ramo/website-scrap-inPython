from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import csv
import time

# Start a Selenium webdriver with Firefox using GeckoDriverManager to manage the driver
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
driver.implicitly_wait(5)

# Read article links from the CSV file
article_links = []
with open('article_links.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        article_links.append(row[0])

# Function to extract data from each article link
def extract_data_from_article(article_link):
    driver.get(article_link)
    time.sleep(2)  # Adding a delay to ensure page is loaded completely

    try:
        # Extract data
        title = driver.find_element(By.CLASS_NAME, 'native_story_title').text
        subtitle = driver.find_element(By.CLASS_NAME, 'synopsis').text

        # Extract image and its text
        image_container = driver.find_element(By.CLASS_NAME, 'custom-caption')
        image = image_container.find_element(By.TAG_NAME, 'img').get_attribute('src')
        image_text = image_container.text

        # Extract text from p tags under story_details
        story_details = driver.find_element(By.CLASS_NAME, 'story_details')
        paragraphs = story_details.find_elements(By.TAG_NAME, 'p')
        paragraphs_text = [p.text for p in paragraphs]

        return {
            "Title": title,
            "Subtitle": subtitle,
            "Image URL": image,
            "Image Text": image_text,
            "Paragraphs Text": '\n'.join(paragraphs_text)
        }
    except:
        title = "Invalid Link"
        subtitle = "Invalid Link"
        image = "Invalid Link"
        image_text = "Invalid Link"
        paragraphs_text = "Invalid Link"

        return {
            "Title": title,
            "Subtitle": subtitle,
            "Image URL": image,
            "Image Text": image_text,
            "Paragraphs Text": '\n'.join(paragraphs_text)
        }

# Extract data from each article link and store in a list
# rama
extracted_data = []
for article_link in article_links:
    extracted_data.append(extract_data_from_article(article_link))

# Write extracted data to a CSV file
csv_file = 'extracted_data.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=extracted_data[0].keys())
    writer.writeheader()
    writer.writerows(extracted_data)

print("Extracted data saved to", csv_file)

# Close the webdriver
driver.quit()
