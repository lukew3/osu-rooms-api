from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import time
import re
import sqlite3

conn = sqlite3.connect('roomMatrix.db')
cursor = conn.cursor()

# Initialize service and driver
service = FirefoxService(executable_path=GeckoDriverManager().install())
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.add_argument('--headless') # Comment this line to see the browser gui
driver = webdriver.Firefox(service=service, options=fireFoxOptions)

print("Getting initial page...")
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

pattern = r"<br>(\d{1,2}:\d{2}[AP]M) - (\d{1,2}:\d{2}[AP]M)<br>"

def get_true_column(col, rowspans):
    # Increment col by the number of blocked columns in front of it
    j = 0
    zero_count = -1
    true_col = col
    while zero_count != col:
        # If a column doesn't have a rowspan, add a zero
        if rowspans[j] == 0:
            zero_count += 1
        else: # If a column has a rowspan, increment the col counter
            true_col += 1
        j += 1
    return true_col


def string_to_minutes(time_string):
    # Convert time string to minutes from midnight
    # Time string is in format "HH:MM AM/PM"
    # Split into hours and minutes
    time_list = time_string.split(':')
    # Convert hours to minutes
    hours = int(time_list[0])
    minutes = int(time_list[1][:-2])
    if time_list[1][-2:] == 'PM' and hours != 12:
        hours += 12
    # I would add a condition for -12 hours at 12:XX AM, but this is unreachable because we are only querying between 8am and 10pm
    return hours * 60 + minutes


def get_room(facility_id):
    print(f"Getting blocks in {facility_id}...")

    # Re-get elements that we need to interact with (Not sure why these get disconnected after each run)
    facility_id_input = driver.find_element(By.ID, "OSR_DERIVED_RM_FACILITY_ID")
    refresh_calendar_btn = driver.find_element(By.ID, "DERIVED_CLASS_S_SSR_REFRESH_CAL")

    # Delete text currently in Facility ID input
    facility_id_input.send_keys(Keys.CONTROL, "a")  # or Keys.COMMAND on Mac
    # Type facility id into input
    facility_id_input.send_keys(facility_id)
    # Request calendar refresh
    refresh_calendar_btn.click()
    # Wait for refresh
    time.sleep(10)
    # driver.implicitly_wait(10)

    # Parse into array of days containing arrays of intervals
      # Each interval added will be a tuple of the minutes from 12 midnight that it starts and the minutes from midnight when it ends
    table = driver.find_element(By.ID, "WEEKLY_SCHED_HTMLAREA").find_element(By.TAG_NAME, 'tbody')
    # Array of integers representing how many more rows a column is blocked for
    rowspans = [0] * 8
    next_rowspans = [0] * 8
    # print(table.get_attribute('innerHTML'))
    for row in table.find_elements(By.TAG_NAME, 'tr'):
        # Decrement next_rowspans
        for i in range(8):
            if next_rowspans[i] != 0: next_rowspans[i] -= 1
        # Move next_rowspans to rowspans
        rowspans = next_rowspans.copy()

        for col, cell in enumerate(row.find_elements(By.TAG_NAME, 'td')):
            true_col = get_true_column(col, rowspans)
            # Add this cell's rowspan to next_rowspans
            rowspan = cell.get_attribute('rowspan')
            if rowspan: next_rowspans[true_col] += int(rowspan)
            # If a cell has a color style on it...
            if (cell.get_attribute('style') != ''):
                # print(cell.get_attribute('innerHTML')) # Full content of each section
                # Use regex to get start and end time
                match = re.search(pattern, cell.get_attribute('innerHTML'))
                #print(calendar.day_name[true_col-1], match.group(1), match.group(2))
                #print('')
                cursor.execute("INSERT INTO block VALUES (?,?,?,?)", (facility_id, true_col-1, string_to_minutes(match.group(1)), string_to_minutes(match.group(2))))
    conn.commit()

# Get each room in classroom table
# get_room("DL0369")
classrooms = [fac[0] for fac in cursor.execute("SELECT facility_id FROM classroom")]
for fac in classrooms:
    get_room(fac)
