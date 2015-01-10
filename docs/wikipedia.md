

## Maintainance template
[Maintainance templates](http://en.wikipedia.org/wiki/Template:Maintained) are added in the talk page, not the article itself.

MediaWiki Shortcode: 
```{{Maintained|[[User talk:SomeInvolvedUser1|SomeInvolvedUser1]]<br />[[User talk:SomeInvolvedUser2|SomeInvolvedUser2]]}}```

## Export
**Download via [Special:Export](http://en.wikipedia.org/wiki/Special:Export):**
Settings
- without template tags
- all Revisionen
- save as file

[XML Schema 0.10 for Special:Export](http://www.mediawiki.org/xml/export-0.10.xsd)

The export function does not work as you may think. It stops creating the xml export after 1000 revisions. So your download scripts needs to grab the history by 1000 revisions pieces and merge it together.

### XML
- revision id 
	- unique 
	- ascending (revisions before 2002 sometimes are a exception to this rule caused by technical errors)
- editor id: is unique and persistent
- editor name: can change over time (unique?)


## Articles
- [Wikipedia:List of controversial issues](https://en.wikipedia.org/wiki/Wikipedia:List_of_controversial_issues)







