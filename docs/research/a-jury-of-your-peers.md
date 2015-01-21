## A Jury of Your Peers: Quality, Experience and Ownership in Wikipedia

Tries to find metrics for reverts and quality of contributions.

- Author: Halfaker, Kittur, Kraut, Riedl
- Date: 2015-01-21
- Status: finished
- Research type: full read

### Citations
- "However, the review process is robust and effective in practice: 42% of vandalistic contributions are repaired within one view and 70% within ten views [15]" [p. 1]
- "but Stvilia et al. explained that the open editing system constitutes an informal peer review that moderates the quality of articles. [16]" [p. 1]
- "To frame the hypotheses, let’s define a few terms. An edit is the act of making and saving changes to an article. A revision is a state in the history of an article — i.e., edits are transitions between revisions. A revert is a special kind of edit that restores the content of an article to a previous revision by removing the effects of intervening edits."[p. 2]
- In forming such a metric, we make the assumption that a good estimate of the quality of a contribution to Wikipedia is the lifespan of its words. Adler and Alfaro measured the number of seconds a word persists [1]. Priedhorsky et al. estimated the number of views of the article with a word in it [15]. We use a different metric: the number of editors who changed the article without removing the word. [p. 4]
- In order to gather those editors who will notice when their words are removed, we use the active editors estimate described in Section 3.3. Our hypothesis assumes that the more active editors who will notice that their words have been removed (in essence having their toes stepped on), the more likely it is that one of those editors will come back to the article to revert the change. [p. 7]
- Figure 6 shows the change in the probability that an edit will be reverted depending on how many active editors toes are stepped on by the edit. The figure shows linear progression of increasing probability of being reverted as the number of editors whose words were removed increases logarithmically [p. 7]
- depending on the number of active editors whose words are removed by the current edit, the probability of being reverted can rise 50% [p. 7]
- Our results strongly supports HYP Removing Established Words. The amount of time a word has persisted in an article predicts whether an edit that removes it will be reverted. This result supports the observation by Vi ́egas et al. of the first mover effect [19] [p8. ]
- We also found strong support for HYP Stepping on Toes, that the more active editors whose words are removed by an edit, the higher the probability will be that the edit will be reverted. he power of this feature does not depend in any way on the recent quality or experience of the editor. [p. 8]
- When evaluating HYP Editor Recent Quality, we found three pieces of evidence that support the assumption that word persistence (as measured by the persistent word revision per word metric) is, in fact, an approximation of the percieved quality of an editor’s contributions [p. 9]
- "Determining the an editor’s status as“active”in an article was less straightforward. Since the watchlists of editors are not included in the database snapshot provided by Wikimedia, we consider an editor as active in an article if that editor has made an edit to the article or its associated talk page within the **previous two weeks**." [p. 5]
- "here is an initial spike in the probability of being reverted for removing very young words. This uncharacteristic data point suggests that an edit that removes the words which were only just added by a previous edit is exceptionally likely to be reverted. This phenomenon could be explained by editors reacting negatively to the immediate removal of the words which they had just added." [p. 5]

### Notes
- seems not really strong paper in terms of assumptions and methods used. but was just shortly reading in. too many ideas in one short paper. too many hypotheses, and seems to weak testing of it.
- lifespan of words is a good measure for quality of metric
- stepping toes likely leads to reverts
- hyp 1 "Edits that remove established words are more likely to be reverted." is supported
- hyp 2 "Editors with a history of high quality contributions are less likely to be reverted." is supported
- hyp 3 "Editors who have been reverted recently are likely to continue to be reverted." is supported
- hyp 4 "Editors with more experience are less likely to be reverted." is partly supported
- hyp 5 "Editors who cite policy often are less likely to be reverted." is not supported
- hyp 6 "Edits that remove the words of active editors are more likely to be reverted." is 

### Sum Up
good written paper. lots of description about the metrics and their limitations. hard to understand for non wikipedia researcher i gues (lot of terms => pre-existing knowledge necessary, very dense)

