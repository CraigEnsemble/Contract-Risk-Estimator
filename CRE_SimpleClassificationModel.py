# CRE_SimpleClassificationModel: Steps to build and run and test a simple risk classification model

import logging

import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

from CRE_RiskClassifier import generateRiskDataFrame, classifyProjectRisk, viewRiskData
from CRE_ModelLibrary import processInputDataFrameValues

def simpleClassificationModel( inputDataModel, inputDataFrame, logger ):
	
	print( "\n" )
	logger.debug("Initializing simple classification model" )
	print( "\n" )
	
	classifiedRiskDataFrame = generateRiskDataFrame( inputDataFrame )
	
	# Uncomment to view graphs of project data
	#viewRiskData( riskDataFrame[ ['Budget', 'FinalSpent', 'AbsoluteTimeDelta', 'RelativeExpenditure'] ])
	
	print( classifiedRiskDataFrame.shape )
	#print( classifiedRiskDataFrame.head(20) )
	print( classifiedRiskDataFrame.describe() )
	
	# class distribution
	print( classifiedRiskDataFrame.groupby('Classification').size())
	
	dataParametersFrame = processInputDataFrameValues( inputDataFrame, logger)
	
	# Make this a merge to join only the rows that have classified outputs
	modelFrame = pandas.merge( left=dataParametersFrame, right=classifiedRiskDataFrame)
	
	print( modelFrame )
	
	dataArray = modelFrame.values
	
	# Input data dimensions
	trainingData = dataArray[:, 1:4]
	
	# Output classification
	trainingScores = dataArray[:, 4]
	
	lab_enc = preprocessing.LabelEncoder()
	encodedTraining = lab_enc.fit_transform( trainingScores )
	
	validation_size = 0.20
	seed = 7
	X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(trainingData, 
																					encodedTraining, 
																					test_size=validation_size, 
																					random_state=seed)
	
		# Test options and evaluation metric
	seed = 6
	scoring = 'accuracy'
	
	# Spot Check Algorithms
	models = []
	models.append(('LR', LogisticRegression()))
	models.append(('LDA', LinearDiscriminantAnalysis()))
	models.append(('KNN', KNeighborsClassifier()))
	models.append(('CART', DecisionTreeClassifier()))
	models.append(('NB', GaussianNB()))
	models.append(('SVM', SVC()))
	
	# evaluate each model in turn
	results = []
	names = []
	for name, model in models:
		kfold = model_selection.KFold(n_splits=10, random_state=seed)
		
		cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
		results.append(cv_results)
		names.append(name)
		msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
		print(msg)
		
	# Make predictions on validation dataset
	#knn = KNeighborsClassifier()
	#knn.fit(X_train, Y_train)
	#predictions = knn.predict(X_validation)
	lda = LinearDiscriminantAnalysis()
	lda.fit( X_train, Y_train )
	predictions = lda.predict( X_validation )
	print(accuracy_score(Y_validation, predictions))
	print(confusion_matrix(Y_validation, predictions))
	print(classification_report(Y_validation, predictions))
	
	
	return results