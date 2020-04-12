from subprocess import check_call, check_output, call
import time

from uiautomator import Device


class PhoneUtils:
    """
    d: adb device object to perform actions on.
    """

    def __init__(self, d):
        self.device = d


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
