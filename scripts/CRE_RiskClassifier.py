#CRE_RiskClassifier.py: Library for the risk classification methods and algorithms

import pandas
import numpy as np

from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt

import CRE_Config

def viewRiskData( riskDataFrame ):
	
	#print ( riskDataFrame )
	
	riskDataFrame.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
	plt.show()
	
	riskDataFrame.hist()
	plt.show()
	
	# scatter plot matrix
	scatter_matrix(riskDataFrame)
	plt.show()
	
	
def filterRiskDataOutliers( inputDataFrame ):
	
	# Filtering method, pretty aggressive right now, sequentially drops everything outside of STD_DEV_FILTER
	# This is necessary for now because we want a relatively gaussian distribution and some project outliers are very large
	inputDataFrame = inputDataFrame[np.abs(inputDataFrame.Budget-inputDataFrame.Budget.mean())<=
								  (CRE_Config.STD_DEV_FILTER*inputDataFrame.Budget.std())]
	inputDataFrame = inputDataFrame[np.abs(inputDataFrame.FinalSpent-inputDataFrame.FinalSpent.mean())<=
								  (CRE_Config.STD_DEV_FILTER*inputDataFrame.FinalSpent.std())]
	inputDataFrame = inputDataFrame[np.abs(inputDataFrame.AbsoluteTimeDelta-inputDataFrame.AbsoluteTimeDelta.mean())<=
								  (CRE_Config.STD_DEV_FILTER*inputDataFrame.AbsoluteTimeDelta.std())]
	inputDataFrame = inputDataFrame[np.abs(inputDataFrame.RelativeExpenditure-inputDataFrame.RelativeExpenditure.mean())<=
								  (CRE_Config.STD_DEV_FILTER*inputDataFrame.RelativeExpenditure.std())]
	
	return inputDataFrame


def generateRiskDataFrame( inputDataFrame ):
	
	# Create a new dataframe with clean budget floats
	riskDataFrame = pandas.DataFrame( inputDataFrame['Project Name'] )
	
	riskDataFrame['Budget'] = inputDataFrame['Budget'].str.replace(',','').astype(float)
	
	# Standardize a new column with full project estimated expenditure
	riskDataFrame['FinalSpent'] = np.where( inputDataFrame['Projected'].str.replace(',','').astype(float) == 0, 
											inputDataFrame['Total Spent'].str.replace(',','').astype(float),
											inputDataFrame['Projected'].str.replace(',','').astype(float) )
	
	# Calculate absolute and relative delta columns
	riskDataFrame['AbsoluteTimeDelta'] = riskDataFrame['Budget'].sub( riskDataFrame['FinalSpent'])
	riskDataFrame['RelativeExpenditure'] = riskDataFrame['Budget'].div( riskDataFrame['FinalSpent'])
	
	# Remove project data with invalid infinite or not applicable values, these inputs will ruin our calculations
	riskDataFrame = riskDataFrame[~riskDataFrame.isin([np.nan, np.inf, -np.inf]).any(1)]
	
	# Normalize relative expenditure
	riskDataFrame['RelativeExpenditure'] = riskDataFrame['RelativeExpenditure'].sub(1)
	
	# Filter out projects with extreme deltas....most likely ongoing internal projects
	riskDataFrame = filterRiskDataOutliers( riskDataFrame )
	
	# Generate risk classification column
	riskDataFrame = classifyProjectRisk( riskDataFrame )
	
	# Slice out intermediate output calculations, just return classification
	riskDataFrame = riskDataFrame.drop(['FinalSpent', 'AbsoluteTimeDelta', 'RelativeExpenditure'], axis=1)
	
	return riskDataFrame

# Next phase is to remove the language bins, and use configurable dynamic bin sizing
def classifyProjectRisk( inputRiskDataFrame ):
	
	binCount = CRE_Config.BIN_COUNT
	binStepSizePercentage = CRE_Config.BIN_STEPSIZE_PERCENTAGE
	
	# If number of bins is < 3 then this is a poor classifier, throw an error for these edge cases
	if binCount < 3:
		logger.error("\nInput bin count: " + CRE_Config.BIN_COUNT + " is not valid")
		
	startInterval = 0;
	endInterval = 0;
	
	inputRiskDataFrame[ 'Classification'] = ""
	
	# If odd bin size center first bin on either side of 0
	if CRE_Config.BIN_COUNT % 2 == 1:
		startInterval = binStepSizePercentage/2
		endInterval = -1 * binStepSizePercentage/2
		
		# Classify the well estimated projects
		inputRiskDataFrame[ 'Classification' ] = np.where(  ( ( inputRiskDataFrame.RelativeExpenditure < 
															  startInterval/100 ) &
															( inputRiskDataFrame.RelativeExpenditure > 
															 endInterval/100 ) ),
														  str(endInterval) + " to " + str(endInterval) + "%", 
														 inputRiskDataFrame.Classification )
		endInterval = startInterval
		binCount -= 1;
		
	while binCount > 0:
		
		startInterval = endInterval
		
		# Edge bins, collect the rest of the samples
		if binCount == 2:
			endInterval = np.inf
		else:
			endInterval = startInterval + binStepSizePercentage
			
		inputRiskDataFrame[ 'Classification'] = np.where(  ( ( inputRiskDataFrame.RelativeExpenditure >= 
															  startInterval/100 ) &
															( inputRiskDataFrame.RelativeExpenditure < 
															 endInterval/100 ) ), 
														 str(startInterval) + "% to " + str(endInterval) + "%",
														 inputRiskDataFrame.Classification  )
		
		inputRiskDataFrame[ 'Classification'] = np.where(  ( ( inputRiskDataFrame.RelativeExpenditure <= 
															  -1 * startInterval/100 ) &
															( inputRiskDataFrame.RelativeExpenditure > 
															 -1 * endInterval/100 ) ), 
														 "-" + str(startInterval) + "% to -" + str(endInterval) + "%",
														 inputRiskDataFrame.Classification  )
		
		binCount -= 2
		
	#print ( inputRiskDataFrame[ 'Classification'] )
	#print( inputRiskDataFrame.groupby('Classification').size())
	
	# Convert input into a category
	inputRiskDataFrame['Classification'] = inputRiskDataFrame['Classification'].astype('category')
	
	# Store PM category as an encoded integer
	inputRiskDataFrame['Classification'] = inputRiskDataFrame['Classification'].cat.codes
	#print( inputRiskDataFrame.groupby('Classification').size())
	
	return inputRiskDataFrame