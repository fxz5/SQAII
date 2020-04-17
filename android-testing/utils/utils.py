import time
from subprocess import check_call, call
import datetime
import os

from uiautomator import Device

from models.exceptions import CallFailed


class PhoneUtils:
    """
    Static methods that provide functionality for the Phone Android app.
    """

    def __init__(self):
        pass

    @staticmethod
    def click_dial_number(device, digit):
        # type: (Device, str) -> None
        """
        Uses UIAutomator to click each digit of a phone number.
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
            return True
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
                return True
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
    def __init__(self):
        pass

    @staticmethod
    def wait_short():
        time.sleep(0.5)

    @staticmethod
    def wait_normal(extra=False):
        if extra:
            time.sleep(3)
        else:
            time.sleep(1)

    @staticmethod
    def wait_long():
        time.sleep(10)

    @staticmethod
    def start_home(device_serial):
        call(
            ['adb', '-s', device_serial, 'shell', 'input keyevent',
             'KEYCODE_WAKEUP']
        )
        Utils.wait_short()

        # Go home
        call(
            ['adb', '-s', device_serial, 'shell', 'input keyevent',
             'KEYCODE_HOME']
        )
        Utils.wait_short()


class AppManager:
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
        Kills and app from the background given the package name.
        """
        check_call(
            ['adb', '-s', device_serial, 'shell', 'am', 'force-stop',
             package_name]
        )
        time.sleep(0.3)


class Logger:

    def __init__(self):
        # Session Initialized
        today = datetime.datetime.today()

        self.file = os.path.join("log",
                                 today.strftime("%Y-%m-%d") + "-" + "log.csv")
        if not os.path.exists('log'):
            os.makedirs('log')

    def log(self, start, module, test, status, error):
        # type: (datetime.datetime,str, str, str, str) -> None
        with open(self.file, "a+") as logfile:
            end = datetime.datetime.now()
            log_string = "\n{}, {}, {}, {}, {}, {}, {}" \
                .format(
                    start.strftime("%H:%M:%S"),
                    end.strftime("%H:%M:%S"),
                    end-start,
                    module,
                    test,
                    status,
                    error
                )
            logfile.write(log_string)
