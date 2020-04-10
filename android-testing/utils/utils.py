from subprocess import check_call, check_output, call


class PhoneUtils:
    """
    d: adb device object to perform actions on.
    """
    def __init__(self, d):
        self.device = d
