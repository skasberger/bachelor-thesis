#!/bin/env python2
# -*- coding: utf-8 -*-
"""
This script computes and analyzes the data created from wikistats.
It imports old and creates new metrics to plot them afterwards.  
"""

from pandas import DataFrame
import pandas as pd
import numpy as np
import simplejson
import matplotlib.pyplot as plt
#import wikiplots

__author__ = "Stefan Kasberger, Felix Stadthaus and Eren Misirli"
__copyright__ = "Copyright 2015"
__license__ = "GPL v2"
__version__ = "1.0.0"
__maintainer__ = "Stefan Kasberger"
__email__ = "mail@stefankasberger.at"
__status__ = "Development"

REL_TO_ROOT = '../../'
FILE_WIKIPAGES = REL_TO_ROOT+'data/csv/wikipages.csv'
FOLDER_JSON = REL_TO_ROOT+'data/json/first-test/'
FOLDER_CSV = REL_TO_ROOT+'data/csv'
FOLDER_FIGURES = REL_TO_ROOT+'figures/first-test'
FILE_FORMATS = ['png']

def PlotViewOne(data):
    """
    DESCRIPTION

    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    x = []
    yO = []
    yE = []
    yCountOwners = []
    yCountEditors = []
    i = 0
    for date in data:
        x.append(date['revision-count'])
        yO.append(date["gini-ownership"])
        yE.append(date["gini-editorship"])
        yCountOwners.append(date["number-authors"])
        yCountEditors.append(len(date["editors"]))
        #print 'editors: '+str(date["editors"])
        #print 'editors number: '+str(len(date["editors"]))
    yCONormalized = [elem*1.0/max(yCountOwners) for elem in yCountOwners]
    yCENormalized = [elem*1.0/max(yCountEditors) for elem in yCountEditors]

    fig = plt.figure()

#    graph = fig.add_subplot(111)
#    tagAreas = {}
#    i = 0
#    for date in data:
#        i += 1;
#        for tagName in date["tagChangeData"]:
#            tagChange = date["tagChangeData"][tagName]
#            if tagChange["type"] == "addition":
#                if(not(tagName in tagAreas)):
#                    tagAreas[tagName] = i
#            else:
#                if(tagName in tagAreas):
#                    tagPlotData = tagList[tagName]
#                    poly = Polygon([(tagAreas[tagName], tagPlotData["bottom"]), (tagAreas[tagName], tagPlotData["top"]), (i, tagPlotData["top"]), (i,tagPlotData["bottom"])], facecolor=tagPlotData["facecolor"], edgecolor="black")
#                    graph.add_patch(poly)
#                    del tagAreas[tagName]
#
#    for tagName in tagAreas:
#        tagPlotData = tagList[tagName]
#        poly = Polygon([(tagAreas[tagName], tagPlotData["bottom"]), (tagAreas[tagName], tagPlotData["top"]), (i, tagPlotData["top"]), (i,tagPlotData["bottom"])], facecolor=tagPlotData["facecolor"], edgecolor="black")
#        graph.add_patch(poly)
#
    graph = fig.add_subplot(111)
    graph.plot(x, yO, 'b-', x, yE, 'g-', x, yCONormalized, "b^", x, yCENormalized, "g^")
    fig = plt.gcf()
    fig.set_size_inches(18.5,10.5)
    plt.xlabel('Revision')
    plt.ylabel('Normalized values')
    plt.legend(["ownership gini (all rev)", "edit gini (all rev)", "#owner (all rev)", "#editors (all rev)"], loc="best", fontsize="x-small")
    plt.title('Plot View One')

# def plotViewTwo(data):
    # """
    # description: 
    # parameters: 
    # return: 
    # """
#     x = []
#     yE = []
#     yEXrev = []
#     yCountEditors = []
#     yCountEditorsLastXrev = []
    
#     i = 0
#     LastXrev = "50"
#     revCount = len(data)
    
#     for date in data:
#         x.append(date['revision-count'])
#         yE.append(date["giniEdit"])
#         yCountEditors.append(len(date["editors"]))
        
#         # dont know if this metrics is computet right => check the algorithm behind
#         yEXrev.append(date["gini-editorship-w1"])
#         yCountEditorsLastXrev.append(date["giniEditLastXRevs"][LastXrev]["authCount"])
#         else:
#             yEXrev.append(0)
#             yCountAuthorsLastXrev.append(0)

#     yCONormalized = [elem*1.0/max(yCountAuthors) for elem in yCountAuthors]
#     yCountAuthorsLastXrevNormalized = [elem*1.0/max(yCountAuthorsLastXrev) for elem in yCountAuthorsLastXrev]

#     fig = plt.figure()

#     graph = fig.add_subplot(111)
#     tagAreas = {}
#     i = 0
#     for date in data:
#         i += 1;
#         for tagName in date["tagChangeData"]:
#             tagChange = date["tagChangeData"][tagName]
#             if tagChange["type"] == "addition":
#                 if(not(tagName in tagAreas)):
#                     tagAreas[tagName] = i
#             else:
#                 if(tagName in tagAreas):
#                     tagPlotData = tagList[tagName]
#                     poly = Polygon([(tagAreas[tagName], tagPlotData["bottom"]), (tagAreas[tagName], tagPlotData["top"]), (i, tagPlotData["top"]), (i,tagPlotData["bottom"])], facecolor=tagPlotData["facecolor"], edgecolor="black")
#                     graph.add_patch(poly)
#                     del tagAreas[tagName]

#     for tagName in tagAreas:
#         tagPlotData = tagList[tagName]
#         poly = Polygon([(tagAreas[tagName], tagPlotData["bottom"]), (tagAreas[tagName], tagPlotData["top"]), (i, tagPlotData["top"]), (i,tagPlotData["bottom"])], facecolor=tagPlotData["facecolor"], edgecolor="black")
#         graph.add_patch(poly)
        
#     graph.plot(x, yEXrev, 'b-', x, yE, 'g-', x, yCountAuthorsLastXrevNormalized, "b^", x, yCONormalized, "g^")
#     plt.legend(["edit gini (last " + LastXrev + " rev)", "edit gini (all rev)", "#editors (last " + LastXrev + " rev)", "#editors (all rev)"], loc="best", fontsize="x-small")
#     plt.xlabel('Revision')
#     plt.ylabel('Normalized values')
#     plt.title('Plot View Two')
#     if(plotFileName):
#         plt.savefig(plotFileName, bbox_inches='tight')
#     else:
#         plt.show()


### Plot 3

def PlotViewThree(data):
    """
    DESCRIPTION

    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    x = []
    yO = []
    yWordCount = []
    yCountOwners = []
    yTime = []
    i = 0
    
    for date in data:
        x.append(date['revision-count'])
        yO.append(date["gini-ownership"])
        yWordCount.append(date["number-tokens"])
        yCountOwners.append(date["number-authors"])
        yTime.append(date["edit-rapidness"])

    yCONormalized = [elem*1.0/max(yCountOwners) for elem in yCountOwners]
    yTimeNormalized = [elem*1.0/max(yTime) for elem in yTime]
    yWordCountNormalized = [elem*1.0/max(yWordCount) for elem in yWordCount]

    fig = plt.figure()

    graph = fig.add_subplot(111)
#    tagAreas = {}
#    i = 0
#    for date in data:
#        i += 1;
#        for tagName in date["tagChangeData"]:
#            tagChange = date["tagChangeData"][tagName]
#            if tagChange["type"] == "addition":
#                if(not(tagName in tagAreas)):
#                    tagAreas[tagName] = i
#            else:
#                if(tagName in tagAreas):
#                    tagPlotData = tagList[tagName]
#                    poly = Polygon([(tagAreas[tagName], tagPlotData["bottom"]), (tagAreas[tagName], tagPlotData["top"]), (i, tagPlotData["top"]), (i,tagPlotData["bottom"])], facecolor=tagPlotData["facecolor"], edgecolor="black")
#                    graph.add_patch(poly)
#                    del tagAreas[tagName]#

#    for tagName in tagAreas:
#        tagPlotData = tagList[tagName]
#        poly = Polygon([(tagAreas[tagName], tagPlotData["bottom"]), (tagAreas[tagName], tagPlotData["top"]), (i, tagPlotData["top"]), (i,tagPlotData["bottom"])], facecolor=tagPlotData["facecolor"], edgecolor="black")
#        graph.add_patch(poly)

    graph.plot(x, yO, 'b-', x[9:], yTimeNormalized[9:], 'y-', x, yCONormalized, "b^", x, yWordCountNormalized, "r-")
    graph.fill_betweenx(yTimeNormalized,x,color='yellow')
    fig = plt.gcf()
    fig.set_size_inches(18.5,10.5)
    plt.legend(["ownership gini (all rev)", "edit frequency", "#authors (all rev)", "#words"], loc="best", fontsize="x-small")
    plt.xlabel('Revision')
    plt.ylabel('Normalized values')
    plt.title('Plot View Three')


def DrawPlot(data, yData=None):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    df = DataFrame(data)
    
    if yData == None:
        df.plot()
    else:
        plt.plot(df)
    fig = plt.gcf()
    fig.set_size_inches(18.5,10.5)

def OpenJSON(filename):
    """
    DESCRIPTION
    
    :Parameters:
        filename : string
            complete relative or absolute path to file
        
    :Return:
        dict(data)
    """
    try:
        fp = open(filename, 'r')
        data = simplejson.loads(fp.read())
        fp.close()
        return data
    except Exception, e:
        raise
        return False

def ReadWikipages(filename):
    """
    Open wikipages.csv and returns data for articles, where analysis column is yes
    
    :Parameters:
        filename : string
            complete relative or absolute path to wikipages.csv
        
    :Return:
        dict(articles) : articles where analysis is yes
        list(maintainers) : name of maintainer where analysis is yes
        list(maintainers_id) : wikipedia ID of maintainer where analysis is yes
    """
    wikipages = pd.read_csv(filename, sep=';')

    row_iterator = wikipages.iterrows()
    articles = []
    maintainers = []
    maintainers_id= []

    for row in row_iterator: 
        if(row['analysis'] == 'yes'):
            articles.append(row['title'])
            maintainers.append(row['maintainer-name'])
            maintainers_id.append(row['maintainer-id'])
    return articles, maintainers, maintainers_id

def ValidateJSONImport(stats, order, articles):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    """
    description: checks json import of all articles if list length of order and stats are the same
    parameters:
    - list(stats) : 
    - list(order) : 
    - list(articles) : 
    return: 
    - bool(valid)
    - list(maintainers) : name of maintainer where analysis is yes
    - list(maintainers_id) : wikipedia ID of maintainer where analysis is yes
    """
    valid = bool
    for article in articles:
        valid = valid and len(order[article]) == len(stats[article])

    return valid

def validate_computation():
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """

    return 1

def validate_analysis():
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """

    return 1

def GetMetric(data, metric):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    """
    description: extracts a metric from every revision
    parameters:
    - list(data) : list of dicts, one for each revision
    - str(metric) : name of the key for the dicts
    return: 
    - list(listMetric) : list of the extracted metrics
    """
    listMetric = []
    for revision in data:
        listMetric.append(revision[metric])

    return listMetric

def SplitMaintainer(data, maintainer, metric, number=False):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    """
    description: extracts a metric from every revision and splits it into maintainer and non-maintainer
    parameters:
    - list(data) : list of dicts, one for each revision
    - str(metric) : name of the key for the dicts
    - str(maintainer) : name of the maintainer
    return: 
    - list(maintainerMetrics) : list of the extracted metrics from maintainer edits
    - list(othersMetrics) : list of the extracted metrics from non-maintianer edits
    """
    maintainerMetrics = []
    othersMetrics = []
    countMaintainer = 0
    countOthers = 0

    for revision in data:
        if revision['editor-name'] == maintainer:
            maintainerMetrics.append(revision[metric])
            othersMetrics.append(0)
            countMaintainer += 1
        else:
            maintainerMetrics.append(0)
            othersMetrics.append(revision[metric])
            countOthers += 1

    return maintainerMetrics, othersMetrics

def Save2CSV(data, filename):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    """
    description: saves data to csv file
    parameters:
    - DataFrame(data) : pandas dataframe
    - str(filename) : full path to file
    return: None
    """
    # needs a dataframe
    data.to_csv(filename, sep=';')

def SavePlot(filename, fileformats=['png']):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    """
    description: saves a plot in several fileformats
    parameters:
    - list(fileformats) : list of fileformats, in which the plot should be saved
    - str(filename) : full path to file
    return: None
    """
    for fileformat in fileformats:
        plt.savefig(filename+'.'+fileformat, bbox_inches='tight', format=fileformat)

def addLabels(legend, title, yLabel, xLabel):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    plt.legend(legend, loc="best", fontsize="x-small")
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)

def Normalize(data):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    """
    description: normalizes a list of numbers
    parameters:
    - list(data) : list of data points
    return: 
    - list(normalized) : list of normalized data points
    """
    normalized = []
    if max(data) == 0:
        normalized = 0
    else:
        normalized = [elem*1.0/max(data) for elem in data]
    return normalized

def GetFirstMaintainedRev(data):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    count=1
    for elem in data:
        if(elem == 1): return count 
        count += 1
    return None

def TempCompare():
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    startMaint = metrics['firstMaintRev']
    tmpMaintainer = antActionsMaintainer
    tmpOthers = antActionsOthers
    window = 50
    numWindowsBefore = 3
    numWindowsAfter = 3
    numWindows = numWindowsBefore+numWindowsAfter
    startRev = startMaint - numWindowsBefore*window
    metrics['windows'] = {}
    i=0
    print title
    while i < numWindows:
        startWin = startRev+i*window
        endWin = startRev+(i+1)*window-1
        if startWin >= 0 and endWin <= len(tmpMaintainer):
            # print 'length: '+len(tmpMaintainer[startRev+i*window):startRev+(i+1)*window-1])
            metrics['windows']['win-'+str(i)+'-maintainer'] = sum(tmpMaintainer[startWin:endWin])
            metrics['windows']['win-'+str(i)+'-others'] = sum(tmpOthers[startWin:endWin]) 
        else:
            metrics['windows']['win-'+str(i)+'-maintainer'] = None
            metrics['windows']['win-'+str(i)+'-others'] = None
        
        if metrics['windows']['win-'+str(i)+'-others'] > 0:
            metrics['windows']['win-'+str(i)+'-ratio'] = sum(tmpMaintainer[startWin:endWin]) / float(sum(tmpOthers[startWin:endWin]) )
        else:
            metrics['windows']['win-'+str(i)+'-ratio'] = 0
        print startWin,' : ',endWin,' | ',metrics['windows']['win-'+str(i)+'-maintainer'], metrics['windows']['win-'+str(i)+'-others'],metrics['windows']['win-'+str(i)+'-ratio']
        if(i == (numWindows/2)-1):
            print 'TAG'
        i += 1


def ComputeMetrics1(stats, filename):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """

    data = {}

    for article in stats:
        metrics = {}
        temp = {}
        
        title = article['article-title']
        
        # get metrics from data
        allActions = GetMetric(article, 'total-actions')
        number_tokens = GetMetric(article, 'number-tokens')
        maintainanceTag = GetMetric(article, 'tag-maintained')

        # split metrics between maintainer and others
        addsMaintainer, addsOthers = SplitMO(article, maintainers[index], 'tokens-added')
        deletesMaintainer, deletesOthers = SplitMO(article, maintainers[index], 'tokens-deleted')
        revertsMaintainer, revertsOthers = SplitMO(article, maintainers[index], 'tokens-reverted')
        antActionsMaintainer, antActionsOthers = SplitMO(article, maintainers[index], 'antagonistic-actions')
        reintroMaintainer, reintroOthers = SplitMO(article, maintainers[index], 'tokens-reintroduced')
        selfreintroMaintainer, selfreintroOthers = SplitMO(article, maintainers[index], 'tokens-self-reintroduced')
        talkpageMaintainer, talkpageOthers = SplitMO(article, maintainers[index], 'talkpage-edits')

        # BLABLA
        ownershipMaintainerAbs = GetOwnership(article, maintainers_id[index], 'tokens-absolute')
        ownershipMaintainerRel = GetOwnership(article, maintainers_id[index], 'tokens-relative')
        
        # get properties of article
        metrics['firstMaintRev'] = GetFirstMaintainedRev(maintainanceTag)
        metrics['maintainer-name'] = article['maintainer-name']
        metrics['maintainer-id'] = article['maintainer-id']
        metrics['all-actions'] = sum(allActions)
        metrics['edits-maintainer'] = len(addsMaintainer)
        metrics['edits-others'] = len(addsOthers)
        metrics['number-revisions'] = metrics['edits-maintainer'] + metrics['edits-others']
        
        # temporal comparison
        TempCompare()


        # to relativize with edits is just an assumptions to have something.
        if talkpageOthers:
            #metrics['talkPageRatio'] = sum(talkpageMaintainer) / float(metrics['edits-maintainer']) / float( sum(talkpageOthers) / float(metrics['edits-others']) )
            metrics['talkPageRatio'] = sum(talkpageMaintainer) / float(sum(talkpageOthers))
        else:
            metrics['talkPageRatio'] = 0

        # if metrics['all-actions'] is 0:
        #     metrics['addsMaintainerAvg'] = 0
        #     metrics['addsOthersAvg'] = 0
        #     metrics['addsRatio'] = 0
            
        #     metrics['deletesMaintainerRel'] = 0
        #     metrics['deletesOthersRel'] = 0
        #     metrics['deletesRatio'] = 0
            
        #     metrics['revertsMaintainerRel'] = 0
        #     metrics['revertsOthersRel'] = 0
        #     metrics['revertsRatio'] = 0

        #     metrics['reintroMaintainerAvg'] = 0
        #     metrics['reintroOthersAvg'] = 0
        #     metrics['selfreintroMaintainerAvg'] = 0
        #     metrics['selfreintroOthersAvg'] = 0
        #     metrics['selfreintroRatio'] = 0

        #     metrics['antActionsMaintainerAvg'] = 0
        #     metrics['antActionsOthersAvg'] = 0
        #     metrics['negActionsRatio'] = 0

        #     metrics['targetedIntroRatio'] = 0
        # metrics['addsMaintainerRel'] = sum(addsMaintainer)/float(metrics['all-actions'])
        # metrics['addsOthersRel'] = sum(addsOthers)/float(metrics['all-actions'])
        # metrics['addsRatio'] = metrics['addsMaintainerRel'] / float(metrics['addsOthersRel'])
        # metrics['deletesMaintainerRel'] = sum(deletesMaintainer)/float(metrics['all-actions'])
        # metrics['deletesOthersRel'] = sum(deletesOthers)/float(metrics['all-actions'])
        # metrics['deletesRatio'] = metrics['deletesMaintainerRel'] / float(metrics['deletesOthersRel'])
        # metrics['revertsMaintainerRel'] = sum(revertsMaintainer)/float(metrics['all-actions'])
        # metrics['revertsOthersRel'] = sum(revertsOthers)/float(metrics['all-actions'])
        # metrics['revertsRatio'] = metrics['revertsMaintainerRel'] / float(metrics['revertsOthersRel'])
        # metrics['reintroMaintainerRel'] = sum(reintroMaintainer)/float(metrics['all-actions'])
        # metrics['reintroOthersRel'] = sum(reintroOthers)/float(metrics['all-actions']) 
        # metrics['selfreintroMaintainerRel'] = sum(selfreintroMaintainer)/float(metrics['all-actions'])
        # metrics['selfreintroOthersRel'] = sum(selfreintroOthers)/float(metrics['all-actions']) 
        # if metrics['selfreintroOthersAvg'] == 0:
        #     metrics['selfreintroRatio'] = 0
        # else:
        #     metrics['selfreintroRatio'] = metrics['selfreintroMaintainerAvg'] / float(metrics['selfreintroOthersAvg'])
        # if metrics['antActionsOthersAvg'] == 0:
        #     metrics['antActionsRatio'] = 0
        # else:
        #     metrics['antActionsRatio'] = metrics['antActionsMaintainerAvg'] / float(metrics['antActionsOthersAvg'])
        
        # if metrics['reintroMaintainerAvg'] == 0 or metrics['selfreintroOthersAvg'] == 0 or metrics['reintroOthersAvg'] == 0:
        #     metrics['targetedIntroRatio'] = 0
        #     metrics['targetedIntroRatio2Ownership'] = 0
        # else:
        #     metrics['targetedIntroRatio'] = (metrics['selfreintroMaintainerAvg'] / float(metrics['reintroMaintainerAvg'])) \
        #         / float((metrics['selfreintroOthersAvg'] / float(metrics['reintroOthersAvg'])))
        #     #metrics['targetedIntroRatio2Ownership'] = (metrics['selfreintroMaintainerRel'] / float(metrics['reintroMaintainerRel'])) \
        #     #    / float((metrics['selfreintroOthersRel'] / float(metrics['reintroOthersRel'])))

        metrics['addsMaintainerAvg'] = sum(addsMaintainer)/float(metrics['edits-maintainer'])
        metrics['addsOthersAvg'] = sum(addsOthers)/float(metrics['edits-others'])
        metrics['addsRatio'] = metrics['addsMaintainerAvg'] / float(metrics['addsOthersAvg'])
        metrics['reintroMaintainerAvg'] = sum(reintroMaintainer) / float(metrics['edits-maintainer'])
        metrics['reintroOthersAvg'] = sum(reintroOthers) / float(metrics['edits-others']) 
        metrics['reintroRatio'] = metrics['reintroMaintainerAvg'] / float(metrics['reintroOthersAvg'])
        metrics['selfreintroMaintainerAvg'] = sum(selfreintroMaintainer) / float(metrics['edits-maintainer'])
        metrics['selfreintroOthersAvg'] = sum(selfreintroOthers) / float(metrics['edits-others']) 
        metrics['selfreintroRatio'] = metrics['selfreintroMaintainerAvg'] / float(metrics['selfreintroOthersAvg'])
        metrics['antActionsMaintainerAvg'] = sum(antActionsMaintainer)/float(metrics['edits-maintainer']) 
        metrics['antActionsOthersAvg'] = sum(antActionsOthers)/float(metrics['edits-others'])
        
        # metrics['deletesMaintainerAvg'] = sum(deletesMaintainer)/float(metrics['edits-maintainer'])
        # metrics['deletesOthersAvg'] = sum(deletesOthers)/float(metrics['edits-others'])
        # metrics['deletesRatio'] = sum(metrics['deletesMaintainerAvg']) / float(metrics['edits-maintainer']) / float(sum(temp['deletesOthersAvg']) / float(metrics['edits-others']))
        
        # metrics['revertsMaintainerAvg'] = sum(revertsMaintainer)/float(metrics['edits-maintainer'])
        # metrics['revertsOthersAvg'] = sum(revertsOthers)/float(metrics['edits-others'])
        # metrics['revertsRatio'] = sum(metrics['revertsMaintainerAvg']) / float(metrics['edits-maintainer']) / float(sum(metrics['revertsOthersAvg']) / float(metrics['edits-others']))
        # metrics['revertsMaintainerPot'] = sum(revertsMaintainer)/float(metrics['edits-maintainer'])
        # metrics['revertsOthersPot'] = sum(revertsOthers)/float(metrics['edits-others'])
        # metrics['revertsPotRatio'] = sum(metrics['revertsMaintainerAvg']) / float(metrics['edits-maintainer']) / float(sum(metrics['revertsOthersAvg']) / float(metrics['edits-others']))
        
        # metrics['reintroMaintainerAvg'] = sum(reintroMaintainer)/float(metrics['edits-maintainer'])
        # metrics['reintroOthersAvg'] = sum(reintroOthers)/float(metrics['edits-others'])
        # metrics['reintroRatio'] = sum(metrics['reintroMaintainerAvg']) / float(metrics['edits-maintainer']) / float(sum(metrics['reintroOthersAvg']) / float(metrics['edits-others']))

        # metrics['selfreintroMaintainerAvg'] = sum(selfreintroMaintainer)/float(metrics['edits-maintainer'])
        # metrics['selfreintroOthersAvg'] = sum(selfreintroOthers)/float(metrics['edits-others'])
        # metrics['selfreintroRatio'] = sum(metrics['selfreintroMaintainerAvg']) / float(metrics['edits-maintainer']) / float(sum(metrics['selfreintroOthersAvg']) / float(metrics['edits-others']))

        # share of selfreintroductions of potential own tokens
        # temp['selfreintroMaintainerPot'] = [(b/float(a)) for a,b in zip(ownershipMaintainerAbs[:len(ownershipMaintainerAbs)-2], selfreintroMaintainer[1:len(selfreintroMaintainer)-1])]
        # temp['selfreintroOthersPot'] = [(b/float(c-a)) for a,b in zip(ownershipMaintainerAbs[:len(ownershipMaintainerAbs)-2], selfreintroOthers[1:len(selfreintroOthers)-1], number_tokens[:len(number_tokens)-2) if a is not 0]
        # metrics['selfreintroPotRatio'] = sum(temp['selfreintroMaintainerPot']) / float(metrics['edits-maintainer']) / float(sum(temp['selfreintroOthersPot']) / float(metrics['edits-others']))
        
        # temp['antActionsMaintainerPot'] = [(b/float(a)) for a,b in zip(ownershipMaintainerAbs[:len(ownershipMaintainerAbs)-2], antActionsMaintainer[1:len(antActionsMaintainer)-1]) if a is not 0]
        # temp['antActionsOthersPot'] = [(b/float(c-a)) for a,b in zip(ownershipMaintainerAbs[:len(ownershipMaintainerAbs)-2], antActionsOthers[1:len(antActionsOthers)-1], number_tokens[:len(number_tokens)-2]) if a is not 0]
        # metrics['antActionsRatio'] = sum(temp['antActionsMaintainerPot']) / float(metrics['edits-maintainer']) / float(sum(temp['antActionsOthersPot']) / float(metrics['edits-others']))
            
        data[title] = metrics

    data = DataFrame(data)
    data = data.transpose()
    save2CSV(data, filename)

    return data

def compute_metrics_2(data, filename):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """

    return 1

def GetOwnership(data, author_id, metric):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """
    listAuthor = []
    for revision in data:
        if author_id in revision['authors'].keys():
            listAuthor.append(revision['authors'][author_id][metric])
        else:
            listAuthor.append(0)

    return listAuthor

def plot_metrics(data, articles, maintainers, maintainers_id, FOLDER_FIGURES):
    """
    DESCRIPTION
    
    :Parameters:
        NAME : TYPE
            DESCRIPTIOIN
        
    :Return:
        DESCRIPTION
    """

    # PLOT 1
    for article in articles:
        filename = FOLDER_FIGURES+'/plot1/'+article
        PlotViewOne(data[article])
        SavePlot(filename, FILE_FORMATS)

    # PLOT 3
    for article in articles:
        filename = FOLDER_FIGURES+'/plot3/'+article
        PlotViewThree(data[article])
        SavePlot(filename, FILE_FORMATS)

    # PLOT NEW
    for index in range(len(articles)):
        article = articles[index]
        revCount = GetMetric(data[article], 'revision-count')
        giniOwnership = GetMetric(data[article], 'gini-ownership')
        giniEditorship = GetMetric(data[article], 'gini-editorship')
        ownershipMaintainerAbs = GetOwnership(data[article], maintainers_id[index], 'tokens-absolute')
        ownershipMaintainerRel = GetOwnership(data[article], maintainers_id[index], 'tokens-relative')
        
        tagMaintained = GetMetric(data[article], 'tag-maintained')
        tagMaintained = [x/float(2) for x in tagMaintained]
        
        #filename = FOLDER_FIGURES+'/new/'+article
        #DrawPlot({'antActionsMaintainer':normalize(antActionsMaintainer), 'antActionsOthers':normalize(antActionsOthers), 'selfreintroMaintainer':normalize(selfreintroMaintainer), 'selfreintroOthers':normalize(selfreintroOthers), 'addsMaintainer':normalize(addsMaintainer), 'addsOthers':normalize(addsOthers), 'tagMaintained':tagMaintained})
        #SavePlot(filename, FILE_FORMATS)
        
        # SPLIT MAINTAINER AND OTHERS
        addsMaintainer, addsOthers = SplitMaintainer(data[article], maintainers[index], 'tokens-added')
        filename = FOLDER_FIGURES+'/adds-abs/splitMO_'+article
        DrawPlot({'addsMaintainerAbs':normalize(addsMaintainer), 'addsOthersAbs':normalize(addsOthers), 'maintained':tagMaintained, 'gini-ownership':giniOwnership, 'ownership-maintainer-rel':ownershipMaintainerRel})
        SavePlot(filename, FILE_FORMATS)
        
        deletesMaintainer, deletesOthers = SplitMaintainer(data[article], maintainers[index], 'tokens-deleted')
        filename = FOLDER_FIGURES+'/deletes-abs/splitMO_'+article
        DrawPlot({'deletesMaintainerAbs':normalize(deletesMaintainer), 'deletesOthersAbs':normalize(deletesOthers), 'maintained':tagMaintained, 'gini-ownership':giniOwnership, 'ownership-maintainer-rel':ownershipMaintainerRel})
        SavePlot(filename, FILE_FORMATS)
        
        reintroMaintainer, reintroOthers = SplitMO(data[article], maintainers[index], 'tokens-reintroduced')
        filename = FOLDER_FIGURES+'/reintro-abs/splitMO_'+article
        DrawPlot({'reintroMaintainerAbs':normalize(reintroMaintainer), 'reintroOthersAbs':normalize(reintroOthers), 'maintained':tagMaintained, 'gini-ownership':giniOwnership, 'ownership-maintainer-rel':ownershipMaintainerRel})
        SavePlot(filename, FILE_FORMATS)
        
        revertsMaintainer, revertsOthers = SplitMO(data[article], maintainers[index], 'tokens-reverted') 
        filename = FOLDER_FIGURES+'/reverts-abs/splitMO_'+article
        DrawPlot({'revertsMaintainerAbs':normalize(revertsMaintainer),
        'revertsOthersAbs':Normalize(revertsOthers),
        'maintained':tagMaintained, 'gini-ownership':giniOwnership,
        'ownership-maintainer-rel':ownershipMaintainerRel})
        SavePlot(filename, FILE_FORMATS)
        
        selfreintroMaintainer, selfreintroOthers = SplitMO(data[article], maintainers[index], 'tokens-self-reintroduced')
        filename = FOLDER_FIGURES+'/selfreintro-abs/splitMO_'+article
        DrawPlot({'selfreintroMaintainerAbs':Normalize(selfreintroMaintainer), 'selfreintroOthersAbs':Normalize(selfreintroOthers), 'maintained':tagMaintained, 'gini-ownership':giniOwnership, 'ownership-maintainer-rel':ownershipMaintainerRel})
        SavePlot(filename, FILE_FORMATS)
        
        # Antagonistic Actions 
        antActionsMaintainer, antActionsOthers = SplitMO(data[article], maintainers[index], 'antagonistic-actions')
        filename = FOLDER_FIGURES+'/ant-actions-abs/splitMO_'+article
        DrawPlot({'antActionsMaintainerAbs':Normalize(antActionsMaintainer), 'antActionsOthersAbs':normalize(antActionsOthers), 'maintained':tagMaintained, 'gini-ownership':giniOwnership, 'ownership-maintainer-rel':ownershipMaintainerRel})
        SavePlot(filename, FILE_FORMATS)
        # filename = FOLDER_FIGURES+'/ant-actions-rel/splitMO_'+article
        # DrawPlot({'antActionsMaintainerRel':normalize(antActionsMaintainer), 'antActionsOthersRel':normalize(antActionsOthers), 'maintained':tagMaintained, 'gini-ownership':giniOwnership, 'ownership-maintainer-rel':ownershipMaintainerRel})
        # SavePlot(filename, FILE_FORMATS)

        ratio = []
        for i in range(len(selfreintroMaintainer)):
            if reintroMaintainer[i] == 0 or ownershipMaintainerAbs[i] == 0 or reintroOthers[i] == 0:
                ratio.append(0)
            else:
                # ratio.append(selfreintroMaintainer[i] / float(reintroMaintainer[i]) / float(ownershipMaintainerAbs[i]) / \
                    # float(selfreintroOthers[i] / float(reintroOthers[i]) / float(data['number-tokens'] - ownershipMaintainerAbs[i])))
                # ratio.append(selfreintroMaintainer[i] / float(ownershipMaintainerAbs[i]) / \
                #     float(selfreintroOthers[i] / (float(data['number-tokens'] - ownershipMaintainerAbs[i]))))
                ratio.append(selfreintroMaintainer[i] / float(ownershipMaintainerAbs[i]))

        #filename = FOLDER_FIGURES+'/ratio2Ownership/splitMO_'+article
        #DrawPlot({'maintained':tagMaintained, 'gini-ownership':giniOwnership, 'ownership-maintainer-rel':ownershipMaintainerRel, 'ratio':normalize(ratio)})
        #SavePlot(filename, FILE_FORMATS)

        filename = FOLDER_FIGURES+'/compAddsAntAct/splitMO_'+article
        DrawPlot({'antActionsMaintainerAbs':normalize(antActionsMaintainer), 'addsOthersAbs':normalize(addsOthers), 'maintained':tagMaintained, 'gini-ownership':giniOwnership, 'ownership-maintainer-rel':ownershipMaintainerRel})
        SavePlot(filename, FILE_FORMATS)

        filename = FOLDER_FIGURES+'/compSRIDel/splitMO_'+article
        drawPlot({'selfreintroMaintainerAbs':normalize(selfreintroMaintainer), 'deletesOthersAbs':normalize(deletesOthers), 'maintained':tagMaintained, 'gini-ownership':giniOwnership, 'ownership-maintainer-rel':ownershipMaintainerRel})
        SavePlot(filename, FILE_FORMATS)

# runs on start and call via shell
if __name__ == '__main__':

    articles = []
    stats = {}
    order = {}

    # read in wikipages.csv
    articles, maintainers, maintainers_id = ReadWikipages(FILE_WIKIPAGES)
    
    # import data for every article
    for article in articles:
        stats[article] = OpenJSON(FOLDER_JSON+'stats_'+article+'.json')
        order[article] = OpenJSON(FOLDER_JSON+'order_'+article+'.json')
    
    #print 'VALIDATION JSON IMPORT: ',ValidateJSONImport(stats, order, articles)
    
    count = 0
    for article in articles:
        stats[article]['maintainer-name'] = maintainers[count]
        stats[article]['maintainer-id'] = maintainers_id[count]
        stats[article]['article-title'] = articles[count]
        count += 1

    dataOne = ComputeMetrics1(stats, FOLDER_CSV+'/metrics.csv')
    #print 'VALIDATION COMPUTE METRIC: ',validate_computation(stats, order, articles)
    
    # dataTwo = ComputeMetrics2()
    #print 'VALIDATION ANALYSE METRICS: ',validate_analysis(stats, order, articles)
    
    #PlotMetrics(stats, articles, maintainers, maintainers_id, FOLDER_FIGURES)



