from datetime import datetime

from suites.suite import Suite
from utils.utils import Logger, WiFiUtils
from models.manager import DeviceUnit


class WiFiSettingsSuite(Suite):

    def __init__(self, d, logger, adb_only=False):
        # type: (DeviceUnit, Logger, bool) -> None
        print "Initializing WiFiSettings Component"
        Suite.__init__(self, d, logger, "WiFi Settings",
                       "Quick Settings", "com.google.android.dialer")

    def execute_suite(self):
        self.wfs_001()
        self.wfs_002()
        self.wfs_003()
        self.wfs_004()

    def wfs_001(self):
        start_time = datetime.now()
        current_test_case = "WFS_001"
        status = WiFiUtils.switch_wifi(self.device, False)
        if not status:
            WiFiUtils.switch_wifi(self.device, True)
            status = WiFiUtils.check_wifi_status(self.device)
            if status:
                self.pass_test(current_test_case, start_time)
                return
        self.fail_test(current_test_case, start_time, "WiFi is not On")

    def wfs_002(self):
        start_time = datetime.now()
        current_test_case = "WFS_002"
        status = WiFiUtils.check_wifi_status(self.device)
        if status:
            WiFiUtils.switch_wifi(self.device, True)
            status = WiFiUtils.check_wifi_status(self.device)
            if status:
                self.pass_test(current_test_case, start_time)
                return
        self.fail_test(current_test_case, start_time, "WiFi is not On")

    def wfs_003(self):
        start_time = datetime.now()
        current_test_case = "WFS_003"
        status = WiFiUtils.check_wifi_status(self.device)
        if status:
            status = WiFiUtils.switch_wifi(self.device, False)
            if not status:
                self.pass_test(current_test_case, start_time)
                return
        self.fail_test(current_test_case, start_time, "WiFi is not On")

    def wfs_004(self):
        start_time = datetime.now()
        current_test_case = "WFS_004"
        status = WiFiUtils.check_wifi_status(self.device)
        if not status:
            status = WiFiUtils.switch_wifi(self.device, False)
            if not status:
                self.pass_test(current_test_case, start_time)
                return
        self.fail_test(current_test_case, start_time, "WiFi is not On")

