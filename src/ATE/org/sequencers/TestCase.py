from abc import ABC


class TestCaseABC(ABC):
    def run(self):
        pass

    def set_instance_number(self, instance_number):
        self.instance_number = instance_number


class TestCaseBase(TestCaseABC):
    def __init__(self, call_values, limits, sbins, active_hardware):
        self.call_values = call_values
        self.limits = limits
        self.sbins = sbins
        self.active_hardware = active_hardware
