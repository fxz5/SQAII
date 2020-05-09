from models.manager import DeviceManager
from suites.phonecall import PhoneCallSuite
from suites.suite import TestRun
from suites.wifi_settings import WiFiSettingsSuite
from utils.utils import Logger

dev_man = DeviceManager(1, 2)
dev_man.show_devices()
log = Logger()

suites = list()
for device in dev_man.devices:
    phone_suite = PhoneCallSuite(device, log, False)
    phone_suite_adb = PhoneCallSuite(device, log, True)
    wifi_suite = WiFiSettingsSuite(device, log)
    suites.append(phone_suite)
    suites.append(phone_suite_adb)
    suites.append(wifi_suite)

test = TestRun()
for suite in suites:
    test.add_suite(suite)
test.execute_all_suites()
