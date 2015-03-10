'''
Created on Feb 20, 2013

@author: Maribel Acosta
@author: Andriy Rodchenko
'''

__author__ = "Maribel Acosta"
__copyright__ = "Copyright 2013"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Maribel Acosta"
__email__ = "maribel.acosta@kit.edu"
__status__ = "Development"

class Sentence(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.hash_value = ''        # The hash value of the sentence.
        self.value = ''             # The sentence (simple text).
        self.splitted = []          # List of strings composing the sentence.
        self.words = []             # List of words in the sentence. It is an array of Word. 
        self.matched = False        # Flag.
    
    def __repr__(self):
        return str(id(self))
    
    def to_dict(self):
        sentence = {}
        sentence.update({'hash' : self.hash_value})
        
        obj_words = []
        for word in self.words: 
            obj_words.append(repr(word))

        sentence.update({'obj' : obj_words})
        return sentence
        
    
    