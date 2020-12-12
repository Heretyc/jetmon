from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common import exceptions as selenium_exceptions
import pathlib
import os
from win10toast import ToastNotifier
import time
import datetime
import humanize

def get_time_string():
    """
    Pulls a human readable time of day string.
    Designed to standardize time storage and display for ease of use and consistency
    :return: Current system time in HH:MM:SS
    :rtype: str
    """
    try:
        now = datetime.datetime.now()
    except AttributeError:
        now = datetime.now()
    return now.strftime("%H:%M:%S")



class Calc_Remaning_Life:
    def __init__(self):
        self.previous_percentages_list = []
        self.previous_times_list = []

    @staticmethod
    def calc_elapsed_minutes(past, present):
        """
        get past and present values using time.time() function

        ex: exec_time_minutes = calc_elapsed_minutes(__time_start, time_stop)[0]
        Be sure to add the [0] parameter to round the result.

        :param past: Any earlier time.time()
        :type past: time.time
        :param present: Any latter time.time()
        :type present: time.time
        :return: A tuple of the minutes between the two. See above notes on rounding the result.
        :rtype: tuple
        """
        #
        past = int(past)
        present = int(present)
        d = divmod(present - past, 86400)  # days
        h = divmod(d[1], 3600)  # hours
        m = divmod(h[1], 60)  # minutes
        return m[0]

    def _calc_remaining_life(self):
        if len(self.previous_percentages_list) < 2:
            raise ResourceWarning("Not enough data to calculate lifespan")
        delta_percentage = self.previous_percentages_list[-1] - self.previous_percentages_list[0]
        delta_seconds = self.previous_times_list[0] - self.previous_times_list[-1]

        avg_percent_per_second = delta_percentage / delta_seconds
        try:
            seconds_left = self.previous_percentages_list[-1] / avg_percent_per_second
        except ZeroDivisionError:
            raise ResourceWarning("Not enough data to calculate lifespan")

        return seconds_left


    def checkpoint(self, current_percentage):
        self.previous_times_list.append(time.time())
        self.previous_percentages_list.append(current_percentage)

        if len(self.previous_times_list) > 100:
            self.previous_times_list.pop(0)
            self.previous_percentages_list.pop(0)

        try:
            seconds_left = self._calc_remaining_life()
            print(f"{humanize.naturaldelta(datetime.timedelta(seconds=seconds_left))} left")
        except ResourceWarning:
            pass

if __name__ == "__main__":
    print("Monitor started...")
    remaining_life_object = Calc_Remaning_Life()
    while True:
        print("==================")
        print(f"=\/= {get_time_string()} =\/=")
        # create an object to ToastNotifier class
        notifier_object = ToastNotifier()


        url = 'http://my.jetpack/'
        page_title = 'Jetpack MiFi 8800L'
        interval_poll = 30
        interval_sleep = 120

        driver_location = pathlib.Path.cwd() / "geckodriver"
        icon_location = pathlib.Path.cwd() / "blackburnDevIcon.ico"
        driver_location = f"{driver_location.resolve()}"
        icon_location = f"{icon_location.resolve()}"
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
        remaining_life_object.checkpoint(status_battery)

        attempts_left = 10
        while attempts_left > 0:
            attempts_left -= 1
            try:
                status_rssi = int(status_rssi.replace('rssi_', ''))
                break
            except ValueError:
                status_rssi = browser.find_element_by_css_selector('#statusBar_rssi').get_attribute('class')

        status_tech = status_tech.replace('tech_', '')

        browser.quit()

        percent_rssi = int((status_rssi/5)*100)
        print(f"""Battery:{status_battery}%
Signal: {percent_rssi}%
Network: {status_tech}""")

        if percent_rssi < 30:
            notifier_object.show_toast("Jetpack Status", f"Poor signal using {status_tech}", duration=interval_poll, icon_path=icon_location)
        elif status_battery < 10:
            notifier_object.show_toast("Jetpack Status", f"Battery at {status_battery}%!", duration=interval_poll, icon_path=icon_location)
        else:
            time.sleep(interval_sleep)




print("Finished.")
