'''
Created on Feb 20, 2013

@author: maribelacosta
'''

__author__ = "Maribel Acosta"
__copyright__ = "Copyright 2013"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Maribel Acosta"
__email__ = "maribel.acosta@kit.edu"
__status__ = "Development"

class Word(object):
    '''
    Implementation of the structure "Word", which includes the authorship information.
    '''


    def __init__(self):
        self.author_id = 0    # Identificator of the author of the word.
        self.author_name = '' # Username of the author of the word.
        self.revision = 0     # Revision where the word was included.
        self.value = ''       # The word (simple text).
        self.matched = False  #
        self.length = 0
        self.freq = []
        self.deleted = []
        self.internal_id = 0
        self.used = []
        
    
    def __repr__(self):
        return str(id(self))
    
    
    def to_dict(self):
        word = {}
        #word.update({'author' : {'id': self.author_id, 'username': self.author_name}})
        word.update({str(self.revision) : self.value})
    
        return word
    
