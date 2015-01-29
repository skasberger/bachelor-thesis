
- [WikiWho](http://f-squared.org/wikiwho/)
- [GitHub](https://github.com/maribelacosta/wikiwho): old version!

## WikiwhoRelationships.py
- One token does not mean neccessarily one action. Different relations with different editors can occur. 

**Vandalism**
The vandalism detection systems is set relatively soft on finding vandalism, so it does not filter out all damaging actions. The revisions with vandalism will get flagged with it and all data are set to zero. **This means for further analysis, revisions with vandalism should not be included in the computation**, cause it is skewing the distrubution of the data. 

## Wikistats.py
Talk Pages are only used to find the maintainance template

### Improvements
- extend existing class model?? revisions, order, relation, and so on
	- detect vandalism
	- calculate metrics
	- define unique id's

### Data
- the counting of the revision starts with 1

## analysis.py

### Todo
- auto update wikipages.csv, metadata.json and dataprotocol.json with dates of plots, computation and analysis

### Data

## Web
- ownership.html: plots top-k authors of article computed by authorship.py


## Cisemcode
- code is prototype quality. erorrs can be inside.
- wikirandomnames downloads list of articlenames with number of revisions
- regex are not perect. should be checked.


