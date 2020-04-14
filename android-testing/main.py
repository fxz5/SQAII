from uiautomator import device
from models.manager import DeviceManager
from suites.phonecall import PhoneCall
from suites.suite import TestRun
from suites.wifi_settings import WiFiSettings
from utils.utils import Logger

dev_man = DeviceManager()
log = Logger()

phone_suite = PhoneCall(dev_man, log, False)
wifi_suite = WiFiSettings(dev_man, log)

test = TestRun()
test.add_suite(phone_suite)
test.add_suite(wifi_suite)
test.execute_all_suites()
# wifi_suite.turn_on_wifi()
# phone_suite.call_number_adb(True)
