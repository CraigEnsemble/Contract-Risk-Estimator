# CRE_ModelLibrary: Test sandbox for creating learning models

import pandas
import numpy
from pandas.tools.plotting import scatter_matrix
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

from CRE_DataModelPackager import readDataFrame

def classifyRisk( inputDataModel, inputDataFrame, logger ):
	
	#fullProjectDataList = readProjectData( "projectReports/ProjectBudget July to Dec 2017 csv.csv" )
	#Fields = ["Manager","Project Name","Budget","Billable Spent","Total Spent","Remaining","% Billable","% Spent","Projected","Delta","Due Date"]
	
	#allProjectDataFrame = pandas.read_csv( "projectReports/ProjectBudget July to Dec 2017 csv.csv")
	
	
	#print( allProjectDataFrame.shape )
	#print( allProjectDataFrame.head(20) )
	#print( allProjectDataFrame.describe() )
	
	# Remove commas from numeric data columns we're calculating from
	inputDataFrame['Budget'] = inputDataFrame['Budget'].str.replace(',','')
	inputDataFrame['Total Spent'] = inputDataFrame['Budget'].str.replace(',','')
	inputDataFrame['Projected'] = inputDataFrame['Projected'].str.replace(',','')
	
	# Convert string columns to floats
	inputDataFrame['Budget'] = inputDataFrame['Budget'].astype(float)
	inputDataFrame['Total Spent'] = inputDataFrame['Total Spent'].astype(float)
	inputDataFrame['Projected'] = inputDataFrame['Projected'].astype(float)
	
	# Generate new column with comparable total expenditures
	inputDataFrame['Final Spent'] = numpy.where(inputDataFrame['Projected'] == 0, 
												inputDataFrame['Total Spent'],
												inputDataFrame['Projected'])
	
	# Generate a new column of absolute budget difference
	#allProjectDataFrame[]
	
	print( inputDataFrame['Final Spent'])
	
	budgetMean = inputDataFrame['Budget'].mean()
	print( budgetMean )

	
#	budgetTotal = 0
#	
#	for projectItem in fullProjectDataList:
#		return
#		#budgetTotal += float(projectItem["Budget"].replace(",",""))
#	
#	for projectItem in inputDataModel:
#		
#		riskClass = -1
#		
#		projectedRemainingHours = projectItem["Projected"]
#		
#		# Something in the model storing process adds the commas, remove them for cast
#		budgetHours = float(projectItem["Budget"].replace(",",""))
#		finalHoursSpent = float(projectItem["Total Spent"].replace(",",""))
#		
#		# For incomplete projects use the projected
#		if not float(projectedRemainingHours) == 0:
#			finalHoursSpent = float(projectItem["Projected"].replace(",",""))
#
#		absoluteBudgetDifference = budgetHours - finalHoursSpent
#		relativeBudgetDifference = budgetHours/finalHoursSpent
#		
#		print( projectItem["Project Name"])
#		print ( absoluteBudgetDifference )
#		print ( relativeBudgetDifference )
#		
#		
#		
#		#riskProportion = 
			
			

def simpleModel( inputDataModel, inputDataFrame, logger ):
	
	calculatedRiskList = classifyRisk( inputDataModel, inputDataFrame, logger )
	
	return

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