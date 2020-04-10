from uiautomator import device
from models.manager import DeviceManager
from suites.phonecall import PhoneCall
print("Hello, tester")

dev_man = DeviceManager(1)

phone_suite = PhoneCall(dev_man)

phone_suite.call_number_adb()
