from subprocess import check_output
from uiautomator import Device


class DeviceManager:
    def __init__(self, device_index=1):
        # type: (int) -> None
        """Creates device Manager, object that handles a UIAutomator
        Device and Serial.

        index: the index a device appears in when running the bash command
        'adb devices'. If none is set, program will use the first device.
        """
        try:
            output = check_output(['adb', 'devices'])
            lines = output.splitlines()
            serial = lines[device_index].split()[0]
            self.device = Device(serial)
            self.serial = serial
        except Exception as e:
            print "can't find desired device: " + str(e)

    def get_device(self):
        """
        Returns the UIAutomator Device Instance.
        """
        try:
            if self.device:
                return self.device
            else:
                return
        except Exception as e:
            print str(e)
            return

    def get_serial(self):
        """
        Returns the UIAutomator Serial ID Instance.
        """
        if self.serial:
            return self.serial
        else:
            return
