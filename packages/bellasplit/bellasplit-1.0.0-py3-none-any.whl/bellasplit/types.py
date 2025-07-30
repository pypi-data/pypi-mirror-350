from bellameta.types import BellametaType

from bellasplit import constants

class Mode(BellametaType, values=constants.MODE):
    '''
    Class providing consistent typing for train, val and test.
    '''

    pass

class Splitname(BellametaType, values=constants.SPLITNAME):
    '''
    Class registering the names of valid splits, use .yaml file to extend this.
    '''

    pass
