from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common import exceptions as selenium_exceptions
import pathlib
import os
from win10toast import ToastNotifier
import time

if __name__ == "__main__":
    print("Monitor started...")
    while True:

        # create an object to ToastNotifier class
        notifier_object = ToastNotifier()


        url = 'http://my.jetpack/'
        page_title = 'Jetpack MiFi 8800L'
        interval_poll = 15
        interval_sleep = 120

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

        try:
            browser.get(url)
        except selenium_exceptions.WebDriverException:
            notifier_object.show_toast("Jetpack Status", f"Jetpack disconnected", duration=interval_sleep, icon_path=icon_location)
            continue
        title = browser.title
        if page_title not in title:
            notifier_object.show_toast("Jetpack Status", f"Jetpack disconnected", duration=interval_sleep, icon_path=icon_location)
            continue
        status_battery = browser.find_element_by_css_selector('#statusBar_battery').text
        status_rssi = browser.find_element_by_css_selector('#statusBar_rssi').get_attribute('class')
        status_tech = browser.find_element_by_css_selector('#statusBar_tech').get_attribute('class')


        attempts_left = 10
        while attempts_left > 0:
            attempts_left -= 1
            try:
                status_battery = int(status_battery.replace('%', ''))
                break
            except ValueError:
                status_battery = browser.find_element_by_css_selector('#statusBar_battery').text


        status_rssi = int(status_rssi.replace('rssi_', ''))
        status_tech = status_tech.replace('tech_', '')

        browser.quit()

        percent_rssi = int((status_rssi/5)*100)

        if percent_rssi < 30:
            notifier_object.show_toast("Jetpack Status", f"Poor signal using {status_tech}", duration=interval_poll, icon_path=icon_location)
        elif status_battery < 10:
            notifier_object.show_toast("Jetpack Status", f"Battery at {status_battery}%!", duration=interval_poll, icon_path=icon_location)
        else:
            time.sleep(interval_sleep)
#             notifier_object.show_toast("Jetpack Status", f"""Battery:{status_battery}%
# Signal: {percent_rssi}%
# Network: {status_tech}""", duration=interval_sleep, icon_path=icon_location)



print("Finished.")
