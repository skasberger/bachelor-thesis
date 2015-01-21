

## Terms
- editor: person who edits an article and creates with this action a new revision 
- owner/author: person who contributed to the article and owns some tokens. mostly it is used to analyse the actual revision (who owns how many tokens)
- article: 
- paragraph: defined by two double line breaks in wiki code. a typical paragraph at the frontend/article. Headlines are also paragraphs.
- talk page:
- token: 
- add: first time add of new token
- delete: first time delete of tokens
- reintroduction: re-adds tokens already been added in the past
- redelete: re-deletes tokens already been deleted in the past
- undo = revert: action which undoes former actions. Undo delete or re-introduction. A revert here is not the same as in the Wikipedia community, where it stands for the revert of an whole edit/revision.
- supportive action = positive action
	- sums up re-introductions and re-deletes
	- Always in relation to another editor. 
- antagonistic action = negative action: 
	- sums up deletes and reverts
	- Always in relation to another editor. 

## Computation

### WikiwhoRelationships.py
- One token does not mean one action. One re-delete of an token for example is an supportive action to the former editor who deletes and also and antagonistic action to the one who introduced it after the past deletion.
- Looking for revisions in the past is not up to the first one. Checking re-deletes or re-introductions for example are only done in an time window backwards (very cost expensive).

**Vandalism**

The vandalism detection systems is set relatively soft on finding vandalism, so it does not filter out all damaging actions. The revisions with vandalism will get flagged with it and all metrics are set to zero. **This means for further analysis, revisions with vandalism should not be included in the computation**, cause it is skewing the distrubution of the data, especially for quantitatevily big ones. 


### analysis
the possibility space for an action is always the last revision. of course, the calcu

### Web
- ownership.html: plots top-k authors of article computed by authorship.py

### Talk Pages
They are only used to find the maintainance template

### Cisemcode
- code is prototype quality. erorrs can be inside.
- wikirandomnames downloads list of articlenames with number of revisions


## Sources
- [WikiWho](http://f-squared.org/wikiwho/)
- [GitHub](https://github.com/maribelacosta/wikiwho): old version!
