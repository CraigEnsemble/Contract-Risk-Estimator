# CRE_DataModelPackager: Package the complete data model to reversible serialized disk save

import pickle

def saveDataModel( dataModelList, outputDirectory, outputDataFile, logger ):
	
	dataModelFilename = outputDirectory + outputDataFile + ".dataModel"

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
	
	