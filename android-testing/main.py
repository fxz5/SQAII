from uiautomator import device
from models.manager import DeviceManager
from suites.phonecall import PhoneCall
from suites.wifi_settings import WiFiSettings
from utils.utils import Logger

dev_man = DeviceManager()
log = Logger()

phone_suite = PhoneCall(dev_man, log, False)
wifi_suite = WiFiSettings(dev_man)

# wifi_suite.turn_on_wifi()
phone_suite.call_number_adb(True)
