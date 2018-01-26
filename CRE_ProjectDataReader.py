# CRE_ProjectDataReader: Process project data TJ dump csv information into data object

import csv
import pandas
import logging

def readProjectDataFile( projectDataFile, logger ):
	
	logger.debug("Reading project data from: " + projectDataFile)
	print( "\n" )
	
	projectDataCsvReader = csv.DictReader( open( projectDataFile, 'r'))
	
	projectDataList = []
	for projectLine in projectDataCsvReader:
		projectDataList.append( projectLine )
		
	projectDataFrame = pandas.read_csv( projectDataFile )
		
	return projectDataList, projectDataFrame