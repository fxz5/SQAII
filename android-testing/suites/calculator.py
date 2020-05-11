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
        self.__preprocess_test_cases()
        for test_case in self.test_cases:
            self.__generic_tc(test_case)

    def __generic_tc(self, tc_id):
        start_time = datetime.datetime.now()
        self.test_conditions()
        array_operation, result = self.__get_tc_data(tc_id)
        for element in array_operation:
            for digit in element:
                CalculatorUtils.input_digit(self.device, digit)
        actual_result = CalculatorUtils.get_result(self.device)
        self.__compare_results(result, actual_result, tc_id, start_time)

    def __preprocess_test_cases(self):
        test_cases = list()
        with open('data/calculator.json') as json_file:
            data = json.load(json_file)
            for tc in data:
                test_cases.append(tc)
        test_cases.sort()
        self.test_cases = test_cases

    def __get_tc_data(self, tc):
        # type: (str) -> ([str], str)
        """
        Retrieves the test case data for the specified test case id. Returns
        operation and results.
        """
        op = self.__read_test_case(tc)
        array_operation = op['operation']
        result = op['result']
        return array_operation, result

    def __compare_results(self, expected, result, test_case, time):
        # type: (str, str, str, datetime.datetime) -> None
        """
        Compares results and determines log and test output.
        """
        print expected
        print result
        print test_case
        print time
        if expected == result:
            print "PASSED"
            self.pass_test(test_case, time)
        else:
            print "NOT EPIC"
            self.fail_test(test_case, time,
                           error="(expected:received) (" + expected + ":" +
                                 result + ")")

    @staticmethod
    def __read_test_case(test_case):
        # type: (str) -> Optional[dict]
        """
        Utility function that reads test_case info from json file.
        """
        with open('data/calculator.json') as json_file:
            data = json.load(json_file)
            return data[test_case] if data[test_case] else None

    def test_conditions(self):
        """
        Sets initial test conditions.
        """
        Utils.start_home(self.serial)
        AppUtils.kill_app(self.serial, self.package)
        AppUtils.open_app(self.device, self.serial, self.app)
        Utils.wait_short()
