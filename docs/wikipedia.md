
## Maintained Template
[Maintained templates](http://en.wikipedia.org/wiki/Template:Maintained) are added in the talk page, not the article itself.

MediaWiki Shortcode: 
```
{{Maintained|[[User talk:SomeInvolvedUser1|SomeInvolvedUser1]]<br />[[User talk:SomeInvolvedUser2|SomeInvolvedUser2]]}}
```

## Get Data
### MediaWiki API
* [API Main Page](https://www.mediawiki.org/wiki/API:Main_page)
* [API Reference](https://en.wikipedia.org/w/api.php)
* [API Properties](https://www.mediawiki.org/wiki/API:Properties)
* Endpoint: [http://en.wikipedia.org/w/api.php](http://en.wikipedia.org/w/api.php

#### Python
[Client Code](https://www.mediawiki.org/wiki/API:Client_code#Python)
[wikitools](https://github.com/alexz-enwp/wikitools)
[wikipedia Package	](https://pypi.python.org/pypi/wikipedia/)


#### Queries
**format**
- format=json

**action**
- [action=query](https://en.wikipedia.org/w/api.php?action=help&modules=query)
- [action=userdailycontribs](https://en.wikipedia.org/w/api.php?action=help&modules=userdailycontribs): Get the total number of user edits, time of registration, and edits in a given timeframe.

**prop**
- [prop=info](https://en.wikipedia.org/w/api.php?action=help&modules=query%2Binfo)
	- inprop=protection: List the protection level of each page.
	- inprop=watchers: The number of watchers, if allowed.
	- inprop=talkid: The page ID of the talk page for each non-talk page.
	- inprop=readable: Whether the user can read this page.
- [prop=templates](https://en.wikipedia.org/w/api.php?action=help&modules=query%2Btemplates)
	- tltemplates: Only list these templates. Useful to check whether a certain template is transcluded in a certain page
- [prop=contributors](https://en.wikipedia.org/w/api.php?action=help&modules=query%2Bcontributors)
	- pclimit: Maximum number of contributors to list. No more than 500 (5000 for bots) allowed. Default: 10
	- pccontinue: When more results are available, use this to continue.
	- pcrights: Limit users to those having given right(s).
- [prop=revisions](https://en.wikipedia.org/w/api.php?action=help&modules=query%2Brevisions)
	- rvprop
		- ids: 
		- userid: 
		- user: 
	- rvlimit: The maximum number of revisions to return. Use the string "max" to return all revisions (subject to being broken up as usual, using continue). Limited by query limits defined in ApiBase, which equals 500 for users and 5000 for bots. 
	- rvuser: Only list revisions made by this user

**list**
- [list=embeddedin](https://www.mediawiki.org/wiki/API:Embeddedin)
	- eititle: List pages including this title. The title need not exist
	- eilimit: Maximum amount of pages to list No more than 500 (5000 for bots) allowed. (Default: 10)
	- eicontinue: Used to continue a previous request
Example: https://en.wikipedia.org/w/api.php?action=query&list=embeddedin&eititle=Template:Maintained&eilimit=20
- list=random

### SQL Queries - Quarry
* [Quarry](http://quarry.wmflabs.org/)
* [Manual:database layout](https://www.mediawiki.org/wiki/Manual:Database_layout)

### Special:Export XML Export
**Download via [Special:Export](http://en.wikipedia.org/wiki/Special:Export):**

Settings
- without template tags
- all Revisionen
- save as file

The export function has some limitations. It stops creating the XML export after 1000 revisions. So your download scripts needs to grab the history in 1000 revision pieces and append it after downloading.

### Wikipedia XML Schema
[XML Schema 0.10 for Special:Export](http://www.mediawiki.org/xml/export-0.10.xsd)

**data**
- revision id 
	- unique 
	- ascending (revisions before 2002 sometimes are a exception to this rule caused by technical errors)
- editor id: is unique and persistent
- editor name: can change over time (unique?)


## Articles
- [Wikipedia:List of controversial issues](https://en.wikipedia.org/wiki/Wikipedia:List_of_controversial_issues)


## Critical points
- Wikipedia user and visitor are not representative for broader society: north/south, women/men, young/old, educated/uneducated, techis/dau's, 
- share of migrants and diversity of ethnics
- Do Bots play a role?

## Sources
* [Effect of various protection levels](https://en.wikipedia.org/wiki/Wikipedia:Pending_changes#Effect_of_various_protection_levels)





