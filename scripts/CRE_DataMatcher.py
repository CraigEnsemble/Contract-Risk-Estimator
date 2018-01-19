# CRE_DataMatcher: Match project data entries to SOW contract data with project names/document titles

import os
import logging
import re
from collections import OrderedDict

titleMatchSplitCharacters = "[:_ \-&]"

def stringWordMatcher( documentTitleString, projectNameString ):
	
	documentBasename = os.path.splitext( documentTitleString )[0]
	
	documentTitleSplit = re.split( titleMatchSplitCharacters, documentBasename )
	
	#Break project name into components
	projectNameSplit = re.split( titleMatchSplitCharacters, projectNameString )
	
	nameWordMatchCount = 0
			
	for projectNameWord in projectNameSplit:
				
		for documentTitleWord in documentTitleSplit:
					
			if projectNameWord.lower() == documentTitleWord.lower():
				nameWordMatchCount += 1
		
	return nameWordMatchCount
	

def projectDataMatcher( sowDataList, projectDataList, logger ):

	print( "\n" )
	logger.debug("Matching input data sources..." )
	print( "\n" )
	
	combinedDataList = []
	matchedCount, unmatchedCount = 0, 0;
	
	for sowItem in sowDataList:
		
		matchedProjectDict = OrderedDict()
		maxNameWordMatchCount = 0
		documentTitle = sowItem["title"]
		
		for projectEntryDict in projectDataList:
			
			nameWordMatchCount = stringWordMatcher( documentTitle, projectEntryDict[ "Project Name"])		
			
			if nameWordMatchCount > maxNameWordMatchCount:
				maxNameWordMatchCount = nameWordMatchCount
				matchedProjectDict = projectEntryDict
			
		if matchedProjectDict:
			logger.debug("Document: " + documentTitle + " matched with project: " + matchedProjectDict["Project Name"])
			
			sowItem.update(matchedProjectDict)
			
			matchedCount += 1;
			combinedDataList.append(sowItem)
		else:
			logger.warning("SOW Contract: " + documentTitle + " was unable to find a matching project entry")
			unmatchedCount +=1;
		
	logger.debug("Match Summary: " + str(matchedCount) + " projects matched, " + str(unmatchedCount) + " projects unmatched")
	
	return combinedDataList
		