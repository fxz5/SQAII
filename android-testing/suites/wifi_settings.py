from datetime import datetime

from uiautomator import Device
import time
import logging

from suites.suite import Suite
from utils.utils import Utils, Logger
from models.manager import DeviceManager


class WiFiSettings(Suite):

    def __init__(self, d, logger, adb_only=False):
        # type: (DeviceManager, Logger, bool) -> None
        logging.info("Initializing WiFiSettings Component")
        Suite.__init__(self, d, logger)
        self.app = "Phone"
        self.package = "com.google.android.dialer"
        logging.basicConfig(filename='example.log', level=logging.DEBUG)

    def execute_suite(self):
        self.turn_off_wifi()
        self.turn_on_wifi()

    def turn_on_wifi(self):
        start_time = datetime.now()
        current_test_case = "WiFi Turn On"
        try:
            # Test Conditions
            Utils.start_home(self.serial)
            self.device.open.quick_settings()
            if not self.__get_toggle_info(0):
                self.__toggle_wifi()
            else:
                self.__toggle_wifi()
                self.__toggle_wifi()
            Utils.wait_long()
            self.pass_test()
            self.logger.log(start_time,
                            self.module,
                            current_test_case, "SUCCESS",
                            "")
        except Exception as e:
            self.fail_test()
            self.logger.log(start_time, self.module,
                            current_test_case,
                            "ERROR", str(e) + e.message)

    def turn_off_wifi(self):
        start_time = datetime.now()
        current_test_case = "WiFi Turn Off"
        try:
            Utils.start_home(self.serial)
            self.device.open.quick_settings()
            if self.__get_toggle_info(0):
                self.__toggle_wifi()
            else:
                self.__toggle_wifi()
                self.__toggle_wifi()
            Utils.wait_long()
            self.pass_test()
            self.logger.log(start_time,
                            self.module,
                            current_test_case, "SUCCESS",
                            "")
        except Exception as e:
            self.fail_test()
            self.logger.log(start_time, self.module,
                            current_test_case,
                            "ERROR", str(e) + e.message)

    def __toggle_wifi(self):
        self.device.open.quick_settings()
        time.sleep(0.5)
        self.device(index=0, className="android.widget.Switch").click()
        time.sleep(0.5)

    def __get_toggle_info(self, i):
        return True if self.device(index=i, className="android.widget.Switch")\
            .info['text'] == 'On' else False
