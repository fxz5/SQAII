import json, datetime

from typing import Optional

from models.TestCaseStatus import TCStatus
from models.manager import DeviceManager
from suites.suite import Suite
from utils.utils import Logger, Utils, AppUtils, CalculatorUtils


class CalculatorSuite(Suite):
    def __init__(self, d, logger):
        # type: (DeviceManager, Logger) -> None
        print "Initializing PhoneCall Component"
        Suite.__init__(self, d, logger, "Calculator", "Calculator",
                       "com.google.android.calculator")

    def execute_suite(self):
        self.cal_001()

    def cal_001(self):
        start_time = datetime.datetime.now()
        self.test_conditions()
        op = self.__read_test_case("cal_001")
        array_operation = op['operation']
        result = op['result']
        for element in array_operation:
            for digit in element:
                CalculatorUtils.input_digit(self.device, digit)
        actual_result = CalculatorUtils.get_result(self.device)
        self.__compare_results(result, actual_result, "cal_001", start_time)

    def __compare_results(self, expected, result, test_case, time):
        if expected == result:
            self.pass_test(test_case, time)
        else:
            self.fail_test(test_case, time,
                           error="(expected, received) (" + expected + ", " +
                                 result + ")")

    @staticmethod
    def __read_test_case(test_case):
        # type: (str) -> Optional[dict]
        with open('data/calculator.json') as json_file:
            data = json.load(json_file)
            return data[test_case] if data[test_case] else None

    def test_conditions(self):
        Utils.start_home(self.serial)
        AppUtils.kill_app(self.serial, self.package)
        AppUtils.open_app(self.device, self.serial, self.app)
        Utils.wait_short()
