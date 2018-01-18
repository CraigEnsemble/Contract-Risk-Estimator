# CRE_InputParser: Input population and validation for CRE script

import os
from datetime import datetime
import argparse
import logging

def invalidInputError( inputArg, logger ):
	
	logger.error("\n\nInput argument " + inputArg + " is not a valid")
	exit();

def inputPopulator( cliArgs, logger ):
	
	cwd = os.getcwd()
	
	# Default Values
	sowLocation = cwd
	outputDirectory = cwd + "/output." + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	projectDataFile = "ProjectBudget July to Dec 2017 csv.csv"
	outputDataFile = "CRE_Summary." + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ".csv"
	
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
		invalidInputError( sowLocation, logger )
	if not os.path.exists( outputDirectory ):
		logger.debug("Creating output directory: " + outputDirectory)
		os.makedirs( outputdirectory)
	if not os.path.exists( projectDataFile ):
		parser.print_help()
		invalidInputError( projectDataFile, logger )
	
	return sowLocation, outputDirectory, projectDataFile, outputDataFile