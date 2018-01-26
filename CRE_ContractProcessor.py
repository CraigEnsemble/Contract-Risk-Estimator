# CRE_ContractProcessor: Convert the input SOW contracts into data objects for analysis

import os
import subprocess
import fnmatch
import PyPDF2
import docx
import docx2txt
import logging
from collections import OrderedDict
from shutil import which

def convertDocToDocx( inputDocument, sowLocation, logger ):
	logger.debug( inputDocument + " is a .doc, searching for docx version...")
	outputDocument = ""
				
	# Check if there's already a converted version in the docx directory
	baseFileName = os.path.splitext( inputDocument )[0]
	if os.path.exists( sowLocation + baseFileName + ".docx" ):
		logger.debug( sowLocation + baseFileName + ".docx: Has been found")
		outputDocument = sowLocation + baseFileName + ".docx"
		
		# If it exists in the same directory just skip for now
		return()
					
	else:
		logger.debug( sowLocation + baseFileName + ".docx: Not found")

		if which( "soffice" ):
			#This isn't working right, just convert manually for now
			logger.debug( "Converting " + baseFileName + " to .docx...")
			subprocess.call(['soffice', '--headless', '--convert-to', 'docx', inputDocument])
			return()
		else:
			logger.warning( "LibreOffice executable not on environment path, skipping " + baseFileName)
			return()

def processContracts( sowLocation, logger ):
	
	logger.debug("Processing SOW contracts in: " + sowLocation)	
	print("\n")
	
	sowDirFileList = os.listdir( sowLocation )

	wordPattern = "*.doc*"
	pdfPattern = "*.pdf*"

	sowDataList = []

	for sowFile in sowDirFileList:
		
		documentText = ""
	
		# Process pdf contracts into PyPDF2 objects
		if fnmatch.fnmatch( sowFile, pdfPattern ):
			inputPDFFileObj = open( sowLocation + "/" + sowFile, 'rb' )
			pdfReader = PyPDF2.PdfFileReader( inputPDFFileObj )

			for pageNum in range( pdfReader.numPages ):
				pdfPage = pdfReader.getPage( pageNum )
				documentText = documentText + pdfPage.extractText()
			
			sowDataEntryDict = OrderedDict( [("title", sowFile),
											 #("documentObject", pdfReader), Can't pickle, remove for now
											 ("documentText", documentText) ])
			
			sowDataList.append( sowDataEntryDict )
			#sowDataList.append(pdfReader)
			logger.debug("Processed SOW Contract: " + sowFile)
		
		# Process Word docs into Document objects	
		elif fnmatch.fnmatch( sowFile, wordPattern ):
		
			# Convert old word docs to docx for docx lib
			if sowFile.endswith('.doc'):
				sowFile = convertDocToDocx( sowFile, sowLocation, logger )
            
			# If the Word Doc is valid...
			if sowFile:
				
				sowDoc = docx.Document( sowLocation + "/" + sowFile )
				documentText = docx2txt.process( sowLocation + "/" + sowFile )
				
				sowDataEntryDict = OrderedDict( [ ("title", sowFile),
												 #("documentObject", sowDoc ), Can't pickle, remove for now
												 ("documentText", documentText)])
					
				sowDataList.append( sowDataEntryDict )
				#sowDataList.append(sowDoc)
				logger.debug("Processed SOW Contract: " + sowFile)

				#titleTest = sowDoc.core_properties.title
				
		else:
			logger.warning( "Input SOW file: " + sowFile + " is not a valid format")
				
	return sowDataList
		