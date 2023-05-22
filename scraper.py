from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import time
import re
import sqlite3
import os.path
  

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

availability_time_pattern = r"<br>(\d{1,2}:\d{2}[AP]M) - (\d{1,2}:\d{2}[AP]M)<br>"


def make_db():
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""CREATE TABLE building
                      (
                         building_number TEXT PRIMARY KEY,
                         name TEXT,
                         latitude REAL,
                         longitude REAL
                      )""")
    cursor.execute("""CREATE TABLE classroom
                      (
                         facility_id TEXT PRIMARY KEY,
                         building_number TEXT,
                         FOREIGN KEY(building_number) REFERENCES building(building_number)
                      )""")
    cursor.execute("""CREATE TABLE block
                      (
                         facility_id TEXT,
                         day_of_week INTEGER,
                         start_minutes INTEGER,
                         end_minutes INTEGER,
                         FOREIGN KEY(facility_id) REFERENCES classroom(facility_id)
                      )""")
    conn.commit()


def get_blocks():
    # Load the base page
    driver.get(MATRIX_URL)
    driver.implicitly_wait(15)
    frame = driver.find_element(By.ID, "ptifrmtgtframe")
    driver.switch_to.frame(frame)

    classrooms = [fac[0] for fac in cursor.execute("SELECT facility_id FROM classroom")]
    for facility_id in tqdm(classrooms):
        print(f"Getting blocks in {facility_id}...")

        # Get elements that we need to interact with (Not sure why these get disconnected after each run)
        facility_id_input = driver.find_element(By.ID, "OSR_DERIVED_RM_FACILITY_ID")
        refresh_calendar_btn = driver.find_element(By.ID, "DERIVED_CLASS_S_SSR_REFRESH_CAL")
        wait_icon = driver.find_element(By.ID, "WAIT_win0")

        # Delete text currently in Facility ID input
        facility_id_input.send_keys(Keys.CONTROL, "a")  # or Keys.COMMAND on Mac
        # Type facility id into input
        facility_id_input.send_keys(facility_id)
        # Request calendar refresh
        refresh_calendar_btn.click()
        # Wait for page to load by waiting until the wait icon is not being displayed. If not loaded in 15 seconds, throw an error
        WebDriverWait(driver, timeout=15).until_not(lambda x: wait_icon.is_displayed())

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
                    match = re.search(availability_time_pattern, cell.get_attribute('innerHTML'))
                    #print(calendar.day_name[true_col-1], match.group(1), match.group(2))
                    #print('')
                    cursor.execute("INSERT INTO block VALUES (?,?,?,?)", (facility_id, true_col-1, string_to_minutes(match.group(1)), string_to_minutes(match.group(2))))
        conn.commit()


def get_classrooms():
    driver.get(MATRIX_URL)
    driver.implicitly_wait(15)
    frame = driver.find_element(By.ID, "ptifrmtgtframe")
    driver.switch_to.frame(frame)
    facility_id_search_btn = driver.find_element(By.ID, "OSR_DERIVED_RM_FACILITY_ID$prompt")
    facility_id_search_btn.click()
    driver.implicitly_wait(10)

    driver.switch_to.default_content()
    frame2 = driver.find_element(By.ID, "ptModFrame_0")
    driver.switch_to.frame(frame2)

    facility_type_select = Select(driver.find_element(By.ID, "#ICKeySelect"))
    facility_type_select.select_by_value('2')
    building_id_input = driver.find_element(By.ID, "FACILITY_TBL_BLDG_CD")
    building_look_up_btn = driver.find_element(By.ID, "#ICSearch")

    buildings = [bldg[0] for bldg in cursor.execute("SELECT building_number FROM building")]
    for bldg_id in tqdm(buildings):
        building_id_input = driver.find_element(By.ID, "FACILITY_TBL_BLDG_CD")
        building_look_up_btn = driver.find_element(By.ID, "#ICSearch")
        building_id_input.send_keys(Keys.CONTROL, "a")  # or Keys.COMMAND on Mac
        building_id_input.send_keys(bldg_id)
        building_look_up_btn.click()
        time.sleep(5)
        try:
            rooms_table = driver.find_element(By.ID, "PTSRCHRESULTS").find_element(By.TAG_NAME, "tbody")
            for row in rooms_table.find_elements(By.TAG_NAME, 'tr')[1:]:
                fac_id = row.find_element(By.TAG_NAME, 'td').find_element(By.TAG_NAME, 'span').text
                print(fac_id)
                cursor.execute("INSERT INTO classroom VALUES (?,?)", (fac_id, bldg_id))
        except Exception:
            print("No rooms found for building:", bldg_id)
    conn.commit()


def get_building_latlong(building_number):
    url = 'https://www.osu.edu/map/building/' + building_number
    driver.get(url)
    driver.implicitly_wait(3)
    building_frame = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(building_frame)
    main_content = driver.find_element(By.ID, "maincontent").get_attribute('innerHTML')
    #print(main_content)
    soup = BeautifulSoup(main_content, 'html.parser').find_all("div", {"class": "column span-9 osu-margin-top"})[0].find_all("p")[0]
    soup.find('strong').decompose()
    address = soup.encode_contents().decode("utf-8").replace("<br/>", " ").split('\n')[-1].strip()
    #print(address)
    try:
        req = requests.get("https://geocode.maps.co/search", params={'q': address}).json()[0]
        # print(req['lat'], req['lon'])
        return req['lat'], req['lon']
    except Exception:
        print(f"Could not get lat/long for #{building_number} at: {address}")
        return 0, 0


def get_buildings():
    response = requests.post('https://www.osu.edu/map/buildingindex.php', data={'sort': 'letter', 'Submit': 'Sort Buildings'})

    # parse results into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # go inside div id: buildingIndex and parse all the li tags
    for li in tqdm(soup.find(id="buildingIndex").find_all("li")):
        # get the building number
        number = li.find_all("strong")[1].text
        building_number = re.search(r"\((\d+)\)", number).group(1)

        # Get lat/long from building_number
        lat, long = get_building_latlong(building_number)

        # get the building name
        a = li.find("a")
        a.span.decompose()
        building_name = a.text.rstrip()

        building = (building_number, building_name, lat, long)
        print("Retrieved building:", building_number, building_name)
        cursor.execute("INSERT INTO building VALUES (?,?,?,?)", building)
    conn.commit()


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


def main():
    if os.path.isfile('roomMatrix.db'):
        print("Database already exists. How do you wish to continue:")
        print("1. Delete and recreate database")
        print("2. Use existing database")
        print("3. Exit")
        choice = input("> ")
        if choice == '1':
            os.remove('roomMatrix.db')
            global conn, cursor
            conn = sqlite3.connect('roomMatrix.db')
            cursor = conn.cursor()
            make_db()
        elif choice == '2':
            pass
        elif choice == '3':
            exit()
    else:
        make_db()

    # Get list of buildings
    get_buildings()

    # Get list of classrooms
    get_classrooms()

    # Get blocks for each classroom
    get_blocks()

if __name__ == '__main__':
    main()