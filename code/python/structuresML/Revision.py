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

class Revision(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.id = 0                  # Fake sequential id. Starts in 0.
        self.wikipedia_id = 0        # Wikipedia revision id.
        self.contributor_id = 0;     # Id of the contributor who performed the revision.
        self.contributor_name = ''   # Name of the contributor who performed the revision.
        self.contributor_ip = ''     # IP of the contributor who performed the revision.
        self.paragraphs = {}         # Dictionary of paragraphs. It is of the form {paragraph_hash : [Paragraph]}.
        self.ordered_paragraphs = [] # Ordered paragraph hash.
        self.length = 0              # Content length (bytes).
        self.content = ''            #TODO: this should be removed. Just for debugging process.
        self.ordered_content = []    #TODO: this should be removed. Just for debugging process.
        self.total_tokens = 0        # Number of tokens in the revision.
        self.timestamp = 0
        
    def __repr__(self):
        return str(id(self))
    
    def to_dict(self):
        revision = {}
        #json_revision.update({'id' : revisions[revision].wikipedia_id})
        #revision.update({'author' : {'id' : self.contributor_id, 'name' : self.contributor_name}})
        #json_revision.update({'length' : revisions[revision].length})
        #json_revision.update({'paragraphs' : revisions[revision].ordered_paragraphs})
        revision.update({'obj' : []})
        for paragraph_hash in self.ordered_paragraphs:
            p = []
            for paragraph in self.paragraphs[paragraph_hash]:
                p.append(repr(paragraph))
            revision['obj'].append(p)
            
        return revision
    