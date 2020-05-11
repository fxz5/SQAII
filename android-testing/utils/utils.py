# coding=utf-8
import time
from subprocess import check_call, call
import datetime
import os

from uiautomator import Device

from models.exceptions import CallFailed
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class CalculatorUtils:
    """
    Static methods that provide helpful and repetitive functionality to
    the calculator app
    """
    def __init__(self):
        pass

    @staticmethod
    def input_digit(device, digit):
        # type: (Device, str) -> None
        base = "com.google.android.calculator:id/"
        digit_map = {
            "1": "digit_1", "2": "digit_2", "3": "digit_3",
            "4": "digit_4", "5": "digit_5", "6": "digit_6",
            "7": "digit_7", "8": "digit_8", "9": "digit_9",
            "0": "digit_0", "+": "op_add", "-": "op_sub",
            "*": "op_mul", "/": "op_div", ".": "dec_point",
            "(": "lparen", ")": "rparen", "^": "op_pow"
        }
        resource_id = base + digit_map[digit]
        special_chars = ["(", ")", "^"]
        if digit in special_chars:
            CalculatorUtils.handle_advanced(device, resource_id)
        else:
            CalculatorUtils.click_button(device, base + digit_map[digit])

    @staticmethod
    def handle_advanced(device, res_id):
        # type: (Device, str) -> None
        if device(resourceId=res_id).exists:
            device(resourceId=res_id).click()
        else:
            device.swipe(device.width - 30, device.height * 2 / 3,
                         device.width / 2, device.height * 2 / 3, steps=20)
            device(resourceId=res_id).click()
            device.swipe(30, device.height * 2 / 3,
                         device.width - 30, device.height * 2 / 3, steps=20)

    @staticmethod
    def click_button(device, button):
        # type: (Device, str) -> None
        device(resourceId=button).click()

    @staticmethod
    def get_result(device):
        # type: (Device) -> str
        device(resourceId="com.google.android.calculator:id/eq").click()
        res = device(
            resourceId="com.google.android.calculator:id/result_final") \
            .info['text']
        res = res.replace(u'\u2212', '-')
        return res


class PhoneUtils:
    """
    Static methods that provide functionality for the Phone Android app.
    """

    def __init__(self):
        pass

    @staticmethod
    def process_phone_number(number):
        # type: (str) -> str
        """
        Strips away non numeric and phone characters from a phone number.
        """
        return number.replace(" ", "")

    @staticmethod
    def call_number(device, serial, number, use_adb=False):
        # type: (Device, str, str, bool) -> None
        """
        Calls a phone number in runtime and decides if it should use adb or
        UIAutomator, using the specified device.
        """
        if use_adb:
            check_call(
                ['adb', '-s', serial, 'shell', 'am', 'start',
                 '-a', 'android.intent.action.CALL', '-d',
                 'tel:' + str(number)
                 ])
            Utils.wait_normal()
        else:
            device(
                resourceId="com.google.android.dialer:id/fab") \
                .click()
            for digit in number:
                PhoneUtils.click_dial_number(device, digit)
                Utils.wait_short()
            device(
                resourceId="com.google.android.dialer:id"
                           "/dialpad_voice_call_button") \
                .click()
            Utils.wait_normal(True)

    @staticmethod
    def click_dial_number(device, digit):
        # type: (Device, str) -> None
        """
        Exclusive to UIAutomator, function clicks the desired digit in a
        specified device.
        """
        if digit == '+':
            device(
                text='0', resourceId="com.google.android.dialer:id"
                                     "/dialpad_key_number") \
                .long_click()
        elif digit == '#':
            device(
                className="android.widget.FrameLayout",
                resourceId="com.google.android.dialer:id/pound") \
                .click()
        elif digit == '*':
            device(
                className="android.widget.FrameLayout",
                resourceId="com.google.android.dialer:id/star") \
                .click()
        else:
            device(
                text=digit,
                resourceId="com.google.android.dialer:id"
                           "/dialpad_key_number") \
                .click()

    @staticmethod
    def end_call(device, use_adb=False):
        # type: (Device, bool) -> (bool, Exception)
        """
        Ends a call given an interface method (adb or UIAutomator) and returns
        a boolean indicating if the call was ended after being successful.
        """
        if use_adb:
            check_call([
                'adb', 'shell', 'input', 'keyevent', 'KEYCODE_ENDCALL'
            ])
            Utils.wait_short()
            return True, None
        else:
            try:
                if device(text="Cancel",
                          className="android.widget.Button") \
                        .exists:
                    device(text="Cancel",
                           className="android.widget.Button") \
                        .click()
                    raise CallFailed("mobile network unavailable")
                elif device(text="OK",
                            className="android.widget.Button") \
                        .exists:
                    device(text="OK",
                           className="android.widget.Button") \
                        .click()
                    raise CallFailed("network not available")
                else:
                    device(
                        resourceId="com.google.android.dialer:id/incall_end_call") \
                        .click()
                Utils.wait_normal()
                return True, None
            except Exception as e:
                return False, e

    @staticmethod
    def open_dialer(device):
        # type: (Device) -> None
        """
        Opens phone dialer
        """
        pass


class Utils:
    """
    Miscellaneous utilities for handling apps and wait times between actions.
    """

    def __init__(self):
        pass

    @staticmethod
    def wait_short():
        """
        Waits a short time of 0.5 seconds.
        """
        time.sleep(0.5)

    @staticmethod
    def wait_normal(extra=False):
        # type: (bool) -> None
        """
            Waits a normal time of 1 second. If the extra flag is true, time
            adds to 3 seconds.
        """
        if extra:
            time.sleep(3)
        else:
            time.sleep(1)

    @staticmethod
    def wait_long():
        """
        Waits for a long 10 second time.
        """
        time.sleep(10)

    @staticmethod
    def start_home(device_serial):
        # type: (str) -> None
        """
        Uses adb connection trough a specified serial so that the phone it
        forced to go to the home screen.
        """
        call(
            ['adb', '-s', device_serial, 'shell', 'input keyevent',
             'KEYCODE_WAKEUP']
        )
        Utils.wait_short()
        call(
            ['adb', '-s', device_serial, 'shell', 'input keyevent',
             'KEYCODE_HOME']
        )
        Utils.wait_short()


class WiFiUtils:
    def __init__(self):
        pass

    @staticmethod
    def switch_wifi(device, status):
        # type: (Device, bool) -> bool
        if status:
            if not WiFiUtils.check_wifi_status(device):
                WiFiUtils.toggle_wifi(device)
        else:
            if WiFiUtils.check_wifi_status(device):
                WiFiUtils.toggle_wifi(device)
        return WiFiUtils.check_wifi_status(device)

    @staticmethod
    def check_wifi_status(device, i=0):
        # type: (Device, int) -> bool
        device.open.quick_settings()
        time.sleep(0.3)
        return True if device(index=i, className="android.widget.Switch") \
                           .info['text'] == 'On' else False

    @staticmethod
    def toggle_wifi(device):
        # type: (Device) -> None
        """
        Toggles WiFi State from Quick Settings through a device connection.
        """
        print "opening quick settings"
        device.open.quick_settings()
        time.sleep(2)
        device(index=0, className="android.widget.Switch").child(
            className="android.widget.FrameLayout"
        ).click()
        time.sleep(0.3)


class AppUtils:
    """
    Utilities that allow to change an app's state. Open, closing and switching
    app logic is handled by this class.
    """

    def __init__(self):
        pass

    @staticmethod
    def open_app(device, device_serial, app_name):
        # type: (Device, str, str) -> None
        """
        Opens an app given a name from the home screen.
        """
        Utils.start_home(device_serial)
        device(text=app_name, className='android.widget.TextView').click()

    @staticmethod
    def kill_app(device_serial, package_name):
        # type: (str, str) -> None
        """
        Kills and app though adb and a device's serial connection. Removes
        app from the background given the package name.
        """
        check_call(
            ['adb', '-s', device_serial, 'shell', 'am', 'force-stop',
             package_name]
        )
        time.sleep(0.3)


class Logger:
    """
    Main structure and functions to interact and write to a logfile in csv
    format.
    """

    def __init__(self):
        # Session Initialized
        """
        Creates necessary directories and files for the logfile to work.
        """
        today = datetime.datetime.today()

        self.file = os.path.join("log",
                                 today.strftime("%Y-%m-%d") + "-" + "log.csv")
        if not os.path.exists('log'):
            os.makedirs('log')

    def log(self, device, start, module, test, status, error):
        # type: (str, datetime.datetime, str, str, str, str) -> None
        """
        Logs a message in the specified csv format to disk. default directory
        is log/
        """
        with open(self.file, "a+") as logfile:
            end = datetime.datetime.now()
            log_string = "\n{}, {}, {}, {}, {}, {}, {}, {}" \
                .format(
                device,
                start.strftime("%H:%M:%S"),
                end.strftime("%H:%M:%S"),
                end - start,
                module,
                test,
                status,
                error
            )
            logfile.write(log_string)
