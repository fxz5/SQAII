import json
from subprocess import call, check_call
import datetime

from models.exceptions import CallFailed
from models.manager import DeviceManager
from suites.suite import Suite
from utils.utils import AppManager, Utils, Logger, PhoneUtils


class PhoneCall(Suite):
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

    def execute_suite(self):
        self.call_number(False)
        self.call_number(True)

    def call_number(self, use_json=False):
        test_case_name = "Phone Number Dialing"
        current_test_case = ""
        start_time = datetime.datetime.now()
        phone_numbers = []
        try:
            if not use_json:
                test_case_name += "-Manual"
                current_test_case = ""
                amount = int(input("how many numbers do you want to test? "))
                print "got here x2"
                for i in range(amount):
                    print "got here x2"
                    number = input("enter phone number " + str(i+1) + ": ")
                    phone_numbers.append(number)
            else:
                test_case_name += "-JSON"
                with open('data/phone.json') as json_file:
                    data = json.load(json_file)
                    phone_numbers = data['phone_numbers']

            # Actual Calling of Numbers
            for number in phone_numbers:
                current_test_case = test_case_name + "-" + str(number)
                if self.use_adb:
                    check_call(
                        ['adb', '-s', self.serial, 'shell', 'am', 'start',
                         '-a', 'android.intent.action.CALL', '-d',
                         'tel:' + str(number)
                         ])
                    Utils.wait_long()
                    success, e = PhoneUtils.end_call(self.device, self.use_adb)
                    if not success:
                        raise e
                else:
                    self.test_conditions()
                    Utils.wait_normal()
                    self.device(
                        resourceId="com.google.android.dialer:id/fab") \
                        .click()
                    for digit in str(number):
                        PhoneUtils.click_dial_number(self.device, digit)
                        Utils.wait_short()
                    self.device(
                        resourceId="com.google.android.dialer:id"
                                   "/dialpad_voice_call_button") \
                        .click()
                    Utils.wait_normal(True)
                    success, e = PhoneUtils.end_call(self.device, self.use_adb)
                    if not success:
                        raise e
                self.logger.log(start_time,
                                self.module,
                                current_test_case, "SUCCESS",
                                "")
                self.pass_test()
        except Exception as e:
            self.logger.log(start_time, self.module,
                            current_test_case,
                            "ERROR", str(e) + e.message)
            self.fail_test()

    def test_conditions(self):
        Utils.start_home(self.serial)
        AppManager.kill_app(self.serial, self.package)
        AppManager.open_app(self.device, self.serial, self.app)

