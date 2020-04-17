from models.manager import DeviceManager
from utils.utils import Logger


class Suite:
    """
    This class makes every TestSuite class modular and compatible with the
    overall framework. This class abstracts the common behaviour of all
    independent Test Suites, and yet provides enough rigidity to provide
    powerful features such as logging, error reporting and on the go status.
    """
    total_tests = 0  # type: int  # amount of tests ran for a suite
    passed_tests = 0  # type: int  # amount of tests passed for a suite
    failed_tests = 0  # type: int  # amount of tests failed for a suite

    def __init__(self, d, logger):
        # type: (DeviceManager, Logger) -> None
        """
        Initializes main components of the suite, the Device, Serial and
        Logger references for all the suites to add.
        """
        self.device = d.get_device()
        self.serial = d.get_serial()
        self.logger = logger
        self.app = ""
        self.package = ""
        self.module = ""

    def evaluate_module(self):
        # type: () -> (int, int, int)
        """
        Performs a self evaluation of the module, presenting a console message
        with the percentage of passed tests, returning the amount of passed,
        failed and total tests executed for a module.
        """
        print "Module {} has passed {}% of its tests ({} out of {})" \
            .format(self.module,
                    float(self.passed_tests) / float(self.total_tests) * 100.0,
                    self.passed_tests, self.total_tests)
        return self.passed_tests, self.failed_tests, self.total_tests

    def fail_test(self):
        """
        This methods indicates an executed test failed, and proceeds to
        document the statistics on the run.
        """
        self.failed_tests += 1
        self.total_tests += 1

    def pass_test(self):
        """
        This methods indicates an executed test passed, and proceeds to
        document the statistics on the run.
        """
        self.passed_tests += 1
        self.total_tests += 1

    def execute_suite(self):
        """
        Executes all test cases in a suite.
        """
        pass

    def test_conditions(self):
        """
        Prepares the test conditions for all tests included in a test suite.
        """
        pass


class TestRun:
    """
    This is the wrapper object that handles all created TestSuites of type
    suites.suite.Suite and executed them in sequential order.
    """

    def __init__(self):
        """
        Initializes an empty test list.
        """
        self.tests = list()

    def add_suite(self, suite):
        # type: (Suite) -> None
        """
        Appends a Suite to the current queue of Test Suites to execute
        """
        self.tests.append(suite)

    def execute_all_suites(self):
        """
        Executes all Test Suites in self.tests and prints a Test Run summary
        at the end of the execution.
        """
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
