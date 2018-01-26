# CRE_DataModelPackager: Package the complete data model to reversible serialized disk save

import pickle
import pandas

import CRE_Config

def saveDataModel( dataModelList, outputDirectory, outputDataFile, logger ):
	
	dataModelFilename = outputDirectory + outputDataFile + CRE_Config.DEFAULT_MODEL_EXTENSION

	print( "\n" )
	logger.debug("Saving CRE data model into file: " + dataModelFilename )
	print( "\n" )
	
	fh = open( dataModelFilename, "bw" )
	pickle.dump( dataModelList, fh )
	fh.close
	
	return dataModelFilename
	
def readDataModel( inputDataModelFile, logger ):
	
	print( "\n" )
	logger.debug("Reading CRE data model from file: " + inputDataModelFile )
	print( "\n" )
	
	fh = open( inputDataModelFile, "rb" )
	dataModel = pickle.load( fh )
	fh.close
	
	return dataModel

def saveDataFrame( inputDataFrame, outputDirectory, outputDataFile, logger ):
	
	dataFrameFilename = outputDirectory + outputDataFile + CRE_Config.DEFAULT_DATA_FRAME_EXTENSION

	print( "\n" )
	logger.debug("Saving CRE data frame into file: " + dataFrameFilename )
	print( "\n" )
	
	inputDataFrame.to_csv( dataFrameFilename )
	
	return dataFrameFilename

def readDataFrame( inputDataFrameFile, logger ):
	
	print( "\n" )
	logger.debug("Reading CRE data frame from file: " + inputDataFrameFile )
	print( "\n" )
	
	outputDataFrame = pandas.read_csv( inputDataFrameFile )

	return outputDataFrame
	
	