Bachelor Thesis Stefan Kasberger
==============================

The bachelor thesis tries to find characteristics of editors on Wikipedia. Main focus is to look on how different communities evolve over time around the process of collaboratively building knowledge through agreeing/disagreeing. Additionaly, it is also planed to publish at the end a paper in a journal.

The Bachelor Thesis is part of the [Environmental Systems Science with focus on Geography](http://umweltsystemwissenschaften.uni-graz.at/) study at [Karl Franzens University of Graz](http://uni-graz.at/). The thesis itself will be done at [GESIS Institute](http://www.gesis.org/) in Cologne, as part of the Data Science team of Markus Strohmaier. 

- Institute: [GESIS Computational Social Sciences - Team Data Science](http://www.gesis.org/en/institute/gesis-scientific-departments/computational-social-science/)
- Advisor: [Fabian Flöck](https://twitter.com/ffloeck) and [Markus Strohmaier](http://twitter.com/mstrohm)
- Status: Explorative
- Start: 10. November 2014
- Language: English
- [Webpage](http://openscienceasap.org/research/bachelor-thesis-stefan-kasberger) 

**The content of my bachelor thesis is under daily changes and some scripts and data exports must be prepared or checked in terms of copyright before adding it to the repo. This will take some time, thanks for your understanding.**

## Openness
### Used software
**Scripts**
- WikiWho: GPL v2
- Cisemcode: GPL v2

**Applications**
- [Python](https://www.python.org/) and [iPython](http://ipython.org/) for data analysis and visualization
	- [wmf]()
	- [virtualenv](https://virtualenv.pypa.io): ```source venv/bin/activate```
- [Sublime](http://www.sublimetext.com/) as text editor for coding
- [Git](http://git-scm.com/) and [GitHub](http://github.com/) for software versioning
- [Zotero](https://www.zotero.org/) with firefox plugin for citation management
- [LaTeX](http://www.latex-project.org/) for writting
- [Wordpress](https://wordpress.org/) for blogging regular outcomes at [openscienceASAP.org](http://openscienceasap.org)
- [orgmode](http://orgmode.org/) and [emacs](http://www.gnu.org/software/emacs/) for project management
- [html 2 markdown editor](http://dillinger.io/) for converting markdown to html

### Used data
Open Data from following data repositories were used:
- [Wikipedia EN](https://en.wikipedia.org/wiki/Main_Page) via [Export Special Page](https://en.wikipedia.org/w/index.php?title=Special:Export)

## USAGE
First you need to adapt the wikipages_server.csv in ```data/csv``` to your needs. title, maintainer id and maintainer name are mandatory. To enable download write ```yes``` in the 'download' column, same for compute_stats and analysis. Then you only have to execute the following command inside ```code/python/```:
```
python wikibuild.py -a 'William_McKendree'

```

## STRUCTURE
- [README.md](README.md): Overview of repository

