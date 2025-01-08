from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import urllib.request as urllib2
import time

# Instagram credentials
USERNAME = "minggongdd"
PASSWORD = "password"
PROFILE_URL = f"https://www.instagram.com/{USERNAME}/"

SCROLL_DELAY = 1
PAGE_DELAY = 5
DIALOG_CLASS = "xyi19xy"
ELEMENT_CLASS = "div[class*='x1dm5mii']"

# automatically scrolls to the bottom
def scroll(driver, path, USERNAME=USERNAME, SCROLL_DELAY=SCROLL_DELAY, PAGE_DELAY=PAGE_DELAY, DIALOG_CLASS=DIALOG_CLASS, ELEMENT_CLASS=ELEMENT_CLASS, PROFILE_URL=PROFILE_URL):

    # Navigate to the profile page
    driver.get(PROFILE_URL)
    time.sleep(PAGE_DELAY)  # Wait for the page to load
    
    # Click the "Followers" or "Following" button, specified by `path`
    button = driver.find_element(By.XPATH, f"//a[contains(@href, '/{USERNAME}/{path}/')]")
    button.click()
    time.sleep(PAGE_DELAY)  # Wait for the dialog to appear

    # Wait for the dialog to appear after clicking the button
    dialog = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, DIALOG_CLASS))
    )

    # Scroll to the bottom of the list
    print("Scrolling to the bottom of the list...")

    last_height = driver.execute_script("return arguments[0].scrollHeight", dialog)

    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
        time.sleep(SCROLL_DELAY)  # Wait for new content to load
        new_height = driver.execute_script("return arguments[0].scrollHeight", dialog)
        if new_height == last_height:
            break
        last_height = new_height

        # Find all the individual follower elements inside the dialog
    elements_list = dialog.find_elements(By.CSS_SELECTOR, ELEMENT_CLASS)

    return elements_list

# extracts a set of usernames from a list of <a>
def extract_profile(elements_list):
    # Loop through and extract information from each follower
    elements_set = set()
    for element in elements_list:
        try:
            # Locate the <a> tag with the follower's profile link
            profile_link = element.find_element(By.CSS_SELECTOR, "a._a6hd")
            username = profile_link.get_attribute("href").split("/")[-2]
            #print(f"Username: {username}")
            elements_set.add(username)
        except NoSuchElementException:
            print("Could not extract info.")
    return elements_set

def save_html(filename, driver):
    html_source = driver.page_source
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_source)
    print("HTML source saved to followers_page.html.")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

try:
    # Log in to Instagram
    driver.get("https://www.instagram.com/")
    time.sleep(SCROLL_DELAY)
    
    # Input username and password
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    time.sleep(PAGE_DELAY)  # Wait for the login to complete

    # Find followers page
    followers_list = scroll(driver, "followers")

    followers_set = extract_profile(followers_list)

    # Find following page
    following_list = scroll(driver, "following")

    following_set = extract_profile(following_list)

finally:
    # Clean up
    driver.quit()

# Process followers and following list
#print(following_set)
#print(followers_set)
count = 0
for f in following_set:
    if f not in followers_set:
        print(f)
        count += 1

print(count)
