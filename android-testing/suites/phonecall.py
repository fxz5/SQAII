import json

from models.manager import DeviceManager
from utils.utils import AppManager, Utils


class PhoneCall:
    total_tests = 2
    passed_tests = 0
    failed_tests = 0

    def __init__(self, d, adb_only=False):
        # type: (DeviceManager, bool) -> None
        self.device = d.get_device()
        self.serial = d.get_serial()
        self.app = "Phone"
        self.package = "com.google.android.dialer"
        print "Initializing PhoneCall Component"

    def call_number_adb(self, use_json=False):
        if not use_json:
            # $ adb -s <serialno> shell am start -a android.intent.action.CALL -d tel:555-5555
            pass
        else:
            with open('data/phone.json') as json_file:
                data = json.load(json_file)
                phone_numbers = data['phone_numbers']
                for number in phone_numbers:
                    self.test_conditions()
                    Utils.wait_normal()
                    self.device(
                        resourceId="com.google.android.dialer:id/fab") \
                        .click()
                    print "Dialing: " + number
                    for digit in number:
                        self.__click_dial_number(digit)
                        Utils.wait_short()
                    self.device(
                        resourceId="com.google.android.dialer:id"
                                   "/dialpad_voice_call_button") \
                        .click()
                    Utils.wait_normal(True)
                    self.__end_call()

    def __end_call(self):
        """
        Ends phone call, even if it failed due to network not being available.
        """
        try:
            if self.device(text="Cancel", className="android.widget.Button")\
                    .exists:
                print "ending call with cancel"
                self.device(text="Cancel", className="android.widget.Button")\
                    .click()
            else:
                print "ending call with red button"
                self.device(
                    resourceId="com.google.android.dialer:id/incall_end_call")\
                    .click()
            Utils.wait_normal()
        except Exception as e:
            print str(e)

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

    def fail_test(self):
        pass

    def pass_test(self):
        pass
