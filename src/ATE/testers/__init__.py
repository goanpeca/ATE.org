class SCT_testers(object):
    '''
    This class manages the testers via zero-conf
    #TODO: this should later on move to the SCT plugin
    '''
    def __init__(self):
        self.testers = ["Tom's MiniSCT", "Achim's MiniSCT", "Sigi's MiniSCT", "MaxiSCT in Lab"]
    
    def rescan(self):
        '''
        this method rescan's the zeroconf network for miniSCT's
        '''
    
    def report(self):
        '''
        this method reports the latest list of MiniSCT's
        '''
        return self.testers