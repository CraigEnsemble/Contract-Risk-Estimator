# CRE_Controller: Controller Script for executing CRE steps
# Type CRE_Controller -h on the command line for input help

# Imports
import sys
import os
import logging

import CRE_Config
from CRE_InputParser import preProcessorInputs
from CRE_Logging import setupLogging
from CRE_ProjectDataReader import readProjectDataFile
from CRE_ContractProcessor import processContracts
from CRE_DataMatcher import projectDataMatcher
import CRE_DataModelPackager
from CRE_ModelLibrary import simpleModel


# Create logging instance
logger = logging.getLogger(CRE_Config.LOGGER_NAME)

# Find and validate script input and output resources
sowLocation, outputDirectory, projectDataFile, outputDataFile = preProcessorInputs( sys.argv, logger )

# Set up logging configuration
setupLogging( outputDirectory, outputDataFile, logger )

# Read project actuals data from TJ dump
projectDataList, projectDataFrame = readProjectDataFile( projectDataFile, logger )

# Process sow contract documents into data objects
sowDataDict = processContracts( sowLocation, logger )

# Match and combine project data object with sow contract object
combinedDataList = projectDataMatcher( sowDataDict, projectDataList, logger )

# Save the combined data model to disk for any future use
dataModelFilename = saveDataModel( combinedDataList, outputDirectory, outputDataFile, logger )

# Technically don't need to do this, just verifying that we can dump/load data correctly
dataModelList = readDataModel( dataModelFilename, logger)
#print( dataModelList )

testResults = simpleModel( dataModelList, logger )

print("\n\n")
logger.debug("CRE_Controller exiting normally..." )	
