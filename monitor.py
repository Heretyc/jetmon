from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pathlib
import os
from win10toast import ToastNotifier

# create an object to ToastNotifier class
notifier_object = ToastNotifier()


url = 'http://my.jetpack/'
page_title = 'Jetpack MiFi 8800L'

driver_location = pathlib.Path.cwd() / "geckodriver"
icon_location = pathlib.Path.cwd() / "blackburnDevIcon.ico"

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
browser.quit()

status_battery = int(status_battery.replace('%', ''))
status_rssi = int(status_rssi.replace('rssi_', ''))
status_tech = status_tech.replace('tech_', '')

percent_rssi = int((status_rssi/5)*100)

notifier_object.show_toast("Jetpack Status", f"""Battery:{status_battery}%
Signal: {percent_rssi}%
Network: {status_tech}""", duration=30, icon_path=icon_location)



print("Finished.")
