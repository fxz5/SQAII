import json
import datetime

from models.exceptions import CallFailed
from models.manager import DeviceManager
from suites.suite import Suite
from utils.utils import AppUtils, Utils, Logger, PhoneUtils


class PhoneCallSuite(Suite):
    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    def __init__(self, d, logger, use_adb=False):
        # type: (DeviceManager, Logger, bool) -> None
        print "Initializing PhoneCall Component"
        Suite.__init__(self, d, logger)
        self.use_adb = use_adb
        self.app = "Phone"
        self.package = "com.google.android.dialer"
        self.module = "PhoneCall"
        if self.use_adb:
            self.module += "ADB"

    def execute_suite(self):
        self.call_number(True)

    def call_number(self, use_json=False):
        # type: (bool) -> None
        """
        Requests or loads phone number data from user or json and proceeds to
        call all numbers in the data.
        """
        test_case_name = "Phone Number Dialing"
        current_test_case = ""
        start_time = datetime.datetime.now()
        phone_numbers = []
        try:
            if not use_json:
                test_case_name += "-Manual"
                current_test_case = ""
                amount = int(raw_input("how many numbers do you want to test? "))
                for i in range(amount):
                    number = str(raw_input("enter phone number " + str(i+1) + ": "))
                    phone_numbers.append(number)
            else:
                test_case_name += "-JSON"
                with open('data/phone.json') as json_file:
                    data = json.load(json_file)
                    phone_numbers = data['phone_numbers']

            # Actual Calling of Numbers
            for number in phone_numbers:
                number = PhoneUtils.process_phone_number(number)
                print "Dialing number " + number
                current_test_case = test_case_name + "-" + str(number)
                if self.use_adb:
                    PhoneUtils.call_number(self.device, self.serial, number, self.use_adb)
                    success, e = PhoneUtils.end_call(self.device, self.use_adb)
                    if not success:
                        raise e
                else:
                    self.test_conditions()
                    PhoneUtils.call_number(self.device, self.serial,
                                           str(number), self.use_adb)
                    success, e = PhoneUtils.end_call(self.device, self.use_adb)
                    if not success:
                        raise e
                self.logger.log(self.serial, start_time,
                                self.module,
                                current_test_case, "SUCCESS",
                                "")
                self.pass_test()
        except Exception as e:
            self.logger.log(self.serial, start_time, self.module,
                            current_test_case,
                            "ERROR", str(e) + e.message)
            self.fail_test()

    def test_conditions(self):
        """
        Sets the initial test conditions for all tests.
        """
        Utils.start_home(self.serial)
        AppUtils.kill_app(self.serial, self.package)
        AppUtils.open_app(self.device, self.serial, self.app)
        Utils.wait_short()

