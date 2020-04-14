from models.manager import DeviceManager
from utils.utils import Logger


class Suite:
    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    def __init__(self, d, logger):
        # type: (DeviceManager, Logger) -> None
        self.device = d.get_device()
        self.serial = d.get_serial()
        self.logger = logger
        self.app = ""
        self.package = ""
        self.module = ""

    def evaluate_module(self):
        print "Module has passed {}% of its tests ({} out of {})" \
            .format(self.passed_tests / self.total_tests * 100.0,
                    self.passed_tests, self.total_tests)

    def fail_test(self):
        self.failed_tests += 1
        self.total_tests += 1

    def pass_test(self):
        self.passed_tests += 1
        self.total_tests += 1

    def execute_suite(self):
        pass

    def test_conditions(self):
        pass
