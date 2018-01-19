# CRE_ModelController: Control the stages to build a contract risk estimation machine learning model from input data model

#imports
import sys
import logging

import CRE_Config
from CRE_InputParser import modelControllerInputs
from CRE_Logging import setupLogging
from CRE_DataModelPackager import readDataModel, readDataFrame
from CRE_ModelLibrary import simpleModel

# Create logging instance
logger = logging.getLogger(CRE_Config.LOGGER_NAME)

# Read in validated input data model from command line input
dataModelFilename, dataFrameFilename, outputDirectory, outputDataFile = modelControllerInputs( sys.argv, logger)

# Set up logging configuration
setupLogging( outputDirectory, outputDataFile, logger )

# Load saved data model into data model list
dataModelList = readDataModel( dataModelFilename, logger)

# Load saved data frame
allProjectDataFrame = readDataFrame( dataFrameFilename, logger )

# Run simple model test
testResults = simpleModel( dataModelList, allProjectDataFrame, logger )

print("\n")
logger.debug("CRE_ModelController exiting normally..." )