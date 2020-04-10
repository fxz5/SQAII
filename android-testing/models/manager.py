from subprocess import check_output
from uiautomator import Device


class DeviceManager:
    def __init__(self, device_index):
        output = check_output(['adb', 'devices'])

        lines = output.splitlines()
        serial = lines[device_index].split()[0]
        print ("1st Device on List = {}".format(serial))

        self.device = Device(serial)
        self.serial = serial
        print self.device

    def get_device(self):
        if self.device:
            return self.device
        else:
            return

    def get_serial(self):
        if self.serial:
            return self.serial
        else:
            return
