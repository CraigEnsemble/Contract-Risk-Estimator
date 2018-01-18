# CRE_Controller: Controller Script for executing CRE steps
# Type CRE_Controller -h on the command line for input help

# Imports
import sys
import os
import logging
import pprint

from CRE_InputParser import inputPopulator
from CRE_Logging import setupLogging
from CRE_ProjectDataReader import readProjectData
from CRE_ContractProcessor import processContracts
from CRE_DataMatcher import projectDataMatcher
from CRE_DataModelPackager import saveDataModel, readDataModel


# Create logging instance
loggerName = "CRE_Logger"
logger = logging.getLogger(loggerName)

# Find and validate script input and output resources
sowLocation, outputDirectory, projectDataFile, outputDataFile = inputPopulator( sys.argv, logger )

# Set up logging configuration
setupLogging( outputDirectory, outputDataFile, logger )

# Read project actuals data from TJ dump
projectDataList = readProjectData( projectDataFile, logger )
#pprint.pprint( projectDataList )

# Process sow contract documents into data objects
sowDataDict = processContracts( sowLocation, logger )

# Match and combine project data object with sow contract object
combinedDataList = projectDataMatcher( sowDataDict, projectDataList, logger )
#print( combinedDataList )

# Save the combined data model to disk for any future use
dataModelFilename = saveDataModel( combinedDataList, outputDirectory, outputDataFile, logger )

# Technically don't need to do this, just verifying that we can dump/load data correctly
dataModelList = readDataModel( dataModelFilename, logger)
#print( dataModelList )



print("\n\n")
logger.debug("CRE_Controller exiting normally..." )	
