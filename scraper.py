from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

# Initialize service and driver
service = FirefoxService(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)

MATRIX_URL = "https://courses.osu.edu/psp/csosuct/EMPLOYEE/PUB/c/OSR_CUSTOM_MENU.OSR_ROOM_MATRIX.GBL?"
# Get base page
driver.get(MATRIX_URL)
# Wait for page to load
driver.implicitly_wait(15)

# switch the webdriver object to the iframe.
frame = driver.find_element(By.ID, "ptifrmtgtframe")
driver.switch_to.frame(frame)

# Get elements that we need to interact with
facility_id_input = driver.find_element(By.ID, "OSR_DERIVED_RM_FACILITY_ID")
refresh_calendar_btn = driver.find_element(By.ID, "DERIVED_CLASS_S_SSR_REFRESH_CAL")

def get_room(facility_id):
    # Delete text currently in Facility ID input
    facility_id_input.send_keys(Keys.CONTROL, "a")  # or Keys.COMMAND on Mac
    # Type facility id into input
    facility_id_input.send_keys(facility_id)
    # Request calendar refresh
    refresh_calendar_btn.click()
    # Wait for refresh
    driver.implicitly_wait(2)

    # Parse into array of days containing arrays of intervals
      # Each interval added will be a tuple of the minutes from 12 midnight that it starts and the minutes from midnight when it ends
    week = [[]] * 7

# Get each room necessary
get_room("DL0369")

