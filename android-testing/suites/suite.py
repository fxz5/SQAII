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
        print "Module {} has passed {}% of its tests ({} out of {})" \
            .format(self.module,
                    float(self.passed_tests) / float(self.total_tests) * 100.0,
                    self.passed_tests, self.total_tests)
        return self.passed_tests, self.failed_tests, self.total_tests

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


class TestRun:

    def __init__(self):
        self.tests = list()

    def add_suite(self, suite):
        # type: (Suite) -> None
        self.tests.append(suite)

    def execute_all_suites(self):
        tp = 0
        tf = 0
        tt = 0
        for i in self.tests:
            i.execute_suite()
            p, f, t = i.evaluate_module()
            tp += p
            tf += f
            tt += t

        print "Test finished with {}% of its tests ({} out of {})" \
            .format(float(tp) / float(tt) * 100.0,
                    tp, tt)

