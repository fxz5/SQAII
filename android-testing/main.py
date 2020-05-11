from models.manager import DeviceManager
from suites.calculator import CalculatorSuite
from suites.phonecall import PhoneCallSuite
from suites.suite import TestRun
from suites.wifi_settings import WiFiSettingsSuite
from utils.utils import Logger

dev_man = DeviceManager(1)
dev_man.show_devices()
log = Logger()

suites = list()
tests = [WiFiSettingsSuite, CalculatorSuite]
for device in dev_man.devices:
    for test_type in tests:
        suites.append(test_type(device, log))
    # phone_suite = PhoneCallSuite(device, log, False)
    # phone_suite_adb = PhoneCallSuite(device, log, True)
    # suites.append(WiFiSettingsSuite(device, log))
    # calculator_suite = CalculatorSuite(device, log)

    # suites.append(phone_suite)
    # suites.append(phone_suite_adb)
    # suites.append(calculator_suite)

test = TestRun()
for suite in suites:
    test.add_suite(suite)
test.execute_all_suites()
