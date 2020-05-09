from subprocess import check_output
from typing import Optional

from uiautomator import Device


class DeviceUnit:
    device = None
    serial = ""

    def __init__(self, device, serial):
        # type: (Device, str) -> None
        self.device = device
        self.serial = serial

    def __str__(self):
        return self.serial

    def get_device(self):
        return self.device

    def get_serial(self):
        return self.serial


class DeviceManager:
    def __init__(self, *args):
        # type: (*int) -> None
        """Creates device Manager, object that handles a UIAutomator
        Device and Serial.

        index: the index a device appears in when running the bash command
        'adb devices'. If none is set, program will use the first device.
        """
        self.devices = list()
        try:
            output = check_output(['adb', 'devices'])
            lines = output.splitlines()
            for index in args:
                try:
                    serial = lines[index].split()[0]
                except Exception as e:
                    print "Could not add device because: " + str(e)
                    continue
                self.devices.append(DeviceUnit(Device(serial), serial))
        except Exception as e:
            print "can't find desired device: " + str(e)

    def show_devices(self):
        s = "Managing these devices:\n"
        for device in self.devices:
            s += "\n" + str(device)
        print s

    def get_device(self, index):
        # type: (int) -> Optional[Device]
        """
        Returns the UIAutomator Device Instance.
        """
        try:
            if self.devices[index]:
                return self.devices[index].device
            else:
                return
        except Exception as e:
            print str(e)
            return

    def get_serial(self, index):
        # type: (int) -> Optional[str]
        """
        Returns the UIAutomator Device Instance.
        """
        try:
            if self.devices[index]:
                return self.devices[index].serial
            else:
                return
        except Exception as e:
            print str(e)
            return
