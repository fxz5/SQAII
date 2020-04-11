from uiautomator import Device
import time
import logging

from utils.utils import Utils
from models.manager import DeviceManager


class WiFiSettings:
    total_tests = 2
    passed_tests = 0
    failed_tests = 0

    def __init__(self, d, adb_only=False):
        # type: (DeviceManager, bool) -> None
        self.device = d.get_device()
        self.serial = d.get_serial()
        self.app = "Phone"
        self.package = "com.google.android.dialer"
        logging.basicConfig(filename='example.log', level=logging.DEBUG)
        logging.info("Initializing WiFiSettings Component")

    def turn_on_wifi(self):
        # Test Conditions
        Utils.start_home(self.serial)
        self.device.open.quick_settings()
        if not self.__get_toggle_info(0):
            self.__toggle_wifi()
        else:
            self.__toggle_wifi()
            self.__toggle_wifi()
        Utils.wait_long()

    def turn_off_wifi(self):
        Utils.start_home()
        self.device.open.quick_settings()
        if self.__get_toggle_info(0):
            self.__toggle_wifi()
        else:
            self.__toggle_wifi()
            self.__toggle_wifi()
        Utils.wait_long()

    def __toggle_wifi(self):
        self.device.open.quick_settings()
        time.sleep(0.5)
        self.device(index=0, className="android.widget.Switch").click()
        time.sleep(0.5)

    def __get_toggle_info(self, i):
        return True if self.device(index=i, className="android.widget.Switch")\
            .info['text'] == 'On' else False
