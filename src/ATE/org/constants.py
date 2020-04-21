from enum import Enum


class TableIds(Enum):
    Flow = 1
    Definition = 2
    Hardware = 3
    Maskset = 4
    Device = 5
    Product = 6
    Package = 7
    Die = 8
    Test = 9

    def __call__(self):
        return self.value
