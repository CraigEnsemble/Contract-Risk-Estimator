# CRE_ModelLibrary: Test sandbox for creating learning models

import pandas
import numpy as np
import re

from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
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

import CRE_Config
from CRE_DataModelPackager import readDataFrame

def extractClientProjectCount( inputDataFrame, dataParametersFrame ):
	
	# Get project name/title acronym
	dataParametersFrame[ 'projectCount' ] = inputDataFrame['Project Name'].str.split( ":" ).str.get(0)
	
	# Parse out client project number count, 1 if not specified
	dataParametersFrame[ 'projectCount' ] = np.where( dataParametersFrame['projectCount'].str.count( r'\d+') == 0,
												1, dataParametersFrame['projectCount'].str.findall( r'[1-9][0-9]*').str.get(0))
	
	# Convert to int
	dataParametersFrame[ 'projectCount' ] = dataParametersFrame[ 'projectCount' ].astype(int)
	
	#print ( dataParametersFrame[ 'projectCount'] )
	
	return dataParametersFrame

def extractEncodeProjectPM( inputDataFrame, dataParametersFrame ):
	
	# Convert input into a category
	dataParametersFrame['pm'] = inputDataFrame['Manager'].astype('category')
	
	# Store PM category as an encoded integer
	dataParametersFrame['pm'] = dataParametersFrame['pm'].cat.codes
	
	#print ( dataParametersFrame['pm'] )
	
	return dataParametersFrame

def processInputDataFrameValues( inputDataFrame, logger):
	
	dataParametersFrame = pandas.DataFrame( inputDataFrame['Project Name'] )
	
	# Extract client project number
	dataParametersFrame = extractClientProjectCount( inputDataFrame, dataParametersFrame )
	
	# Extract and encode PM data
	dataParametersFrame = extractEncodeProjectPM( inputDataFrame, dataParametersFrame )
	
	return dataParametersFrame

# Reference Test
def irisModelTest():
	
	# Load dataset
	#url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
	names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
	#dataset = pandas.read_csv(url, names=names)
	dataset = pandas.read_csv( "allData/iris.data.csv", names=names )
	
	# shape
	print(dataset.shape)
	
	#head
	print( dataset.head(20) )
	
	# descriptions
	print( dataset.describe() )
		  
	# class distribution
	print(dataset.groupby('class').size())
	
	# box and whisker plots
	dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
	plt.show()

	# histograms note distribution types
	dataset.hist()
	plt.show()
	
	# scatter plot matrix
	scatter_matrix(dataset)
	plt.show()
	
	# Split-out validation dataset
	array = dataset.values
	X = array[:,0:4]
	Y = array[:,4]
	validation_size = 0.20
	seed = 7
	X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
	
	# Test options and evaluation metric
	seed = 7
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
		
	# Compare Algorithms
	fig = plt.figure()
	fig.suptitle('Algorithm Comparison')
	ax = fig.add_subplot(111)
	plt.boxplot(results)
	ax.set_xticklabels(names)
	plt.show()
	
	# Make predictions on validation dataset
	knn = KNeighborsClassifier()
	knn.fit(X_train, Y_train)
	predictions = knn.predict(X_validation)
	print(accuracy_score(Y_validation, predictions))
	print(confusion_matrix(Y_validation, predictions))
	print(classification_report(Y_validation, predictions))