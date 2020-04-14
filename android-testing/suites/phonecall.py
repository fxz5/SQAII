import json
from subprocess import call, check_call
import datetime

from models.exceptions import CallFailed
from models.manager import DeviceManager
from suites.suite import Suite
from utils.utils import AppManager, Utils, Logger


class PhoneCall(Suite):
    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    def __init__(self, d, logger, adb_only=False):
        # type: (DeviceManager, Logger, bool) -> None
        print "Initializing PhoneCall Component"
        Suite.__init__(self, d, logger)
        self.adb = adb_only
        self.app = "Phone"
        self.package = "com.google.android.dialer"
        self.module = "PhoneCall"

    def execute_suite(self):
        self.call_number_adb(True)
        self.call_number_adb(False)

    def call_number_adb(self, use_json=False):
        test_case_name = "Phone Number Dialing"
        current_test_case = ""
        start_time = datetime.datetime.now()
        phone_numbers = []
        try:
            if not use_json:
                test_case_name += "-Manual"
                current_test_case = ""
                amount = int(input("how many numbers do you want to test? "))
                for i in range(amount):
                    number = input("enter phone number " + str(i) + ": ")
                    phone_numbers.append(number)
            else:
                test_case_name += "-JSON"
                with open('data/phone.json') as json_file:
                    data = json.load(json_file)
                    phone_numbers = data['phone_numbers']

            # Actual Calling of Numbers
            for number in phone_numbers:
                current_test_case = test_case_name + "-" + number
                if self.adb:
                    check_call(
                        ['adb', '-s', self.serial, 'shell', 'am', 'start',
                         '-a', 'android.intent.action.CALL', '-d',
                         'tel:' + str(number)
                         ])
                    Utils.wait_long()
                    self.__end_call()
                    self.logger.log(start_time, datetime.datetime.now(),
                                    self.module,
                                    current_test_case, "SUCCESS",
                                    "")
                    self.pass_test()
                else:
                    self.test_conditions()
                    Utils.wait_normal()
                    self.device(
                        resourceId="com.google.android.dialer:id/fab") \
                        .click()
                    for digit in number:
                        self.__click_dial_number(digit)
                        Utils.wait_short()
                    self.device(
                        resourceId="com.google.android.dialer:id"
                                   "/dialpad_voice_call_button") \
                        .click()
                    Utils.wait_normal(True)
                    self.__end_call()
                    self.logger.log(start_time, datetime.datetime.now(),
                                    self.module,
                                    current_test_case, "SUCCESS",
                                    "")
                    self.pass_test()
            self.evaluate_module()
        except Exception as e:
            end_time = datetime.datetime.now()
            self.logger.log(start_time, end_time, self.module,
                            current_test_case,
                            "ERROR", str(e) + e.message)
            self.fail_test()

    def __end_call(self):
        """
        Ends phone call, even if it failed due to network not being available.
        """
        try:
            if self.adb:
                call([
                    'adb', 'shell', 'input', 'keyevent', 'KEYCODE_ENDCALL'
                ])
            else:
                if self.device(text="Cancel",
                               className="android.widget.Button") \
                        .exists:
                    self.device(text="Cancel",
                                className="android.widget.Button") \
                        .click()
                    # raise CallFailed("mobile network unavailable")
                elif self.device(text="OK",
                                 className="android.widget.Button") \
                        .exists:
                    self.device(text="OK",
                                className="android.widget.Button") \
                        .click()
                    # raise CallFailed("network not available")
                else:
                    self.device(
                        resourceId="com.google.android.dialer:id/incall_end_call") \
                        .click()
                Utils.wait_normal()
        except Exception as e:
            raise e

    def __click_dial_number(self, digit):
        # type: (str) -> None
        """
        Determines the method used for phone dialing input.
        """
        if digit == '+':
            self.device(
                text='0', resourceId="com.google.android.dialer:id"
                                     "/dialpad_key_number") \
                .long_click()
        elif digit == '#':
            self.device(
                className="android.widget.FrameLayout",
                resourceId="com.google.android.dialer:id/pound") \
                .click()
        elif digit == '*':
            self.device(
                className="android.widget.FrameLayout",
                resourceId="com.google.android.dialer:id/star") \
                .click()
        else:
            self.device(
                text=digit,
                resourceId="com.google.android.dialer:id"
                           "/dialpad_key_number") \
                .click()

    def test_conditions(self):
        Utils.start_home(self.serial)
        AppManager.kill_app(self.serial, self.package)
        AppManager.open_app(self.device, self.serial, self.app)

