# CRE_PreProcessor: Preprocessing script to read project and SOW Contract data and save into data model
# Type CRE_Preprocessor -h on the command line for input help

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
from CRE_DataModelPackager import saveDataModel, saveDataFrame


# Create logging instance
logger = logging.getLogger(CRE_Config.LOGGER_NAME)

# Find and validate script input and output resources
sowLocation, outputDirectory, projectDataFile, outputDataFile = preProcessorInputs( sys.argv, logger )

# Set up logging configuration
setupLogging( outputDirectory, outputDataFile, logger )

# Read project actuals data from TJ dump
projectDataList, projectDataFrame = readProjectDataFile( projectDataFile, logger )
#pprint.pprint( projectDataList )

# Process sow contract documents into data objects
sowDataDict = processContracts( sowLocation, logger )

# Match and combine project data object with sow contract object
combinedDataList = projectDataMatcher( sowDataDict, projectDataList, logger )
#print( combinedDataList )

# Save the combined data model to disk for any future use
dataModelFilename = saveDataModel( combinedDataList, outputDirectory, outputDataFile, logger )

dataFrameFilename = saveDataFrame( projectDataFrame, outputDirectory, outputDataFile, logger )

print("\n")
logger.debug("CRE_PreProcessor exiting normally..." )	