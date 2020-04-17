from models.manager import DeviceManager
from suites.phonecall import PhoneCallSuite
from suites.suite import TestRun
from suites.wifi_settings import WiFiSettingsSuite
from utils.utils import Logger

dev_man = DeviceManager()
log = Logger()

phone_suite = PhoneCallSuite(dev_man, log, False)
phone_suite_adb = PhoneCallSuite(dev_man, log, True)
wifi_suite = WiFiSettingsSuite(dev_man, log)

test = TestRun()
# test.add_suite(phone_suite_adb)
test.add_suite(phone_suite)
test.add_suite(wifi_suite)
test.execute_all_suites()
# wifi_suite.turn_on_wifi()
# phone_suite.call_number_adb(True)
