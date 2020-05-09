from models.manager import DeviceManager
from suites.suite import Suite
from utils.utils import Logger


class CalculatorSuite(Suite):
    def __init__(self, d, logger):
        # type: (DeviceManager, Logger) -> None
        print "Initializing PhoneCall Component"
        Suite.__init__(self, d, logger)
        self.app = "Calculator"
        self.package = "com.google.android.calculator"
        self.module = "Calculator"

    def execute_suite(self):
        pass
