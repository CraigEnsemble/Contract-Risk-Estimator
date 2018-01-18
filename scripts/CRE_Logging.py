# CRE_Logging: Logging Setup for CRE Script
import logging

def setupLogging( outputDirectory, outputDataFile, logger ):

	logger.setLevel(logging.DEBUG)

	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

	logFileName = outputDirectory + "/" + outputDataFile + ".log"
	fh = logging.FileHandler(logFileName)
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(formatter)
	logger.addHandler(fh)

	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	ch.setFormatter(formatter)
	logger.addHandler(ch)
	
	# Add some spaces below command for readability
	print( "\n\n")
	logger.debug("Outputting results,artifacts, and logs to: " + outputDirectory)
	logger.debug("Opening log file: " + logFileName)
	print( "\n" )
	