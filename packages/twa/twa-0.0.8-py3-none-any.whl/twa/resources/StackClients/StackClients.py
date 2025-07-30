
from twa import JPSGateway
class StackClients(JPSGateway):
    def __init__(self,**JGkwargs):
        super(StackClients, self).__init__(resName='StackClients',**JGkwargs)
    __init__.__doc__ = JPSGateway.__init__.__doc__.replace('        resName : str\n            name of the Java resource'\
            +'\n        jarPath : str\n            absolute path to the main jar file of the java resource\n','')