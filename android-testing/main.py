from models.manager import DeviceManager
from suites.calculator import CalculatorSuite
from suites.suite import TestRun
from utils.utils import Logger

dev_man = DeviceManager(1)
dev_man.show_devices()
log = Logger()

suites = list()
tests = [CalculatorSuite]
for device in dev_man.devices:
    for test_type in tests:
        suites.append(test_type(device, log))

test = TestRun()
for suite in suites:
    test.add_suite(suite)
test.execute_all_suites()
