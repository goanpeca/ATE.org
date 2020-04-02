DEFINITION = {'WaferDiameter': None,
              'Bondpads': None,
              'DieSize': None,
              'DieRef': None,
              'Offset': None,
              'Scribe': None,
              'Flat': None,
              'BondpadTable': None, # template {1: ('bondpad1name', 100, 100, 90, 90),
                                    #           2: ('bondpad2name', -100, -100, 90, 90)},
              'Wafermap': None}     # {'rim': [(100, 80), (-80, -100)],
                                    # 'blank': [(80, 80)],
                                    # 'test_insert': [],
                                    # 'unused': []}}


UI_FILE = "MasksetWizard.ui"


from enum import Enum


class PadType(Enum):
    Digital = ('D', 'Digital')
    Analog = ('A', 'Analog')
    Mixed = ('M', 'Mixed')
    Power = ('P', 'Power')

    def __call__(self):
        return self.value


class PadDirection(Enum):
    Input = ('I', 'Input')
    Output = ('O', 'Output')
    Bidirectional = ('IO', 'Bidirectional')

    def __call__(self):
        return self.value
        

DEFAULT_ROW = [['', 0, 0, '100', '100', PadType.Analog()[0], PadDirection.Input()[0]]]