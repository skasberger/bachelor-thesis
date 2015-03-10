#!/bin/env python2
# -*- coding: utf-8 -*-
"""
Generates the basic WikiWho metrics and saves them in JSON. 
"""

import os
from copy import deepcopy
import operator
from sys import argv, exit
import getopt
import re
import datetime
import json
import io
from structuresML.Revision import Revision
from wmf import dump
import WikiwhoRelationships

__author__ = "Maribel Acosta, Fabian Floeck, and Stefan Kasberger"
__copyright__ = "Copyright 2015"
__license__ = "MIT"
__version__ = "3.0.0"
__maintainer__ = "Stefan Kasberger"
__email__ = "mail@stefankasberger.at"
__status__ = "Production"

def getArticleStats(revisions, order, relations, tags, talk_pages):
	"""
	compute metrics
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
	""" 
	# data for whole article
	stats = []
	editorsTokensAbs = {}
	editors = {}
	all_authors = set([])
	top_authors = {}
	all_editors = []
	outgoing_negative_actions = {}
	incoming_negative_actions = {}
	self_reintroductions = []
	self_supports = []
	all_antagonized_editors = []
	all_supported_editors = []
	
	prev_revision = None
	k = 5
	totalEditCount = 0
	window1 = 50
	counterRevisions = 0

	# Graph structures.
	edges_rev = {}    
	nodes = {}
	# graph metrics
	ordered_editors = []
	ordered_not_vandalism = []
	all_antagonized_editors = []
	all_supported_editors = []
	data_graph = []
	contributors_rev = {}


	window1 = GetWindowSize()


	# loop over every revision
	for (rev_id, vandalism) in order:
		
		# VANDALISM

		if (vandalism):
			# this must stand as the first call in the for loop, cause else a not existing revision id for the vandalized revision will throw an KeyError whan assigning it
			data = {
				'revision-id' : revision_id, 
				'revision-count': counterRevisions,
				'number-tokens': 0,
				'number-authors': 0,
				'length-change' : 0, 
				'edit-rapidness': 0, 
				'editor-name': editor_name,
				'editor-id': editor_id,
				#'authors': dataAuthors,
				#'editors': editorsTokensAbs,
				'talkpage-edits': talkPageEdits, 
				'window1-size': 0,
				'total-actions': 0, 
				'tokens-added': 0, 
				'tokens-deleted': 0,
				'tokens-redeleted': 0,
				'tokens-reintroduced': 0,
				'tokens-reverted': 0,
				'tokens-self-deleted': 0,
				'tokens-self-reverted': 0,
				'tokens-self-redeleted': 0,
				'tokens-self-reintroduced': 0,
				'gini-ownership':0, 
				'gini-editorship': 0, 
				'gini-editorship-w1': 0,
				'gini-OutNegActions': 0,
				'gini-InNegActions': 0, 
				'antagonistic-actions': 0, 
				'antagonizedEditorsAvgW1' : 0,
				'antagonized-editors': 0,
				'numAntagonizedEditors': 0, 
				'supportive-actions': 0,
				'supported-editors': 0,
				'number-supported-editors': 0, 
				'supported-editors-w1' : 0,
				'self-reintroduction-ratio': 0,
				'self-reintroduction-ratio-w1':0, 
				'self-support-ratio': 0,
				'self-support-ratio-w1': 0, 
				'self-support-actions': 0, 
				'tag-maintained': 0, 
				'tag-NPOV': 0, 
				'tag-goodArticle': 0, 
				'tag-featuredArticle': 0,
				'tag-disputed': 0,
			}
			data_graph.append(
				{
					'revision': revision, 
			        'distinct_editors': 0, 
			        'deletion_edges_contributors_w': 0,
			        'deletion_outgoing_ratio': 0,
			        'deletion_incoming_ratio': 0,
			        'deletion_reciprocity': 0,
			        'deletion_weight_avg': 0,
			        'bipolarity' : 0
				}
			)
			stats.append(data)
			counterRevisions += 1
		else:     

			# VARIABLES

			# revision specific data
			authors = [] # list with all authors of revision
			data = {} # revision related data
			dataAuthors = {} # authors related data

			talkPageEdits = 0 # number of talk page edits since last edit
			positiveActions = 0
			negativeActions = 0
			maintained = 0
			npov = 0
			good_article = 0
			featured_article = 0
			disputed = 0 

			# BASIC SETS
			revision = revisions[rev_id]
			revision_id = revision.wikipedia_id
			relation = relations[revision_id]

			authors = getAuthorshipDataFromRevision(revision) # returns list with all authors for every token
			
			all_authors.update(set(authors))
			editor_name = revision.contributor_name
			editor_id = revision.contributor_id
			tokens_added = relation.added
			tokens_deleted = sum(relation.deleted.values())
			tokens_redeleted = sum(relation.redeleted.values())
			tokens_reintroduced = sum(relation.reintroduced.values())
			tokens_reverted = sum(relation.revert.values())
			tokens_selfdeleted = sum(relation.self_deleted.values())
			tokens_selfreverted = sum(relation.self_revert.values())
			tokens_selfredeleted = sum(relation.self_redeleted.values())
			tokens_selfreintroductions = sum(relation.self_reintroduced.values())
			
			# Compute authorship distribution information
			authorsTokensRel, authorsTokensAbs = getAuthorsTokenCount(authors, revision.total_tokens) # relative and absolute number of tokens for every author
			sortedAuthorsTokensAbs = sorted(authorsTokensAbs.iteritems(), key=operator.itemgetter(1))
			totalTokensCount = len(authors)
			totalAuthorCountAS = len(sortedAuthorsTokensAbs)

			#Compute top k contributors in this revision.
			top_k = sorted(authorsTokensAbs.iteritems(), key=operator.itemgetter(1), reverse=True)[:k]
			top_authors.update({revision_id : dict(top_k)})

			# Compute editorship distribution information
			all_editors.append(editor_id)
			editorsTokensAbs = getAuthorsTokenCount(all_editors)
			sortedEditorsTokensAbs = sorted(editorsTokensAbs.iteritems(), key=operator.itemgetter(1))
			
			# editorship with window1
			editorsTokensAbs_w1 = None
			if (len(all_editors) >= window1):
				editorsTokensAbs_w1 = getAuthorsTokenCount(all_editors[len(all_editors) - window1:])
				sortedEditorsTokensAbs_w1 = sorted(editorsTokensAbs_w1.iteritems(), key=operator.itemgetter(1))

			# Compute length change in percentage
			if (prev_revision == None):
				lengthChange = 0
			else:
				lengthChange = ((revision.total_tokens - revisions[prev_revision].total_tokens) / float(revisions[prev_revision].total_tokens)) 
				
			# Compute edit rapidness
			if (prev_revision == None):
				editRapidness = 0
			else:
				editRapidness = (revision.timestamp - revisions[prev_revision].timestamp) / 3600.0

			# GINI OWNERSHIP
			# Compute wikigini: V1
			i = 1
			res = 0
			for tup in sortedAuthorsTokensAbs:
				res = res + (i * tup[1])
				i = i + 1        
			wikiGini = ((2.0 * res)/ (len(sortedAuthorsTokensAbs) * totalTokensCount)) - ((len(sortedAuthorsTokensAbs) + 1.0   ) / len(sortedAuthorsTokensAbs))  
			
			# ANTAGONISTIC ACTIONS

			# antagonized_editors: Revert actions + delete actions in revision (distinct editors)
			antagonized_editors = {}
			for elem in relation.revert.keys():
				antagonized_editors.update(relation.revert)
			for elem in relation.deleted.keys():
				antagonized_editors.update(relation.deleted)   
				
			all_antagonized_editors.appendgetUsernamegetUsername(len(antagonized_editors))
			
			antagonized_editors_avg_w1 = 0
			if (len(all_antagonized_editors) >= window1):
				antagonized_editors_avg_w1 = sum(all_antagonized_editors[len(all_antagonized_editors)-window1:]) / float(window1)
			
			# antagonistic_actions: Revert actions + delete actions in revision (number of tokens)    
			antagonistic_actions = 0
			for elem in relation.revert.keys():
				antagonistic_actions = antagonistic_actions + relation.revert[elem]
			for elem in relation.deleted.keys():
				antagonistic_actions = antagonistic_actions + relation.deleted[elem]
				
			# SUPPORTIVE ACTIONS

			# supported_editors: reintroductions + redeletes (distinct editors)
			supported_editors = {}
			for elem in relation.reintroduced.keys():
				supported_editors.update(relation.reintroduced)
			for elem in relation.redeleted.keys():
				supported_editors.update(relation.redeleted)
			 
			all_supported_editors.append(len(supported_editors))
			
			supported_editors_avg_w1 = 0
			if (len(all_supported_editors) >= window1):
				supported_editors_avg_w1 = sum(all_supported_editors[len(all_supported_editors)-window1:]) / float(window1)
				
			# supportive actions:  reintroductions + redeletes (number of tokens)
			supportive_actions = 0
			for elem in relation.reintroduced.keys():
				supportive_actions = supportive_actions + relation.reintroduced[elem]
			for elem in relation.redeleted.keys():
				supportive_actions = supportive_actions + relation.redeleted[elem]
				
			# TOTAL TOKEN ACTIONS

			tokenActions = 0
			for elem in relation.deleted.keys():
				tokenActions += relation.deleted[elem]
			for elem in relation.reintroduced.keys():
				tokenActions += relation.reintroduced[elem]
			for elem in relation.redeleted.keys():
				tokenActions += relation.redeleted[elem]
			for elem in relation.revert.keys():
				tokenActions += relation.revert[elem]
			tokenActions += tokens_added
			
			# GINI EDITORSHIP
			i = 1
			res = 0
			for tup in sortedEditorsTokensAbs:
				res = res + (i * tup[1])
				i = i + 1        
			giniEditorship = ((2.0 * res)/ (len(sortedEditorsTokensAbs) * len(all_editors))) - ((len(sortedEditorsTokensAbs) + 1.0   ) / len(sortedEditorsTokensAbs))  
			
			# Compute gini editorship with window 1 --> OBSOLETE, NOT USED
			giniEditorship_w1 = 0
			if (editorsTokensAbs_w1 != None):
				i = 1
				res = 0
				for tup in sortedEditorsTokensAbs_w1:
					res = res + (i * tup[1])
					i = i + 1        
				giniEditorship_w1 = ((2.0 * res)/ (len(sortedEditorsTokensAbs_w1) * window1)) - ((len(sortedEditorsTokensAbs_w1) + 1.0   ) / len(sortedEditorsTokensAbs_w1))  
			
			# Computing gini of outgoing negative actions
			if (editor_name in outgoing_negative_actions.keys()):
				outgoing_negative_actions.update({editor_name: outgoing_negative_actions[editor_name] + antagonistic_actions}) 
			else:
				outgoing_negative_actions.update({editor_name: antagonistic_actions}) 
			
			sortedNegDistSum = sorted(outgoing_negative_actions.iteritems(), key=operator.itemgetter(1))        
			i = 1
			res = 0
			for tup in sortedNegDistSum:
				res = res + (i * tup[1])
				i = i + 1    
			
			giniOutgoingNegativeActions = 0
			if (sum(outgoing_negative_actions.values()) > 0):
				giniOutgoingNegativeActions = ((2.0 * res)/ (len(sortedNegDistSum) * sum(outgoing_negative_actions.values()))) - ((len(sortedNegDistSum) + 1.0   ) / len(sortedNegDistSum))  
					
			# Computing gini of incoming negative actions
			for elem in relation.revert.keys():
				if elem in incoming_negative_actions.keys():
					incoming_negative_actions.update({elem : incoming_negative_actions[elem] + relation.revert[elem]}) 
				else:
					incoming_negative_actions.update({elem : relation.revert[elem]})
			for elem in relation.deleted.keys():
				if elem in incoming_negative_actions.keys():
					incoming_negative_actions.update({elem : incoming_negative_actions[elem] + relation.deleted[elem]}) 
				else:
					incoming_negative_actions.update({elem : relation.deleted[elem]})
			
			sortedNegDistSum = sorted(incoming_negative_actions.iteritems(), key=operator.itemgetter(1))        
			i = 1
			res = 0
			for tup in sortedNegDistSum:
				res = res + (i * tup[1])
				i = i + 1    
			
			giniIncomingNegativeActions = 0
			if (sum(incoming_negative_actions.values()) > 0):
				giniIncomingNegativeActions = ((2.0 * res)/ (len(sortedNegDistSum) * sum(incoming_negative_actions.values()))) - ((len(sortedNegDistSum) + 1.0   ) / len(sortedNegDistSum))  
			
			# ALL ACTIONS

			# this metric can include token specific actions several times: reintroduction + self-reintroduction
			all_actions = tokens_added + tokens_deleted + tokens_redeleted + tokens_reintroduced + tokens_reverted + tokens_selfreintroductions + tokens_selfredeleted + tokens_selfdeleted + sum(relation.self_revert.values())
			
			# SELF SUPPORT

			# self-reintroduction ratio
			selfReintroductionRatio = 0
			if (all_actions != 0):
				selfReintroductionRatio = tokens_selfreintroductions / all_actions
			self_reintroductions.append(selfReintroductionRatio)
			
			selfReintroductionRatio_avg_w1 = 0
			if (len(self_reintroductions) >= window1):
				selfReintroductionRatio_avg_w1 = sum(self_reintroductions[len(self_reintroductions)-window1:]) / float(window1)
			
			# self-supported actions ration
			selfSupportRatio = 0
			if (all_actions != 0):
				selfSupportActions = tokens_selfredeleted + tokens_selfreintroductions
				selfSupportRatio = (tokens_selfreintroductions + tokens_selfredeleted) / all_actions
			self_supports.append(selfSupportRatio)
			
			selfSupportRatio_avg_w1 = 0
			if (len(self_reintroductions) >= window1):
				selfSupportRatio_avg_w1 = (sum(self_reintroductions[len(self_reintroductions)-window1:]) + sum(self_supports[len(self_reintroductions)-window1:])) / float(window1)

			# get number of talk page edits from editor since last (article) revision.	   
			if (editor_name in talk_pages.keys()):
				while len(talk_pages[editor_name]) > 0:
					if (talk_pages[editor_name][0] <= revision.timestamp):
						talkPageEdits += 1
						talk_pages[editor_name].pop(0)
					else:
						break
			
			# TEMPLATE TAGS

			timestamps = tags.keys()
			timestamps.sort()
			for talk_ts in timestamps:
				if talk_ts <= revision.timestamp:
					for t in tags[talk_ts]:
						
						# Handling "maintained" tag
						if (t["tagname"] == "maintained") and (t["type"] == "addition"):
							maintained = 1
						elif (t["tagname"] == "maintained") and (t["type"] == "removal"):
							maintained = 0
						
						# Handling "npov" tag    
						elif (t["tagname"] == "npov") and (t["type"] == "addition"):
							npov = 1
						elif (t["tagname"] == "npov") and (t["type"] == "removal"):
							npov = 0
							
						# Handling "good article" tag
						elif (t["tagname"] == "good article") and (t["type"] == "addition"):
							good_article = 1
						elif (t["tagname"] == "good article") and (t["type"] == "removal"):
							good_article = 0
							
						# Handling "featured article" tag    
						elif (t["tagname"] == "featured article") and (t["type"] == "addition"):
							featured_article = 1    
						elif (t["tagname"] == "featured article") and (t["type"] == "removal"):
							featured_article = 0
						
						# Handling "disputed" tag
						elif (t["tagname"] == "disputed") and (t["type"] == "addition"):
							disputed = 1
						elif (t["tagname"] == "disputed") and (t["type"] == "removal"):
							disputed = 0
					
			# WIKIGRAPH 
			relation = relations[revision]
			
			# List of editors in each order.
			ordered_editors.append(relation.author)
			ordered_not_vandalism.append(revision)
			
			if (relation.author in contributors_rev.keys()):
			    contributors_rev[relation.author].append(revision)
			else:
			    contributors_rev.update({relation.author : [revision]})
			
			# Update the nodes.
			if relation.author in nodes.keys():
			    nodes[relation.author].append(revisions[revision].id)
			else:
			    nodes.update({relation.author : [revisions[revision].id]})
			
			# Update the edges.
			# Edges: (edge_type, editor_source, rev_source, editor_target, rev_target, weight)
			edges_rev.update({revision : []})
			
			for elem in relation.deleted.keys():
			    edges_rev[revision].append(("deletion", relation.author, revision, revisions[elem].contributor_name, elem, relation.deleted[elem]))
			
			for elem in relation.reintroduced.keys():
			    edges_rev[revision].append(("reintroduction", relation.author, revision, revisions[elem].contributor_name, elem, relation.reintroduced[elem]))
			        
			for elem in relation.redeleted.keys():
			    edges_rev[revision].append(("redeletion", relation.author, revision, revisions[elem].contributor_name, elem, relation.redeleted[elem]))
			
			for elem in relation.revert.keys():
			    edges_rev[revision].append(("revert", relation.author, revision,  revisions[elem].contributor_name, elem, relation.revert[elem]))
			
			# Calculate metrics.
			distinct_editors = 0
			deletion_edges_contributors_w = 0
			deletion_sender_ratio = 0
			deletion_receivers_ratio = 0
			deletion_reciprocal_edges = []
			deletion_reciprocity = 0
			deletion_edges_total = 0
			deletion_weight_avg = 0
			bipolarity = 0
			
			A = []
			editors_window = []
			R = {}
			C = {}
			
			if (len(ordered_editors) >= window1):
			    deletion_sender_ratio = set([])
			    deletion_receivers_ratio = set([])
			    editors_window = list(set(ordered_editors[len(ordered_editors)-window1:]))
			    A = np.zeros((len(editors_window), len(editors_window)))
			    R = {}
			    C = {}
			    for past_rev in ordered_not_vandalism[len(ordered_not_vandalism)-window1:]:
			        for edge in edges_rev[past_rev]:
			            (edge_type, source, rev_source, target, rev_target, weight) = edge
			            if edge_type == "deletion":
			                # Checking if the target editor belongs to the window.
			                if (target in editors_window):
			                    # Counts the total number of edges in the window.
			                    deletion_edges_total = deletion_edges_total + 1  

			                    # For metric 2: ratio of number of edges e only between editors in w.
			                    deletion_edges_contributors_w = deletion_edges_contributors_w + 1 
			                    
			                    # For metric 3: ratio of n that sent nodes at least once in w.
			                    deletion_sender_ratio.add(source) 
			                
			                    # For metric 6: avg. weight of the edges e in w
			                    deletion_weight_avg = deletion_weight_avg + weight
			                    
			                    # Update adjacency matrix
			                    s = editors_window.index(source)
			                    t = editors_window.index(target)
			                    A[s][t] = A[s][t] + math.log10(1 + weight) + 1
			                    A[t][s] = A[t][s] + math.log10(1 + weight) + 1
			                    
			                    if (s,t) in R.keys():
			                        R[(s,t)] = R[(s,t)] + 1
			                    else:
			                        R.update({(s,t) : 1})
			                        
			                    if (s,t) in C.keys():
			                        C[(s,t)] = C[(s,t)] + "<br /><br /><a target=_blank href=http://en.wikipedia.org/w/index.php?&diff=" + str(rev_target) + ">" + source + "->" + target + " Revision: " + str(rev_target) + "</a><br />" + printContext(rev_source, rev_target)
			                        C[(t,s)] = C[(t,s)] + "<br /><br /><a target=_blank href=http://en.wikipedia.org/w/index.php?&diff=" + str(rev_target) + ">" + target + "->" + source + " Revision: " + str(rev_target) + "</a><br />" + printContext(rev_source, rev_target)
			                    else:
			                        C.update({(s,t) : "<a target=_blank href=http://en.wikipedia.org/w/index.php?&diff=" + str(rev_target) + ">" + source + "->" + target + " Revision: " + str(rev_target) + "</a><br />" + printContext(rev_source, rev_target)})
			                        C.update({(t,s) : "<a target=_blank href=http://en.wikipedia.org/w/index.php?&diff=" + str(rev_target) + ">" + target + "->" + source + " Revision: " + str(rev_target) + "</a><br />" + printContext(rev_source, rev_target)})
			                
			                # For metric 4: ratio of n that received edges at least once in w.
			                # Checking if the target revision belongs to the window.
			                if (rev_target in ordered_not_vandalism[len(ordered_not_vandalism)-window1:]):
			                    deletion_receivers_ratio.add(target)
			                
			                # for metric 5: ratio of e that was reciprocal
			                # Don't discriminate edges that target revisions outside the window.    
			                if ((target, source) in deletion_reciprocal_edges):
			                    deletion_reciprocal_edges.remove((target, source))
			                    deletion_reciprocity = deletion_reciprocity + 1
			                else:
			                    deletion_reciprocal_edges.append((source, target))
			                
			    # 1: Number of distinct editors n that edited in window1.
			    distinct_editors = len(set(ordered_editors[len(ordered_editors)-window1:]))                
			    
			    # 2: Ratio of # of edges e only between editors in w
			    deletion_edges_contributors_w = deletion_edges_contributors_w / float(distinct_editors) 
			                 
			    # 3: Ratio of n that sent edges at least once in w 
			    deletion_sender_ratio = len(deletion_sender_ratio) / float(distinct_editors)
			    
			    # 4: Ratio of n that received edges at least once in w 
			    deletion_receivers_ratio = len(deletion_receivers_ratio) / float(distinct_editors)
			    
			    if (deletion_edges_total != 0):
			        # 5: Ratio of e that was reciprocal
			        deletion_reciprocity = deletion_reciprocity / float((deletion_edges_total / 2.0))
			    
			        # 6: Average weight of the edges e in w
			        deletion_weight_avg = deletion_weight_avg / float(deletion_edges_total)
			    else:
			        deletion_reciprocity = 0
			        
			        deletion_weight_avg = 0
			    
			    # Update the reciprocity on the weights of the adjacency matrix.
			    for (s_index, t_index) in R.keys():
			        #print "s_index", s_index, "t_index", t_index,  R
			        if ((t_index, s_index) in R.keys()):
			            reciprocity = min(R[(s_index, t_index)], R[(t_index, s_index)])
			        else:
			            reciprocity = 0
			        A[s_index][t_index] = A[s_index][t_index] #+  (2*reciprocity)
			        A[t_index][s_index] = A[t_index][s_index] #+  (2*reciprocity)
			    
			    eigenvalues, eigenvectors = np.linalg.eig(A)
			    lambda_max = max(eigenvalues)
			    lambda_min = min(eigenvalues)  
			    
			    bipolarity = 0
			    if (lambda_max != 0):  
			        bipolarity = -lambda_min / lambda_max 
			        bipolarity = bipolarity.real
			
			# antagonized_editors: Revert actions + delete actions in revision (distinct editors)
			antagonized_editors = set([])
			for elem in relation.revert.keys():
			    antagonized_editors.add(revisions[elem].contributor_id)
			for elem in relation.deleted.keys():
			    antagonized_editors.add(revisions[elem].contributor_id)   
			    
			all_antagonized_editors.append(len(antagonized_editors))
			
			antagonized_editors_avg_w1 = 0
			if (len(all_antagonized_editors) >= window1):
			    antagonized_editors_avg_w1 = sum(all_antagonized_editors[len(all_antagonized_editors)-window1:]) / float(window1)
			
			# supported_editors: reintroductions + redeletes (distinct editors)
			supported_editors = set([])
			for elem in relation.reintroduced.keys():
			    supported_editors.add(revisions[elem].contributor_id)
			for elem in relation.redeleted.keys():
			    supported_editors.add(revisions[elem].contributor_id)
			 
			all_supported_editors.append(len(supported_editors))
			supported_editors_avg_w1 = 0
			if (len(all_supported_editors) >= window1):
			    supported_editors_avg_w1 = sum(all_supported_editors[len(all_supported_editors)-window1:]) / float(window1)

			# CREATE DATA
			for author in authors:
				dataAuthors[author] = {}
				dataAuthors[author]['tokens-absolute'] = authorsTokensAbs[author]
				dataAuthors[author]['tokens-relative'] = authorsTokensRel[author]

			data = {
				'revision-id': revision.wikipedia_id, 
				'revision-count': counterRevisions,
				'number-tokens': totalTokensCount,
				'number-authors': totalAuthorCountAS,
				'length-change': lengthChange, 
				'edit-rapidness': editRapidness, 
				'editor-name': editor_name,
				'editor-id': editor_id,
				'timestamp': datetime.datetime.fromtimestamp(int(revision.timestamp)).strftime('%Y-%m-%d %H:%M:%S'),
				'vandalism': False,
				'authors': dataAuthors,
				'editors': editorsTokensAbs,
				'number-editors':len(editorsTokensAbs),
				'talkpage-edits': talkPageEdits, 
				'window1-size': window1,
				'total-actions': all_actions, 
				'tokens-added': tokens_added, 
				'tokens-deleted': tokens_deleted,
				'tokens-redeleted': tokens_redeleted,
				'tokens-reintroduced': tokens_reintroduced,
				'tokens-reverted': tokens_reverted,
				'tokens-self-deleted': tokens_selfdeleted,
				'tokens-self-reverted': tokens_selfreverted,
				'tokens-self-redeleted': tokens_selfredeleted,
				'tokens-self-reintroduced': tokens_selfreintroductions,
				#'negative-actions': negativeActionsAbs, 
				#'positive-actions': positiveActionsAbs, 
				#'negative-actions-rel': negativeActionsRel, # share of positive and negative actions (no adds!)
				#'positive-actions-rel': positiveActionsRel, # share of positive and negative actions (no adds!)
				'gini-ownership':wikiGini, 
				'gini-editorship': giniEditorship, 
				'gini-editorship-w1': giniEditorship_w1,
				'gini-OutNegActions': giniOutgoingNegativeActions,
				'gini-InNegActions': giniIncomingNegativeActions, 
				'antagonistic-actions': antagonistic_actions, 
				#'antagonizedEditorsAvgW1': antagonized_editors_avg_w1,
				'antagonized-editors': antagonized_editors,
				'numAntagonizedEditors': len(antagonized_editors), 
				'supportive-actions': supportive_actions,
				'supported-editors': supported_editors_avg_w1,
				'number-supported-editors': len(supported_editors), 
				'supported-editors-w1': supported_editors_avg_w1,
				'self-reintroduction-ratio': selfReintroductionRatio,
				'self-reintroduction-ratio-w1':selfReintroductionRatio_avg_w1, 
				'self-support-ratio': selfSupportRatio,
				'self-support-ratio-w1': selfSupportRatio_avg_w1, 
				'self-support-actions': selfSupportActions, 
				'tag-maintained': maintained, # bool(), is maintained template used at the same time on the talk page
				'tag-NPOV': npov, # bool(), is npov template used at the same time on the talk page
				'tag-goodArticle': good_article, # bool(), is goodarticle template used at the same time on the talk page
				'tag-featuredArticle': featured_article, # bool(), is featured article template used at the same time on the talk page
				'tag-disputed': disputed, # bool(), is disputed tag used at the same time on the talk page 
			}
			stats.append(data)
			prev_revision = revision_id
			counterRevisions += 1
			
			data_graph.append({'revision': revision, 
			                  'author': revisions[revision].contributor_name, 
			                  'distinct_editors': distinct_editors, 
			                  'deletion_edges_contributors_w': deletion_edges_contributors_w,
			                  'deletion_sender_ratio': deletion_sender_ratio,
			                  'deletion_receiver_ratio': deletion_receivers_ratio,
			                  'deletion_reciprocity': deletion_reciprocity,
			                  'deletion_weight_avg': deletion_weight_avg,
			                  'antagonized_editors_avg_w1': antagonized_editors_avg_w1,
			                  'supported_editors_avg_w1': supported_editors_avg_w1,
			                  'bipolarity' : bipolarity, 
			                  'adjacency_matrix' : (A, editors_window, authDistSum, totalWordCount),
			                  'reciprocity_matrix' : R,
			                  'context' : C})    




	metadata[article] = { 
		'num-editors': int(),
		'title_url': str(),
		'stats-created': datetime.now().strftime('%Y-%m-%d %H:%M'),
		'stats-analyzed': bool(),
		'last-updated', datetime(),
	}
	return stats, metadata, graph_data

def saveDataToFile(filename, data):
	"""
	export data to text file
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
	""" 
	text_file = open(filename, "w")
	text_file.write(data)
	text_file.close()

def getAuthorsTokenCount(authors, length=False):
	"""
	gets number of tokens for every author

    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
	"""
	wordAbsolute = {}
	wordRelative = {}

	for author in authors:
		if(author in wordAbsolute.keys()):
			wordAbsolute[author] += 1
		else:
			wordAbsolute[author] = 1
			
	if(length):
		for author in wordAbsolute.keys():
			wordRelative[author] = wordAbsolute[author] / float(length) 
		return wordRelative, wordAbsolute
	else:
		return wordAbsolute

def getTagDatesFromPage(file_name):
	"""
	DESCRIPTION

    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
	"""
	# Compile regexp
	reglist = list()
	first_rev = {}
	reglist.append({"tagname": "maintained", "regexp": re.compile('\{\{(articleissues\|((?:(?!\}\}).)*\||)|multiple issues\|((?:(?!\}\}).)*\||)|)maintained((\||=)(?:(?!\}\}).)*|)\}\}', re.IGNORECASE)})
	# reglist.append({"tagname": "good article", "regexp": re.compile('\{\{(articleissues\|((?:(?!\}\}).)*\||)|multiple issues\|((?:(?!\}\}).)*\||)|)good article((\||=)(?:(?!\}\}).)*|)\}\}', re.IGNORECASE)})
	# reglist.append({"tagname": "featured article", "regexp": re.compile('\{\{(articleissues\|((?:(?!\}\}).)*\||)|multiple issues\|((?:(?!\}\}).)*\||)|)featured article((\||=)(?:(?!\}\}).)*|)\}\}', re.IGNORECASE)})
	# reglist.append({"tagname": "npov", "regexp": re.compile('\{\{(articleissues\|((?:(?!\}\}).)*\||)|multiple issues\|((?:(?!\}\}).)*\||)|)(pov|npov)((\||=)(?:(?!\}\}).)*|)\}\}', re.IGNORECASE)})
	# reglist.append({"tagname": "disputed", "regexp": re.compile('\{\{(articleissues\|((?:(?!\}\}).)*\||)|multiple issues\|((?:(?!\}\}).)*\||)|)disputed((\||=)(?:(?!\}\}).)*|)\}\}', re.IGNORECASE)})
	re_user = re.compile('({{|\[\[)user.*?[:|](.*?)[}/\]|]', re.IGNORECASE)
	
	# Access the file.
	dumpIterator = dump.Iterator(file_name)
	
	# Revisions to compare.
	revision_curr = Revision()
	revision_prev = Revision()
	text_curr = None

	listOfTagChanges = {}
	maintainers = []
	all_contributors = {"maintained": {}, "good article": {}, "featured article": {}, "npov": {}, "disputed": {}}

	# Iterate over the pages.
	for page in dumpIterator.readPages():
		# Iterate over revisions of the article.
		i = 0
		prev_matched = list()
		is_maintained = False
		for revision in page.readRevisions():
			revision.wikipedia_id = int(revision.getId())
			revision.timestamp = revision.getTimestamp()
			# Some revisions don't have contributor.
			if (revision.getContributor() != None):
				revision.contributor_id = revision.getContributor().getId()
				revision.contributor_name = revision.getContributor().getUsername()
			else:
				revision.contributor_id = 'Not Available'
				revision.contribur_name = 'Not Available'

			text_curr = revision.getText()
			if(text_curr):
				text_curr = text_curr.encode('utf-8')
				text_curr = text_curr.lower()
			else:
				continue
			matched = list()
			aux = list()

			for regexp in reglist:
				m = regexp["regexp"].search(text_curr)
				if m:
					users = []
					i = 2
					mc = re_user.split(m.group(0))
					users.append(mc[2])
					while (i+3 < len(mc)):
						users.append(mc[i+3])
						i = i +3
					if is_maintained == False: 
						first_rev['revision_id'] = revision.wikipedia_id
						first_rev['editor'] = revision.getContributor().getUsername()
						first_rev['revision_timestamp'] = datetime.datetime.fromtimestamp(int(revision.timestamp)).strftime('%Y-%m-%d %H:%M:%S')
						is_maintained = True
					
					matched.append(regexp["tagname"])
					aux.append((regexp["tagname"], users))

			# Calculate additions
			for (match, contributor) in aux:
				if not (match in prev_matched):
					if not (revision.timestamp in listOfTagChanges.keys()):
						listOfTagChanges[revision.timestamp] = list()
					listOfTagChanges[revision.timestamp].append({"rev": revision.wikipedia_id, "type": "addition", "tagname": match, "wikiname": revision.contributor_name, "timestamp": revision.timestamp, "date": datetime.datetime.fromtimestamp(int(revision.timestamp)).strftime('%Y-%m-%d %H:%M:%S')})
				all_contributors[match].update({revision.timestamp : {"rev": revision.wikipedia_id, "user":contributor, "date":datetime.datetime.fromtimestamp(int(revision.timestamp)).strftime('%Y-%m-%d %H:%M:%S')}})
		   
			# Calculate removals
			for match in prev_matched:
				if not (match in matched):
					if not (revision.timestamp in listOfTagChanges.keys()):
						listOfTagChanges[revision.timestamp] = list()
					listOfTagChanges[revision.timestamp].append({"rev": revision.wikipedia_id, "type": "removal", "tagname": match, "wikiname": revision.contributor_name, "timestamp": revision.timestamp, "date": datetime.datetime.fromtimestamp(int(revision.timestamp)).strftime('%Y-%m-%d %H:%M:%S')})

			prev_matched = matched

	return listOfTagChanges, all_contributors, maintainers, first_rev

def getAuthorshipDataFromRevision(revision):
	"""
	get list of authors for every token

    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
	"""
	authors = []
	for hash_paragraph in revision.ordered_paragraphs:
		
		p_copy = deepcopy(revision.paragraphs[hash_paragraph])
		paragraph = p_copy.pop(0)
		
		for hash_sentence in paragraph.ordered_sentences:
			sentence = paragraph.sentences[hash_sentence].pop(0)
			
			for word in sentence.words:
				#text.append(word.value)
				authors.append(word.author_id)
	
	return authors

def printStatsCSV(stats):
	"""
	DESCRIPTION

    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
	"""
	# Stats to print
	finalStats = {}
	
	# Mappings of revisions and fake ids
	revs = {}
	
	# Stats per revisions
	wikiGini1 = []
	#wikiGini2 = []
	#totalLength = []
	lengthChange = []
	editRapidness = []
	antagonizedEditors = []
	antagonisticActions = []
	supportedEditors = []
	supportiveActions = []
	#tokenActions = []
	giniEditorship = []
	giniEditorship_w1 = []

	giniOutgoingNegativeActions = []
	giniIncomingNegativeActions = []
	selfReintroductionRatio = []
	selfSupportRatio = []
	selfReintroductionRatio_avg_w1 = []
	selfSupportRatio_avg_w1 = []
	#vandalism = []
	maintained = []
	npov = []
	goodArticle = []
	featuredArticle = []
	disputed = []
	antagonized_editors_avg_w1 = []
	supported_editors_avg_w1 = []
	
	# Stats per editors
	editorStats = {}

	lines = []
	
	header = ["wikiGiniV1", "length-change"]
	
	",".join(header)
	
	lines.append(header)
	
	for elem in stats:
		row = []
		row.append(elem["revisionId"])
		row.append(elem['wikiGiniV1'])
		row.append(elem['lengthChange']) 
		row.append(elem['editRapidness'])
		row.append(elem['antagonizedEditors'])
		row.append(elem['antagonizedEditorsAvgW1'])
		row.append(elem['antagonisticActions'])
		row.append(elem['supportedEditors'])
		",".join(row)
		lines.append(row)
		
	"\n".join(lines)
	
	return lines

def processTalkPages(file_name):
	"""
	DESCRIPTION

    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
	"""
	talk_pages = {}
	
	# Access the file
	dumpIterator = dump.Iterator(file_name)
	
	# Iterate over pages of the dump
	for page in dumpIterator.readPages():
		
		# Iterate over revisions of the article.
		for revision in page.readRevisions():
			
			contributor_name = revision.getContributor().getUsername()
			
			if (contributor_name in talk_pages.keys()):    
				talk_pages[contributor_name].append(revision.getTimestamp())
			else:
				talk_pages.update({contributor_name : [revision.getTimestamp()]})
			
	return talk_pages

def saveTags(contributors, revisions, order, file_name):
	"""
	DESCRIPTION

    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
	"""
	maintainers = contributors["maintained"] 
	timestamps = maintainers.keys()
	timestamps.sort()
	
	csv_file = open(file_name, "w")    
	for (rev_id, vandalism) in order:
		users = None
		for talk_ts in timestamps:
			if not(vandalism) and talk_ts <= revisions[rev_id].timestamp:
				users = maintainers[talk_ts]["user"]
		
		if (users != None):
			csv_file.write(str(rev_id) + "\t" + "maintained" + "\t " + "\t".join(users) + "\n")
			
	csv_file.close()

def startScript(file_name, folder_json, output):
	"""
	starts computation and export

    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
	"""
	revisions, order, relations = WikiwhoRelationships.analyseArticle(file_name)


	# Compute file name of talk page data file
	talk_file = os.path.join(os.path.dirname(file_name), "talk_" + os.path.basename(file_name))
	tags, contributors, maintainer, first_rev = getTagDatesFromPage(talk_file)
	print first_rev
	
	#saveTags(contributors, revisions, order, file_name.replace(".xml", "_maintainers.csv"))

	if output == None or output == 'json':
		
		talk_pages = processTalkPages(talk_file)
		
		# Compute statistics
		stats, metadata = getArticleStats(revisions, order, relations, tags, talk_pages)
		metadata[]

		# export objects as json files
		saveDataToFile(folder_json+'/stats_'+os.path.basename(file_name).split('.')[0]+'.json', json.dumps(stats, indent=2))
		saveDataToFile(folder_json+'/order_'+os.path.basename(file_name).split('.')[0]+'.json', json.dumps(order, indent=2))

	elif (output == 'table'):
		WikiwhoRelationships.printRelationships(relations, order) 
		
	elif (output== 'csv'):
		stats = getStatsOfFile(revisions, order, relations, tags)
		printStatsCSV(stats)
		
	else:
		print "Output format", output, "not supported"

def main(my_argv):
	"""
	Reads out shell arguments and writes help statements

    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
	"""
	inputfile = ''
	output = None

	# check shell argument list
	if (len(my_argv) <= 3):
		try:
			opts, _ = getopt.getopt(my_argv,"i:",["ifile="])
		except getopt.GetoptError:
			print 'Usage: wikistats.py -i <inputfile> [-o <output>]'
			exit(2)
	else:
		try:
			opts, _ = getopt.getopt(my_argv,"i:o:",["ifile=","output="])
		except getopt.GetoptError:
			print 'Usage: wikistats.py -i <inputfile> [-o <output>]'
			exit(2)
	
	for opt, arg in opts:
		if opt in ('-h', "--help"):
			print "wikistats"
			print
			print 'Usage: wikistats.py -i <inputfile> [-rev <revision_id>]'
			print "-i --ifile File to analyze"
			print "-o --output Type of output. Options: 'json', 'table'. If not specified, JSON is the default."
			print "-h --help This help."
			exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--output"):
			output = arg
		 
	return (inputfile, output)

# runs on start and call via shell
if __name__ == '__main__':

	file_name, output = main(argv[1:])

	#folder_json = '../../data/json/first-test'
	folder_json = '../../data/json/test'
	file_name = '../../data/raw/xml/test/William_McKendree.xml'
	# file_name = '../../data/raw/xml/test/Alden_Partridge.xml'

	startScript(file_name, folder_json, 'json')


