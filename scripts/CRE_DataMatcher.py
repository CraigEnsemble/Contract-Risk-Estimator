# CRE_DataMatcher: Match project data entries to SOW contract data with project names/document titles

import os
import logging
import re
from collections import OrderedDict

titleMatchSplitCharacters = "[:_ \-&]"

def projectDataMatcher( sowDataList, projectDataList, logger ):

	print( "\n" )
	logger.debug("Matching input data sources..." )
	print( "\n" )
	
	combinedDataList = []
	
	for sowItem in sowDataList:
		
		documentTitle = sowItem["title"]
			
		documentBasename = os.path.splitext( documentTitle )[0]
		
		# SOW Contract Titles seem to be split on "_"...assume this for now
		documentTitleSplit = re.split( titleMatchSplitCharacters, documentBasename)
		
		maxNameWordMatchCount = 0
		matchedProjectDict = OrderedDict()
		
		for projectEntryDict in projectDataList:
			projectName = projectEntryDict[ "Project Name"]
			
			#Break project name into components
			projectNameSplit = re.split( titleMatchSplitCharacters, projectName)
			
			nameWordMatchCount = 0
			
			for projectNameWord in projectNameSplit:
				
				for documentTitleWord in documentTitleSplit:
					
					if projectNameWord.lower() == documentTitleWord.lower():
						nameWordMatchCount += 1
						
			
			if nameWordMatchCount > maxNameWordMatchCount:
				maxNameWordMatchCount = nameWordMatchCount
				matchedProjectDict = projectEntryDict
			
		if matchedProjectDict:
			logger.debug("Document: " + documentTitle + " matched with project: " + matchedProjectDict["Project Name"])
			
			sowItem.update(matchedProjectDict)
			
			combinedDataList.append(sowItem)
		else:
			logger.warning("SOW Contract: " + documentTitle + " was unable to find a matching project entry")
		
		
	return combinedDataList
		