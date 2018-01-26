# CRE_InputParser: Input population and validation for CRE script

import os
from datetime import datetime
import argparse
import fnmatch
import logging

import CRE_Config

def invalidInputError( inputArg, logger ):
	
	logger.error("\nInput argument " + inputArg + " is not valid")
	exit();

def preProcessorInputs( cliArgs, logger ):
	
	cwd = os.getcwd()
	
	# Default Values
	sowLocation = cwd
	outputDirectory = cwd + CRE_Config.DEFAULT_OUTPUT_DIRECTORY
	projectDataFile = CRE_Config.DEFAULT_PROJECT_DATA_FILE
	outputDataFile = CRE_Config.PREPROCESS_OUTPUT_FILENAME
	
	# Set up input argument parsing
	parser = argparse.ArgumentParser(description='Preprocess SOW contract and linked actuals data.')
		
	parser.add_argument( '-s', '--sowdir', dest='sowLocation', action='store', help='directory containing SOW docs')
	parser.add_argument( '-d', '--outdir', dest='outputDirectory', action='store', help='directory to store output results')
	parser.add_argument( '-i', '--infile', dest='projectDataFile', action='store', help='datafile containing project actuals data')
	parser.add_argument( '-o', '--outfile', dest='outputDataFile', action='store', help='processed output file name')
	
	if( len(cliArgs) > 1):
	
		args = parser.parse_args()

		if( args.sowLocation ):
			sowLocation = args.sowLocation
		if( args.outputDirectory ):
			outputDirectory = args.outputDirectory
		if( args.projectDataFile ):
			projectDataFile = args.projectDataFile
		if( args.outputDataFile ):
			outputDataFile = args.outputDataFile
			
	if not os.path.isdir(sowLocation):
		parser.print_help()
		invalidInputError( "sowLocation", logger )
	if not os.path.exists( outputDirectory ):
		logger.debug("Creating output directory: " + outputDirectory)
		os.makedirs( outputdirectory)
	if not os.path.exists( projectDataFile ):
		parser.print_help()
		invalidInputError( "projectDataFile", logger )
	
	return sowLocation, outputDirectory, projectDataFile, outputDataFile

def modelControllerInputs( cliArgs, logger ):
	
	cwd = os.getcwd()
	
	dataModelFilename = ""
	dataFrameFilename = ""
	outputDirectory = cwd + CRE_Config.DEFAULT_OUTPUT_DIRECTORY
	outputDataFile = CRE_Config.MODEL_OUTPUT_FILENAME
	
	parser = argparse.ArgumentParser(description='Read saved data model to generate CRE learning models')
	parser.add_argument( '-m', '--modelfile', dest='dataModelFilename', action='store', help='file containing input data model')
	parser.add_argument( '-f', '--dffile', dest='dataFrameFilename', action='store', help='file containing input data frame')
	parser.add_argument( '-d', '--outdir', dest='outputDirectory', action='store', help='directory to store output results')
	parser.add_argument( '-o', '--outfile', dest='outputDataFile', action='store', help='processed output file name')

	if( len(cliArgs) > 1):
	
		args = parser.parse_args()
		
		if( args.dataModelFilename ):
			dataModelFilename = args.dataModelFilename
		if( args.dataFrameFilename ):
			dataFrameFilename = args.dataFrameFilename
		if( args.outputDirectory ):
			outputDirectory = args.outputDirectory
		if( args.outputDataFile ):
			outputDataFile = args.outputDataFile
	
	# If no model specified take a look in current directory for simple no arg use case
	if not os.path.exists( dataModelFilename ):
		
		modelPattern = "*.dataModel"
		pwdList = os.listdir( cwd )
		
		for file in pwdList:
			if fnmatch.fnmatch( file, modelPattern ):
				dataModelFilename = file
				
		if not os.path.exists( dataModelFilename ):
			invalidInputError( "dataModelFilename", logger )
			
	# If no dataFrame specified take a look in current directory for simple no arg use case
	if not os.path.exists( dataFrameFilename ):
		
		framePattern = "*.dataFrame*"
		pwdList = os.listdir( cwd )
		
		for file in pwdList:
			if fnmatch.fnmatch( file, framePattern ):
				dataFrameFilename = file
				
		if not os.path.exists( dataFrameFilename ):
			invalidInputError( "dataFrameFilename", logger )
		
	if not os.path.exists( outputDirectory ):
		logger.debug("Creating output directory: " + outputDirectory)
		os.makedirs( outputdirectory)
		
	return dataModelFilename, dataFrameFilename, outputDirectory, outputDataFile
		
				
				
		
		
		
		
			