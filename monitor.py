from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pathlib
import os

url = 'http://my.jetpack/'
page_title = 'Jetpack MiFi 8800L'

driver_location = pathlib.Path.cwd() / "geckodriver"

options = Options()
# We use all methods available to ensure the browser is headless
# Depending on OS, Firefox build and execution environment, some work, others do not
options.headless = True
options.add_argument("-headless")
os.environ['MOZ_HEADLESS'] = '1'
driver = webdriver.Firefox(options=options, executable_path=driver_location)

browser = webdriver.Firefox(executable_path=driver_location)
browser.implicitly_wait(3)


browser.get(url)
title = browser.title
if page_title not in title:
    exit(1)
status_battery = browser.find_element_by_css_selector('#statusBar_battery').text
status_rssi = browser.find_element_by_css_selector('#statusBar_rssi').get_attribute('class')
status_tech = browser.find_element_by_css_selector('#statusBar_tech').get_attribute('class')

status_battery = status_battery.replace('%', '')
status_rssi = status_rssi.replace('rssi_', '')
status_tech = status_tech.replace('tech_', '')
browser.quit()
print("Finished.")
