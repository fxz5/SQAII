from subprocess import check_call, check_output, call
import time


class PhoneUtils:
    """
    d: adb device object to perform actions on.
    """

    def __init__(self, d):
        self.device = d


class AppManager:
    def __init__(self):
        pass

    @staticmethod
    def open_app(device, app_name):
        call(
            ['adb', '-s', device.get_serial(), 'shell', 'input keyevent', 'KEYCODE_WAKEUP']
        )
        time.sleep(1)

        # Go home
        call(
            ['adb', '-s', device.get_serial(), 'shell', 'input keyevent', 'KEYCODE_HOME']
        )
        time.sleep(1)
        # Menu_click
        d = device.get_device()
        d(text=app_name, className='android.widget.TextView').click()
