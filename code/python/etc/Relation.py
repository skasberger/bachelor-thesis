'''
Created on Jun 14, 2014

@author: maribelacosta
'''

__author__ = "Maribel Acosta"
__copyright__ = "Copyright 2014"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Maribel Acosta"
__email__ = "maribel.acosta@kit.edu"
__status__ = "Development"

class Relation(object):
    """The summary line for a class docstring should fit on one line.
        
    The __init__ method may be documented in either the class level
    docstring, or as a docstring on the __init__ method itself.

    Either form is acceptable, but the two should not be mixed. Choose one
    convention to document the __init__ method and be consistent with it.

    Do not include the self parameters in the ``Args`` section

    If the class has public attributes, they should be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section.

    Args:
        msg (str): Human readable string describing the exception.
        code (int, optional): Error code, defaults to 2.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (list of str): Description of `attr2`.
        attr3 (int): Description of `attr3`.
    """
    def __init__(self):
        """
        DESCRIPTION
            
        :Parameters:
            NAME : TYPE
                DESCRIPTIOIN
                
        :Return:
            DESCRIPTION
        """
        self.revision = ''     # Wikipedia revision id
        self.author = ''       # Author of the revision
        self.length = 0        # Total length of 'revision'
        self.total_tokens = 0
        
        self.added = 0         # Number of new tokens.
        
        self.deleted = {}      # Given a revision, the number of tokens deleted from that revision
        self.reintroduced = {} # Given a revision, the number of tokens reintroduced from that revision 
        self.redeleted = {}    #
        self.revert = {} 
        
        self.self_reintroduced = {}
        self.self_redeleted = {}
        self.self_deleted = {}
        self.self_revert = {}

